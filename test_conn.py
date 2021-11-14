import redis
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

host = '172.17.0.2'
port_redis = 6379
# r = redis.StrictRedis(host,port_redis)
# print(r.ping())

port_mongo = 27017
conn = AsyncIOMotorClient('mongodb://root:1@172.17.0.2:27017/')
print(conn.server_info())