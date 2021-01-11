from flask import Flask, render_template, request
from algo import main
from data import courses, plan, plan_specs

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/select", methods=["POST", "GET"])
def select():
    return render_template("select.html")


@app.route("/plan", methods=["POST", "GET"])
def planner():
    # POST -> data.py?
    output = main(selected_course_codes=[course.code for course in courses], plan=plan, plan_specs=plan_specs)
    return render_template("plan.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)
