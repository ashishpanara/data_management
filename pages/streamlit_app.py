import streamlit as st

# Set page configuration

match_page = st.Page("01_matching.py", title="Data Matching", icon=":material/add_circle:")
profile_page = st.Page("02_profiling.py", title="Data Profiling", icon=":material/add_circle:")

pg = st.navigation([match_page, profile_page])
st.set_page_config(page_title="Data Quality Check Automation")
pg.run()