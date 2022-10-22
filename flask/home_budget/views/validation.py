from typing import Optional, ClassVar

from bson import ObjectId
from bson.errors import InvalidId

from home_budget.db.users import User
from home_budget.db.budgets import Budget
from home_budget.db.budget_sharing import BudgetSharing


def validate_share_budget_params(current_user: User, budget_id_str: str, other_user_id_str: str) \
        -> tuple[bool, Optional[str], Optional[int]]:
    if not valid_objectid(budget_id_str) or not valid_objectid(other_user_id_str):
        return False, "invalid user or budget id", None
    budget_id, other_user_id = ObjectId(budget_id_str), ObjectId(other_user_id_str)

    if not check_if_exists(budget_id, Budget):
        return False, "budget with given id not found", None

    if not check_if_exists(other_user_id, User):
        return False, "other user with given id not found", None

    shared_budget = Budget.objects(id=budget_id)[0]
    if shared_budget.owner_id != current_user.id:
        return False, "user is not owner of shared budget", 401

    if other_user_id == current_user.id:
        return False, "user cannot share budget with himself", None

    existing_sharing = BudgetSharing.objects(shared_to_user_id=other_user_id, budget_id=budget_id)
    if len(existing_sharing) != 0:
        return False, "given budget is already shared with given user", None

    return True, None, None


def valid_objectid(id_str: str) -> bool:
    try:
        ObjectId(id_str)
        return True
    except InvalidId:
        return False


def check_if_exists(id: ObjectId, collection) -> bool:
    return len(collection.objects(id=id)) != 0
