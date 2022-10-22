from mongoengine import StringField, Document
from werkzeug.security import generate_password_hash


class User(Document):
    """Db model representing single app user."""
    name = StringField(max_length=50, required=True, unique=True)
    password = StringField(max_length=100, required=True)


def create_user(username: str, password: str):
    """Function for creating users with given credentials."""
    hashed_password = generate_password_hash(password, method="sha256")
    new_user = User(name=username, password=hashed_password)
    new_user.save()
