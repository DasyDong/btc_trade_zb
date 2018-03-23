# /usr/bin/python
from __future__ import absolute_import
from zb import get_market, get_usdt
import os
import sys
import logging
from mail import send_email_qq
#LOG = logging.getLogger(__name__)

#logging.basicConfig(filename="log/notify.log",
#                    format='%(asctime)s %(levelname)s %(message)s',
#                    level=logging.INFO)

def notify():
    max_percent = 5
    path = os.path.join(sys.path[0], 'zb_market1.txt')
    with open(path, 'rb') as ff:
        content = ff.readlines()
        notify_message = []
        for line in content:
            try:
                name, price = line.split(':')
            except:
                continue
            try:
                price_new = float(get_usdt(name))
            except Exception as ex:
                print ex.message
                continue
            price = float(price)
            percent = abs((price - price_new) / price_new * 100)
            if name in['ddm_usdt', 'cdc_usdt']:
                max_percent = 12
            if percent >= max_percent:
                message = ' : '.join([name, str(price), str(price_new)]) + 'new'
                notify_message.append(message)
        if notify_message:
            send_email_qq('\n'.join(notify_message))
            get_market()


if __name__ == '__main__':
    try:
        ##LOG.info('start notify')
        notify()
    except Exception as e:
        pass
        ##LOG.error(e)
