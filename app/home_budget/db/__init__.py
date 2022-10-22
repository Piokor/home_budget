from mongoengine import connect

from home_budget import app

connect(host=app.config["MONGO_URI"])
