import requests
import json
import time
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.tokens = {}
        self.ids = {}
        self.test_results = []
        
    def log_test(self, test_name: str, status: bool, response_data: Any = None, error: str = None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": "✅ PASS" if status else "❌ FAIL",
            "response": response_data,
            "error": error
        }
        self.test_results.append(result)
        print(f"{result['status']} {test_name}")
        if error:
            print(f"   Error: {error}")
        elif response_data:
            print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
        print("-" * 60)
    
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None, expected_status: int = 200):
        """Generic endpoint tester"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            response_data = None
            
            try:
                response_data = response.json()
            except:
                response_data = {"status_code": response.status_code, "text": response.text[:100]}
            
            return success, response_data, None
            
        except Exception as e:
            return False, None, str(e)
    
    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting Comprehensive API Testing")
        print("=" * 70)
        
        # Phase 1: Basic Endpoints
        print("\n📍 Phase 1: Basic Endpoints")
        self.test_basic_endpoints()
        
        # Phase 2: Authentication
        print("\n📍 Phase 2: Authentication")
        self.test_authentication()
        
        # Phase 3: User Management
        print("\n📍 Phase 3: User Management")
        self.test_user_management()
        
        # Phase 4: Course Management
        print("\n📍 Phase 4: Course Management")
        self.test_course_management()
        
        # Phase 5: Lesson Management
        print("\n📍 Phase 5: Lesson Management")
        self.test_lesson_management()
        
        # Phase 6: Enrollment System
        print("\n📍 Phase 6: Enrollment System")
        self.test_enrollment_system()
        
        # Phase 7: Quiz System
        print("\n📍 Phase 7: Quiz System")
        self.test_quiz_system()
        
        # Phase 8: Review System
        print("\n📍 Phase 8: Review System")
        self.test_review_system()
        
        # Phase 9: Notification System
        print("\n📍 Phase 9: Notification System")
        self.test_notification_system()
        
        # Phase 10: Payment System
        print("\n📍 Phase 10: Payment System")
        self.test_payment_system()
        
        # Summary
        self.print_summary()
    
    def test_basic_endpoints(self):
        """Test basic endpoints"""
        # Test root endpoint
        success, data, error = self.test_endpoint("GET", "/")
        self.log_test("Root Endpoint", success, data, error)
        
        # Test home feed
        success, data, error = self.test_endpoint("GET", "/home-feed")
        self.log_test("Home Feed", success, data, error)
    
    def test_authentication(self):
        """Test authentication endpoints"""
        # Register student
        student_data = {
            "name": "Test Student",
            "email": "student@test.com",
            "password": "password123",
            "role": "student"
        }
        success, data, error = self.test_endpoint("POST", "/users/register", student_data)
        if success and data:
            self.ids["student_id"] = data.get("id")
        self.log_test("Register Student", success, data, error)
        
        # Register instructor
        instructor_data = {
            "name": "Test Instructor",
            "email": "instructor@test.com",
            "password": "password123",
            "role": "instructor"
        }
        success, data, error = self.test_endpoint("POST", "/users/register", instructor_data)
        if success and data:
            self.ids["instructor_id"] = data.get("id")
        self.log_test("Register Instructor", success, data, error)
        
        # Login student
        login_data = {
            "email": "student@test.com",
            "password": "password123"
        }
        success, data, error = self.test_endpoint("POST", "/users/login", login_data)
        if success and data:
            self.tokens["student_token"] = data.get("access_token")
        self.log_test("Login Student", success, data, error)
        
        # Login instructor
        login_data = {
            "email": "instructor@test.com",
            "password": "password123"
        }
        success, data, error = self.test_endpoint("POST", "/users/login", login_data)
        if success and data:
            self.tokens["instructor_token"] = data.get("access_token")
        self.log_test("Login Instructor", success, data, error)
    
    def test_user_management(self):
        """Test user management endpoints"""
        if not self.tokens.get("student_token"):
            self.log_test("Get Current User", False, None, "No student token available")
            return
        
        headers = {"Authorization": f"Bearer {self.tokens['student_token']}"}
        
        # Get current user
        success, data, error = self.test_endpoint("GET", "/users/me", headers=headers)
        self.log_test("Get Current User", success, data, error)
        
        # Get all users
        success, data, error = self.test_endpoint("GET", "/users/", headers=headers)
        self.log_test("Get All Users", success, data, error)
    
    def test_course_management(self):
        """Test course management endpoints"""
        # Get all courses (public)
        success, data, error = self.test_endpoint("GET", "/courses/")
        self.log_test("Get All Courses", success, data, error)
        
        if not self.tokens.get("instructor_token"):
            self.log_test("Create Course", False, None, "No instructor token available")
            return
        
        headers = {"Authorization": f"Bearer {self.tokens['instructor_token']}"}
        
        # Create course
        course_data = {
            "title": "Python Programming Fundamentals",
            "description": "Learn Python programming from scratch",
            "price": 99.99,
            "is_active": True
        }
        success, data, error = self.test_endpoint("POST", "/courses/", course_data, headers)
        if success and data:
            self.ids["course_id"] = data.get("id")
        self.log_test("Create Course", success, data, error)
        
        # Get course by ID
        if self.ids.get("course_id"):
            success, data, error = self.test_endpoint("GET", f"/courses/{self.ids['course_id']}")
            self.log_test("Get Course by ID", success, data, error)
    
    def test_lesson_management(self):
        """Test lesson management endpoints"""
        # Get all lessons
        success, data, error = self.test_endpoint("GET", "/lessons/")
        self.log_test("Get All Lessons", success, data, error)
        
        if not self.tokens.get("instructor_token") or not self.ids.get("course_id"):
            self.log_test("Create Lesson", False, None, "Missing instructor token or course ID")
            return
        
        headers = {"Authorization": f"Bearer {self.tokens['instructor_token']}"}
        
        # Create lesson
        lesson_data = {
            "course_id": self.ids["course_id"],
            "title": "Introduction to Python",
            "content": "Welcome to Python programming!",
            "video_url": "",
            "document_url": ""
        }
        success, data, error = self.test_endpoint("POST", "/lessons/", lesson_data, headers)
        if success and data:
            self.ids["lesson_id"] = data.get("id")
        self.log_test("Create Lesson", success, data, error)
        
        # Get lesson by ID
        if self.ids.get("lesson_id"):
            success, data, error = self.test_endpoint("GET", f"/lessons/{self.ids['lesson_id']}")
            self.log_test("Get Lesson by ID", success, data, error)
    
    def test_enrollment_system(self):
        """Test enrollment system"""
        if not self.tokens.get("student_token") or not self.ids.get("course_id"):
            self.log_test("Enroll in Course", False, None, "Missing student token or course ID")
            return
        
        headers = {"Authorization": f"Bearer {self.tokens['student_token']}"}
        
        # Enroll in course
        enrollment_data = {
            "course_id": self.ids["course_id"],
            "progress": 0.0
        }
        success, data, error = self.test_endpoint("POST", "/enrollments/", enrollment_data, headers)
        if success and data:
            self.ids["enrollment_id"] = data.get("id")
        self.log_test("Enroll in Course", success, data, error)
        
        # Get my courses
        success, data, error = self.test_endpoint("GET", "/enrollments/my-courses", headers=headers)
        self.log_test("Get My Courses", success, data, error)
        
        # Update progress
        if self.ids.get("enrollment_id"):
            progress_data = {"progress": 25.5}
            success, data, error = self.test_endpoint("PUT", f"/enrollments/{self.ids['enrollment_id']}/progress", progress_data, headers)
            self.log_test("Update Progress", success, data, error)
    
    def test_quiz_system(self):
        """Test quiz system"""
        # Get all quizzes
        success, data, error = self.test_endpoint("GET", "/quizzes/")
        self.log_test("Get All Quizzes", success, data, error)
        
        if not self.tokens.get("instructor_token") or not self.ids.get("course_id"):
            self.log_test("Create Quiz", False, None, "Missing instructor token or course ID")
            return
        
        headers = {"Authorization": f"Bearer {self.tokens['instructor_token']}"}
        
        # Create quiz
        quiz_data = {
            "course_id": self.ids["course_id"],
            "lesson_id": self.ids.get("lesson_id"),
            "questions": [
                {
                    "question": "What is Python?",
                    "options": ["A programming language", "A snake", "A tool", "A framework"],
                    "answer": "A programming language"
                }
            ]
        }
        success, data, error = self.test_endpoint("POST", "/quizzes/", quiz_data, headers)
        if success and data:
            self.ids["quiz_id"] = data.get("id")
        self.log_test("Create Quiz", success, data, error)
        
        # Get quiz by ID
        if self.ids.get("quiz_id"):
            success, data, error = self.test_endpoint("GET", f"/quizzes/{self.ids['quiz_id']}")
            self.log_test("Get Quiz by ID", success, data, error)
        
        # Submit quiz (as student)
        if self.tokens.get("student_token") and self.ids.get("quiz_id"):
            student_headers = {"Authorization": f"Bearer {self.tokens['student_token']}"}
            submission_data = {
                "quiz_id": self.ids["quiz_id"],
                "answers": ["A programming language"]
            }
            success, data, error = self.test_endpoint("POST", f"/quizzes/{self.ids['quiz_id']}/submit", submission_data, student_headers)
            self.log_test("Submit Quiz", success, data, error)
        
        # Get quiz results (as instructor)
        if self.ids.get("quiz_id"):
            success, data, error = self.test_endpoint("GET", f"/quizzes/{self.ids['quiz_id']}/results", headers=headers)
            self.log_test("Get Quiz Results", success, data, error)
    
    def test_review_system(self):
        """Test review system"""
        if not self.ids.get("student_id") or not self.ids.get("course_id"):
            self.log_test("Add Review", False, None, "Missing student ID or course ID")
            return
        
        # Add review
        review_data = {
            "user_id": self.ids["student_id"],
            "course_id": self.ids["course_id"],
            "rating": 5,
            "comment": "Excellent course!"
        }
        success, data, error = self.test_endpoint("POST", "/reviews/", review_data)
        self.log_test("Add Review", success, data, error)
        
        # Get course reviews
        success, data, error = self.test_endpoint("GET", f"/reviews/course/{self.ids['course_id']}")
        self.log_test("Get Course Reviews", success, data, error)
    
    def test_notification_system(self):
        """Test notification system"""
        if not self.ids.get("student_id"):
            self.log_test("Create Notification", False, None, "Missing student ID")
            return
        
        # Create notification
        notification_data = {
            "user_id": self.ids["student_id"],
            "message": "New course available!",
            "is_read": False
        }
        success, data, error = self.test_endpoint("POST", "/notifications/", notification_data)
        if success and data:
            self.ids["notification_id"] = data.get("id")
        self.log_test("Create Notification", success, data, error)
        
        # Get user notifications
        success, data, error = self.test_endpoint("GET", f"/notifications/user/{self.ids['student_id']}")
        self.log_test("Get User Notifications", success, data, error)
        
        # Mark notification as read
        if self.ids.get("notification_id"):
            success, data, error = self.test_endpoint("PUT", f"/notifications/{self.ids['notification_id']}/read")
            self.log_test("Mark Notification as Read", success, data, error)
    
    def test_payment_system(self):
        """Test payment system"""
        # Get all payments
        success, data, error = self.test_endpoint("GET", "/payments/")
        self.log_test("Get All Payments", success, data, error)
        
        if not self.ids.get("student_id") or not self.ids.get("course_id"):
            self.log_test("Create Payment", False, None, "Missing student ID or course ID")
            return
        
        # Create payment
        payment_data = {
            "user_id": self.ids["student_id"],
            "course_id": self.ids["course_id"],
            "amount": 99.99,
            "status": "completed"
        }
        success, data, error = self.test_endpoint("POST", "/payments/", payment_data)
        self.log_test("Create Payment", success, data, error)
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if "✅" in r["status"]])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if "❌" in result["status"]:
                    print(f"   - {result['test']}: {result.get('error', 'Unknown error')}")
        
        print("\n🎉 API Testing Complete!")

if __name__ == "__main__":
    # Initialize tester
    tester = APITester("http://localhost:8000")
    
    # Run all tests
    tester.run_all_tests()
