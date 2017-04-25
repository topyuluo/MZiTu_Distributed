# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

from db.RedisUtil import RedisUtils
from utils.UtilsFunction import download
from bs4 import BeautifulSoup
import os
import threading
import threadpool
from multiprocessing import  Process
import time

'''
图片下载类
'''
class pageCrawel(object):
    def __init__(self):
        self.client = RedisUtils()
        self.pool = threadpool.ThreadPool(10)

    def getdownloadUrl(self):
        '''
        从redis 获取链接地址
        :return:
        '''
        while True:
            url = self.client.pop()
            print 'download url : %s' % url
            if not url:
                break
            html = download(url)
            soup = BeautifulSoup(html.text, 'lxml')
            a_list = soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
            self.download_page(a_list ,url )

    def download_page(self ,pageNum ,url):
        '''
        下载标题详情页面，创建保存图片文件夹，启用多线程下载图片
        :param pageNum:
        :param url:
        :return:
        '''
        title = self.client.get_hashvalue(url)
        path = title.strip().replace('?', '_').replace(' ', '').decode('utf-8')
        self.mkdir(path)
        for page in range(1 ,int(pageNum)+1):
            page_url = url+"/"+str(page)
            # print page_url
            time.sleep(0.3)
            thread = threading.Thread(target=self.mutliprocess, args=(page_url ,))
            thread.start()
            # self.mutliprocess(page_url)

    def mutliprocess(self , page_url):
        '''
        多线程下载图片
        :param page_url:
        :return:
        '''
        page_html = download(page_url)
        imgurl = BeautifulSoup(page_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.down_img(imgurl)

    def down_img(self , imgurl):
        '''
        保存图片
        :param imgurl:
        :return:
        '''
        with open(imgurl[-9:] ,'wb') as f :
            f.write(download(imgurl).content)

    def mkdir(self ,path):
        '''
        本机创建文件夹
        :param path:
        :return:
        '''
        print path
        realpath = os.path.join('d:\mzitu' ,path)
        isexists = os.path.exists(realpath)
        if not isexists:
            os.makedirs(realpath)
        os.chdir(os.path.join('d:\mzitu' ,path))

def run():
    pageCrawel().getdownloadUrl()




if __name__ == '__main__':

    ###以多继承的方式启动函数 ，并启动了5个线程

    # pageCrawel().getdownloadUrl()
    start = time.time()
    proc_list = []
    for num in range(5):
        proc = Process(target=run, args=())
        proc_list.append(proc)

    for p in proc_list:
        p.start()

    for p in proc_list:
        p.join()
    end = time.time()
    print end -start
