from Choori import Choori
from config import db
from crud.user import bp as user, users, authentication_bp as auth
from crud.location import bp as location, locations
from crud.order import bp as order, orders
from crud.road import bp as road, roads
from crud.history import bp as history, histories

server = Choori(db)
server.blueprint(auth, users)
server.blueprint(user, users)
server.blueprint(location, locations)
server.blueprint(order, orders)
server.blueprint(road, roads)
server.blueprint(history, histories)
server.run()
