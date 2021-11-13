# import requests
import aiohttp
import asyncio
import json
# import functools


class Spider():
    def __init__(self) -> None:
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; TAS-AN00 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 dzhapp;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:140248;packageName:com.android.dazhihui',
            }

    def gen_url_news(self,lnum=379990,rnum=380000):
        # 大智慧 news url 规律
        url = lambda id: f'https://detailpage.dzh.com.cn/index.php?service=getNewsContent&id=topkuaixun-{id}&version=&token='
        # full_urls = [url(i) for i in range(lnum,rnum)]
        for i in range(lnum,rnum):
            yield url(i)

    async def get_data(self,url,method="get",data=None,sem_num=32):
        async with asyncio.Semaphore(sem_num):  # 限制并发数为5个
            async with aiohttp.ClientSession(headers=self.header) as session:
                async with session.get(url) as resp:
                    # errors='ignore'，不加这个参数的话，会报错，具体错误内容见下面图片
                    # response = await resp.text(encoding='utf-8',errors='ignore')
                    data = await resp.read()
                    # print(data)
                    return data

    def callback(self,mydb,set_name,task):
        mydb.save_set(set_name,task.result())
        # if method=="get":
        #     return requests.get(url,headers=self.header)
        # elif method== "post":
        #     return requests.post(url,headers=self.header,data=data)

    async def parse_news(self,url):
        data = await self.get_data(url)
        json_news = json.loads(data)
        # 如果找到数据，则返回。否则返回 False
        if not json_news["Data"]["Found"]:
            return False
        return json_news

    async def strat_queue(self,myredis,mydb,set_name):
        await myredis.run_redis(self,mydb,set_name)

    def main_news(self,mydb,myredis,set_name='dzh_news',lnum=370100,rnum=370101):
        # tasks = [asyncio.ensure_future(test.request(url(id))) for id in range(379132,379133)]
        # for id in range(379132,379133):
        tasks = []
        myredis.creatQueue('url_list',self.gen_url_news(lnum,rnum))

        for _ in range(32):
            task = asyncio.ensure_future(self.strat_queue(myredis,mydb,set_name))
            # task.add_done_callback(functools.partial(self.callback, mydb,set_name))
            tasks.append(task)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()