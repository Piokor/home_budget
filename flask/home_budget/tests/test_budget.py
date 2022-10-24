import json

from home_budget.tests.utils import mock_app, mock_current_user, mock_headers, send_post_request, send_get_request
from home_budget.db.budgets import Budget
from home_budget.db.users import User
from home_budget.db.budget_sharing import BudgetSharing


title = "a budget"
description = "a budget desc"


def test_create_budget_view(mock_app, mock_current_user):
    client = mock_app.test_client()
    response = send_post_request(
        client,
        '/api/create_budget',
        {
            "title": title,
            "description": description
        }
    )
    assert response.status_code == 200, "Correct budget request failed"
    try:
        created_budget = Budget.objects(title=title)[0]
    except IndexError:
        assert False, "Budget was not created after successful request"
    assert str(created_budget.owner_id) == str(mock_current_user.id), "Budget was assigned wrong id"
    assert created_budget.description == description, "Budget had wrong description"


def test_create_budget_view_no_description(mock_app, mock_current_user):
    client = mock_app.test_client()
    response = send_post_request(
        client,
        '/api/create_budget',
        {
            "title": title
        }
    )
    assert response.status_code == 200, "Request with optional parameter failed"


def test_create_budget_view_no_title(mock_app, mock_current_user):
    client = mock_app.test_client()
    response = send_post_request(
        client,
        '/api/create_budget',
        {
            "description": description
        }
    )
    assert response.status_code != 200, "Create budget request without title failed"


def test_get_budget_view(mock_app, mock_current_user):
    client = mock_app.test_client()
    created_budget_id = Budget(title=title, owner_id=mock_current_user.id).save().id
    response = send_get_request(
        client,
        '/api/budget',
        {
            "id": created_budget_id
        }
    )
    assert response.status_code == 200, "Correct get_budget request failed"
    fetched_budget = json.loads(response.data)
    assert fetched_budget["title"] == title, "get_budget returned budget with wrong title"


def test_get_budget_view_fail(mock_app, mock_current_user):
    client = mock_app.test_client()
    response = send_get_request(
        client,
        '/api/budget',
        {
            "id": "63555ce7bd5cdc9448dbb9cf"
        }
    )
    assert response.status_code != 200, "Non-existent budget request returned 200"


def test_share_budget_view(mock_app, mock_current_user):
    client = mock_app.test_client()
    other_user_id = User(name="other name", password="other pwd").save().id
    budget_id = Budget(title=title, owner_id=mock_current_user.id).save().id

    response = send_post_request(
        client,
        '/api/share_budget',
        {
            "budget_id": str(budget_id),
            "other_user_id": str(other_user_id)
        }
    )
    assert response.status_code == 200, "Correct share budget request failed"
    try:
        BudgetSharing.objects(shared_to_user_id=other_user_id, budget_id=budget_id)[0]
    except IndexError:
        assert False, "Budget sharing was not created after correct request"


def test_share_budget_view_no_perm(mock_app, mock_current_user):
    client = mock_app.test_client()
    other_user_id = User(name="other name", password="other pwd").save().id
    even_otherer_user_id = User(name="otherer name", password="otherer pwd").save().id
    other_user_budget_id = Budget(title=title, owner_id=other_user_id).save().id

    response = send_post_request(
        client,
        '/api/share_budget',
        {
            "budget_id": str(other_user_budget_id),
            "other_user_id": str(even_otherer_user_id)
        }
    )
    assert response.status_code != 200, "User was able to share budget that he didn't own"
