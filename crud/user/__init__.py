from Choori.mongo import Mongo
from config import user as config
from sanic import Blueprint
from crud import prime

users = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, users)

from crud.user import authentication