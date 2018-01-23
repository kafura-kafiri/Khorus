import hashlib


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
