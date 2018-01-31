from functools import wraps
from sanic import response
import jwt
import ujson as json
import numbers
from bson import ObjectId
import ast

maximal = {
    '-au': '--author',  # done
    '-b': '--bulk',  # done
    '-s': '--symlink',
    '-d': '--date',  # done
    '-q': '--query',  # done
    '-p': '--project',  # done
    '-sort': '--sort',  # done
    '-skip': '--skip',  # done
    '-limit': '--limit',  # done
}


def extract_options():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, options='', **kwargs):
            phrases = options.split('-')
            os = {}
            for op in phrases:
                if op:
                    parts = op.split(':')
                    parts[0] = maximal.get('-{}'.format(parts[0]), '--{}'.format(parts[0]))
                    if len(parts) == 1:
                        parts.append('')
                    os[parts[0]] = parts[1]
            return await f(request, *args, **kwargs, options=os)
        return decorated_function

    return decorator


def privileges(*roles):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            try:
                key = request.form['key'][0] if request.form['key'][0] else request.args['key'][0]
                del [request.form['key']]
                payload = jwt.decode(key, 'secret', algorithms=['HS256'])
            except:
                return response.json({'status': 'not_authorized'}, 403)
            if not roles or (payload['privileges'] and not set(payload['privileges']).isdisjoint(roles)):
                rv = await f(request, *(args + (payload,)), **kwargs)
                return rv
            else:
                return response.json({'status': 'roles_disjoint', 'roles_required': roles}, 403)

        return decorated_function

    return decorator


def retrieve(*requirements):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            _requirements = requirements
            if 'options' in kwargs:
                _requirements = list(_requirements)
                options = kwargs['options']
                if '--project' in options:
                    _requirements.append('<project:dict:$form:k>')
                if '--sort' in options:
                    _requirements.append('<sort:dict:$form:k>')
                if '--skip' in options:
                    _requirements.append('<skip:int:{}:k>'.format(options['--skip']))
                if '--limit' in options:
                    _requirements.append('<limit:int:{}:k>'.format(options['--limit']))
            _args = []
            for requirement in _requirements:
                param = None
                try:
                    param_name, _type, src, dst = requirement[1:-1].split(':')
                    if '$' in src:
                        param = getattr(request, src[1:])[param_name][0]
                    else:
                        param = src
                    if _type == 'num':
                        try:
                            param = ast.literal_eval(param)
                        except: pass
                        if not isinstance(param, numbers.Real):
                            return response.json({'status': 'type mismatch'}, 404)
                    elif _type == 'id':
                        try:
                            param = ObjectId(param)
                        except:
                            return response.json({'status': 'type mismatch'}, 404)
                    else:
                        try:
                            param = json.loads(param)
                        except: pass
                        if _type != 'node' and param.__class__.__name__ != _type:
                            return response.json({'status': 'type mismatch'}, 404)
                finally:
                    if param is None:
                        return response.json({'status': "can't retrieve"})
                if dst == 'a':
                    _args.append(param)
                elif dst == 'k':
                    kwargs[param_name] = param
            return await f(request, *(args + tuple(_args)), **kwargs)
        return decorated_function
    return decorator
