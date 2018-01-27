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
        "privilages": {},
        "bank": {
            "name": "",
            "account": "",
            "fee_per_order": "",
            "fixed_salary": ""
        },
        "detail": {
            "probation": "",
            "mellicode": "",
            "birthdate": "",
            "sheba": ""
        }
    }
    
    return json(await users.insert(options, payload, d, ))


@bp.route('/<username>/add-privilege:<privilege>', methods=['POST', ])
@privileges('Z', 'O', )
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
@privileges('dev', 'porter', )
@retrieve(
)
async def update_status(request, payload, status, ):
    
    options = [
        "--me"
    ]
    
    query = {}
    
    node = "status"
    
    d = status
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))


@bp.route('/@shift'.format(), methods=['POST', ])
@privileges('dev', 'porter', )
@retrieve(
    '<list:form:shift>', 
)
async def update_all_shifts(request, payload, shift, ):
    
    options = [
        "--me"
    ]
    
    query = {}
    
    node = "shift"
    
    d = shift
    
    operator = "set"
    
    return json(await users.update(options, payload, query, node, d, operator, ))
