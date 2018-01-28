from Choori.mongo import Mongo
from Choori.decorators import privileges, retrieve
from config import road as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from crud import prime
import datetime
from bson import ObjectId
from crud.order import orders

roads = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, roads, os.path.join(crud_path, config['name']), config)


@bp.route('/init/'.format(), methods=['POST', ])
@privileges('dev', 'khorus', 'operator', )
@retrieve(
    '<num:form:src_lat>',
    '<num:form:src_lng>',
    '<num:form:dst_lat>',
    '<num:form:dst_lng>',
)
async def init(request, payload, src_lng, src_lat, dst_lng, dst_lat, ):
    
    options = [
        "--date"
    ]
    
    d = {
        "src": [
            src_lat,
            src_lng
        ],
        "dst": [
            dst_lat,
            dst_lng
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
        "_id": ObjectId(_id)
    }
    
    node = "username"
    
    d = payload['username']  # --username
    
    operator = "set"

    order_result = await orders.update(options, payload, {"road_id": ObjectId(_id)}, node, d, operator)
    road_result = await roads.update(options, payload, query, node, d, operator, )
    return json([order_result, road_result])


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
        "_date": {"$gte": today}
    }
    
    projection = {}
    
    return json(await roads.find(options, payload, query, projection, ))
