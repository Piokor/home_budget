from mongoengine import Document, ObjectIdField


class BudgetSharing(Document):
    """Db model representing a many-to-many relationship of budgets and users that they have been shared to. Mongodb
    arrays could be used as well, but they are unadvised when arrays can grow endlessly."""
    budget_id = ObjectIdField(required=True)
    shared_to_user_id = ObjectIdField(required=True)
