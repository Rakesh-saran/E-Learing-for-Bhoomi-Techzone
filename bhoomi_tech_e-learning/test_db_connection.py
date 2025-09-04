"""
Test database connection
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing database connection...")
    from src.database.__init_db import db
    print("✅ Database imported successfully")
    
    # Test connection
    result = db.users.count_documents({})
    print(f"✅ Database connected - Users count: {result}")
    
    # Test if we can insert
    test_doc = {"test": "connection", "timestamp": "now"}
    result = db.test_collection.insert_one(test_doc)
    print(f"✅ Can insert documents - ID: {result.inserted_id}")
    
    # Clean up test
    db.test_collection.delete_one({"_id": result.inserted_id})
    print("✅ Test cleanup completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed")
