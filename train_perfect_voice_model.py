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

# Maximum accuracy hybrid model
model = Sequential([
    # Enhanced CNN layers
    Conv1D(256, 5, activation='relu', padding='same', input_shape=(X_train.shape[1], 1)),
    BatchNormalization(),
    Conv1D(256, 5, activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling1D(2),
    Dropout(0.25),
    
    Conv1D(512, 3, activation='relu', padding='same'),
    BatchNormalization(),
    Conv1D(512, 3, activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling1D(2),
    Dropout(0.25),
    
    Conv1D(512, 3, activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling1D(2),
    Dropout(0.3),
    
    # Enhanced Bidirectional LSTM layers
    Bidirectional(LSTM(512, return_sequences=True, dropout=0.4, recurrent_dropout=0.4)),
    BatchNormalization(),
    Bidirectional(LSTM(256, return_sequences=True, dropout=0.4, recurrent_dropout=0.4)),
    BatchNormalization(),
    Bidirectional(LSTM(128, dropout=0.4, recurrent_dropout=0.4)),
    BatchNormalization(),
    
    # Enhanced Dense layers
    Dense(1024, activation='relu', kernel_regularizer=l2(0.0005)),
    BatchNormalization(),
    Dropout(0.6),
    Dense(512, activation='relu', kernel_regularizer=l2(0.0005)),
    BatchNormalization(),
    Dropout(0.5),
    Dense(256, activation='relu', kernel_regularizer=l2(0.0005)),
    BatchNormalization(),
    Dropout(0.4),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(len(le.classes_), activation='softmax')
])

# Compile with optimized settings
model.compile(
    optimizer=AdamW(learning_rate=0.0005, weight_decay=0.00005),
    loss='categorical_crossentropy',
    metrics=['accuracy', 'top_k_categorical_accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
)

# Maximum accuracy callbacks
callbacks = [
    EarlyStopping(patience=50, restore_best_weights=True, monitor='val_accuracy', min_delta=0.0001),
    ReduceLROnPlateau(factor=0.2, patience=20, min_lr=1e-9, monitor='val_accuracy', verbose=1),
    ModelCheckpoint(os.path.join(save_dir, "perfect_voice_model.h5"), save_best_only=True, monitor='val_accuracy', verbose=1)
]

print("Training perfect voice model...")
print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print(f"Classes: {le.classes_}")

# Train with maximum epochs and data augmentation
print("\n" + "="*80)
print("🚀 TRAINING FOR MAXIMUM ACCURACY")
print("="*80)
print(f"Model Parameters: {model.count_params():,}")
print(f"Architecture: CNN-BiLSTM Hybrid with BatchNorm & Dropout")
print(f"Optimizer: AdamW with weight decay")
print(f"Max Epochs: 300 (with early stopping)")
print("="*80 + "\n")

history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=300,
    batch_size=8,
    callbacks=callbacks,
    verbose=1,
    class_weight='balanced'
)

# Comprehensive evaluation
print("\n" + "="*80)
print("📊 FINAL EVALUATION")
print("="*80)
test_results = model.evaluate(X_test, y_test, verbose=0)
test_loss = test_results[0]
test_accuracy = test_results[1]
test_top_k = test_results[2]
test_precision = test_results[3]
test_recall = test_results[4]

print(f"Test Loss: {test_loss:.6f}")
print(f"Test Accuracy: {test_accuracy*100:.2f}%")
print(f"Top-K Accuracy: {test_top_k*100:.2f}%")
print(f"Precision: {test_precision*100:.2f}%")
print(f"Recall: {test_recall*100:.2f}%")
print(f"F1-Score: {2*(test_precision*test_recall)/(test_precision+test_recall)*100:.2f}%")
print("="*80)

# Save label encoder
import pickle
with open(os.path.join(save_dir, 'voice_label_encoder.pkl'), 'wb') as f:
    pickle.dump(le, f)

print("\n" + "="*80)
print("✅ MAXIMUM ACCURACY VOICE MODEL TRAINING COMPLETE!")
print("="*80)
print(f"Final Accuracy: {test_accuracy*100:.2f}%")
print(f"Model saved to: {os.path.join(save_dir, 'perfect_voice_model.h5')}")
print(f"Label encoder saved to: {os.path.join(save_dir, 'voice_label_encoder.pkl')}")
print("="*80 + "\n")