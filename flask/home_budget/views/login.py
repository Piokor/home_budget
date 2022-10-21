import datetime

import jwt
from flask import request, make_response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from home_budget import app
from home_budget.db.users import User


@app.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(name=data['name'], password=hashed_password)
    new_user.save()

    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401)

    try:
        user = User.objects(name=auth.username)[0]
    except IndexError:
        return make_response('user associated with that token not exists', 400)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'id': str(user.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")

        return make_response({'token': token}, 200)

    return make_response('could not verify', 401)
