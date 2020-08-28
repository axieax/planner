from flask import Flask, render_template, request
from main import main
from courses import courses

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/select", methods=["POST", "GET"])
def select():
    return render_template("select.html")


@app.route("/plan", methods=["POST", "GET"])
def plan():
    output = main(courses=courses)
    return render_template("plan.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)
