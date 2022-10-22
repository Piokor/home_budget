from mongoengine import StringField, Document

from home_budget.auth import hash_password


class User(Document):
    """Db model representing single app user."""
    name = StringField(max_length=50, required=True, unique=True)
    password = StringField(max_length=100)


def create_user(username: str, password: str):
    """Function for creating users with given credentials."""
    hashed_password = hash_password(password)
    new_user = User(name=username, password=hashed_password)
    new_user.save()
