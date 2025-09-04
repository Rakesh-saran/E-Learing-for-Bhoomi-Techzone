"""
Simple admin user creation script
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.auth import get_password_hash
    from src.database.__init_db import db
    from datetime import datetime, timezone
    
    print("🎓 Creating Admin User...")
    print("=" * 40)
    
    # Check if admin exists
    existing_admin = db.users.find_one({"email": "admin@bhoomi.com"})
    
    if existing_admin:
        print("✅ Admin user already exists!")
        print(f"   Name: {existing_admin.get('name', 'N/A')}")
        print(f"   Email: {existing_admin['email']}")
        print(f"   Role: {existing_admin.get('role', 'N/A')}")
        print(f"   Active: {existing_admin.get('is_active', 'N/A')}")
        
        # Test password
        from src.auth import verify_password
        if verify_password("admin123", existing_admin["password"]):
            print("✅ Password verification: PASSED")
        else:
            print("❌ Password verification: FAILED")
            print("   Updating password...")
            db.users.update_one(
                {"email": "admin@bhoomi.com"}, 
                {"$set": {"password": get_password_hash("admin123")}}
            )
            print("✅ Password updated!")
    else:
        print("Creating new admin user...")
        
        admin_data = {
            "name": "Admin User",
            "email": "admin@bhoomi.com",
            "password": get_password_hash("admin123"),
            "role": "admin",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        result = db.users.insert_one(admin_data)
        
        if result.inserted_id:
            print("✅ Admin user created successfully!")
            print(f"   ID: {result.inserted_id}")
            print(f"   Email: admin@bhoomi.com")
            print(f"   Password: admin123")
        else:
            print("❌ Failed to create admin user")
    
    print("\n" + "=" * 40)
    print("📊 Database Statistics:")
    total_users = db.users.count_documents({})
    admin_users = db.users.count_documents({"role": "admin"})
    print(f"   Total Users: {total_users}")
    print(f"   Admin Users: {admin_users}")
    
    print("\n✅ Setup completed! You can now login with:")
    print("   Email: admin@bhoomi.com")
    print("   Password: admin123")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Error: {e}")

input("\nPress Enter to continue...")
