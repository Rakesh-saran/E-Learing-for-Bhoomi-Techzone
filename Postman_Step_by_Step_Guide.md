# 🚀 Postman Step-by-Step API Testing Guide

## 🎯 Quick Start Instructions

### Step 1: Import Files
1. Open Postman
2. Click "Import" button
3. Import `Bhoomi_ELearning_API_Collection.postman_collection.json`
4. Import `Bhoomi_ELearning_Environment.postman_environment.json`
5. Select "Bhoomi ELearning Environment" from environment dropdown

### Step 2: Verify Server
✅ Confirm server is running at: http://localhost:8000

## 📋 Testing Sequence (Follow Exactly)

### **🏠 PHASE 1: Basic Endpoints**

#### Test 1: Root Endpoint
- **Request**: GET `/`
- **Expected Status**: 200
- **Expected Response**:
```json
{
  "message": "Welcome to Bhoomi Tech E-Learning Platform!"
}
```
- **✅ Check**: Message appears correctly

#### Test 2: Home Feed
- **Request**: GET `/home-feed`
- **Expected Status**: 200
- **Expected Response**: Array of courses (may be empty initially)
- **✅ Check**: Returns array format

---

### **👤 PHASE 2: User Registration & Authentication**

#### Test 3: Register Student
- **Request**: POST `/users/register`
- **Body** (JSON):
```json
{
  "name": "John Student",
  "email": "john@student.com", 
  "password": "password123",
  "role": "student"
}
```
- **Expected Status**: 201
- **✅ Check**: User created with ID returned
- **📝 Copy**: Save `user_id` from response

#### Test 4: Register Instructor
- **Request**: POST `/users/register`
- **Body** (JSON):
```json
{
  "name": "Jane Instructor",
  "email": "jane@instructor.com",
  "password": "password123", 
  "role": "instructor"
}
```
- **Expected Status**: 201
- **✅ Check**: User created with ID returned
- **📝 Copy**: Save `instructor_id` from response

#### Test 5: Login Student
- **Request**: POST `/users/login`
- **Body** (JSON):
```json
{
  "email": "john@student.com",
  "password": "password123"
}
```
- **Expected Status**: 200
- **✅ Check**: `access_token` returned
- **📝 Copy**: Token should auto-save to environment as `studentToken`

#### Test 6: Login Instructor  
- **Request**: POST `/users/login`
- **Body** (JSON):
```json
{
  "email": "jane@instructor.com", 
  "password": "password123"
}
```
- **Expected Status**: 200
- **✅ Check**: `access_token` returned
- **📝 Copy**: Token should auto-save to environment as `instructorToken`

---

### **👥 PHASE 3: User Management**

#### Test 7: Get Current User (Student)
- **Request**: GET `/users/me`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Expected Status**: 200
- **✅ Check**: Returns student profile data

#### Test 8: Get All Users
- **Request**: GET `/users/`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Expected Status**: 200
- **✅ Check**: Returns array with 2 users (student + instructor)

#### Test 8.1: Update User Profile 🆕
- **Request**: PUT `/users/{{studentId}}`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Body** (JSON):
```json
{
  "name": "John Updated Student",
  "email": "john.updated@student.com"
}
```
- **Expected Status**: 200
- **✅ Check**: User profile updated successfully

#### Test 8.2: Upload User Avatar 🆕
- **Request**: POST `/users/{{studentId}}/avatar`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Body**: Form-data with "avatar" file field (select an image file)
- **Expected Status**: 200
- **✅ Check**: Avatar uploaded and URL returned

#### Test 8.3: Delete User Avatar 🆕
- **Request**: DELETE `/users/{{studentId}}/avatar`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Expected Status**: 200
- **✅ Check**: Avatar deleted successfully

---

### **📚 PHASE 4: Course Management**

#### Test 9: Get All Courses (Public)
- **Request**: GET `/courses/`
- **Expected Status**: 200
- **✅ Check**: Returns empty array initially

