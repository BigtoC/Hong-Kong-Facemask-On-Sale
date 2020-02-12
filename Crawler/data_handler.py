# coding=utf-8

from Crawler.handle_fb_page import analysis_fb_page

from _datetime import datetime, timedelta

all_result: dict = {}


def handler_selector(shop_name: str, url: str, contents: str):
    if "www.facebook.com/pg/" in url:
        all_result.update(analysis_fb_page(shop_name, contents))


def write_data():
    last_update: datetime = datetime.now()
    last_update_str: str = f"const last_update = {last_update}"

    for shop, content in all_result.items():
        print(f"{shop}: \n    {content}")
