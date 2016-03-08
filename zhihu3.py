from pymongo import MongoClient
from lxml import etree
import threading
import requests
import re
from datetime import datetime

start = datetime.now()
#数据库配置
mc=MongoClient('localhost',27017)
db=mc.fuli

mylock = threading.RLock()  
all_urls_o=[]
iuse=[]
all_urls_c=[]
threads=[]
currentNum=[0]
cookie={'Cookie':'_za=e845c5d0-ecbe-4ea8-92a4-f251fa35466c; q_c1=1ee6953b2fd049f29171d79e26436020|1445780798000|1443087353000; cap_id="Nzc5ZDg5MDE1MTg2NGMwMGE0YTUyMjM4OGU4MDA5MDc=|1447150718|30bd3701e467d0a761d83292c220814fd303885f"; __utma=51854390.470477516.1443087355.1447906495.1447911956.3; __utmz=51854390.1447844437.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _xsrf=acf970e0903bb0de931493a3065d490f; _ga=GA1.2.470477516.1443087355; z_c0="QUJCTTF1Rk5fQWdYQUFBQVlRSlZUVEJTYVZiOU8wZWZ5bWgzVGc4Tl9INHpFVnNzc0VPVDdBPT0=|1447150896|958f746493670365afa1950df4fb3a36eed2bbe8"; __utmv=51854390.100-2|2=registration_date=20151110=1^3=entry_date=20150924=1; __utmb=51854390.2.10.1447911956; __utmc=51854390; __utmt=1'}
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}

def datebase_urls():
    for each in db.alldata.find({},{'主页':1,'_id':0}):
        all_urls_o.append(each['主页'])
    for each in db.allinfo.find({},{'主页':1,'_id':0}):
        all_urls_o.remove(each['主页'])
        


def getOtherInfo(urls):
    for url in urls:
        try:
            otherInfo=requests.get(url+'/about',cookies=cookie,headers=header,timeout=4).text
            source=etree.HTML(otherInfo)
        except Exception:
            print('远程主机关闭连接或者解析页面出错，正在重试......')
            try:
                otherInfo=requests.get(url+'/about',cookies=cookie,headers=header,timeout=4).text
                source=etree.HTML(otherInfo)
            except Exception:
                print('远程主机关闭连接或者解析页面出错(已重试)，结束本条URL后续操作！')
        allInfo1=source.xpath('//a[@class="item "]/span/text()')
        allInfo2=source.xpath('//div[@class="zm-profile-module-desc"]/span/strong/text()')
        care=source.xpath('//div/div/a/strong/text()')[:2]
        zl=re.findall('<strong>(.*?)个专栏</strong>',otherInfo)[0] if re.findall('<strong>(.*?)个专栏</strong>',otherInfo) !=[] else '0'
        try:
            topic=re.findall('<strong>(.*?)个话题</strong>',otherInfo)[0]
        except Exception:
            print('页面出现问题了',url)
        mylock.acquire()
        try:
            db.allinfo.insert({'主页':url,'提问':allInfo1[0],'回答':allInfo1[1],'专栏文章':allInfo1[2],'收藏':allInfo1[3],'公共编辑':allInfo1[4],'获得赞同':allInfo2[0],'获得感谢':allInfo2[1],'获得收藏':allInfo2[2],'获得分享':allInfo2[3],'关注了':care[0],'关注者':care[1],'关注专栏':zl,
            '关注话题':topic})
        except IndexError:
            print('存入信息出错，暂时跳过本条URL：',url)
            iuse.append(url)
        currentNum[0]+=1
        print(currentNum[0],'/',len(all_urls_o),'   错误:',len(iuse))
        mylock.release()
        
class Thread(threading.Thread):
    def __init__(self,urls):
        threading.Thread.__init__(self)
        self.urls=urls
    def run(self):
        getOtherInfo(self.urls)
       

def createThreads():
    k=0
    span=int(len(all_urls_o)/4)
    for i in range(3):
        threads.append(Thread(all_urls_o[k:(i+1)*span]))
        k=(i+1)*span            
    threads.append(Thread(all_urls_o[3*span:]))
    for eachThread in threads:
        eachThread.start()

if __name__=='__main__':
    datebase_urls()
    createThreads()
    for eachThread in threads:
        eachThread.join()
    end=datetime.now()
    print('---搜集结束---')
    print('用时：'+str(end-start))
