import sys
import time
import json
import urllib2
import hashlib
import struct
import sha
import requests

from settings import *


class ZBTrade(object):
    def __init__(self, mykey, mysecret):
        self.mykey = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), aKey)
        value = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value = struct.pack("%ds" % len(aValue), aValue)
        print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params=''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time() * 1000)
            params += '&sign=%s&reqTime=%d' % (sign, reqTime)
            url = ZB.get('trade_url') + path + '?' + params
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception, ex:
            print >> sys.stderr, 'zb request ex: ', ex
            return None

    def query_account(self):
        try:
            params = "accesskey=" + self.mykey + "&method=getAccountInfo"
            path = 'getAccountInfo'

            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception, ex:
            print >> sys.stderr, 'zb query_account exception,', ex
            return None


def get_account():
    access_key = ZB.get('access_key')
    access_secret = ZB.get('access_secret')

    api = ZBTrade(access_key, access_secret)

    print api.query_account()


def get_usdt(key):
    url = ZB.get('url') + 'data/v1/ticker?market={}'.format(key)
    text = requests.get(url, timeout=30).text
    content = json.loads(text)
    value = content.get('ticker').get('last')
    return value


def get_market():
    url = ZB.get('url') + 'data/v1/markets'
    text = requests.get(url, timeout=30).text
    content = json.loads(text)
    keys = content.keys()
    with open('zb_market', 'wb') as ff:
        for key in keys:
            if not key.endswith('_usdt'):
                continue
            ff.write(key + ":" + get_usdt(key) + "\n")
