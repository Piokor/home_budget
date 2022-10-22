from bson import ObjectId
from flask import request, make_response
from mongoengine import ValidationError

from home_budget import app
from home_budget.auth import token_required
from home_budget.db.budget_sharing import BudgetSharing, get_budgets_shared_with_user
from home_budget.db.budgets import Budget
from home_budget.views.validation import validate_share_budget_params


@app.route('/create_budget', methods=['POST'])
@token_required
def create_budget(current_user):
    """Create a budget view."""
    data = request.get_json()
    if "title" not in data:
        return make_response('budget title required', 400)
    description = data.get("description")

    try:
        new_budget = Budget(title=data["title"], description=description, owner_id=current_user.id)
        new_budget.save()
    except ValidationError:
        return make_response('incorrect parameter format', 400)

    return make_response(new_budget.to_json(), 200)


@app.route('/share_budget', methods=['POST'])
@token_required
def share_budget(current_user):
    """Share a budget with a different user."""
    data = request.get_json()
    if "budget_id" not in data or "other_user_id" not in data:
        return make_response('budget or other user id not sent', 400)
    budget_id_str, other_user_id_str = data["budget_id"], data["other_user_id"]

    valid, message, code = validate_share_budget_params(current_user, budget_id_str, other_user_id_str)
    if not valid:
        return make_response(message, code or 400)

    budget_id, other_user_id = ObjectId(budget_id_str), ObjectId(other_user_id_str)

    new_sharing = BudgetSharing(shared_to_user_id=other_user_id, budget_id=budget_id)
    new_sharing.save()

    return make_response(new_sharing.to_json(), 200)


@app.route('/budgets', methods=['GET'])
@token_required
def get_budgets(current_user):
    """Get list of users budgets and list of budgets shared with him."""

    own_budgets = Budget.objects(owner_id=current_user.id).to_json()
    shared_budgets = get_budgets_shared_with_user(current_user.id)
    budget_lists = {
        "own": own_budgets,
        "shared": shared_budgets
    }

    return make_response(budget_lists, 200)