# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
from mail import send_email_qq

if __name__ == '__main__':
    blog_id_path = sys.path[0] + '/blog_id'
    with open(blog_id_path, 'r') as ff:
        blog_id = int(ff.readlines()[0].strip())

    url = 'https://www.zb.com/i/blog?item={}&type='.format(blog_id)
    resonse = requests.get(url)
    text = resonse.text
    bs = BeautifulSoup(text, 'html.parser')
    elements = bs.find_all('article')
    if elements:
        text = elements[0].find_all('p')
        send_email_qq(str(text))
        with open(blog_id_path, 'w') as ff:
            ff.write(str(blog_id + 1))
