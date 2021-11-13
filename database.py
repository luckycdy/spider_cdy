import pymongo
from motor.motor_asyncio import AsyncIOMotorClient

class MyDB():
    def __init__(self,host,port, dbName):
        self.conn = AsyncIOMotorClient(host = host, port = port)
        self.db = self.conn[dbName]

    async def save_set(self,setName,data):
        # 如果 data 为 json则直接保存，否则构造字典再保存
        if isinstance(data,dict):
            await self.db[setName].insert_one(data)
        else:
            await self.db[setName].insert_one({"data":data})
