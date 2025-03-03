from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  # Allows requests from any origin (change to specific domains if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Load your model
model = load_model('Road_Sign_Model_resnet.h5')

label_mapping = {
    0: 'SPEED LIMIT 20', 
    1: 'SPEED LIMIT 30', 
    2: 'STOP', 
    3: 'SPEED LIMIT 50', 
    4: 'SPEED-LIMIT-60', 
    5: 'SPEED LIMIT 70', 
    6: 'SPEED-LIMIT-80', 
    7: 'SPEED LIMIT 100', 
    8: 'SPEED LIMIT 120'
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Road Sign Classification API"}

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    # Read the uploaded file as bytes
    img_bytes = await file.read()

    # Convert bytes to an image using OpenCV
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (96, 96))  # Resize to the model's input size
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img = img.astype('float32') / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Predict the label
    prediction = model.predict(img)
    predicted_label = np.argmax(prediction, axis=1)[0]  # Get the class index

    # Map the predicted label to the actual class name
    predicted_label_name = label_mapping[predicted_label]

    return {"predicted_label": predicted_label_name}
