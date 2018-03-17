# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import os
from mail import send_email_qq
from settings import ZB


def spider_zb(url):
    s = requests.session()
    s.keep_alive = False
    resonse = requests.get(url)
    text = resonse.text
    bs = BeautifulSoup(text, 'html.parser')
    elements = bs.find_all('article')
    return elements


def spider_clamation():
    url = ZB.get('platform_url') + 'i/blog?type=proclamation'
    elements = spider_zb(url)
    if elements:
        blog_latest = elements[0]  # get the latest blog
    else:
        raise Exception('No blog found')
    blog_href = blog_latest.find_all('a')[1]['href']
    blog_title = blog_latest.find_all('a')[1].text
    return blog_href, blog_title.strip()


def spider_blog_detail(blog_href):
    url = ZB.get('platform_url') + blog_href[1:]
    elements = spider_zb(url)
    if elements:
        return elements[0].text
    else:
        raise Exception('No detail blog found')


if __name__ == '__main__':
    blog_path = os.path.join(sys.path[0], 'blog_latest_title1.txt')
    with open(blog_path, 'r') as rr:
        blog_title = rr.readlines()

    try:
        href, title = spider_clamation()
        if not blog_title or blog_title[0] != title:
            blog_text = spider_blog_detail(href)
            send_email_qq(blog_text)
            with open(blog_path, 'w+') as ww:
                ww.write(title)
    except Exception as e:
        print(e)
