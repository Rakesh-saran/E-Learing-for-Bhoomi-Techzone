from database.__init_db import quizzes_collection
from bson import ObjectId

class QuizRepository:
    @staticmethod
    def create(quiz_dict):
        return quizzes_collection.insert_one(quiz_dict)
    @staticmethod
    def find_all():
        return list(quizzes_collection.find())
    @staticmethod
    def find_by_id(quiz_id):
        return quizzes_collection.find_one({"_id": ObjectId(quiz_id)})
    @staticmethod
    def delete(quiz_id):
        return quizzes_collection.delete_one({"_id": ObjectId(quiz_id)})
