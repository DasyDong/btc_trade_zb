# /usr/bin/python
from __future__ import absolute_import
from zb import get_market, get_usdt
import os, sys
from mail import send_email_qq, send_email_ctrip


def notify():
    with open(sys.path[0] + '/zb_market', 'rb') as ff:
        content = ff.readlines()
        notify_message = []
        for line in content:
            name, price = line.split(':')
            try:
                price_new = float(get_usdt(name))
            except Exception as ex:
                print ex.message
                continue
            price = float(price)
            percent = abs((price - price_new) / price_new * 100)
            if percent >= 6:
                message = ' : '.join([name, str(price), str(price_new)]) + 'new'
                notify_message.append(message)
        if notify_message:
            send_email_qq('\n'.join(notify_message))
            get_market()


if __name__ == '__main__':
    notify()
