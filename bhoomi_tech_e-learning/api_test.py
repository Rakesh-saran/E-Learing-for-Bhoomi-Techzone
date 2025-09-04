import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:8000"

print("🚀 Testing Bhoomi Tech E-Learning API")
print("=" * 40)

def test_root_endpoint():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
    except Exception as e:
        print(f"❌ Root endpoint error: {str(e)}")
    return False

def test_register_admin():
    """Test admin registration"""
    try:
        admin_data = {
            "name": "Admin User",
            "email": "admin@bhoomi.com", 
            "password": "admin123",
            "role": "admin"
        }
        
        response = requests.post(f"{BASE_URL}/users/register", json=admin_data)
        print(f"Admin registration: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Admin user created successfully!")
            return True
        elif response.status_code == 400:
            print("ℹ️ Admin user might already exist")
            return True
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Admin registration error: {str(e)}")
    return False

def test_login_admin():
    """Test admin login"""
    try:
        login_data = {
            "email": "admin@bhoomi.com",
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        print(f"Admin login: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access_token')
            print("✅ Admin login successful!")
            print(f"Token: {token[:50]}...")
            return token
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Admin login error: {str(e)}")
    return None

def test_admin_dashboard(token):
    """Test admin dashboard"""
    if not token:
        return False
        
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{BASE_URL}/admin/dashboard", headers=headers)
        print(f"Admin dashboard: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin dashboard loaded!")
            print(f"Total users: {data.get('stats', {}).get('total_users', 0)}")
            return True
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Dashboard error: {str(e)}")
    return False

def test_create_sample_users(token):
    """Create sample users through API"""
    if not token:
        return False
        
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    sample_users = [
        {"name": "John Instructor", "email": "instructor@bhoomi.com", "password": "instructor123", "role": "instructor"},
        {"name": "Alice Student", "email": "alice@example.com", "password": "student123", "role": "student"},
        {"name": "Bob Student", "email": "bob@example.com", "password": "student123", "role": "student"}
    ]
    
    for user in sample_users:
        try:
            response = requests.post(f"{BASE_URL}/admin/users", json=user, headers=headers)
            if response.status_code == 201:
                print(f"✅ Created user: {user['name']}")
            elif response.status_code == 400:
                print(f"ℹ️ User {user['name']} might already exist")
            else:
                print(f"❌ Failed to create {user['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Error creating {user['name']}: {str(e)}")

def main():
    print("Testing API connectivity...")
    
    # Test root endpoint
    if not test_root_endpoint():
        print("❌ API server is not responding. Make sure it's running on http://localhost:8000")
        return
    
    # Register admin
    test_register_admin()
    
    # Login admin 
    token = test_login_admin()
    if not token:
        print("❌ Could not get admin token")
        return
    
    # Test dashboard
    if test_admin_dashboard(token):
        print("✅ Admin panel is working!")
    
    # Create sample users
    print("\n📝 Creating sample users...")
    test_create_sample_users(token)
    
    # Test dashboard again
    print("\n📊 Testing dashboard with new data...")
    test_admin_dashboard(token)
    
    print("\n🎉 API testing completed!")
    print("You can now:")
    print("1. Visit http://localhost:8000/docs for API documentation")
    print("2. Login with admin@bhoomi.com / admin123")
    print("3. Use admin endpoints with the Bearer token")

if __name__ == "__main__":
    main()
