from functools import wraps
from sanic import response
import jwt
import ujson as json


def privileges(roles):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                key = request.form['key'][0] if request.form['key'][0] else request.args['key'][0]
                del[request.form['key']]
                payload = jwt.decode(key, 'secret', algorithms=['HS256'])
            except:
                return response.json({'status': 'not_authorized'}, 403)
            if not roles or (payload['roles'] and not set(payload['roles']).isdisjoint(roles)):
                rv = await f(request, *(lambda a, b: a.extend(b) or a)(args, [payload]), **kwargs)
                return rv
            else:
                return response.json({'status': 'roles_disjoint', 'roles_required': roles}, 403)
        return decorated_function
    return decorator


def retrieve(requirements):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            parameters = []
            for requirement in requirements:
                param = None
                try:
                    _type, space, param_name = requirement[1:-1].split(':')
                    param = getattr(request, space)[param_name][0]
                    try:
                        param = json.loads(param)
                    finally:
                        if type(param) is not _type:
                            return response.json({'status': 'type mismatch'}, 404)
                finally:
                    if not param:
                        return response.json({'status': "can't retrieve"})
                parameters.append(param)
            return await f(request, *(lambda a, b: a.extend(b) or a)(args, parameters), **kwargs)
        return decorated_function
    return decorator


maximal = {
    '-u': '--username',
    '-b': '--bulk',
    '-s': '--symlink',
}


def options():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            path = request.path
            os = path.split('-')
            for index, op in enumerate(os[1:]):
                if op:
                    os[index] = maximal.get('-{}'.format(op), '--{}'.format(op))
            os = [op for op in os if op]
            return await f(request, *(lambda a, b: a.extend(b) or a)(args, os), **kwargs)
        return decorated_function
    return decorator


