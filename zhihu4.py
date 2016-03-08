import requests
import random
from pymongo import MongoClient
from lxml import etree
import threading
from datetime import datetime
from bs4 import BeautifulSoup
cookie={'Cookie':'_za=e845c5d0-ecbe-4ea8-92a4-f251fa35466c; q_c1=1ee6953b2fd'
    '049f29171d79e26436020|1445780798000|1443087353000; cap_id="Nzc5ZDg5MDE1'
    'MTg2NGMwMGE0YTUyMjM4OGU4MDA5MDc=|1447150718|30bd3701e467d0a761d83292c22'
    '0814fd303885f"; __utma=51854390.470477516.1443087355.1447253883.1447401'
    '778.6; __utmz=51854390.1447253883.5.2.utmcsr=baidu|utmccn=(organic)|utm'
    'cmd=organic; _xsrf=acf970e0903bb0de931493a3065d490f; _ga=GA1.2.47047751'
    '6.1443087355; z_c0="QUJCTTF1Rk5fQWdYQUFBQVlRSlZUVEJTYVZiOU8wZWZ5bWgzVGc'
    '4Tl9INHpFVnNzc0VPVDdBPT0=|1447150896|958f746493670365afa1950df4fb3a36ee'
    'd2bbe8"; __utmv=51854390.100-2|2=registration_date=20151110=1^3=entry_d'
    'ate=20150924=1; __utmb=51854390.4.10.1447401778; __utmc=51854390; __utmt=1'}
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}

#计时开始
start = datetime.now()
#抓取线url线程池
allthread_u=[]
#获取信息线程池
allthread_i=[]
#已经存在的URL集合
set_urls=set()
#列本次搜集不重复的URL列表
list_urls=[]
#入口URL列表
all_url=[]
#存入有效的url数
useful=[0]
#数据库配置
mc=MongoClient('localhost',27017)
db=mc.fuli
#创建锁
mylock = threading.RLock()  
#遍历URL数
temps=[0]

#初始化已存在的URL集合(来自数据库Mongo)
def init():
    databases_urls=db.info.find({},{'主页':1,'_id':0})
    for each in databases_urls:
        set_urls.add(each['主页'])


#获取入口url列表
def get_all_urls(threadNum):
        for each in db.info.find().limit(threadNum).skip(random.randint(1,len(set_urls))):
            all_url.append([each['主页']])


#多线程抓取类
class getUrl(threading.Thread):
    def __init__(self,url,total):
        threading.Thread.__init__(self)
        self.url=url
        self.total=total
    def run(self):
       getFollowees(self.url,0,self.total)

#创建抓取用户url多线程
def createGetUrlThreads(all_url,total):
    for i,url in enumerate(all_url):
        allthread_u.append(getUrl(url,total))
        allthread_u[i].start()             

#多线程获取类
class getInfor(threading.Thread):
    def __init__(self,urls):
        threading.Thread.__init__(self)
        self.urls=urls
    def run(self):
       personalInformation(self.urls)

#创建获取用户信息多线程
def createGetInforThreads(list_urls):
    k=0
    span=int(len(list_urls)/4)
    for i in range(3):
        allthread_i.append(getInfor(list_urls[k:(i+1)*span]))
        k=(i+1)*span            
    allthread_i.append(getInfor(list_urls[3*span:]))
    for eachThread in allthread_i:
        eachThread.start()


