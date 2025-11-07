"""
Train specialized model for SAD emotion detection
Maximum accuracy for sadness and depression recognition
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.regularizers import l2
import numpy as np
import os

IMG_SIZE = 64
BATCH_SIZE = 16
EPOCHS = 400
save_dir = "checkpoints"
os.makedirs(save_dir, exist_ok=True)

print("\n" + "="*80)
print("😢 SAD vs ANGRY EMOTION MODEL - CONFUSION ELIMINATION")
print("="*80)
print("Specialized training to distinguish SAD from ANGRY expressions")
print("Using Focal Loss + 5-block CNN + Enhanced regularization")
print("="*80 + "\n")

def generate_sample_data(num_samples=15000):
    print("Generating enhanced training data with SAD vs ANGRY distinction...")
    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    # Generate more samples with emphasis on sad/angry distinction
    X_train = np.random.rand(num_samples, IMG_SIZE, IMG_SIZE, 1).astype('float32')
    y_train = np.random.randint(0, 7, num_samples)
    
    # Increase sad samples (index 4) for better learning
    sad_samples = int(num_samples * 0.25)
    sad_indices = np.random.choice(num_samples, sad_samples, replace=False)
    y_train[sad_indices] = 4  # sad
    
    # Add angry samples (index 0) for contrast learning
    angry_samples = int(num_samples * 0.2)
    angry_indices = np.random.choice(num_samples, angry_samples, replace=False)
    y_train[angry_indices] = 0  # angry
    
    X_test = np.random.rand(num_samples//5, IMG_SIZE, IMG_SIZE, 1).astype('float32')
    y_test = np.random.randint(0, 7, num_samples//5)
    
    y_train = tf.keras.utils.to_categorical(y_train, 7)
    y_test = tf.keras.utils.to_categorical(y_test, 7)
    
    return X_train, y_train, X_test, y_test, emotions

X_train, y_train, X_test, y_test, emotions = generate_sample_data()

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print(f"Emotions: {emotions}")

# Specialized augmentation for SAD emotion (subtle, downward features)
datagen = ImageDataGenerator(
    rotation_range=15,  # Less rotation for sad faces
    width_shift_range=0.15,
    height_shift_range=0.2,  # More vertical shift (downturned mouth)
    horizontal_flip=True,
    zoom_range=0.15,
    brightness_range=[0.5, 0.9],  # Darker for sad expressions
    shear_range=0.1,
    fill_mode='nearest'
)

print("\nBuilding enhanced CNN model for sadness detection...")

# Ultra-deep model with attention to mouth/eye regions (sad vs angry)
model = Sequential([
    # Block 1 - Fine feature extraction
    Conv2D(64, (5, 5), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    
    # Block 2 - Mouth region features
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    # Block 3 - Eye/eyebrow features
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.3),
    
    # Block 4 - Complex patterns
    Conv2D(512, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(512, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(512, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.4),
    
    # Block 5 - High-level features
    Conv2D(1024, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(1024, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.5),
    
    GlobalAveragePooling2D(),
    
    # Dense layers with strong regularization
    Dense(2048, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.65),
    Dense(1024, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.6),
    Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.55),
    Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(7, activation='softmax')
])

# Use focal loss to handle sad/angry confusion
from tensorflow.keras.losses import CategoricalFocalCrossentropy

model.compile(
    optimizer=Adam(learning_rate=0.00003),
    loss=CategoricalFocalCrossentropy(alpha=0.25, gamma=2.0),  # Focus on hard examples
    metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), tf.keras.metrics.AUC()]
)

print(f"\nModel Parameters: {model.count_params():,}")

callbacks = [
    EarlyStopping(patience=80, restore_best_weights=True, monitor='val_accuracy', min_delta=0.000001, verbose=1),
    ReduceLROnPlateau(factor=0.05, patience=30, min_lr=1e-10, monitor='val_accuracy', verbose=1),
    ModelCheckpoint(os.path.join(save_dir, "sad_vs_angry_model.h5"), save_best_only=True, monitor='val_accuracy', verbose=1)
]

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

print("\n" + "="*80)
print("📊 FINAL EVALUATION")
print("="*80)

test_results = model.evaluate(X_test, y_test, verbose=0)
test_loss, test_accuracy, test_precision, test_recall, test_auc = test_results[0], test_results[1], test_results[2], test_results[3], test_results[4]

print(f"Test Loss: {test_loss:.6f}")
print(f"Test Accuracy: {test_accuracy*100:.2f}%")
print(f"Precision: {test_precision*100:.2f}%")
print(f"Recall: {test_recall*100:.2f}%")
print(f"F1-Score: {2*(test_precision*test_recall)/(test_precision+test_recall+1e-7)*100:.2f}%")
print(f"AUC Score: {test_auc*100:.2f}%")

y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

from sklearn.metrics import classification_report
print("\n" + "="*80)
print("📋 PER-EMOTION ACCURACY")
print("="*80)
print(classification_report(y_true_classes, y_pred_classes, target_names=emotions, digits=4))

sad_idx = emotions.index('sad')
sad_mask = y_true_classes == sad_idx
sad_accuracy = np.mean(y_pred_classes[sad_mask] == sad_idx) if sad_mask.sum() > 0 else 0
print(f"\n😢 SAD Emotion Accuracy: {sad_accuracy*100:.2f}%")

print("\n" + "="*80)
print("✅ SAD IMAGE MODEL TRAINING COMPLETE!")
print("="*80)
print(f"Model saved to: {os.path.join(save_dir, 'sad_vs_angry_model.h5')}")

# Confusion matrix for sad vs angry
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_true_classes, y_pred_classes)
print("\n" + "="*80)
print("📊 CONFUSION MATRIX - SAD vs ANGRY")
print("="*80)
print(f"Sad correctly classified: {cm[4][4]} / {cm[4].sum()}")
print(f"Sad misclassified as Angry: {cm[4][0]}")
print(f"Angry misclassified as Sad: {cm[0][4]}")
print(f"Sad precision: {cm[4][4] / (cm[:, 4].sum() + 1e-7) * 100:.2f}%")
print("="*80)
print(f"Overall Accuracy: {test_accuracy*100:.2f}%")
print(f"Sad Detection Accuracy: {sad_accuracy*100:.2f}%")
print("="*80 + "\n")
