"""
Halaman Utama (Dashboard) Aplikasi.

Menampilkan halaman selamat datang, deskripsi singkat proyek, dan ringkasan
topik-topik yang akan dibahas di setiap pekannya.
"""

import streamlit as st
from config import PAGE_CONFIG
from utils.helpers import load_css

st.set_page_config(**PAGE_CONFIG)
# load_css("assets/styles/custom.css") # Uncomment jika file CSS sudah ada

def show_home():
    """
    Menampilkan konten halaman utama.
    """
    st.title("🎨 Selamat Datang di Aplikasi Pembelajaran Grafika Komputer")
    st.markdown("---" )

    st.info(
        "**Gunakan sidebar di sebelah kiri untuk menavigasi ke materi yang berbeda.**\n\n" 
        "Aplikasi ini dirancang untuk memberikan pemahaman interaktif tentang konsep-konsep inti dalam grafika komputer, "
        "mulai dari dasar-dasar hingga teknik-teknik yang lebih canggih."
    )

    st.header("Struktur Materi Pembelajaran")
    st.markdown(
        """
        Setiap halaman (minggu) akan fokus pada topik tertentu. Anda akan menemukan:
        - **Penjelasan Konsep:** Teori dasar di balik setiap topik.
        - **Visualisasi Interaktif:** Demo yang memungkinkan Anda bereksperimen dengan parameter secara real-time.
        - **Perbandingan Algoritma:** Analisis performa dan visual antara berbagai metode.
        - **Tampilan Kode:** Implementasi dari algoritma yang dibahas.
        """
    )

    # Daftar Topik per Minggu
    topics = {
        "🏠 Home": "Halaman dashboard ini.",
        "📚 Week 1: Pengantar": "Sejarah, aplikasi, dan konsep dasar grafika komputer.",
        "🔄 Week 2: Transformasi 2D": "Translasi, rotasi, skala, dan shear pada objek 2D.",
        "📏 Week 3: Algoritma Garis": "Visualisasi dan perbandingan algoritma DDA dan Bresenham.",
        "🎨 Week 4: Polygon Fill": "Teknik mengisi area poligon seperti Scanline dan Flood Fill.",
        "🌈 Week 5: Model Warna": "Eksplorasi model warna RGB, HSV, CMYK dan pencahayaan dasar.",
        "💡 Week 6: Shading": "Perbandingan teknik shading Flat, Gouraud, dan Phong pada objek 3D.",
        "🖼️ Week 7: Texturing": "Dasar-dasar pemetaan tekstur pada objek 3D.",
    }

    for title, description in topics.items():
        with st.expander(f"**{title}**"):
            st.write(description)

    st.markdown("---" )
    st.header("Tim Pengembang")
    st.markdown(
        """
Aplikasi ini dikembangkan oleh:
        - **Person 1:** Foundation & Week 1-2
        - **Person 2:** Week 3-4 (Line & Polygon Algorithms)
        - **Person 3:** Week 5-6 (Color & Lighting)
        - **Person 4:** Week 7, Documentation & Assets
        """
    )

if __name__ == "__main__":
    show_home()
