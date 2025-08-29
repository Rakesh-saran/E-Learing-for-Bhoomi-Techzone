from pymongo import MongoClient
from config import config

client = MongoClient(config.MONGO_URL)
db = client.get_database()

# Export collections
users_collection = db["users"]
courses_collection = db["courses"]
lessons_collection = db["lessons"]
enrollments_collection = db["enrollments"]
quizzes_collection = db["quizzes"]
reviews_collection = db["reviews"]
notifications_collection = db["notifications"]
payments_collection = db["payments"]
