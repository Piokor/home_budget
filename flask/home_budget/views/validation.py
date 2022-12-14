from functools import wraps
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from flask import request, make_response

from home_budget.db.transactions import TransactionType, Currency
from home_budget.db.users import User
from home_budget.db.budgets import Budget
from home_budget.db.budget_sharing import BudgetSharing


def validate_share_budget_params(
        current_user: User,
        budget_id_str: str,
        other_user_id_str: str
        ) -> tuple[bool, Optional[str], Optional[int]]:
    """
    Validate parameters for share_budget view. Returns 3 values: boolean result, message in case of failure and code in
    case of failure
    """
    if not _valid_objectid(budget_id_str) or not _valid_objectid(other_user_id_str):
        return False, "invalid user or budget id", 400
    budget_id, other_user_id = ObjectId(budget_id_str), ObjectId(other_user_id_str)

    if not _check_if_exists(budget_id, Budget):
        return False, "budget with given id not found", 400

    if not _check_if_exists(other_user_id, User):
        return False, "other user with given id not found", 400

    shared_budget = Budget.objects(id=budget_id)[0]
    if shared_budget.owner_id != current_user.id:
        return False, "user is not owner of shared budget", 401

    if other_user_id == current_user.id:
        return False, "user cannot share budget with himself", 400

    existing_sharing = BudgetSharing.objects(shared_to_user_id=other_user_id, budget_id=budget_id)
    if len(existing_sharing) != 0:
        return False, "given budget is already shared with given user", 400

    return True, None, None


def validate_transaction(transaction: dict, current_user: User) -> tuple[bool, Optional[str], Optional[int]]:
    """
    Validate parameters for create_transaction view. Returns 3 values: boolean result, message in case of failure and
    code in case of failure
    """
    try:
        TransactionType(transaction["type"])
        Currency(transaction["currency"])
    except ValueError:
        return False, "Not supported transaction type or currency", 400

    budget_id_str = transaction["budget_id"]
    if not _valid_objectid(budget_id_str):
        return False, "invalid budget id", 400
    budget_id = ObjectId(budget_id_str)

    if not _check_if_exists(budget_id, Budget):
        return False, "budget with given id not found", 400

    budget = Budget.objects(id=budget_id)[0]
    if budget.owner_id != current_user.id:
        return False, "user is not owner of given budget", 401

    return True, None, None


def validate_password(password: str) -> tuple[bool, Optional[str], Optional[int]]:
    """
    Validate user password. Returns 3 values: boolean result, message in case of failure and code in case of failure
    """
    if type(password) is not str:
        return False, "incorrect password format", 400

    if len(password) < 3 or len(password) > 50:
        return False, "incorrect password length", 400

    return True, None, None


def validate_get_budget(current_user: User, budget_id_str: str) -> tuple[bool, Optional[str], Optional[int]]:
    """
    Params of get budget request. Returns 3 values: boolean result, message in case of failure and code in case of failure
    """
    if type(budget_id_str) is not str:
        return False, "incorrect id format", 400

    if not _valid_objectid(budget_id_str):
        return False, "invalid budget id", 400
    budget_id = ObjectId(budget_id_str)

    try:
        budget = Budget.objects(id=budget_id)[0]
    except IndexError:
        return False, "budget with given id not found", 400

    existing_sharing = BudgetSharing.objects(shared_to_user_id=current_user.id, budget_id=budget_id)
    if current_user.id != budget.owner_id and len(existing_sharing) == 0:
        return False, "given budget is not shared with given user", 400

    return True, None, None


def _valid_objectid(id_str: str) -> bool:
    """Validate if string is a valid bson object id."""
    try:
        ObjectId(id_str)
        return True
    except InvalidId:
        return False


def _check_if_exists(id: ObjectId, collection) -> bool:
    """Validate if document with given id exists in given collection"""
    return len(collection.objects(id=id)) != 0


def required_fields(*fields):
    """Decorator for POST views functions. Checks if all required fields are present in a request."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            for field in fields:
                if field not in data:
                    return make_response(f'\"{field}\" parameter is required', 400)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def required_args(*req_args):
    """Decorator for GET views functions. Checks if all required args are present in a request."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.args
            for field in req_args:
                if field not in data:
                    return make_response(f'\"{field}\" arg is required', 400)
            return func(*args, **kwargs)
        return wrapper
    return decorator
