from Choori.mongo import Mongo
from Choori.decorators import privileges, retrieve
from config import order as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from crud import prime
from bson import ObjectId
import datetime

orders = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, orders, os.path.join(crud_path, config['name']), config)


@bp.route('/init'.format(), methods=['POST', ])
@privileges('dev', 'applicator', )
@retrieve(
    '<dict:form:object>', 
    '<list:form:src>', 
    '<list:form:dst>', 
    '<num:form:delay>', 
)
async def init(request, payload, object, src, dst, delay, ):
    
    options = [
        "--date"
    ]
    
    d = {
        "applicator": payload['username'],
        "object": object,
        "src": src,
        "dst": dst,
        "status": "init",
        "delay": delay,
    }
    
    return json(await orders.insert(options, payload, d, ))


@bp.route('/<{_id}>/@delay:<{delay}>'.format(_id='_id', delay='delay', ), methods=['POST', ])
@privileges('dev', 'applicator', )
@retrieve(
)
async def _delay(request, payload, _id, delay, ):
    
    options = []
    
    query = {
        "_id": ObjectId(_id)
    }
    
    node = "delay"
    
    d = int(delay)
    
    operator = "inc"
    
    return json(await orders.update(options, payload, query, node, d, operator, ))


@bp.route('/unassigned'.format(), methods=['POST', ])
@privileges('dev', 'khorus', 'operator', )
@retrieve(
)
async def unassigned(request, payload, ):
    
    options = []
    
    query = {
        "username": {
            "$exists": False
        }
    }
    
    projection = {}
    
    return json(await orders.find(options, payload, query, projection, ))


@bp.route('/history-back:<{days}>'.format(days='days', ), methods=['POST', ])
@privileges('dev', 'porter', )
@retrieve(
)
async def history_from(request, payload, days, ):
    
    options = [
        "--me"
    ]

    days_ago = datetime.datetime.now() - datetime.timedelta(days=int(days))
    query = {
        "_date": {
            "$gte": days_ago
        }
    }
    
    group = {
        "count": {
            "$sum": 1
        },
        "year_month_day": {
            "$first": "$year_month_day"
        },
        "_id": "$year_month_day",
    }
    
    projection = {
        "year_month_day": {
            "$dateToString": {
                "format": "%Y-%m-%d",
                "date": "$_date"
            }
        },
        "count": {
            "$dateToString": {
                "format": "%H:%M:%S:%L",
                "date": "$_date"
            }
        }
    }
    
    foreign = None
    
    return json(await orders.aggregate(options, payload, query, group, projection, foreign, ))


@bp.route('/<{_id}>/@road_id=<{road_id}>'.format(_id='_id', road_id='road_id', ), methods=['POST', ])
@privileges('khorus', 'dev', 'operator', )
@retrieve(
)
async def set_road(request, payload, _id, road_id, ):
    
    options = []
    
    query = {
        "_id": ObjectId(_id)
    }
    
    node = "road_id"
    
    d = ObjectId(road_id)
    
    operator = "set"
    
    return json(await orders.update(options, payload, query, node, d, operator, ))
