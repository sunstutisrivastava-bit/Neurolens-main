"""
Test script to verify Flask routes are working
Run this AFTER starting the server with: python app.py
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("Testing NeuroLens Routes...")
print("=" * 50)

# Test 1: Home page
try:
    response = requests.get(BASE_URL)
    print(f"✓ Home page: {response.status_code}")
except Exception as e:
    print(f"✗ Home page failed: {e}")

# Test 2: Register
try:
    data = {
        "username": "testuser123",
        "password": "test123",
        "role": "child",
        "parent_code": None,
        "user_type": "student"
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    result = response.json()
    print(f"✓ Register: {result}")
except Exception as e:
    print(f"✗ Register failed: {e}")

# Test 3: Login
try:
    data = {
        "username": "testuser123",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/login", json=data)
    result = response.json()
    print(f"✓ Login: {result}")
    
    if result.get('success'):
        print("\n✓✓✓ LOGIN WORKING! ✓✓✓")
        print("You can now use the web interface")
    else:
        print("\n✗ Login returned success=False")
except Exception as e:
    print(f"✗ Login failed: {e}")

print("=" * 50)
print("\nIf you see errors, make sure:")
print("1. Server is running: python app.py")
print("2. Port 5000 is not blocked")
print("3. Install requests: pip install requests")
