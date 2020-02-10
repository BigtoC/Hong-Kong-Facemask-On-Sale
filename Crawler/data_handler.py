# coding=utf-8


def handler_selector(shop_name: str, url: str, contents: str):
    if "pg" in url:
        analysis_fb_page(shop_name, contents)


def extract_fb_post_text(text: str) -> tuple:
    position = text.find("查看更多")
    post_text = text[0: position]

    post_time = post_text.split(" · ")[0]
    content = post_text.split(" · ")[1]

    return post_time, content


def analysis_fb_page(shop_name: str, contents: str):
    content_list: list = contents.split(shop_name)

    for c in content_list:
        if "指定分店" and "派籌時間" in c:
            post_time, post_content = extract_fb_post_text(c)
            print(post_time)
            break
        elif "沒有" and "發售" or "返貨" in c:
            post_time, post_content = extract_fb_post_text(c)
            print(post_content)
            break


if __name__ == "__main__":
    pass