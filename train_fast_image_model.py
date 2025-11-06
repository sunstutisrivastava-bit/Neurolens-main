import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
import os

train_dir = "models/images"
save_dir = "checkpoints"
os.makedirs(save_dir, exist_ok=True)

# Fast parameters
img_size = (128, 128)
batch_size = 32

# Minimal augmentation for speed
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    validation_split=0.2
)

val_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_gen = train_datagen.flow_from_directory(
    train_dir, target_size=img_size, batch_size=batch_size, subset="training"
)

val_gen = val_datagen.flow_from_directory(
    train_dir, target_size=img_size, batch_size=batch_size, subset="validation"
)

# Fast base model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
base_model.trainable = True

# Simple architecture
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(train_gen.num_classes, activation='softmax')
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [EarlyStopping(patience=3, restore_best_weights=True)]

print("Training fast model (under 5 minutes)...")
model.fit(train_gen, validation_data=val_gen, epochs=10, callbacks=callbacks, verbose=1)

model.save(os.path.join(save_dir, "fast_image_model.h5"))
val_loss, val_accuracy = model.evaluate(val_gen)
print(f"Validation accuracy: {val_accuracy:.4f}")
print("SUCCESS: Fast training complete!")