from flask import render_template
from flask.helpers import send_from_directory

from home_budget import app

@app.route('/', methods=["GET"])
def serve_vue_app():
    return render_template('dist/index.html')

@app.route('/css/<path:path>')
def serve_vue_app_css(path):
    return send_from_directory('templates/dist/css', path)

@app.route('/js/<path:path>')
def serve_vue_app_js(path):
    return send_from_directory('templates/dist/js', path)

@app.route('/img/<path:path>')
def serve_vue_app_img(path):
    return send_from_directory('templates/dist/img', path)
