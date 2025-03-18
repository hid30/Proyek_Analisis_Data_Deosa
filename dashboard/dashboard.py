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


### Assessing Data
"""

# Assessing Data: Cek informasi dataset
print("\nInformasi Dataset:")
print(df.info())
print("\nJumlah Missing Value:")
print(df.isnull().sum())

"""**Insight:**
- Data Assessing dilakukan untuk memeriksa kualitas dan kesesuaian data sebelum dilakukan analisis lebih lanjut. Tujuan utama dari data assessing adalah memastikan bahwa data bersih, lengkap, dan valid. Dan pada data yang digunakan tidak ditemukan adanya missing value.

### Cleaning Data
"""

# Cleaning Data: Preprocessing
df['dteday'] = pd.to_datetime(df['dteday'])
weather_map = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Berat'}
df['weather_desc'] = df['weathersit'].map(weather_map)
df['is_weekend'] = df['weekday'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
print("\nData Setelah Preprocessing:")
print(df[['dteday', 'weather_desc', 'is_weekend', 'cnt']].head())

"""**Insight:**
- Data Cleaning digunakan untuk proses membersihkan dataset dari error, data yang hilang, atau inkonsistensi agar siap digunakan dalam analisis, contohnya Penyewaan sepeda lebih tinggi pada hari kerja, menunjukkan dominasi pekerja dan mahasiswa sebagai pengguna utama, sehingga strategi bisnis dapat fokus pada langganan harian atau mingguan.

## Exploratory Data Analysis (EDA)

### Explore ...
"""

# Statistik deskriptif
print("Statistik Deskriptif:")
print(df[['cnt', 'temp', 'hum', 'windspeed']].describe())

# Pertanyaan 1: Pengaruh cuaca terhadap jumlah sepeda yang disewa
weather_impact = df.groupby('weather_desc')['cnt'].agg(['mean', 'median', 'std']).reset_index()
print("\nPengaruh Cuaca terhadap Penyewaan Sepeda:")
print(weather_impact)

# Pertanyaan 2: Perbedaan pola penyewaan pada hari kerja (workingday) dan hari libur (holiday)
day_type_impact = df.groupby(['workingday', 'holiday'])['cnt'].agg(['mean', 'median', 'std']).reset_index()
print("\nPerbedaan Pola Penyewaan pada Hari Kerja vs Hari Libur:")
print(day_type_impact)

"""**Insight:**
1. **Pengaruh Cuaca:** Penyewaan sepeda tertinggi terjadi saat cuaca cerah (**mean: 387**) dan berkabut (**mean: 374**), sedangkan penyewaan turun drastis saat hujan, terutama hujan berat (**mean: 74**). Hal ini menunjukkan bahwa kondisi cuaca sangat memengaruhi minat pengguna, sehingga strategi bisnis dapat mencakup layanan alternatif saat hujan, seperti penyewaan payung atau diskon pada hari hujan.  

2. **Pola Penyewaan pada Hari Kerja vs Libur:** Penyewaan sepeda lebih tinggi pada hari kerja (**mean: 370**) dibandingkan hari libur (**mean: 301**), mengindikasikan bahwa sebagian besar pengguna memanfaatkan sepeda untuk keperluan transportasi harian, bukan sekadar rekreasi. Bisnis dapat menargetkan promosi untuk pekerja atau mahasiswa dengan paket langganan harian/mingguan pada hari kerja.

## Visualization & Explanatory Analysis

### Pertanyaan 1:
"""

plt.figure(figsize=(8, 5))
sns.barplot(x='weather_desc', y='cnt', data=weather_group, palette='Blues_d')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Penyewaan (Rata-rata)')
plt.show()

"""### Pertanyaan 2:"""

plt.figure(figsize=(8, 5))
sns.barplot(x='is_weekend', y='cnt', data=day_group, palette='Blues')
plt.title('Rata-rata Penyewaan Sepeda: Weekday vs Weekend')
plt.xlabel('Tipe Hari')
plt.ylabel('Jumlah Penyewaan (Rata-rata)')
plt.show()

"""**Insight:**
- Viusalisasi 1: Penyewaan sepeda paling tinggi terjadi saat cuaca cerah dan berkabut, sedangkan saat hujan ringan dan hujan berat, jumlah penyewaan turun drastis, menunjukkan bahwa cuaca buruk secara signifikan mengurangi minat penyewaan.
- Visualisasi 2: Dari grafik, terlihat bahwa rata-rata penyewaan sepeda pada akhir pekan sedikit lebih tinggi dibandingkan hari kerja, menunjukkan bahwa selain digunakan untuk transportasi harian, sepeda juga diminati untuk aktivitas rekreasi di akhir pekan.

## Analisis Lanjutan (Opsional)
"""

