####前言
最近把目光投向了，妹子图（你一看见这三个字是不是头都大了， 怎么又是这个网站，被这帮搞爬虫的都爬烂了吧），先不要着急，别人爬过不代表你也能爬，每个人写爬虫的思路都是不一样的。 重要的是自己动手做一遍。整体看这个网站的爬取难度并不大，而且还有福利，为啥不试试呢。单线程的毕竟是太慢了，那么多进程+多线程+redis ,做一个简易的分布式程序将是我接下来叙述的重点。 

程序虽小，也要五脏俱全。 

####全军出击

**抓取流程整理：**
网站首页：
![网站首页](http://upload-images.jianshu.io/upload_images/2192701-bb75bb92c84ff847.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

抓取的方式就不多叙述了，使用浏览器抓取工具可以很容易获取到，如下图：

![源码分析](http://upload-images.jianshu.io/upload_images/2192701-f3de1ebbbc8716f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

之后点击标题，多点击几个分页，分析url生成规律，便于程序拼接网址链接，之后查看图片的地址，分析抓取规则，便于程序下载：

![标题详情](http://upload-images.jianshu.io/upload_images/2192701-41b6f997eba11318.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在该页面下，主要做两个分析，一个是分析该套标题下，一共有多少张图片，也就是图片中的64要抓下来，还有就是图片的链接地址，也要抓下来。

好了网站基本分析完了，开始写程序。

#### 代码解析
下面只是部分主要的代码完整代码请见文后地址。
抓取所有的标题,并入库：
<pre><code>
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
'''
</code></pre>
从redis获取信息，并完成下载保存：
<pre><code>
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
            time.sleep(0.8)
            thread = threading.Thread(target=self.mutliprocess, args=(page_url ,))
            thread.start()
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
</code></pre>
#### 程序框架

![简易框架图](http://upload-images.jianshu.io/upload_images/2192701-4f2967401b15059e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

####运行效果

![效果图](http://upload-images.jianshu.io/upload_images/2192701-19cec42c79bd384b.gif?imageMogr2/auto-orient/strip)

#### 源码地址
github:https://github.com/topyuluo/MZiTu_Distributed
代理池：http://www.jianshu.com/p/fd92ca79c9c7