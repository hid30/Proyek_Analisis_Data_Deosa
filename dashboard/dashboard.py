import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi tema
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide", page_icon="🚲")

# Load data
df = pd.read_csv('all_data.csv')
df['weather_desc'] = df['weathersit'].map({1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Berat'})
df['is_weekend'] = df['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')


# Sidebar
st.sidebar.title("Filter Data")
weather_options = df['weather'].unique()
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", weather_options, default=weather_options)

day_type = st.sidebar.radio("Pilih Jenis Hari", ["Hari Kerja", "Akhir Pekan", "Semua"], index=2)

# Filter data berdasarkan pilihan
filtered_df = df[df['weather'].isin(selected_weather)]
if day_type == "Hari Kerja":
    filtered_df = filtered_df[df['weekday'].isin([0, 1, 2, 3, 4])]
elif day_type == "Akhir Pekan":
    filtered_df = filtered_df[df['weekday'].isin([5, 6])]

# Dashboard Header
st.title("Dashboard Penyewaan Sepeda")
st.write("Analisis Pengaruh Cuaca terhadap Penyewaan Sepeda")

# Grafik 1: Tren Penyewaan Sepeda
st.subheader("Tren Penyewaan Sepeda")
fig1 = px.line(filtered_df, x="date", y="count", title="Jumlah Penyewaan Sepeda Harian", labels={"count": "Jumlah Penyewaan", "date": "Tanggal"})
st.plotly_chart(fig1)

# Grafik 2: Distribusi Penyewaan Berdasarkan Cuaca
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig2 = px.box(filtered_df, x="weather", y="count", title="Distribusi Penyewaan Berdasarkan Cuaca", labels={"weather": "Kondisi Cuaca", "count": "Jumlah Penyewaan"})
st.plotly_chart(fig2)

# Grafik 3: Perbandingan Hari Kerja vs Akhir Pekan
st.subheader("Perbandingan Pola Penyewaan")
fig3 = px.bar(filtered_df, x="weekday", y="count", title="Pola Penyewaan Sepeda di Hari Kerja dan Akhir Pekan", labels={"weekday": "Hari", "count": "Jumlah Penyewaan"}, color="weekday")
st.plotly_chart(fig3)

st.write("\n\n**Dashboard ini membantu memahami pola penyewaan sepeda berdasarkan cuaca dan jenis hari.**")
