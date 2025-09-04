"""
Create default admin user for Bhoomi Tech E-Learning Platform
Run this script to ensure admin user exists
"""
import asyncio
import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.__init_db import db
from database.repositories.user_repository import UserRepository
from auth import get_password_hash
from datetime import datetime, timezone

async def create_admin_user():
    """Create default admin user if it doesn't exist"""
    
    try:
        # Check if admin user already exists
        existing_admin = UserRepository.find_by_email("admin@bhoomi.com")
        if existing_admin:
            print("✅ Admin user already exists!")
            print(f"   Email: {existing_admin['email']}")
            print(f"   Role: {existing_admin['role']}")
            return existing_admin
        
        # Create admin user
        admin_data = {
            "name": "Admin User",
            "email": "admin@bhoomi.com",
            "password": "admin123",  # Will be hashed
            "role": "admin",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        # Hash the password
        admin_data["password"] = get_password_hash(admin_data["password"])
        
        # Insert into database
        result = db.users.insert_one(admin_data)
        
        if result.inserted_id:
            print("🎉 Admin user created successfully!")
            print(f"   Email: admin@bhoomi.com")
            print(f"   Password: admin123")
            print(f"   Role: admin")
            print(f"   ID: {result.inserted_id}")
            return admin_data
        else:
            print("❌ Failed to create admin user")
            return None
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return None

async def create_sample_users():
    """Create some sample users for testing"""
    
    sample_users = [
        {
            "name": "John Instructor",
            "email": "instructor@bhoomi.com",
            "password": "instructor123",
            "role": "instructor"
        },
        {
            "name": "Alice Student",
            "email": "alice@example.com",
            "password": "student123",
            "role": "student"
        },
        {
            "name": "Bob Student",
            "email": "bob@example.com",
            "password": "student123",
            "role": "student"
        }
    ]
    
    created_count = 0
    
    for user_data in sample_users:
        try:
            # Check if user already exists
            existing_user = UserRepository.find_by_email(user_data["email"])
            if existing_user:
                continue
            
            # Add timestamps and hash password
            user_data["is_active"] = True
            user_data["created_at"] = datetime.now(timezone.utc)
            user_data["updated_at"] = datetime.now(timezone.utc)
            user_data["password"] = get_password_hash(user_data["password"])
            
            # Insert into database
            result = db.users.insert_one(user_data.copy())
            
            if result.inserted_id:
                created_count += 1
                print(f"✅ Created user: {user_data['name']} ({user_data['role']})")
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['name']}: {e}")
    
    if created_count > 0:
        print(f"\n🎉 Created {created_count} sample users!")
    else:
        print("\nℹ️  All sample users already exist")

async def main():
    print("🎓 Bhoomi Tech E-Learning - Admin Setup")
    print("=" * 50)
    
    # Create admin user
    admin = await create_admin_user()
    
    if admin:
        print("\n" + "=" * 50)
        print("Creating sample users...")
        await create_sample_users()
        
        print("\n" + "=" * 50)
        print("📊 Database Summary:")
        
        # Count users by role
        total_users = db.users.count_documents({})
        admin_count = db.users.count_documents({"role": "admin"})
        instructor_count = db.users.count_documents({"role": "instructor"})
        student_count = db.users.count_documents({"role": "student"})
        
        print(f"   Total Users: {total_users}")
        print(f"   Admins: {admin_count}")
        print(f"   Instructors: {instructor_count}")
        print(f"   Students: {student_count}")
        
        print("\n✅ Setup completed successfully!")
        print("\nYou can now login to the admin panel with:")
        print("   Email: admin@bhoomi.com")
        print("   Password: admin123")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
