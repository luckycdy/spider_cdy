import redis
import asyncio
# import spider

class MyRedis():
    def __init__(self,host,port) -> None:
        self.r = redis.StrictRedis(host = host, port = port,db = 2,decode_responses=True)
        self.spi_num = 0

    def creatQueue(self,QName,serials):
        # 分布式只初始化一次即可
        is_exsit = self.r.scard('set_gen')
        if not is_exsit:
            self.r.sadd('set_gen',1)
            for serial in serials:
                self.r.lpush(QName,serial)

    def clearQueue(self,):
        self.r.delete('set_gen')

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
                await mydb.save_set(set_name,data)
            # print('成功')
            self.spi_num += 1
            self.r.sadd('history', url)      # 将该 URL 加入已爬取的集合中
            