import json
from flask import Flask, request
from plan.algo import place_courses

APP = Flask(__name__)

@APP.route('/')
def index():
    return 'Hello, World!'

@APP.route('/plan/', methods=['POST'])
def plan():
    payload = request.get_json()
    new_plan = place_courses(**payload)
    return json.dumps(new_plan)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', debug=True)

