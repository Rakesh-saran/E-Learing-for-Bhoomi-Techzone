# 🚀 Bhoomi E-Learning API - Manual Testing Guide

## Server Status: ✅ RUNNING
- **URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## 📋 API Endpoints Testing Checklist

### 1. Basic Endpoints
- [ ] **GET** `/` - Root endpoint ✅ ACCESSIBLE
- [ ] **GET** `/home-feed` - Home feed with courses ✅ ACCESSIBLE

### 2. User Authentication & Management
- [ ] **POST** `/users/register` - Register new user
- [ ] **POST** `/users/login` - Login user
- [ ] **GET** `/users/me` - Get current user profile
- [ ] **GET** `/users/` - Get all users
- [ ] **GET** `/users/{user_id}` - Get user by ID
- [ ] **PUT** `/users/{user_id}` - Update user profile 🆕
- [ ] **DELETE** `/users/{user_id}` - Delete user
- [ ] **POST** `/users/{user_id}/avatar` - Upload user avatar 🆕
- [ ] **DELETE** `/users/{user_id}/avatar` - Delete user avatar 🆕

### 3. Course Management
- [ ] **GET** `/courses/` - Get all courses
- [ ] **POST** `/courses/` - Create course (instructor only)
- [ ] **GET** `/courses/{course_id}` - Get course by ID
- [ ] **PUT** `/courses/{course_id}` - Update course (instructor only) 🆕
- [ ] **DELETE** `/courses/{course_id}` - Delete course
- [ ] **GET** `/courses/instructor/{instructor_id}` - Get instructor courses

### 4. Lesson Management
- [ ] **GET** `/lessons/` - Get all lessons
- [ ] **POST** `/lessons/` - Create lesson
- [ ] **GET** `/lessons/{lesson_id}` - Get lesson by ID
- [ ] **PUT** `/lessons/{lesson_id}` - Update lesson
- [ ] **DELETE** `/lessons/{lesson_id}` - Delete lesson
- [ ] **GET** `/lessons/course/{course_id}` - Get course lessons

### 5. Enrollment System
- [ ] **POST** `/enrollments/` - Enroll in course
- [ ] **GET** `/enrollments/my-courses` - Get user's enrolled courses
- [ ] **PUT** `/enrollments/{enrollment_id}/progress` - Update progress
- [ ] **GET** `/enrollments/course/{course_id}/students` - Get course students

### 6. Quiz System
- [ ] **GET** `/quizzes/` - Get all quizzes
- [ ] **POST** `/quizzes/` - Create quiz
- [ ] **GET** `/quizzes/{quiz_id}` - Get quiz by ID
- [ ] **PUT** `/quizzes/{quiz_id}` - Update quiz
- [ ] **DELETE** `/quizzes/{quiz_id}` - Delete quiz
- [ ] **POST** `/quizzes/{quiz_id}/submit` - Submit quiz answers
- [ ] **GET** `/quizzes/{quiz_id}/results` - Get quiz results
- [ ] **GET** `/quizzes/course/{course_id}` - Get course quizzes

### 7. Review System
- [ ] **POST** `/reviews/` - Add review
- [ ] **GET** `/reviews/course/{course_id}` - Get course reviews
- [ ] **PUT** `/reviews/{review_id}` - Update review
- [ ] **DELETE** `/reviews/{review_id}` - Delete review

### 8. Notification System
- [ ] **POST** `/notifications/` - Create notification
- [ ] **GET** `/notifications/user/{user_id}` - Get user notifications
- [ ] **PUT** `/notifications/{notification_id}/read` - Mark as read
- [ ] **DELETE** `/notifications/{notification_id}` - Delete notification

### 9. Payment System
- [ ] **GET** `/payments/` - Get all payments
- [ ] **POST** `/payments/` - Create payment
- [ ] **GET** `/payments/{payment_id}` - Get payment by ID
- [ ] **PUT** `/payments/{payment_id}` - Update payment
- [ ] **GET** `/payments/user/{user_id}` - Get user payments

### 10. File Upload
- [ ] **POST** `/upload/video/` - Upload video file
- [ ] **POST** `/upload/photo/` - Upload photo file

