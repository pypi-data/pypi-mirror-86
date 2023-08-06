import asyncio.subprocess
import contextlib
import itertools
import json
import logging
import os
import signal
import string
import tempfile
import time
from datetime import datetime

import jsonpyth

from . import playbook, proctree, procfile, procrec, procret, utility


__all__ = 'CommandError', 'query', 'record', 'plot', 'watch', 'play'

logger = logging.getLogger(__package__)


class CommandError(Exception):
    """Generic command error."""


def query(
    procfile_list,
    output_file,
    delimiter=None,
    indent=None,
    query=None,
    sql_query=None,
    environment=None,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    tree = proctree.Tree(readers)
    result = tree.get_root()

    if environment:
        evaluated = utility.evaluate(environment)
        query = string.Template(query or '').safe_substitute(evaluated)
        sql_query = string.Template(sql_query or '').safe_substitute(evaluated)

    if query:
        try:
            result = jsonpyth.jsonpath(result, query, always_return_list=True)
        except jsonpyth.JsonPathSyntaxError as ex:
            raise CommandError(f'JSONPath error: {ex}') from ex

    if sql_query:
        with tempfile.NamedTemporaryFile() as f:
            with procrec.SqliteStorage(f.name, procfile_list, utility.get_meta()) as store:
                store.record(time.time(), proctree.flatten(result, procfile_list))
                try:
                    result = procret.query(f.name, procret.Query(sql_query, None))
                except procret.QueryError as ex:
                    raise CommandError(f'SQL error: {ex}') from ex

    if delimiter:
        result = delimiter.join(map(str, result))
    else:
        result = json.dumps(result, indent=indent, sort_keys=True, ensure_ascii=False)

    output_file.write(result)
    output_file.write('\n')


def record(
    procfile_list,
    database_file,
    interval,
    environment=None,
    query=None,
    recnum=None,
    reevalnum=None,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    tree = proctree.Tree(readers)

    count = 1
    query_tpl = string.Template(query)
    with procrec.SqliteStorage(database_file, procfile_list, utility.get_meta()) as store:
        while True:
            start = time.time()
            if (
                query_tpl.template
                and environment
                and (count == 1 or reevalnum and (count + 1) % reevalnum == 0)
            ):
                query = query_tpl.safe_substitute(utility.evaluate(environment))

            result = tree.get_root()
            if query:
                try:
                    result = jsonpyth.jsonpath(result, query, always_return_list=True)
                except jsonpyth.JsonPathSyntaxError as ex:
                    raise CommandError(str(ex)) from ex

            store.record(start, proctree.flatten(result, procfile_list))

            count += 1
            if recnum and count > recnum:
                break

            latency = time.time() - start
            time.sleep(max(0, interval - latency))


def _get_file_queries(filenames: list):
    for filename in filenames:
        with open(filename, 'r') as f:
            yield procret.Query(f.read(), 'Custom query')

def _get_expr_queries(exprs: list):
    for expr in exprs:
        yield procret.create_query(expr, 'Custom expression')

def _get_named_queries(names: list):
    for query_name in names:
        try:
            query = procret.registry[query_name]
        except KeyError:
            raise CommandError(f'Unknown query {query_name}')
        else:
            yield query

def _get_pid_series_points(
    timeseries: list,
    epsilon: float = None,
    moving_average_window: int = None,
) -> dict:
    pid_series = {}
    for pid, series in itertools.groupby(timeseries, lambda r: r['pid']):
        pid_series[pid] = [(r['ts'], r['value']) for r in series]
        if epsilon:
            pid_series[pid] = utility.decimate(pid_series[pid], epsilon)
        if moving_average_window:
            x, y = zip(*pid_series[pid])
            pid_series[pid] = list(zip(
                utility.moving_average(x, moving_average_window),
                utility.moving_average(y, moving_average_window),
            ))

    return pid_series

def plot(
    database_file: str,
    plot_file: str,
    query_name_list: list = None,
    after: datetime = None,
    before: datetime = None,
    pid_list: list = None,
    epsilon: float = None,
    moving_average_window: int = None,
    logarithmic: bool = False,
    style: str = None,
    formatter: str = None,
    title: str = None,
    custom_query_file_list: list = None,
    custom_value_expr_list: list = None,
):
    queries = []
    if query_name_list:
        queries.extend(_get_named_queries(query_name_list))
    if custom_value_expr_list:
        queries.extend(_get_expr_queries(custom_value_expr_list))
    if custom_query_file_list:
        queries.extend(_get_file_queries(custom_query_file_list))

    if not (0 < len(queries) <= 2):
        raise CommandError('No or more than 2 queries to plot')

    for i, query in enumerate(queries):
        if title:
            queries[i] = query._replace(title=title)
        elif len(queries) > 1:
            queries[i] = query._replace(title=f'{queries[0].title} vs {queries[1].title}')

    pid_series_list = []
    for query in queries:
        timeseries = procret.query(database_file, query, after, before, pid_list)
        pid_series_list.append(_get_pid_series_points(timeseries, epsilon, moving_average_window))

    utility.plot(
        plot_file=plot_file,
        title=queries[0].title,
        pid_series1=pid_series_list[0],
        pid_series2=pid_series_list[1] if len(pid_series_list) > 1 else None,
        logarithmic=logarithmic,
        style=style,
        formatter=formatter,
    )


async def _forward_stream(stream_reader: asyncio.StreamReader, number: int, level: int):
    async for line in stream_reader:
        logger.log(level, '№%d: %s', number, line.strip().decode())

async def _create_process(cmd: str, number: int) -> asyncio.subprocess.Process:
    logger.debug('Starting №%d: %s', number, cmd)
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    asyncio.ensure_future(_forward_stream(process.stdout, number, logging.INFO))
    asyncio.ensure_future(_forward_stream(process.stderr, number, logging.WARNING))
    return process

async def _watch(
    interval: float,
    command_list: list,
    procfile_list: list,
    environment: list = None,
    query_list: list = None,
    repeat: int = None,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    tree = proctree.Tree(readers)

    count = 1
    process_list = []
    while True:
        start = time.time()
        result_command_list = _evaluate_command_list(tree, command_list, environment, query_list)
        if not process_list:
            process_list.extend(await asyncio.gather(
                *[_create_process(cmd, i + 1) for i, cmd in enumerate(result_command_list)]
            ))
        else:
            restart_list = []
            for i, p in enumerate(process_list):
                if p.returncode is not None:
                    logger.info('№%d exited with code %d, restarting', i + 1, p.returncode)
                    restart_list.append((i, _create_process(result_command_list[i], i + 1)))

            if restart_list:
                restart_indices, restart_coroutines = zip(*restart_list)
                for i, process in zip(restart_indices, await asyncio.gather(*restart_coroutines)):
                    process_list[i] = process

        latency = time.time() - start
        await asyncio.sleep(max(0, interval - latency))

        count += 1
        if repeat and count > repeat:
            break

def _evaluate_command_list(
    tree: proctree.Tree,
    command_list: list,
    environment: list = None,
    query_list: list = None,
):
    env_dict = {}

    if environment:
        env_dict.update(utility.evaluate(environment))

    if query_list:
        tree_root = tree.get_root()
        for query_name, query in query_list:
            query = string.Template(query).safe_substitute(env_dict)
            try:
                query_result = jsonpyth.jsonpath(tree_root, query, always_return_list=True)
            except jsonpyth.JsonPathSyntaxError as ex:
                raise CommandError(str(ex)) from ex

            if not query_result:
                logger.warning('Query %s evaluated empty', query_name)

            env_dict[query_name] = ','.join(map(str, query_result))

    return [string.Template(command).safe_substitute(env_dict) for command in command_list]

def _stop_process_tree(stop_signal: signal.Signals):
    """
    Interrupt any descendant of current process by sending SIGINT.

    In case procpath is running in foreground Ctrl+C causes
    SIGINT to be sent to all processing in its tree. But when
    it's in background it's not the case, so the tree has to
    be terminated.
    """

    tree = proctree.Tree({'stat': procfile.registry['stat']}, skip_self=False)
    query = '$..children[?(@.stat.ppid == {})]..stat.pid'.format(os.getpid())
    for pid in jsonpyth.jsonpath(tree.get_root(), query, always_return_list=True):
        with contextlib.suppress(ProcessLookupError):
            os.kill(pid, stop_signal)

def watch(stop_signal: str, **kwargs):
    stop_signal = signal.Signals[stop_signal]
    # In py37+ use asyncio.run
    loop = asyncio.get_event_loop()
    watch_fut = asyncio.ensure_future(_watch(**kwargs))
    try:
        loop.run_until_complete(watch_fut)
    finally:
        _stop_process_tree(stop_signal)

        watch_fut.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            loop.run_until_complete(watch_fut)

        # Let stream forwarding tasks finish when watched processes output
        # something upon, say, SIGINT
        try:
            all_tasks = asyncio.all_tasks  # py37+
        except AttributeError:
            all_tasks = asyncio.Task.all_tasks
        task_list = asyncio.gather(*all_tasks(loop), return_exceptions=True)
        task_list_with_timeout = asyncio.wait_for(task_list, timeout=10)
        loop.run_until_complete(task_list_with_timeout)

        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


def play(
    playbook_file: str,
    target: list,
    list_sections: bool,
    dry_run: bool,
    output_file,
    option_override_list: list = None,
):
    try:
        with open(playbook_file) as f:
            book = playbook.Playbook(f, dict(option_override_list or {}))

        if list_sections:
            output_file.write('\n'.join(book.get_command_sections(target)) + '\n')
            return

        section_names = list(book.get_command_sections(target))
        if not section_names:
            raise CommandError('No section matches the target(s)')

        for section_name in section_names:
            logger.info('Executing section %s', section_name)

            command_kwargs = book.get_command(section_name)
            if 'output_file' in command_kwargs:
                command_kwargs['output_file'] = output_file

            command_fn = globals()[command_kwargs.pop('command')]
            if not dry_run:
                command_fn(**command_kwargs)
            else:
                command_kwargs.pop('output_file', None)
                output = json.dumps(command_kwargs, indent=2, sort_keys=True, ensure_ascii=False)
                output_file.write(output + '\n')

    except playbook.PlaybookError as ex:
        raise CommandError(str(ex)) from ex
