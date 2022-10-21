from functools import wraps

import jwt
from flask import request, make_response
from bson import ObjectId

from home_budget import app
from home_budget.db.users import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return make_response('a valid token is missing', 400)
        try:
            data = jwt.decode("a" + token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = ObjectId(data["id"])
            current_user = User.objects(id=user_id)[0]
        except jwt.DecodeError:
            return make_response('token is invalid', 400)
        except IndexError:
            return make_response('user associated with that token not exists', 400)

        return f(current_user, *args, **kwargs)

    return decorator
