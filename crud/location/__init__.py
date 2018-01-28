from Choori.mongo import Mongo
from Choori.decorators import privileges, retrieve
from config import location as config, crud_path
import os
from sanic import Blueprint
from sanic.response import json
from crud import prime

locations = Mongo(config['collection']['name'], config['collection']['indexes'])
bp = Blueprint(config['name'], url_prefix=config['path'])
prime(bp, locations, os.path.join(crud_path, config['name']), config)


@bp.route('/send-location', methods=['POST', ])
@privileges('porter', 'dev', )
@retrieve(
    '<num:form:lat>', 
    '<num:form:lng>', 
)
async def send_location(request, payload, lat, lng, ):
    
    options = [
        "--username",
        "--bulk",
        "--date",
    ]
    
    d = {
        "lat": lat,
        "lng": lng
    }
    
    return json(await locations.insert(options, payload, d, ))