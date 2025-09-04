# 🎓 Bhoomi Tech E-Learning - Complete Project Setup Guide

## 🚀 How to Run the Full Project

This guide will help you run the complete Bhoomi Tech E-Learning platform with both backend API and admin panel.

## 📋 Prerequisites

### Required Software
- ✅ **Python 3.8+** (Already installed)
- ✅ **MongoDB** (Community Edition)
- ✅ **Modern Web Browser** (Chrome, Firefox, Edge)
- ✅ **Code Editor** (VS Code recommended)

### Check Your Installation
```bash
python --version          # Should show Python 3.8+
mongod --version         # Should show MongoDB version
```

## 🛠️ Project Structure

```
bhoomi_tech_e-learning/
├── src/                     # Backend API Source Code
│   ├── main.py             # FastAPI main application
│   ├── auth.py             # Authentication & JWT
│   ├── config.py           # Configuration settings
│   ├── middleware.py       # CORS and middleware
│   ├── database/           # Database layer
│   │   ├── repositories/   # Data access layer
│   │   └── schemas/        # Pydantic models
│   └── routes/             # API endpoints
│       ├── admin.py        # Admin management
│       ├── user.py         # User management
│       ├── course.py       # Course management
│       └── ...
├── admin-frontend/         # Admin Panel Frontend
│   ├── index.html          # Main admin interface
│   ├── styles.css          # Styling
│   ├── app.js              # JavaScript functionality
│   └── README.md           # Frontend documentation
└── requirements.txt        # Python dependencies
```

## 🔧 Step-by-Step Setup

### Step 1: Install Dependencies
```bash
# Navigate to project directory
cd "c:\Users\HP\Desktop\bhoomilearning1\bhoomilearning\bhoomi_tech_e-learning"

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Configure Database
```bash
# Start MongoDB service (Windows)
net start MongoDB

# Or manually start MongoDB
mongod --dbpath "C:\Program Files\MongoDB\Server\7.0\data"
```

### Step 3: Start Backend Server
```bash
# Navigate to src directory
cd src

# Start FastAPI server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Step 4: Verify Backend is Running
Open these URLs in your browser:
- **API Root**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health (if available)

### Step 5: Launch Admin Panel
```bash
# Navigate to admin-frontend directory
cd admin-frontend

# Open the admin panel in browser
# Double-click index.html or open in browser
```

## 🎯 Quick Start Commands

### Option 1: Manual Setup
```bash
# Terminal 1: Start MongoDB
mongod

# Terminal 2: Start Backend
cd "c:\Users\HP\Desktop\bhoomilearning1\bhoomilearning\bhoomi_tech_e-learning\src"
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Browser: Open Admin Panel
# Navigate to: admin-frontend/index.html
```

### Option 2: Using Batch Script (Create this)
Create `start_project.bat`:
```batch
@echo off
echo Starting Bhoomi Tech E-Learning Platform...

echo.
echo Starting MongoDB...
net start MongoDB

echo.
echo Starting Backend Server...
cd /d "c:\Users\HP\Desktop\bhoomilearning1\bhoomilearning\bhoomi_tech_e-learning\src"
start cmd /k "python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo.
echo Opening Admin Panel...
cd /d "c:\Users\HP\Desktop\bhoomilearning1\bhoomilearning\bhoomi_tech_e-learning\admin-frontend"
start index.html

echo.
echo Project Started Successfully!
echo Backend API: http://localhost:8000
echo Admin Panel: Opened in browser
echo API Docs: http://localhost:8000/docs
pause
```

## 🔐 Default Login Credentials

### Admin Panel Access
- **Email**: `admin@bhoomi.com`
- **Password**: `admin123`

*Note: If admin user doesn't exist, register it first through the admin panel*

## 📊 Available Endpoints

### Authentication Endpoints
- `POST /users/register` - Register new user
- `POST /users/login` - User login
- `GET /users/me` - Get current user profile

### Admin Endpoints
- `GET /admin/dashboard` - Dashboard statistics
- `GET /admin/users` - List all users
- `POST /admin/users` - Create new user
- `DELETE /admin/users/{user_id}` - Delete user
- `GET /admin/courses` - List all courses
- `POST /admin/courses` - Create new course
- `DELETE /admin/courses/{course_id}` - Delete course

### Course Endpoints
- `GET /courses` - Public course listing
- `GET /courses/{course_id}` - Course details
- `POST /courses/{course_id}/enroll` - Enroll in course

