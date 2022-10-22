import os

FLASK_ENV = os.environ["APP_ENV"] or "dev"
SECRET_KEY = "secret"

if FLASK_ENV == "prod":
    MONGO_URI = 'mongodb://' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
else:
    MONGO_URI = 'mongodb://localhost:27017/flaskdb'
