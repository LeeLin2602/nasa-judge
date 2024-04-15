from flask import url_for, jsonify, request, g

from main import app
from service import ProblemService

# check user role at here 
# parse json

@app.route("/problems", methods=["POST"])
def create_problem():
    problem_id = ProblemService.create_problem("New Problem")
    return jsonify({"problem_id": problem_id})

@app.route("/problems/<string:problem_id>", method=["DELETE"])
def delete_problem(problem_id):
    problem_id = ProblemService.delete_problem(problem_id)
    return jsonify({"problem_id": problem_id})

@app.route("/problems/<string:problem_id>", method=["GET"])
def query_problem(problem_id):
    problem = ProblemService.query_problem(problem_id)
    return jsonify(problem)

@app.route("/problems", method=["GET"])
def query_all_problems():
    problems = ProblemService.query_all_problems()
    return jsonify(problems)

@app.route("/problems/<string:problem_id>", method=["PUT"])
def update_problem(problem_id):
    problem_name = request.json.get("problem_name")
    start_time = request.json.get("start_time")
    deadline = request.json.get("deadline")
    problem_id = ProblemService.update_problem(problem_id, problem_name, start_time, deadline)
    return jsonify({"problem_id": problem_id})