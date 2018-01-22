class Mongo:
    def __init__(self, collection, cache):
        self.collection = collection
        self.cache = cache

    @handle_exp()
    async def insert(self, D):
        if D is list:
            return await self.collection.insert_many(D)
        elif D is dict:
            return await self.collection.insert_one(D)
        return

    async def delete(self, query):
        return await self.collection.delete_many(query)

    async def update(self, query, document):
        return await self.collection.update(query, {'$set': document})

    async def patch(self, query, node, sub_document, mode):
        return await self.collection.update(query, {'${}'.format(mode): {node: sub_document}})

    async def find(self, query, projection):
        return await self.collection.update(query, projection)

    async def aggregate(self, query, projection, ):
        pass

    async def group(self, query, projection):
        pass
