from flask import request, make_response

from home_budget import app
from home_budget.auth import token_required
from home_budget.db.users import User
from home_budget.views import required_args


@app.route('/api/users', methods=['GET'])
@required_args("query_str")
@token_required
def get_users(current_user):
    """Get users with a name contain given string. Results are limited to 20 users."""
    query_str = request.args["query_str"]
    if type(query_str) != str:
        return make_response('incorrect query format', 400)

    users = User.objects(name__icontains=query_str, id__ne=current_user.id)[:20]
    result = [
        {"name": user.name, "id": str(user.id)} for user in users
    ]

    return make_response(result, 200)