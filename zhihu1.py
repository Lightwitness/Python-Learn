import requests
from pymongo import MongoClient
from lxml import etree
import threading
from datetime import datetime
from bs4 import BeautifulSoup
cookie={'Cookie':'_za=e845c5d0-ecbe-4ea8-92a4-f251fa35466c; q_c1=1ee6953b2fd049f29171d79e26436020|1445780798000|1443087353000; cap_id="Nzc5ZDg5MDE1MTg2NGMwMGE0YTUyMjM4OGU4MDA5MDc=|1447150718|30bd3701e467d0a761d83292c220814fd303885f"; __utma=51854390.470477516.1443087355.1447253883.1447401778.6; __utmz=51854390.1447253883.5.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _xsrf=acf970e0903bb0de931493a3065d490f; _ga=GA1.2.470477516.1443087355; z_c0="QUJCTTF1Rk5fQWdYQUFBQVlRSlZUVEJTYVZiOU8wZWZ5bWgzVGc4Tl9INHpFVnNzc0VPVDdBPT0=|1447150896|958f746493670365afa1950df4fb3a36eed2bbe8"; __utmv=51854390.100-2|2=registration_date=20151110=1^3=entry_date=20150924=1; __utmb=51854390.4.10.1447401778; __utmc=51854390; __utmt=1'}
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}

#计时开始
start = datetime.now()
#MongoDB配置
mc=MongoClient('localhost',27017)
db=mc.fuli
#抓取线url线程池
allthread_u=[]
#获取信息线程池
allthread_i=[]
#已经存在的URL集合
set_urls=set()
#列表化存在的URL集合
list_urls=[]
#入口URL列表
all_url=[]
#搜集的用户信息
information={}
#创建锁
mylock = threading.RLock()  
#测试URL列表
temps=[]

#初始化已存在的URL集合(来自数据库Mongo)
def init():
    databases_urls=db.info.find({},{'主页':1,'_id':0})
    for each in databases_urls:
        set_urls.add(each['主页'])

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
                FolloweesPage=requests.get(url+'/followees',cookies=cookie,headers=header).text
            # selector=etree.HTML(FolloweesPage)
            source = BeautifulSoup(FolloweesPage,"html5lib")
            # Guanzhu_a=selector.xpath('//*[@id="zh-profile-follows-list"]/div/div/div[2]/h2/a')
            # for everyone in Guanzhu_a:
            for everyone in source.body('div',class_='zm-profile-card zm-profile-section-item zg-clear no-hovercard'):
                #href=everyone.xpath('@href')[0]
                href = everyone.find('a',class_='zg-link')['href']
                #name=everyone.xpath('text()')[0]
                name=everyone.find('a',class_='zg-link')['title']
                mylock.acquire() #获得锁
                temp.append(href)
                temps.append(href)
                #list_urls.append(href)
                if href not in set_urls:
                     set_urls.add(href)
                     list_urls.append(href)
                    # temp.append(href)
                     print('加入：'+href+'    '+name)
                # else:
                #      print('已经存在：'+everyone.xpath('@href')[0]+'    '+everyone.xpath('text()')[0])
                mylock.release()
                # print('找到的：'+everyone.xpath('@href')[0]+'    '+everyone.xpath('text()')[0])
            getFollowees(temp,cur,total)
def PIitem(item):
    if item!=None:
        return item['title']
    else:
        return '未知'
        
#获取用户信息       
def personalInformation(urls):
    for url in urls:
        try:
            html= requests.get(url+'/about',cookies=cookie,headers=header).text
        except(TypeError,ConnectionResetError,requests.packages.urllib3.exceptions.ProtocolError,requests.exceptions.ConnectionError):
            print('遇见连接错误啦，正在重新连接')
            try:
                html= requests.get(url+'/about',cookies=cookie,headers=header).text
            except (TypeError,ConnectionResetError,requests.packages.urllib3.exceptions.ProtocolError,requests.exceptions.ConnectionError):
                print('远程主机关闭连接，跳过本条url。')
        source = BeautifulSoup(html,"html5lib")
        genders=source.find('span',class_='item gender')
        #genders=source.xpath('//*[@id="zh-pm-page-wrap"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span/i/@class')
        if genders:
            if genders.i['class'][1] == 'icon-profile-male':
                gender='男'
            elif genders.i['class'][1] == 'icon-profile-female':
                gender='女'
        else:
                gender='未知'
        try:
            name=source.find('div',class_='title-section ellipsis').a.string
        except AttributeError as e:
            print('查找名字出错！，正在重新找。。'+url)
            try:
                html= requests.get(url+'/about',cookies=cookie).text
                source = BeautifulSoup(html,"html5lib")
                name=source.find('div',class_='title-section ellipsis').a.string
            except AttributeError as e:
                print('查找名字出错！将会跳过本条记录')
        business = PIitem(source.find('span',class_='business item'))
        locations= PIitem(source.find('span',class_='location item'))
        companys = PIitem(source.find('span',class_='employment item'))
        posts    = PIitem(source.find('span',class_='position item'))
        schools  = PIitem(source.find('span',class_='education item'))
        professionals=PIitem(source.find('span',class_='education-extra item'))
        mylock.acquire()
        information[url]=name,gender,business,locations,companys,posts,schools,professionals
        mylock.release()
        print(len(information),'/',len(list_urls))
        
#解析出问题时运行
def inerror():
    for each in information:
        if each in list_urls:
            list_urls.pop()
    personalInformation(list_urls)
    

#将URL写入本地文件
def writeUlrs(urls):
     with open('all_url.txt','w') as f:
        for each in urls:
            f.write(each+'\n')   
           
#存入数据库
def mongo(information):
    for each in information:
        db.info.insert({'主页':each,'姓名':information[each][0],'性别':information[each][1],'行业':information[each][2],'住址':information[each][3],'公司':information[each][4],'职位':information[each][5],'学校':information[each][6],'专业':information[each][7]})
        #db.test.insert({'url':each})
         
def main():
    threadNum=int(input('输入线程数(建议四个以内)：'))
    for i in range(threadNum):
        all_url.append([input('线程'+str(i+1)+':::输入第一个主页地址：')])
    total=int(input('输入爬取层数：'))
    createGetUrlThreads(all_url,total)
    for each in allthread_u:
        each.join()
    print('用户查找完毕！\n正在搜集用户信息......')
    createGetInforThreads(list_urls)
    for each in allthread_i:
       each.join()
    print('用户信息搜集完毕！\n存入数据库...')
    mongo(information)
    #mongo(list_urls)
    print('信息存入完毕！')
    print('\n当前集合已有url（含未存入数据库）：',len(set_urls))
    print('本次搜集未重复：',len(list_urls))
    print('全部查看的url：',len(temps))
    print('本次存入有效url：',len(information))
    print('当前数据库已有url:',db.info.count())
    end = datetime.now()
    print('\n!!!!!抓取完毕!!!!!!\n花费时间：'+str(end-start))                                    

if __name__=='__main__':
    init()
    main()
