import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@bhoomi.com"
ADMIN_PASSWORD = "admin123"

class AdminAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
    
    def login_admin(self):
        """Login and get admin token"""
        try:
            # First, create an admin user if not exists
            admin_data = {
                "name": "Admin User",
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD,
                "role": "admin"
            }
            
            # Try to create admin user (might fail if already exists)
            try:
                response = requests.post(f"{self.base_url}/users/register", 
                                       json=admin_data, headers=self.headers)
                print(f"Admin user creation: {response.status_code}")
            except:
                pass
            
            # Login
            login_data = {
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }
            
            response = requests.post(f"{self.base_url}/users/login", 
                                   json=login_data, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get('access_token')
                self.headers['Authorization'] = f"Bearer {self.token}"
                print("✅ Admin login successful")
                return True
            else:
                print(f"❌ Admin login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def test_dashboard(self):
        """Test dashboard endpoint"""
        print("\n📊 Testing Dashboard...")
        try:
            response = requests.get(f"{self.base_url}/admin/dashboard", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                print("✅ Dashboard loaded successfully")
                print(f"   Total Users: {data.get('stats', {}).get('total_users', 0)}")
                print(f"   Total Courses: {data.get('stats', {}).get('total_courses', 0)}")
                print(f"   Total Enrollments: {data.get('stats', {}).get('total_enrollments', 0)}")
                return True
            else:
                print(f"❌ Dashboard failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Dashboard error: {str(e)}")
            return False
    
    def test_users_crud(self):
        """Test user CRUD operations"""
        print("\n👥 Testing User CRUD Operations...")
        
        # Test GET users
        try:
            response = requests.get(f"{self.base_url}/admin/users", headers=self.headers)
            if response.status_code == 200:
                print("✅ Get users successful")
                users_data = response.json()
                print(f"   Found {len(users_data.get('users', []))} users")
            else:
                print(f"❌ Get users failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Get users error: {str(e)}")
        
        # Test CREATE user
        test_user = {
            "name": "Test User API",
            "email": f"testapi{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "testpass123",
            "role": "student",
            "is_active": True
        }
        
        try:
            response = requests.post(f"{self.base_url}/admin/users", 
                                   json=test_user, headers=self.headers)
            if response.status_code == 201:
                result = response.json()
                user_id = result.get('user_id')
                print("✅ Create user successful")
                print(f"   New user ID: {user_id}")
                
                # Test UPDATE user
                if user_id:
                    update_data = {
                        "name": "Updated Test User",
                        "is_active": False
                    }
                    
                    response = requests.put(f"{self.base_url}/admin/users/{user_id}", 
                                          json=update_data, headers=self.headers)
                    if response.status_code == 200:
                        print("✅ Update user successful")
                    else:
                        print(f"❌ Update user failed: {response.status_code}")
                    
                    # Test GET specific user
                    response = requests.get(f"{self.base_url}/admin/users/{user_id}", 
                                          headers=self.headers)
                    if response.status_code == 200:
                        user_details = response.json()
                        print("✅ Get user details successful")
                        print(f"   User name: {user_details.get('name')}")
                        print(f"   User active: {user_details.get('is_active')}")
                    else:
                        print(f"❌ Get user details failed: {response.status_code}")
                    
                    # Test DELETE user (soft delete)
                    response = requests.delete(f"{self.base_url}/admin/users/{user_id}", 
                                             headers=self.headers)
                    if response.status_code == 200:
                        print("✅ Delete user successful")
                    else:
                        print(f"❌ Delete user failed: {response.status_code}")
                        
            else:
                print(f"❌ Create user failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ User CRUD error: {str(e)}")
    
    def test_courses_crud(self):
        """Test course CRUD operations"""
        print("\n📚 Testing Course CRUD Operations...")
        
        # First, get an instructor for the course
        try:
            response = requests.get(f"{self.base_url}/admin/users?role=instructor", 
                                  headers=self.headers)
            if response.status_code == 200:
                users_data = response.json()
                instructors = [u for u in users_data.get('users', []) if u.get('role') == 'instructor']
                
                if not instructors:
                    # Create an instructor first
                    instructor_data = {
                        "name": "Test Instructor",
                        "email": f"instructor{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
                        "password": "instrpass123",
                        "role": "instructor",
                        "is_active": True
                    }
                    
                    response = requests.post(f"{self.base_url}/admin/users", 
                                           json=instructor_data, headers=self.headers)
                    if response.status_code == 201:
                        instructor_id = response.json().get('user_id')
                        print("✅ Created test instructor")
                    else:
                        print("❌ Failed to create instructor")
                        return
                else:
                    instructor_id = instructors[0]['id']
                    print("✅ Found existing instructor")
                
                # Test CREATE course
                test_course = {
                    "title": f"Test Course API {datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "description": "This is a test course created via API",
                    "instructor_id": instructor_id,
                    "lessons": [],
                    "price": 99.99,
                    "is_active": True
                }
                
                response = requests.post(f"{self.base_url}/admin/courses", 
                                       json=test_course, headers=self.headers)
                if response.status_code == 201:
                    result = response.json()
                    course_id = result.get('course_id')
                    print("✅ Create course successful")
                    print(f"   New course ID: {course_id}")
                    
                    # Test UPDATE course
                    if course_id:
                        update_data = {
                            "title": "Updated Test Course",
                            "price": 149.99,
                            "is_active": False
                        }
                        
                        response = requests.put(f"{self.base_url}/admin/courses/{course_id}", 
                                              json=update_data, headers=self.headers)
                        if response.status_code == 200:
                            print("✅ Update course successful")
                        else:
                            print(f"❌ Update course failed: {response.status_code}")
                        
                        # Test GET specific course
                        response = requests.get(f"{self.base_url}/admin/courses/{course_id}", 
                                              headers=self.headers)
                        if response.status_code == 200:
                            course_details = response.json()
                            print("✅ Get course details successful")
                            print(f"   Course title: {course_details.get('title')}")
                            print(f"   Course price: ${course_details.get('price')}")
                        else:
                            print(f"❌ Get course details failed: {response.status_code}")
                
                else:
                    print(f"❌ Create course failed: {response.status_code} - {response.text}")
                    
        except Exception as e:
            print(f"❌ Course CRUD error: {str(e)}")
    
    def test_analytics(self):
        """Test analytics endpoints"""
        print("\n📈 Testing Analytics...")
        
        endpoints = [
            "/admin/analytics/users",
            "/admin/analytics/courses", 
            "/admin/analytics/instructors"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
                if response.status_code == 200:
                    print(f"✅ {endpoint} successful")
                else:
                    print(f"❌ {endpoint} failed: {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint} error: {str(e)}")
    
    def test_system_health(self):
        """Test system endpoints"""
        print("\n🔧 Testing System Endpoints...")
        
        try:
            response = requests.get(f"{self.base_url}/admin/system/health", headers=self.headers)
            if response.status_code == 200:
                health_data = response.json()
                print("✅ System health check successful")
                print(f"   Status: {health_data.get('status')}")
                print(f"   Database: {health_data.get('database')}")
            else:
                print(f"❌ System health failed: {response.status_code}")
                
            response = requests.get(f"{self.base_url}/admin/system/stats", headers=self.headers)
            if response.status_code == 200:
                stats_data = response.json()
                print("✅ System stats successful")
                collection_stats = stats_data.get('collection_stats', {})
                print(f"   Collections: {len(collection_stats)}")
            else:
                print(f"❌ System stats failed: {response.status_code}")
        except Exception as e:
            print(f"❌ System endpoints error: {str(e)}")
    
    def test_bulk_operations(self):
        """Test bulk operations"""
        print("\n🔄 Testing Bulk Operations...")
        
        # Create multiple test users for bulk operations
        user_ids = []
        for i in range(3):
            test_user = {
                "name": f"Bulk Test User {i+1}",
                "email": f"bulktest{i+1}{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
                "password": "bulkpass123",
                "role": "student",
                "is_active": True
            }
            
            try:
                response = requests.post(f"{self.base_url}/admin/users", 
                                       json=test_user, headers=self.headers)
                if response.status_code == 201:
                    user_id = response.json().get('user_id')
                    user_ids.append(user_id)
            except Exception as e:
                print(f"❌ Error creating bulk test user: {str(e)}")
        
        if user_ids:
            # Test bulk deactivate
            bulk_action = {
                "action": "deactivate",
                "ids": user_ids
            }
            
            try:
                response = requests.post(f"{self.base_url}/admin/users/bulk-action", 
                                       json=bulk_action, headers=self.headers)
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Bulk deactivate successful")
                    print(f"   Affected users: {result.get('affected_count')}")
                else:
                    print(f"❌ Bulk deactivate failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Bulk operation error: {str(e)}")
    
    def run_all_tests(self):
        """Run all admin API tests"""
        print("🚀 Starting Admin API Tests...")
        print("=" * 50)
        
        if not self.login_admin():
            print("❌ Cannot proceed without admin authentication")
            return
        
        self.test_dashboard()
        self.test_users_crud()
        self.test_courses_crud()
        self.test_analytics()
        self.test_system_health()
        self.test_bulk_operations()
        
        print("\n" + "=" * 50)
        print("🏁 Admin API Tests Completed!")

if __name__ == "__main__":
    tester = AdminAPITester()
    tester.run_all_tests()
