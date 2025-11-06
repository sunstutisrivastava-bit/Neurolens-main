"""
Simple script to run NeuroLens server with debug info
"""
import sys
print("=" * 50)
print("Starting NeuroLens Server...")
print("=" * 50)

try:
    import flask
    print(f"✓ Flask installed: {flask.__version__}")
except ImportError:
    print("✗ Flask not installed. Run: pip install flask")
    sys.exit(1)

try:
    import database as db
    print("✓ Database module loaded")
    db.init_db()
    print("✓ Database initialized")
except Exception as e:
    print(f"✗ Database error: {e}")

try:
    from app import app
    print("✓ App module loaded")
    print("\n" + "=" * 50)
    print("Server starting on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)
except Exception as e:
    print(f"✗ Error starting server: {e}")
    import traceback
    traceback.print_exc()
