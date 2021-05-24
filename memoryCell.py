# the database to be implemented is a mongo db
import pymongo
from bson.objectid import ObjectId
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["MemoryCell"]
btc_coll = mydb["BTC4HourCandleStick"]
eth_coll = mydb["ETH4HourCandleStick"]


def memory_update(dict, coll):
    # This function takes 2 parameters coll; collection name and dict; the dict obj to be stored
    coll.insert_one(dict)
def get_last_updated_doc(coll):
    D = []
    var = coll.find().sort("Time", -1)
    for i in var:
         D.append(i)
         return D
#
# # print(get_last_updated_doc(btc_coll))
