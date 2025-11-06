╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🧠 NEUROLENS - CONNECTION ERROR FIX             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝


CONNECTION ERROR = SERVER NOT RUNNING!

Follow these 3 simple steps:


┌──────────────────────────────────────────────────────────────┐
│ STEP 1: START THE SERVER                                    │
└──────────────────────────────────────────────────────────────┘

Double-click this file:
  📁 START_SERVER.bat

Wait until you see:
  * Running on http://127.0.0.1:5000

⚠️ KEEP THIS WINDOW OPEN! Don't close it!


┌──────────────────────────────────────────────────────────────┐
│ STEP 2: CHECK IF SERVER IS WORKING                          │
└──────────────────────────────────────────────────────────────┘

Open this file in your browser:
  📁 CHECK_SERVER.html

Click "TEST CONNECTION"

If it says "SERVER IS RUNNING" → Go to Step 3
If it says "SERVER NOT RUNNING" → Go back to Step 1


┌──────────────────────────────────────────────────────────────┐
│ STEP 3: USE THE APP                                         │
└──────────────────────────────────────────────────────────────┘

Open your browser and go to:
  http://localhost:5000/simple

Register → Login → Done!


═══════════════════════════════════════════════════════════════

STILL NOT WORKING?

1. Install Python dependencies:
   pip install flask numpy librosa torch werkzeug

2. Check if Python is installed:
   python --version

3. Try manual start:
   - Open Command Prompt
   - Type: cd c:\Users\sunst\Downloads\NeuroLens-main\NeuroLens-main
   - Type: python test_server.py

4. Check port 5000:
   netstat -ano | findstr :5000

═══════════════════════════════════════════════════════════════

FILES YOU NEED:
✓ START_SERVER.bat     → Starts the server
✓ CHECK_SERVER.html    → Tests if server works
✓ QUICK_START.txt      → Detailed instructions
✓ TROUBLESHOOTING.md   → Advanced help

═══════════════════════════════════════════════════════════════
