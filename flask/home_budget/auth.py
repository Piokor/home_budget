import datetime
from functools import wraps

import jwt
from flask import request, make_response
from bson import ObjectId

from home_budget import app
from home_budget.db.users import User


SIGN_ALGORITHM = "HS256"


def token_required(f):
    """
    Wrapper for views where token authorization is required. Puts id of a user associated with the token as a 1st
    parameter of wrapped view.
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return make_response('a valid token is missing', 400)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[SIGN_ALGORITHM])
            user_id = ObjectId(data["id"])
            current_user = User.objects(id=user_id)[0]
        except jwt.DecodeError:
            return make_response('token is invalid', 400)
        except IndexError:
            return make_response('user associated with that token not exists', 400)
        except jwt.exceptions.ExpiredSignatureError:
            return make_response('session expired', 440)

        return f(current_user, *args, **kwargs)

    return decorator


def create_token(user_id: ObjectId):
    """Create jwt token for a user with given id."""
    return jwt.encode({
            'id': str(user_id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90)},
            app.config['SECRET_KEY'],
            SIGN_ALGORITHM)
