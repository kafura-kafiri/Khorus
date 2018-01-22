from sanic import Sanic
from Choori import app
from Choori.decorators import privileges, retrieve, options

@options
@app.route('/symlink')
@privileges(['dev'])
@retrieve([
    '<dict:form:symlink>',
    '<dict:form:inputs>',
])
async def __symlink__(request, options, symlink, inputs):