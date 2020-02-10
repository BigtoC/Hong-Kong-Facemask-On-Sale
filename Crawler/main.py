# coding=utf-8

import time
from Crawler.crawler_fb import login, get_web_instance, get_data_from_web
from Crawler.data_handler import handler_selector
from Crawler.util import *

import asyncio
import nest_asyncio

sources = {
    "Bonjour Cosmetics": "https://www.facebook.com/pg/bonjourhk/posts/",
    "Sasa Hong Kong 莎莎香港": "https://www.facebook.com/pg/sasahongkong/posts/",
    "JHC 日本城": "https://www.facebook.com/pg/JHC-%E6%97%A5%E6%9C%AC%E5%9F%8E-289317227159/posts/"

}


def start_crawling():
    for shop, url in sources.items():
        print_time_and_msg(f"Start crawling {shop}")
        current_contents: str = asyncio.get_event_loop().run_until_complete(
            get_data_from_web(page, url)
        )
        handler_selector(shop, url, current_contents)
        print()


if __name__ == "__main__":
    nest_asyncio.apply()

    page, browser = asyncio.get_event_loop().run_until_complete(
        get_web_instance("https://www.facebook.com/")
    )

    page = asyncio.get_event_loop().run_until_complete(login(page))

    start_crawling()
