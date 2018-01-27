from Choori.mongo import Mongo
from Choori.decorators import privileges, retrieve
from config import road as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from crud import prime
import datetime

roads = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, roads, os.path.join(crud_path, config['name']), config)


@bp.route('/init'.format(), methods=['POST', ])
@privileges('dev', 'khorus', 'operator', )
@retrieve(
    '<num:form:src_lng>', 
    '<num:form:src_lat>', 
    '<num:form:dst_lng>', 
    '<num:form:dst_lat>', 
)
async def init(request, payload, src_lng, src_lat, dst_lng, dst_lat, ):
    
    options = [
        "--username",
        "--date"
    ]
    
    d = {
        "status": "init",
        "src": [
            src_lng,
            src_lat
        ],
        "dst": [
            dst_lng,
            dst_lat
        ]
    }
    
    return json(await roads.insert(options, payload, d, ))


@bp.route('/<{_id}>/<{ack}>'.format(_id='_id', ack='ack', ), methods=['POST', ])
@privileges('dev', 'porter', )
@retrieve(
)
async def ack(request, payload, _id, ack, ):
    
    options = []
    
    query = {
        "_id": _id
    }
    
    node = "status"
    
    d = ack
    
    operator = "set"
    
    return json(await roads.update(options, payload, query, node, d, operator, ))


@bp.route('/@status:<{status}>'.format(status='status', ), methods=['POST', ])
@privileges('dev', 'porter', )
@retrieve(
)
async def user_trips(request, payload, status, ):
    
    options = [
        "--me"
    ]

    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0)
    query = {
        "status": status,
        "_date": {"$gt": today}
    }
    
    projection = {}
    
    return json(await roads.find(options, payload, query, projection, ))
