#!/usr/bin/env python3
"""
Setup script for Bhoomi Tech E-Learning Admin Panel
This script creates the initial admin user and sets up the system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.__init_db import users_collection
from auth import get_password_hash
from datetime import datetime, timezone
import getpass

def create_admin_user():
    """Create the initial admin user"""
    print("🚀 Bhoomi Tech E-Learning Admin Setup")
    print("=" * 40)
    
    # Check if admin already exists
    admin_exists = users_collection.find_one({"role": "admin"})
    if admin_exists:
        print("⚠️  Admin user already exists!")
        print(f"   Email: {admin_exists['email']}")
        response = input("Do you want to create another admin user? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Get admin details
    print("\n📝 Enter admin user details:")
    name = input("Full Name: ").strip()
    if not name:
        print("❌ Name is required!")
        return
    
    email = input("Email: ").strip()
    if not email or '@' not in email:
        print("❌ Valid email is required!")
        return
    
    # Check if email already exists
    if users_collection.find_one({"email": email}):
        print("❌ User with this email already exists!")
        return
    
    password = getpass.getpass("Password: ")
    if len(password) < 6:
        print("❌ Password must be at least 6 characters!")
        return
    
    confirm_password = getpass.getpass("Confirm Password: ")
    if password != confirm_password:
        print("❌ Passwords do not match!")
        return
    
    # Create admin user
    admin_data = {
        "name": name,
        "email": email,
        "password": get_password_hash(password),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
    
    try:
        result = users_collection.insert_one(admin_data)
        print(f"\n✅ Admin user created successfully!")
        print(f"   User ID: {result.inserted_id}")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Role: admin")
        
        print("\n🎉 Setup completed!")
        print("\nYou can now:")
        print("1. Start the server: python src/main.py")
        print("2. Test the API: python test_admin_api.py")
        print("3. Access admin endpoints at: http://localhost:8000/admin/")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")

def create_sample_data():
    """Create sample data for testing"""
    response = input("\nDo you want to create sample data? (y/N): ")
    if response.lower() != 'y':
        return
    
    print("\n📊 Creating sample data...")
    
    # Create sample instructor
    instructor_data = {
        "name": "John Instructor",
        "email": "instructor@bhoomi.com",
        "password": get_password_hash("instructor123"),
        "role": "instructor",
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
    
    try:
        if not users_collection.find_one({"email": "instructor@bhoomi.com"}):
            users_collection.insert_one(instructor_data)
            print("✅ Sample instructor created")
    except Exception as e:
        print(f"❌ Error creating instructor: {str(e)}")
    
    # Create sample students
    students = [
        {"name": "Alice Student", "email": "alice@example.com"},
        {"name": "Bob Student", "email": "bob@example.com"},
        {"name": "Carol Student", "email": "carol@example.com"}
    ]
    
    for student in students:
        student_data = {
            "name": student["name"],
            "email": student["email"],
            "password": get_password_hash("student123"),
            "role": "student",
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        
        try:
            if not users_collection.find_one({"email": student["email"]}):
                users_collection.insert_one(student_data)
                print(f"✅ Sample student created: {student['name']}")
        except Exception as e:
            print(f"❌ Error creating student {student['name']}: {str(e)}")
    
    print("\n✅ Sample data creation completed!")

def show_system_info():
    """Show system information"""
    print("\n📊 System Information:")
    print(f"   Total users: {users_collection.count_documents({})}")
    print(f"   Admins: {users_collection.count_documents({'role': 'admin'})}")
    print(f"   Instructors: {users_collection.count_documents({'role': 'instructor'})}")
    print(f"   Students: {users_collection.count_documents({'role': 'student'})}")

if __name__ == "__main__":
    try:
        create_admin_user()
        create_sample_data()
        show_system_info()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
