from sanic import Sanic

from Choori.decorators import privileges, retrieve
from Choori.mongo import Mongo

users = Mongo()

app = Sanic(__name__)

'''
let's generate
'''


@app.route('/send_location', methods=['POST', 'GET'])
@privileges(['dev', 'admin'])
@retrieve([
    '<float:form:lat>',
    '<float:form:lng>',
    '<str:form:username>',
])
async def send_location(request, options, lat, lng, username):
    args = render()
    return users.insert(*args)
