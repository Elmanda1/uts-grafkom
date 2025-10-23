"""
Entry Point Utama Aplikasi Pembelajaran Grafika Komputer.

File ini bertanggung jawab untuk:
1. Mengatur konfigurasi halaman utama Streamlit.
2. Memuat gaya CSS kustom.
3. Menampilkan halaman utama/dashboard.

Streamlit secara otomatis akan mendeteksi file di dalam folder `pages`
untuk membuat navigasi sidebar.
"""

import streamlit as st
from config import PAGE_CONFIG, ASSETS_PATH
from utils.helpers import load_css

# --- Konfigurasi Halaman --- #
# Mengatur konfigurasi halaman sebagai hal pertama yang dijalankan
st.set_page_config(**PAGE_CONFIG)

# --- Memuat Aset & Gaya --- #
# Memuat CSS kustom dari path yang didefinisikan di config
# try:
#     load_css(ASSETS_PATH["styles"])
# except Exception as e:
#     st.warning(f"Gagal memuat file CSS. Error: {e}")

# --- Konten Halaman Utama --- #
# Streamlit akan secara otomatis mengarahkan ke halaman "Home" dari folder `pages`
# jika ada. Namun, kita bisa mendefinisikan konten default di sini jika diperlukan.

st.title("🎨 Selamat Datang di Aplikasi Pembelajaran Grafika Komputer")
st.markdown("---")

st.info(
    "**Gunakan sidebar di sebelah kiri untuk menavigasi ke materi yang berbeda.**\n\n" 
    "Aplikasi ini dirancang untuk memberikan pemahaman interaktif tentang konsep-konsep inti dalam grafika komputer."
)

st.success("Pilih salah satu halaman dari sidebar untuk memulai.")

# Menambahkan toggle tema (opsional, Streamlit > 1.10.0 punya bawaan)
st.sidebar.markdown("---")
st.sidebar.markdown("**Pengaturan Tampilan**")
# Streamlit modern sudah memiliki toggle tema di menu utama, jadi tidak perlu menambahkannya secara manual.
# st.sidebar.checkbox("Mode Gelap", value=True)


# --- Penjelasan Struktur Proyek --- #
with st.expander("Tentang Aplikasi Ini"):
    st.markdown("""
    Aplikasi ini adalah sebuah platform pembelajaran interaktif yang dibuat menggunakan Streamlit.
    Tujuannya adalah untuk mendemonstrasikan konsep-konsep fundamental dalam Grafika Komputer,
    mulai dari menggambar garis hingga shading 3D.

    **Navigasi:**
    - Gunakan menu di sidebar untuk berpindah antar topik/minggu.
    - Setiap halaman berisi demo interaktif dan penjelasan konsep terkait.

    **Teknologi:**
    - **Framework:** Streamlit
    - **Library:** NumPy, Pillow, Plotly, Streamlit-Drawable-Canvas
    - **Bahasa:** Python
    """)
