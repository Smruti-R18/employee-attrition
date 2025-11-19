# src/recommendation.py

def safe_num(row, key, default=0):
    try:
        v = row.get(key, default)
        if v is None or v == "":
            return default
        return float(v)
    except:
        return default

def safe_str(row, key, default=""):
    v = row.get(key)
    if v is None:
        return default
    return str(v).strip()

def generate_recommendation(row, probability):
    """
    Returns:
        display_id (str)
        risk_level (str)
        recommendations (list)
    """

    # ----------------------------
    # 1) Employee ID (simple)
    # ----------------------------
    if "EmployeeNumber" in row:
        display_id = str(row["EmployeeNumber"])
    elif "EmployeeID" in row:
        display_id = str(row["EmployeeID"])
    else:
        display_id = f"EMP-{hash(str(row)) % 100000}"  # fallback mini ID

    # ----------------------------
    # 2) Risk Category
    # ----------------------------
    if probability >= 0.75:
        risk = "High"
    elif probability >= 0.40:
        risk = "Medium"
    else:
        risk = "Low"

    # ----------------------------
    # 3) Recommendations
    # ----------------------------
    recs = []

    income = safe_num(row, "MonthlyIncome", 0)
    if income < 3000:
        recs.append("Increase salary by 10–15%")
    elif income < 5000:
        recs.append("Increase salary by around 5%")
    else:
        recs.append("Salary is fine — consider non-monetary benefits")

    # Overtime
    if safe_str(row, "OverTime", "").lower() == "yes":
        recs.append("Reduce overtime workload")

    # Job satisfaction
    if safe_num(row, "JobSatisfaction", 3) <= 2:
        recs.append("Schedule a one-on-one discussion for improvement")

    # Tenure
    if safe_num(row, "YearsAtCompany", 0) < 2:
        recs.append("Assign mentorship / onboarding support")

    # Performance
    if safe_num(row, "PerformanceRating", 3) <= 2:
        recs.append("Provide performance coaching")

    # Role
    role = safe_str(row, "JobRole", "")
    if role:
        recs.append(f"Discuss growth opportunities for role: {role}")

    return display_id, risk, recs
