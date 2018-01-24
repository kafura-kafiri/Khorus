from functools import wraps
from sanic import response
import jwt
import ujson as json
import numbers

maximal = {
    '-u': '--username',
    '-b': '--bulk',
    '-s': '--symlink',
}


def options():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, options='', **kwargs):
            os = options.split('-')
            for index, op in enumerate(os):
                if op:
                    os[index] = maximal.get('-{}'.format(op), '--{}'.format(op))
            os = [op for op in os if op]
            return await f(request, *(lambda a, b: a.extend(b) or a)([os], args), **kwargs)
        return decorated_function
    return decorator


def privileges(*roles):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                key = request.form['key'][0] if request.form['key'][0] else request.args['key'][0]
                del[request.form['key']]
                payload = jwt.decode(key, 'secret', algorithms=['HS256'])
            except:
                return response.json({'status': 'not_authorized'}, 403)
            if not roles or (payload['privileges'] and not set(payload['privileges']).isdisjoint(roles)):
                rv = await f(request, *(args + (payload, )), **kwargs)
                return rv
            else:
                return response.json({'status': 'roles_disjoint', 'roles_required': roles}, 403)
        return decorated_function
    return decorator


def retrieve(*requirements):
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
                    except: pass
                    if _type =='num':
                        if not isinstance(param, numbers.Real):
                            return response.json({'status': 'type mismatch'}, 404)
                    elif param.__class__.__name__ != _type:
                        return response.json({'status': 'type mismatch'}, 404)
                finally:
                    if param is None:
                        return response.json({'status': "can't retrieve"})
                parameters.append(param)
            return await f(request, *(args + tuple(parameters)), **kwargs)
        return decorated_function
    return decorator

