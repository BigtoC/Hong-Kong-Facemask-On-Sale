# coding=utf-8

from Crawler.util import *

import re
from _datetime import datetime, timedelta
import pysnooper


posts_dict: dict = {}


def convert_str_to_time(time_str: str) -> datetime:
    if len(re.findall(r"\d+\s*分鐘", time_str)) > 0:
        minute = timedelta(minutes=
                           int(re.findall(r"(\d+)\s*分鐘", time_str)[0])
                           )
        return datetime.now() - minute

    elif len(re.findall(r"\d+\s*小時", time_str)) > 0:
        hour = timedelta(hours=
                         int(re.findall(r"(\d+)\s*小時", time_str)[0])
                         )
        return datetime.now() - hour

    elif "昨天" in time_str:
        no_in_str = re.findall(r"\d+", time_str)
        hour = int(no_in_str[0])
        minute = int(no_in_str[1])

        return datetime(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day - 1,
            hour, minute, 00
        )

    elif len(re.findall(r"\d+\s*月\d+\s*日", time_str)) > 0:
        no_in_str = re.findall(r"\d+", time_str)
        print(time_str)

        month = int(no_in_str[0])
        date = int(no_in_str[1])
        hour = int(no_in_str[2])
        minute = int(no_in_str[3])
        return datetime(datetime.now().year, month, date, hour, minute, 00)

    else:
        pass


def extract_fb_post_text(text: str) -> tuple:

    p1 = text.find("查看更多")
    p2 = text.find("個回應")
    position = 0

    if p1 < p2:
        if p1 == -1:
            position = p2
        elif p1 != -1:
            position = p1
    elif p2 < p1:
        if p2 == -1:
            position = p1
        elif p2 != -1:
            print(f"{p1} : {p2}")
            print(text)
            position_text = re.findall(r"[\d+\W*]*個回應", text)[0]
            position = text.find(position_text)
    else:
        pass
    post_text = text[0: position]
    post_time = convert_str_to_time(post_text.split(" · ")[0])
    try:
        content = post_text.split(" · ")[1]
    except IndexError:
        content = "No info"
    return post_time, content


def load_to_dict(shop_name: str, on_sale: bool, post_time: str, post_content: str, url: str):
    dict_key = re.sub('[\u4e00-\u9fa5]', '', shop_name).replace(" ", "")

    posts_dict[dict_key] = {
        "Shop Name": shop_name,
        "Today On Sale": on_sale,
        "Post Time": post_time,
        "Post Content": post_content,
        "FB Page Url": url,
    }


def detect_on_sale(content: str):

    on_sale_result = re.findall(r'指定\S*分店|派籌時間|\S口罩\S*返貨', content)
    not_sale_result = re.findall(r'"沒有口罩"|"沒有發售"|"沒有發售口罩"', content)
    if len(on_sale_result) > 0:
        return True
    elif len(not_sale_result) > 0:
        return False
    else:
        return None


def beautify_content(contents: str) -> str:
    contents: str = contents.replace("派籌時間：", "<b>派籌時間：</b><br/>")

    try:
        sell_time: str = re.findall(r"\w*售時間：", contents)[0]
        contents: str = contents.replace(f"{sell_time}：", f"<b>{sell_time}:</b><br/>")
    except IndexError:
        pass

    contents: str = contents.replace("地點：", "<b>地點：</b><br/>")

    contents: str = contents.replace("#", "<br/>#")

    contents: str = contents.replace("-", "<br/><br/>- ")

    return contents


def analysis_fb_page(shop_name: str, contents: str, url: str):

    content_list: list = contents.split(shop_name)
    content_list = content_list[1: -1]

    for c in content_list:
        if "口罩" in c:
            post_time, post_content = extract_fb_post_text(c)
            today_date = datetime.now()

            on_sale = detect_on_sale(post_content)

            if on_sale:
                if post_time.month == today_date.month and post_time.day == today_date.day:
                    selling = True
                else:
                    selling = False
                load_to_dict(
                    shop_name, selling, datetime_to_str(post_time), beautify_content(post_content), url)
                break

            elif on_sale is False:
                load_to_dict(shop_name, False, datetime_to_str(post_time), beautify_content(post_content), url)
                break

            elif on_sale is None:
                pass

    dict_key = re.sub('[\u4e00-\u9fa5]', '', shop_name).replace(" ", "")
    if dict_key not in posts_dict:
        load_to_dict(
            shop_name, False,
            datetime_to_str(datetime.now()),
            f"Cannot find recent facemask sales info",
            url
        )

    print_time_and_msg(f"Finish analysing {shop_name}...")

    return posts_dict


if __name__ == "__main__":
    pass
