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




# Data Assessment
st.subheader("Assessing Data: Cek Informasi Dataset")
st.write("Data Assessing dilakukan untuk memastikan data bersih, lengkap, dan valid.")

st.write(df.info())
st.write("Jumlah Missing Value:")
st.write(df.isnull().sum())

# Data Cleaning
df['dteday'] = pd.to_datetime(df['dteday'])
weather_map = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Berat'}
df['weather_desc'] = df['weathersit'].map(weather_map)
df['is_weekend'] = df['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

st.subheader("Cleaning Data")
st.write("Proses membersihkan dataset dari error, data yang hilang, atau inkonsistensi agar siap untuk analisis.")
st.write(df[['dteday', 'weather_desc', 'is_weekend', 'cnt']].head())

# Exploratory Data Analysis (EDA)
st.subheader("Exploratory Data Analysis (EDA)")

st.write("### Pertanyaan 1: Pengaruh Cuaca terhadap Jumlah Sepeda yang Disewa")
weather_impact = df.groupby('weather_desc')['cnt'].agg(['mean', 'median', 'std']).reset_index()
st.write(weather_impact)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='weather_desc', y='mean', data=weather_impact, palette='Blues_d', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan (Rata-rata)")
st.pyplot(fig)

st.write("**Insight:** Penyewaan tertinggi saat cuaca cerah dan berkabut. Penyewaan menurun drastis saat hujan.")

st.write("### Pertanyaan 2: Perbedaan Pola Penyewaan pada Hari Kerja dan Hari Libur")
day_type_impact = df.groupby(['workingday', 'holiday'])['cnt'].agg(['mean', 'median', 'std']).reset_index()
st.write(day_type_impact)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='is_weekend', y='cnt', data=df, estimator=sum, palette='Blues', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda: Weekday vs Weekend")
ax.set_xlabel("Tipe Hari")
ax.set_ylabel("Jumlah Penyewaan (Rata-rata)")
st.pyplot(fig)

st.write("**Insight:** Penyewaan lebih tinggi pada hari kerja, menunjukkan penggunaan utama untuk transportasi.")

# Analisis Lanjutan
st.subheader("Analisis Lanjutan")

st.write("### Pertanyaan 3: Distribusi Penyewaan Sepeda Sepanjang Hari")
hourly_rentals = df.groupby('hr')['cnt'].describe()
st.write(hourly_rentals)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='hr', y='cnt', data=df, estimator='mean', marker='o', ax=ax)
ax.set_title("Distribusi Penyewaan Sepeda Sepanjang Hari")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.write("**Insight:** Puncak penyewaan terjadi pada pukul 08:00 dan 17:00, menunjukkan pola kerja kantoran.")

st.write("### Pertanyaan 4: Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
windspeed_correlation = df[['windspeed', 'cnt']].corr().iloc[0, 1]
st.write(f"Korelasi antara Kecepatan Angin dan Penyewaan: {windspeed_correlation:.2f}")

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x='windspeed', y='cnt', data=df, alpha=0.5, ax=ax)
ax.set_title("Hubungan Kecepatan Angin dengan Penyewaan Sepeda")
ax.set_xlabel("Kecepatan Angin")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.write("**Insight:** Kecepatan angin memiliki korelasi lemah terhadap jumlah penyewaan sepeda.")

st.write("### Pertanyaan 5: Tren Penyewaan Sepeda Setiap Bulan")
df['month'] = df['dteday'].dt.month
monthly_rentals = df.groupby('month')['cnt'].mean().reset_index()
st.write(monthly_rentals)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='month', y='cnt', data=monthly_rentals, marker='o', ax=ax)
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan (Rata-rata)")
st.pyplot(fig)

st.write("**Insight:** Penyewaan meningkat dari awal tahun dan mencapai puncaknya di bulan September.")

# Kesimpulan
st.subheader("Kesimpulan")
st.write("1. **Cuaca sangat memengaruhi penyewaan sepeda.** Penyewaan tertinggi terjadi saat cuaca cerah, sedangkan hujan berat mengurangi penyewaan drastis.")
st.write("2. **Penyewaan lebih tinggi pada hari kerja dibanding akhir pekan.** Hal ini menunjukkan bahwa sebagian besar pengguna memanfaatkan sepeda untuk keperluan transportasi harian.")
st.write("3. **Puncak penyewaan terjadi pada jam sibuk (08:00 dan 17:00).** Tren ini konsisten dengan penggunaan sepeda untuk transportasi kerja.")
st.write("4. **Kecepatan angin memiliki dampak yang sangat kecil terhadap penyewaan sepeda.**")
st.write("5. **Tren bulanan menunjukkan peningkatan jumlah penyewaan hingga bulan September, kemudian menurun.**")

st.write("📌 **Rekomendasi Bisnis:** Penyedia layanan dapat mempertimbangkan promosi di hari hujan, paket langganan untuk pekerja, serta peningkatan jumlah sepeda di bulan dengan permintaan tinggi.")




