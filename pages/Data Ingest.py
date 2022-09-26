import streamlit as st
import pandas as pd
from support_functions import *
from st_aggrid import *
from linuep_builder import *
from reports import *
from streamlit_extras.switch_page_button import switch_page

st.title('Fantasy Football Optimizer')

st.sidebar.title('File Upload')
uploaded_file = st.sidebar.file_uploader("")


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


try:
    st.session_state['uploaded_file'] = uploaded_file
    df = pd.read_csv(uploaded_file)
    st.session_state['df'] = df
except:
    st.write('')



st.subheader('Ingest Data Preview')
try:
    ingest_data = uploadInitalFile(st.session_state['df'])
    st.session_state['ingest_data'] = ingest_data
    AgGrid(st.session_state['ingest_data'].head(10), fit_columns_on_grid_load = True)

    column_labels = st.session_state['ingest_data'].columns
    column_labels = column_labels.insert(0, '-')

except:
    st.info('Please Upload File')


try:
    st.sidebar.title('Column Mapping')
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.write('Target Field')
        new_col_name_key = st.text_input("Key", value="key", key= "key", disabled=True)
        new_col_name_name = st.text_input("Name", value="name", key= "name", disabled=True)
        new_col_name_position = st.text_input("Position", value="position", key= "position", disabled=True)            
        new_col_name_salary = st.text_input("Salary", value="salary", key= "salary", disabled=True)
        new_col_name_points = st.text_input("Points", value="points", key= "points", disabled=True)
        new_col_name_team = st.text_input("Team", value="team", key= "team", disabled=True)
        new_col_name_opponent = st.text_input("Opponent", value="opponent", key= "opponent", disabled=True)
    with col2:
        st.write('CSV Header')
        col_to_change_key = st.selectbox("Select Column", column_labels, key="keyChange")
        col_to_change_name = st.selectbox("Select Column", column_labels, key="nameChange")
        col_to_change_position = st.selectbox("Select Column", column_labels, key="namePosition")
        col_to_change_salary = st.selectbox("Select Column", column_labels, key="salaryChange")
        col_to_change_points = st.selectbox("Select Column", column_labels, key="pointsChange")
        col_to_change_team = st.selectbox("Select Column", column_labels, key="teamChange")
        col_to_change_opponent= st.selectbox("Select Column", column_labels, key="opponentChange")
        

    submit_button = st.sidebar.button(label='Map Columns')

    if submit_button:
        remap_data = pd.DataFrame()
        remap_data[new_col_name_key] = ingest_data[col_to_change_key]
        remap_data[new_col_name_name] = ingest_data[col_to_change_name]
        remap_data[new_col_name_position] = ingest_data[col_to_change_position]
        remap_data[new_col_name_salary] = ingest_data[col_to_change_salary]
        remap_data[new_col_name_points] = ingest_data[col_to_change_points]
        remap_data[new_col_name_team] = ingest_data[col_to_change_team]
        remap_data[new_col_name_opponent] = ingest_data[col_to_change_opponent]
        st.session_state['remap_data'] = remap_data
except:
    st.write('')



st.subheader('Remap Data Preview')

try: 
    AgGrid(st.session_state['remap_data'].head(10), fit_columns_on_grid_load = True)

except:
    st.info('Please Map Columns')


if 'remap_data' in st.session_state:
    lineupConfigurationButton = st.button('Generator Settings >>')
    if lineupConfigurationButton:
        switch_page('Generator Settings')








