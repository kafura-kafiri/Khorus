import hashlib
from jinja2 import Environment, FileSystemLoader
import json


def get_hexdigest(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg.encode())
    return m.hexdigest()


def set_password(raw_password):
    import random
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s$%s' % ('sha256', salt, hsh)


def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    algo, salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(salt, raw_password)

import jwt

# e_jwt = jwt.encode({'username': 'shahin', 'password': 'qarebaqi'}, 'secret', algorithm='HS256')
# payload = jwt.decode(e_jwt, 'secret', algorithms=['HS256'])

import pprint
def render(path, data):
    env = Environment(loader=FileSystemLoader('Choori/templates'))

    def render_json(tree):
        s = json.dumps(tree, indent=4)
        ss = s.split('\n')
        s = '\n    '.join(ss)
        s = s.replace('"$', '')
        s = s.replace('$"', '')
        s = s.replace('null,', 'None,')
        s = s.replace('false,', 'False,')
        s = s.replace('true,', 'True,')
        return s
    env.globals.update(render_json=render_json)
    template = env.get_template(path)
    return template.render(**data)
