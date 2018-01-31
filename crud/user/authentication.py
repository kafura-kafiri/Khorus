from sanic.response import text, json
from crud.user import authentication_bp as bp
from crud.user import users
from Choori.decorators import privileges, retrieve
import jwt


@bp.route('/signup', methods=['POST'])
@retrieve(
    '<username:str:$form:a>',
    '<password:str:$form:a>'
)
async def signup(request, username, password):
    u = {
        'username': username,
        'password': password,
        'privileges': ['dev']
    }
    from Choori.utility import set_password
    u['password'] = set_password(u['password'])
    result = await users.insert([], {}, u)
    return json(result)


@bp.route('/key', methods=['POST'])
@retrieve(
    '<username:str:$form:a>',
    '<password:str:$form:a>'
)
async def create_key(request, username, password):
    u = {
        'username': username,
        'password': password
    }
    from Choori.utility import check_password
    _users = await users.find({}, {}, {'username': u['username']})
    if not _users:
        return text('user not found')
    user = _users[0]
    if not check_password(u['password'], user['password']):
        return json({'status': 'not_authorized'}, 403)
    return text(jwt.encode(
        {
            'username': user['username'],
            'privileges': user['privileges']
        }, 'secret', algorithm='HS256'))


@bp.route('/logout', methods=['POST'])
async def logout(request):
    u = {
        'key': request.form['key'][0]
    }
    # redis_test, redis|async, jump->here
    return text('huli')


@bp.route('/protected', methods=['POST', 'GET'])
@privileges('dev')
async def protected(request, payload):
    return text(str(payload))
