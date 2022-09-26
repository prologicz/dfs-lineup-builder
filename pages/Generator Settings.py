import streamlit as st
from linuep_builder import *
from streamlit_extras.switch_page_button import switch_page

st.title('Fantasy Football Optimizer')

st.subheader('Generator Settings')



if 'remap_data' in st.session_state:
    numberOfLineups = st.slider('Number of lineups:', min_value=1, max_value=150, value=20)
    run_button = st.button('Generate Lineups', key='generateLineups')
    if run_button:
        with st.spinner('Generating Lineups'):
            solutions = lineupBuilder(st.session_state['remap_data'], numberOfLineups)
            st.session_state['solutions'] = solutions

else:
    st.info('Data Ingest Not Complete')


if 'solutions' in st.session_state:
    lineupSolutionsButton = st.button('View Lineups >>')
    if lineupSolutionsButton:
        switch_page('Lineup Solutions')