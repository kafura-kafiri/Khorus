from Choori.mongo import Mongo
from Choori.decorators import privileges, retrieve
from config import user as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from crud import prime

users = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
authentication_bp = Blueprint('authentication')

prime(bp, users, os.path.join(crud_path, bp.name), config)

from crud.user import authentication


@bp.route('/init'.format(), methods=['POST', ])
@privileges()
@retrieve(
    '<str:form:username>', 
    '<str:form:password>', 
    '<str:form:first_name>', 
    '<str:form:last_name>', 
    '<str:form:cellphone>', 
)
async def new_user(request, payload, username, password, first_name, last_name, cellphone, ):
    
    options = []
    
    d = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "cellphone": cellphone,
        "salt": "",
        "privileges": {},
        "bank": {
            "name": "",
            "account": "",
            "fee_per_order": "",
            "fixed_salary": ""
        },
        "detail": {
            "probation": "",
            "melli_code": "",
            "birth_date": "",
            "sheba": ""
        }
    }
    
    return json(await users.insert(options, payload, d, ))


@bp.route('/<username>/add-privilege:<privilege>', methods=['POST', ])
@privileges('zoodfood', 'dev', )
@retrieve()
async def add_privilege(request, payload, privilege, username, ):
    
    options = []
    
    query = {
        "username": username
    }
    
    node = "privileges.{privilege}".format(privilege=privilege)
    
    d = {
        "status": "",
        "shift": {}
    }
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))


@bp.route('/@status:<{status}>'.format(status='status', ), methods=['POST', ])
@privileges('porter', )
@retrieve(
)
async def update_status(request, payload, status, ):
    
    options = [
        "--me"
    ]
    
    query = {}
    
    node = "privileges.porter.status"
    
    d = int(status)
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))


@bp.route('/@shift:<{shift}>=<{head}>,<{tail}>'.format(shift='shift', head='head', tail='tail'), methods=['POST', ])
@privileges('porter', )
@retrieve(
)
async def update_shift(request, payload, shift, head, tail, ):
    
    options = [
        "--me"
    ]
    
    query = {}
    
    node = "privileges.porter.shift.{shift}".format(shift=shift)
    
    d = [int(head), int(tail)]
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))
