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






df['dteday'] = pd.to_datetime(df['dteday'])
df['month'] = df['dteday'].dt.month

st.title("Analisis Lanjutan")

# Pertanyaan 3: Bagaimana distribusi jumlah penyewaan sepeda sepanjang hari?
st.header("Distribusi Jumlah Penyewaan Sepeda Sepanjang Hari")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x=df['hr'], y=df['cnt'], ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Distribusi Penyewaan Sepeda Sepanjang Hari")
st.pyplot(fig)
st.write("\nInsight: Penyewaan sepeda mencapai puncak pada pukul 08:00 dan 17:00, menandakan pola penggunaan utama terkait jam kerja.")

# Pertanyaan 4: Seberapa besar pengaruh kecepatan angin terhadap penyewaan sepeda?
st.header("Pengaruh Kecepatan Angin terhadap Penyewaan Sepeda")
windspeed_correlation = df[['windspeed', 'cnt']].corr().iloc[0, 1]
st.write(f"Korelasi antara kecepatan angin dan jumlah penyewaan: {windspeed_correlation:.2f}")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=df['windspeed'], y=df['cnt'], ax=ax, alpha=0.5)
ax.set_xlabel("Kecepatan Angin")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.set_title("Hubungan Kecepatan Angin dan Penyewaan Sepeda")
st.pyplot(fig)
st.write("\nInsight: Korelasi rendah menunjukkan kecepatan angin tidak berpengaruh signifikan terhadap jumlah penyewaan sepeda.")

# Pertanyaan 5: Bagaimana tren penyewaan sepeda setiap bulan?
st.header("Tren Penyewaan Sepeda Setiap Bulan")
monthly_rentals = df.groupby('month')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=monthly_rentals['month'], y=monthly_rentals['cnt'], marker='o', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda Per Bulan")
st.pyplot(fig)
st.write("\nInsight: Penyewaan sepeda meningkat hingga September, kemudian menurun setelahnya, kemungkinan dipengaruhi oleh perubahan musim.")

# Kesimpulan Akhir
st.header("Kesimpulan")
st.write("1. Pengaruh Cuaca terhadap Penyewaan: Cuaca cerah meningkatkan penyewaan, sementara hujan deras menyebabkan penurunan drastis.")
st.write("2. Perbedaan Hari Kerja dan Akhir Pekan: Penyewaan sedikit lebih tinggi di akhir pekan, kemungkinan karena aktivitas rekreasi.")
st.write("3. Distribusi Sepanjang Hari: Puncak penyewaan terjadi pada jam 08:00 dan 17:00, menunjukkan penggunaan utama untuk perjalanan kerja.")
st.write("4. Kecepatan Angin: Tidak ada pengaruh signifikan terhadap penyewaan.")
st.write("5. Tren Bulanan: Penyewaan meningkat hingga September sebelum menurun, mungkin karena faktor musiman.")
