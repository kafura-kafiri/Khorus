from motor.motor_asyncio import AsyncIOMotorClient

import asyncio
import uvloop
import os
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

client = AsyncIOMotorClient(
    host='127.0.0.1',
    port=27017,
    connectTimeoutMS=20000,
    serverSelectionTimeoutMS=50000,
)

crud_path = os.path.join(os.getcwd(), 'crud')
db_name = 'BLOODY_DB'
db = client[db_name]

blood_collection_name = 'blood_collection'
blood_collection_indexes = [[('blood_id', 1)]]

user = {
    'name': 'user',
    'path': 'users',
    'collection': {
        'name': 'users',
        'indexes': [
            [('username', 1)]
        ]
    }
}

location = {
    'name': 'location',
    'path': 'locations',
    'collection': {
        'name': 'locations',
        'indexes': [
            [('username', 1)]
        ]
    }
}

order = {
    'name': 'order',
    'path': 'orders',
    'collection': {
        'name': 'orders',
        'indexes': [
            [('username', 1)]
        ]
    }
}
road = {
    'name': 'road',
    'path': 'roads',
    'collection': {
        'name': 'roads',
        'indexes': [
            [('username', 1)]
        ]
    }
}
history = {
    'name': 'history',
    'path': 'histories',
    'collection': {
        'name': 'histories',
        'indexes': [
            [('username', 1)]
        ]
    }
}