#### Test 10: Create Course (Instructor)
- **Request**: POST `/courses/`
- **Headers**: Authorization: Bearer {{instructorToken}}
- **Body** (JSON):
```json
{
  "title": "Python Programming Fundamentals",
  "description": "Learn Python programming from scratch with hands-on examples and projects",
  "price": 99.99,
  "is_active": true
}
```
- **Expected Status**: 201
- **✅ Check**: Course created with ID
- **📝 Copy**: Save `course_id` from response (should auto-save as `courseId`)

#### Test 11: Get Course by ID
- **Request**: GET `/courses/{{courseId}}`
- **Expected Status**: 200
- **✅ Check**: Returns the created course details

#### Test 11.1: Update Course 🆕
- **Request**: PUT `/courses/{{courseId}}`
- **Headers**: Authorization: Bearer {{instructorToken}}
- **Body** (JSON):
```json
{
  "title": "Advanced Python Programming Fundamentals",
  "description": "Learn Python programming from basics to advanced concepts with real-world projects",
  "price": 149.99,
  "is_active": true
}
```
- **Expected Status**: 200
- **✅ Check**: Course updated successfully

#### Test 11.2: Get Instructor Courses 🆕
- **Request**: GET `/courses/instructor/{{instructorId}}`
- **Expected Status**: 200
- **✅ Check**: Returns array with instructor's courses

---

### **📖 PHASE 5: Lesson Management**

#### Test 12: Get All Lessons
- **Request**: GET `/lessons/`
- **Expected Status**: 200
- **✅ Check**: Returns empty array initially

#### Test 13: Create Lesson
- **Request**: POST `/lessons/`
- **Headers**: Authorization: Bearer {{instructorToken}}
- **Body** (JSON):
```json
{
  "course_id": "{{courseId}}",
  "title": "Introduction to Python",
  "content": "Welcome to Python programming! In this lesson, we'll cover the basics of Python syntax and structure.",
  "video_url": "",
  "document_url": ""
}
```
- **Expected Status**: 201
- **✅ Check**: Lesson created with ID
- **📝 Copy**: Save `lesson_id` (should auto-save as `lessonId`)

#### Test 14: Get Lesson by ID
- **Request**: GET `/lessons/{{lessonId}}`
- **Expected Status**: 200
- **✅ Check**: Returns the created lesson

#### Test 15: Get Course Lessons
- **Request**: GET `/lessons/course/{{courseId}}`
- **Expected Status**: 200
- **✅ Check**: Returns array with 1 lesson

---

### **🎓 PHASE 6: Enrollment System**

#### Test 16: Enroll in Course (Student)
- **Request**: POST `/enrollments/`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Body** (JSON):
```json
{
  "course_id": "{{courseId}}",
  "progress": 0.0
}
```
- **Expected Status**: 201
- **✅ Check**: Enrollment created
- **📝 Copy**: Save `enrollment_id` (should auto-save as `enrollmentId`)

#### Test 17: Get My Courses
- **Request**: GET `/enrollments/my-courses`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Expected Status**: 200
- **✅ Check**: Returns array with 1 enrolled course

#### Test 18: Update Progress
- **Request**: PUT `/enrollments/{{enrollmentId}}/progress`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Body** (JSON):
```json
{
  "progress": 25.5
}
```
- **Expected Status**: 200
- **✅ Check**: Progress updated successfully

---

### **❓ PHASE 7: Quiz System**

#### Test 19: Get All Quizzes
- **Request**: GET `/quizzes/`
- **Expected Status**: 200
- **✅ Check**: Returns empty array initially

#### Test 20: Create Quiz (Instructor)
- **Request**: POST `/quizzes/`
- **Headers**: Authorization: Bearer {{instructorToken}}
- **Body** (JSON):
```json
{
  "course_id": "{{courseId}}",
  "lesson_id": "{{lessonId}}",
  "questions": [
    {
      "question": "What is Python?",
      "options": ["A programming language", "A snake", "A tool", "A framework"],
      "answer": "A programming language"
    },
    {
      "question": "Which of the following is a Python data type?",
      "options": ["String", "Integer", "List", "All of the above"],
      "answer": "All of the above"
    }
  ]
}
```
- **Expected Status**: 201
- **✅ Check**: Quiz created with ID
- **📝 Copy**: Save `quiz_id` (should auto-save as `quizId`)