## 🧪 Sample Test Data

### User Registration (Student)
```json
{
  "name": "John Student",
  "email": "john@student.com",
  "password": "password123",
  "role": "student"
}
```

### User Registration (Instructor)
```json
{
  "name": "Jane Instructor",
  "email": "jane@instructor.com",
  "password": "password123",
  "role": "instructor"
}
```

### User Login
```json
{
  "email": "john@student.com",
  "password": "password123"
}
```

### Create Course (Instructor Token Required)
```json
{
  "title": "Python Programming Fundamentals",
  "description": "Learn Python from scratch with hands-on examples",
  "price": 99.99,
  "is_active": true
}
```

### Update Course (Instructor Token Required)
```json
{
  "title": "Advanced Python Programming",
  "description": "Master advanced Python concepts and frameworks",
  "price": 149.99,
  "is_active": true
}
```

### Update User Profile
```json
{
  "name": "John Updated Student",
  "email": "john.updated@student.com",
  "avatar": "/uploads/avatars/user123_avatar.jpg"
}
```

### Create Lesson (Instructor Token Required)
```json
{
  "course_id": "COURSE_ID_HERE",
  "title": "Introduction to Python",
  "content": "Python is a high-level programming language...",
  "video_url": "",
  "document_url": ""
}
```

### Enroll in Course (Student Token Required)
```json
{
  "course_id": "COURSE_ID_HERE",
  "progress": 0.0
}
```

### Create Quiz (Instructor Token Required)
```json
{
  "course_id": "COURSE_ID_HERE",
  "lesson_id": "LESSON_ID_HERE",
  "questions": [
    {
      "question": "What is Python?",
      "options": ["A programming language", "A snake", "A tool", "A framework"],
      "answer": "A programming language"
    }
  ]
}
```

### Submit Quiz (Student Token Required)
```json
{
  "quiz_id": "QUIZ_ID_HERE",
  "answers": ["A programming language"]
}
```

### Add Review
```json
{
  "user_id": "USER_ID_HERE",
  "course_id": "COURSE_ID_HERE",
  "rating": 5,
  "comment": "Excellent course! Highly recommended."
}
```

### Create Notification
```json
{
  "user_id": "USER_ID_HERE",
  "message": "New course available in your area of interest!",
  "is_read": false
}
```

### Create Payment
```json
{
  "user_id": "USER_ID_HERE",
  "course_id": "COURSE_ID_HERE",
  "amount": 99.99,
  "status": "completed"
}
```

## 🔐 Authentication Headers

After login, use the access token in requests:
```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

## 🛠️ Testing Tools Available

1. **Swagger UI**: http://localhost:8000/docs
2. **Postman Collection**: `Bhoomi_ELearning_API_Collection.postman_collection.json`
3. **Postman Environment**: `Bhoomi_ELearning_Environment.postman_environment.json`

## ✅ Quick Verification Steps

1. **Test Root Endpoint**
   - Visit: http://localhost:8000/
   - Should return: `{"message": "Welcome to Bhoomi Tech E-Learning Platform!"}`

2. **Test Home Feed**
   - Visit: http://localhost:8000/home-feed
   - Should return course list (may be empty initially)

3. **Test API Documentation**
   - Visit: http://localhost:8000/docs
   - Should show interactive API documentation

4. **Register Test Users**
   - Create one student and one instructor account
   - Use these for testing role-based functionality

5. **Test Authentication Flow**
   - Register → Login → Access protected endpoints

6. **Test CRUD Operations**
   - Create course (as instructor)
   - Create lessons in the course
   - Enroll student in course
   - Create and submit quiz

## 🚨 Common Issues & Solutions

- **CORS Issues**: Server allows all origins in development
- **Token Expiration**: Re-login if getting 401 errors
- **Role Permissions**: Ensure correct user role for protected endpoints
- **MongoDB Connection**: Check if MongoDB is running locally
- **Module Import Errors**: Ensure server is running from correct directory

## 📊 Server Status
✅ **Server Running**: http://localhost:8000
✅ **API Documentation**: http://localhost:8000/docs
✅ **All Dependencies**: Installed
✅ **Database Schema**: Configured
