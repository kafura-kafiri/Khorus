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


async def start_collection(loop, collection_name, indexes):
    print('connecting to mongodb! for creating collection: {}'.format(collection_name))
    try:
        await db.create_collection(collection_name)
    except CollectionInvalid:
        pass
    except ServerSelectionTimeoutError:
        await asyncio.sleep(0.5)
        print('trying to connect to mongodb again...')
        loop.create_task(start_collection(loop, collection_name, indexes))
        return

    # Indexes are supposed to be created here
    collection = db[collection_name]
    collection.create_indexes()
    print('connected to mongodb! {} with indexes created'.format(collection_name))

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

async def start_db(loop):
    await start_collection(loop, users_collection, users_indexes)
    await start_collection(loop, roads_collection, roads_indexes)
    await start_collection(loop, orders_collection, orders_indexes)
    await start_collection(loop, locations_collection, locations_indexes)
    await start_collection(loop, histories_collections, histories_indexes)