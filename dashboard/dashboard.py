import pandas as pd
import altair as alt
import streamlit as st

day_df = pd.read_csv('https://raw.githubusercontent.com/josuapane13/ProyekAnalisisData/main/dataset/cleaned/day_df.csv')

def filter_data(selected_season, selected_holiday, selected_weather, selected_month):
    return day_df[
        (day_df['season'].isin(selected_season if selected_season else day_df['season'])) &
        (day_df['holiday'] == selected_holiday) &
        (day_df['weather'].isin(selected_weather if selected_weather else day_df['weather'])) &
        (day_df['month'].isin(selected_month if selected_month else day_df['month']))
    ]

def usecase1():
    st.title('Pengguna rental sepeda berdasarkan musim')
    musim = day_df.groupby(by="season").agg({
        "casual": "sum",
        "registered": "sum",
        "total": "sum"
    }).sort_values(by="total", ascending=False)

    bar_chart_musim = alt.Chart(musim.reset_index()).mark_bar().encode(
        x='season:N',
        y='total:Q',
        color='season:N',
        tooltip=['season', 'total']
    ).interactive()

    st.altair_chart(bar_chart_musim, use_container_width=True)

def usecase2():
    st.title('Penggunaan Rental Sepeda Berdasarkan Temperatur')
    scatter_plot = alt.Chart(day_df).mark_circle().encode(
        x='temperature:Q',
        y='total:Q',
        color='season:N',
        tooltip=['temperature', 'total']
    ).interactive()

    st.altair_chart(scatter_plot, use_container_width=True)

def filter_data_usecase():
    st.title('Filter Data Interaktif')
    
    selected_season = st.multiselect('Pilih Musim', day_df['season'].unique())
    selected_holiday = st.selectbox('Pilih Hari Libur', [True, False])
    selected_weather = st.multiselect('Pilih Cuaca', day_df['weather'].unique())
    selected_month = st.multiselect('Pilih Bulan', day_df['month'].unique())
    filtered_data_result = filter_data(selected_season, selected_holiday, selected_weather, selected_month)


    st.write('Data Setelah Difilter:')
    st.write(filtered_data_result)


navigation = st.sidebar.radio("Navigation", ["Usecase 1", "Usecase 2", "Filter Data"])

if navigation == "Usecase 1":
    usecase1()
elif navigation == "Usecase 2":
    usecase2()
elif navigation == "Filter Data":
    filter_data_usecase()

st.sidebar.text('Copyright (c) Josua Pane 2024')
