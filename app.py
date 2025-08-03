import streamlit as st
import joblib
import numpy as np

# Load model and feature list
model = joblib.load("model.pkl")
features_list = joblib.load("features.pkl")

st.set_page_config(page_title="Employee Attrition Predictor", layout="centered")

st.title("🏢 Employee Attrition Prediction App")
st.markdown("This app predicts whether an employee is likely to leave the company based on various factors.")

# Mapping dictionaries
education_levels = {
    "Below College": 1, "College": 2,
    "Bachelor’s Degree": 3, "Master’s Degree": 4, "Doctorate": 5
}
satisfaction_levels = {
    "Low": 1, "Medium": 2, "High": 3, "Very High": 4
}
worklife_balance = {
    "Bad": 1, "Good": 2, "Better": 3, "Best": 4
}
yes_no = {
    "No": 0, "Yes": 1
}

label_maps = {
    "BusinessTravel": {
        "Non-Travel": 0, "Travel_Rarely": 1, "Travel_Frequently": 2
    },
    "Department": {
        "Sales": 2, "Research & Development": 1, "Human Resources": 0
    },
    "Gender": {
        "Female": 0, "Male": 1
    },
    "JobRole": {
        "Healthcare Representative": 0, "Human Resources": 1,
        "Laboratory Technician": 2, "Manager": 3, "Manufacturing Director": 4,
        "Research Director": 5, "Research Scientist": 6,
        "Sales Executive": 7, "Sales Representative": 8
    },
    "MaritalStatus": {
        "Divorced": 0, "Married": 1, "Single": 2
    }
}

# Sidebar inputs for all necessary features
st.sidebar.header("📋 Enter Employee Details")

inputs = {
    'Age': st.sidebar.slider("Age", 18, 60, 30),
    'BusinessTravel': label_maps['BusinessTravel'][
        st.sidebar.selectbox("Business Travel", list(label_maps['BusinessTravel'].keys()))],
    'DailyRate': st.sidebar.slider("Daily Rate", 100, 1500, 800),
    'Department': label_maps['Department'][st.sidebar.selectbox("Department", list(label_maps['Department'].keys()))],
    'DistanceFromHome': st.sidebar.slider("Distance From Home", 1, 50, 10),
    'Education': education_levels[st.sidebar.selectbox("Education Level", list(education_levels.keys()))],
    'EducationField': st.sidebar.selectbox("Education Field",
                                           ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree',
                                            'Human Resources', 'Other']),
    'EnvironmentSatisfaction': satisfaction_levels[
        st.sidebar.selectbox("Environment Satisfaction", list(satisfaction_levels.keys()))],
    'Gender': label_maps['Gender'][st.sidebar.selectbox("Gender", list(label_maps['Gender'].keys()))],
    'HourlyRate': st.sidebar.slider("Hourly Rate", 30, 100, 50),
    'JobInvolvement': st.sidebar.slider("Job Involvement (1-4)", 1, 4, 3),
    'JobLevel': st.sidebar.slider("Job Level", 1, 5, 2),
    'JobRole': label_maps['JobRole'][st.sidebar.selectbox("Job Role", list(label_maps['JobRole'].keys()))],
    'JobSatisfaction': satisfaction_levels[st.sidebar.selectbox("Job Satisfaction", list(satisfaction_levels.keys()))],
    'MaritalStatus': label_maps['MaritalStatus'][
        st.sidebar.selectbox("Marital Status", list(label_maps['MaritalStatus'].keys()))],
    'MonthlyIncome': st.sidebar.number_input("Monthly Income", 1000, 50000, 7000),
    'MonthlyRate': st.sidebar.slider("Monthly Rate", 1000, 30000, 15000),
    'NumCompaniesWorked': st.sidebar.slider("Number of Companies Worked", 0, 10, 2),
    'OverTime': yes_no[st.sidebar.selectbox("OverTime", list(yes_no.keys()))],
    'PercentSalaryHike': st.sidebar.slider("Percent Salary Hike", 10, 25, 15),
    'PerformanceRating': st.sidebar.slider("Performance Rating", 1, 4, 3),
    'RelationshipSatisfaction': satisfaction_levels[
        st.sidebar.selectbox("Relationship Satisfaction", list(satisfaction_levels.keys()))],
    'StockOptionLevel': st.sidebar.slider("Stock Option Level", 0, 3, 1),
    'TotalWorkingYears': st.sidebar.slider("Total Working Years", 0, 40, 10),
    'TrainingTimesLastYear': st.sidebar.slider("Training Times Last Year", 0, 6, 3),
    'WorkLifeBalance': worklife_balance[st.sidebar.selectbox("Work Life Balance", list(worklife_balance.keys()))],
    'YearsAtCompany': st.sidebar.slider("Years at Company", 0, 40, 5),
    'YearsInCurrentRole': st.sidebar.slider("Years in Current Role", 0, 20, 3),
    'YearsSinceLastPromotion': st.sidebar.slider("Years Since Last Promotion", 0, 15, 1),
    'YearsWithCurrManager': st.sidebar.slider("Years with Current Manager", 0, 20, 3)
}

# Manual encoding for EducationField
education_field_map = {
    'Life Sciences': 1, 'Medical': 4, 'Marketing': 3,
    'Technical Degree': 5, 'Human Resources': 0, 'Other': 2
}
inputs['EducationField'] = education_field_map[inputs['EducationField']]

# Prepare input row in correct feature order
input_row = [inputs[feature] for feature in features_list]

# Predict
if st.button("🔮 Predict"):
    prediction = model.predict([input_row])
    confidence = model.predict_proba([input_row])[0][prediction[0]] * 100
    confidence_text = f"📊 Assurance Level of Prediction: {confidence:.2f}%"

    if prediction[0] == 1:
        st.error(f"⚠️ The employee is likely to leave the company.\n\n*{confidence_text}*")
    else:
        st.success(f"✅ The employee is likely to stay in the company.\n\n*{confidence_text}*")

