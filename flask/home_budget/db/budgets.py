from mongoengine import StringField, Document, ObjectIdField


class Budget(Document):
    """Db model representing a budget assigned to a single user."""
    title = StringField(max_length=100, required=True)
    description = StringField(max_length=300)
    owner_id = ObjectIdField(required=True)
