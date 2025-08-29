from database.__init_db import lessons_collection
from bson import ObjectId

class LessonRepository:
    @staticmethod
    def create(lesson_dict):
        return lessons_collection.insert_one(lesson_dict)
    @staticmethod
    def find_all():
        return list(lessons_collection.find())
    @staticmethod
    def find_by_id(lesson_id):
        return lessons_collection.find_one({"_id": ObjectId(lesson_id)})
    @staticmethod
    def delete(lesson_id):
        return lessons_collection.delete_one({"_id": ObjectId(lesson_id)})
