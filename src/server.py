from flask import Flask, request, jsonify
from src.plan import place_courses

APP = Flask(__name__)


@APP.route("/")
def index():
    return "Hello, World!"


@APP.route("/plan", methods=["POST"])
def plan():
    payload = request.get_json()
    new_plan = place_courses(payload)
    resp = jsonify(new_plan)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def start_flask_server() -> None:
    APP.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    start_flask_server()
