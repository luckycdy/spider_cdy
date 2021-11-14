from spider import Spider
from redis_queue import MyRedis
# import redis
from database import MyDB
import json
import time

if __name__ == "__main__":
    with open('conf.json', 'r') as f:
        conf = json.load(f)
    # r = redis.StrictRedis(host = conf["host"], port = conf["Redis"]["port"],db = 2,decode_responses=True)
    myredis = MyRedis(host = conf["host"], port = conf["Redis"]["port"])
    # if r.ping():
    #     print("redis 已连接")
    mydb = MyDB(host = conf["host"], port = conf["DBMS"]["port"],dbName = conf["DBMS"]["database"],user=conf["DBMS"]["user"],pswd=conf["DBMS"]["password"])
    # if mydb.conn.server_info():
    #     print("mongo 已连接")
    myspider = Spider()

    start_time = time.time()

    myspider.main_news(mydb=mydb,myredis=myredis,lnum=378277,rnum=381277)

    
    end_time = time.time()
    use_time = end_time-start_time
    print(use_time)
    print(f'该机器爬取任务数量: {myredis.spi_num}')
