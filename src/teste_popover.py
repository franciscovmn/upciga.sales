import streamlit as st
import pandas as pd
from st_keyup import st_keyup  # streamlit-keyup allows text input to be rendered on keyup, meaning the input value updates after every key press.

def teste_popover():
    with st.sidebar:

        if 'yr_result' not in st.session_state:
            st.session_state.yr_result = None
        if 'airline_result' not in st.session_state:
            st.session_state.airline_result = None


        DATAFRAME_HEIGTH = 150


        data = {
            'Year': [
                '2020', '2020', '2020', '2020', '2020', '2020', '2020', '2020', '2020', '2020',
                '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021', '2021',
                '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022', '2022',
                '2023', '2023', '2023', '2023', '2023', '2023', '2023', '2023', '2023', '2023',
                '2024', '2024', '2024', '2024', '2024', '2024', '2024', '2024', '2024', '2024'
            ],
            'Airlines': [
                'Philippine Airlines', 'Japan Airlines', 'China Airlines', 'American Airlines',
                'Qantas', 'Emirates', 'Delta Airlines', 'United Airlines', 'British Airways',
                'Air France', 'Philippine Airlines', 'Japan Airlines', 'China Airlines',
                'American Airlines', 'Qantas', 'Emirates', 'Delta Airlines', 'United Airlines',
                'British Airways', 'Air France', 'Philippine Airlines', 'Japan Airlines',
                'China Airlines', 'American Airlines', 'Qantas', 'Emirates', 'Delta Airlines',
                'United Airlines', 'British Airways', 'Air France', 'Philippine Airlines',
                'Japan Airlines', 'China Airlines', 'American Airlines', 'Qantas', 'Emirates',
                'Delta Airlines', 'United Airlines', 'British Airways', 'Air France',
                'Philippine Airlines', 'Japan Airlines', 'China Airlines', 'American Airlines',
                'Qantas', 'Emirates', 'Delta Airlines', 'United Airlines', 'British Airways',
                'Air France'
            ]
        }


        def change_year_cb(df):
            st.session_state.yr_result = filter_by_year(
                df, st.session_state.txt_searchyeark)


        def filter_by_year(df, year):
            filtered_df = df[df['Year'] == year]
            unique_year = filtered_df['Year'].unique()
            return unique_year


        def change_airline_cb(df):
            st.session_state.airline_result = filter_by_airline(
                df, st.session_state.txt_searchairlinek)


        def filter_by_airline(df, airline):
            filtered_df = df[df['Airlines'].str.contains(airline, case=False)]
            unique_airlines = filtered_df['Airlines'].unique()
            return unique_airlines


        df = pd.DataFrame(data)
            
        # con_cols = st.columns([2, 1])
        # with con_cols[0]:
        #     with st.container(border=True):
        #         st.markdown('**Please Select Filters**')

        with st.popover(label='Year', use_container_width=True):
            cols = st.columns([2, 1], gap='small')
            with cols[0]:
                st_keyup("Search Year", key='txt_searchyeark',
                        on_change=change_year_cb, args=(df,),
                        placeholder='type to search')
                st.dataframe(st.session_state.yr_result, hide_index=True,
                            use_container_width=True, height=DATAFRAME_HEIGTH)

            # Shows year checkboxes
            for y in df['Year'].unique():
                st.checkbox(y, value=True, key=y)

        with st.popover(label='Airlines', use_container_width=True):
            cols = st.columns([2, 1], gap='small')
            with cols[0]:
                st_keyup('Search Airlines', key='txt_searchairlinek',
                        on_change=change_airline_cb, args=(df,),
                        placeholder='type to search')
                st.dataframe(st.session_state.airline_result, hide_index=True,
                            use_container_width=True, height=DATAFRAME_HEIGTH)

            # Shows airline checkboxes
            for a in df['Airlines'].unique():
                st.checkbox(a, value=True, key=a)