import requests
import json

def test_basic_endpoints():
    base_url = "http://localhost:8000"
    
    print("🚀 Quick API Test")
    print("=" * 50)
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    print("-" * 50)
    
    # Test 2: Home feed
    try:
        response = requests.get(f"{base_url}/home-feed")
        print(f"✅ Home feed: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Home feed failed: {e}")
    
    print("-" * 50)
    
    # Test 3: Get all courses
    try:
        response = requests.get(f"{base_url}/courses/")
        print(f"✅ Get courses: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Get courses failed: {e}")
    
    print("-" * 50)
    
    # Test 4: Get all users
    try:
        response = requests.get(f"{base_url}/users/")
        print(f"✅ Get users: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Get users failed: {e}")
    
    print("-" * 50)
    
    # Test 5: Register a new user
    try:
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "role": "student"
        }
        response = requests.post(f"{base_url}/users/register", json=user_data)
        print(f"✅ Register user: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Register user failed: {e}")
    
    print("\n🎉 Quick test completed!")

if __name__ == "__main__":
    test_basic_endpoints()
