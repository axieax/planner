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
    return jsonify(new_plan)


def start_flask_server() -> None:
    APP.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    start_flask_server()
