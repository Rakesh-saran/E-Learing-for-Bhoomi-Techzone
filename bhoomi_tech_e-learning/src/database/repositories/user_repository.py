from database.__init_db import users_collection
from bson import ObjectId

class UserRepository:
    @staticmethod
    def create(user_dict):
        return users_collection.insert_one(user_dict)
    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})
    @staticmethod
    def find_all():
        return list(users_collection.find())
    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})
    @staticmethod
    def update(user_id, update_data):
        return users_collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": update_data}
        )
    @staticmethod
    def delete(user_id):
        return users_collection.delete_one({"_id": ObjectId(user_id)})
