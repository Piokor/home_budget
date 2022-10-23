from enum import Enum, auto

from mongoengine import StringField, Document, ObjectIdField, EnumField, FloatField


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Currency(Enum):
    USD = "USD"
    PLN = "PLN"
    EURO = "EURO"


class Transaction(Document):
    """
    Db model representing a single budget transaction, can be either an income or expense. Transaction is assigned to
    a single budget
    """
    title = StringField(max_length=200, required=True)
    type = EnumField(TransactionType, required=True)
    amount = FloatField(required=True)
    currency = EnumField(Currency, required=True, default=Currency.USD)
    budget_id = ObjectIdField(required=True)
    category = StringField(max_length=100, required=True)
