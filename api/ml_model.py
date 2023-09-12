# ml_model.py
import joblib
import os
import pandas as pd

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

    # Construct the path to the model.joblib file
    model_path = os.path.join(module_dir, 'ml_models', 'model.joblib')
    model = joblib.load(model_path)
    result = model.predict(df)
    return result[0]