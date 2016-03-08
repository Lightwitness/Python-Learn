import requests
from lxml import etree
import re
import threading

 #print('---------开始工作-------')
 #header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
 header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'}
 #url='http://jandan.net/ooxx/page-'+str(page)+'1589#comments'
 #html=requests.get(url,headers=header).content
 #html=html.decode('utf8')
 #source=etree.HTML(html)
 #meiziurls=source.xpath('//li[starts-with(@id,"comment")]/div/div[@class="row"]/div[@class="text"]/p/img/@src')
 
def patu(self,page):
     #for index,page in enumerate(range(1400,1400+pages))
     print('\n------正在爬取第',page,'页------')
     url='http://jandan.net/ooxx/page-'+str(page)+'#comments'
     html=requests.get(url,headers=header).content
     html=html.decode('utf8')
     if re.findall('.*?屏蔽.*?',html):
         html2=requests.get('http://jandan.net/block.php?from=http%3A%2F%2Fjandan.net%2Fooxx%2Fpage-'+str(page)).content.decode('utf8')
         hash_info=re.findall('value="(.*?)"',html2)[1]
         data={'form':'http://jandan.net/ooxx/page-'+str(page),'hash':hash_info}
         html=requests.post('http://jandan.net/block.php?action=check_human',data=data,headers=header).content.decode('utf8')
     else:
      source=etree.HTML(html)
      meiziurls=source.xpath('//li[starts-with(@id,"comment")]/div/div[@class="row"]/div[@class="text"]/p/img/@src')
      for meizi in meiziurls:
         print('正在爬取本页第',index+1,'张图片......')
         meizitu=requests.get(meizi).content
         if meizi[-3:] == 'jpg':
            f=open('C:/Users/FLCRS/temp/'+str(page)+'页第'+str(index+1)+'张无聊图.jpg','wb')
            f.write(meizitu)
            f.close()
            index=index+1
         else:
            f=open('C:/Users/FLCRS/temp/'+str(page)+'页第'+str(index+1)+'无聊图.gif','wb')
            f.write(meizitu)
            f.close()
            index=index+1
 
def getRange(self,pageStart,pageEnd):
       for i in range(pageStart,pageEnd):
             patu(i)
 
if __name__ == '__main__':
        pages=int(input('请输入页数:'))
        pageStart = 1400
        pageEnd = 1400+pages
        totalThread = 2
        gap = int((pageEnd - pageStart) / totalThread)
        mutex = threading.Lock()
        for i in range(pageStart,pageEnd,gap):
              t = threading.Thread(target=getRange,args=(pageStart,pageStart+gap))
              t.start()
        print('\n。。。。爬取完成！。。。。。')
        
