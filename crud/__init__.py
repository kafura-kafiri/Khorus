from sanic.response import json
from Choori.decorators import options as handle_options, privileges, retrieve
from Choori.utility import render

import os
import json as native_json


def save(prime_name, parameters, path, config):
    data = {
        'ancillary': {
            'uri': '',
            'name': '',
            'methods': [],
            'parameters': {},
            'privileges': [],
        },
        'prime': {
            'name': prime_name,
            'parameters': parameters,
        },
        'config': config,
    }
    path = os.path.join(path, 'symlinks')
    try:
        os.mkdir(path)
    except FileExistsError as e:
        print(e)
    except:
        return {'status': "can't create folder SYMLINK"}
    path = os.path.join(path, prime_name)
    try:
        os.mkdir(path)
    except FileExistsError as e:
        print(e)
    except:
        return {'status': "can't create folder {}".format(prime_name.upper())}
    cnt = len(os.listdir(path))
    with open(os.path.join(path, '{}.json'.format(cnt)), 'w+') as f:
        f.write(native_json.dumps(data, indent=4))
    return {'status': path}


def prime(bp, mongo, path, config):
    """

    :param bp:
    :param mongo:
    :param crud_path:
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
        if '--symlink' not in options:
            return json(await mongo.find(options, payload, query, projection))
        else:
            options.remove('--symlink')
            params = {
                'options': options,
                'payload': payload,
                'query': query,
                'projection': projection
            }
            return json(save('find', params, path, config))

    @bp.route('/', methods=['PUT'])
    @bp.route('/-<options>', methods=['PUT'])
    @handle_options()
    @privileges('dev')
    @retrieve(
        '<dict:form:d>'
    )  # add bulk, add user options.
    async def _post(request, options, payload, d):
        if '--symlink' not in options:
            return json(await mongo.insert(options, payload, d))
        else:
            options.remove('--symlink')
            params = {
                'options': options,
                'payload': payload,
                'd': d,
            }
            return json(save('insert', params, path, config))

    @bp.route('/', methods=['DELETE'])
    @bp.route('/-<options>', methods=['DELETE'])
    @handle_options()
    @privileges('dev')
    @retrieve(
        '<dict:form:query>'
    )
    async def _delete(request, options, payload, query):
        if '--symlink' not in options:
            return json(await mongo.delete(options, payload, query))
        else:
            options.remove('--symlink')
            params = {
                'options': options,
                'payload': payload,
                'query': query,
            }
            return json(save('update', params, path, config))

    @bp.route('/', methods=['PATCH'])
    @bp.route('/-<options>', methods=['PATCH'])
    @handle_options()
    @privileges('dev')
    @retrieve(
        '<dict:form:query>',
        '<str:form:node>',
        '<node:form:d>',
        '<str:form:operator>'
    )
    async def _update(request, options, payload, query, node, d, operator):
        if '--symlink' not in options:
            return json(await mongo.update(options, payload, query, node, d, operator))
        else:
            options.remove('--symlink')
            params = {
                'options': options,
                'payload': payload,
                'query': query,
                'node': node,
                'd': d,
                'operator': operator,
            }
            return json(save('update', params, path, config))

    @bp.route('/@', methods=['POST'])
    @privileges('dev')
    @retrieve(
        '<dict:form:symlink>',
    )
    async def symlink(request, payload, symlink):
        _path = os.path.join(path, '__init__.py')
        with open(_path, 'a') as f:
            f.write(render('primes/symlink.py.jinja', symlink))
        return json({'status': 'congratulations'})
