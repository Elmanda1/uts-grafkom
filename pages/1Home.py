import streamlit as st
from config import PAGE_CONFIG
from utils.helpers import load_css

st.set_page_config(**PAGE_CONFIG)

# Memuat CSS kustom
try:
    load_css("assets/styles/custom.css")
except Exception as e:
    st.warning(f"⚠️ CSS kustom tidak dimuat: {e}")

def show_home():
    """
    Menampilkan konten halaman utama dengan tampilan modern dan interaktif.
    """
    
    # --- Hero Section --- #
    st.markdown("""
        <div class="header-container">
            <h1>Grafika Komputer</h1>
            <p class="subtitle">Konsep fundamental grafika komputer dengan visualisasi real-time</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Welcome Section --- #
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### Selamat Datang!")
        st.markdown("""
        Aplikasi pembelajaran ini dirancang khusus untuk membantu Anda memahami 
        **konsep-konsep inti grafika komputer** melalui pendekatan yang **interaktif** 
        dan **visual**. 
        
        Dari algoritma dasar menggambar garis hingga teknik shading 3D yang kompleks, 
        setiap materi disajikan dengan:
        
        - **Penjelasan Konsep** yang jelas dan terstruktur
        - **Demo Interaktif** untuk eksperimen langsung
        - **Perbandingan Algoritma** dengan visualisasi side-by-side
        - **Implementasi Kode** yang dapat dipelajari
        """)
    
    with col2:
        st.info("""
        ### Mulai Belajar
        
        **Cara menggunakan aplikasi:**
        
        1. Pilih **topik** dari sidebar
        2. Baca **penjelasan konsep**
        3. Ubah **parameter** interaktif
        4. Amati **hasil visualisasi**
        5. Pahami **perbedaan algoritma**
        
        *Gunakan sidebar untuk navigasi!*
        """)
    
    st.markdown("---")
    
    # --- Detailed Topics --- #
    st.markdown("### 📖 Materi Per Minggu")
    
    # Daftar topik dengan detail lebih lengkap
    topics = [
        {
            "icon": "",
            "title": "Home: Dashboard",
            "week": "Orientasi",
            "description": "Halaman utama dengan overview materi dan panduan navigasi aplikasi.",
            "concepts": ["Struktur Aplikasi", "Navigasi", "Overview Materi"],
            "difficulty": "Beginner"
        },
        {
            "icon": "",
            "title": "Week 1: Pengantar Grafika Komputer",
            "week": "Minggu 1",
            "description": "Memahami sejarah, aplikasi, dan konsep fundamental grafika komputer.",
            "concepts": ["Sejarah CG", "Aplikasi Modern", "Pixel & Rasterization", "Koordinat 2D/3D"],
            "difficulty": "Beginner"
        },
        {
            "icon": "",
            "title": "Week 2: Transformasi 2D",
            "week": "Minggu 2",
            "description": "Manipulasi objek 2D menggunakan matriks transformasi.",
            "concepts": ["Translation", "Rotation", "Scaling", "Shearing", "Matrix Composition"],
            "difficulty": "Beginner"
        },
        {
            "icon": "",
            "title": "Week 3: Algoritma Garis & Lingkaran",
            "week": "Minggu 3",
            "description": "Visualisasi dan perbandingan algoritma menggambar primitif.",
            "concepts": ["DDA Algorithm", "Bresenham Line", "Bresenham Circle", "Midpoint Circle"],
            "difficulty": "Intermediate"
        },
        {
            "icon": "",
            "title": "Week 4: Polygon Filling",
            "week": "Minggu 4",
            "description": "Teknik mengisi area poligon dengan berbagai metode.",
            "concepts": ["Scanline Fill", "Flood Fill", "Boundary Fill", "Pattern Fill"],
            "difficulty": "Intermediate"
        },
        {
            "icon": "",
            "title": "Week 5: Model Warna & Pencahayaan",
            "week": "Minggu 5",
            "description": "Eksplorasi model warna dan dasar-dasar pencahayaan 3D.",
            "concepts": ["RGB Model", "HSV/HSL", "CMYK", "Ambient Light", "Diffuse Light"],
            "difficulty": "Intermediate"
        },
        {
            "icon": "",
            "title": "Week 6: Shading Models",
            "week": "Minggu 6",
            "description": "Perbandingan teknik shading untuk rendering objek 3D realistis.",
            "concepts": ["Flat Shading", "Gouraud Shading", "Phong Shading", "Normal Vectors"],
            "difficulty": "Advanced"
        },
        {
            "icon": "",
            "title": "Week 7: Texture Mapping",
            "week": "Minggu 7",
            "description": "Penerapan tekstur pada permukaan objek 3D.",
            "concepts": ["UV Mapping", "Texture Coordinates", "Filtering", "Wrapping"],
            "difficulty": "Advanced"
        }
    ]
    
    # Tampilkan dalam bentuk ekspander dengan styling yang lebih baik
    for idx, topic in enumerate(topics, 1):
        with st.expander(f"{topic['icon']} **{topic['title']}**", expanded=(idx == 1)):
            topic_col1, topic_col2 = st.columns([3, 1])
            
            with topic_col1:
                st.markdown(f"**{topic['week']}** | Tingkat: `{topic['difficulty']}`")
                st.write(topic['description'])
                
                st.markdown("**Konsep yang Dipelajari:**")
                concepts_list = " • ".join(topic['concepts'])
                st.markdown(f"*{concepts_list}*")
    
    st.markdown("---")
    
    # --- Team Section --- #
    st.markdown("### Tim Pengembang")
    
    st.markdown("""
    Aplikasi ini dikembangkan sebagai bagian dari pembelajaran Grafika Komputer 
    dengan kontribusi dari berbagai anggota tim:
    """)
    
    team_col1, team_col2 = st.columns(2)
    
    with team_col1:
        st.markdown("""
        **Development & Foundation**
        - **Juen Denardy** - Core Architecture
        - **Falih Elmanda Ghaisan** - Line & Polygon Algorithms
        
        **Visualization & Advanced Topics**
        - **Muhammad Rafif Dwiarka** - Color Models & Shading
        - **Ahmad Raihan** - Documentation & Asset Management
        """)
    
    with team_col2:
        st.info("""
        **Informasi Kontak**
        
        Untuk pertanyaan, saran, atau pelaporan bug:
        
        - Email: rapipaja@gmail.com
        - Discord: @rapipupipu
        - Issues: GitHub repository Duwii-0
        
        *Kami senang mendengar feedback Anda!*
        """)
    
    st.markdown("---")
    
    # --- Quick Tips --- #
    with st.expander(" Tips untuk Pembelajaran Efektif", expanded=False):
        tip_col1, tip_col2 = st.columns(2)
        
        with tip_col1:
            st.markdown("""
            **Strategi Belajar:**
            - Mulai dari Week 1 untuk fondasi yang kuat
            - Luangkan waktu untuk eksperimen dengan setiap demo
            - Catat observasi Anda tentang perbedaan algoritma
            - Coba implementasi sendiri setelah memahami konsep
            """)
        
        with tip_col2:
            st.markdown("""
            **⚡ Navigasi Cepat:**
            - Gunakan sidebar untuk berpindah antar topik
            - Bookmark halaman favorit di browser
            - Gunakan mode fullscreen (F11) untuk fokus maksimal
            - Refresh halaman jika visualisasi tidak muncul
            """)
    
    # --- Footer --- #
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Dibuat menggunakan Streamlit | © 2025 Grafika Komputer </p>
    </div>
    """, unsafe_allow_html=True)

# Entry point
if __name__ == "__main__":
    show_home()