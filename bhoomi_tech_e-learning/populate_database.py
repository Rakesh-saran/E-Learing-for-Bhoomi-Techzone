"""
Populate database with sample data for testing the admin panel
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.auth import get_password_hash
    from src.database.__init_db import db
    from datetime import datetime, timezone
    from bson import ObjectId
    import random
    
    print("🎓 Populating Bhoomi Tech E-Learning Database")
    print("=" * 50)
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("Clearing existing data...")
    db.users.delete_many({})
    db.courses.delete_many({})
    db.enrollments.delete_many({})
    db.lessons.delete_many({})
    print("✅ Existing data cleared")
    
    # Create Admin User
    print("\n1. Creating Admin User...")
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
    admin_id = admin_result.inserted_id
    print(f"✅ Admin created: {admin_id}")
    
    # Create Instructors
    print("\n2. Creating Instructors...")
    instructors = [
        {"name": "Dr. John Smith", "email": "john@bhoomi.com", "password": "instructor123"},
        {"name": "Prof. Sarah Johnson", "email": "sarah@bhoomi.com", "password": "instructor123"},
        {"name": "Mr. Mike Wilson", "email": "mike@bhoomi.com", "password": "instructor123"},
        {"name": "Dr. Emily Davis", "email": "emily@bhoomi.com", "password": "instructor123"},
        {"name": "Prof. David Brown", "email": "david@bhoomi.com", "password": "instructor123"}
    ]
    
    instructor_ids = []
    for instructor in instructors:
        instructor_data = {
            **instructor,
            "password": get_password_hash(instructor["password"]),
            "role": "instructor",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        result = db.users.insert_one(instructor_data)
        instructor_ids.append(result.inserted_id)
        print(f"✅ Instructor created: {instructor['name']}")
    
    # Create Students
    print("\n3. Creating Students...")
    students = [
        {"name": "Alice Cooper", "email": "alice@example.com"},
        {"name": "Bob Johnson", "email": "bob@example.com"},
        {"name": "Charlie Brown", "email": "charlie@example.com"},
        {"name": "Diana Prince", "email": "diana@example.com"},
        {"name": "Eve Adams", "email": "eve@example.com"},
        {"name": "Frank Miller", "email": "frank@example.com"},
        {"name": "Grace Lee", "email": "grace@example.com"},
        {"name": "Henry Ford", "email": "henry@example.com"},
        {"name": "Ivy Chen", "email": "ivy@example.com"},
        {"name": "Jack Wilson", "email": "jack@example.com"}
    ]
    
    student_ids = []
    for student in students:
        student_data = {
            **student,
            "password": get_password_hash("student123"),
            "role": "student",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        result = db.users.insert_one(student_data)
        student_ids.append(result.inserted_id)
        print(f"✅ Student created: {student['name']}")
    
    # Create Courses
    print("\n4. Creating Courses...")
    courses = [
        {
            "title": "Python Programming Fundamentals",
            "description": "Learn Python programming from scratch with hands-on projects",
            "price": 99.99,
            "duration_minutes": 1200,
            "instructor_id": instructor_ids[0]
        },
        {
            "title": "Web Development with HTML, CSS & JavaScript",
            "description": "Build responsive websites using modern web technologies",
            "price": 149.99,
            "duration_minutes": 1800,
            "instructor_id": instructor_ids[1]
        },
        {
            "title": "Data Science with Python",
            "description": "Master data analysis, visualization, and machine learning",
            "price": 199.99,
            "duration_minutes": 2400,
            "instructor_id": instructor_ids[2]
        },
        {
            "title": "Mobile App Development",
            "description": "Create mobile apps for iOS and Android platforms",
            "price": 179.99,
            "duration_minutes": 2000,
            "instructor_id": instructor_ids[3]
        },
        {
            "title": "Database Design and SQL",
            "description": "Learn database fundamentals and advanced SQL techniques",
            "price": 129.99,
            "duration_minutes": 1500,
            "instructor_id": instructor_ids[4]
        },
        {
            "title": "Digital Marketing Mastery",
            "description": "Complete guide to modern digital marketing strategies",
            "price": 89.99,
            "duration_minutes": 1000,
            "instructor_id": instructor_ids[0]
        },
        {
            "title": "Graphic Design with Adobe Creative Suite",
            "description": "Professional graphic design using Photoshop, Illustrator, and InDesign",
            "price": 159.99,
            "duration_minutes": 1600,
            "instructor_id": instructor_ids[1]
        },
        {
            "title": "Business Analytics and Intelligence",
            "description": "Transform data into actionable business insights",
            "price": 219.99,
            "duration_minutes": 2200,
            "instructor_id": instructor_ids[2]
        }
    ]
    
    course_ids = []
    for course in courses:
        course_data = {
            **course,
            "is_active": True,
            "lessons": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        result = db.courses.insert_one(course_data)
        course_ids.append(result.inserted_id)
        print(f"✅ Course created: {course['title']}")
    
    # Create Sample Lessons for each course
    print("\n5. Creating Lessons...")
    lesson_titles = [
        "Introduction and Overview",
        "Getting Started",
        "Basic Concepts",
        "Hands-on Practice",
        "Advanced Topics",
        "Real-world Examples",
        "Best Practices",
        "Final Project",
        "Review and Summary",
        "Additional Resources"
    ]
    
    total_lessons = 0
    for course_id in course_ids:
        num_lessons = random.randint(5, 10)
        lessons = []
        for i in range(num_lessons):
            lesson_data = {
                "_id": ObjectId(),
                "title": f"{lesson_titles[i % len(lesson_titles)]} {i+1}",
                "description": f"Detailed lesson content for lesson {i+1}",
                "video_url": f"https://example.com/video_{i+1}",
                "duration_minutes": random.randint(15, 60),
                "order": i + 1,
                "is_free": i == 0,  # First lesson is always free
                "created_at": datetime.now(timezone.utc)
            }
            lessons.append(lesson_data)
            total_lessons += 1
        
        # Update course with lessons
        db.courses.update_one(
            {"_id": course_id},
            {"$set": {"lessons": lessons}}
        )
    
    print(f"✅ Created {total_lessons} lessons across all courses")
    
    # Create Enrollments
    print("\n6. Creating Enrollments...")
    enrollment_count = 0
    for student_id in student_ids:
        # Each student enrolls in 2-5 random courses
        num_enrollments = random.randint(2, 5)
        enrolled_courses = random.sample(course_ids, num_enrollments)
        
        for course_id in enrolled_courses:
            enrollment_data = {
                "user_id": student_id,
                "course_id": course_id,
                "enrolled_at": datetime.now(timezone.utc),
                "progress_percentage": random.randint(0, 100),
                "completed_at": None,
                "is_active": True
            }
            db.enrollments.insert_one(enrollment_data)
            enrollment_count += 1
    
    print(f"✅ Created {enrollment_count} enrollments")
    
    # Create Sample Payments
    print("\n7. Creating Sample Payments...")
    payment_count = 0
    for enrollment in db.enrollments.find():
        # 80% chance of having a payment record
        if random.random() < 0.8:
            course = db.courses.find_one({"_id": enrollment["course_id"]})
            payment_data = {
                "user_id": enrollment["user_id"],
                "course_id": enrollment["course_id"],
                "amount": course["price"] if course else 99.99,
                "currency": "USD",
                "status": "completed",
                "payment_method": random.choice(["credit_card", "paypal", "bank_transfer"]),
                "transaction_id": f"txn_{payment_count + 1000}",
                "created_at": datetime.now(timezone.utc)
            }
            db.payments.insert_one(payment_data)
            payment_count += 1
    
    print(f"✅ Created {payment_count} payment records")
    
    # Print Summary
    print("\n" + "=" * 50)
    print("📊 DATABASE POPULATION COMPLETE!")
    print("=" * 50)
    
    # Get final counts
    total_users = db.users.count_documents({})
    total_courses = db.courses.count_documents({})
    total_enrollments = db.enrollments.count_documents({})
    total_payments = db.payments.count_documents({})
    
    print(f"👥 Total Users: {total_users}")
    print(f"   - Admins: {db.users.count_documents({'role': 'admin'})}")
    print(f"   - Instructors: {db.users.count_documents({'role': 'instructor'})}")
    print(f"   - Students: {db.users.count_documents({'role': 'student'})}")
    print(f"📚 Total Courses: {total_courses}")
    print(f"🎓 Total Enrollments: {total_enrollments}")
    print(f"💰 Total Payments: {total_payments}")
    print(f"📝 Total Lessons: {total_lessons}")
    
    print(f"\n🎉 Your admin panel now has data to display!")
    print("🔐 Login credentials:")
    print("   Email: admin@bhoomi.com")
    print("   Password: admin123")
    
    print("\n📱 You can now test:")
    print("   ✅ Dashboard statistics")
    print("   ✅ User management")
    print("   ✅ Course management")
    print("   ✅ Enrollment tracking")
    print("   ✅ Payment records")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

input("\nPress Enter to continue...")