### User Management
- `GET /users` - List users (admin only)
- `PUT /users/{user_id}` - Update user profile
- `DELETE /users/{user_id}` - Delete user account

## 🌐 Accessing the Platform

### 1. Backend API
- **URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Status**: Should show "Welcome to Bhoomi Tech E-Learning API"

### 2. Admin Panel
- **Location**: `admin-frontend/index.html`
- **Features**: User management, course management, analytics
- **Authentication**: JWT-based admin access

### 3. API Testing
- **Postman Collection**: Available in project root
- **Interactive Docs**: http://localhost:8000/docs
- **Test Scripts**: `test_api.py`, `comprehensive_api_test.py`

## 🔍 Verification Checklist

### ✅ Backend Server
- [ ] Server starts without errors
- [ ] http://localhost:8000 shows welcome message
- [ ] http://localhost:8000/docs shows API documentation
- [ ] MongoDB connection established

### ✅ Admin Panel
- [ ] Admin panel loads in browser
- [ ] Login form appears
- [ ] Can register/login admin user
- [ ] Dashboard shows statistics
- [ ] User management works
- [ ] Course management works

### ✅ Database
- [ ] MongoDB service running
- [ ] Database connection successful
- [ ] Collections created automatically
- [ ] Sample data can be inserted

## 🐛 Troubleshooting

### Common Issues

#### 1. **"Module not found" Error**
```bash
# Solution: Install missing packages
pip install fastapi uvicorn pymongo bcrypt python-jose python-multipart
```

#### 2. **"MongoDB connection failed"**
```bash
# Solution: Start MongoDB service
net start MongoDB
# Or check MongoDB installation
```

#### 3. **"Port 8000 already in use"**
```bash
# Solution: Use different port
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8080
# Update admin panel API_BASE_URL to http://localhost:8080
```

#### 4. **"Admin login failed"**
- First register admin user through the interface
- Check if backend server is running
- Verify MongoDB is connected

#### 5. **"CORS Error"**
- Backend includes CORS middleware
- Should allow requests from file:// origin
- Check browser console for detailed errors

## 📱 Platform Features

### For Administrators
- **Dashboard**: Real-time statistics and metrics
- **User Management**: Create, edit, delete users
- **Course Management**: Full course lifecycle management
- **Analytics**: Enrollment and revenue tracking
- **System Monitoring**: Platform health and activity

### For Instructors
- **Course Creation**: Build and publish courses
- **Student Management**: Track student progress
- **Content Upload**: Add videos, materials, quizzes
- **Analytics**: Course performance metrics

### For Students
- **Course Browsing**: Discover available courses
- **Enrollment**: Join courses and track progress
- **Learning**: Access course materials and quizzes
- **Progress Tracking**: Monitor learning journey

## 🔄 Development Workflow

### Making Changes
1. **Backend Changes**: Edit files in `src/` directory
2. **Frontend Changes**: Edit files in `admin-frontend/`
3. **Database Changes**: Update schemas in `database/schemas/`
4. **API Changes**: Modify routes in `routes/` directory

### Testing Changes
1. **Backend**: Use http://localhost:8000/docs for API testing
2. **Frontend**: Refresh browser to see changes
3. **Database**: Use MongoDB Compass or CLI to verify data

### Deployment Preparation
1. **Environment Variables**: Set production database URLs
2. **Security**: Change default passwords and JWT secrets
3. **Performance**: Configure production settings
4. **Monitoring**: Set up logging and error tracking

## 🎉 Success!

If you can:
- ✅ Access http://localhost:8000 and see the API welcome message
- ✅ Open the admin panel and login successfully
- ✅ Create users and courses through the admin interface
- ✅ See data reflected in the dashboard

**Your Bhoomi Tech E-Learning platform is fully operational!** 🚀

## 📞 Support

### Getting Help
1. **Check Logs**: Look at terminal output for errors
2. **Browser Console**: Press F12 to see JavaScript errors
3. **API Documentation**: Use http://localhost:8000/docs for API reference
4. **Database**: Use MongoDB Compass to inspect data

### Next Steps
1. **Customize**: Modify the admin panel styling and features
2. **Extend**: Add new API endpoints and functionality
3. **Deploy**: Set up production environment
4. **Scale**: Add more features and optimize performance

---

**🎯 Your complete e-learning platform is ready to use!**
