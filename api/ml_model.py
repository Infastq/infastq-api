import joblib
import pandas as pd

def calculate(red, green, blue):
    data = {
        'Red Freq': [red],
        'Green Freq': [green],
        'Blue Freq': [blue]
    }
    df = pd.DataFrame(data=data)
    model = joblib.load('model.joblib')
    result = model.predict(df)
    return result[0]