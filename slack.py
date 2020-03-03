# coding:utf-8
import requests
import settings
import json


# 发送消息到slack频道 https://api.slack.com/
def send_slack(title, message):
    url = settings.Slack
    params = {
        'text':  title + message
    }
    try:
        res = requests.request('POST', url, data=json.dumps(params))
        return res
    except Exception as e:
        print e
