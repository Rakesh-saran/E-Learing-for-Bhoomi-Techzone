#!/usr/bin/env python3
"""
Simple test script to verify the admin API is working
"""

import json
import time

def test_basic_endpoints():
    """Test basic endpoints without authentication"""
    try:
        import requests
        
        base_url = "http://localhost:8000"
        
        print("🚀 Testing Bhoomi Tech E-Learning Admin API...")
        print("=" * 50)
        
        # Test root endpoint
        print("\n📡 Testing root endpoint...")
        try:
            response = requests.get(f"{base_url}/")
            if response.status_code == 200:
                print("✅ Root endpoint working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Root endpoint error: {str(e)}")
        
        # Test docs endpoint
        print("\n📚 Testing API docs...")
        try:
            response = requests.get(f"{base_url}/docs")
            if response.status_code == 200:
                print("✅ API docs accessible at http://localhost:8000/docs")
            else:
                print(f"❌ API docs failed: {response.status_code}")
        except Exception as e:
            print(f"❌ API docs error: {str(e)}")
        
        # Test home feed
        print("\n🏠 Testing home feed...")
        try:
            response = requests.get(f"{base_url}/home-feed")
            if response.status_code == 200:
                data = response.json()
                print("✅ Home feed working")
                print(f"   Courses: {len(data.get('courses', []))}")
            else:
                print(f"❌ Home feed failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Home feed error: {str(e)}")
        
        print("\n" + "=" * 50)
        print("✅ Basic API test completed!")
        print("\n🔐 To test admin endpoints, you need to:")
        print("1. Create an admin user: python setup_admin.py")
        print("2. Login via /users/login to get a token")
        print("3. Use the token to access /admin/* endpoints")
        print("\n📖 Full API documentation: http://localhost:8000/docs")
        
    except ImportError:
        print("❌ Requests library not found. Install with: pip install requests")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_basic_endpoints()
