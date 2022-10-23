from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
CORS(app)

import home_budget.views