from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
import pandas as pd
from .model import DelayModel

app = FastAPI()
model = DelayModel()

test_data = pd.DataFrame([
    {"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 3},
    {"OPERA": "Aerolineas Argentinas", "TIPOVUELO": "N", "MES": 5}
])
features = model.preprocess(test_data)
target = pd.DataFrame({'delay': [0, 1]})
model.fit(features, target)

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

    @validator('MES')
    def validate_month(cls, v):
        if not 1 <= v <= 12:
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
        return v

    @validator('TIPOVUELO')
    def validate_flight_type(cls, v):
        if v not in ['N', 'I']:
            raise HTTPException(status_code=400, detail="Flight type must be 'N' or 'I'")
        return v

    @validator('OPERA')
    def validate_operator(cls, v):
        valid_operators = [
            "Aerolineas Argentinas",
            "Grupo LATAM",
            "Sky Airline",
            "Copa Air",
            "Latin American Wings"
        ]
        if v not in valid_operators:
            raise HTTPException(status_code=400, detail="Invalid operator")
        return v

class PredictRequest(BaseModel):
    flights: List[Flight]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK",
        "model_trained": model._model is not None
    }

@app.post("/predict", status_code=200)
async def post_predict(data: PredictRequest) -> dict:
    try:
        df = pd.DataFrame([flight.dict() for flight in data.flights])
        features = model.preprocess(df)
        predictions = model.predict(features)
        return {"predict": predictions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))