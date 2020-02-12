# coding=utf-8

from Crawler.handle_fb_page import analysis_fb_page
from Crawler.util import *

from _datetime import datetime, timedelta
import json

all_result: dict = {}


def handler_selector(shop_name: str, url: str, contents: str):
    if "www.facebook.com/pg/" in url:
        all_result.update(analysis_fb_page(shop_name, contents, url))


def write_data():
    last_update: datetime = datetime.now()
    last_update_str: str = f'const last_update = "{datetime_to_str(last_update)}"; \n'

    with open("../Web/latest_data.js", "w+", encoding="utf-8") as js:
        js.write(last_update_str)
        js.write(f"const data = ")
        json.dump(all_result, js, indent='  ', ensure_ascii=False)
        js.write(";")
        js.close()
    print_time_and_msg("Finish writing data")

    # for shop, content in all_result.items():
    #     print(f"{shop}: \n    {content}")
