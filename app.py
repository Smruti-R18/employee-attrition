import os
import sys
from flask import Flask, request, render_template, send_file
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.exception import CustomException

app = Flask(__name__)

# Paths to model and preprocessor
MODEL_PATH = os.path.join("artifacts", "model.pkl")
PREPROCESSOR_PATH = os.path.join("artifacts", "preprocessor.pkl")

# Initialize the prediction pipeline
pipeline = PredictionPipeline(model_path=MODEL_PATH, preprocessor_path=PREPROCESSOR_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return "No file part in the request"

        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        # Save uploaded CSV temporarily
        upload_folder = "uploads"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Make predictions
        output_file_path = pipeline.predict_from_file(file_path)

        # Return the CSV with predictions for download
        return send_file(output_file_path, as_attachment=True)

    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    app.run(debug=True)
