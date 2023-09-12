# ml_model.py
import joblib
import os
import pandas as pd
import xgboost as xgb
import numpy as np
from .ml_models.label import CustomLabelEncoder, label
def calculate(red, green, blue):
    data = {
        'red_freq': [red],
        'green_freq': [green],
        'blue_freq': [blue],
        'r-g': [abs(red-green)],
        'r-b':[abs(red-blue)],
        'g-b':[abs(green-blue)]
    }
    df = pd.DataFrame(data=data)
    module_dir = os.path.dirname(__file__)
    data_matrix = xgb.DMatrix(data=df)
    # Construct the path to the model.joblib file
    # model_path = os.path.join(module_dir, 'ml_models', 'model.joblib')
    model_path = os.path.join(module_dir, 'ml_models', 'xgboost_model.bin')
    model = xgb.XGBClassifier(model_file=model_path)
    model_json = os.path.join(module_dir, 'ml_models', 'xgboost_model.json')
    model.load_model(model_json)

    # model = joblib.load(model_path)
    # result = model.predict(df)
    result = model.predict(data_matrix)
    decoded_result = CustomLabelEncoder(label).inverse_transform(result[0])

    return decoded_result[0]