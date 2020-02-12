# coding=utf-8

from _datetime import datetime
import time
import pytz
import random
import locale

locale.setlocale(locale.LC_CTYPE, 'chinese')


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


if __name__ == "__main__":
    print_time_and_msg("https://www.facebook.com/pg/JHC-%E6%97%A5%E6%9C%AC%E5%9F%8E-289317227159/posts/")
