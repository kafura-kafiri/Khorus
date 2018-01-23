from Choori.mongo import Mongo
from config import paper as config
from sanic import Blueprint
from crud import prime

papers = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, papers)
