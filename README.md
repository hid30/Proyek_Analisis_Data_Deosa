Projek-Analisis-Data-Dengn-Python
Setup Environment
Langkah-langkah untuk menyiapkan lingkungan agar dashboard bisa dijalankan.

1. Instal Python
Unduh Python dari python.org.
Instal dengan mencentang opsi "Add Python to PATH".
Verifikasi instalasi:
Buka Command Prompt (CMD): Win + R, ketik cmd, Enter.
Ketik: python --version.
Harusnya muncul versi (misalnya, Python 3.9.0).
2. Unduh File Proyek
Salin semua file (day.csv, dashboard.py, requirements.txt) ke folder lokal, misalnya: C:\Proyek_Analisis_Data.
Setup Environment - Shell/Terminal
Instruksi spesifik untuk menyiapkan dependensi menggunakan shell/terminal (CMD di Windows).

Buka Command Prompt:

Tekan Win + R, ketik cmd, lalu tekan Enter.
Pastikan CMD terbuka.
Navigasi ke Folder Proyek:

Ketik perintah berikut untuk masuk ke folder proyek:

Cek Instalasi Ulang: -pip uninstall streamlit -pip install streamlit

-Gunakan Virtual Environment (opsi bersih):

Buat environment: python -m venv myenv
Aktifkan: myenv\Scripts\activate
Instal: pip install streamlit pandas matplotlib seaborn
Jalankan: cd C:/Proyek_Analisis_Data-Dengn-Python
Lanjutkan streamlit run dashboard.py
-Dan Nanti hasilnya akan seperti ini: You can now view your Streamlit app in your browser. Local URL: http://localhost:8501
