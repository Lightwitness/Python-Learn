import requests
from lxml import etree
import time
class wallhaven():
    def __init__(self):    #初始化
        print('正在执行请求：......')


    def getSource(self,url):    #获取网页源代码
        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'}
        html=requests.get(url,headers=header).text
        return html
        # image=requests.get(url).content
        # return image

    def getlis(self,html):    #获取所有li标签
        item=etree.HTML(html)
        all_li=item.xpath('//div[@id="thumbs"]/section[@class="thumb-listing-page"]/ul/li')
        print('本页有：',len(all_li),'张图片')
        return all_li


    def changeUrl(self,page):    #改变url
        #url='http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+str(num)+'.jpg'
        url='http://alpha.wallhaven.cc/random?page='+str(page)
        return url


    def getImage(self,li):    #获取具体信息
        src_small=li.xpath('figure/a/@href')[0]
        image_id=src_small[36:]
        src_full='http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+str(image_id)+'.jpg'
        image=requests.get(src_full).content
        return image

    def saveImage(self,image,index):    #保存信息
         f= open('C:/Users/FLCRS/temp/wallheavn-'+str(index)+'.jpg','wb')
         f.write(image)
         f.close()


if __name__ == '__main__':
    time1=time.time()
    pages=int(input("输入爬取的页数（最多7075页）："))
    # num=int(input('输入爬取的图片数量：'))
    # for each in range(num):
    #      url=spider.changeUrl(each) 
    #      image=spider.getSource(url)
    #      spider.saveImage(image,each)
    page=pages if pages <= 7075 else 7075
    spider=wallhaven()
    index=1
    for page in range(0,page):
        pic=1
        print('\n正在爬取第'+str(page+1)+'页:')
        url=spider.changeUrl(page+1)
        print('处理URL:'+url)
        html=spider.getSource(url)
        all_li=spider.getlis(html)
        for li in all_li:
            print('正在处理本页第',pic,'张图片')
            image=spider.getImage(li)
            spider.saveImage(image,index)
            index=index+1
            pic=pic+1
    time2=time.time()    
    print('\n 爬取完成!!!')
    print(' 用时：'+str(time2-time1))
