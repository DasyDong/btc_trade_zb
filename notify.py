# /usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import absolute_import

import os
import sys
from zb import get_market, get_price
from mail import send_email_qq
from wechat import send_wechat
from slack import send_slack
from settings import *


def notify():
    path = os.path.join(sys.path[0], 'zb_market1.txt')
    with open(path, 'rb') as ff:
        content = ff.readlines()
        notify_message = []
        for line in content:
            try:
                name, price = line.split(':')
            except:
                continue
            max_percent = 10 if name in main_b else 20
            try:
                price_new = float(get_price(name))
            except Exception as ex:
                print name
                print ex.message
                continue

            price = float(price)
            if not price_new:
                continue
            percent = (price_new - price) / price_new * 100
            tooltip = '上' if percent > 0 else '下'
            if abs(percent) >= max_percent:
                message = ' : '.join([name, str(price), str(price_new)]) + tooltip + '\n'
                notify_message.append(message)
        if notify_message:
            # send_wechat('Market', '\n'.join(notify_message))
            send_slack('Market', '\n'.join(notify_message))
            # send_email_qq('\n'.join(notify_message))
            get_market()


if __name__ == '__main__':
    notify()
