import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import torch
import numpy as np
import librosa
from werkzeug.utils import secure_filename
from chatbot import NeuroLensChatbot
import database as db

app = Flask(__name__)
app.secret_key = 'neurolens_secret_key_2024'
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize chatbot
chatbot = NeuroLensChatbot()
db.init_db()

# --- Fake Models (replace with your own) ---
emotions_image = ["angry", "disgust", "fear", "happy"]
emotions_voice = ["euphoric", "sad", "joyful", "surprised"]

def predict_image(filepath):
    # TODO: replace with your trained image model
    # Right now: return random class
    return np.random.choice(emotions_image)

def predict_voice(filepath):
    # Load audio
    y, sr = librosa.load(filepath, sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    features = np.mean(mfccs.T, axis=0)

    # TODO: replace with your trained voice model
    # Right now: return random class
    return np.random.choice(emotions_voice)

# --- Routes ---
@app.route("/")
def home():
    if 'user_id' in session:
        if session['role'] == 'parent':
            return redirect(url_for('parent_dashboard'))
        else:
            return redirect(url_for('child_dashboard'))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    
    user = db.verify_user(username, password)
    if user:
        session['user_id'] = user[0]
        session['role'] = user[1]
        session['username'] = username
        return jsonify({"success": True, "role": user[1]})
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    role = request.json.get("role")
    parent_code = request.json.get("parent_code")
    
    parent_id = None
    if role == 'child' and parent_code:
        parent_id = int(parent_code)
    
    user_id = db.create_user(username, password, role, parent_id)
    if user_id:
        return jsonify({"success": True, "user_id": user_id})
    return jsonify({"success": False, "message": "Username already exists"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/parent_dashboard")
def parent_dashboard():
    if 'user_id' not in session or session['role'] != 'parent':
        return redirect(url_for('home'))
    return render_template("parent_dashboard.html")

@app.route("/child_dashboard")
def child_dashboard():
    if 'user_id' not in session or session['role'] != 'child':
        return redirect(url_for('home'))
    return render_template("index.html")

@app.route("/analyze_image", methods=["POST"])
def analyze_image():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)
    emotion = predict_image(filepath)
    return jsonify({"emotion": emotion})

@app.route("/analyze_voice", methods=["POST"])
def analyze_voice():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)
    emotion = predict_voice(filepath)
    return jsonify({"emotion": emotion})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    bot_response = chatbot.get_response(user_message)
    
    if 'user_id' in session:
        sentiment = chatbot.analyze_response(user_message)
        db.log_chat(session['user_id'], user_message, bot_response, sentiment)
    
    return jsonify({"response": bot_response})

@app.route("/log_emotion", methods=["POST"])
def log_emotion():
    if 'user_id' not in session:
        return jsonify({"success": False})
    
    emotion = request.json.get("emotion")
    confidence = request.json.get("confidence", 0.9)
    db.log_emotion(session['user_id'], emotion, confidence)
    return jsonify({"success": True})

@app.route("/get_children_data")
def get_children_data():
    if 'user_id' not in session or session['role'] != 'parent':
        return jsonify({"success": False})
    
    children = db.get_children(session['user_id'])
    emotions = db.get_child_emotions(session['user_id'])
    chats = db.get_child_chats(session['user_id'])
    
    return jsonify({
        "success": True,
        "children": children,
        "emotions": emotions,
        "chats": chats
    })

@app.route("/reset_chat", methods=["POST"])
def reset_chat():
    global chatbot
    chatbot = NeuroLensChatbot()
    return jsonify({"response": "Chat reset! How can I help you today?"})

@app.route("/get_user_info")
def get_user_info():
    if 'user_id' in session:
        return jsonify({
            "logged_in": True,
            "username": session['username'],
            "role": session['role'],
            "user_id": session['user_id']
        })
    return jsonify({"logged_in": False})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
