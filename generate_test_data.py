import pandas as pd
import numpy as np

# Define columns after dropping
columns = [
    'Age','BusinessTravel', 'DailyRate', 'Department', 'DistanceFromHome',
    'Education', 'EducationField', 'EnvironmentSatisfaction', 'Gender',
    'HourlyRate','JobInvolvement', 'JobLevel', 'JobRole', 'JobSatisfaction',
    'MaritalStatus', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
    'OverTime', 'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
    'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
    'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager'
]

# Number of rows
n_rows = 10

# Generate synthetic data
np.random.seed(42)
data = {
    'Age': np.random.randint(18, 60, size=n_rows),
    'BusinessTravel': np.random.choice(['Travel_Rarely', 'Travel_Frequently', 'Non-Travel'], size=n_rows),
    'DailyRate': np.random.randint(100, 1500, size=n_rows),
    'Department': np.random.choice(['Sales', 'Research & Development', 'Human Resources'], size=n_rows),
    'DistanceFromHome': np.random.randint(1, 30, size=n_rows),
    'Education': np.random.randint(1, 5, size=n_rows),
    'EducationField': np.random.choice(['Life Sciences', 'Other', 'Medical', 'Marketing', 'Technical Degree'], size=n_rows),
    'EnvironmentSatisfaction': np.random.randint(1, 5, size=n_rows),
    'Gender': np.random.choice(['Male', 'Female'], size=n_rows),
    'JobInvolvement': np.random.randint(1, 5, size=n_rows),
    'JobLevel': np.random.randint(1, 5, size=n_rows),
    'JobRole': np.random.choice(['Sales Executive', 'Research Scientist', 'Laboratory Technician', 'Manufacturing Director','Manager','Healthcare Representative'], size=n_rows),
    'JobSatisfaction': np.random.randint(1, 5, size=n_rows),
    'MaritalStatus': np.random.choice(['Single', 'Married', 'Divorced'], size=n_rows),
    'MonthlyIncome': np.random.randint(2000, 20000, size=n_rows),
    'MonthlyRate': np.random.randint(1000, 20000, size=n_rows),
    'NumCompaniesWorked': np.random.randint(0, 10, size=n_rows),
    'OverTime': np.random.choice(['Yes', 'No'], size=n_rows),
    'PercentSalaryHike': np.random.randint(10, 25, size=n_rows),
    'PerformanceRating': np.random.randint(1, 5, size=n_rows),
    'RelationshipSatisfaction': np.random.randint(1, 5, size=n_rows),
    'StockOptionLevel': np.random.randint(0, 3, size=n_rows),
    'TotalWorkingYears': np.random.randint(0, 40, size=n_rows),
    'TrainingTimesLastYear': np.random.randint(0, 6, size=n_rows),
    'WorkLifeBalance': np.random.randint(1, 5, size=n_rows),
    'YearsAtCompany': np.random.randint(0, 30, size=n_rows),
    'YearsInCurrentRole': np.random.randint(0, 15, size=n_rows),
    'YearsSinceLastPromotion': np.random.randint(0, 10, size=n_rows),
    'YearsWithCurrManager': np.random.randint(0, 15, size=n_rows),
}

# Create DataFrame
df_test = pd.DataFrame(data, columns=columns)

# Save CSV
df_test.to_csv("synthetic_test_hr.csv", index=False)
print("Synthetic test CSV created: synthetic_test_hr.csv")
