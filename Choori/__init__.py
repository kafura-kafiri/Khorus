import asyncio
from sanic import Sanic


class Choori:
    def __init__(self, db):
        self.app = Sanic(__name__)
        self.nodes = []
        self.db = db

    def blueprint(self, bp, mongo):
        self.nodes.append((bp, mongo))
        self.app.blueprint(bp)

    def run(self):
        server = self.app.create_server(
            host='127.0.0.1',
            port=5000,
            debug=True,
        )

        asyncio.ensure_future(server)
        loop = asyncio.get_event_loop()

        async def start_db():
            for node in self.nodes:
                await node[1].start(loop, self.db)
        loop.create_task(start_db())

        # Start other asyncio things here
        loop.run_forever()

