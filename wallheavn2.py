import requests
from lxml import etree
import time


if __name__ == '__main__':
    time1=time.time()
    pages=int(input("pageNum:"))
    for page in range(1,pages):
        pic=1
        index=1
        print('\zhangzaipaqu'+str(page+1)+'ye:')
        url='http://alpha.wallhaven.cc/random?page='+str(page)
        print('url:'+url)
        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'}
        html=requests.get(url,headers=header).text
        item=etree.HTML(html)
        all_li=item.xpath('//div[@id="thumbs"]/section[@class="thumb-listing-page"]/ul/li')
        print('this page',len(all_li),'Pictures')
        for li in all_li:
            print('chulidi',pic,'Picture')
            src_small=li.xpath('figure/a/@href')[0]
            image_id=src_small[36:]
            src_full='http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+str(image_id)+'.jpg'
            image=requests.get(src_full).content
            with open('/home/kity/Pictures/wallheavn-'+str(index)+'.jpg','wb') as f:
                f.write(image)
            index=index+1
            pic=pic+1

    time2=time.time()    
    print('\n ok!!!')
    print(' time'+str(time2-time1))