# coding=utf-8


def handler_selector(shop_name: str, url: str, contents: str):
    if "pg" in url:
        analysis_fb_page(shop_name, contents)


def analysis_fb_page(shop_name: str, contents: str):
    content_list: list = contents.split(shop_name)


if __name__ == "__main__":
    pass
