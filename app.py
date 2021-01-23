from flask import Flask, request
from plan import main
from data import courses, plan, plan_specs
import json

APP = Flask(__name__)


@APP.route('/')
def index():
    return 'beep boop'

@APP.route('/api', methods=['GET'])
def api():
    return json.dumps(main(
        plan=request.args.get('plan'),
        plan_specs=request.args.get('plan_specs'),
        selected_course_codes=request.args.get('selected_course_codes'),
        find_optimal=request.args.get('find_optimal'),
    ))

@APP.route('/test')
def test():
    return json.dumps(main(
        plan=plan,
        plan_specs=plan_specs,
        selected_course_codes=[course.code for course in courses],
        find_optimal=True,
    ))

sample_request = json.dumps({
    'selected_course_codes': [course.code for course in courses],
    'plan': plan,
    'plan_specs': plan_specs,
})
print(sample_request)

if __name__ == "__main__":
    APP.run(debug=True)
