# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

'''
妹子图首页抓取类
'''

from  bs4 import BeautifulSoup

from  utils.UtilsFunction import  download
from  db.RedisUtil import RedisUtils

class IndexCrawel(object):

    def __init__(self):
        self.client = RedisUtils()

    def get_page_count(self ,url):
        '''
        根据首页地址，获取标题页面的总数，并拼接标题页网址
        :param url:
        :return:
        '''
        html = download(url)
        soup = BeautifulSoup(html.text, 'lxml')
        pageNum = soup.find('div', class_='nav-links').find_all('a')[-2].get_text()
        for page in range(1 ,int(pageNum)+1):
            url = 'http://www.mzitu.com/page/{}/'.format(page)
            self.download_html(url)

    def download_html(self ,url):
        '''
        下载单个页面
        :param url:
        :return:
        '''
        print 'download : %s ' % url
        html = download(url)
        self.parse_html(html.text)

    def parse_html(self ,html):
        '''
        解析html,并入库
        :param html:
        :return:
        '''
        soup = BeautifulSoup(html, 'lxml')
        li_list = soup.find('ul', id='pins').find_all('li')
        valus = dict()
        for li in li_list:
            a = li.find('span').find('a')
            valus[a.get('href')] = a.get_text()
        self.save_in_hash('mzitu' ,valus)

    def save_in_hash(self ,key, valus):
        self.client.set_hash(key ,valus)
        self.save_in_query(valus.keys())
    def save_in_query(self ,urls):
        self.client.set_list( 'urllist' ,urls )

if __name__ == '__main__':
    IndexCrawel().get_page_count('http://www.mzitu.com/')