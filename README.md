# Gemini SQL Query Generator and Database Interface

This is a Streamlit-based application that uses Google Gemini (Generative AI) to convert English-language questions into SQL queries. It also allows users to upload data from an Excel file to a SQLite database and retrieve results based on generated SQL queries.

## Features

- Converts natural language questions into SQL queries using Google Gemini.
- Executes generated SQL queries on an SQLite database named `STUDENT`.
- Allows users to upload Excel files and insert data directly into the SQLite database.
- Displays the results of executed queries within the Streamlit interface.

## Setup

### Prerequisites

1. **Python**: Make sure Python 3.7 or higher is installed on your system.
2. **Google Gemini API Key**: Obtain an API key for Google Gemini and set it in an environment variable named `GOOGLE_API_KEY`.
3. **SQLite Database**: The app uses an SQLite database (`student.db`). Ensure this file is in your working directory or create one with a table structure matching the app requirements.

### Environment Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
