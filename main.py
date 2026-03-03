from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from predictions import make_pred



class PredictionRequest(BaseModel):
    restaurant_id: int
    target_date: str  # "YYYY-MM-DD"
    promo_flag: int = 0

app = FastAPI(title="Time Series Prediction API")


@app.get("/")
def home():
    return {"message": "Churn Prediction API is live!"}

@app.post("/predict")
def predict_orders(request: PredictionRequest):
    print("Request data:", request)
    return make_pred(request)
