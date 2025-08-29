from database.__init_db import payments_collection
from bson import ObjectId

class PaymentRepository:
    @staticmethod
    def create(payment_dict):
        return payments_collection.insert_one(payment_dict)
    @staticmethod
    def find_all():
        return list(payments_collection.find())
    @staticmethod
    def find_by_id(payment_id):
        return payments_collection.find_one({"_id": ObjectId(payment_id)})
    @staticmethod
    def delete(payment_id):
        return payments_collection.delete_one({"_id": ObjectId(payment_id)})
