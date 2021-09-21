from flask import Flask, request, jsonify
from src.plan.algo import place_courses

APP = Flask(__name__)


@APP.route("/")
def index():
    return "Hello, World!"


@APP.route("/plan/", methods=["POST"])
def plan():
    payload = request.get_json()
    degree_details = payload["degree_details"]
    plan_details = payload["plan_details"]
    plan = payload["plan"]
    new_plan = place_courses(degree_details, plan_details, plan)
    return jsonify(new_plan)


def start_flask_server() -> None:
    APP.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    start_flask_server()
