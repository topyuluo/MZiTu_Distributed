# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

'''
工具函数
    download():下载函数，默认使用本机地址抓取，抓取失败使用代理，并重试5次
    get_header():生成headers 函数
    get_proxy():获取代理函数
    del_proxy():删除失效代理函数
    volidate_proxy():验证代理可用性函数
'''

import random
import requests
import json
import traceback
import time

def download(url ,proxy=None , timeout = 15 , retryNum = 5):
    try:
        if proxy is None:
            response = requests.get(url, headers=get_header())
            return response
        else:
            if retryNum > 0:
                response = requests.get(url, proxies=proxy, timeout=timeout, headers=get_header())
                return response
    except Exception as e:
        # traceback.print_exc()
        print e
        while not volidate_proxy(proxy):
            ip = get_proxy()
            proxy = {'http':ip}
        print 'use proxy : %s' % proxy
        if not proxy:
            time.sleep(10)
        return  download(url , proxy = proxy , timeout= timeout , retryNum= retryNum -1 )



def get_header():
    useragent_list = [
        'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/532.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/532.3',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5'
    ]
    useragent = random.choice(useragent_list)
    headers = {'User-Agent':useragent}
    return headers

def get_proxy():
    proxy = requests.get('http://127.0.0.1:5000/get')
    json_object = json.loads(proxy.text)
    return json_object['proxy']

def del_proxy(proxy):
    proxydel = proxy['http']
    url = 'http://127.0.0.1:5000/delete?proxy={}'.format(proxydel)
    requests.get(url)
    print 'del proxy : %s ' % proxydel

def  volidate_proxy(proxy):
    if not proxy:
        return False
    try:
        response = requests.get('http://www.mzitu.com', proxies=proxy, headers=get_header(), timeout=5)
        if response.status_code == requests.codes.ok:
            return True
    except Exception as e:
        print e
        del_proxy(proxy)
        return False

