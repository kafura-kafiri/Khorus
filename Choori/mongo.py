from functools import wraps
import asyncio
from pymongo.errors import CollectionInvalid, ServerSelectionTimeoutError
import datetime


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
    async def insert(self, options, payload, D):
        if type(D) is dict:
            D = [D]
        if '--author' in options:
            for d in D:
                d['_inserting_author'] = payload['username']
        if '--date' in options:
            now = datetime.datetime.now()
            for d in D:
                d['_inserting_date'] = now
        if '--bulk' in options:
            bulk = self.cache['bulk']
            if len(bulk) < 10:
                bulk.extend(D)
            if len(bulk) >= 10:
                result = await self.collection.insert_many(bulk)
                bulk.clear()
            else:
                return {'status': 'bulked'}
        else:
            result = await self.collection.insert_many(D)
        return [str(_id) for _id in result.inserted_ids]

    @try_out("can't delete")
    async def delete(self, options, payload, query):
        if '--query' in options:
            query[options['--query']] = payload['username']
        return await self.collection.delete_many(query)

    @try_out("can't update")
    async def update(self, options, payload, query, updating_json):
        if '--query' in options:
            query[options['--query']] = payload['username']
        if '--author' in options:
            if '$set' not in updating_json:
                updating_json['$set'] = {}
            updating_json['$set']['_updating_author'] = payload['username']
        if '--date' in options:
            if '$set' not in updating_json:
                updating_json['$set'] = {}
            updating_json['$set']['_updating_date'] = datetime.datetime.now()
        return await self.collection.update(query, updating_json)

    @try_out("can't find")
    async def find(self, options, payload, query, project=None, sort=None, skip=None, limit=None):
        if '--query' in options:
            query[options['--query']] = payload['username']
        args = [query]
        if project is not None:
            args.append(project)
        documents = self.collection.find(*args)
        if skip is not None:
            documents = documents.skip(skip)
        if limit is not None:
            documents = documents.limit(limit)
        if sort is not None:
            sort = [(key, value) for key, value in sort.items()]
            documents = documents.sort(sort)
        documents = await documents.to_list(None)
        for doc in documents:
            del doc['_id']
        return documents

    @try_out("can't aggregate")
    async def aggregate(self, options, payload, aggregation):
        documents = await self.collection.aggregate(aggregation).to_list(None)
        return documents
