# NeuroLens Troubleshooting Guide

## Problem: Login/Register Not Working

### Step 1: Check if Server is Running
Open terminal and run:
```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Running on http://localhost:5000
```

If you see errors, check Step 2.

### Step 2: Install Missing Dependencies
```bash
pip install flask numpy librosa torch werkzeug
```

### Step 3: Test the Server
Open a NEW terminal (keep server running) and run:
```bash
python test_routes.py
```

This will test if login/register routes work.

### Step 4: Check Browser Console
1. Open browser (Chrome/Firefox)
2. Go to http://localhost:5000
3. Press F12 to open Developer Tools
4. Click "Console" tab
5. Try to login/register
6. Look for RED error messages

Common errors:
- **CORS error**: Server not running
- **404 error**: Wrong URL
- **500 error**: Server crash (check terminal)

### Step 5: Clear Browser Cache
1. Press Ctrl+Shift+Delete
2. Clear "Cached images and files"
3. Refresh page (Ctrl+F5)

### Step 6: Try Different Browser
- Chrome
- Firefox
- Edge

### Step 7: Check Firewall
Windows Firewall might block port 5000:
1. Search "Windows Firewall"
2. Click "Allow an app through firewall"
3. Find Python and check both boxes

### Step 8: Use Different Port
Edit `app.py`, change last line:
```python
app.run(debug=True, port=5001)  # Changed from 5000
```

Then go to: http://localhost:5001

## Quick Test Account
After server starts, open browser console (F12) and paste:

```javascript
// Register test user
fetch('http://localhost:5000/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    username: 'test',
    password: 'test',
    role: 'child',
    parent_code: null,
    user_type: 'student'
  })
}).then(r => r.json()).then(d => console.log('Register:', d));

// Login test user (wait 2 seconds after register)
setTimeout(() => {
  fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      username: 'test',
      password: 'test'
    })
  }).then(r => r.json()).then(d => {
    console.log('Login:', d);
    if (d.success) window.location.href = '/child_dashboard';
  });
}, 2000);
```

## Still Not Working?

### Check Python Version
```bash
python --version
```
Should be Python 3.7 or higher.

### Reinstall Everything
```bash
pip uninstall flask
pip install flask
```

### Delete Database and Restart
```bash
del neurolens.db
python app.py
```

### Check if Port is Already Used
```bash
netstat -ano | findstr :5000
```

If something is using port 5000, kill it or use different port.

## Contact Info
If nothing works, check:
1. Terminal output for errors
2. Browser console (F12) for errors
3. Make sure you're using http://localhost:5000 (not https)
