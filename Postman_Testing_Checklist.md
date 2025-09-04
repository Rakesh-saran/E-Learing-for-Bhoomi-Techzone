# 🧪 Postman API Testing Checklist - Bhoomi E-Learning Platform

## 📋 Pre-Testing Setup
- [x] Server running at http://localhost:8000
- [ ] Postman collection imported
- [ ] Environment file imported and selected
- [ ] Environment variables cleared (for fresh start)

## 🔄 Testing Progress Tracker

### **Phase 1: Basic Endpoints** 🏠
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 1 | `/` | GET | ⏳ | - | Welcome message |
| 2 | `/home-feed` | GET | ⏳ | - | Course feed |

### **Phase 2: User Authentication** 👤
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 3 | `/users/register` | POST | ⏳ | - | Student registration |
| 4 | `/users/register` | POST | ⏳ | - | Instructor registration |
| 5 | `/users/login` | POST | ⏳ | - | Student login + token |
| 6 | `/users/login` | POST | ⏳ | - | Instructor login + token |

### **Phase 3: User Management** 👥
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 7 | `/users/me` | GET | ⏳ | - | Current user profile |
| 8 | `/users/` | GET | ⏳ | - | All users list |
| 9 | `/users/{user_id}` | GET | ⏳ | - | Get user by ID |
| 10 | `/users/{user_id}` | PUT | ⏳ | - | Update user |

### **Phase 4: Course Management** 📚
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 11 | `/courses/` | GET | ⏳ | - | All courses (public) |
| 12 | `/courses/` | POST | ⏳ | - | Create course (instructor) |
| 13 | `/courses/{course_id}` | GET | ⏳ | - | Get course by ID |
| 14 | `/courses/{course_id}` | PUT | ⏳ | - | Update course |
| 15 | `/courses/instructor/{instructor_id}` | GET | ⏳ | - | Instructor courses |

### **Phase 5: Lesson Management** 📖
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 16 | `/lessons/` | GET | ⏳ | - | All lessons |
| 17 | `/lessons/` | POST | ⏳ | - | Create lesson |
| 18 | `/lessons/{lesson_id}` | GET | ⏳ | - | Get lesson by ID |
| 19 | `/lessons/{lesson_id}` | PUT | ⏳ | - | Update lesson |
| 20 | `/lessons/course/{course_id}` | GET | ⏳ | - | Course lessons |

### **Phase 6: Enrollment System** 🎓
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 21 | `/enrollments/` | POST | ⏳ | - | Enroll in course |
| 22 | `/enrollments/my-courses` | GET | ⏳ | - | Student's courses |
| 23 | `/enrollments/{enrollment_id}/progress` | PUT | ⏳ | - | Update progress |
| 24 | `/enrollments/course/{course_id}/students` | GET | ⏳ | - | Course students |

### **Phase 7: Quiz System** ❓
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 25 | `/quizzes/` | GET | ⏳ | - | All quizzes |
| 26 | `/quizzes/` | POST | ⏳ | - | Create quiz |
| 27 | `/quizzes/{quiz_id}` | GET | ⏳ | - | Get quiz by ID |
| 28 | `/quizzes/{quiz_id}` | PUT | ⏳ | - | Update quiz |
| 29 | `/quizzes/{quiz_id}/submit` | POST | ⏳ | - | Submit quiz |
| 30 | `/quizzes/{quiz_id}/results` | GET | ⏳ | - | Quiz results |
| 31 | `/quizzes/course/{course_id}` | GET | ⏳ | - | Course quizzes |

### **Phase 8: Review System** ⭐
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 32 | `/reviews/` | POST | ⏳ | - | Add review |
| 33 | `/reviews/course/{course_id}` | GET | ⏳ | - | Course reviews |
| 34 | `/reviews/{review_id}` | PUT | ⏳ | - | Update review |
| 35 | `/reviews/{review_id}` | DELETE | ⏳ | - | Delete review |

### **Phase 9: Notification System** 🔔
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 36 | `/notifications/` | POST | ⏳ | - | Create notification |
| 37 | `/notifications/user/{user_id}` | GET | ⏳ | - | User notifications |
| 38 | `/notifications/{notification_id}/read` | PUT | ⏳ | - | Mark as read |
| 39 | `/notifications/{notification_id}` | DELETE | ⏳ | - | Delete notification |

### **Phase 10: Payment System** 💳
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 40 | `/payments/` | GET | ⏳ | - | All payments |
| 41 | `/payments/` | POST | ⏳ | - | Create payment |
| 42 | `/payments/{payment_id}` | GET | ⏳ | - | Get payment by ID |
| 43 | `/payments/{payment_id}` | PUT | ⏳ | - | Update payment |
| 44 | `/payments/user/{user_id}` | GET | ⏳ | - | User payments |

### **Phase 11: File Upload** 📁
| # | Endpoint | Method | Status | Response | Notes |
|---|----------|--------|--------|----------|--------|
| 45 | `/upload/video/` | POST | ⏳ | - | Upload video |
| 46 | `/upload/photo/` | POST | ⏳ | - | Upload photo |

## 📊 Testing Summary
- **Total Endpoints**: 46
- **Completed**: 0
- **Passed**: 0
- **Failed**: 0
- **Success Rate**: 0%

## 🔑 Status Legend
- ⏳ = Pending
- ✅ = Passed
- ❌ = Failed
- ⚠️ = Warning/Issue

## 📝 Notes Section
- Record any issues, errors, or observations here
- Note any missing environment variables
- Document any authentication problems

---
*Update this checklist as you test each endpoint in Postman*
