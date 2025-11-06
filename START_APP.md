# NeuroLens - Quick Start Guide

## How to Run the Application

### Step 1: Start the Flask Server
Open a terminal/command prompt in this directory and run:
```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 2: Open Your Browser
Go to: **http://localhost:5000**

### Step 3: Register a New Account
1. Click the "Register" tab
2. Fill in:
   - Username: (your choice)
   - Password: (your choice)
   - Role: Child (or Parent if you want to monitor children)
   - User Type: Student/College/Corporate
3. Click "Register"
4. If you're a Parent, note your Parent ID shown in the success message

### Step 4: Login
1. Enter your username and password
2. Click "Login"
3. You'll be redirected to the main dashboard

## Troubleshooting

### Login/Register Not Working?
1. Make sure Flask server is running (check terminal)
2. Check browser console for errors (F12 → Console tab)
3. Try the test page: http://localhost:5000/test_login.html

### Database Issues?
Delete `neurolens.db` and restart the app to reset the database.

### Port Already in Use?
Change port in app.py:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

## Features Available After Login
- 🎥 Real-time Emotion Detection
- 🌈 Color Dashboard (weekly emotion visualization)
- 💬 AI Chatbot Assistant
- 😊 AI Companion Avatar (with voice feedback)
- 📊 Mood Forecast
- 💡 Productivity Coach
- 🎯 Role-based Personalization

## Default Test Account
If you want to test quickly:
- Username: testuser
- Password: test123
- Role: child
- Type: student

(Register this account first using the test_login.html page)
