import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import datetime
import time
import pytz
from sklearn.cluster import KMeans
import folium


st.title('Proyek Analisi Data')
st.info('Kelas Visualisasi Data Dengan Python - Deosa Putra Caniago')

# Load data
github_url_day = "https://raw.githubusercontent.com/hid30/Proyek_Analisis_Data_Deosa/main/dashboard/day.csv"
github_url_hour = "https://raw.githubusercontent.com/hid30/Proyek_Analisis_Data_Deosa/main/dashboard/hour.csv"
day_df = pd.read_csv(github_url_day)
hour_df = pd.read_csv(github_url_hour)

st.title('Data - Dicoding Laskar AI')
tab1, tab2, tab3 , tab4 = st.tabs(["Data Hari", "Data Jam", "RFM Analysis", "Clustering"])
 
with tab1:
    st.header("Data Harian")
    st.dataframe(day_df)
 
with tab2:
    st.header("Data Per Jam")
    st.dataframe(hour_df)

with tab3:
     st.header("RFM Analysis (Recency, Frequency, Monetary)")
     rfm_df = day_df.groupby("dteday").agg({"cnt": ['sum', 'count']})
     rfm_df.columns = ["Total_Peminjaman", "Frekuensi_Peminjaman"]
     rfm_df['Recency'] = (pd.to_datetime(day_df['dteday']).max() - pd.to_datetime(day_df['dteday'])).dt.days
     st.dataframe(rfm_df)

with tab4:
     st.header("Clustering Pengguna Berdasarkan Peminjaman")
     kmeans = KMeans(n_clusters=3)
     day_df['Cluster'] = kmeans.fit_predict(day_df[['cnt']])
     fig, ax = plt.subplots()
     sns.scatterplot(data=day_df, x="dteday", y="cnt", hue="Cluster", palette="viridis", ax=ax)
     st.pyplot(fig)





# Data processing
season_avg = day_df.groupby("season")["cnt"].mean()
hour_avg = hour_df.groupby("hr")["cnt"].mean()

# Streamlit UI
st.header("Pertanyaan Analisis Data")
st.write("1. Bagaimana pola penggunaan sepeda berubah berdasarkan musim?")
fig, ax = plt.subplots()
season_avg.plot(kind='bar', ax=ax, color=['blue', 'green', 'orange', 'red'])
ax.set_xticklabels(['Semi', 'Panas', 'Gugur', 'Dingin'], rotation=0)
ax.set_ylabel("Rata-rata peminjaman")
st.pyplot(fig)

st.write("2. Pada jam berapa jumlah peminjaman sepeda paling tinggi dalam sehari?")
fig, ax = plt.subplots()
hour_avg.plot(kind='line', ax=ax, marker='o', color='purple')
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata peminjaman")
st.pyplot(fig)

max_rent_day = day_df.loc[day_df["cnt"].idxmax(), ["dteday", "cnt"]]
min_rent_day = day_df.loc[day_df["cnt"].idxmin(), ["dteday", "cnt"]]

st.write(f"Hari dengan peminjaman terbanyak: {max_rent_day['dteday']} dengan {max_rent_day['cnt']} peminjaman.")
st.write(f"Hari dengan peminjaman tersedikit: {min_rent_day['dteday']} dengan {min_rent_day['cnt']} peminjaman.")

# Analisis Proporsi Peminjaman antara Hari Kerja dan Akhir Pekan
st.write("3. Bagaimana proporsi peminjaman sepeda pada hari kerja vs akhir pekan?")
weekend_count = day_df[day_df['weekday'].isin([0, 6])]['cnt'].sum()
weekday_count = day_df[~day_df['weekday'].isin([0, 6])]['cnt'].sum()

labels = ["Hari Kerja", "Akhir Pekan"]
values = [weekday_count, weekend_count]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', colors=["blue", "orange"])
ax.set_title("Distribusi Peminjaman Sepeda pada Hari Kerja vs Akhir Pekan")
st.pyplot(fig)



# Assessing Data: Cek informasi dataset
print("\nInformasi Dataset:")
print(df.info())
print("\nJumlah Missing Value:")
print(df.isnull().sum())

