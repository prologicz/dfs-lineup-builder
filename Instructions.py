import streamlit as st
import pandas as pd
from support_functions import *
from st_aggrid import *
from linuep_builder import *
from reports import *

st.set_page_config(
    page_title='Instructions'
)
st.title('Fantasy Football Optimizer')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
