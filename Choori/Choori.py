import asyncio
from sanic import Sanic
from config import start_db

from crud.user import auth_bp as authentication
from crud.user import bp as user
from crud.road import bp as road
from crud.order import bp as order
from crud.location import bp as location
from crud.history import bp as history

app = Sanic(__name__)
app.blueprint(authentication)
app.blueprint(user)
app.blueprint(road)
app.blueprint(order)
app.blueprint(location)
app.blueprint(history)


def main():
    server = app.create_server(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )

    asyncio.ensure_future(server)
    loop = asyncio.get_event_loop()
    loop.create_task(start_db(loop))

    # Start other asyncio things here
    loop.run_forever()


if __name__ == '__main__':
    main()
