from Choori.mongo import Mongo
from Choori.decorators import privileges, retrieve
from config import road as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from crud import prime

roads = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, roads, os.path.join(crud_path, config['name']), config)