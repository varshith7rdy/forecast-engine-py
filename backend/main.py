from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from predictions import make_pred
from decide_action import action



class PredictionRequest(BaseModel):
    query: str

app = FastAPI(title="Time Series Prediction API")

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path, html=True), name="static")


@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

@app.post("/predict")
def predict_orders(request: PredictionRequest):

    try:

        print("Request data:", request.query)
        result = action(request.query)
        return result
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {"error": f"Failed to process request: {str(e)}", "chartdata": {}}
