import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import torch
import numpy as np
import librosa
from werkzeug.utils import secure_filename
from chatbot import NeuroLensChatbot
from productivity_coach import ProductivityCoach
from mood_forecast import MoodForecast
from role_personalization import RolePersonalization
from emotion_twin import EmotionTwin
from neuro_challenges import NeuroChallenges
from bio_sync import BioSync
from micro_empathy import MicroEmpathy
from emotion_privacy import EmotionPrivacy
from resilience_builder import ResilienceBuilder
from emotion_forecast import EmotionForecast
from mind_rooms import MindRooms
from emotion_anchors import EmotionAnchors
from coping_coach import CopingCoach
import database as db

app = Flask(__name__)
app.secret_key = 'neurolens_secret_key_2024'
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize all modules
chatbot = NeuroLensChatbot()
productivity_coach = ProductivityCoach()
mood_forecast = MoodForecast()
role_personalization = RolePersonalization()
emotion_twin = EmotionTwin()
neuro_challenges = NeuroChallenges()
bio_sync = BioSync()
micro_empathy = MicroEmpathy()
emotion_privacy = EmotionPrivacy()
resilience_builder = ResilienceBuilder()
emotion_forecast = EmotionForecast()
mind_rooms = MindRooms()
emotion_anchors = EmotionAnchors()
coping_coach = CopingCoach()
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
    # Auto-login as demo user
    if 'user_id' not in session:
        session['user_id'] = 1
        session['role'] = 'child'
        session['username'] = 'demo'
        session['user_type'] = 'student'
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    
    user = db.verify_user(username, password)
    if user:
        session['user_id'] = user[0]
        session['role'] = user[1]
        session['username'] = username
        session['user_type'] = user[3] if len(user) > 3 else 'child'
        return jsonify({"success": True, "role": user[1], "user_type": session['user_type']})
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    role = request.json.get("role")
    parent_code = request.json.get("parent_code")
    user_type = request.json.get("user_type", "child")
    
    parent_id = None
    if role == 'child' and parent_code:
        parent_id = int(parent_code)
    
    user_id = db.create_user(username, password, role, parent_id, user_type)
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
    if 'user_id' not in session:
        session['user_id'] = 1
        session['role'] = 'child'
        session['username'] = 'demo'
        session['user_type'] = 'student'
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
    detected_emotion = request.json.get("emotion", None)  # Get emotion from frontend
    
    bot_response = chatbot.get_response(user_message, detected_emotion)
    
    if 'user_id' in session:
        sentiment = chatbot.analyze_response(user_message)
        db.log_chat(session['user_id'], user_message, bot_response, sentiment)
    
    return jsonify({"response": bot_response})

@app.route("/log_emotion", methods=["POST"])
def log_emotion():
    if 'user_id' not in session:
        session['user_id'] = 1
        session['username'] = 'demo'
    
    emotion = request.json.get("emotion")
    confidence = request.json.get("confidence", 0.9)
    
    # Create privacy-protected record
    privacy_record = emotion_privacy.create_privacy_record(emotion, confidence, session['user_id'])
    
    try:
        db.log_emotion(session['user_id'], emotion, confidence)
    except:
        pass
    
    # Get productivity coaching based on emotion
    coaching = productivity_coach.analyze_emotion(emotion, confidence)
    
    return jsonify({"success": True, "coaching": coaching, "privacy": privacy_record})

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
            "user_id": session['user_id'],
            "user_type": session.get('user_type', 'child')
        })
    return jsonify({"logged_in": False})

@app.route("/get_personalized_content", methods=["GET"])
def get_personalized_content():
    if 'user_id' not in session:
        session['user_id'] = 1
        session['user_type'] = 'student'
    
    user_type = session.get('user_type', 'child')
    emotion = request.args.get('emotion', None)
    
    content = role_personalization.get_personalized_content(user_type, emotion)
    daily_challenge = role_personalization.get_daily_challenge(user_type)
    time_tip = role_personalization.get_role_specific_tips(user_type, None)
    
    return jsonify({
        "success": True,
        "content": content,
        "daily_challenge": daily_challenge,
        "time_tip": time_tip
    })

