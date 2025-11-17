import os
import sys
import pandas as pd
from flask import Flask, request, render_template, send_file, redirect, session, url_for
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.exception import CustomException
from src.database import insert_prediction
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.secret_key = 'secretKey'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

# Paths to model and preprocessor
MODEL_PATH = os.path.join("artifacts", "model.pkl")
PREPROCESSOR_PATH = os.path.join("artifacts", "preprocessor.pkl")

# Initialize the prediction pipeline
pipeline = PredictionPipeline(model_path=MODEL_PATH, preprocessor_path=PREPROCESSOR_PATH)


@app.route('/home')
def home():
    print(session)
    if 'name' in session:
        return render_template('index.html')
    return redirect("/login")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("HIIIIII LOGIN")
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid User")
    return render_template('login.html')
        
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print("HIIIIII REGISTER")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, password=password, email=email)

        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login'))

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == "POST":
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
            data_pred = df.to_dict(orient="records")
            
            return render_template("result.html", data=data_pred)
        

            # # Iterate through predictions and insert each into MySQL
            # for _, row in df.iterrows():
            #     record = (
            #         int(row["Age"]),
            #         row["BusinessTravel"],
            #         int(row["DailyRate"]),
            #         row["Department"],
            #         int(row["DistanceFromHome"]),
            #         int(row["Education"]),
            #         row["EducationField"],
            #         int(row["EnvironmentSatisfaction"]),
            #         row["Gender"],
            #         int(row["HourlyRate"]),
            #         int(row["JobInvolvement"]),
            #         int(row["JobLevel"]),
            #         row["JobRole"],
            #         int(row["JobSatisfaction"]),
            #         row["MaritalStatus"],
            #         float(row["MonthlyIncome"]),
            #         int(row["MonthlyRate"]),
            #         int(row["NumCompaniesWorked"]),
            #         row["OverTime"],
            #         int(row["PercentSalaryHike"]),
            #         int(row["PerformanceRating"]),
            #         int(row["RelationshipSatisfaction"]),
            #         int(row["StockOptionLevel"]),
            #         int(row["TotalWorkingYears"]),
            #         int(row["TrainingTimesLastYear"]),
            #         int(row["WorkLifeBalance"]),
            #         int(row["YearsAtCompany"]),
            #         int(row["YearsInCurrentRole"]),
            #         int(row["YearsSinceLastPromotion"]),
            #         int(row["YearsWithCurrManager"]),
            #         float(row["Attrition_Probability"]),        # from your model output
            #         row["Attrition_Prediction"]                 # from your model output
            #     )
            #     insert_prediction(record)

            # print("All predictions saved to MySQL successfully.")

            # Return the CSV with predictions for download
            # return send_file(output_file_path, as_attachment=True)

        except Exception as e:
            raise CustomException(e, sys)
    else:
        print(session)
        if 'name' in session:
            return redirect(url_for('home'))
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
