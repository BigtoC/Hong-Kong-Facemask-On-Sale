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

email = "xxx"
password = "xxx"

bonjour_url = "https://www.facebook.com/pg/bonjourhk/posts/"


async def get_web_instance(url: str):
    # browser = await launch()
    print("Setting up browser for web page...")

    browser = await launch({
        "headless": False,
    })
    page = await browser.newPage()

    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto(url, {'timeout': 10000 * 30})
    return page, browser


async def login(page):

    await page.type("#email", email)
    await page.type("#pass", password)
    await page.click("#u_0_3")
    await page.waitForNavigation()

    time.sleep(2)

    return page


async def get_data_from_web():
    # page_source = requests.get(bonjour_url).text

    page, browser = asyncio.get_event_loop().run_until_complete(get_web_instance(bonjour_url))
    after_login = asyncio.get_event_loop().run_until_complete(login(page))

    content = Bs(await after_login.content(), 'lxml')
    print(content)


if __name__ == '__main__':
    nest_asyncio.apply()

    asyncio.get_event_loop().run_until_complete(get_data_from_web())