st.write("- Data Assessing dilakukan untuk memeriksa kualitas dan kesesuaian data sebelum dilakukan analisis lebih lanjut. Tujuan utama dari data assessing adalah memastikan bahwa data bersih, lengkap, dan valid. Dan pada data yang digunakan tidak ditemukan adanya missing value.")

st.write("Cleaning Data")
df['dteday'] = pd.to_datetime(df['dteday'])
weather_map = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Berat'}
df['weather_desc'] = df['weathersit'].map(weather_map)
df['is_weekend'] = df['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
print("\nData Setelah Preprocessing:")
print(df[['dteday', 'weather_desc', 'is_weekend', 'cnt']].head())


st.write("- Data Cleaning digunakan untuk proses membersihkan dataset dari error, data yang hilang, atau inkonsistensi agar siap digunakan dalam analisis, contohnya Penyewaan sepeda lebih tinggi pada hari kerja, menunjukkan dominasi pekerja dan mahasiswa sebagai pengguna utama, sehingga strategi bisnis dapat fokus pada langganan harian atau mingguan.")

## Exploratory Data Analysis (EDA)

# Statistik deskriptif
print("Statistik Deskriptif:")
print(df[['cnt', 'temp', 'hum', 'windspeed']].describe())

st.write(" Pertanyaan 1: Pengaruh cuaca terhadap jumlah sepeda yang disewa")
weather_impact = df.groupby('weather_desc')['cnt'].agg(['mean', 'median', 'std']).reset_index()
print("\nPengaruh Cuaca terhadap Penyewaan Sepeda:")
print(weather_impact)

st.write(" Pertanyaan 2: Perbedaan pola penyewaan pada hari kerja (workingday) dan hari libur (holiday)")
day_type_impact = df.groupby(['workingday', 'holiday'])['cnt'].agg(['mean', 'median', 'std']).reset_index()
print("\nPerbedaan Pola Penyewaan pada Hari Kerja vs Hari Libur:")
print(day_type_impact)


st.write("1. **Pengaruh Cuaca:** Penyewaan sepeda tertinggi terjadi saat cuaca cerah (**mean: 387**) dan berkabut (**mean: 374**), sedangkan penyewaan turun drastis saat hujan, terutama hujan berat (**mean: 74**). Hal ini menunjukkan bahwa kondisi cuaca sangat memengaruhi minat pengguna, sehingga strategi bisnis dapat mencakup layanan alternatif saat hujan, seperti penyewaan payung atau diskon pada hari hujan.")  

st.write("2. **Pola Penyewaan pada Hari Kerja vs Libur:** Penyewaan sepeda lebih tinggi pada hari kerja (**mean: 370**) dibandingkan hari libur (**mean: 301**), mengindikasikan bahwa sebagian besar pengguna memanfaatkan sepeda untuk keperluan transportasi harian, bukan sekadar rekreasi. Bisnis dapat menargetkan promosi untuk pekerja atau mahasiswa dengan paket langganan harian/mingguan pada hari kerja.")

st.write("Visualization & Explanatory Analysis")

st.write("Pertanyaan 1:")

plt.figure(figsize=(8, 5))
sns.barplot(x='weather_desc', y='cnt', data=weather_group, palette='Blues_d')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Penyewaan (Rata-rata)')
plt.show()

st.write("Pertanyaan 2:")

plt.figure(figsize=(8, 5))
sns.barplot(x='is_weekend', y='cnt', data=day_group, palette='Blues')
plt.title('Rata-rata Penyewaan Sepeda: Weekday vs Weekend')
plt.xlabel('Tipe Hari')
plt.ylabel('Jumlah Penyewaan (Rata-rata)')
plt.show()

st.write("- Viusalisasi 1: Penyewaan sepeda paling tinggi terjadi saat cuaca cerah dan berkabut, sedangkan saat hujan ringan dan hujan berat, jumlah penyewaan turun drastis, menunjukkan bahwa cuaca buruk secara signifikan mengurangi minat penyewaan.")
st.write("- Visualisasi 2: Dari grafik, terlihat bahwa rata-rata penyewaan sepeda pada akhir pekan sedikit lebih tinggi dibandingkan hari kerja, menunjukkan bahwa selain digunakan untuk transportasi harian, sepeda juga diminati untuk aktivitas rekreasi di akhir pekan.")










st.caption('Copyright (c) 2025')
