import pytest
from werkzeug.security import check_password_hash
from mongoengine.errors import NotUniqueError

from home_budget.tests.utils import mock_app
from home_budget.db.users import create_user, User

USERNAME, PASSWORD = "usrnm", "passwd"


def test_create_user(mock_app):
    """Test if create_user creates user and hashes password correctly"""
    create_user(USERNAME, PASSWORD)

    try:
        new_user = User.objects(name=USERNAME)[0]
    except IndexError:
        assert False, "User was not created"

    assert check_password_hash(new_user.password, PASSWORD), \
        "Password hash was not saved correctly"

        
def test_create_duplicate_user(mock_app):
    """Test if create_user won't allow creating 2 users with same username"""
    create_user(USERNAME, PASSWORD)

    with pytest.raises(NotUniqueError):
        create_user(USERNAME, password=PASSWORD)

    
