import requests
from pymongo import MongoClient
from lxml import etree
import threading
cookie={'Cookie':'_za=e845c5d0-ecbe-4ea8-92a4-f251fa35466c; q_c1=1ee6953b2fd049f29171d79e26436020|1445780798000|1443087353000; cap_id="OTRmNmRkZjc2ZDFiNDUxZTgzYmQyNDRjMDYxNDc4YjA=|1446902765|e310eb84a4c91010f6ecd8ef2bfa53435e1d728b"; __utma=51854390.470477516.1443087355.1447043898.1447054060.9; __utmz=51854390.1446949347.3.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _xsrf=acf970e0903bb0de931493a3065d490f; _ga=GA1.2.470477516.1443087355; z_c0="QUJCTXl3c3E5d2dYQUFBQVlRSlZUU09KWlZadVBkRDJHMjIzNWQ2T3FKaGpzbXVZcVJCT2VBPT0=|1446902819|6e11b96e02ef250284777ef63c3eda7a37ab7d42"; __utmv=51854390.100-2|2=registration_date=20151106=1^3=entry_date=20150924=1; __utmb=51854390.2.10.1447054060; __utmc=51854390; __utmt=1'}

#递归查找用户
def getFollowees(urls):
    for url in urls: 
           temp=[]
           FolloweesPage=requests.get(url+'/followees',cookies=cookie).text
           selector=etree.HTML(FolloweesPage)
           Guanzhu_a=selector.xpath('//*[@id="zh-profile-follows-list"]/div/div/div[2]/h2/a')
           for everyone in Guanzhu_a:
                href=everyone.xpath('@href')[0]
                name=everyone.xpath('text()')[0]
                temp.append(href)
                if href not in hrefs:
                    hrefs.add(href)
                else:
                    print('已经存在：'+everyone.xpath('@href')[0]+'    '+everyone.xpath('text()')[0])
           return temp
        
# url='http://www.zhihu.com/people/fu-li-64-88'
#循环查找用户
def diedai(url):
     for one in getFollowees(url):
         for two in getFollowees(one):
            for three in getFollowees(two):
                print(len(hrefs))
#                for four in getFollowees(three):
#                     getFollowees(four)
                
        

#用户个人信息
def personalInformation(url):
    r = requests.get(url+'/about',cookies=cookie)
    source = etree.HTML(r.text)
    genders=source.xpath('//*[@id="zh-pm-page-wrap"]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span/i/@class')
    if genders:
        if genders[0] == "icon icon-profile-male":
            gender=['男']
        elif genders[0] == "icon icon-profile-female":
            gender=['女']
    else:
        gender=['未知']
    tempName=source.xpath('//div[@class="title-section ellipsis"]/a[@class="name"]/text()')
    tempBusiness=source.xpath('//span[@class="business item"]/@title')
    tempLocations=source.xpath('//span[@class="location item"]/@title')
    tempCompanys=source.xpath('//span[@class="employment item"]/@title')
    tempPosts=source.xpath('//span[@class="position item"]/@title')
    tempSchools=source.xpath('//span[@class="education item"]/@title')
    tempProfessionals=source.xpath('//span[@class="education-extra item"]/@title')
    temp=[tempName,gender,tempBusiness,tempLocations,tempCompanys,tempPosts,tempSchools,tempProfessionals]
    for i,eachTemp in enumerate(temp):
        if eachTemp == []:
            temp[i]=['未知']
    information[url]=temp[0][0],temp[1][0],temp[2][0],temp[3][0],temp[4][0],temp[5][0],temp[6][0],temp[7][0]

#写入信息
# def writedata(information):
#     with open('C:/Users/FLCRS/temp/data.txt','w') as f:
#         f.write('姓名      性别      行业      所在地     公司      职位      学校      专业 \n')
#         for each in information:
#             f.write(each+'\n')
#             for content in information[each]:
#                 f.write(content+'   ')
#将URL存入本地文件
def writeUlrs(urls):
     with open('all_url.txt','w') as f:
        for each in urls:
            f.write(each+'\n')   
           
#存入数据库
def mongo(information):
    mc=MongoClient('localhost',27017)
    db=mc.fuli
    for each in information:
              db.info.insert({'姓名':information[each][0],'性别':information[each][1],'行业':information[each][2],'所在地':information[each][3],'公司':information[each][4],'职位':information[each][5],'学校':information[each][6],'专业':information[each][6]})
              
                        
if __name__=='__main__':
    information={}
    hrefs=set()
    url=[input('输入一个主页地址：')]
    #total=int(input('输入爬取层数：'))
    #getFollowees(url,0,total)
    diedai(url)
    #writeUlrs(hrefs)
    print('用户查找完毕！\n正在搜集用户信息......')
    for url in hrefs:
          personalInformation(url)
          print(len(information),'/',len(hrefs))
    print('用户信息搜集完毕！\n存入数据库...')
    #writedata(information)
    #mongo(information)
    print('信息存入完毕！')
