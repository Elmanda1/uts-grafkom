import streamlit as st
from config import PAGE_CONFIG, ASSETS_PATH
from utils.helpers import load_css

# --- Konfigurasi Halaman --- #
st.set_page_config(**PAGE_CONFIG)

# --- Memuat Aset & Gaya --- #
try:
    load_css(ASSETS_PATH["styles"])
except Exception as e:
    st.error(f"⚠️ Gagal memuat file CSS: {e}")

# --- Header Section --- #
st.markdown("""
    <div class="header-container">
        <h1>Ujian Tengah Semester Grafika Komputer</h1>
        <p class="subtitle">Eksplorasi konsep fundamental grafika komputer dengan visualisasi real-time</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Hero Section --- #
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Selamat Datang!
    
    Aplikasi ini dirancang untuk membantu Anda memahami konsep-konsep inti dalam **grafika komputer** 
    melalui pendekatan interaktif dan visual. Dari algoritma menggambar garis hingga rendering 3D, 
    semua materi disajikan dengan demo yang dapat Anda eksperimen langsung.
    
    **Fitur Utama:**
    - Visualisasi algoritma real-time
    - Kontrol interaktif untuk eksplorasi
    - Perbandingan metode side-by-side
    - Penjelasan konsep yang jelas dan terstruktur
    """)

with col2:
    st.info("""
    **Cara Menggunakan:**
    
    1. Pilih topik dari **sidebar**
    2. Ikuti penjelasan konsep
    3. Eksperimen dengan parameter
    4. Amati hasil visualisasi
    """)

# --- Statistics/Progress Section --- #
st.markdown("### Materi yang Tersedia")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric(label="Total Topik", value="7", delta="Terus bertambah")

with stat_col2:
    st.metric(label="Algoritma", value="7", delta="Interaktif")

with stat_col3:
    st.metric(label="Visualisasi", value="6", delta="Real-time")

with stat_col4:
    st.metric(label="Demo", value="5", delta="Hands-on")

st.markdown("---")

# --- About Section --- #
with st.expander("Tentang Aplikasi Ini", expanded=False):
    st.markdown("""
    ### Tujuan Pembelajaran
    
    Aplikasi ini dikembangkan untuk memberikan pengalaman pembelajaran yang **interaktif** dan **visual** 
    dalam memahami konsep grafika komputer. Setiap topik dilengkapi dengan:
    
    - **Teori**: Penjelasan konsep fundamental
    - **Implementasi**: Kode algoritma yang dapat dipelajari
    - **Visualisasi**: Demo interaktif dengan parameter yang dapat diubah
    - **Latihan**: Eksperimen untuk memperdalam pemahaman
    
    ### Struktur Materi
    
    Materi disusun secara progresif dari konsep dasar hingga lanjutan:
    
    1. **Primitif Grafis**: Line, Circle, Ellipse drawing algorithms
    2. **Transformasi 2D**: Translation, Rotation, Scaling
    3. **Clipping**: Line & Polygon clipping algorithms
    4. **Filling**: Boundary & Flood fill, Scanline
    5. **Proyeksi 3D**: Orthographic & Perspective projection
    6. **Shading**: Flat, Gouraud, Phong shading models
    
    ### Teknologi yang Digunakan
    
    | Komponen | Teknologi |
    |----------|-----------|
    | **Framework** | Streamlit 1.28+ |
    | **Visualisasi** | Plotly, Pillow, Matplotlib |
    | **Komputasi** | NumPy, SciPy |
    | **Interaktif** | Streamlit-Drawable-Canvas |
    | **Bahasa** | Python 3.8+ |
    
    ### Pengembang
    
    Aplikasi ini dikembangkan sebagai bagian dari Ujian Tengah Semester Grafika Komputer.
    1. Ahmad Raihan
    2. Falih Elmanda Ghaisan
    3. Juen Denardu
    4. Muhammad Rafif Dwiarka
    """)

# --- Tips Section --- #
with st.expander("Tips Penggunaan", expanded=False):
    st.markdown("""
    ### Maksimalkan Pembelajaran Anda
    
    - **Eksperimen Aktif**: Ubah parameter dan amati efeknya secara real-time
    - **Bandingkan Metode**: Gunakan fitur perbandingan untuk memahami perbedaan algoritma
    - **Catat Observasi**: Perhatikan kompleksitas dan kualitas output dari setiap metode
    - **Latihan Mandiri**: Coba implementasi sendiri setelah memahami konsep
    
    ### Navigasi Efektif
    
    - Gunakan **sidebar** untuk berpindah antar topik
    - Setiap halaman memiliki struktur: Teori → Demo → Latihan
    - Bookmark halaman favorit di browser Anda
    - Gunakan mode fullscreen (F11) untuk fokus maksimal
    
    ### Troubleshooting
    
    - **Loading lambat?** Refresh halaman atau kurangi kompleksitas parameter
    - **Visualisasi tidak muncul?** Pastikan browser mendukung WebGL
    - **Error?** Cek console browser (F12) untuk detail error
    """)

# --- Sidebar Enhancement --- #
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Pengaturan")
st.sidebar.caption("Streamlit memiliki toggle tema bawaan di menu (☰)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Dibuat menggunakan Streamlit | © 2025 Grafika Komputer </p>
</div>
""", unsafe_allow_html=True)