@app.route("/get_break_suggestion", methods=["GET"])
def get_break_suggestion():
    suggestions = productivity_coach.get_break_suggestion()
    return jsonify(suggestions)

@app.route("/reset_work_session", methods=["POST"])
def reset_work_session():
    productivity_coach.reset_session()
    return jsonify({"success": True, "message": "Work session reset!"})

@app.route("/get_mood_forecast", methods=["GET"])
def get_mood_forecast():
    if 'user_id' not in session:
        session['user_id'] = 1
        session['role'] = 'child'
    
    # Get user's emotion history
    emotions = db.get_child_emotions(session['user_id']) if session['role'] == 'parent' else []
    
    # For child users, get their own emotions
    if session['role'] == 'child':
        import sqlite3
        conn = sqlite3.connect('neurolens.db')
        c = conn.cursor()
        c.execute('''SELECT username, emotion, confidence, timestamp 
                     FROM emotion_logs 
                     WHERE user_id = ? 
                     ORDER BY timestamp DESC LIMIT 100''', (session['user_id'],))
        emotions = c.fetchall()
        conn.close()
    
    # Analyze mood patterns
    insights = mood_forecast.analyze_mood_history(emotions)
    daily_forecast = mood_forecast.get_daily_forecast(emotions)
    weekly_outlook = mood_forecast.get_weekly_outlook(emotions)
    
    return jsonify({
        "success": True,
        "insights": insights,
        "daily_forecast": daily_forecast,
        "weekly_outlook": weekly_outlook
    })

@app.route("/get_focus_game", methods=["GET"])
def get_focus_game():
    game = role_personalization.get_focus_game()
    return jsonify(game)

@app.route("/get_journal_prompt", methods=["GET"])
def get_journal_prompt():
    prompt = role_personalization.get_journal_prompt()
    return jsonify({"prompt": prompt})

@app.route("/get_peer_topic", methods=["GET"])
def get_peer_topic():
    topic = role_personalization.get_peer_topic()
    return jsonify({"topic": topic})

@app.route("/get_weekly_emotions", methods=["GET"])
def get_weekly_emotions():
    if 'user_id' not in session:
        session['user_id'] = 1
    
    try:
        import sqlite3
        conn = sqlite3.connect('neurolens.db')
        c = conn.cursor()
        c.execute('''SELECT emotion, timestamp 
                     FROM emotion_logs 
                     WHERE user_id = ? 
                     AND datetime(timestamp) >= datetime('now', '-7 days')
                     ORDER BY timestamp ASC''', (session['user_id'],))
        emotions = c.fetchall()
        conn.close()
        return jsonify({"success": True, "emotions": emotions})
    except:
        return jsonify({"success": True, "emotions": []})

@app.route("/get_twin_response", methods=["POST"])
def get_twin_response():
    if 'user_id' not in session:
        session['user_id'] = 1
    user_message = request.json.get('message', None)
    response = emotion_twin.twin_response(session['user_id'], user_message)
    return jsonify(response)

@app.route("/get_twin_profile", methods=["GET"])
def get_twin_profile():
    if 'user_id' not in session:
        session['user_id'] = 1
    profile = emotion_twin.get_emotion_profile(session['user_id'])
    return jsonify(profile if profile else {})

@app.route("/get_weekly_reflection", methods=["GET"])
def get_weekly_reflection():
    if 'user_id' not in session:
        session['user_id'] = 1
    reflection = emotion_twin.get_weekly_reflection(session['user_id'])
    return jsonify({'reflection': reflection})

@app.route("/get_challenge", methods=["GET"])
def get_challenge():
    challenge = neuro_challenges.get_daily_challenge()
    return jsonify(challenge)

