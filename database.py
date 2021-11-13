import pymongo

class MyDB():
    def __init__(self,host,port, dbName):
        self.conn = pymongo.MongoClient(host = host, port = port)
        self.db = self.conn[dbName]

    def save_set(self,setName,data):
        # 如果 data 为 json则直接保存，否则构造字典再保存
        if isinstance(data,dict):
            self.db[setName].save(data)
        else:
            self.db[setName].save({"data":data})
