from motor.motor_asyncio import AsyncIOMotorClient

import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

client = AsyncIOMotorClient(
    host='127.0.0.1',
    port=27017,
    connectTimeoutMS=20000,
    serverSelectionTimeoutMS=50000,
)

db_name = 'BLOODY_DB'
db = client[db_name]

blood_collection_name = 'blood_collection'
blood_collection_indexes = [[('blood_id', 1)]]

paper = {
    'name': 'paper',
    'path': 'papers',
    'collection': {
        'name': 'papers',
        'indexes': [
            [('title', 1)]
        ]
    }
}
user = {
    'name': 'user',
    'path': 'users',
    'collection': {
        'name': 'users',
        'indexes': [
            [('title', 1)]
        ]
    }
}