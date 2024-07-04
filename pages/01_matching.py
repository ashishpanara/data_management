
# Import libraries
import streamlit as st
import os
import sqlite3
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

###############################################################################################################################
# Database name, source table name and target table name
db = "college.db"

###############################################################################################################################
# Function to read sql query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql, conn)
    conn.commit()
    conn.close()
    return df

# Function to get table names from the SQLite3 database
def get_table_names(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    sql_source_tables = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%source%';"
    cursor.execute(sql_source_tables)
    source_tables = cursor.fetchall()
    source_tables = [table[0] for table in source_tables]

    sql_target_tables = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%target%';"
    cursor.execute(sql_target_tables)
    target_tables = cursor.fetchall()
    target_tables = [table[0] for table in target_tables]

    conn.close()
    return source_tables, target_tables

# Function to check the schema match between source table and target table
def check_schema_match(db, source_table, target_table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    st.subheader(':red[Schema Match]')
    col1, col2 = st.columns(2)

    with col1:
        st.write(f":orange[Source Schema:]")
        source_sql = f'PRAGMA table_info({source_table})'
        source_df = read_sql_query(source_sql, db)
        st.write(source_df)

    with col2:
        st.write(f":orange[Target Schema:]")
        target_sql = f'PRAGMA table_info({target_table})'
        target_df = read_sql_query(target_sql, db)
        st.write(target_df)

    merged_df = pd.merge(source_df, target_df, how='outer', indicator=True)
    df_diff = merged_df[merged_df['_merge'] != 'both']
    df_diff = df_diff.rename(columns={'_merge': '_table'})
    df_diff['_table'] = df_diff['_table'].replace({'left_only': 'source', 'right_only': 'target'})
    df_diff = df_diff[['_table'] + [col for col in df_diff.columns if col != '_table']]
    df_diff = df_diff.reset_index(drop=True)

    df_diff_source = df_diff[df_diff['_table'] == 'source']
    df_diff_target = df_diff[df_diff['_table'] == 'target']

    df_diff_source = df_diff_source.drop('_table', axis=1).reset_index(drop = True)
    df_diff_target = df_diff_target.drop('_table', axis=1).reset_index(drop = True)

    conn.close()
    
    return df_diff_source, df_diff_target, len(df_diff) == 0

# Function to check the record count match between source table and target table
def check_count_match(db, source_table, target_table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(f'SELECT COUNT(*) FROM {source_table}')
    source_count = cursor.fetchone()[0]

    cursor.execute(f'SELECT COUNT(*) FROM {target_table}')
    target_count = cursor.fetchone()[0]

    st.subheader(':red[Count Match]')
    col1, col2 = st.columns(2)

    with col1:
        st.write(f":orange[Source Count:] {source_count}")

    with col2:
        st.write(f":orange[Target Count:] {target_count}")

    conn.close()

    return source_count, target_count, source_count == target_count

# Function to check the data match between source table and target table
def check_data_match(db, source_table, target_table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    st.subheader(':red[Data Match]')
    col1, col2 = st.columns(2)

    with col1:
        st.write(f":orange[Source Data:]")
        source_sql = f'SELECT * FROM {source_table}'
        source_df = read_sql_query(source_sql, db)
        st.write(source_df)

    with col2:
        st.write(f":orange[Target Data:]")
        target_sql = f'SELECT * FROM {target_table}'
        target_df = read_sql_query(target_sql, db)
        st.write(target_df)

    merged_df = pd.merge(source_df, target_df, how='outer', indicator=True)
    df_diff = merged_df[merged_df['_merge'] != 'both']
    df_diff = df_diff.rename(columns={'_merge': '_table'})
    df_diff['_table'] = df_diff['_table'].replace({'left_only': 'source', 'right_only': 'target'})
    df_diff = df_diff[['_table'] + [col for col in df_diff.columns if col != '_table']]
    df_diff = df_diff.reset_index(drop=True)

    df_diff_source = df_diff[df_diff['_table'] == 'source']
    df_diff_target = df_diff[df_diff['_table'] == 'target']

    df_diff_source = df_diff_source.drop('_table', axis=1).reset_index(drop = True)
    df_diff_target = df_diff_target.drop('_table', axis=1).reset_index(drop = True)

    conn.close()
    
    return df_diff_source, df_diff_target, len(df_diff) == 0

###############################################################################################################################
## Streamlit App - UI

# Add a header
st.header(":orange[Data Matching]")

# Choose table names
with st.container():
    st.subheader(':red[Select Tables for Data Matching]')
    source_tables, target_tables = get_table_names(db)
    col1, col2 = st.columns(2)
    with col1:
        selected_source_table = st.selectbox("Choose Source Table: ", source_tables)
        st.write(f":orange[Source Table:] {selected_source_table}")
    with col2:
        selected_target_table = st.selectbox("Choose Target Table: ", target_tables)
        st.write(f":orange[Target Table:] {selected_target_table}")

# Check schema match
with st.container():
    df_diff_source, df_diff_target, schema_match = check_schema_match(db, selected_source_table, selected_target_table)

    if schema_match:
        st.success("Source table schema and target table schema match!")
    else:
        st.error("Source table schema and target table schema do not match!")
        st.write(":red[Schema that did not match:]")
        col1, col2 = st.columns(2)
        with col1:
            st.write(df_diff_source)
        with col2:
            st.write(df_diff_target)

# Check count match
with st.container():
    source_count, target_count, count_match = check_count_match(db, selected_source_table, selected_target_table)
    if count_match:
        st.success("Counts in source table and target table match!")
    else:
        st.error("Counts in source table and target table do not match!")

# Check data match
with st.container():
    df_diff_source, df_diff_target, data_match = check_data_match(db, selected_source_table, selected_target_table)
    if data_match:
        st.success("Data in source table matches data in target table!")
    else:
        st.error("Data in source table does not match data in target table!")
        st.write(":red[Data that did not match:]")
        col1, col2 = st.columns(2)
        with col1:
            st.write(df_diff_source)
        with col2:
            st.write(df_diff_target)
