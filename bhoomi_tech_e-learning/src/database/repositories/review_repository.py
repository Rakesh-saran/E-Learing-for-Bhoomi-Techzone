from database.__init_db import reviews_collection
from bson import ObjectId

class ReviewRepository:
    @staticmethod
    def create(review_dict):
        return reviews_collection.insert_one(review_dict)
    @staticmethod
    def find_by_course(course_id):
        return list(reviews_collection.find({"course_id": course_id}))
    @staticmethod
    def delete(review_id):
        return reviews_collection.delete_one({"_id": ObjectId(review_id)})
