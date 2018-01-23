from sanic.response import json
from Choori.decorators import options as handle_options, privileges, retrieve


def prime(bp, mongo):
    """

    :param bp:
    :param mongo:
    :return:
    """
    @bp.route('/', methods=['POST'])
    @bp.route('/-<options>', methods=['POST'])
    @handle_options()
    @privileges('dev')
    @retrieve(
        '<dict:form:query>',
        '<dict:form:projection>',
    )
    async def _get(request, options, payload, query, projection):
        return json(await mongo.find(query, projection))

    @bp.route('/', methods=['PUT'])
    @bp.route('/-<options>', methods=['PUT'])
    @handle_options()
    @privileges('dev')
    @retrieve(
        '<dict:form:d>'
    )  # add bulk, add user options.
    async def _post(request, options, payload, d):
        if '--username' in options:
            d['username'] = payload['username']
        if '--bulk' in options:
            bulk = mongo.cache['bulk']
            if len(bulk) < 10:
                bulk.append(d)
            if len(bulk) == 10:
                result = await mongo.insert(bulk)
                bulk.clear()
                return json(result)
        return json(await mongo.insert(d))

    @bp.route('/', methods=['DELETE'])
    @bp.route('/-<options>', methods=['DELETE'])
    @handle_options()
    @privileges('dev')
    @retrieve(
        '<dict:form:query>'
    )
    async def _delete(request, options, payload, query):
        return json(await mongo.delete(query))

    @bp.route('/', methods=['PATCH'])
    @bp.route('/-<options>', methods=['PATCH'])
    @handle_options()
    @privileges('dev')
    @retrieve(
        '<dict:form:query>',
        '<dict:form:node>',
        '<dict:form:d>'
    )
    async def _delete(request, options, payload):
        print(options)
        print(payload)
        return json({'few': 'few'})

    @bp.route('/send-location', methods=['POST'])
    @privileges(
        'dev',
        'porter'
    )
    @retrieve(
        '<float:form:lat>',
        '<float:form:lng>',
    )
    async def send_location(request, payload, lat, lng):
        options, payload, d = render('func_key', payload=payload, lat=lat, lng=lng)
        return await _post(request, options, payload, d)
