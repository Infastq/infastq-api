from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
label = {
    "1000":0,
    "2000":1,
    "5000":2,
    "10000":3,
    "20000":4,
    "50000":5,
    "100000":6
}

# Create a custom LabelEncoder class
class CustomLabelEncoder(LabelEncoder):
    def __init__(self, label_dict):
        self.label_dict = label_dict
        super().__init__()

    def fit(self, y):
        super().fit(y)
        self.classes_ = [self.label_dict[label] for label in self.classes_]

    def transform(self, y):
        return super().transform(y)

    def inverse_transform(self, y):
        y_original = [list(self.label_dict.keys())[list(self.label_dict.values()).index(encoded)] for encoded in y]
        return y_original
    
# custom_label_encoder = CustomLabelEncoder(label)
# module_dir = os.path.dirname(__file__)
# path = os.path.join(module_dir, 'data_uang_gemastik.xlsx')
# df = pd.read_excel(path)
# encoded = custom_label_encoder.fit_transform(df['value'])