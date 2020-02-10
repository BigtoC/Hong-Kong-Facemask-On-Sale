# coding=utf-8

from Crawler.util import *

import re


def handler_selector(shop_name: str, url: str, contents: str):
    if "pg" in url:
        analysis_fb_page(shop_name, contents)


def extract_fb_post_text(text: str) -> tuple:
    p1 = text.find("查看更多")
    p2 = text.find("個回應")

    if p1 < p2:
        position = p1
    else:
        position_text = re.findall(r"[\d+\W*]*個回應", text)[0]
        position = text.find(position_text)

    post_text = text[0: position]
    post_time = post_text.split(" · ")[0]
    content = post_text.split(" · ")[1]

    return post_time, content


def analysis_fb_page(shop_name: str, contents: str):
    print_time_and_msg(f"Analysing {shop_name}...")

    content_list: list = contents.split(shop_name)
    content_list = content_list[1: -1]

    for c in content_list:
        if "指定分店" and "派籌時間" in c:
            post_time, post_content = extract_fb_post_text(c)
            print(f"{post_time} - {post_content}")
            break
        elif "沒有口罩" in c:
            post_time, post_content = extract_fb_post_text(c)
            print(f"{post_time} - {post_content}")
            break
        else:
            pass


if __name__ == "__main__":
    pass
