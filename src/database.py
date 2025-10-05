import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='Smruti',              # your MySQL username
            password='Smruti@2005',  # your MySQL password
            database='employee_attrition'
        )
        return connection
    except Error as e:
        print(f"MySQL connection error: {e}")
        return None


def insert_prediction(record):
    """
    record: tuple containing (Age, BusinessTravel, ..., YearsWithCurrManager, AttritionProbability, RecommendedAction)
    """
    connection = get_connection()
    if not connection:
        print("DB connection failed. Record not saved.")
        return

    insert_query = """
    INSERT INTO employee (
        Age, BusinessTravel, DailyRate, Department, DistanceFromHome, Education, EducationField,
        EnvironmentSatisfaction, Gender, HourlyRate, JobInvolvement, JobLevel, JobRole, JobSatisfaction,
        MaritalStatus, MonthlyIncome, MonthlyRate, NumCompaniesWorked, OverTime, PercentSalaryHike,
        PerformanceRating, RelationshipSatisfaction, StockOptionLevel, TotalWorkingYears, TrainingTimesLastYear,
        WorkLifeBalance, YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion, YearsWithCurrManager,
        AttritionProbability, AttritionPrediction
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """

    cursor = connection.cursor()
    cursor.execute(insert_query, record)
    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Prediction record saved to MySQL.")
