from functools import wraps
import asyncio
from pymongo.errors import CollectionInvalid, ServerSelectionTimeoutError


def try_out(message):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            try:
                return await f(*args, **kwargs)
            except Exception as e:
                return {'status': message, 'error': str(e)}
        return decorated_function
    return decorator


class Mongo:
    def __init__(self, collection_name, indexes):
        self.collection = None
        self._collection_name = collection_name
        self._indexes = indexes
        self.cache = {
            'bulk': []
        }

    async def start(self, loop, db):
        print('connecting to mongodb! for creating collection: {}'.format(self._collection_name))
        try:
            await db.create_collection(self._collection_name)
        except CollectionInvalid:
            pass
        except ServerSelectionTimeoutError:
            await asyncio.sleep(0.5)
            print('trying to connect to mongodb again...')
            loop.create_task(self.start(loop, db))
            return

        self.collection = db[self._collection_name]
        # Indexes are supposed to be created here
        self.collection.drop_indexes()
        for index in self._indexes:
            self.collection.create_index(index)
        print('connected to mongodb! {} with indexes created'.format(self._collection_name))

    @try_out("can't insert")
    async def insert(self, D):
        if type(D) is list:
            result = await self.collection.insert_many(D)
            return [str(_id) for _id in result.inserted_ids]
        elif type(D) is dict:
            result = await self.collection.insert_one(D)
            return str(result.inserted_id)
        raise Exception

    @try_out("can't delete")
    async def delete(self, query):
        return await self.collection.delete_many(query)

    @try_out("can't update")
    async def update(self, query, document):
        return await self.collection.update(query, {'$set': document})

    @try_out("can't patch")
    async def patch(self, query, node, sub_document, mode):
        return await self.collection.update(query, {'${}'.format(mode): {node: sub_document}})

    @try_out("can't find")
    async def find(self, query, projection=None):
        if projection:
            documents = await self.collection.find(query, projection).to_list(None)
        else:
            documents = await self.collection.find(query).to_list(None)
        for doc in documents:
            del doc['_id']
        return documents

    @try_out("can't aggregate")
    async def aggregate(self, query, projection, ):
        pass

    @try_out("can't group")
    async def group(self, query, projection):
        pass
