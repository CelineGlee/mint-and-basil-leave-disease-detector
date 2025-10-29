# Mint & Basil Leaves Disease Detector

A complete end-to-end machine learning application for detecting diseases in mint and basil plant leaves using computer vision and deep learning.

![Plant Disease Detection](https://img.shields.io/badge/TensorFlow-2.15.0-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![React Native](https://img.shields.io/badge/React%20Native-Expo-blue)
![Deployment](https://img.shields.io/badge/Deployed-Hugging%20Face-yellow)


## Table of Contents
- [Mint \& Basil Leaves Disease Detector](#mint--basil-leaves-disease-detector)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Technology Stack](#technology-stack)
    - [Machine Learning](#machine-learning)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [DevOps](#devops)
  - [How to Use](#how-to-use)
  - [Security Considerations](#security-considerations)
  - [Future Improvements](#future-improvements)
      - [1. Model Optimization \& Code Quality](#1-model-optimization--code-quality)
      - [2. Image Upload Functionality](#2-image-upload-functionality)
      - [3. Treatment Recommendations](#3-treatment-recommendations)
  - [Link](#link)


## Features

- **Real-time Disease Detection**: Capture mint or basil leaf images and get disease predictions
- **High Accuracy**: Deep learning model trained to classify plant health conditions
- **Mobile-First**: Native Android application built with React Native and Expo
- **Cloud Deployment**: Scalable API hosted on Hugging Face Spaces

The model can detect four conditions:
- **Healthy** - No visible symptoms, healthy plant leaf.
- **Leaf Spot** - No visible symptoms, healthy plant leaf.
- **Powdery** - Fungal disease causing white powdery spots
- **Rust** - Fungal disease causing orange/brown pustules

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA COLLECTION                              │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                       MODEL TRAINING PHASE                          │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ 1. Load Images                                              │    │
│  │ 2. Data Augmentation                                        │    │
│  │ 3. Transfer Learning (Xception pretrained on ImageNet)      │    │
│  │ 4. Initial Training                                         │    │
│  │ 5. Fine-tuning                                              │    │
│  │ 6. Export Model → plant_disease_model.h5                    │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND DEVELOPMENT PHASE                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ FastAPI Application                                         │    │
│  │  ├── Load model.h5                                          │    │
│  │  ├── Image preprocessing                                    │    │
│  │  ├── Model inference                                        │    │
│  │  └── Return prediction as JSON                              │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT PHASE                             │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Docker Container                                            │    │
│  │  ├── Python 3.9 + TensorFlow 2.15                           │    │
│  │  ├── FastAPI + Uvicorn                                      │    │
│  │  ├── OpenCV for preprocessing                               │    │
│  │  └── Exposed on port 7860                                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                             ↓                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ Hugging Face Spaces                                         │    │
│  │  ├── Git LFS for large model file                           │    │
│  │  ├── Automatic Docker build                                 │    │
│  │  └── Public URL: yuting270-plant-disease-detector.hf.space  │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    MOBILE APP INTEGRATION PHASE                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ React Native (Expo) Application                             │    │
│  │  ├── Camera Screen: Capture leaf image                      │    │
│  │  ├── Loading Screen: Show progress                          │    │
│  │  ├── API Call: POST image to backend                        │    │
│  │  └── Result Screen: Display prediction                      │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Machine Learning
- **Base Model**: Xception (ImageNet weights)

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Image Processing**: OpenCV 4.8.1, Pillow 10.1.0
- **ML Inference**: TensorFlow 2.15.0

### Frontend
- **Framework**: React Native (Expo)
- **Language**: TypeScript
- **HTTP Client**: Axios
- **Camera**: Expo Camera API

### DevOps
- **Containerization**: Docker
- **Version Control**: Git + Git LFS
- **Deployment**: Hugging Face Spaces
- **CI/CD**: Git-based auto-deployment

## How to Use
- Open the `android-apk-download` folder.
- Download the `application-1.0.0.apk` file to your Android device.
- Open the downloaded file and follow the installation instructions.
  
> ⚠️ Note: You may need to enable **“Install from unknown sources”** in your Android settings before installing the APK.

## Security Considerations

- API has CORS enabled for all origins (consider restricting in production)
- No authentication implemented (add JWT tokens for production)
- Input validation on file uploads
- Timeout limits on requests

## Future Improvements

#### 1. Model Optimization & Code Quality
- [ ] Experiment with newer architectures (EfficientNet, Vision Transformer)
- [ ] Implement ensemble methods for better accuracy
- [ ] Optimize inference speed and model size

#### 2. Image Upload Functionality
- [ ] Add image upload feature to mobile app

#### 3. Treatment Recommendations
- [ ] Disease-specific treatment advice

## Link

- **API Endpoint**: https://yuting270-plant-disease-detector.hf.space
- **HuggingFace Account**：https://huggingface.co/Yuting270

---

💚 🌱 *Developed by Yuting — combining AI, computer vision, and mobile app development for practical agricultural insights.*