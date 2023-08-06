import os
import re
import subprocess
from typing import Iterable

FILE_PATH_REGEXP = re.compile('[^\s]+\.[^\s]+')
SPACE_REGEXP = re.compile('\s+')
LINE_CONTINUATION_SEQUENCE = '...'


def get_env_variable(name: str, default=None, post_process=None):
    if name not in os.environ and default is None:
        raise ValueError(f'{name} environment variable is not set!')
    value = os.environ.get(name, default)
    return value if post_process is None else post_process(value)


def execute(command: tuple):
    # return subprocess.run(SPACE_REGEXP.split(' '.join(command)), stdout=subprocess.PIPE).stdout.decode('utf-8')
    # return subprocess.Popen(SPACE_REGEXP.split(' '.join(command)), stdout=subprocess.PIPE).communicate()[0]
    return subprocess.check_output(' '.join((*command, '; exit 0')), shell=True, text=True, stderr=subprocess.STDOUT)


def get_tail(text: str, n_lines: int = 10, max_line_length: int = 100):
    assert max_line_length > len(LINE_CONTINUATION_SEQUENCE)

    def get_lines():
        for i, line in enumerate(reversed(text.split('\n'))):
            if i < n_lines:
                if len(line) < max_line_length:
                    yield line
                else:
                    yield line[:max_line_length - len(LINE_CONTINUATION_SEQUENCE)] + LINE_CONTINUATION_SEQUENCE
            else:
                break

    return '\n'.join(
        reversed(
            tuple(
                get_lines()
            )
        )
    )


def format_log(log: str, header: str = None):
    return ('' if header is None else f'{header}\n') + '```\n{text}\n```'.format(
        text=get_tail(
            log,
            n_lines=get_env_variable('OVERWATCHER_N_LINES', 20, post_process=int),
            max_line_length=get_env_variable('OVERWATCHER_MAX_LINE_LENGTH', 100, post_process=int),
        )
    )


def stringify_elapsed_time(elapsed_time):
    def reduce_remainder(remainder: float, base: int, suffix: str):
        logged_amount = int(remainder) // base
        remainder -= logged_amount * base
        return f'{logged_amount} {suffix}', remainder

    def get_timer_entries():
        remainder = elapsed_time
        while remainder > 0:
            if remainder < 60:
                yield f'{remainder:.3f} seconds'
                remainder = 0
            elif remainder < 3600:
                entry, remainder = reduce_remainder(remainder, 60, 'minutes')
                yield entry
            elif remainder < 86400:
                entry, remainder = reduce_remainder(remainder, 3600, 'hours')
                yield entry
            else:
                entry, remainder = reduce_remainder(remainder, 86400, 'days')
                yield entry

    return ' '.join(get_timer_entries())


def find_files(names: Iterable):
    names = tuple(names)
    names_ = {name: None for name in names}
    name_keys = set(names_.keys())
    for root, dirs, files in os.walk(get_env_variable('OVERWATCHER_BASE_FILE_PATH', '/home')):
        for name in name_keys.intersection(set(files)):
            names_[name] = os.path.join(root, name)
    for name in names:
        if names_[name] is not None:
            yield names_[name]


def get_file_paths(log: str):
    return tuple(
        reversed(
            tuple(
                find_files(
                    map(
                        lambda filename: filename.split('/')[-1],
                        reversed(FILE_PATH_REGEXP.findall(log))
                    )
                )
            )[:get_env_variable('OVERWATCHER_N_FILES', 3, post_process=int)]
        )
    )
