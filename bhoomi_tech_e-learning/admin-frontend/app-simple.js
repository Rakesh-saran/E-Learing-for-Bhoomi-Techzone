// Simplified Dashboard App
console.log('Loading simplified dashboard app...');

// Global variables
const apiBase = 'http://127.0.0.1:8001';
let authToken = localStorage.getItem('adminToken') || 'demo-token';

// DOM elements
let mainApp, loginModal;

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting Dashboard...');
    
    // Initialize DOM elements
    mainApp = document.getElementById('mainApp');
    loginModal = document.getElementById('loginModal');
    
    // Load dashboard immediately
    loadDashboard();
    
    console.log('Dashboard initialization complete');
});

function loadDashboard() {
    console.log('=== LOADING DASHBOARD ===');
    
    try {
        // Load sample stats
        console.log('Setting dashboard stats...');
        document.getElementById('totalUsers').textContent = '245';
        document.getElementById('totalCourses').textContent = '18';
        document.getElementById('totalEnrollments').textContent = '342';
        document.getElementById('totalPayments').textContent = '189';
        document.getElementById('totalReviews').textContent = '156';
        document.getElementById('totalRevenue').textContent = '$24,580';
        
        // Load detailed stats
        const detailElements = [
            'newUsersToday', 'activeUsers', 'publishedCourses', 'draftCourses',
            'completedEnrollments', 'activeEnrollments', 'monthlyRevenue', 
            'avgRevenue', 'avgRating', 'pendingReviews'
        ];
        
        const sampleValues = ['8', '234', '15', '3', '145', '197', '4,250', '1,365', '4.6', '12'];
        
        detailElements.forEach((id, index) => {
            const element = document.getElementById(id);
            if (element && sampleValues[index]) {
                element.textContent = sampleValues[index];
            }
        });
        
        console.log('✓ Dashboard stats loaded successfully');
        showToast('Dashboard loaded successfully!', 'success');
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Error loading dashboard', 'error');
    }
}

// Utility functions
function showToast(message, type) {
    console.log(`Toast: ${message} (${type})`);
    // Simple toast implementation
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.padding = '10px 20px';
    toast.style.backgroundColor = type === 'success' ? '#4CAF50' : 
                                   type === 'error' ? '#f44336' : '#2196F3';
    toast.style.color = 'white';
    toast.style.borderRadius = '4px';
    toast.style.zIndex = '10000';
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        document.body.removeChild(toast);
    }, 3000);
}

// Navigation function
function navigateToSection(sectionName) {
    console.log(`Navigating to section: ${sectionName}`);
    
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const navItem = document.querySelector(`[data-section="${sectionName}"]`);
    if (navItem) {
        navItem.classList.add('active');
    }
    
    // Update content
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    const section = document.getElementById(sectionName);
    if (section) {
        section.classList.add('active');
    }
    
    // Update page title
    const title = sectionName.charAt(0).toUpperCase() + sectionName.slice(1);
    const pageTitle = document.getElementById('pageTitle');
    if (pageTitle) {
        pageTitle.textContent = title;
    }
    
    // Load section data
    if (sectionName === 'dashboard') {
        loadDashboard();
    }
}

console.log('Simplified dashboard app loaded!');
