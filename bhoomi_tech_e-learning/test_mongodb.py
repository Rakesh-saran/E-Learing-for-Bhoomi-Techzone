import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

print("🔧 Testing MongoDB Connection...")

try:
    from pymongo import MongoClient
    print("✅ PyMongo imported successfully")
    
    # Try to connect
    MONGO_URL = "mongodb://localhost:27017/bhoomi_elearning"
    print(f"🔗 Connecting to: {MONGO_URL}")
    
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.admin.command('ismaster')
    print("✅ MongoDB connection successful!")
    
    # Get database
    db = client.get_database()
    print(f"✅ Database connected: {db.name}")
    
    # Test collections
    users_collection = db["users"]
    print("✅ Users collection accessible")
    
    # Count existing documents
    user_count = users_collection.count_documents({})
    print(f"📊 Current users in database: {user_count}")
    
    # Test insert capability
    test_doc = {"test": "connection", "timestamp": "2025-09-04"}
    result = users_collection.insert_one(test_doc)
    print(f"✅ Test insert successful: {result.inserted_id}")
    
    # Remove test document
    users_collection.delete_one({"_id": result.inserted_id})
    print("✅ Test cleanup successful")
    
    print("\n🎉 MongoDB is working correctly!")
    
except Exception as e:
    print(f"❌ MongoDB Error: {str(e)}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure MongoDB is installed and running")
    print("2. Check if MongoDB service is started")
    print("3. Verify MongoDB is running on localhost:27017")
    print("4. Try starting MongoDB with: mongod --dbpath /data/db")
