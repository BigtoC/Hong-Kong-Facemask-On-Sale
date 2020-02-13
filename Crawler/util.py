# coding=utf-8

from _datetime import datetime
import time
import pytz
import random
import locale
from git import Repo
import logging

locale.setlocale(locale.LC_CTYPE, 'chinese')
dot_git_folder_path = "../.git"


def print_time_and_msg(msg: str):
    now_time = time.time()
    readable_time = datetime.fromtimestamp(
        now_time,
        pytz.timezone('Asia/Shanghai')
    ).strftime(f'[%H:%M:%S:%m] - {msg}')
    print(readable_time)


def random_wait():
    wait_time = random.uniform(0.5, 1.5)
    time.sleep(wait_time)


def datetime_to_str(para_datetime: datetime) -> str:
    return para_datetime.strftime(f'[%Y-%m-%d %H:%M:%S]')


def git_push(commit_msg: str):
    try:
        repo = Repo(dot_git_folder_path)
        repo.git.add(update=True)
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
        print_time_and_msg(f"Committed as \"{commit_msg}\"")
    except BaseException as e:
        logging.exception("An exception was thrown!")


if __name__ == "__main__":
    pass
