import asyncio
import uvloop

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid, ServerSelectionTimeoutError

db_name = 'CHOORI'
users_collection = 'users'
roads_collection = 'roads'
orders_collection = 'orders'
locations_collection = 'locations'
histories_collections = 'histories'

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

connection = AsyncIOMotorClient(
    host='127.0.0.1',
    port=27017,
    connectTimeoutMS=20000,
    serverSelectionTimeoutMS=50000,
)



db = connection[db_name]
users = db[users_collection]
users_indexes = []
roads = db[roads_collection]
roads_indexes = []
orders = db[orders_collection]
orders_indexes = []
locations = db[locations_collection]
locations_indexes = []
histories = db[histories_collections]
histories_indexes = []
