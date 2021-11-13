import redis
import asyncio
# import spider

class MyRedis():
    def __init__(self,host,port) -> None:
        self.r = redis.StrictRedis(host = host, port = port,db = 2,decode_responses=True)

    def creatQueue(self,QName,serials):
        for serial in serials:
            self.r.lpush(QName,serial)

    # def setQueue(self,QName,data):
    #     if self.r.sismember(QName,data):
    #         return False
        
    async def run_redis(self,myspider,mydb,set_name):
        while True:
            url = self.r.rpop('url_list')
            if url == None:
                break
            # 是否已爬取
            if self.r.sismember('history',url):
                continue
            # response = myspider.get_response(url)
            data = await myspider.parse_news(url)
            # 如果有数据则保存
            if data:
                mydb.save_set(set_name,data)
            self.r.sadd('history', url)      # 将该 URL 加入已爬取的集合中
            