@app.route("/complete_challenge", methods=["POST"])
def complete_challenge():
    if 'user_id' not in session:
        session['user_id'] = 1
    challenge_id = request.json.get('challenge_id')
    detected_emotion = request.json.get('detected_emotion')
    duration_met = request.json.get('duration_met', True)
    
    if neuro_challenges.verify_challenge(challenge_id, detected_emotion, duration_met):
        result = neuro_challenges.complete_challenge(session['user_id'], challenge_id)
        return jsonify({'success': True, **result})
    return jsonify({'success': False, 'message': 'Challenge not completed correctly'})

@app.route("/get_user_stats", methods=["GET"])
def get_user_stats():
    if 'user_id' not in session:
        session['user_id'] = 1
    stats = neuro_challenges.get_user_stats(session['user_id'])
    return jsonify(stats)

@app.route("/get_bio_sync", methods=["GET"])
def get_bio_sync():
    emotion = request.args.get('emotion', 'neutral')
    data = bio_sync.get_bio_sync_data(emotion)
    return jsonify(data)

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/get_empathy_prompt", methods=["GET"])
def get_empathy_prompt():
    emotion = request.args.get('emotion', 'neutral')
    user_type = session.get('user_type', 'general')
    prompt_data = micro_empathy.get_empathy_prompt(emotion, user_type)
    return jsonify(prompt_data)

@app.route("/get_privacy_stats", methods=["GET"])
def get_privacy_stats():
    stats = emotion_privacy.get_privacy_stats()
    return jsonify(stats)

@app.route("/export_emotion_dna", methods=["GET"])
def export_emotion_dna():
    if 'user_id' not in session:
        session['user_id'] = 1
    
    import sqlite3
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    c.execute('SELECT emotion, confidence FROM emotion_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 100', (session['user_id'],))
    logs = c.fetchall()
    conn.close()
    
    dna_data = emotion_privacy.export_emotion_dna(session['user_id'], logs)
    
    from flask import Response
    return Response(
        dna_data,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=emotion_dna.mooddna'}
    )

@app.route("/admin/emotion_cloud", methods=["GET"])
def emotion_cloud():
    import sqlite3
    from collections import Counter
    from datetime import datetime, timedelta
    
    conn = sqlite3.connect('neurolens.db')
    c = conn.cursor()
    
    # Get all emotions from last 24 hours
    c.execute('''SELECT emotion, timestamp FROM emotion_logs 
                 WHERE datetime(timestamp) >= datetime('now', '-1 day')''')
    emotions = c.fetchall()
    
    # Distribution
    emotion_counts = Counter([e[0] for e in emotions])
    total = len(emotions) or 1
    distribution = {k: round(v/total*100, 1) for k, v in emotion_counts.items()}
    
    # Hourly trends (last 24 hours)
    hourly_data = {i: {'happy': 0, 'sad': 0, 'stress': 0} for i in range(24)}
    for emotion, timestamp in emotions:
        hour = datetime.fromisoformat(timestamp).hour
        if emotion == 'happy':
            hourly_data[hour]['happy'] += 1
        elif emotion == 'sad':
            hourly_data[hour]['sad'] += 1
        elif emotion in ['angry', 'fear']:
            hourly_data[hour]['stress'] += 1
    
    # Anomaly detection
    anomalies = []
    sad_count = emotion_counts.get('sad', 0)
    if sad_count > total * 0.3:
        anomalies.append({
            'title': 'High Sadness Detected',
            'message': f'Sadness levels at {round(sad_count/total*100, 1)}% - above normal threshold'
        })
    
    stress_count = emotion_counts.get('angry', 0) + emotion_counts.get('fear', 0)
    if stress_count > total * 0.25:
        anomalies.append({
            'title': 'Stress Surge',
            'message': f'Stress emotions increased by {round(stress_count/total*100, 1)}%'
        })
    
    # Get unique users
    c.execute('SELECT COUNT(DISTINCT user_id) FROM emotion_logs')
    total_users = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'distribution': distribution,
        'hourly_labels': [f'{i}:00' for i in range(24)],
        'hourly_happy': [hourly_data[i]['happy'] for i in range(24)],
        'hourly_sad': [hourly_data[i]['sad'] for i in range(24)],
        'hourly_stress': [hourly_data[i]['stress'] for i in range(24)],
        'total_users': total_users,
        'dominant_emotion': emotion_counts.most_common(1)[0][0] if emotion_counts else 'neutral',
        'avg_health': round(75 - (sad_count/total*20) if total > 0 else 75, 1),
        'peak_stress_time': max(hourly_data.items(), key=lambda x: x[1]['stress'])[0] if emotions else 'N/A',
        'anomalies': anomalies
    })

