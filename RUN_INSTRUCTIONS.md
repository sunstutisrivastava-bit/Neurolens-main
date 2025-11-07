# NeuroLens - How to Run

## Quick Start Guide

### 1. View Model Information (Check what's trained)
```bash
python view_model_info.py
```

This shows:
- All trained models with accuracy
- Model file sizes and dates
- Architecture details
- Training statistics

### 2. Train Models (If not trained yet)
```bash
python train_all_models.py
```

This will:
- Train Voice Emotion Model (LSTM)
- Train Image Emotion Model (CNN)
- Show real-time progress
- Display accuracy for each model
- Save results to training_results.json

### 3. Run the Application
```bash
python app.py
```

Then open browser: http://localhost:5000

## Step-by-Step Instructions

### First Time Setup:
1. Open terminal/command prompt
2. Navigate to project folder:
   ```bash
   cd c:\Users\sunst\Downloads\NeuroLens-main\NeuroLens-main
   ```

3. Check if models exist:
   ```bash
   python view_model_info.py
   ```

4. If no models found, train them:
   ```bash
   python train_all_models.py
   ```
   (This may take 10-30 minutes depending on your computer)

5. Run the app:
   ```bash
   python app.py
   ```

6. Open browser and go to: http://localhost:5000

### Using the App:
1. Click "Start Detection" to begin emotion tracking
2. Allow camera/microphone access
3. Your emotions will be detected in real-time
4. Try different features:
   - Challenges (earn coins)
   - Mood Journal (10 photos/day)
   - Resilience Builder
   - Mind Rooms
   - Bio-Sync

## Troubleshooting

### No models found?
Run: `python train_all_models.py`

### Training fails?
Check if you have these installed:
```bash
pip install tensorflow keras numpy pandas scikit-learn
```

### Camera not working?
- Allow browser camera permissions
- Check if another app is using camera

### Port 5000 already in use?
Change port in app.py:
```python
app.run(debug=True, port=5001)
```

## File Structure
```
NeuroLens-main/
├── app.py                      # Main Flask application
├── train_all_models.py         # Train all models with tracking
├── view_model_info.py          # View model information
├── checkpoints/                # Trained models saved here
│   ├── perfect_voice_model.h5
│   └── perfect_image_model.h5
├── training_results.json       # Training accuracy results
└── templates/
    └── index.html              # Frontend UI
```

## Commands Summary
```bash
# View models
python view_model_info.py

# Train models
python train_all_models.py

# Run app
python app.py
```
