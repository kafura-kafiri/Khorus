from Choori.mongo import Mongo
from Choori.decorators import privileges, retrieve
from config import order as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from crud import prime

orders = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, orders, os.path.join(crud_path, config['name']), config)


@bp.route('/init'.format(), methods=['POST', ])
@privileges('dev', 'applicator', )
@retrieve(
    '<dict:form:applicator>', 
    '<dict:form:object>', 
    '<list:form:src>', 
    '<list:form:dst>', 
    '<num:form:delay>', 
)
async def init(request, payload, applicator, object, src, dst, delay, ):
    
    options = [
        "--date"
    ]
    
    d = {
        "applicator": applicator,
        "object": object,
        "src": src,
        "dst": dst,
        "status": "init",
        "delay": delay,
        "road_id": "",
        "username": ""
    }
    
    return json(await orders.insert(options, payload, d, ))


@bp.route('/<{_id}>/@delay:<{delay}'.format(_id='_id', delay='delay', ), methods=['POST', ])
@privileges('dev', 'applicator', )
@retrieve(
)
async def _delay(request, payload, _id, delay, ):
    
    options = []
    
    query = {
        "_id": _id
    }
    
    node = "delay"
    
    d = delay
    
    operator = "inc"
    
    return json(await orders.update(options, payload, query, node, d, operator, ))
