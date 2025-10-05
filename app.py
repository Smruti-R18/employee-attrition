import os
import sys
import pandas as pd
from flask import Flask, request, render_template, send_file
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.exception import CustomException
from src.database import insert_prediction

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

        # Make predictions (returns path to output file)
        output_file_path = pipeline.predict_from_file(file_path)

        # Load the predicted CSV
        df = pd.read_csv(output_file_path)

        # Iterate through predictions and insert each into MySQL
        for _, row in df.iterrows():
            record = (
                int(row["Age"]),
                row["BusinessTravel"],
                int(row["DailyRate"]),
                row["Department"],
                int(row["DistanceFromHome"]),
                int(row["Education"]),
                row["EducationField"],
                int(row["EnvironmentSatisfaction"]),
                row["Gender"],
                int(row["HourlyRate"]),
                int(row["JobInvolvement"]),
                int(row["JobLevel"]),
                row["JobRole"],
                int(row["JobSatisfaction"]),
                row["MaritalStatus"],
                float(row["MonthlyIncome"]),
                int(row["MonthlyRate"]),
                int(row["NumCompaniesWorked"]),
                row["OverTime"],
                int(row["PercentSalaryHike"]),
                int(row["PerformanceRating"]),
                int(row["RelationshipSatisfaction"]),
                int(row["StockOptionLevel"]),
                int(row["TotalWorkingYears"]),
                int(row["TrainingTimesLastYear"]),
                int(row["WorkLifeBalance"]),
                int(row["YearsAtCompany"]),
                int(row["YearsInCurrentRole"]),
                int(row["YearsSinceLastPromotion"]),
                int(row["YearsWithCurrManager"]),
                float(row["Attrition_Probability"]),        # from your model output
                row["Attrition_Prediction"]                 # from your model output
            )
            insert_prediction(record)

        print("All predictions saved to MySQL successfully.")

        # Return the CSV with predictions for download
        return send_file(output_file_path, as_attachment=True)

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    app.run(debug=True)
