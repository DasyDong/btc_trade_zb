import requests
import settings


def send_wechat(title, message):
    url, key = settings.WeChat.get('url'), settings.WeChat.get('key')
    params = {
        'sendkey': key,
        'text': title,
        'desp': message
    }
    try:
        res = requests.get(url, params)
        return res
    except Exception as e:
        print e
