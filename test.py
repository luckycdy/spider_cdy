import requests
from lxml import etree
import redis
import asyncio,aiohttp
import time
import pymongo
# conn = pymongo.MongoClient('localhost',27017)
conn = pymongo.MongoClient('127.0.0.1',27017)
# print(111111111111111111111111111111111111111111111111111111111)
# myclient = pymongo.MongoClient()
# myclient = pymongo.MongoClient('mongodb://localhost:27017/')
# mydb = myclient["runoobdb"]
# mycol = mydb["sites"]
# print(111111111111111111111111111111111111111111111111111111111)
# try:
#     print(myclient.server_info())                   # 输出服务信息
# except Exception:
#     print("无法连接到MongoDB服务") 
# myclient = pymongo.MongoClient('mongodb://localhost:27017/')
 
# dblist = myclient.list_database_names()
# # dblist = myclient.database_names() 
# if "runoobdb" in dblist:
#   print("数据库已存在！")
# print(myclient.list_database_names())
db = conn.nicedb # 指定数据库名称，连接nicedb数据库，没有则自动创建
my_set = db.test_set # 使用test_set集合，没有则自动创建
# my_set.save({"test":111})
# 以上两步都是延时操作，当往数据库插入第一条数据的时候，才会真正的创建数据库和集合
header = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; PCRT00 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36"}

# decode_responses=True，记得加这个参数，不加的话取出来的数据都是bytes类型的
r = redis.StrictRedis(host = '127.0.0.1', port = 6379, db = 2,decode_responses=True)
# pool = redis.ConnectionPool(host = '127.0.0.1', port = 6379, db = 2)
# r = redis.StrictRedis(connection_pool=pool,decode_responses=True)

def master(page):
    url = 'https://tieba.baidu.com/f?kw=美女&ie=utf-8&pn={}'.format(page*50)
    base = 'https://tieba.baidu.com'
    res = requests.get(url,headers=header).text
    print(res)
    html = etree.HTML(res)
    half_urls = html.xpath("//div[@class='threadlist_title pull_left j_th_tit ']/a/@href")
    print(half_urls)
    full_urls = [base + i for i in half_urls]
    for url in full_urls:
        # 从url_list列表头部塞任务，也就是url
        r.lpush('url_list',url)
    #print(r.llen('url_list'))

async def get_html(url):
    async with asyncio.Semaphore(5):  # 限制并发数为5个
        async with aiohttp.ClientSession() as session:
            async with session.get(url,headers=header) as html:
                # errors='ignore'，不加这个参数的话，会报错，具体错误内容见下面图片
                response = await html.text(encoding='utf-8',errors='ignore')
                return response
async def parse():
    while True:
        # 从redis的url_list列表取任务，从右边开始取
        url = r.rpop('url_list')
        if url == None:
            break
        # 判断这个任务是否已经做过了，也就是判断这个url在没在redis的history集合里
        if r.sismember('history',url) == 1:
            continue
        response = await get_html(url)
        html = etree.HTML(response)
        content = html.xpath("//div[@class='left_section']/div[2]/div[1]//cc/div[1]/text()")
        if content:
            content = content[0].strip()
        # content = html.xpath('//*[@id="post_content_141917793831"]/div/div/video')[0].strip()
        if content != '':
            # 当内容不为空时，将内容存到mongo里
            my_set.save({'content':content})
            print("成功")
            #print(content)
        # 将爬取过的任务放到redis的history集合里，也就是已完成任务队列
        r.sadd('history', url)
# master(1)
# t1 = time.time()
# 爬取前10页
for i in range(1):
    master(i)

# async的一些步骤
loop = asyncio.get_event_loop()
tasks = [parse() for _ in range(15)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# t2 = time.time()
# print(t2-t1)
# 最后用时：32.930299043655396
# 把mongo数据库换成mysql后，用时：43.06192493438721
