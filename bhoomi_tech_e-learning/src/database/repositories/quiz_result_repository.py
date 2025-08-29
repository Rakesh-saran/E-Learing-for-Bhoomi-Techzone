from database.__init_db import db
from bson import ObjectId

quiz_results_collection = db["quiz_results"]

class QuizResultRepository:
    @staticmethod
    def create(result_dict):
        return quiz_results_collection.insert_one(result_dict)
    @staticmethod
    def find_by_user(user_id):
        return list(quiz_results_collection.find({"user_id": user_id}))
    @staticmethod
    def find_by_quiz(quiz_id):
        return list(quiz_results_collection.find({"quiz_id": quiz_id}))
