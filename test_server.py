"""
Minimal test to verify server starts correctly
"""
print("=" * 60)
print("NEUROLENS SERVER TEST")
print("=" * 60)

# Test 1: Check imports
print("\n[1/5] Testing imports...")
try:
    from flask import Flask
    print("✓ Flask imported")
    import database
    print("✓ Database imported")
    from chatbot import NeuroLensChatbot
    print("✓ Chatbot imported")
    from productivity_coach import ProductivityCoach
    print("✓ Productivity Coach imported")
    from mood_forecast import MoodForecast
    print("✓ Mood Forecast imported")
    from role_personalization import RolePersonalization
    print("✓ Role Personalization imported")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)

# Test 2: Initialize database
print("\n[2/5] Initializing database...")
try:
    database.init_db()
    print("✓ Database initialized")
except Exception as e:
    print(f"✗ Database failed: {e}")
    exit(1)

# Test 3: Load app
print("\n[3/5] Loading Flask app...")
try:
    from app import app
    print("✓ App loaded")
except Exception as e:
    print(f"✗ App failed: {e}")
    exit(1)

# Test 4: Check routes
print("\n[4/5] Checking routes...")
routes = [str(rule) for rule in app.url_map.iter_rules()]
important_routes = ['/', '/login', '/register', '/child_dashboard', '/simple']
for route in important_routes:
    if route in routes:
        print(f"✓ {route}")
    else:
        print(f"✗ {route} missing")

# Test 5: Start server
print("\n[5/5] Starting server...")
print("=" * 60)
print("SERVER STARTING ON http://localhost:5000")
print("=" * 60)
print("\nOpen your browser and go to:")
print("  → http://localhost:5000/simple")
print("\nPress Ctrl+C to stop the server")
print("=" * 60)
print()

try:
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
except Exception as e:
    print(f"\n✗ Server failed to start: {e}")
    print("\nPossible solutions:")
    print("1. Port 5000 might be in use - try closing other programs")
    print("2. Run: netstat -ano | findstr :5000")
    print("3. Try a different port by editing app.py")
