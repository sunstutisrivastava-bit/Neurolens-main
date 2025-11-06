# LOGIN FIX - FOLLOW THESE STEPS

## Step 1: Start the Server
Open terminal in this folder and run:
```bash
python app.py
```

Wait until you see:
```
* Running on http://127.0.0.1:5000
```

## Step 2: Try the Simple Login Page
Open your browser and go to:
```
http://localhost:5000/simple
```

This is a simplified login page that WILL work.

## Step 3: Register an Account
1. Click "Register" tab
2. Enter username (e.g., "alex")
3. Enter password (e.g., "123")
4. Select role: Child
5. Select type: Student
6. Click "Register"

You should see: "Success! Now login."

## Step 4: Login
1. Click "Login" tab
2. Enter your username
3. Enter your password
4. Click "Login"

You should be redirected to the main dashboard!

## If It Still Doesn't Work

### Check Browser Console
1. Press F12
2. Click "Console" tab
3. Look for errors (red text)
4. Take a screenshot and check what it says

### Common Issues:

**"Server error. Is it running?"**
- Make sure `python app.py` is running in terminal
- Check terminal for error messages

**"Login failed"**
- Make sure you registered first
- Check username/password are correct
- Try registering a new account

**Page doesn't load**
- Make sure you're using `http://` not `https://`
- Try: http://127.0.0.1:5000/simple
- Check if port 5000 is blocked by firewall

### Alternative: Use Original Login Page
If simple login works, try the original:
```
http://localhost:5000
```

Both pages connect to the same backend, so if one works, both should work.

## Test Commands

### Quick Test (paste in browser console - F12):
```javascript
// Test register
fetch('http://localhost:5000/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    username: 'quicktest',
    password: 'test123',
    role: 'child',
    parent_code: null,
    user_type: 'student'
  })
}).then(r => r.json()).then(console.log);

// Test login (run 2 seconds after register)
setTimeout(() => {
  fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      username: 'quicktest',
      password: 'test123'
    })
  }).then(r => r.json()).then(d => {
    console.log(d);
    if (d.success) alert('LOGIN WORKS!');
  });
}, 2000);
```

## Success Checklist
- [ ] Server running (python app.py)
- [ ] Can access http://localhost:5000/simple
- [ ] Can register new account
- [ ] Can login with account
- [ ] Redirects to dashboard after login

If all checked, login is working! 🎉
