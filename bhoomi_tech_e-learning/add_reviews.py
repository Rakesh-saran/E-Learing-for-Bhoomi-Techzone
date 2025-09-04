"""
Add sample reviews to the database
"""
from pymongo import MongoClient
from datetime import datetime, timezone
from bson import ObjectId
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/e_learning")
db = client.get_database()

print("🌟 Adding Sample Reviews...")

# Get some existing users and courses
users = list(db.users.find({"role": "student"}).limit(5))
courses = list(db.courses.find().limit(5))

if not users or not courses:
    print("❌ No users or courses found. Please run the populate script first.")
    exit()

# Sample reviews
sample_reviews = [
    {
        "rating": 5,
        "review": "Excellent course! The instructor explains everything clearly and the hands-on projects are very helpful."
    },
    {
        "rating": 4,
        "review": "Great content and well-structured. Could use more interactive elements but overall very satisfied."
    },
    {
        "rating": 5,
        "review": "Amazing course! I learned so much and can already apply the skills in my work. Highly recommend!"
    },
    {
        "rating": 3,
        "review": "Decent course with good information, but the pace could be improved. Some sections felt rushed."
    },
    {
        "rating": 4,
        "review": "Very informative and practical. The examples were relevant and easy to follow."
    },
    {
        "rating": 5,
        "review": "Outstanding course! The instructor is knowledgeable and the course material is top-notch."
    },
    {
        "rating": 4,
        "review": "Good course overall. I especially liked the real-world applications and case studies."
    },
    {
        "rating": 2,
        "review": "The course content was okay but the video quality could be better. Also needs more practice exercises."
    },
    {
        "rating": 5,
        "review": "Perfect course for beginners! Well explained with great examples and supportive community."
    },
    {
        "rating": 4,
        "review": "Comprehensive course with good coverage of topics. The final project was challenging but rewarding."
    }
]

# Create reviews
review_count = 0
for i in range(min(15, len(sample_reviews))):
    user = random.choice(users)
    course = random.choice(courses)
    review_data = random.choice(sample_reviews)
    
    # Check if this user already reviewed this course
    existing = db.reviews.find_one({"user_id": user["_id"], "course_id": course["_id"]})
    if existing:
        continue
    
    review_doc = {
        "user_id": user["_id"],
        "course_id": course["_id"],
        "rating": review_data["rating"],
        "review": review_data["review"],
        "created_at": datetime.now(timezone.utc),
        "is_approved": True
    }
    
    db.reviews.insert_one(review_doc)
    review_count += 1
    print(f"✅ Added review by {user['name']} for {course['title']} - {review_data['rating']} stars")

print(f"\n🎉 Added {review_count} sample reviews!")
print(f"📊 Total reviews in database: {db.reviews.count_documents({})}")

print("\nDone!")
