from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import xgboost as xgb
from tensorflow.keras.models import load_model

# 1. Define request schema
class PredictRequest(BaseModel):
    features: list[float]  # your feature vector (e.g. [feature1, feature2, day_of_week, ..., event_type_counts])

# 2. Initialize FastAPI app
app = FastAPI(title="Churn Prediction API")

# 3. Load trained models (make sure you’ve saved them to disk)
lstm_model = load_model("models/lstm.h5")
xgb_model = xgb.Booster()
xgb_model.load_model("models/xgb.model")

@app.post("/predict")
def predict(req: PredictRequest):
    # Convert features to array
    X = np.array(req.features, dtype=float).reshape(1, -1)
    # LSTM expects shape (batch, timesteps, features)
    X_seq = X.reshape((1, 1, X.shape[1]))
    # Get LSTM probability
    lstm_pred = float(lstm_model.predict(X_seq)[0, 0])
    # Stack LSTM output with original features for XGBoost
    combined = np.hstack([lstm_pred, X.flatten()]).reshape(1, -1)
    dmat = xgb.DMatrix(combined)
    xgb_pred = float(xgb_model.predict(dmat)[0])
    return {"churn_probability": xgb_pred}

