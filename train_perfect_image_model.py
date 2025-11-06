import tensorflow as tf
from tensorflow.keras.applications import EfficientNetV2B3
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import AdamW
from tensorflow.keras.regularizers import l2
import os

# Paths
train_dir = "models/images"
save_dir = "checkpoints"
os.makedirs(save_dir, exist_ok=True)

# Parameters for maximum accuracy
img_size = (300, 300)
batch_size = 8

# Extreme data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.4,
    height_shift_range=0.4,
    horizontal_flip=True,
    vertical_flip=True,
    zoom_range=0.4,
    shear_range=0.3,
    brightness_range=[0.7, 1.3],
    channel_shift_range=0.2,
    fill_mode='reflect',
    validation_split=0.15
)

val_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.15)

train_gen = train_datagen.flow_from_directory(
    train_dir, target_size=img_size, batch_size=batch_size, subset="training"
)

val_gen = val_datagen.flow_from_directory(
    train_dir, target_size=img_size, batch_size=batch_size, subset="validation"
)

# State-of-the-art base model
base_model = EfficientNetV2B3(weights='imagenet', include_top=False, input_shape=(300, 300, 3))
base_model.trainable = False

# Advanced architecture
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(1024, activation='relu', kernel_regularizer=l2(0.001))(x)
x = Dropout(0.6)(x)
x = BatchNormalization()(x)
x = Dense(512, activation='relu', kernel_regularizer=l2(0.001))(x)
x = Dropout(0.5)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(train_gen.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Advanced optimizer
model.compile(
    optimizer=AdamW(learning_rate=0.001, weight_decay=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy', 'top_k_categorical_accuracy']
)

# Aggressive callbacks
callbacks = [
    EarlyStopping(patience=25, restore_best_weights=True, monitor='val_accuracy'),
    ReduceLROnPlateau(factor=0.1, patience=10, min_lr=1e-8, monitor='val_accuracy'),
    ModelCheckpoint(os.path.join(save_dir, "perfect_image_model.h5"), save_best_only=True, monitor='val_accuracy')
]

print("Phase 1: Initial training...")
history1 = model.fit(train_gen, validation_data=val_gen, epochs=50, callbacks=callbacks)

# Fine-tuning
print("Phase 2: Fine-tuning all layers...")
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

model.compile(
    optimizer=AdamW(learning_rate=0.0001, weight_decay=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history2 = model.fit(train_gen, validation_data=val_gen, epochs=100, callbacks=callbacks)

# Final fine-tuning
print("Phase 3: Ultra fine-tuning...")
for layer in base_model.layers:
    layer.trainable = True

model.compile(
    optimizer=AdamW(learning_rate=0.00001, weight_decay=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history3 = model.fit(train_gen, validation_data=val_gen, epochs=50, callbacks=callbacks)

val_loss, val_accuracy = model.evaluate(val_gen)
print(f"Final validation accuracy: {val_accuracy:.6f}")
print("✅ Perfect image model training complete!")