#递归查找用户
def getFollowees(urls,cur,total):
    if cur<total:
       cur+=1
       for url in urls: 
            temp=[]
            try:
                FolloweesPage=requests.get(url+'/followees',cookies=cookie,headers=header).text
            except(TypeError,ConnectionResetError,requests.packages.urllib3.exceptions.ProtocolError,requests.exceptions.ConnectionError):
                print('获取关注列表出错，正在重连。。。')
                try:
                    FolloweesPage=requests.get(url+'/followees',cookies=cookie,headers=header).text
                except(TypeError,ConnectionResetError,requests.packages.urllib3.exceptions.ProtocolError,requests.exceptions.ConnectionError):
                    print('远程主机关闭连接，结束本条URL后续操作！')
            source = BeautifulSoup(FolloweesPage,"html5lib")
            for everyone in source.body('div',class_='zm-profile-card zm-profile-section-item zg-clear no-hovercard'):
                href = everyone.find('a',class_='zg-link')['href']
                name=everyone.find('a',class_='zg-link')['title']
                mylock.acquire() #获得锁
                temp.append(href)
                temps[0]+=1
                if href not in set_urls:
                     set_urls.add(href)
                     list_urls.append(href)
                     print('                加入：     '+href+'    '+name)
                else:
                     print('已经存在啦： '+href+'    '+name)
                mylock.release()
            getFollowees(temp,cur,total)

    
#获取用户信息       
def personalInformation(urls):
    for url in urls:
        try:
            html= requests.get(url+'/about',cookies=cookie,headers=header).text
        except Exception:
            print('遇见连接错误啦，正在重新连接')
            try:
                html= requests.get(url+'/about',cookies=cookie,headers=header).text
            except Exception:
                print('远程主机关闭连接，跳过本条url。')
        source = BeautifulSoup(html,"html5lib")
        genders=source.find('span',class_='item gender')
        if genders:
            if genders.i['class'][1] == 'icon-profile-male':
                gender='男'
            elif genders.i['class'][1] == 'icon-profile-female':
                gender='女'
        else:
                gender=''
        try:
            name=source.find('div',class_='title-section ellipsis').a.string
        except AttributeError as e:
            print('查找名字出错！，正在重新找。。'+url)
            try:
                html= requests.get(url+'/about',cookies=cookie).text
                source = BeautifulSoup(html,"html5lib")
                name=source.find('div',class_='title-section ellipsis').a.string
            except AttributeError as e:
                print('查找名字出错(已重试)！将会跳过本条记录')
        business = source.find('span',class_='business item')['title'] if source.find('span',class_='business item') !=None else ''
        locations= source.find('span',class_='location item')['title'] if source.find('span',class_='location item') !=None else ''
        companys = source.find('span',class_='employment item')['title'] if source.find('span',class_='employment item') !=None else ''
        posts    = source.find('span',class_='position item')['title'] if source.find('span',class_='position item') !=None else ''
        schools  = source.find('span',class_='education item')['title'] if source.find('span',class_='education item') !=None else ''
        professionals=source.find('span',class_='education-extra item')['title'] if source.find('span',class_='education-extra item') !=None else ''
        mylock.acquire()
        db.info.insert({'主页':url,'姓名':name,'性别':gender,'行业':business,'住址':locations,'公司':companys,'职位':posts,'学校':schools,'专业':professionals})
        useful[0]+=1
        print(useful[0],'/',len(list_urls))
        mylock.release()
        
        
def main():
    threadNum=int(input('输入线程数(建议四个以内)：'))
    get_all_urls(threadNum)
    total=int(input('输入爬取层数：'))
    createGetUrlThreads(all_url,total)
    for each in allthread_u:
        each.join()
    print('用户查找完毕！\n正在搜集用户信息......')
    createGetInforThreads(list_urls)
    for each in allthread_i:
        each.join()
    print('用户信息搜集完毕！\n存入数据库...')
    print('信息存入完毕！')
    print('\n当前集合已有url（含未存入数据库）：',len(set_urls))
    print('本次搜集未重复：',len(list_urls))
    print('全部查看的url：',temps[0])
    print('存入有效的url数：',useful[0])
    print('当前数据库已有url:',db.info.count())
    end = datetime.now()
    print('\n!!!!!抓取完毕!!!!!!\n花费时间：'+str(end-start))
    

if __name__=='__main__':
    init()
    main()
    
