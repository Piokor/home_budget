from bson import ObjectId
from mongoengine import Document, ObjectIdField

from home_budget.db.budgets import Budget


class BudgetSharing(Document):
    """Db model representing a many-to-many relationship of budgets and users that they have been shared to. Mongodb
    arrays could be used as well, but they are unadvised when arrays can grow endlessly."""
    budget_id = ObjectIdField(required=True)
    shared_to_user_id = ObjectIdField(required=True)


def get_budgets_shared_with_user(user_id: ObjectId):
    shared_budgets_ids = [sharing.budget_id for sharing in BudgetSharing.objects(shared_to_user_id=user_id)]
    budgets = Budget.objects(id__in=shared_budgets_ids)
    return budgets.to_json()
