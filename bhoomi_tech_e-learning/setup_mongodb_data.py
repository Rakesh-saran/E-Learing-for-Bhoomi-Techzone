#!/usr/bin/env python3
"""
Manual MongoDB Data Creation Script
This script directly connects to MongoDB and creates sample data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from pymongo import MongoClient
from datetime import datetime, timezone
import bcrypt

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017/bhoomi_elearning"
client = MongoClient(MONGO_URL)
db = client.get_database()

# Collections
users_collection = db["users"]
courses_collection = db["courses"]
enrollments_collection = db["enrollments"]
payments_collection = db["payments"]

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_admin_user():
    """Create admin user"""
    print("🔧 Creating admin user...")
    
    # Check if admin already exists
    existing_admin = users_collection.find_one({"email": "admin@bhoomi.com"})
    if existing_admin:
        print("✅ Admin user already exists!")
        return str(existing_admin["_id"])
    
    admin_data = {
        "name": "Admin User",
        "email": "admin@bhoomi.com", 
        "password": hash_password("admin123"),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
    
    result = users_collection.insert_one(admin_data)
    print(f"✅ Admin user created with ID: {result.inserted_id}")
    return str(result.inserted_id)

def create_instructor_user():
    """Create instructor user"""
    print("👨‍🏫 Creating instructor user...")
    
    existing_instructor = users_collection.find_one({"email": "instructor@bhoomi.com"})
    if existing_instructor:
        print("✅ Instructor user already exists!")
        return str(existing_instructor["_id"])
    
    instructor_data = {
        "name": "John Instructor",
        "email": "instructor@bhoomi.com",
        "password": hash_password("instructor123"),
        "role": "instructor", 
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
    
    result = users_collection.insert_one(instructor_data)
    print(f"✅ Instructor user created with ID: {result.inserted_id}")
    return str(result.inserted_id)

def create_student_users():
    """Create sample student users"""
    print("👥 Creating student users...")
    
    students = [
        {"name": "Alice Johnson", "email": "alice@example.com"},
        {"name": "Bob Smith", "email": "bob@example.com"},
        {"name": "Carol Wilson", "email": "carol@example.com"},
        {"name": "David Brown", "email": "david@example.com"},
        {"name": "Eva Davis", "email": "eva@example.com"}
    ]
    
    student_ids = []
    
    for student in students:
        existing_student = users_collection.find_one({"email": student["email"]})
        if existing_student:
            student_ids.append(str(existing_student["_id"]))
            print(f"✅ Student {student['name']} already exists!")
            continue
            
        student_data = {
            "name": student["name"],
            "email": student["email"],
            "password": hash_password("student123"),
            "role": "student",
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        
        result = users_collection.insert_one(student_data)
        student_ids.append(str(result.inserted_id))
        print(f"✅ Student {student['name']} created!")
    
    return student_ids

def create_sample_courses(instructor_id):
    """Create sample courses"""
    print("📚 Creating sample courses...")
    
    courses = [
        {
            "title": "Python Programming Basics",
            "description": "Learn Python programming from scratch. Perfect for beginners who want to start their coding journey.",
            "price": 99.99
        },
        {
            "title": "Web Development with JavaScript",
            "description": "Master modern web development using JavaScript, HTML, and CSS. Build responsive websites.",
            "price": 149.99
        },
        {
            "title": "Data Science Fundamentals", 
            "description": "Introduction to data science, statistics, and machine learning using Python and popular libraries.",
            "price": 199.99
        },
        {
            "title": "Mobile App Development",
            "description": "Create mobile applications for Android and iOS using modern frameworks and tools.",
            "price": 179.99
        }
    ]
    
    course_ids = []
    
    for course in courses:
        existing_course = courses_collection.find_one({"title": course["title"]})
        if existing_course:
            course_ids.append(str(existing_course["_id"]))
            print(f"✅ Course '{course['title']}' already exists!")
            continue
        
        from bson import ObjectId
        course_data = {
            "title": course["title"],
            "description": course["description"],
            "instructor_id": ObjectId(instructor_id),
            "lessons": [],  # Empty for now
            "price": course["price"],
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        
        result = courses_collection.insert_one(course_data)
        course_ids.append(str(result.inserted_id))
        print(f"✅ Course '{course['title']}' created!")
    
    return course_ids

def create_sample_enrollments(student_ids, course_ids):
    """Create sample enrollments"""
    print("🎓 Creating sample enrollments...")
    
    import random
    enrollment_count = 0
    
    # Each student enrolls in 1-3 random courses
    for student_id in student_ids:
        from bson import ObjectId
        num_courses = random.randint(1, 3)
        selected_courses = random.sample(course_ids, num_courses)
        
        for course_id in selected_courses:
            existing_enrollment = enrollments_collection.find_one({
                "user_id": ObjectId(student_id),
                "course_id": ObjectId(course_id)
            })
            
            if existing_enrollment:
                continue
                
            enrollment_data = {
                "user_id": ObjectId(student_id),
                "course_id": ObjectId(course_id),
                "enrolled_at": datetime.now(timezone.utc),
                "progress": random.randint(0, 100),  # Random progress
                "completed": random.choice([True, False])
            }
            
            enrollments_collection.insert_one(enrollment_data)
            enrollment_count += 1
    
    print(f"✅ Created {enrollment_count} enrollments!")

def create_sample_payments(student_ids, course_ids):
    """Create sample payments"""
    print("💳 Creating sample payments...")
    
    import random
    payment_count = 0
    
    # Create payments for some enrollments
    enrollments = list(enrollments_collection.find())
    
    for enrollment in enrollments[:10]:  # First 10 enrollments get payments
        course = courses_collection.find_one({"_id": enrollment["course_id"]})
        if not course:
            continue
            
        payment_data = {
            "user_id": enrollment["user_id"],
            "course_id": enrollment["course_id"],
            "amount": course["price"],
            "status": random.choice(["completed", "completed", "completed", "pending"]),  # Mostly completed
            "payment_method": random.choice(["card", "paypal", "bank_transfer"]),
            "payment_date": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc)
        }
        
        payments_collection.insert_one(payment_data)
        payment_count += 1
    
    print(f"✅ Created {payment_count} payments!")

def show_database_stats():
    """Show database statistics"""
    print("\n📊 Database Statistics:")
    print(f"   👥 Users: {users_collection.count_documents({})}")
    print(f"      - Admins: {users_collection.count_documents({'role': 'admin'})}")
    print(f"      - Instructors: {users_collection.count_documents({'role': 'instructor'})}")
    print(f"      - Students: {users_collection.count_documents({'role': 'student'})}")
    print(f"   📚 Courses: {courses_collection.count_documents({})}")
    print(f"   🎓 Enrollments: {enrollments_collection.count_documents({})}")
    print(f"   💳 Payments: {payments_collection.count_documents({})}")
    
    print("\n🔍 Sample Data:")
    print("   Admin Login: admin@bhoomi.com / admin123")
    print("   Instructor Login: instructor@bhoomi.com / instructor123") 
    print("   Student Login: alice@example.com / student123 (and others)")

def main():
    print("🚀 Setting up MongoDB data for Bhoomi Tech E-Learning")
    print("=" * 60)
    
    try:
        # Test connection
        client.admin.command('ismaster')
        print(f"✅ Connected to MongoDB: {MONGO_URL}")
        
        # Create users
        admin_id = create_admin_user()
        instructor_id = create_instructor_user()
        student_ids = create_student_users()
        
        # Create courses
        course_ids = create_sample_courses(instructor_id)
        
        # Create enrollments
        create_sample_enrollments(student_ids, course_ids)
        
        # Create payments
        create_sample_payments(student_ids, course_ids)
        
        # Show stats
        show_database_stats()
        
        print("\n🎉 Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Your API server should be running on http://localhost:8000")
        print("2. Visit http://localhost:8000/docs for API documentation")
        print("3. Login with admin credentials to get access token")
        print("4. Use the token to access admin endpoints")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure MongoDB is running on localhost:27017")

if __name__ == "__main__":
    main()
