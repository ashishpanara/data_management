
# Import libraries
from nbformat import write
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np 
import ydata_profiling
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport

# Database name
db = "college.db"

# Function to get table names from the SQLite3 database
def get_table_names(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    sql_source_tables = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(sql_source_tables)
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]

    conn.close()
    return tables

# Function to read sql query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql, conn)
    conn.commit()
    conn.close()
    return df

# Add a header
st.header(":orange[Data Profiling]")

# Choose table names
with st.container():
    st.subheader(':red[Select Table for Data Profiling]')
    tables = get_table_names(db)
    selected_table = st.selectbox("Select Table: ", tables)
    # st.write(f":orange[Selected Table:] {selected_table}")

    sql = f'SELECT * FROM {selected_table}'
    df = read_sql_query(sql, db)
    st.write(df)

    if st.button('Generate Profile Report'):
        profile = ProfileReport(df, title = "Summary of Data")
        st_profile_report(profile)
