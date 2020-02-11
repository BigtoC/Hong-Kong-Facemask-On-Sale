# coding=utf-8

from Crawler.util import *

import re
from _datetime import datetime, timedelta


posts_dict: dict = {}


def handler_selector(shop_name: str, url: str, contents: str):
    if "pg" in url:
        analysis_fb_page(shop_name, contents)


def convert_str_to_time(time_str: str) -> datetime:
    dt = None

    if "小時" in time_str:
        hour = timedelta(hours=int(time_str.replace("小時", "")))
        dt = datetime.now() - hour

    if "分鐘" in time_str:
        minute = timedelta(minutes=int(time_str.replace("分鐘", "")))
        dt = datetime.now() - minute

    elif "月" and "日" in time_str:
        month = int(time_str[0])
        date = int(time_str[2])
        tmp_time = time_str[4: -1]
        hour = int(tmp_time.split(":")[0])
        minute = int(tmp_time.split(":")[1])
        dt = datetime(datetime.now().year, month, date, hour, minute, 00)

    else:
        pass

    return dt


def extract_fb_post_text(text: str) -> tuple:
    p1 = text.find("查看更多")
    p2 = text.find("個回應")

    if p1 < p2:
        position = p1
    else:
        position_text = re.findall(r"[\d+\W*]*個回應", text)[0]
        position = text.find(position_text)

    post_text = text[0: position]

    post_time = convert_str_to_time(post_text.split("·")[0])
    content = post_text.split("·")[1]

    return post_time, content


def load_to_dict(shop_name: str, on_sale: bool, post_time: datetime, post_content: str,):

    posts_dict[shop_name] = {
        "Today On Sale": on_sale,
        "Post Time": post_time,
        "Post Content": post_content
    }


def detect_on_sale(content: str):

    if "口罩" in content:
        on_sale_result = re.findall(r'指定分店|派籌時間', content)
        not_sale_result = re.findall(r'"沒有口罩"|"沒有發售"|"沒有發售口罩"', content)

        if len(on_sale_result) > 0 and not_sale_result == 0:
            return True
        elif len(on_sale_result) == 0 and len(not_sale_result) > 0:
            return False
        else:
            return None


def analysis_fb_page(shop_name: str, contents: str):

    content_list: list = contents.split(shop_name)
    content_list = content_list[1: -1]

    for c in content_list:
        post_time, post_content = extract_fb_post_text(c)
        # print(f"{post_time} - {post_content}")

        on_sale = detect_on_sale(post_content)

        if on_sale:
            load_to_dict(shop_name, on_sale, post_time, post_content)
            break

        elif on_sale is False:
            load_to_dict(shop_name, on_sale, post_time, post_content)
            print(posts_dict)
            break

        elif on_sale is None:
            load_to_dict(shop_name, on_sale, datetime.now(), f"Cannot find recently mask sales info")

    print_time_and_msg(f"Finish analysing {shop_name}...")


def write_data():
    last_update: datetime = datetime.now()
    last_update_str: str = f"const last_update = {last_update}"

    for shop, content in posts_dict.items():
        print(f"{shop}: \n    {content}")


if __name__ == "__main__":
    pass
