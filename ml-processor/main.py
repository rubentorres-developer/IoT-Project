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
        try:
            model_instance = joblib.load('ML-model.pkl')
            scaler = joblib.load('custom_transformer.pkl')
        except FileNotFoundError:
            print("Model initialization")
            ModelInit()
    # Convert input data to a dictionary for prediction
    df = pd.DataFrame(data.model_dump(), index=[0])
    
    new_df = df.drop(columns=df.columns[:4])
    np_data = np.array(new_df, dtype = float)

    np_data = scaler.transform(np_data)

    data.activity = int (model_instance.predict(np_data))

    return data
