from mongoengine import StringField, Document


class User(Document):
    name = StringField(max_length=50, required=True)
    password = StringField(max_length=100)
