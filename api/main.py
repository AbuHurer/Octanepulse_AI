import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="OctanePulse AI - UFC Fight Predictor API",
    description="Real-time ML inference API for predicting UFC fight outcomes and win probabilities.",
    version="1.0.0"
)

# Global variable to hold the loaded model artifact
model_artifact = None

@app.on_event("startup")
def load_model():
    global model_artifact
    model_path = os.path.join("models", "fight_predictor_model.joblib")
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model artifact not found at {model_path}. Please run src/train.py first!")
    
    model_artifact = joblib.load(model_path)
    print("Model artifact loaded successfully into FastAPI!")

# Define Pydantic request body schema based on your features
class FightFeatures(BaseModel):
    height_diff: float
    weight_diff: float
    reach_diff: float
    slpm_diff: float
    str_acc_diff: float
    sapm_diff: float
    str_def_diff: float
    td_avg_diff: float
    td_acc_diff: float
    td_def_diff: float
    sub_avg_diff: float

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to OctanePulse AI API!"}

@app.post("/predict")
def predict_fight(features: FightFeatures):
    if model_artifact is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    try:
        model = model_artifact['model']
        feature_columns = model_artifact['feature_columns']
        
        # Convert incoming request to DataFrame matching training columns
        input_data = pd.DataFrame([features.dict()])[feature_columns]
        
        # Predict probability
        probabilities = model.predict_proba(input_data)[0]
        prediction = int(model.predict(input_data)[0])
        
        # probabilities[1] = Red Win Probability, probabilities[0] = Blue Win Probability
        red_win_prob = float(probabilities[1])
        blue_win_prob = float(probabilities[0])
        
        winner_name = "Red Corner" if prediction == 1 else "Blue Corner"
        
        return {
            "predicted_winner": winner_name,
            "red_win_probability": round(red_win_prob * 100, 2),
            "blue_win_probability": round(blue_win_prob * 100, 2),
            "confidence": round(max(red_win_prob, blue_win_prob) * 100, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))