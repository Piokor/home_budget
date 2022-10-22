from flask import make_response, request
from mongoengine import ValidationError

from home_budget import app
from home_budget.auth import token_required
from home_budget.db.transactions import Transaction
from home_budget.views.validation import validate_transaction, required_fields


@app.route('/api/create_transaction', methods=['POST'])
@required_fields("title", "type", "amount", "budget_id", "category", "currency")
@token_required
def create_transaction(current_user):
    """Create a transaction view."""
    transaction = request.get_json()

    valid, message, code = validate_transaction(transaction, current_user)
    if not valid:
        return make_response(message, code or 400)

    try:
        new_transaction = Transaction(
            title=transaction["title"],
            type=transaction["type"],
            amount=transaction["amount"],
            currency=transaction["currency"],
            budget_id=transaction["budget_id"],
            category=transaction["category"])
        new_transaction.save()
    except ValidationError:
        return make_response('incorrect parameter format', 400)

    return make_response(new_transaction.to_json(), 200)
