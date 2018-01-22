from sanic.response import text, json
from crud.user import bp
from crud.user import users
from utility import roles_required
import jwt


@bp.route('/signup', methods=['POST'])
async def signup(request):
    u = {
        'username': request.form['username'][0],
        'password': request.form['password'][0],
        'roles': ['piaz', 'sir']
    }
    from utility import set_password
    u['password'] = set_password(u['password'])
    result = await users.insert_one(u)
    return text(result.inserted_id)


@bp.route('/key', methods=['POST'])
async def create_key(request):
    u = {
        'username': request.form['username'][0],
        'password': request.form['password'][0]
    }
    from utility import check_password
    user = await users.find_one({'username': u['username']})
    if not user:
        return text('user not found')
    if not check_password(u['password'], user['password']):
        return json({'status': 'not_authorized'}, 403)
    return text(jwt.encode(
        {
            'username': user['username'],
            'roles': user['roles']
        }, 'secret', algorithm='HS256'))


@bp.route('/logout', methods=['POST'])
async def logout(request):
    u = {
        'key': request.form['key'][0]
    }
    # redis_test, redis|async, jump->here
    return text('huli')


@bp.route('/protected', methods=['POST', 'GET'])
@roles_required(['sss'])
async def protected(request, payload):
    return text(str(payload))