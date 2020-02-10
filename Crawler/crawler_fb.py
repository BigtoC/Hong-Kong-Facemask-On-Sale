# coding=utf-8
from typing import List, Any, Union

import requests
from pyppeteer import launch
import asyncio
import nest_asyncio
import pysnooper
from Crawler.util import *

# Generated a temp email from https://temp-mail.org/ for creating a new FB account
email: str = "xiside2970@jmail7.com"
password: str = "hkmask2020"


async def get_web_instance(url: str):
    # browser = await launch()
    print_time_and_msg("Setting up browser for web page...")

    browser = await launch({
        "headless": False,
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

    for i in range(10):
        await page.evaluate('_ => {window.scrollBy(0, window.innerHeight);}')
        random_wait()

    return page


async def get_data_from_web(url: str) -> str:
    page, browser = asyncio.get_event_loop().run_until_complete(
        get_web_instance(url)
    )

    after_login = asyncio.get_event_loop().run_until_complete(login(page))
    print_time_and_msg(f"Crawling contents...")

    content_str = ""
    all_post_contents = await after_login.xpath('//*[@id="pagelet_timeline_main_column"]')

    for item in all_post_contents:
        # 获取文本
        content_str += await (await item.getProperty('textContent')).jsonValue()

    await browser.close()

    return content_str


if __name__ == '__main__':
    nest_asyncio.apply()
    bonjour_url = "https://www.facebook.com/pg/bonjourhk/posts/"
    asyncio.get_event_loop().run_until_complete(
        get_data_from_web(bonjour_url)
    )
