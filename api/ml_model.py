import joblib
import pandas as pd

def calculate(jsonValue):
    data = {
        'Red Freq': [jsonValue.red],
        'Green Freq': [jsonValue.green],
        'Blue Freq': [jsonValue.blue]
    }
    df = pd.DataFrame(data=data)
    model = joblib.load('model.joblib')
    result = model.predict(df)
    return result[0]