# Pertanyaan 3: Bagaimana distribusi jumlah penyewaan sepeda sepanjang hari?
hourly_rentals = df.groupby('hr')['cnt'].describe()
print("\nDistribusi Jumlah Penyewaan Sepeda Sepanjang Hari:")
print(hourly_rentals)

# Pertanyaan 4: Seberapa besar pengaruh kecepatan angin (windspeed) terhadap jumlah penyewaan sepeda?
windspeed_correlation = df[['windspeed', 'cnt']].corr().iloc[0, 1]
print(f"\nKorelasi antara Kecepatan Angin dan Penyewaan: {windspeed_correlation:.2f}")

# Pertanyaan 5: Bagaimana tren penyewaan sepeda setiap bulan?
df['month'] = pd.to_datetime(df['dteday']).dt.month  # Pastikan 'dteday' bertipe datetime
monthly_rentals = df.groupby('month')['cnt'].mean().reset_index()
print("\nRata-rata Penyewaan Berdasarkan Bulan:")
print(monthly_rentals)

"""- **Pola Penyewaan Sepeda Berdasarkan Jam**
Penyewaan sepeda mencapai puncak pada pukul 08:00 (359 penyewaan) dan 17:00 (461 penyewaan), menunjukkan pola penggunaan utama untuk perjalanan pagi dan sore hari, kemungkinan terkait dengan aktivitas kerja dan pulang kerja.
Hubungan Kecepatan Angin dengan Penyewaan Sepeda

- **Korelasi antara kecepatan angin dan jumlah penyewaan** sangat lemah (0.01), menunjukkan bahwa faktor ini hampir tidak berpengaruh terhadap keputusan pengguna dalam menyewa sepeda.
Tren Penyewaan Sepeda Berdasarkan Bulan

- **Penyewaan meningkat dari awal tahun hingga mencapai** puncaknya pada bulan September (462 penyewaan), kemudian menurun setelah bulan Oktober, kemungkinan dipengaruhi oleh faktor musiman atau perubahan pola aktivitas

## Conclusion

-  1: Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda

Berdasarkan analisis jumlah penyewaan sepeda terhadap kondisi cuaca, terdapat tren yang jelas bahwa kondisi cuaca sangat memengaruhi keputusan pengguna dalam menyewa sepeda.

Cuaca Cerah memiliki jumlah penyewaan tertinggi, dengan rata-rata sekitar 390 sepeda per hari. Hal ini menunjukkan bahwa pengguna lebih aktif menyewa sepeda saat cuaca mendukung aktivitas luar ruangan.
Cuaca Berkabut juga menunjukkan angka penyewaan yang tinggi, hanya sedikit di bawah cuaca cerah, mengindikasikan bahwa kabut tidak menjadi hambatan signifikan dalam penyewaan sepeda.
Hujan Ringan menyebabkan penurunan jumlah penyewaan yang cukup signifikan dibandingkan kondisi cerah atau berkabut.
Hujan Lebat memiliki jumlah penyewaan terendah, dengan rata-rata di bawah 80 sepeda per hari, yang menunjukkan bahwa kondisi ini sangat menghambat aktivitas penyewaan.

📌 Insight:
Dari pola ini, terlihat bahwa cuaca menjadi faktor utama dalam keputusan penyewaan sepeda. Bisnis penyewaan sepeda dapat mempertimbangkan strategi seperti promosi atau diskon saat cuaca buruk untuk tetap menarik pengguna. Selain itu, informasi prakiraan cuaca dapat digunakan untuk mengelola stok sepeda dengan lebih optimal.


- 2: Perbandingan Penyewaan Sepeda di Hari Kerja dan Akhir Pekan
Analisis jumlah penyewaan sepeda berdasarkan hari kerja dan akhir pekan menunjukkan pola berikut:

Hari Kerja → Rata-rata penyewaan sepeda tercatat sekitar 4.458 unit per hari, sedikit lebih rendah dibandingkan akhir pekan.
Akhir Pekan → Jumlah penyewaan meningkat menjadi 4.620 unit per hari, mengindikasikan adanya kenaikan meskipun selisihnya tidak terlalu besar.
Selisih → Perbedaan antara hari kerja dan akhir pekan berkisar 162 sepeda per hari, dengan tren yang menunjukkan bahwa akhir pekan memiliki tingkat penyewaan yang lebih tinggi.

📌 Insight:
Meskipun diasumsikan bahwa hari kerja akan memiliki lebih banyak penyewaan karena penggunaan sepeda sebagai alat transportasi ke tempat kerja, data menunjukkan bahwa akhir pekan justru mencatat jumlah penyewaan yang lebih tinggi. Hal ini kemungkinan besar disebabkan oleh aktivitas rekreasi atau wisata. Oleh karena itu, penyedia layanan dapat mempertimbangkan strategi pemasaran khusus, seperti paket diskon atau peningkatan jumlah sepeda pada akhir pekan untuk mengakomodasi lonjakan permintaan.
"""










st.caption('Copyright (c) 2025')
