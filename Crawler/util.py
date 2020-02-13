# coding=utf-8

from _datetime import datetime
import time
import pytz
import random
import locale
from git import Repo

locale.setlocale(locale.LC_CTYPE, 'chinese')
git_path = "https://github.com/BigtoC/Hong-Kong-Facemask-On-Sale"


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
        repo = Repo(git_path)
        repo.git.add(update=True)
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
        print_time_and_msg(f"Committed as \"{commit_msg}\"")
    except:
        print_time_and_msg('Some error occurred while pushing the code')


if __name__ == "__main__":
    # print(datetime_to_str(datetime.now()))
    print("aaa".upper().count("aaa"))
