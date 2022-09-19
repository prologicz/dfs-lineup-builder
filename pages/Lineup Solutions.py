import streamlit as st
from st_aggrid import *
from reports import draftKingsAllLineups, summaryReport

st.title('Fantasy Football Optimizer')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if 'solutions' not in st.session_state:
    st.info('File Ingest has not been completed')
else:
    summary_report = summaryReport(st.session_state['data'], st.session_state['solutions'])
    AgGrid(summary_report, fit_columns_on_grid_load = True)

    lineups = draftKingsAllLineups(st.session_state['data'], st.session_state['solutions'])
    csv = lineups.to_csv(index=False)

    st.sidebar.title('Data Download')
    st.sidebar.download_button(
        label = 'Download Draftkings File',
        data = csv,
        file_name='dk_all_lineups.csv'
    )