import inspect
import os
import sys


def dump_constants(logger_func, hidden_keys):
    def is_empty(v):
        return v is None or v == ''

    logger_func("dumping constants...")
    frame = inspect.currentframe()
    globals = frame.f_back.f_globals  # globals()
    constants_keys = [k for k in globals.keys() if k[0].isupper()]
    for k in constants_keys:
        global_value = globals.get(k)
        value = global_value if not is_empty(global_value) else ''
        if k in hidden_keys:
            value = len(value) * "*"
        logger_func(f'{k} = {value}')


def show_banner(logger_func, lines: str | list[str]):
    logger_func('#' * 64)
    if isinstance(lines, str):
        lines = [lines]
    for line in lines:
        logger_func(f'# {line}')
    logger_func('#' * 64)


def validate_and_crash(logger_func, variable, message):
    if not variable:
        logger_func(message)
        sys.exit(message)


def get_bool_env(env_name: str, default: bool = False) -> bool:
    return os.getenv(env_name, str(default)).lower() in ['1', 'yes', 'true']
