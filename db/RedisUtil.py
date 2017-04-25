# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

import redis
'''
    操作redis 工具类
    set_hash():将妹子图标题全部抓取，存入hash中，比使用url 作为键，方便根据链接地址提取标题
    set_list():将标题地址放入列表中，方便下载
    pop():从列表中取出一个地址，并放入已下载列表中
    get_hashvalue():根据链接取出该连接对应的标题
'''

class RedisUtils(object):
    def __init__(self , host = '192.168.1.15' , port = 6379 , db = 0):
        self.__conn = redis.Redis( host , port , db)

    def set_hash(self , key , values):
        self.__conn.hmset(key , values)

    def set_list(self , key,values):
        for url in values:
            self.__conn.lpush(key ,url)

    def pop(self):
        url = self.__conn.brpoplpush('urllist', 'downlist', 1)
        return url

    def get_hashvalue(self , key):
        value = self.__conn.hget('mzitu', key)
        return str(value).strip().replace('?','_').replace(' ' ,'' )


if __name__ == '__main__':
    RedisUtils().get_hashvalue('http://www.mzitu.com/90324')