from distutils.command.upload import upload
import streamlit as st
import pandas as pd
from support_functions import *
from st_aggrid import *

st.title('Fantasy Football Optimizer')
st.subheader('Welcome to my fantasy football optimizer.')
uploaded_file = st.sidebar.file_uploader("Choose a file")


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

try:
    data = uploadInitalFile(df)
except:
    st.warning('Please Upload File')

try: 
    AgGrid(data, fit_columns_on_grid_load = True)
except:
    st.write('')


