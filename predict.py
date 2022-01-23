import pickle
import pandas as pd
from flask import Flask


df_final = pd.read_pickle("df_evaluate.pickle")
model_file = 'RandomForestRegressor.pickle'
with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)



app = Flask(__name__, template_folder="template")

@app.route('/predict', methods=['POST'])
def predict():
    X = df_final.drop('fare_amount', axis=1)
    y = df_final['fare_amount']
   
    return f'The train accurcay of linear regression model is {model.score(X,y)}'


            
if __name__ == "__main__":
    app.run(debug=True,  port=9696)