# coding=utf-8


import requests
from pyppeteer import launch
import asyncio
import nest_asyncio
import pysnooper
from bs4 import BeautifulSoup as Bs
import re
import time
from dataclasses import dataclass
from Crawler.util import *

# ToDo: Remember to delete before commit
email = "xxx"
password = "xxx"

bonjour_url = "https://www.facebook.com/pg/bonjourhk/posts/"


async def get_web_instance(url: str):
    # browser = await launch()
    print_time_and_msg("Setting up browser for web page...")

    browser = await launch({
        "headless": True,
    })
    page = await browser.newPage()

    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto(url, {'timeout': 10000 * 30})

    print_time_and_msg(f"The browser is set!")
    return page, browser


async def login(page):
    print_time_and_msg(f"Processing login as {email}...")

    await page.type("#email", email)
    random_wait()

    await page.type("#pass", password)
    random_wait()

    await page.click("#u_0_3")
    random_wait()

    await page.waitForNavigation()

    time.sleep(2)

    return page


async def get_data_from_web():
    page, browser = asyncio.get_event_loop().run_until_complete(get_web_instance(bonjour_url))
    after_login = asyncio.get_event_loop().run_until_complete(login(page))
    print_time_and_msg(f"Phrasing contents...")

    all_post_contents = await after_login.xpath('//*[@id="pagelet_timeline_main_column"]')
    content_list = []

    for item in all_post_contents:
        # 获取文本
        item_str = await (await item.getProperty('textContent')).jsonValue()
        content_list = item_str.split("Bonjour Cosmetics")

    for c in content_list:
        print(c)

    await browser.close()


if __name__ == '__main__':
    nest_asyncio.apply()

    asyncio.get_event_loop().run_until_complete(get_data_from_web())
