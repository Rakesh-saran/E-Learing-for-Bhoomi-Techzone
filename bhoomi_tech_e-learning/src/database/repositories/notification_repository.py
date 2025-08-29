from database.__init_db import notifications_collection
from bson import ObjectId

class NotificationRepository:
    @staticmethod
    def create(notification_dict):
        return notifications_collection.insert_one(notification_dict)
    @staticmethod
    def find_by_user(user_id):
        return list(notifications_collection.find({"user_id": user_id}))
    @staticmethod
    def mark_as_read(notification_id):
        return notifications_collection.update_one({"_id": ObjectId(notification_id)}, {"$set": {"is_read": True}})
    @staticmethod
    def delete(notification_id):
        return notifications_collection.delete_one({"_id": ObjectId(notification_id)})
