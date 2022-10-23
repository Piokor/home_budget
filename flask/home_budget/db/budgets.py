from mongoengine import StringField, Document, ObjectIdField
import json

from home_budget.db.transactions import Transaction
from home_budget.db.users import User


class Budget(Document):
    """Db model representing a budget assigned to a single user."""
    title = StringField(min_length=1, max_length=100, required=True)
    description = StringField(max_length=300)
    owner_id = ObjectIdField(required=True)


def budget_with_transactions(budget: Budget, include_username: bool = False) -> dict:
    """Returns dict with budget, and it's transactions as json strings"""
    transactions_str = Transaction.objects(budget_id=budget.id).to_json()
    transactions = json.loads(transactions_str)

    budget_dict = json.loads(budget.to_json())
    budget_dict["transactions"] = transactions
    if include_username:
        budget_dict["owner_name"] = get_budget_owner_name(budget)

    return budget_dict


def budgets_with_transactions(budget_list: list[Budget], include_usernames: bool = False) -> list[dict]:
    """Returns dict with budgets, and it's transactions as json strings, corresponding to given budget list"""
    with_transactions = map(lambda b: budget_with_transactions(b, include_usernames), budget_list)
    return list(with_transactions)


def get_budget_owner_name(budget: Budget) -> str:
    """Returns name of the budget owner"""
    owner_id = budget.owner_id
    try:
        name = User.objects(id=owner_id)[0].name
    except IndexError:
        return "unknown"

    return name
