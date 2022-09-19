import streamlit as st
import pandas as pd
from support_functions import *
from st_aggrid import *
from linuep_builder import *
from reports import *

st.title('Fantasy Football Optimizer')

st.sidebar.title('Data Ingest')
uploaded_file = st.sidebar.file_uploader("Choose a file")


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if uploaded_file is None:
    st.info(' Please Upload File')

else:
    df = pd.read_csv(uploaded_file)

    try:
        data = uploadInitalFile(df)
    except:
        st.info(' Please Upload File')


    st.subheader('Column Mapping')

    column_labels = data.columns
    column_labels = column_labels.insert(0, '-')
    try:
        col1, col2 = st.columns(2)
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
            

        submit_button = st.button(label='Submit')

        if submit_button:
            data = data.rename(columns={col_to_change_key: new_col_name_key, 
                                        col_to_change_name: new_col_name_name,
                                        col_to_change_position: new_col_name_position,
                                        col_to_change_salary: new_col_name_salary,
                                        col_to_change_points: new_col_name_points,
                                        col_to_change_team: new_col_name_team,
                                        col_to_change_opponent: new_col_name_opponent})
            remove_data_headers = [new_col_name_key, new_col_name_name, new_col_name_position, new_col_name_salary, new_col_name_points, new_col_name_team, new_col_name_opponent]
            data = data.drop(columns = [col for col in data if col not in remove_data_headers])

    except:
        st.write('issue')

    st.subheader('Data Preview')

    try: 
        AgGrid(data.head(5), fit_columns_on_grid_load = True)
    except:
        st.write('issue')


    try:
        solutions = lineupBuilder(data) 
        lineups_file = draftKingsAllLineups(data, solutions)
        st.session_state['lineups_file'] = lineups_file
    except:
        st.write('')



