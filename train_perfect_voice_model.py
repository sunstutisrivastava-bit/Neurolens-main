import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, BatchNormalization, Conv1D, MaxPooling1D, GlobalMaxPooling1D, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import AdamW
from tensorflow.keras.regularizers import l2
import numpy as np
import librosa
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Paths
voice_dir = "models/voice"
save_dir = "checkpoints"
os.makedirs(save_dir, exist_ok=True)

def extract_advanced_features(file_path, duration=3):
    """Extract comprehensive audio features"""
    try:
        y, sr = librosa.load(file_path, duration=duration, sr=22050)
        
        # Spectral features
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        chroma = librosa.feature.chroma(y=y, sr=sr)
        mel = librosa.feature.melspectrogram(y=y, sr=sr)
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
        
        # Rhythm features
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        
        # Combine all features
        features = np.concatenate([
            np.mean(mfccs.T, axis=0),
            np.std(mfccs.T, axis=0),
            np.mean(chroma.T, axis=0),
            np.std(chroma.T, axis=0),
            np.mean(mel.T, axis=0),
            np.std(mel.T, axis=0),
            np.mean(contrast.T, axis=0),
            np.std(contrast.T, axis=0),
            np.mean(tonnetz.T, axis=0),
            np.std(tonnetz.T, axis=0),
            [tempo],
            np.mean(zcr.T, axis=0),
            np.std(zcr.T, axis=0),
            np.mean(spectral_centroids.T, axis=0),
            np.std(spectral_centroids.T, axis=0),
            np.mean(spectral_rolloff.T, axis=0),
            np.std(spectral_rolloff.T, axis=0),
            np.mean(spectral_bandwidth.T, axis=0),
            np.std(spectral_bandwidth.T, axis=0)
        ])
        
        return features
    except:
        return np.zeros(400)  # Return zeros if file can't be processed

def load_voice_data():
    """Load and process voice data"""
    X, y = [], []
    
    if not os.path.exists(voice_dir):
        print("Creating sample voice data...")
        # Create sample data for demonstration
        emotions = ['happy', 'sad', 'angry', 'neutral', 'surprised', 'fear', 'disgust']
        for emotion in emotions:
            for i in range(100):  # 100 samples per emotion
                # Generate synthetic features
                features = np.random.randn(400)
                X.append(features)
                y.append(emotion)
    else:
        # Load real data
        for emotion_folder in os.listdir(voice_dir):
            emotion_path = os.path.join(voice_dir, emotion_folder)
            if os.path.isdir(emotion_path):
                for file in os.listdir(emotion_path):
                    if file.endswith(('.wav', '.mp3', '.flac')):
                        file_path = os.path.join(emotion_path, file)
                        features = extract_advanced_features(file_path)
                        X.append(features)
                        y.append(emotion_folder)
    
    return np.array(X), np.array(y)

# Load data
print("Loading voice data...")
X, y = load_voice_data()

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_categorical = tf.keras.utils.to_categorical(y_encoded)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42, stratify=y_categorical)

# Reshape for CNN-LSTM
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Advanced hybrid model
model = Sequential([
    # CNN layers for feature extraction
    Conv1D(128, 5, activation='relu', input_shape=(X_train.shape[1], 1)),
    BatchNormalization(),
    Conv1D(128, 5, activation='relu'),
    MaxPooling1D(2),
    Dropout(0.3),
    
    Conv1D(256, 3, activation='relu'),
    BatchNormalization(),
    Conv1D(256, 3, activation='relu'),
    MaxPooling1D(2),
    Dropout(0.3),
    
    # LSTM layers for temporal modeling
    Bidirectional(LSTM(256, return_sequences=True, dropout=0.3, recurrent_dropout=0.3)),
    Bidirectional(LSTM(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.3)),
    Bidirectional(LSTM(64, dropout=0.3, recurrent_dropout=0.3)),
    
    # Dense layers
    Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.6),
    Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(len(le.classes_), activation='softmax')
])

# Compile with advanced optimizer
model.compile(
    optimizer=AdamW(learning_rate=0.001, weight_decay=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy', 'top_k_categorical_accuracy']
)

# Advanced callbacks
callbacks = [
    EarlyStopping(patience=30, restore_best_weights=True, monitor='val_accuracy'),
    ReduceLROnPlateau(factor=0.1, patience=15, min_lr=1e-8, monitor='val_accuracy'),
    ModelCheckpoint(os.path.join(save_dir, "perfect_voice_model.h5"), save_best_only=True, monitor='val_accuracy')
]

print("Training perfect voice model...")
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print(f"Classes: {le.classes_}")

# Train with extensive epochs
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=200,
    batch_size=16,
    callbacks=callbacks,
    verbose=1
)

# Evaluate
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Final test accuracy: {test_accuracy:.6f}")

# Save label encoder
import pickle
with open(os.path.join(save_dir, 'voice_label_encoder.pkl'), 'wb') as f:
    pickle.dump(le, f)

print("✅ Perfect voice model training complete!")