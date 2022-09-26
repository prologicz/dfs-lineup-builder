from textwrap import indent
import streamlit as st
from st_aggrid import *
from reports import draftKingsAllLineups, summaryReport, usagePercentage

st.title('Fantasy Football Optimizer')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if 'solutions' not in st.session_state:
    st.info('Lineup Generator Not Run')
else:
    usePercent = usagePercentage(st.session_state['remap_data'], st.session_state['solutions'])
    usePercent = pd.merge(left=usePercent, right= st.session_state['remap_data'], left_on=usePercent.index, right_on='key', how='left')
    print(usePercent)
    usePercentDisplays = pd.DataFrame()
    usePercentDisplays['name'] = usePercent['name']
    usePercentDisplays['position'] = usePercent['position']
    usePercentDisplays['percent'] = usePercent['percent of lineups']
    print(usePercentDisplays)

    usePercentQB = (usePercentDisplays .loc[usePercentDisplays ['position'] == 'QB']).sort_values('percent', ascending=False)
    usePercentRB = (usePercentDisplays .loc[usePercentDisplays ['position'] == 'RB']).sort_values('percent', ascending=False)
    usePercentWR= (usePercentDisplays .loc[usePercentDisplays ['position'] == 'WR']).sort_values('percent', ascending=False)
    usePercentTE= (usePercentDisplays .loc[usePercentDisplays ['position'] == 'TE']).sort_values('percent', ascending=False)
    usePercentDST= (usePercentDisplays .loc[usePercentDisplays ['position'] == 'DST']).sort_values('percent', ascending=False)
    st.header('Ownership Percentage')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1 :
        style = usePercentQB.style.hide_index()
        style.hide_columns()
        st.subheader('Quarterbacks')
        st.write(style.to_html(), unsafe_allow_html=True)
    
    with col2:
        style = usePercentRB.style.hide_index()
        style.hide_columns()
        st.subheader('Running Backs')
        st.write(style.to_html(), unsafe_allow_html=True)
    
    with col3:
        style = usePercentWR.style.hide_index()
        style.hide_columns()
        st.subheader('Wide Receivers')
        st.write(style.to_html(), unsafe_allow_html=True)
    
    with col4:
        style = usePercentTE.style.hide_index()
        style.hide_columns()
        st.subheader('Tight End')
        st.write(style.to_html(), unsafe_allow_html=True)
    
    with col5:
        style = usePercentDST.style.hide_index()
        style.hide_columns()
        st.subheader('Defense')
        st.write(style.to_html(), unsafe_allow_html=True)



    st.header('Lineups')
    lineupSummary =summaryReport(st.session_state['remap_data'], st.session_state['solutions'])
    AgGrid(lineupSummary, fit_columns_on_grid_load = True)


    lineups = draftKingsAllLineups(st.session_state['remap_data'], st.session_state['solutions'])
    csv = lineups.to_csv(index=False)

    st.sidebar.title('Data Download')
    st.sidebar.download_button(
        label = 'Download Draftkings File',
        data = csv,
        file_name='dk_all_lineups.csv'
    )