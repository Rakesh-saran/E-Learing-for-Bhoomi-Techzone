from database.__init_db import enrollments_collection
from bson import ObjectId

class EnrollmentRepository:
    @staticmethod
    def create(enrollment_dict):
        return enrollments_collection.insert_one(enrollment_dict)
    @staticmethod
    def find_all():
        return list(enrollments_collection.find())
    @staticmethod
    def find_by_user(user_id):
        return list(enrollments_collection.find({"user_id": user_id}))
    @staticmethod
    def find_by_user_and_course(user_id, course_id):
        return enrollments_collection.find_one({"user_id": user_id, "course_id": course_id})
    @staticmethod
    def update_progress(enrollment_id, progress):
        return enrollments_collection.update_one(
            {"_id": ObjectId(enrollment_id)}, 
            {"$set": {"progress": progress}}
        )
    @staticmethod
    def delete(enrollment_id):
        return enrollments_collection.delete_one({"_id": ObjectId(enrollment_id)})
