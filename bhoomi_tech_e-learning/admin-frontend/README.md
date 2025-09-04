# 🎓 Bhoomi Tech E-Learning Admin Panel

A modern, responsive admin panel for managing the Bhoomi Tech E-Learning platform.

## 🎯 Features

### 📊 **Dashboard**
- Real-time statistics (Users, Courses, Enrollments, Revenue)
- Recent activity feed
- Quick action buttons
- System overview

### 👥 **User Management**
- View all users with filtering
- Create new users (Admin/Instructor/Student)
- Edit user details
- Delete users
- Role-based access control

### 📚 **Course Management**
- List all courses
- Create new courses
- Edit course details
- Delete courses
- Track enrollment statistics

### 🎓 **Enrollment Management**
- View all enrollments
- Track student progress
- Enrollment analytics
- Status management

### 📈 **Analytics & Reports**
- User growth charts
- Course popularity metrics
- Revenue trends
- Custom report generation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with FastAPI backend running
- Modern web browser
- Backend API running on `http://localhost:8000`

### Setup Instructions

1. **Start Backend Server**
   ```bash
   cd bhoomi_tech_e-learning/src
   python -m uvicorn main:app --reload
   ```

2. **Open Admin Panel**
   - Double-click `welcome.html` to see setup instructions
   - Click "Open Admin Panel" to access the interface
   - Or directly open `index.html` in your browser

3. **Login Credentials**
   ```
   Email: admin@bhoomi.com
   Password: admin123
   ```
   
   *If admin user doesn't exist, register first then login*

## 🖥️ Interface Overview

### Login Screen
- Secure JWT-based authentication
- Remember login session
- Admin role verification

### Main Dashboard
- **Sidebar Navigation**: Easy access to all sections
- **Header**: User info and logout
- **Stats Cards**: Key metrics at a glance
- **Activity Feed**: Recent platform activity

### Data Tables
- **Sortable columns**
- **Search and filter**
- **Pagination support**
- **Action buttons** (View/Edit/Delete)

## 🔧 Technical Details

### Frontend Stack
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with flexbox/grid
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icons
- **Google Fonts**: Typography

### Key Features
- **Responsive Design**: Works on desktop, tablet, mobile
- **JWT Authentication**: Secure token-based login
- **RESTful API Integration**: Full CRUD operations
- **Real-time Updates**: Auto-refresh capabilities
- **Toast Notifications**: User feedback system
- **Modal Dialogs**: Create/edit forms

### API Integration
All data operations connect to your FastAPI backend:
- `GET /admin/dashboard` - Dashboard statistics
- `GET /admin/users` - List users
- `POST /admin/users` - Create user
- `DELETE /admin/users/{id}` - Delete user
- `GET /admin/courses` - List courses
- `POST /admin/courses` - Create course
- And more...

## 📱 Responsive Design

The admin panel is fully responsive:
- **Desktop**: Full sidebar navigation
- **Tablet**: Collapsible sidebar
- **Mobile**: Bottom navigation bar

## 🔐 Security Features

- **JWT Token Authentication**
- **Role-based Access Control**
- **Secure API Communication**
- **Auto-logout on Token Expiry**
- **CORS Protection**

## 🎨 Customization

### Styling
- Edit `styles.css` to customize colors, fonts, layout
- Modern CSS with CSS Grid and Flexbox
- Easy theme customization

### Functionality
- Modify `app.js` to add new features
- Extend API endpoints as needed
- Add new sections/pages

## 📋 File Structure

```
admin-frontend/
├── index.html          # Main admin panel
├── styles.css          # All styling
├── app.js             # JavaScript functionality
├── welcome.html       # Setup instructions
└── README.md          # This file
```

## 🐛 Troubleshooting

### Common Issues

1. **Login Not Working**
   - Ensure backend server is running
   - Check API endpoint URLs
   - Verify admin user exists

2. **Data Not Loading**
   - Check browser console for errors
   - Verify JWT token is valid
   - Ensure API endpoints are accessible

3. **Styling Issues**
   - Clear browser cache
   - Check CSS file loading
   - Verify font/icon CDN links

### Browser Console
Press `F12` to open developer tools and check for JavaScript errors.

## 🔄 API Endpoints Used

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/users/login` | Admin authentication |
| GET | `/users/me` | Get current user |
| GET | `/admin/dashboard` | Dashboard stats |
| GET | `/admin/users` | List all users |
| POST | `/admin/users` | Create new user |
| DELETE | `/admin/users/{id}` | Delete user |
| GET | `/admin/courses` | List all courses |
| POST | `/admin/courses` | Create new course |
| DELETE | `/admin/courses/{id}` | Delete course |
| GET | `/admin/enrollments` | List enrollments |

## 🎯 Next Steps

1. **Test the Interface**: Try all CRUD operations
2. **Customize Design**: Modify colors/layout to match brand
3. **Add Features**: Implement additional functionality
4. **Deploy**: Set up proper hosting for production

## 📞 Support

For issues or questions:
1. Check browser console for errors
2. Verify backend API is running
3. Ensure all file paths are correct
4. Test with different browsers

---

**🎉 Your admin panel is ready! Click "Open Admin Panel" to start managing your e-learning platform.**
