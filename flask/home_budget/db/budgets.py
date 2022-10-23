from mongoengine import StringField, Document, ObjectIdField

from home_budget.db.transactions import Transaction


class Budget(Document):
    """Db model representing a budget assigned to a single user."""
    title = StringField(max_length=100, required=True)
    description = StringField(max_length=300)
    owner_id = ObjectIdField(required=True)


def budget_with_transactions(budget: Budget) -> dict:
    """Returns dict with budget, and it's transactions as json strings"""
    transactions = Transaction.objects(budget_id=budget.id)
    return {
        "budget": budget.to_json(),
        "transactions": transactions.to_json()
    }


def budgets_with_transactions(budget_list: list[Budget]) -> list[dict]:
    """Returns dict with budgets, and it's transactions as json strings, corresponding to given budget list"""
    with_transactions = map(budget_with_transactions, budget_list)
    return list(with_transactions)
