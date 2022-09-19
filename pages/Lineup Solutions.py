import streamlit as st
from st_aggrid import *

st.title('Fantasy Football Optimizer')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if 'summary_report' not in st.session_state:
    st.info('File Ingest has not been completed')
else:
    AgGrid(st.session_state['summary_report'], fit_columns_on_grid_load = True)