from sqlalchemy.orm import scoped_session, sessionmaker

from utils import managed_session
from models import db


class Problems:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def add_problems(self, problem_name, start_time, deadline):
        with managed_session(self.session_factory) as session:
            problem = db.Problem(
                problem_name=problem_name, start_time=start_time, deadline=deadline
            )
            session.add(problem)
            return problem.id

    def query_problem(self, problem_name):
        with managed_session(self.session_factory) as session:
            problem = (
                session.query(db.Problem).filter_by(problem_name=problem_name).first()
            )
            if problem:
                problem_data = {
                    "id": problem.id,
                    "problem_name": problem.problem_name,
                    "created_time": problem.created_time,
                    "start_time": problem.start_time,
                    "deadline": problem.deadline,
                }
                return problem_data
            return None

    def del_problem(self, problem_id):
        with managed_session(self.session_factory) as session:
            problem = session.query(db.Problem).filter_by(id=problem_id).first()
            if problem:
                problem.is_valid = 0
                return problem.id
            return None

    def update_problem(self, problem_id, problem_name, start_time, deadline):
        with managed_session(self.session_factory) as session:
            problem = session.query(db.Problem).filter_by(id=problem_id).first()
            if problem:
                problem.problem_name = problem_name
                problem.start_time = start_time
                problem.deadline = deadline
                return problem.id
            return None

    def query_all_problems(self):
        with managed_session(self.session_factory) as session:
            problems = session.query(db.Problem).all()
            problem_data = [
                {
                    "id": problem.id,
                    "problem_name": problem.problem_name,
                    "created_time": problem.created_time,
                    "start_time": problem.start_time,
                    "deadline": problem.deadline,
                }
                for problem in problems
            ]
            return problem_data

    def query_subtask(self, problem_id):
        with managed_session(self.session_factory) as session:
            task_list = (
                session.query(db.Subtask)
                .filter_by(problem_id=problem_id, is_valid=1)
                .all()
            )
            task_data = [
                {
                    "id": task.id,
                    "task_name": task.task_name,
                    "points": task.points,
                }
                for task in task_list
            ]
            return task_data