@app.route("/get_resilience_score", methods=["GET"])
def get_resilience_score():
    if 'user_id' not in session:
        session['user_id'] = 1
    metrics = resilience_builder.calculate_resilience_score(session['user_id'])
    resilience_builder.save_weekly_metrics(session['user_id'], metrics)
    goal = resilience_builder.generate_weekly_goal(session['user_id'], metrics)
    return jsonify({**metrics, 'goal': goal})

@app.route("/get_resilience_trend", methods=["GET"])
def get_resilience_trend():
    if 'user_id' not in session:
        session['user_id'] = 1
    trend = resilience_builder.get_weekly_trend(session['user_id'])
    return jsonify({'trend': trend})

@app.route("/get_emotion_forecast", methods=["GET"])
def get_emotion_forecast():
    if 'user_id' not in session:
        session['user_id'] = 1
    forecast = emotion_forecast.get_3day_forecast(session['user_id'])
    return jsonify({'forecast': forecast, 'success': True})

@app.route("/join_mind_room", methods=["GET"])
def join_mind_room():
    if 'user_id' not in session:
        session['user_id'] = 1
    room = mind_rooms.assign_room(session['user_id'])
    participants = mind_rooms.get_room_participants(room['name'])
    return jsonify({
        'room': room['name'],
        'color': room['color'],
        'sound': room['sound'],
        'bpm': room['bpm'],
        'participants': participants
    })

@app.route("/create_anchor", methods=["POST"])
def create_anchor():
    if 'user_id' not in session:
        session['user_id'] = 1
    data = request.json
    anchor = emotion_anchors.create_anchor(
        session['user_id'],
        data['emotion'],
        data['confidence'],
        data['image_data'],
        data.get('note', '')
    )
    return jsonify({'success': True, 'anchor': anchor})

@app.route("/get_anchors", methods=["GET"])
def get_anchors():
    if 'user_id' not in session:
        session['user_id'] = 1
    anchors = emotion_anchors.get_anchors(session['user_id'])
    return jsonify({'anchors': anchors})

@app.route("/get_anchor/<anchor_id>", methods=["GET"])
def get_anchor(anchor_id):
    anchor = emotion_anchors.get_anchor(anchor_id)
    return jsonify(anchor if anchor else {'error': 'Not found'})

@app.route("/suggest_anchor", methods=["GET"])
def suggest_anchor():
    if 'user_id' not in session:
        session['user_id'] = 1
    anchor = emotion_anchors.get_random_positive_anchor(session['user_id'])
    return jsonify(anchor if anchor else {'none': True})

@app.route("/get_coping_action", methods=["GET"])
def get_coping_action():
    emotion = request.args.get('emotion', 'stressed')
    if coping_coach.should_suggest(emotion):
        action = coping_coach.get_coping_action(emotion)
        return jsonify({'suggest': True, 'action': action, 'emotion': emotion})
    return jsonify({'suggest': False})

@app.route("/log_coping", methods=["POST"])
def log_coping():
    if 'user_id' not in session:
        session['user_id'] = 1
    data = request.json
    coping_coach.log_action(
        session['user_id'],
        data['emotion_before'],
        data['coping_type'],
        data['coping_title'],
        data.get('emotion_after', '')
    )
    return jsonify({'success': True})

@app.route("/get_coping_history", methods=["GET"])
def get_coping_history():
    if 'user_id' not in session:
        session['user_id'] = 1
    history = coping_coach.get_history(session['user_id'])
    return jsonify({'history': history})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
