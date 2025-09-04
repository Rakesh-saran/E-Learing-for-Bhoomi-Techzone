import requests
import json

base_url = "http://localhost:8000"

print("🚀 Testing Bhoomi Tech E-Learning APIs")
print("=" * 50)

# Test 1: Root endpoint
try:
    response = requests.get(f"{base_url}/")
    print(f"✅ Root endpoint: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Root endpoint failed: {e}")

print("-" * 30)

# Test 2: Home feed endpoint
try:
    response = requests.get(f"{base_url}/home-feed")
    print(f"✅ Home feed: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Home feed failed: {e}")

print("-" * 30)

# Test 3: Register a new user
try:
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "role": "student"
    }
    response = requests.post(f"{base_url}/users/register", json=user_data)
    print(f"✅ User registration: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ User registration failed: {e}")

print("-" * 30)

# Test 4: Login user
try:
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    response = requests.post(f"{base_url}/users/login", json=login_data)
    print(f"✅ User login: {response.status_code}")
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"   Token: {token[:50]}...")
    else:
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ User login failed: {e}")

print("-" * 30)

# Test 5: Get all courses
try:
    response = requests.get(f"{base_url}/courses/")
    print(f"✅ Get courses: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Get courses failed: {e}")

print("-" * 30)

# Test 6: Get all lessons
try:
    response = requests.get(f"{base_url}/lessons/")
    print(f"✅ Get lessons: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Get lessons failed: {e}")

print("\n🎉 API Testing Complete!")
