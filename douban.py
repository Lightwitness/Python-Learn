import requests
from lxml import etree
from datetime import datetime
class douban():
    def __init__(self):    #初始化
        print('正在执行请求：......\n')


    def getSource(self,url):    #获取网页源代码
        html=requests.get(url).text
        return html


    def getlis(self,html):    #获取所有li标签
        item=etree.HTML(html)
        all_li=item.xpath('//ol[@class="grid_view"]/li')
        return all_li


    def changeUrl(self,start):    #改变url
        url='http://movie.douban.com/top250?start='+str(start)+'&filter=&type='
        return url


    def getInfo(self,li):    #获取具体信息
        info={}
        title_info=li.xpath('div[@class="item"]/div[@class="info"]/div[@class="hd"]')[0]
        title=title_info.xpath('string(.)')
        title=title.replace('\n','/').replace(' ','').replace('\xa0/\xa0','/').replace('//','/')
        info['movie_title']=title    #电影标题

        dir_act_info=li.xpath('div[@class="item"]/div[@class="info"]/div[@class="bd"]/p')[0]
        dir_act=dir_act_info.xpath('string(.)')
        dir_act=dir_act.replace('\n','/').replace('  ','-').replace('\xa0','').replace('\xa0','').replace('//','/')
        info['dir_act']=dir_act    #导演和演员信息

        #info['star']=li.xpath('div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/em/text()')    #评分&评价
        
        info['Evaluation']=li.xpath('div[@class="item"]/div[@class="info"]/div[@class="bd"]/div/span/text()')    #评价
        
        quote=li.xpath('div[@class="item"]/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()')    #经典语句
        if quote:
            info['quote']=quote
        else:
            info['quote']=['无']
        return info


    def saveInfo(self,info,index):    #保存信息
        f.writelines('===电影排名：'+str(index)+'=== \n')
        f.writelines('电影标题：'+str(info['movie_title'])+'\n')
        f.writelines('导演/演员：'+str(info['dir_act'])+'\n')
        f.writelines('电影评分：'+str(info['Evaluation'][0])+'\n')
        f.writelines('电影评价：'+str(info['Evaluation'][1])+'\n')
        f.writelines('经典台词：'+str(info['quote'][0])+'\n\n\n')



if __name__ == '__main__':
    time1=datetime.now()
    inpage=int(input("输入爬取的页数（最多10页）："))
    pages=inpage if inpage <= 10 else 10
    spider=douban()
    index=1
    with open('top250.txt','w',encoding='utf-8') as f:
     for page in range(0,pages):
        print('正在爬取第'+str(page+1)+'页:')
        start=25*page
        url=spider.changeUrl(start)
        print('处理URL: '+url)
        html=spider.getSource(url)
        all_li=spider.getlis(html)
        
        for li in all_li:
            info=spider.getInfo(li)
            spider.saveInfo(info,index)
            index=index+1
    time2=datetime.now()    
    print('\n 爬取完成!!!')
    print(' 用时：'+str(time2-time1))
    f.close()
