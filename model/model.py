import numpy as np
import matplotlib.pyplot as plt
import keras
import tensorflow as tf
import os
import cv2

from matplotlib import pyplot
from PIL import Image
from tensorflow.keras import layers
from tensorflow import data as tf_data
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

gpus = tf.config.list_physical_devices("GPU")
if gpus:
    for gpu in gpus:
            print("Found a GPU with the name:", gpu)
else:
    print("Failed to detect a GPU.")

# define image parameters Xception
batch_size = 32
img_size = (299, 299)

# datasets dir
train_dir = "./Train/Train"
valid_dir = "./Validation/Validation"
test_dir = "./Test/Test"

# Load train dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    shuffle=True,
    image_size=img_size,
    batch_size=batch_size,
)

# Load valid dataset
valid_ds = tf.keras.utils.image_dataset_from_directory(
    valid_dir,
    image_size=img_size,
    batch_size=batch_size,
    shuffle=True
)

# Load test dataset
test_ds= tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=img_size,
    batch_size=batch_size,
    shuffle=False
)

# horizontal flip, rotate, and brightness adjust
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"), 
    tf.keras.layers.RandomRotation(0.3),                   
    tf.keras.layers.RandomZoom(0.2),                               
    tf.keras.layers.RandomBrightness(0.3),                  
    tf.keras.layers.RandomContrast(0.3),                              
    tf.keras.layers.GaussianNoise(0.1),
    tf.keras.layers.RandomTranslation(0.2, 0.2), 
])

# Apply `data_augmentation` to the training images.
train_dataset = train_ds.map(
    lambda image, label: (data_augmentation(image), label),
    num_parallel_calls=tf_data.AUTOTUNE,
)

train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
test_dataset = test_ds.prefetch(tf_data.AUTOTUNE)
validation_dataset = valid_ds.prefetch(tf_data.AUTOTUNE)

# base model using Xception model
img_shape = img_size + (3,)

Xcp_base_model = tf.keras.applications.Xception(input_shape=img_shape,
                                               include_top=False,
                                               weights='imagenet',
)

# Freeze the base_model
Xcp_base_model.trainable = False

# Early stopping to prevent overfitting
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=7,
    restore_best_weights=True,
    verbose=1
)

# Build a model
num_classes = 4

inputs = keras.Input(shape=(299, 299, 3))

x = keras.layers.Rescaling(scale=1 / 127.5, offset=-1)(inputs) # Normalization 

x = Xcp_base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.5)(x)
x = tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.02))(x)
x = tf.keras.layers.Dropout(0.3)(x) # avoid overfitting

outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
Xcp_model = tf.keras.Model(inputs, outputs)

#Xcp_model.summary(show_trainable=True)

# compile model
base_learning_rate = 1e-4
initial_epochs = 20

Xcp_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy'],
)

# train model
history = Xcp_model.fit(train_dataset, epochs=initial_epochs, callbacks=early_stop, validation_data=validation_dataset)

# fine-tuning

# unfreeze
Xcp_base_model.trainable = True

# Freeze all layers except the last 20
for layer in Xcp_base_model.layers[:-20]:
    layer.trainable = False

# compile model
Xcp_model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy'],
)

# Continue training the model
fine_tune_epochs = 20
total_epochs =  initial_epochs + fine_tune_epochs # 30

history_fine = Xcp_model.fit(train_dataset,
                        epochs=total_epochs,
                        callbacks=early_stop,
                        initial_epoch=len(history.epoch),
                        validation_data=validation_dataset)

print("Test dataset evaluation")
Xcp_model.evaluate(test_dataset)

class_names = train_ds.class_names

# Retrieve a batch of images from the test set
image_batch, label_batch = test_dataset.as_numpy_iterator().next()

predictions = Xcp_model.predict_on_batch(image_batch)
predicted_classes = tf.argmax(predictions, axis=1)

print('Predicted Classes:\n', predicted_classes.numpy())
print('True Labels:\n', label_batch)

plt.figure(figsize=(10, 10))
for i in range(9):
  ax = plt.subplot(3, 3, i + 1)
  plt.imshow(image_batch[i].astype("uint8"))

  pred_class = predicted_classes[i].numpy()
  confidence = predictions[i][pred_class] * 100

  plt.title(f"{class_names[pred_class]}\n{confidence:.1f}%")
  plt.axis("off")

# each image read
# process each image
# predict these image using the model

own_image_folder_path = "./own_test_samples"

def load_and_preprocess_image(image_path, img_size=img_size):
    """Load and preprocess a single image"""
    img = tf.keras.preprocessing.image.load_img(
        image_path,
        target_size=img_size)

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    return img_array

def predict_single_image(model, image_path, class_names):
    """Predict class for a single image"""

    # Preprocess
    img_array = load_and_preprocess_image(image_path)
    
    # Predict
    predictions = model.predict(img_array, verbose=0)

    # Apply softmax to convert logits to probabilities
    predicted_class = tf.argmax(predictions[0])
    confidence = predictions[0][predicted_class] * 100

    return predicted_class, confidence, predictions[0]

# Get all images from folder
image_files = [f for f in os.listdir(own_image_folder_path) 
               if f.lower().endswith('.jpg')]

# Predict on all images
results = []
for image_file in image_files:
    image_path = os.path.join(own_image_folder_path, image_file)
    pred_class, confidence, probabilities = predict_single_image(Xcp_model, image_path, class_names)

    results.append({
        'filename': image_file,
        'predicted_class': class_names[pred_class],
        'confidence': confidence,
        'probabilities': probabilities
    })

    print(f"{image_file}: {class_names[pred_class]} ({confidence:.2f}%)")

# Visualization of result
num_images = len(image_files)
cols = 3
rows = (num_images + cols - 1) // cols

plt.figure(figsize=(15, 5 * rows))

for i, image_file in enumerate(image_files):
    image_path = os.path.join(own_image_folder_path, image_file)
    
    # Load original image for display
    img = Image.open(image_path)
    
    # Get prediction
    result = results[i]
    
    # Plot
    ax = plt.subplot(rows, cols, i + 1)
    plt.imshow(img)
    
    title = f"{result['predicted_class']}\n"
    title += f"Confidence: {result['confidence']:.1f}%"
    
    plt.title(title, fontsize=12, fontweight='bold')
    plt.axis('off')

plt.tight_layout()
plt.savefig('predictions_results.png', dpi=150, bbox_inches='tight')
plt.show()