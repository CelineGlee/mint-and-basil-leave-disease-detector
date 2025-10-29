from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from PIL import Image
import numpy as np
import tempfile
import io
import os
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model when service starts
model_path = os.path.join(os.path.dirname(__file__), "plant_disease_model.h5")

try:
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully from:", model_path)
except Exception as e:
    print("Failed to load model:", e)

class_names = [ 'Healthy', 'Leaf Spot', 'Powdery', 'Rust', ]
img_size = (299, 299)

def load_and_preprocess_image(image_path, img_size=img_size):
    """Load and preprocess a single image"""
    img = tf.keras.preprocessing.image.load_img(
        image_path,
        target_size=img_size
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    return img_array

def predict_single_image(model, file_bytes):
    """Predict class for a single image"""

    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name
    try:
        # Preprocess
        img_array = load_and_preprocess_image(temp_path, img_size=img_size)

        # Predict
        predictions = model.predict(img_array, verbose=0)
    
        # Apply softmax to convert logits to probabilities
        predicted_class = tf.argmax(predictions[0])

        return {"predicted_class": class_names[predicted_class]}
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/")
async def health_check(): 
    """Health check endpoint."""
    return {"message": "Plant Disease Detection API", "status": "healthy"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Receive image upload from frontend and return prediction."""
    try:
        file_bytes = await file.read()
        result = predict_single_image(model, file_bytes)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )