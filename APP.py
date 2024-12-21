import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

# SQL Server connection using SQLAlchemy
def get_connection():
    try:
        conn_str = 'mssql+pyodbc://DESKTOP-58MFL3I\\SQLEXPRESS/EmployeeDB?driver=ODBC+Driver+17+for+SQL+Server'
        engine = create_engine(conn_str)
        return engine
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to load data from SQL
def load_data():
    engine = get_connection()
    if engine:
        try:
            query = "SELECT * FROM EmployeeProfiles"
            return pd.read_sql(query, engine)
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return pd.DataFrame()  # Return empty DataFrame if connection fails

# Function to add new data into SQL
def add_new_data(name, department, salary, experience_years, performance_score):
    engine = get_connection()
    if engine:
        query = """
        INSERT INTO EmployeeProfiles (Name, Department, Salary, ExperienceYears, PerformanceScore)
        VALUES (:name, :department, :salary, :experience_years, :performance_score)
        """
        try:
            with engine.connect() as conn:
                conn.execute(text(query), {
                    'name': name,
                    'department': department,
                    'salary': salary,
                    'experience_years': experience_years,
                    'performance_score': performance_score
                })
            st.success("New data added successfully!")
        except Exception as e:
            st.error(f"Error adding data: {e}")

# Load data
data = load_data()

# --- Interactive Key Insights ---
st.subheader("🔑 Interactive Key Insights")
insight_option = st.selectbox("Select an Insight to Explore", 
                              ["Department Distribution", "Salary Insights", "Experience and Salary", "Salary Distribution", "Show Raw Data"])

# Show Raw Data option
if insight_option == "Show Raw Data":
    st.write("### Raw Employee Data")
    st.dataframe(data)

# Based on the user's selection, show the relevant insight.
elif insight_option == "Department Distribution":
    st.write("### Department Distribution")
    if not data.empty:
        dept_counts = data['Department'].value_counts()
        fig1 = px.pie(values=dept_counts, names=dept_counts.index, title="Employee Distribution by Department", hole=0.3)
        st.plotly_chart(fig1)
    else:
        st.warning("No data available to show department distribution.")
    
elif insight_option == "Salary Insights":
    st.write("### Salary Insights")
    if not data.empty:
        avg_salary = data.groupby('Department')['Salary'].mean().sort_values()
        fig2 = px.bar(x=avg_salary.index, y=avg_salary.values, title="Average Salary by Department", labels={'x': 'Department', 'y': 'Average Salary'})
        st.plotly_chart(fig2)
    else:
        st.warning("No data available for salary insights.")
    
elif insight_option == "Experience and Salary":
    st.write("### Experience vs. Salary")
    if not data.empty:
        fig3 = px.scatter(data, x='ExperienceYears', y='Salary', size='PerformanceScore', color='PerformanceScore', 
                          hover_name='Name', title="Experience vs. Salary vs. Performance")
        st.plotly_chart(fig3)
    else:
        st.warning("No data available for experience vs. salary visualization.")

elif insight_option == "Salary Distribution":
    st.write("### Salary Distribution")
    if not data.empty:
        plt.figure(figsize=(10,6))
        sns.histplot(data['Salary'], kde=True, color='skyblue', bins=20)
        st.pyplot(plt)
    else:
        st.warning("No data available to show salary distribution.")

# --- Add New Data ---
st.subheader("🖊️ Add New Employee Data")

with st.form(key='new_data_form'):
    name = st.text_input("Employee Name")
    department = st.selectbox("Department", data['Department'].unique() if not data.empty else ["Underwater Basket Weaving"])
    salary = st.number_input("Salary", min_value=30000, max_value=200000, step=1000)
    experience_years = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
    performance_score = st.slider("Performance Score", min_value=1, max_value=5, step=1)
    
    submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        if name and department and salary and experience_years is not None:
            add_new_data(name, department, salary, experience_years, performance_score)
        else:
            st.warning("Please fill in all fields before submitting.")
