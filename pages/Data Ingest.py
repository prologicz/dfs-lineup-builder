import streamlit as st
import pandas as pd
from support_functions import *
from st_aggrid import *
from linuep_builder import *
from reports import *

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
        remap_data = ingest_data.rename(columns={col_to_change_key: new_col_name_key, 
                                    col_to_change_name: new_col_name_name,
                                    col_to_change_position: new_col_name_position,
                                    col_to_change_salary: new_col_name_salary,
                                    col_to_change_points: new_col_name_points,
                                    col_to_change_team: new_col_name_team,
                                    col_to_change_opponent: new_col_name_opponent})
        remove_remap_data_headers = [new_col_name_key, new_col_name_name, new_col_name_position, new_col_name_salary, new_col_name_points, new_col_name_team, new_col_name_opponent]
        remap_data = remap_data.drop(columns = [col for col in remap_data if col not in remove_remap_data_headers])
        st.session_state['remap_data'] = remap_data
except:
    st.write('')






st.subheader('Remap Data Preview')

try: 
    AgGrid(st.session_state['remap_data'].head(10), fit_columns_on_grid_load = True)
except:
    st.info('Please Map Columns')


if 'remap_data' in st.session_state:
    run_button = st.button('Generate Lineups', key='generateLineups')
    if run_button:
        with st.spinner('Generating Lineups'):
            solutions = lineupBuilder(st.session_state['remap_data'], 50)
            st.session_state['solutions'] = solutions








