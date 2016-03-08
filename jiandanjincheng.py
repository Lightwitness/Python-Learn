import threading
from multiprocessing import Process
import os
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

os.chdir('C:/Users/FLCRS/temp/temp')
#存储获取开始网页地址的地址
start_url = 'http://jandan.net/ooxx'
#存储User-Agent
header =[{'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30 ChromePlus/1.6.3.1'}, 
         {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.98 Safari/534.13 ChromePlus/1.6.0.0'},
         {'User-Agent':'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.0.1) Gecko/20021220 Chimera/0.6'},
         {'User-Agent':'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.0.1) Gecko/20021216 Chimera/0.6'}]
#存储User-Agent可用信息
header_Available=[None for i in range(len(header))]
#存储开始网页地址
start_page = None
#线程上限
Maxthreads = 4
#存储线程数量
threadnum = None
#线程容器
allthread =[]
#存储爬取的页数
numberOfPages = None

#显示可用User-Agent信息
def show_info():
    for i in range(len(header)):
        print('                第'+str(i)+'个User-Agent: '+str(header_Available[i]))

#函数功能：解析网页
#def goodjob(children,imglist,comparetolist):
#    for tmp in children:
#        comparelist = []
#        for parent in tmp.parents:
#            if (parent!=None) and (parent.name!='html'):
#                comparelist.append(parent.name)
#            else:
#                break
#        if comparelist == comparetolist:
#            imglist.append(tmp)

#抓取函数
def main(page):
    for i in range(len(header)):
        if header_Available[i]!=False:
            url = start_url+'/page-'+str(page)+'#comments'
            r = requests.get(url,headers=header[i])
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text,"lxml")
            if soup.find(text=re.compile('屏蔽'))==None:
                print('=============================')
                print('正在下载第 '+str(page)+' 页')
#               存储包含图片地址的标签
                img = []
                
#               筛选img标签的替代方案A：
#               comparetolist = ['p','div','div','div','li','ol','div','div','div','div','body']
#               goodjob(soup.find_all('img',src=True),img,comparetolist)

                imgall = soup.body('li',id = re.compile("comment-"))
                for tmp in imgall:
                    img+=tmp.div.find('div',class_ = 'row').find('div',class_ = 'text').find_all('img',src=True)

                for n,girl in enumerate(img):
                    print('       第 '+str(n)+' 张',end='')
                    if not girl.has_attr('org_src'):
                        url = girl['src']
                        with open('妹纸图'+str(page)+'-'+str(n)+url[-4:],'wb') as f:
                            f.write(requests.get(url).content)
                    else:
                        url = girl['org_src']
                        with open('妹纸图'+str(page)+'-'+str(n)+url[-4:],'wb') as f:
                            f.write(requests.get(url).content)
                    print('...OK!')
                print('第 '+str(page)+' 页下载完成啦！！！')
                return True
            else:
                if header_Available[i]!=False:
                    header_Available[i]=False
                    print('被屏蔽，正在反屏蔽.....\n        User-Agent 可用信息:')
                    show_info()
                    if header_Available[len(header)-1]==False:
                        print('反屏蔽失败,线程终止!\nUser-Agent 可用信息:')
                        show_info()
                        return False

#创建多线程
def creatBackGroundThreads ():
    for i in range(threadnum):
       allthread.append(Async(start_page-i-1))
       #allthread.append(Process(target=main, args=('start_page-i-1',)))
       allthread[i].start()
#当前线程
def currentThreads():
    if numberOfPages != 0:
        for pages in range(start_page,start_page-numberOfPages,-1-threadnum):
            if header_Available[len(header)-1]!=False:
                main(pages)
            else:
                return False
 
#多线程类
class Async(threading.Thread):
    def __init__(self,h_page):
        threading.Thread.__init__(self)
        self.h_page=h_page
    def run(self):
        for pages in range(self.h_page,start_page-numberOfPages,-1-threadnum):
            if header_Available[len(header)-1]!=False:
                main(pages)
            else:
                return False

start = datetime.now()

#获得 start_page
for i in range(len(header)):
    rs = requests.get(start_url,headers=header[i])
    rs.encoding = 'utf-8'
    soups = BeautifulSoup(rs.text,"lxml")
    if soups.find(text=re.compile('屏蔽'))==None:
        start_page = int(soups.body.find('span', class_= 'current-comment-page').contents[0][1:-1])
#       上一行可替代方案
#       int(soups.body.find('span', class_= 'current-comment-page').string[1:-1])
        numberOfPages=int(input('输入爬取的页数: '))
        threadnum=int(input('输入线程数(线程数量上限'+str(Maxthreads)+'): '))%(Maxthreads+1)-1
        if threadnum < 0:
            threadnum = 0
        break
    else:
        header_Available[i]=False
        print('被屏蔽，正在反屏蔽.....\n        User-Agent 可用信息:')
        show_info()
    if header_Available[len(header)-1]==False:
        print('反屏蔽失败!\nUser-Agent 可用信息:')
        show_info()
            
if header_Available[len(header)-1]!=False:
    creatBackGroundThreads()
    currentThreads()
    for m in allthread:
        m.join()
    end = datetime.now()
    if header_Available[len(header)-1]!=False:
        print('\n!!!!!抓取完毕!!!!!!\n花费时间：'+str(end-start))
    else:
        print('!!!!!部分图片未能抓取!!!!!')
else:
    print('!!!!不能进行抓取!!!!!')
