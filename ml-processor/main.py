import pandas as pd
import joblib
import numpy as np
import time
from Data import Data
from Model import Model
from DataScaler import DataScaler
from contextlib import asynccontextmanager
from fastapi import FastAPI

model_instance = None
scaler = None

def read_data(input):
    df = pd.read_csv(input, delimiter=';')
    data = np.array(df.values[: , 2:], dtype = float)
    return data

def ModelInit():
    data = read_data('trainning_data.csv')
    model_instance = Model()
    scaler = DataScaler()
    input = data[:, 1:]
    output = data[:, 0]
    X_train, X_test, y_train, y_test = model_instance.split_data(input, output)
    Xt_train = scaler.fit_transform(X_train)
    model_instance.fit_model(Xt_train, y_train)
    joblib.dump(model_instance, 'ML-model.pkl')
    joblib.dump(scaler, 'custom_transformer.pkl')

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_instance, scaler
    try:
        model_instance = joblib.load('ML-model.pkl')
        scaler = joblib.load('custom_transformer.pkl')
    except FileNotFoundError:
        print("Model initialization")
        ModelInit()
    yield
    print("Shutting down the ML models and releasing resources")
    

app = FastAPI(lifespan=lifespan)    

@app.post("/data")
async def predict(data: Data):
    global model_instance, scaler
    while (scaler == None or model_instance == None):
        time.sleep(1)
    # Convert input data to a dictionary for prediction
    df = pd.DataFrame(data.model_dump(), index=[0])
    
    df2 = df.drop(columns=df.columns[:4])
    data2 = np.array(df2, dtype = float)

    
    # Make scaling and predictions using the model
    data3 = scaler.transform(data2)

    data.activity = int (model_instance.predict(data3))
    
    # Return predictions
    return data


"""
uvicorn main:app --reload
Result = 0
{
   "acceleration_x": 0.2650,
   "acceleration_y": -0.7814,
   "acceleration_z": -0.0076,
   "gyro_x": -0.0590,
   "gyro_y": 0.0325,
   "gyro_z": -2.9296
}

Result = 1
{
  "acceleration_x": -0.4418,
  "acceleration_y": 0.3335,
  "acceleration_z": -0.3227,
  "gyro_x": 0.0139,
  "gyro_y": -0.6016,
  "gyro_z": -0.1992
}

Result = 1
{
  "acceleration_x": 0.1,
  "acceleration_y": 0.2,
  "acceleration_z": 0.3,
  "gyro_x": 0.1,
  "gyro_y": 0.2,
  "gyro_z": 0.3
}

Result = 0
{
   "acceleration_x": 0.0658,
   "acceleration_y": -1.0527,
   "acceleration_z": -0.2025,
   "gyro_x": 0.6859,
   "gyro_y": -0.0266,
   "gyro_z": 0.4760
}


"""