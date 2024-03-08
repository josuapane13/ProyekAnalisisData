import pandas as pd
import altair as alt
import streamlit as st

day_df = pd.read_csv('https://raw.githubusercontent.com/josuapane13/ProyekAnalisisData/main/dataset/cleaned/day_df.csv')
hour_df = pd.read_csv("https://raw.githubusercontent.com/josuapane13/ProyekAnalisisData/main/dataset/cleaned/hour_df.csv")

hour_df.sort_values(by="date", inplace=True)
hour_df.reset_index(inplace=True)
hour_df["date"] = pd.to_datetime(hour_df["date"])
min_date = hour_df["date"].min()
max_date = hour_df["date"].max()


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
    st.subheader("Pilih Rentang Waktu")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    main_hour_df = hour_df[(hour_df["date"] >= str(start_date)) & 
        (hour_df["date"] <= str(end_date))]
    main_day_df = day_df[(day_df["date"] >= str(start_date)) & 
        (day_df["date"] <= str(end_date))]

 
    chart_temperature_season = {
        "mark": "point",
        "encoding": {
            "x": {
                "field": "temperature",
                "type": "quantitative",
            },
            "y": {
                "field": "total",
                "type": "quantitative",
            },
            "color": {"field": "season", "type": "nominal"},
            "shape": {"field": "season", "type": "nominal"},
        },
    }
    st.subheader("Penggunaan Rental Sepeda Berdasarkan Temperature")
    main_hour_df['weather'] = main_hour_df['weather'].map({1: 'Clear', 2: 'Mist / Cloudy', 3: 'Light Snow / Light Rain', 4: 'Heavy Rain / Ice Pallets'})

    temperature = f"{round(main_hour_df['temperature'].mean(), 2)}°C"
    windspeed = f"{round(main_hour_df['windspeed'].mean(), 2)} km/h"
    humidity = f"{round(main_hour_df['humidity'].mean(), 2)}%"


    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", temperature)
    col2.metric("Wind", windspeed)
    col3.metric("Humidity", humidity)


    st.subheader("Penggunaan Rental Sepeda Berdasarkan Temperature")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Penggunaan Rental Sepeda per Jam")
        st.vega_lite_chart(main_hour_df, chart_temperature_season, theme="streamlit", use_container_width=True)
    with col2:
        st.write("Penggunaan Rental Sepeda per Hari")
        st.vega_lite_chart(main_day_df, chart_temperature_season, theme="streamlit", use_container_width=True)
    st.subheader("Penggunaan Rental Sepeda Berdasarkan Cuaca")

    st.write("Penggunaan Rental Sepeda Berdasarkan Cuaca")
    st.bar_chart(main_hour_df, x='weather', y='total', use_container_width=True)
    
navigation = st.sidebar.radio("Navigation", ["Usecase 1", "Usecase 2"])

if navigation == "Usecase 1":
    usecase1()
elif navigation == "Usecase 2":
    usecase2()

st.sidebar.text('Copyright (c) Josua Pane 2024')
