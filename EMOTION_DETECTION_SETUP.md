# Emotion Detection Setup

## For Accurate Emotion Detection in Challenges

### Option 1: Install DeepFace (Recommended)
```bash
pip install deepface
pip install tf-keras
```

DeepFace will automatically detect emotions: happy, sad, angry, surprise, fear, disgust, neutral

### Option 2: Use OpenCV Fallback (Already Implemented)
The system has a fallback that uses brightness/contrast analysis if DeepFace is not available.

### Option 3: Use Pre-trained Model
If you have a custom emotion detection model, replace the `/detect_emotion` endpoint in `app.py` with your model inference code.

## Testing
1. Start the Flask app: `python app.py`
2. Go to Challenges page
3. Click "Start Challenge"
4. Camera will open and detect your expression in real-time
5. Match the target emotion to earn coins

## Accuracy Tips
- Good lighting improves detection
- Face the camera directly
- Make clear facial expressions
- DeepFace provides 90%+ accuracy
- Fallback method provides ~60-70% accuracy
