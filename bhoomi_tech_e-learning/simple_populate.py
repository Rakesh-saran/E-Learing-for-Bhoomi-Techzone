"""
Simple database population script
"""
from pymongo import MongoClient
from datetime import datetime, timezone
from bson import ObjectId
import bcrypt
import random
import sys
import os

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

try:
    # Connect to MongoDB
    print("🔗 Connecting to MongoDB...")
    client = MongoClient("mongodb://localhost:27017/e_learning")
    db = client.get_database()
    print("✅ Connected to database")
    
    # Clear existing data (optional)
    print("\n🗑️ Clearing existing data...")
    db.users.delete_many({})
    db.courses.delete_many({})
    db.enrollments.delete_many({})
    db.payments.delete_many({})
    print("✅ Data cleared")
    
    # Create Admin User
    print("\n👤 Creating Admin User...")
    admin_data = {
        "name": "Admin User",
        "email": "admin@bhoomi.com",
        "password": get_password_hash("admin123"),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    admin_result = db.users.insert_one(admin_data)
    print(f"✅ Admin created with ID: {admin_result.inserted_id}")
    
    # Create Students
    print("\n🎓 Creating Students...")
    students_data = [
        {"name": "Alice Cooper", "email": "alice@example.com"},
        {"name": "Bob Johnson", "email": "bob@example.com"},
        {"name": "Charlie Brown", "email": "charlie@example.com"},
        {"name": "Diana Prince", "email": "diana@example.com"},
        {"name": "Eve Adams", "email": "eve@example.com"}
    ]
    
    student_ids = []
    for student in students_data:
        student_doc = {
            **student,
            "password": get_password_hash("student123"),
            "role": "student",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        result = db.users.insert_one(student_doc)
        student_ids.append(result.inserted_id)
        print(f"✅ Student created: {student['name']}")
    
    # Create Instructors
    print("\n👨‍🏫 Creating Instructors...")
    instructors_data = [
        {"name": "Dr. John Smith", "email": "john@bhoomi.com"},
        {"name": "Prof. Sarah Johnson", "email": "sarah@bhoomi.com"},
        {"name": "Mr. Mike Wilson", "email": "mike@bhoomi.com"}
    ]
    
    instructor_ids = []
    for instructor in instructors_data:
        instructor_doc = {
            **instructor,
            "password": get_password_hash("instructor123"),
            "role": "instructor",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        result = db.users.insert_one(instructor_doc)
        instructor_ids.append(result.inserted_id)
        print(f"✅ Instructor created: {instructor['name']}")
    
    # Create Courses
    print("\n📚 Creating Courses...")
    courses_data = [
        {"title": "Python Programming", "description": "Learn Python from basics", "price": 99.99},
        {"title": "Web Development", "description": "HTML, CSS, JavaScript course", "price": 149.99},
        {"title": "Data Science", "description": "Data analysis with Python", "price": 199.99},
        {"title": "Mobile Development", "description": "Build mobile apps", "price": 179.99},
        {"title": "Digital Marketing", "description": "Modern marketing strategies", "price": 89.99}
    ]
    
    course_ids = []
    for i, course in enumerate(courses_data):
        course_doc = {
            **course,
            "instructor_id": instructor_ids[i % len(instructor_ids)],
            "duration_minutes": random.randint(600, 2400),
            "is_active": True,
            "lessons": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        result = db.courses.insert_one(course_doc)
        course_ids.append(result.inserted_id)
        print(f"✅ Course created: {course['title']}")
    
    # Create Enrollments
    print("\n📝 Creating Enrollments...")
    enrollment_count = 0
    for student_id in student_ids:
        # Each student enrolls in 2-3 courses
        enrolled_courses = random.sample(course_ids, random.randint(2, 3))
        for course_id in enrolled_courses:
            enrollment_doc = {
                "user_id": student_id,
                "course_id": course_id,
                "enrolled_at": datetime.now(timezone.utc),
                "progress_percentage": random.randint(0, 100),
                "completed_at": None,
                "is_active": True
            }
            db.enrollments.insert_one(enrollment_doc)
            enrollment_count += 1
    
    print(f"✅ Created {enrollment_count} enrollments")
    
    # Create Payments
    print("\n💰 Creating Payments...")
    payment_count = 0
    for enrollment in db.enrollments.find():
        course = db.courses.find_one({"_id": enrollment["course_id"]})
        payment_doc = {
            "user_id": enrollment["user_id"],
            "course_id": enrollment["course_id"],
            "amount": course["price"],
            "currency": "USD",
            "status": "completed",
            "payment_method": random.choice(["credit_card", "paypal"]),
            "transaction_id": f"txn_{payment_count + 1000}",
            "created_at": datetime.now(timezone.utc)
        }
        db.payments.insert_one(payment_doc)
        payment_count += 1
    
    print(f"✅ Created {payment_count} payments")
    
    # Final Summary
    print("\n" + "="*50)
    print("🎉 DATABASE POPULATED SUCCESSFULLY!")
    print("="*50)
    print(f"👥 Users: {db.users.count_documents({})}")
    print(f"📚 Courses: {db.courses.count_documents({})}")
    print(f"📝 Enrollments: {db.enrollments.count_documents({})}")
    print(f"💰 Payments: {db.payments.count_documents({})}")
    
    print("\n🔐 Admin Login:")
    print("Email: admin@bhoomi.com")
    print("Password: admin123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone! Press Enter to continue...")
input()
