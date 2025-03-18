import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Overview", layout="wide")

# Fungsi untuk memuat data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    return day_df, hour_df

# Memuat data
day_df, hour_df = load_data()

# Sidebar untuk pemilihan dataset
st.sidebar.title("Pilih Dataset")
dataset = st.sidebar.radio("Dataset", ("Day Data", "Hour Data"))

# Menampilkan dataset yang dipilih
if dataset == "Day Data":
    st.title("Day Dataset Overview")
    st.write(day_df.head())
    
    # Visualisasi Data
    st.subheader("Distribusi Jumlah Penyewaan")
    fig = px.histogram(day_df, x="cnt", nbins=30, title="Distribusi Jumlah Penyewaan Harian")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.title("Hour Dataset Overview")
    st.write(hour_df.head())
    
    # Visualisasi Data
    st.subheader("Distribusi Jumlah Penyewaan per Jam")
    fig = px.histogram(hour_df, x="cnt", nbins=30, title="Distribusi Jumlah Penyewaan Per Jam")
    st.plotly_chart(fig, use_container_width=True)

# Menampilkan ringkasan statistik
st.subheader("Ringkasan Statistik")
st.write(day_df.describe() if dataset == "Day Data" else hour_df.describe())
