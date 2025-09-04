import requests
import json

# Test API endpoints
base_url = "http://127.0.0.1:8001"

try:
    # Test root endpoint
    response = requests.get(f"{base_url}/")
    print(f"Root endpoint status: {response.status_code}")
    print(f"Root response: {response.json()}")
    
    # Test docs endpoint
    docs_response = requests.get(f"{base_url}/docs")
    print(f"Docs endpoint status: {docs_response.status_code}")
    
    # Test admin dashboard endpoint
    admin_response = requests.get(f"{base_url}/admin/dashboard")
    print(f"Admin dashboard status: {admin_response.status_code}")
    
    # Test home feed
    home_response = requests.get(f"{base_url}/home-feed")
    print(f"Home feed status: {home_response.status_code}")
    
except Exception as e:
    print(f"Error testing API: {e}")
