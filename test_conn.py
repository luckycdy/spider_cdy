import redis
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

host = '172.17.0.2'
port_redis = 6379
r = redis.StrictRedis(host,port_redis)
print(r.ping())

is_exsit = r.scard('set_gen')
print(is_exsit)
if not is_exsit:
    print(11111)
    r.sadd('set_gen',1)
# r.set('set_gen','ss')
# test = r.get("set_gen")
test = r.scard("set_gen")
print(test)
# port_mongo = 27017
# conn = AsyncIOMotorClient('mongodb://root:1@172.17.0.2:27017/')
# print(conn.server_info())