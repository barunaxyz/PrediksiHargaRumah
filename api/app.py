from flask import Flask, request, jsonify
import pandas as pd
import util as utils
import joblib
import os

app = Flask(__name__)

# Load config and model
config_path = utils.get_config_path()
config = utils.load_params(config_path)
model_path = utils.get_model_path(config)
model = utils.pickle_load(model_path)

import data_preparation
import preprocessing
# Helper needed for pickle loading if it uses classes from these modules

@app.route('/')
def home():
    return "House Price Prediction API is Up!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data_json = request.get_json()
        
        # Expecting input keys matching the predictors
        predictors = config['prediktor'] # LB, LT, KT, KM, GRS
        
        # Ensure all predictors are present
        input_data = {}
        missing_fields = []
        for p in predictors:
            if p not in data_json:
                missing_fields.append(p)
            else:
                input_data[p] = [data_json[p]]
        
        if missing_fields:
             return jsonify({"error": f"Missing features: {missing_fields}"}), 400

        # Create DataFrame
        df = pd.DataFrame(input_data)
        
        # Ensure correct data types (int64)
        for p in predictors:
            df[p] = df[p].astype('int64')

        # Validate data
        try:
           data_preparation.cek_data(df, config, True)
        except AssertionError as ae:
            return jsonify({"status": "error", "message": f"Validation Error: {str(ae)}"}), 400

        # Predict
        prediction = model.predict(df)
        
        # Result
        result = prediction[0]
        
        return jsonify({
            "status": "success",
            "prediction": float(result)
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
