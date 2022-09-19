import streamlit as st

st.title('Fantasy Football Optimizer')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if 'lineups_file' not in st.session_state:
    st.info('File Ingest has not been completed')
else:
    st.write(st.session_state['lineups_file'])