#### Test 21: Get Quiz by ID
- **Request**: GET `/quizzes/{{quizId}}`
- **Expected Status**: 200
- **✅ Check**: Returns quiz with questions

#### Test 22: Submit Quiz (Student)
- **Request**: POST `/quizzes/{{quizId}}/submit`
- **Headers**: Authorization: Bearer {{studentToken}}
- **Body** (JSON):
```json
{
  "quiz_id": "{{quizId}}",
  "answers": ["A programming language", "All of the above"]
}
```
- **Expected Status**: 201
- **✅ Check**: Quiz submission recorded

#### Test 23: Get Quiz Results (Instructor)
- **Request**: GET `/quizzes/{{quizId}}/results`
- **Headers**: Authorization: Bearer {{instructorToken}}
- **Expected Status**: 200
- **✅ Check**: Returns quiz results/submissions

---

### **⭐ PHASE 8: Review System**

#### Test 24: Add Review
- **Request**: POST `/reviews/`
- **Body** (JSON):
```json
{
  "user_id": "{{studentId}}",
  "course_id": "{{courseId}}",
  "rating": 5,
  "comment": "Excellent course! Very well structured and easy to follow. Highly recommended for beginners."
}
```
- **Expected Status**: 201
- **✅ Check**: Review created
- **📝 Copy**: Save `review_id` (should auto-save as `reviewId`)

#### Test 25: Get Course Reviews
- **Request**: GET `/reviews/course/{{courseId}}`
- **Expected Status**: 200
- **✅ Check**: Returns array with 1 review

---

### **🔔 PHASE 9: Notification System**

#### Test 26: Create Notification
- **Request**: POST `/notifications/`
- **Body** (JSON):
```json
{
  "user_id": "{{studentId}}",
  "message": "New course available in your area of interest! Check out 'Python Programming Fundamentals'.",
  "is_read": false
}
```
- **Expected Status**: 201
- **✅ Check**: Notification created
- **📝 Copy**: Save `notification_id` (should auto-save as `notificationId`)

#### Test 27: Get User Notifications
- **Request**: GET `/notifications/user/{{studentId}}`
- **Expected Status**: 200
- **✅ Check**: Returns array with 1 notification

#### Test 28: Mark Notification as Read
- **Request**: PUT `/notifications/{{notificationId}}/read`
- **Expected Status**: 200
- **✅ Check**: Notification marked as read

---

### **💳 PHASE 10: Payment System**

#### Test 29: Get All Payments
- **Request**: GET `/payments/`
- **Expected Status**: 200
- **✅ Check**: Returns empty array initially

#### Test 30: Create Payment
- **Request**: POST `/payments/`
- **Body** (JSON):
```json
{
  "user_id": "{{studentId}}",
  "course_id": "{{courseId}}",
  "amount": 99.99,
  "status": "completed"
}
```
- **Expected Status**: 201
- **✅ Check**: Payment created
- **📝 Copy**: Save `payment_id` (should auto-save as `paymentId`)

#### Test 31: Get Payment by ID
- **Request**: GET `/payments/{{paymentId}}`
- **Expected Status**: 200
- **✅ Check**: Returns payment details

---

## 🎯 Success Criteria

### ✅ What Should Work:
- All GET requests return 200 status
- User registration returns 201 status
- Login returns access tokens
- Course/lesson creation works with instructor token
- Enrollment works with student token
- Quiz creation and submission work
- Reviews and notifications can be created
- Payments can be processed

### ⚠️ Expected Behaviors:
- Some endpoints may return empty arrays initially (normal)
- Role-based access control enforced (instructor vs student)
- Authentication required for protected endpoints
- IDs auto-populate in environment variables

### ❌ Common Issues:
- 401 Unauthorized: Check if token is properly set
- 403 Forbidden: Check user role permissions
- 404 Not Found: Check if IDs are properly saved
- 422 Unprocessable Entity: Check request body format

## 🏁 Completion Checklist
- [ ] All 31 core tests completed
- [ ] All tokens properly generated and saved
- [ ] All IDs captured in environment variables
- [ ] Full user journey tested (register → login → enroll → quiz)
- [ ] Role-based permissions verified
- [ ] CRUD operations working for all entities

**🎉 SUCCESS**: If all tests pass, your API is fully functional!
