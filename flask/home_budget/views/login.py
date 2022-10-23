from flask import request, make_response, jsonify
from mongoengine import ValidationError
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash

from home_budget import app
from home_budget.db.users import User, create_user
from home_budget.auth import create_token
from home_budget.views.validation import validate_password, required_fields


@app.route('/api/register', methods=['POST'])
@required_fields("name", "password")
def signup_user():
    """Sign up view. If successful creates a new user in the db."""
    data = request.get_json()

    password = data['password']
    valid, message, code = validate_password(password)
    if not valid:
        return make_response(message, code or 400)

    try:
        create_user(data['name'], password)
    except DuplicateKeyError:
        return make_response('username already taken', 400)
    except NotUniqueError:
        return make_response('username already taken', 400)
    except ValidationError:
        return make_response('incorrect parameter format', 400)

    return make_response('registered successfully', 200)


@app.route('/api/login', methods=['POST'])
def login_user():
    """Login view. If successful returns a new jwt token."""
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401)

    try:
        user = User.objects(name=auth.username)[0]
    except IndexError:
        return make_response('user associated with that token do not exists', 400)

    if check_password_hash(user.password, auth.password):
        token = create_token(user.id)
        return make_response({'token': token}, 200)

    return make_response('could not verify', 401)
