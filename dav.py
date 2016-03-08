from pymongo import MongoClient
mc=MongoClient('localhost',27017)
db=mc.fuli
# a=[]
# for each in db.allinfo.find({},{'_id':0}):
#     a.append((each['主页'],int(each['关注者'])))

# b=sorted(a,key=lambda x:x[1],reverse=True)
# for i,each1 in enumerate(b[0:100]):
#     for each2 in db.alldata.find({'主页':each1[0]},{'_id':0,'姓名':1}):
#         print(i+1,each1,each2['姓名'])
# input('输入任意字符结束！')    

# # a=db.alldata.find()
# # for each in a:
# #     for each in db.allinfo.find({'主页':each['主页']},{'_id':0}):
# #         db.alldata.update({'主页':each['主页']},{'$set':each})
# db.alldata.find({'主页':'http://www.zhihu.com/people/mokun'})
# a=db.alldata.find()
# a=1
# for info1 in db.allinfo.find({},{'_id':0,'主页':1}):
#     for info2 in db.allinfo.find({'主页':info1['主页']},{'_id':0,'主页':0}):
#         db.alldata.update({'主页':info1['主页']},{'$set':info2})
#         print(a)
#         a+=1
# b=1
# a=db.alldata.find({},{'_id':0})
# for each in a:
# ...     for each in db.allinfo.find({'主页':each['主页']},{'_id':0}):
# ...           db.alldata.update({'主页':each['主页']},{'$set':each})
#               print(b)
#               b+=1

x=set()            
for each in db.all.find({},{'主页':1,'_id':0}):
    x.add(each['主页'])             
count=db.alldata.count()
for data in db.alldata.find({},{'_id':0}):
    if data['主页'] not in x:
        for info in db.allinfo.find({'主页':data['主页']},{'_id':0,'主页':0}):
            db.all.insert(data)
            db.all.update({'主页':data['主页']},{'$set':info})
            print('进度：',db.all.count(),'/',count)

# a=[]
# count=db.test.count()
# i=1
# for each in db.test.find({},{'_id':0,'主页':1}):
#     a.append(each['主页'])
# for info in a:
#     for each in db.allinfo.find({'主页':info},{'_id':0,'主页':0}):
#         db.test.update({'主页':info},{'$set':each})
#         print('进度：',i,'/',count)
#         i+=1


# C:\Users\FLCRS\Desktop>mongoexport -d fuli -c all --type=csv --fields 学校,主页,姓名 >test.csv
# 2015-11-27T09:48:22.610+0800    connected to: localhost
# 2015-11-27T09:48:25.666+0800    exported 185891 records

# C:\Users\mongoexport -d fuli -c all --type=csv --fields 主页,姓名,性别,学校,专业,职位,住址,行业,公司,回答,提问,收藏,关注专栏,获得分享,公共编辑,关注了,关注者,关注话题,获得赞同,专栏文章,获得感谢 >test.csv
# 2015-11-27T10:00:35.716+0800    connected to: localhost
# 2015-11-27T10:00:47.429+0800    exported 189012 records

# C:\Users\FLCRS\Desktop>


# for each in db.allinfo.find({},{'_id':0}):
#     db.alldata.update({'主页':each['主页']},{'$set':each})