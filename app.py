from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import pandas as pd
import sys

# Load environment variables
load_dotenv()

# Configure generative AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    # Combine the prompt and question into a single string
    combined_prompt = prompt[0] + "\n" + question
    response = model.generate_content(combined_prompt)
    return response.text

def read_sql_query(sql, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    con.commit()
    con.close()
    return rows

def add_data_to_db(dataframe, db):
    con = sqlite3.connect(db)
    try:
        dataframe.to_sql('STUDENT', con, if_exists='append', index=False)
        st.success("Data added to the database successfully!")
    except Exception as e:
        st.error(f"An error occurred while adding data: {e}")
    finally:
        con.close()

# Initialize Streamlit app
st.set_page_config(page_title="LLM_with_sql")
st.header("Gemini App To Retrieve SQL Data" )

# Prompt for SQL conversion
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit input
question = st.text_input("Input: ", key="input")
submit_query = st.button("Ask the question")

# Execute query if button is clicked
if submit_query:
    response_sql = get_gemini(question, prompt)
    st.subheader("Generated SQL Query")
    st.write(response_sql)  # Show the generated SQL query

    try:
        # Execute the SQL query
        rows = read_sql_query(response_sql, "student.db")
        st.subheader("The Response is")
        for row in rows:
            st.write(row)
    except Exception as e:
        st.write("An error occurred:", e)

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file to add data to the database", type=["xlsx"])

if uploaded_file:
    # Read the Excel file into a DataFrame
    dataframe = pd.read_excel(uploaded_file)
    st.write("Preview of uploaded data:", dataframe.head())  # Display preview of data

    # Add button to insert data into the database
    if st.button("Add data to database"):
        add_data_to_db(dataframe, "student.db")
