"""
Train specialized model for ANGRY emotion detection
Maximum accuracy for facial expression recognition
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.regularizers import l2
import numpy as np
import os

# Configuration
IMG_SIZE = 48
BATCH_SIZE = 32
EPOCHS = 150
save_dir = "checkpoints"
os.makedirs(save_dir, exist_ok=True)

print("\n" + "="*80)
print("😠 ANGRY EMOTION IMAGE MODEL TRAINING")
print("="*80)
print("Specialized model for detecting angry facial expressions")
print("="*80 + "\n")

# Generate synthetic training data (replace with real dataset)
def generate_sample_data(num_samples=5000):
    """Generate synthetic facial expression data"""
    print("Generating sample training data...")
    
    # 7 emotions: angry, disgust, fear, happy, sad, surprise, neutral
    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    X_train = np.random.rand(num_samples, IMG_SIZE, IMG_SIZE, 1).astype('float32')
    y_train = np.random.randint(0, 7, num_samples)
    
    X_test = np.random.rand(num_samples//5, IMG_SIZE, IMG_SIZE, 1).astype('float32')
    y_test = np.random.randint(0, 7, num_samples//5)
    
    # Convert to categorical
    y_train = tf.keras.utils.to_categorical(y_train, 7)
    y_test = tf.keras.utils.to_categorical(y_test, 7)
    
    return X_train, y_train, X_test, y_test, emotions

# Load data
X_train, y_train, X_test, y_test, emotions = generate_sample_data()

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print(f"Emotions: {emotions}")
print(f"Image size: {IMG_SIZE}x{IMG_SIZE}")

# Data augmentation for better generalization
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    shear_range=0.2,
    fill_mode='nearest'
)

# Build enhanced CNN model
print("\nBuilding enhanced CNN model...")

model = Sequential([
    # Block 1
    Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # Block 2
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # Block 3
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.3),
    
    # Block 4
    Conv2D(512, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(512, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.4),
    
    # Global pooling
    GlobalAveragePooling2D(),
    
    # Dense layers
    Dense(1024, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.5),
    Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.4),
    Dense(7, activation='softmax')
])

# Compile model
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
)

print(f"\nModel Parameters: {model.count_params():,}")
print("Architecture: Deep CNN with BatchNorm & Dropout")

# Callbacks
callbacks = [
    EarlyStopping(patience=30, restore_best_weights=True, monitor='val_accuracy', verbose=1),
    ReduceLROnPlateau(factor=0.2, patience=10, min_lr=1e-7, monitor='val_accuracy', verbose=1),
    ModelCheckpoint(
        os.path.join(save_dir, "angry_image_model.h5"),
        save_best_only=True,
        monitor='val_accuracy',
        verbose=1
    )
]

# Train model
print("\n" + "="*80)
print("🚀 STARTING TRAINING")
print("="*80 + "\n")

history = model.fit(
    datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
    validation_data=(X_test, y_test),
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1
)

# Evaluate
print("\n" + "="*80)
print("📊 FINAL EVALUATION")
print("="*80)

test_results = model.evaluate(X_test, y_test, verbose=0)
test_loss = test_results[0]
test_accuracy = test_results[1]
test_precision = test_results[2]
test_recall = test_results[3]

print(f"Test Loss: {test_loss:.6f}")
print(f"Test Accuracy: {test_accuracy*100:.2f}%")
print(f"Precision: {test_precision*100:.2f}%")
print(f"Recall: {test_recall*100:.2f}%")
print(f"F1-Score: {2*(test_precision*test_recall)/(test_precision+test_recall+1e-7)*100:.2f}%")

# Per-class accuracy (focus on angry)
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

from sklearn.metrics import classification_report
print("\n" + "="*80)
print("📋 PER-EMOTION ACCURACY")
print("="*80)
print(classification_report(y_true_classes, y_pred_classes, target_names=emotions, digits=4))

# Angry emotion specific metrics
angry_idx = emotions.index('angry')
angry_mask = y_true_classes == angry_idx
angry_accuracy = np.mean(y_pred_classes[angry_mask] == angry_idx) if angry_mask.sum() > 0 else 0
print(f"\n😠 ANGRY Emotion Accuracy: {angry_accuracy*100:.2f}%")

print("\n" + "="*80)
print("✅ ANGRY IMAGE MODEL TRAINING COMPLETE!")
print("="*80)
print(f"Model saved to: {os.path.join(save_dir, 'angry_image_model.h5')}")
print(f"Overall Accuracy: {test_accuracy*100:.2f}%")
print(f"Angry Detection Accuracy: {angry_accuracy*100:.2f}%")
print("="*80 + "\n")
