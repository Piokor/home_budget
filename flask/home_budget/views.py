from home_budget import app

@app.route('/')
def index():
    return 'Hello World!'