import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import *
from linuep_builder import *
from streamlit_extras.switch_page_button import switch_page

st.title('Fantasy Football Optimizer')

st.subheader('Generator Settings')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



if 'remap_data' in st.session_state:
    st.subheader('Select Number of Lineups')
    numberOfLineups = st.slider('Numer Of Lineups', min_value=1, max_value=150, value=20, label_visibility='collapsed')

    st.subheader('Select QBs For Stacks')
    st.write('If specific stacks are not required, no selection should be made')
    remap_data = pd.DataFrame(st.session_state['remap_data'])
    quarterbacks = remap_data[remap_data['position'] == 'QB']
    gd = GridOptionsBuilder.from_dataframe(quarterbacks)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gridoptions = gd.build()

    grid_table = AgGrid(quarterbacks, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED, fit_columns_on_grid_load = True)


    selected_row = grid_table['selected_rows']
    qb_selections = []

    for row in range(len(selected_row)):
        qb = selected_row[row]['key']
        qb_selections.append(qb)
    
    if (len(qb_selections) > 0):
        final_quarterbacks = quarterbacks[quarterbacks['key'].isin(qb_selections)]
        remap_data = remap_data.drop(remap_data[remap_data.position == 'QB'].index)
        remap_data = remap_data.append(final_quarterbacks)



    run_button = st.button('Generate Lineups', key='generateLineups')
    if run_button:
        with st.spinner('Generating Lineups'):
            solutions = lineupBuilder(remap_data, numberOfLineups)
            st.session_state['solutions'] = solutions
            switch_page('Lineup Solutions')

else:
    st.info('Data Ingest Not Complete')


if 'solutions' in st.session_state:
    lineupSolutionsButton = st.button('View Lineups >>')
    if lineupSolutionsButton:
        switch_page('Lineup Solutions')