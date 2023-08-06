from time import time

import click

from overwatcher.TelegramBot import TelegramBot
from overwatcher.utils import get_env_variable, execute, get_file_paths, format_log, stringify_elapsed_time


@click.group()
def main():
    pass


@main.command()
@click.argument("command", nargs=-1)
def notify(command):
    """

    Accepts a command for overwatching and sending a notification when execution completes as an only argument.

    """
    bot = TelegramBot(
        token=get_env_variable('OVERWATCHER_TOKEN'),
        chat_id=get_env_variable('OVERWATCHER_CHAT')
    )
    start = time()
    execution_result = execute(
        command
    )
    finish = time()
    bot.send_message(
        format_log(execution_result, header=f'Command `{" ".join(command)}` is completed in `{stringify_elapsed_time(finish - start)}`. Result:')
    )
    file_paths = tuple(get_file_paths(execution_result))
    if len(file_paths) > 0:
        bot.send_message('Mentioned files:')
        for file in file_paths:
            bot.send_file(file, overflow_error_message=f'Oops, file {file} is too big')


if __name__ == "__main__":
    main()
