from fastapi import FastAPI, HTTPException, Request
import joblib
import numpy as np
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend access (Adjust origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for security reasons in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler with error handling
try:
    model = joblib.load("random_forest_model.pkl")
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    model, scaler = None, None  # Ensure API fails gracefully if models aren't loaded

# Define input schema with validation
class InputData(BaseModel):
    features: list[float] = Field(..., min_items=1, description="List of numerical features for prediction")

@app.post("/predict")
async def predict(request: Request, data: InputData):
    """Predict endpoint to make model predictions."""
    
    # Debugging: Print received raw JSON for troubleshooting
    raw_body = await request.body()
    print("Received Raw JSON:", raw_body.decode())  # Logs request payload
    
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or scaler not loaded properly")

    try:
        # Convert input data to numpy array
        input_array = np.array(data.features).reshape(1, -1)

        # Apply scaling
        input_scaled = scaler.transform(input_array)

        # Make prediction
        prediction = model.predict(input_scaled)

        return {"prediction": str(prediction[0])}  # Convert to string for consistency
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/")
def home():
    """Root endpoint to check if the API is running."""
    return {"message": "API is running!"}
