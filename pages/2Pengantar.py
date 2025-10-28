"""
Halaman Minggu 1: Pengantar Grafika Komputer.

Berisi materi tekstual mengenai sejarah, aplikasi, dan konsep dasar
dalam grafika komputer dengan visualisasi interaktif.
"""

import streamlit as st
from config import PAGE_CONFIG
from PIL import Image
import os

st.set_page_config(**PAGE_CONFIG)

def show_week1():
    """
    Menampilkan materi pengantar grafika komputer dengan layout yang menarik.
    """
    
    # --- Header --- #
    st.markdown("""
        <div class="header-container">
            <h1>📚 Minggu 1: Pengantar Grafika Komputer</h1>
            <p class="subtitle">Sejarah, Aplikasi, dan Konsep Fundamental</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Intro Section --- #
    st.markdown("""
    ### 🎯 Tujuan Pembelajaran
    
    Setelah mempelajari materi ini, Anda diharapkan dapat:
    - 📖 Memahami sejarah perkembangan grafika komputer
    - 🌍 Mengenali berbagai aplikasi grafika komputer dalam kehidupan sehari-hari
    - 🧩 Memahami konsep-konsep fundamental dalam grafika komputer
    - 🔄 Mengenal pipeline rendering dan sistem koordinat
    """)
    
    st.markdown("---")
    
    # --- Timeline Sejarah --- #
    st.header("🕰️ Sejarah Singkat Grafika Komputer")
    
    st.markdown("""
    Grafika komputer telah berkembang pesat sejak pertama kali muncul pada tahun 1950-an.
    Mari kita telusuri perjalanan evolusinya:
    """)
    
    # Timeline dengan expander
    timeline_data = [
        {
            "year": "1951",
            "title": "Era Awal: Komputer Whirlwind",
            "description": "Komputer Whirlwind di MIT menampilkan data secara visual di layar CRT untuk pertama kalinya.",
            "icon": "🖥️",
            "color": "blue"
        },
        {
            "year": "1963",
            "title": "Revolusi Sketchpad",
            "description": "Ivan Sutherland menciptakan **Sketchpad**, program interaktif pertama yang memungkinkan pengguna menggambar dengan *light pen*. Dianggap sebagai cikal bakal CAD (Computer-Aided Design).",
            "icon": "✏️",
            "color": "green"
        },
        {
            "year": "1970-an",
            "title": "Fondasi Algoritma",
            "description": "Perkembangan algoritma fundamental seperti algoritma garis Bresenham, algoritma z-buffer untuk visibilitas, dan model pencahayaan Phong yang masih digunakan hingga sekarang.",
            "icon": "🔬",
            "color": "orange"
        },
        {
            "year": "1980-an",
            "title": "Era CGI Dimulai",
            "description": "Munculnya workstation grafis dari Silicon Graphics (SGI) dan film dengan CGI seperti *Tron* (1982) yang mengubah industri hiburan.",
            "icon": "🎬",
            "color": "red"
        },
        {
            "year": "1990-an",
            "title": "Akselerasi 3D untuk Semua",
            "description": "Kartu grafis 3D seperti Voodoo (3dfx) dan GeForce (NVIDIA) membawa grafis 3D ke PC rumahan. Film *Toy Story* (1995) menjadi film panjang CGI penuh pertama.",
            "icon": "🎮",
            "color": "purple"
        },
        {
            "year": "2000-an+",
            "title": "Era Modern: Real-time & Fotorealisme",
            "description": "Perkembangan pesat dalam real-time rendering, GPGPU, ray tracing real-time, dan fotorealisme yang mencapai tingkat yang belum pernah terjadi sebelumnya.",
            "icon": "🚀",
            "color": "indigo"
        }
    ]
    
    for item in timeline_data:
        with st.expander(f"{item['icon']} **{item['year']}: {item['title']}**"):
            st.markdown(f"**Era:** {item['year']}")
            st.write(item['description'])
    
    st.markdown("---")
    
    # --- Aplikasi Section --- #
    st.header("🌍 Aplikasi Grafika Komputer")
    
    st.markdown("""
    Grafika komputer ada di mana-mana dalam kehidupan modern kita. 
    Berikut adalah berbagai bidang aplikasi yang memanfaatkan teknologi grafika komputer:
    """)
    
    # Aplikasi dalam cards
    app_col1, app_col2 = st.columns(2)
    
    with app_col1:
        st.markdown("""
        <div class="nav-card">
            <h4>🎬 Hiburan & Media</h4>
            <p><strong>Film:</strong> Visual effects, animasi karakter CGI</p>
            <p><strong>Video Games:</strong> Rendering real-time, simulasi fisika</p>
            <p><strong>Animasi:</strong> Serial TV, iklan, konten digital</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>📐 Desain & Rekayasa</h4>
            <p><strong>CAD/CAM:</strong> Desain produk, manufaktur</p>
            <p><strong>Arsitektur:</strong> Visualisasi bangunan 3D</p>
            <p><strong>Desain Industri:</strong> Prototipe virtual</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>🔬 Visualisasi Ilmiah</h4>
            <p><strong>Medis:</strong> MRI, CT scan, simulasi operasi</p>
            <p><strong>Sains:</strong> Simulasi fluida, molekul, astronomi</p>
            <p><strong>Data:</strong> Visualisasi data statistik kompleks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with app_col2:
        st.markdown("""
        <div class="nav-card">
            <h4>✈️ Pelatihan & Simulasi</h4>
            <p><strong>Penerbangan:</strong> Flight simulator untuk pilot</p>
            <p><strong>Militer:</strong> Simulasi pertempuran dan strategi</p>
            <p><strong>Medis:</strong> Pelatihan operasi virtual</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>💻 Antarmuka & Interaksi</h4>
            <p><strong>GUI:</strong> Sistem operasi modern (Windows, macOS)</p>
            <p><strong>Web:</strong> Visualisasi interaktif, WebGL</p>
            <p><strong>Mobile:</strong> Aplikasi iOS/Android</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>🥽 VR & AR</h4>
            <p><strong>Virtual Reality:</strong> Gaming, pelatihan imersif</p>
            <p><strong>Augmented Reality:</strong> Pokemon GO, filter Instagram</p>
            <p><strong>Mixed Reality:</strong> Microsoft HoloLens, Apple Vision Pro</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Konsep Dasar Section --- #
    st.header("🧩 Konsep Fundamental")
    
    # Tabs untuk konsep
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Raster vs Vektor", 
        "🔄 Pipeline Grafika", 
        "📍 Sistem Koordinat",
        "🎨 Model Warna"
    ])
    
    with tab1:
        st.subheader("Raster vs Vektor")
        
        col_raster, col_vektor = st.columns(2)
        
        with col_raster:
            st.markdown("""
            ### 🖼️ Grafik Raster (Bitmap)
            
            **Definisi:**
            Gambar direpresentasikan sebagai grid piksel (picture elements).
            
            **Karakteristik:**
            - ✅ Cocok untuk foto dan gambar kompleks
            - ✅ Detail warna dan tekstur yang tinggi
            - ❌ Kehilangan kualitas saat diperbesar (pixelated)
            - ❌ Ukuran file relatif besar
            
            **Format:**
            - JPEG (foto, kompresi lossy)
            - PNG (transparansi, kompresi lossless)
            - BMP (tanpa kompresi)
            - GIF (animasi sederhana)
            
            **Aplikasi:**
            - Fotografi digital
            - Editing gambar (Photoshop)
            - Texturing dalam 3D
            """)
        
        with col_vektor:
            st.markdown("""
            ### 📐 Grafik Vektor
            
            **Definisi:**
            Gambar direpresentasikan oleh objek geometris yang didefinisikan dengan persamaan matematika.
            
            **Karakteristik:**
            - ✅ Dapat diskalakan tanpa kehilangan kualitas
            - ✅ Ukuran file kecil
            - ✅ Mudah diedit (objek independen)
            - ❌ Tidak cocok untuk gambar kompleks seperti foto
            
            **Format:**
            - SVG (Scalable Vector Graphics)
            - AI (Adobe Illustrator)
            - EPS (Encapsulated PostScript)
            - PDF (untuk grafis)
            
            **Aplikasi:**
            - Logo dan branding
            - Ilustrasi dan icon
            - Font (TrueType, OpenType)
            - Peta dan diagram
            """)
    
    with tab2:
        st.subheader("Pipeline Rendering Grafika")
        
        st.markdown("""
        Pipeline rendering adalah serangkaian langkah yang mengubah model 3D menjadi gambar 2D di layar.
        Proses ini terjadi sangat cepat (60+ kali per detik untuk 60 FPS).
        """)
        
        pipeline_stages = [
            {
                "stage": "1️⃣ Application Stage",
                "processor": "CPU",
                "description": "Logika aplikasi, AI, deteksi tabrakan, input handling",
                "example": "Game logic, physics simulation"
            },
            {
                "stage": "2️⃣ Geometry Processing",
                "processor": "GPU",
                "description": "Transformasi vertex, proyeksi 3D→2D, pencahayaan per-vertex",
                "example": "Model-View-Projection transformation"
            },
            {
                "stage": "3️⃣ Rasterization",
                "processor": "GPU",
                "description": "Mengubah primitif (segitiga) menjadi fragmen (calon piksel)",
                "example": "Scanline conversion, interpolasi atribut"
            },
            {
                "stage": "4️⃣ Fragment Processing",
                "processor": "GPU",
                "description": "Menentukan warna setiap fragmen (per-pixel shading, texturing)",
                "example": "Phong shading, texture mapping"
            },
            {
                "stage": "5️⃣ Per-Fragment Operations",
                "processor": "GPU",
                "description": "Z-buffering (depth test), alpha blending, stencil test",
                "example": "Menentukan piksel mana yang visible"
            }
        ]
        
        for stage in pipeline_stages:
            with st.expander(f"**{stage['stage']}** - {stage['processor']}"):
                st.markdown(f"**Fungsi:** {stage['description']}")
                st.markdown(f"**Contoh:** {stage['example']}")
    
    with tab3:
        st.subheader("Sistem Koordinat dalam Grafika")
        
        st.markdown("""
        Dalam grafika komputer, objek melewati berbagai sistem koordinat sebelum akhirnya 
        ditampilkan di layar:
        """)
        
        coord_col1, coord_col2 = st.columns(2)
        
        with coord_col1:
            st.info("""
            **🌍 Local/Object Space**
            - Koordinat relatif terhadap titik pusat objek
            - Digunakan saat modeling
            
            **🗺️ World Space**
            - Koordinat global dalam scene
            - Semua objek ditempatkan di sini
            """)
        
        with coord_col2:
            st.info("""
            **👁️ View/Camera Space**
            - Koordinat relatif terhadap kamera
            - Origin di posisi kamera
            
            **📺 Screen Space**
            - Koordinat 2D akhir di layar
            - Pixel coordinates (x, y)
            """)
        
        st.markdown("""
        **Transformasi Koordinat:**
        ```
        Local → World → View → Projection → Screen
        (Model)  (World) (View)  (Clip)      (NDC)
        ```
        """)
    
    with tab4:
        st.subheader("Model Warna Digital")
        
        color_col1, color_col2, color_col3 = st.columns(3)
        
        with color_col1:
            st.markdown("""
            **🔴🟢🔵 RGB**
            
            Model warna **aditif** untuk layar.
            
            - R: Red (0-255)
            - G: Green (0-255)
            - B: Blue (0-255)
            
            **Contoh:**
            - Putih: (255,255,255)
            - Hitam: (0,0,0)
            - Merah: (255,0,0)
            
            **Digunakan:** Monitor, TV, web
            """)
        
        with color_col2:
            st.markdown("""
            **🌈 HSV/HSL**
            
            Model warna berbasis persepsi.
            
            - H: Hue (0-360°)
            - S: Saturation (0-100%)
            - V: Value/L: Lightness
            
            **Keuntungan:**
            - Lebih intuitif untuk manusia
            - Mudah untuk color picking
            
            **Digunakan:** Color pickers, editing
            """)
        
        with color_col3:
            st.markdown("""
            **🖨️ CMYK**
            
            Model warna **subtraktif** untuk cetak.
            
            - C: Cyan
            - M: Magenta
            - Y: Yellow
            - K: Key (Black)
            
            **Digunakan:**
            - Printing
            - Publikasi cetak
            - Desain grafis
            """)
    
    st.markdown("---")
    
    # --- Image Section (with error handling) --- #
    st.header("🖼️ Visualisasi Grafika Komputer")
    
    image_path = "assets/images/IU.jpeg"
    
    try:
        if os.path.exists(image_path):
            image = Image.open(image_path)
            st.image(image, caption="Contoh Aplikasi Grafika Komputer", use_container_width=True)
        else:
            st.warning(f"⚠️ Gambar tidak ditemukan di: `{image_path}`")
            st.info("""
            **Tips:** Pastikan struktur folder Anda seperti ini:
            ```
            uts-grafkom/
            ├── assets/
            │   └── images/
            │       └── IU.jpeg
            └── pages/
                └── 2_📚_Week1_Pengantar.py
            ```
            """)
    except Exception as e:
        st.error(f"❌ Error memuat gambar: {e}")
        st.info("Gambar akan ditampilkan setelah masalah NumPy teratasi.")
    
    st.markdown("---")
    
    # --- Quiz/Review Section --- #
    with st.expander("📝 Uji Pemahaman Anda", expanded=False):
        st.markdown("""
        ### Pertanyaan Review:
        
        1. **Sejarah:** Siapa yang menciptakan Sketchpad dan mengapa penting?
        2. **Aplikasi:** Sebutkan 3 bidang yang menggunakan grafika komputer dan contohnya.
        3. **Konsep:** Apa perbedaan utama antara grafik raster dan vektor?
        4. **Pipeline:** Sebutkan 5 tahap dalam rendering pipeline.
        5. **Warna:** Kapan Anda sebaiknya menggunakan RGB vs CMYK?
        
        ### Aktivitas:
        - Cari contoh aplikasi grafika komputer dalam kehidupan sehari-hari Anda
        - Identifikasi apakah sebuah gambar menggunakan raster atau vektor
        - Eksplorasi color picker dan perhatikan konversi RGB ↔ HSV
        """)
    
    # --- Navigation Tips --- #
    st.success("""
    ✅ **Selamat!** Anda telah menyelesaikan Minggu 1.
    
    Lanjutkan ke **Week 2: Transformasi 2D** untuk mempelajari bagaimana 
    memanipulasi objek dalam ruang 2D menggunakan matriks transformasi.
    """)
    
    # --- Footer --- #
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>📚 Week 1: Pengantar Grafika Komputer | Next: Week 2 - Transformasi 2D →</p>
    </div>
    """, unsafe_allow_html=True)

# Entry point
if __name__ == "__main__":
    show_week1()