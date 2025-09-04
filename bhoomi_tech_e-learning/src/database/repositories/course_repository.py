from database.__init_db import courses_collection
from bson import ObjectId

class CourseRepository:
    @staticmethod
    def create(course_dict):
        return courses_collection.insert_one(course_dict)
    @staticmethod
    def find_all():
        return list(courses_collection.find())
    @staticmethod
    def find_by_id(course_id):
        return courses_collection.find_one({"_id": ObjectId(course_id)})
    @staticmethod
    def update(course_id, update_data):
        return courses_collection.update_one(
            {"_id": ObjectId(course_id)}, 
            {"$set": update_data}
        )
    @staticmethod
    def delete(course_id):
        return courses_collection.delete_one({"_id": ObjectId(course_id)})
