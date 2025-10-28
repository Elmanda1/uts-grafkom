"""
Halaman Minggu 1: Pengantar Grafika Komputer.

Berisi materi tekstual mengenai sejarah, aplikasi, dan konsep dasar
dalam grafika komputer dengan visualisasi interaktif.
"""

import streamlit as st
from config import PAGE_CONFIG
from utils.helpers import load_css
from PIL import Image
import os

st.set_page_config(**PAGE_CONFIG)

# Memuat CSS kustom
try:
    load_css("assets/styles/custom.css")
except Exception as e:
    st.warning(f"⚠️ CSS kustom tidak dimuat: {e}")

def show_week1():
    """
    Menampilkan materi pengantar grafika komputer dengan layout yang menarik.
    """
    
    # --- Hero Section --- #
    st.markdown("""
        <div class="header-container">
            <h1>Pengantar Grafika Komputer</h1>
            <p class="subtitle">Sejarah, Aplikasi, dan Konsep Fundamental</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Introduction Section --- #
    intro_col1, intro_col2 = st.columns([3, 2])
    
    with intro_col1:
        st.markdown("### Tujuan Pembelajaran")
        st.markdown("""
        Pada minggu pertama ini, Anda akan membangun fondasi pemahaman tentang 
        grafika komputer yang akan menjadi dasar untuk materi-materi selanjutnya:
        
        - **Sejarah Perkembangan** - Memahami evolusi grafika komputer dari era 1950-an hingga modern
        - **Aplikasi Praktis** - Mengenali berbagai penerapan grafika komputer dalam kehidupan sehari-hari
        - **Konsep Fundamental** - Memahami prinsip-prinsip dasar seperti rasterisasi dan sistem koordinat
        - **Rendering Pipeline** - Mengenal tahapan transformasi dari 3D ke layar 2D
        - **Model Warna** - Memahami berbagai representasi warna dalam komputer
        
        Materi ini bersifat **teoritis namun interaktif**, dengan visualisasi dan contoh konkret 
        untuk memudahkan pemahaman.
        """)
    
    with intro_col2:
        st.info("""
        ### Petunjuk Belajar
        
        **Cara menggunakan halaman ini:**
        
        1. **Baca penjelasan** di setiap section
        2. **Klik expander** untuk detail lebih lanjut
        3. **Eksplorasi tabs** untuk konsep berbeda
        4. **Coba uji pemahaman** di akhir halaman
        5. **Catat konsep penting** untuk referensi
        
        *Materi ini menjadi fondasi untuk minggu-minggu berikutnya!*
        """)
    
    st.markdown("---")
    
    # --- What is Computer Graphics --- #
    with st.expander("**Apa itu Grafika Komputer?**", expanded=True):
        what_col1, what_col2 = st.columns([2, 1])
        
        with what_col1:
            st.markdown("""
            **Grafika Komputer** (Computer Graphics) adalah bidang ilmu komputer yang 
            mempelajari teknik dan metode untuk **menciptakan, memanipulasi, dan 
            menampilkan gambar** menggunakan komputer.
            
            ### Tujuan Utama:
            
            **1. Sintesis Gambar (Image Synthesis)**
            - Membuat gambar baru dari deskripsi geometris
            - Contoh: Rendering 3D, CGI dalam film
            
            **2. Manipulasi Gambar (Image Manipulation)**
            - Mengubah atau mengedit gambar yang sudah ada
            - Contoh: Photoshop, Instagram filters
            
            **3. Analisis Gambar (Image Analysis)**
            - Mengekstrak informasi dari gambar
            - Contoh: Computer Vision, Face Recognition
            
            ### Komponen Utama:
            - **Hardware:** GPU, Display devices, Input devices
            - **Software:** Graphics APIs (OpenGL, DirectX, Vulkan)
            - **Algoritma:** Rendering, transformasi, shading
            - **Matematika:** Linear algebra, geometri, kalkulus
            """)
        
        with what_col2:
            st.success("""
            **Fakta Menarik:**
            
            - Industri grafika komputer bernilai **$200+ miliar**
            
            - GPU modern dapat melakukan **10+ triliun** operasi per detik
            
            - Film CGI modern memerlukan **jutaan jam** CPU time
            
            - Game AAA menggunakan **ratusan GB** tekstur berkualitas tinggi
            """)
            
            st.info("""
            **Bidang Terkait:**
            
            - Computer Vision
            - Image Processing
            - Computational Geometry
            - Human-Computer Interaction
            - Virtual Reality
            """)
    
    st.markdown("---")
    
    # --- Timeline Sejarah --- #
    st.markdown("### Sejarah Singkat Grafika Komputer")
    
    st.markdown("""
    Grafika komputer telah berkembang dari eksperimen sederhana menjadi teknologi 
    yang mengubah cara kita berinteraksi dengan dunia digital. Mari kita telusuri 
    perjalanan evolusinya:
    """)
    
    # Timeline dengan expander yang lebih detail
    timeline_data = [
        {
            "year": "1951",
            "title": "Era Awal: Komputer Whirlwind",
            "description": """
            Komputer **Whirlwind I** di MIT menjadi komputer pertama yang menampilkan 
            informasi grafis secara real-time pada layar CRT (Cathode Ray Tube). 
            
            **Pencapaian:**
            - Display vektor pertama
            - Basis untuk sistem pertahanan udara SAGE
            - Membuktikan potensi visualisasi komputer
            
            **Dampak:** Membuka era baru dalam interaksi manusia-komputer
            """,
            "icon": "🖥️",
            "color": "blue"
        },
        {
            "year": "1963",
            "title": "Revolusi Sketchpad",
            "description": """
            **Ivan Sutherland** menciptakan **Sketchpad**, program interaktif revolusioner 
            yang memungkinkan pengguna menggambar langsung di layar menggunakan light pen.
            
            **Inovasi Utama:**
            - Object-oriented programming concepts
            - Constraint-based drawing
            - Hierarchical modeling
            - GUI manipulation langsung
            
            **Signifikansi:** 
            - Disertasi PhD Sutherland memenangkan Turing Award (1988)
            - Cikal bakal CAD (Computer-Aided Design)
            - Fondasi untuk modern GUI
            
            **Legacy:** Konsep-konsep Sketchpad masih digunakan dalam software desain modern
            """,
            "icon": "✏️",
            "color": "green"
        },
        {
            "year": "1970-an",
            "title": "Fondasi Algoritma & Teori",
            "description": """
            Era pembentukan fondasi teoritis dan algoritmik grafika komputer modern.
            
            **Algoritma Fundamental:**
            - **Bresenham's Line Algorithm** (1965): Menggambar garis efisien
            - **Z-Buffer** (1974): Menentukan visibilitas objek
            - **Phong Shading** (1975): Model pencahayaan realistis
            - **Ray Tracing** (1979): Rendering fotorealistis
            
            **Institusi Penting:**
            - University of Utah (program grafika pertama)
            - Xerox PARC (GUI development)
            - Stanford & MIT (computer vision)
            
            **Buku Penting:**
            - "Principles of Interactive Computer Graphics" (1973)
            
            **Dampak:** Algoritma-algoritma ini masih digunakan hingga sekarang
            """,
            "icon": "🔬",
            "color": "orange"
        },
        {
            "year": "1980-an",
            "title": "Era CGI & Komersial",
            "description": """
            Grafika komputer mulai masuk ke mainstream entertainment dan bisnis.
            
            **Hardware:**
            - **Silicon Graphics (SGI)** menciptakan workstation grafis profesional
            - Munculnya graphics accelerators
            
            **Film Milestone:**
            - **Tron** (1982): 15 menit CGI pertama dalam film live-action
            - **The Last Starfighter** (1984): Extensive CGI
            - **Young Sherlock Holmes** (1985): CG character pertama
            
            **Software:**
            - Adobe Photoshop (1988)
            - Autodesk 3D Studio (1988)
            - Pixar RenderMan (1989)
            
            **Industry:**
            - Pixar Animation Studios didirikan (1986)
            - SIGGRAPH menjadi konferensi utama
            
            **Dampak:** CGI mulai menjadi industri bernilai miliaran dollar
            """,
            "icon": "🎬",
            "color": "red"
        },
        {
            "year": "1990-an",
            "title": "Akselerasi 3D untuk Konsumen",
            "description": """
            Era demokratisasi grafika 3D - dari workstation mahal ke PC rumahan.
            
            **Hardware Revolution:**
            - **3dfx Voodoo** (1996): Kartu grafis 3D terjangkau pertama
            - **NVIDIA GeForce 256** (1999): GPU term coined, hardware T&L
            - **ATI Radeon** (2000): Pesaing utama NVIDIA
            
            **Gaming:**
            - **Doom** (1993): 3D rendering real-time populer
            - **Quake** (1996): True 3D dengan OpenGL
            - **Half-Life** (1998): Advanced 3D storytelling
            
            **Film Milestone:**
            - **Toy Story** (1995): Film CGI full-length pertama (77 menit rendering!)
            - **Jurassic Park** (1993): CG dinosaurus photorealistic
            - **The Matrix** (1999): Bullet time effect
            
            **APIs:**
            - OpenGL menjadi standar
            - DirectX untuk Windows gaming
            
            **Dampak:** 3D graphics menjadi accessible untuk semua orang
            """,
            "icon": "🎮",
            "color": "purple"
        },
        {
            "year": "2000-an",
            "title": "Era Programmable Shaders",
            "description": """
            Munculnya programmable graphics pipeline yang mengubah segalanya.
            
            **GPU Evolution:**
            - Programmable vertex & pixel shaders
            - Unified shader architecture
            - GPGPU (General Purpose GPU computing)
            - CUDA & OpenCL
            
            **Teknologi Baru:**
            - **HDR Rendering** (High Dynamic Range)
            - **Normal Mapping** & **Parallax Mapping**
            - **Deferred Rendering**
            - **Screen Space Ambient Occlusion**
            
            **Film:**
            - **Avatar** (2009): Motion capture revolutionary
            - **Lord of the Rings** trilogy: Massive crowd simulation
            - Pixar films mencapai fotorealisme tinggi
            
            **Gaming:**
            - Crysis (2007): Benchmark grafis
            - Unreal Engine 3
            - Next-gen consoles (PS3, Xbox 360)
            
            **Dampak:** Artists mendapat kontrol penuh atas rendering pipeline
            """,
            "icon": "🎨",
            "color": "pink"
        },
        {
            "year": "2010-an+",
            "title": "Era Modern: Real-time Ray Tracing & AI",
            "description": """
            Teknologi yang dulunya hanya untuk film, kini real-time dalam games.
            
            **Breakthrough Technologies:**
            - **Real-time Ray Tracing** (NVIDIA RTX, 2018)
            - **Machine Learning** untuk graphics (DLSS, upscaling)
            - **Physically Based Rendering** (PBR) menjadi standar
            - **Photogrammetry** untuk assets realistis
            
            **Hardware:**
            - GPU dengan dedicated RT cores
            - Tensor cores untuk AI
            - 8K rendering capabilities
            
            **VR/AR:**
            - Oculus Rift, HTC Vive
            - Microsoft HoloLens
            - Apple Vision Pro (2024)
            
            **Film & TV:**
            - **The Mandalorian** (2019): LED wall virtual production
            - Marvel CGI achieving photorealism
            - Real-time rendering dalam production
            
            **Game Engines:**
            - Unreal Engine 5 (Nanite, Lumen)
            - Unity HDRP
            
            **Trends:**
            - Cloud gaming & streaming
            - Neural rendering
            - Digital humans
            - Metaverse applications
            
            **Dampak:** Batas antara real-time dan offline rendering menghilang
            """,
            "icon": "🚀",
            "color": "indigo"
        }
    ]
    
    for idx, item in enumerate(timeline_data, 1):
        with st.expander(f"{item['icon']} **{item['year']}: {item['title']}**", expanded=(idx==1)):
            st.markdown(item['description'])
            
            if idx == 1:
                st.image("https://via.placeholder.com/600x200/1E88E5/FFFFFF?text=Whirlwind+Computer", 
                        use_container_width=True)
    
    st.markdown("---")
    
    # --- Aplikasi Section --- #
    st.markdown("### Aplikasi Grafika Komputer")
    
    st.markdown("""
    Grafika komputer ada di mana-mana dalam kehidupan modern kita. Teknologi ini 
    tidak hanya untuk hiburan, tetapi juga untuk pendidikan, kesehatan, sains, 
    dan berbagai bidang profesional lainnya.
    """)
    
    # Aplikasi dalam cards dengan detail lebih lengkap
    app_col1, app_col2 = st.columns(2)
    
    with app_col1:
        st.markdown("""
        <div class="nav-card">
            <h4>Hiburan & Media Digital</h4>
            <p><strong>Film & TV:</strong></p>
            <ul>
                <li>Visual effects (VFX) - Marvel, Avatar</li>
                <li>Animasi karakter CGI - Pixar, Disney</li>
                <li>Virtual production - The Mandalorian</li>
            </ul>
            <p><strong>Video Games:</strong></p>
            <ul>
                <li>Real-time rendering 60+ FPS</li>
                <li>Simulasi fisika dan fluida</li>
                <li>Procedural generation</li>
            </ul>
            <p><strong>Streaming & Broadcasting:</strong></p>
            <ul>
                <li>Real-time compositing</li>
                <li>Virtual sets dan AR graphics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>Desain & Rekayasa</h4>
            <p><strong>CAD/CAM:</strong></p>
            <ul>
                <li>Desain produk manufaktur</li>
                <li>Simulasi dan testing virtual</li>
                <li>CNC programming</li>
            </ul>
            <p><strong>Arsitektur & Konstruksi:</strong></p>
            <ul>
                <li>Visualisasi bangunan 3D</li>
                <li>BIM (Building Information Modeling)</li>
                <li>Virtual walkthroughs</li>
            </ul>
            <p><strong>Desain Industri:</strong></p>
            <ul>
                <li>Prototipe virtual</li>
                <li>Ergonomics testing</li>
                <li>Material visualization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>Visualisasi Ilmiah</h4>
            <p><strong>Medis:</strong></p>
            <ul>
                <li>MRI, CT scan reconstruction</li>
                <li>Simulasi operasi</li>
                <li>Molecular visualization</li>
            </ul>
            <p><strong>Sains & Penelitian:</strong></p>
            <ul>
                <li>Simulasi fluida dinamis (CFD)</li>
                <li>Visualisasi molekul dan protein</li>
                <li>Simulasi astronomi</li>
            </ul>
            <p><strong>Data Science:</strong></p>
            <ul>
                <li>Data visualization</li>
                <li>Statistical graphics</li>
                <li>Information graphics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with app_col2:
        st.markdown("""
        <div class="nav-card">
            <h4>Pelatihan & Simulasi</h4>
            <p><strong>Penerbangan:</strong></p>
            <ul>
                <li>Flight simulator untuk pilot training</li>
                <li>Air traffic control simulation</li>
                <li>Emergency scenario practice</li>
            </ul>
            <p><strong>Militer & Pertahanan:</strong></p>
            <ul>
                <li>Combat simulation</li>
                <li>Strategy planning</li>
                <li>Vehicle operation training</li>
            </ul>
            <p><strong>Medis & Kesehatan:</strong></p>
            <ul>
                <li>Surgical simulation</li>
                <li>Anatomy learning</li>
                <li>Emergency response training</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>Antarmuka & Interaksi</h4>
            <p><strong>Desktop:</strong></p>
            <ul>
                <li>Operating systems (Windows, macOS, Linux)</li>
                <li>GUI frameworks</li>
                <li>Desktop applications</li>
            </ul>
            <p><strong>Web:</strong></p>
            <ul>
                <li>WebGL untuk 3D browser</li>
                <li>Canvas 2D rendering</li>
                <li>Interactive visualizations (D3.js)</li>
            </ul>
            <p><strong>Mobile:</strong></p>
            <ul>
                <li>iOS & Android UI</li>
                <li>Mobile games (Unity, Unreal)</li>
                <li>AR applications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="nav-card">
            <h4>VR, AR, & Mixed Reality</h4>
            <p><strong>Virtual Reality:</strong></p>
            <ul>
                <li>Immersive gaming experiences</li>
                <li>VR training simulations</li>
                <li>Social VR platforms (VRChat, Horizon)</li>
            </ul>
            <p><strong>Augmented Reality:</strong></p>
            <ul>
                <li>Pokemon GO, AR gaming</li>
                <li>Instagram/Snapchat filters</li>
                <li>IKEA Place, AR shopping</li>
            </ul>
            <p><strong>Mixed Reality:</strong></p>
            <ul>
                <li>Microsoft HoloLens enterprise</li>
                <li>Apple Vision Pro applications</li>
                <li>Industrial maintenance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Konsep Dasar Section --- #
    st.markdown("### Konsep Fundamental Grafika Komputer")
    
    st.info("""
    💡 **Catatan:** Konsep-konsep berikut adalah fondasi yang akan terus Anda gunakan 
    sepanjang pembelajaran grafika komputer. Pahami dengan baik sebelum melanjutkan 
    ke materi praktis di minggu-minggu berikutnya.
    """)
    
    # Tabs untuk konsep
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Raster vs Vektor", 
        "Pipeline Grafika", 
        "Sistem Koordinat",
        "Model Warna",
        "Pixel & Resolusi"
    ])
    
    with tab1:
        st.markdown("#### Raster vs Vektor")
        
        st.markdown("""
        Dua pendekatan fundamental untuk merepresentasikan gambar digital, 
        masing-masing dengan kelebihan dan kekurangan yang berbeda.
        """)
        
        col_raster, col_vektor = st.columns(2)
        
        with col_raster:
            st.markdown("""
            ### Grafik Raster (Bitmap)
            
            **Definisi:**
            Gambar direpresentasikan sebagai **grid piksel** (picture elements), 
            di mana setiap piksel menyimpan informasi warna spesifik.
            
            **Karakteristik:**
            - ✅ Sangat baik untuk foto dan gambar kompleks
            - ✅ Detail warna dan tekstur yang tinggi
            - ✅ Mudah untuk efek dan filter
            - ✅ Langsung dari kamera digital
            - ❌ Kehilangan kualitas saat diperbesar (pixelated)
            - ❌ Ukuran file relatif besar
            - ❌ Sulit untuk diedit individual objects
            
            **Format File:**
            - **JPEG** (.jpg, .jpeg)
              - Kompresi lossy
              - Cocok untuk foto
              - Tidak support transparansi
            
            - **PNG** (.png)
              - Kompresi lossless
              - Support transparansi (alpha channel)
              - Cocok untuk graphics dengan text
            
            - **GIF** (.gif)
              - Max 256 colors
              - Support animasi sederhana
              - Transparansi 1-bit
            
            - **BMP** (.bmp)
              - Tanpa kompresi
              - Ukuran file besar
              - Windows native format
            
            - **TIFF** (.tif, .tiff)
              - Professional photography
              - Lossless, support layers
            
            **Aplikasi Umum:**
            - Fotografi digital dan editing
            - Texture mapping dalam 3D
            - Screen captures
            - Web images
            - Digital painting (Photoshop, Procreate)
            
            **Resolusi Umum:**
            - HD: 1920×1080 px (2.07 MP)
            - 4K: 3840×2160 px (8.29 MP)
            - 8K: 7680×4320 px (33.18 MP)
            """)
        
        with col_vektor:
            st.markdown("""
            ### Grafik Vektor
            
            **Definisi:**
            Gambar direpresentasikan oleh **objek geometris** (garis, kurva, shape) 
            yang didefinisikan dengan **persamaan matematika**.
            
            **Karakteristik:**
            - ✅ Dapat diskalakan tanpa kehilangan kualitas (infinite resolution)
            - ✅ Ukuran file sangat kecil
            - ✅ Mudah diedit (objek independen)
            - ✅ Sharp di resolusi apapun
            - ✅ Ideal untuk print dalam ukuran besar
            - ❌ Tidak cocok untuk gambar kompleks seperti foto
            - ❌ Rendering bisa lambat untuk objek kompleks
            - ❌ Tidak menangkap detail natural dengan baik
            
            **Format File:**
            - **SVG** (.svg - Scalable Vector Graphics)
              - XML-based
              - Web-friendly, dapat diedit dengan text editor
              - Support CSS dan JavaScript
            
            - **AI** (.ai - Adobe Illustrator)
              - Industry standard untuk desain
              - Proprietary format
            
            - **EPS** (.eps - Encapsulated PostScript)
              - Untuk printing profesional
              - Support raster dan vektor
            
            - **PDF** (.pdf)
              - Dapat contain vektor dan raster
              - Universal format
            
            **Komponen Vektor:**
            - **Points** (vertices/anchor points)
            - **Paths** (garis lurus atau kurva Bézier)
            - **Fills** (warna solid, gradients)
            - **Strokes** (outline dengan properti)
            
            **Aplikasi Umum:**
            - Logo dan branding (scalability penting)
            - Ilustrasi dan icon design
            - Infografis dan diagram
            - Typography (font files TrueType, OpenType)
            - Peta dan technical drawings
            - Cutting machine patterns (Cricut, laser)
            
            **Tools Populer:**
            - Adobe Illustrator
            - Inkscape (free, open-source)
            - CorelDRAW
            - Affinity Designer
            - Figma (web-based)
            """)
        
        st.markdown("---")
        
        comparison_col1, comparison_col2 = st.columns(2)
        
        with comparison_col1:
            st.success("""
            **Kapan Menggunakan Raster:**
            - Foto dan gambar dengan banyak detail
            - Digital painting dan artwork
            - Texture untuk 3D models
            - Ketika final output size sudah diketahui
            - Web images (dengan optimisasi)
            """)
        
        with comparison_col2:
            st.success("""
            **Kapan Menggunakan Vektor:**
            - Logo dan brand identity
            - Icon dan UI elements
            - Infografis dan charts
            - Print materials (ukuran bervariasi)
            - Illustrations dengan clean lines
            """)
    
    with tab2:
        st.markdown("#### Pipeline Rendering Grafika")
        
        st.markdown("""
        **Graphics Pipeline** adalah serangkaian langkah yang mengubah deskripsi 3D scene 
        menjadi gambar 2D di layar Anda. Proses ini terjadi sangat cepat - **60 hingga 144 
        kali per detik** dalam aplikasi real-time seperti game!
        """)
        
        st.info("""
        💡 **Catatan:** Pipeline modern sangat dapat dikonfigurasi (programmable shaders), 
        memungkinkan artists dan programmers untuk menciptakan efek visual yang luar biasa.
        """)
        
        pipeline_stages = [
            {
                "stage": "1️⃣ Application Stage",
                "processor": "CPU",
                "description": """
                Tahap yang berjalan di CPU, menangani logika aplikasi dan persiapan data.
                
                **Proses:**
                - Logika game (AI, physics, collision detection)
                - Input handling (keyboard, mouse, gamepad)
                - Scene management (culling object yang tidak terlihat)
                - Animation updates
                - Mengirim draw calls ke GPU
                
                **Output:** Geometry data (vertices, indices) siap untuk GPU
                """,
                "example": "Game logic, physics simulation, culling"
            },
            {
                "stage": "2️⃣ Geometry Processing",
                "processor": "GPU (Vertex Shader)",
                "description": """
                Memproses setiap vertex secara parallel di GPU.
                
                **Proses:**
                - **Vertex Shader:** Transform vertices dari object space → world → view → clip space
                - **Model-View-Projection (MVP) transformation**
                - Pencahayaan per-vertex (untuk Gouraud shading)
                - Normal transformation
                - Texture coordinate generation
                
                **Transformasi Koordinat:**
                ```
                Object Space → World Space → View Space → Clip Space
                ```
                
                **Output:** Transformed vertices dalam clip space coordinates
                """,
                "example": "MVP transformation, vertex lighting"
            },
            {
                "stage": "3️⃣ Rasterization",
                "processor": "GPU (Rasterizer - Fixed Function)",
                "description": """
                Mengubah primitif geometris (triangles) menjadi fragments (calon piksel).
                
                **Proses:**
                - **Clipping:** Buang geometry di luar view frustum
                - **Perspective Division:** Clip space → NDC (Normalized Device Coordinates)
                - **Viewport transformation:** NDC → Screen space
                - **Triangle setup:** Menentukan piksel mana yang covered oleh triangle
                - **Interpolation:** Interpolasi atribut (color, texcoords, normals) dari vertices ke fragments
                
                **Scanline Conversion:**
                Menentukan piksel mana yang berada di dalam triangle menggunakan edge equations.
                
                **Output:** Fragments dengan interpolated attributes
                """,
                "example": "Scanline conversion, attribute interpolation"
            },
            {
                "stage": "4️⃣ Fragment Processing",
                "processor": "GPU (Fragment/Pixel Shader)",
                "description": """
                Menentukan warna akhir setiap fragment (per-pixel operations).
                
                **Proses:**
                - **Pixel/Fragment Shader execution**
                - Texture sampling (texture mapping)
                - Per-pixel lighting calculations (Phong, PBR)
                - Normal mapping, parallax mapping
                - Shadow calculations
                - Fog and atmospheric effects
                
                **Shading Models:**
                - Flat shading (1 color per triangle)
                - Gouraud shading (interpolate vertex colors)
                - Phong shading (interpolate normals, per-pixel lighting)
                - PBR (Physically Based Rendering)
                
                **Output:** Final color value untuk setiap fragment
                """,
                "example": "Phong shading, texture mapping, normal mapping"
            },
            {
                "stage": "5️⃣ Per-Fragment Operations",
                "processor": "GPU (Output Merger - Fixed Function)",
                "description": """
                Tahap akhir yang menentukan apakah fragment akan ditampilkan di layar.
                
                **Tests & Operations:**
                - **Scissor Test:** Buang fragments di luar rectangle
                - **Alpha Test:** Buang fragments berdasarkan alpha value
                - **Stencil Test:** Stencil buffer untuk masking effects
                - **Depth Test (Z-buffering):** Tentukan fragment terdekat ke kamera
                - **Blending:** Combine dengan color yang sudah ada di framebuffer
                - **Dithering:** Simulasi lebih banyak color
                
                **Z-Buffer/Depth Buffer:**
                Menyimpan depth value untuk setiap pixel, memastikan object 
                yang lebih dekat menutupi yang lebih jauh.
                
                **Alpha Blending:**
                ```
                C_final = C_source × α + C_dest × (1 - α)
                ```
                
                **Output:** Final pixel color di framebuffer (layar)
                """,
                "example": "Z-buffering, alpha blending, multisampling"
            }
        ]
        
        for stage in pipeline_stages:
            with st.expander(f"**{stage['stage']}** | {stage['processor']}"):
                st.markdown(stage['description'])
                st.caption(f"💡 **Contoh:** {stage['example']}")
        
        st.markdown("---")
        
        st.success("""
        **Kesimpulan Pipeline:**
        
        Setiap frame dalam game atau aplikasi 3D melewati seluruh pipeline ini. 
        Untuk 60 FPS, seluruh proses harus selesai dalam **16.67 ms**!
        
        **Modern Extensions:**
        - **Geometry Shader:** Dapat membuat/menghancurkan geometry
        - **Tessellation:** Subdivide geometry untuk detail lebih
        - **Compute Shader:** General purpose GPU computing
        - **Ray Tracing:** Alternative rendering approach
        """)
    
    with tab3:
        st.markdown("#### Sistem Koordinat dalam Grafika")
        
        st.markdown("""
        Dalam grafika komputer, sebuah objek 3D melewati **berbagai sistem koordinat** 
        (coordinate spaces/systems) sebelum akhirnya ditampilkan sebagai piksel 2D di layar. 
        Setiap space memiliki tujuan spesifik dalam rendering pipeline.
        """)
        
        coord_col1, coord_col2 = st.columns(2)
        
        with coord_col1:
            st.info("""
            **1. Local/Object Space**
            
            **Definisi:**
            Koordinat relatif terhadap **titik pusat objek itu sendiri** (object's origin).
            
            **Karakteristik:**
            - Origin (0,0,0) di center of object
            - Axes sesuai orientasi object
            - Independent dari scene
            
            **Penggunaan:**
            - Saat modeling di software 3D
            - Vertex data disimpan di space ini
            - Mudah untuk transformasi object
            
            **Contoh:**
            Vertex mobil: (2, 1, 0.5) dalam local space mobil
            """)
            
            st.info("""
            **2. World Space**
            
            **Definisi:**
            Koordinat **global dalam scene** - semua objek ditempatkan relatif 
            terhadap origin world yang sama.
            
            **Karakteristik:**
            - Origin tunggal untuk seluruh scene
            - Axes tetap (biasanya Y-up atau Z-up)
            - Posisi absolute dalam scene
            
            **Transformasi:**
            ```
            World Position = Model Matrix × Local Position
            ```
            
            **Penggunaan:**
            - Positioning objects dalam scene
            - Collision detection
            - Physics simulation
            
            **Contoh:**
            Mobil di posisi (100, 0, 50) dalam world space
            """)
            
            st.info("""
            **3. View/Camera Space**
            
            **Definisi:**
            Koordinat relatif terhadap **posisi dan orientasi kamera**.
            
            **Karakteristik:**
            - Origin di posisi kamera
            - Z-axis menunjuk ke viewing direction
            - X-axis ke kanan, Y-axis ke atas
            
            **Transformasi:**
            ```
            View Position = View Matrix × World Position
            ```
            
            **View Matrix:**
            Inverse dari camera's world transformation
            
            **Penggunaan:**
            - Lighting calculations
            - Fog effects
            - View frustum culling
            
            **Contoh:**
            Object 10 unit di depan kamera: (0, 0, -10) dalam view space
            """)
        
        with coord_col2:
            st.info("""
            **4. Clip Space**
            
            **Definisi:**
            Hasil dari **perspective projection**, mempersiapkan untuk clipping.
            
            **Karakteristik:**
            - Homogeneous coordinates (x, y, z, w)
            - View frustum menjadi cube [-w, w]³
            - Perspective division belum dilakukan
            
            **Transformasi:**
            ```
            Clip Position = Projection Matrix × View Position
            ```
            
            **Projection Types:**
            - **Perspective:** Objects jauh tampak lebih kecil
            - **Orthographic:** No perspective distortion
            
            **Penggunaan:**
            - Clipping against frustum
            - Hardware-accelerated
            """)
            
            st.info("""
            **5. NDC (Normalized Device Coordinates)**
            
            **Definisi:**
            Koordinat **ternormalisasi** setelah perspective division.
            
            **Karakteristik:**
            - Range: [-1, 1] untuk x, y, z
            - Device-independent
            - Ready untuk viewport transform
            
            **Transformasi:**
            ```
            NDC = Clip Position / w
            ```
            
            **Penggunaan:**
            - Hardware independent representation
            - Depth testing preparation
            """)
            
            st.info("""
            **6. Screen/Window Space**
            
            **Definisi:**
            Koordinat **piksel akhir** di layar/window.
            
            **Karakteristik:**
            - Origin di corner (top-left atau bottom-left)
            - X: [0, width], Y: [0, height]
            - Z: depth value [0, 1] atau [0, far]
            
            **Transformasi:**
            ```
            Screen X = (NDC.x + 1) × width / 2
            Screen Y = (NDC.y + 1) × height / 2
            ```
            
            **Penggunaan:**
            - Rasterization
            - Final pixel output
            - UI overlay positioning
            
            **Contoh:**
            Pixel (640, 360) pada layar 1280×720
            """)
        
        st.markdown("---")
        
        st.success("""
        **Full Transformation Pipeline:**
        
        ```
        Local Space (Object)
            ↓ Model Matrix
        World Space (Scene)
            ↓ View Matrix
        View Space (Camera)
            ↓ Projection Matrix
        Clip Space (Homogeneous)
            ↓ Perspective Division
        NDC (Normalized)
            ↓ Viewport Transform
        Screen Space (Pixels)
        ```
        
        **💡 Tip:** Memahami coordinate spaces sangat penting untuk debugging 
        rendering issues dan implementing advanced graphics techniques!
        """)
    
    with tab4:
        st.markdown("#### Model Warna Digital")
        
        st.markdown("""
        Warna dalam komputer dapat direpresentasikan dengan berbagai **model warna** 
        (color models). Setiap model memiliki tujuan dan aplikasi yang berbeda.
        """)
        
        color_col1, color_col2, color_col3 = st.columns(3)
        
        with color_col1:
            st.markdown("""
            **RGB (Red-Green-Blue)**
            
            Model warna **aditif** yang digunakan untuk perangkat yang **memancarkan cahaya** 
            (emissive devices).
            
            **Komponen:**
            - **R:** Red (0-255 atau 0.0-1.0)
            - **G:** Green (0-255 atau 0.0-1.0)
            - **B:** Blue (0-255 atau 0.0-1.0)
            
            **Prinsip Aditif:**
            - Menambahkan cahaya
            - R + G + B = White
            - No light = Black
            
            **Representasi:**
            - 8-bit per channel: 0-255 (24-bit color)
            - Float: 0.0-1.0 (HDR capable)
            - Hex: #RRGGBB (web colors)
            
            **Contoh Warna:**
            - White: `(255, 255, 255)` `#FFFFFF`
            - Black: `(0, 0, 0)` `#000000`
            - Red: `(255, 0, 0)` `#FF0000`
            - Green: `(0, 255, 0)` `#00FF00`
            - Blue: `(0, 0, 255)` `#0000FF`
            - Yellow: `(255, 255, 0)` `#FFFF00`
            - Cyan: `(0, 255, 255)` `#00FFFF`
            - Magenta: `(255, 0, 255)` `#FF00FF`
            
            **Color Depth:**
            - 8-bit: 256³ = 16.7 million colors
            - 10-bit: 1024³ = 1.07 billion colors
            - 16-bit (HDR): floating point range
            
            **Digunakan untuk:**
            - Monitor, TV, projector
            - Digital cameras
            - Web design (HTML/CSS)
            - Game development
            - Video editing
            """)
        
        with color_col2:
            st.markdown("""
            **HSV/HSL (Hue-Saturation-Value/Lightness)**
            
            Model warna berbasis **persepsi manusia**, lebih intuitif untuk pemilihan warna.
            
            **HSV Komponen:**
            - **H:** Hue (0-360°) - Tipe warna
              - 0°: Red
              - 120°: Green
              - 240°: Blue
            - **S:** Saturation (0-100%) - Intensitas warna
              - 0%: Gray
              - 100%: Pure color
            - **V:** Value (0-100%) - Brightness
              - 0%: Black
              - 100%: Full brightness
            
            **HSL Komponen:**
            - **H:** Hue (sama seperti HSV)
            - **S:** Saturation (berbeda dari HSV)
            - **L:** Lightness (0-100%)
              - 0%: Black
              - 50%: Pure color
              - 100%: White
            
            **Keuntungan:**
            - Lebih intuitif untuk manusia
            - Mudah untuk:
              - Color picking
              - Color harmonies
              - Tinting/shading
              - Desaturasi
            
            **Konversi RGB ↔ HSV:**
            Matematika yang kompleks, biasanya 
            di-handle oleh libraries.
            
            **Aplikasi:**
            - Color pickers di software design
            - Image processing (color adjustment)
            - Computer vision (color-based segmentation)
            - Lighting effects dalam games
            
            **Digunakan untuk:**
            - Photoshop, GIMP color pickers
            - CSS (hsl() function)
            - Video color grading
            """)
        
        with color_col3:
            st.markdown("""
            **CMYK (Cyan-Magenta-Yellow-Key/Black)**
            
            Model warna **subtraktif** untuk perangkat yang **memantulkan cahaya** 
            (reflective devices).
            
            **Komponen:**
            - **C:** Cyan (0-100%)
            - **M:** Magenta (0-100%)
            - **Y:** Yellow (0-100%)
            - **K:** Key/Black (0-100%)
            
            **Prinsip Subtraktif:**
            - Menyerap (subtract) cahaya
            - Ink mengurangi light reflection
            - CMY maksimal ≈ Dark brown (bukan pure black)
            - K (Black) untuk pure black
            
            **Mengapa K (Black)?**
            - CMY 100% = expensive dan basah
            - Black ink lebih murah
            - Better contrast
            - Text readability
            
            **Contoh:**
            - Black: `C:0 M:0 Y:0 K:100`
            - Red: `C:0 M:100 Y:100 K:0`
            - Blue: `C:100 M:100 Y:0 K:0`
            
            **Color Gamut:**
            CMYK memiliki gamut **lebih kecil** 
            dari RGB - tidak semua RGB color 
            dapat direproduksi dalam print!
            
            **Conversion Issues:**
            - Bright RGB colors → dull CMYK
            - Out-of-gamut colors need adjustment
            - Proof printing penting
            
            **Digunakan untuk:**
            - Offset printing
            - Digital printing
            - Publikasi majalah/buku
            - Packaging design
            - Large format printing
            
            **Catatan:**
            Selalu convert ke CMYK sebelum 
            mengirim ke printer profesional!
            """)
        
        st.markdown("---")
        
        additional_col1, additional_col2 = st.columns(2)
        
        with additional_col1:
            st.warning("""
            **⚠️ Color Space vs Color Model**
            
            - **Color Model:** Cara merepresentasikan warna (RGB, HSV, CMYK)
            - **Color Space:** Color model + range spesifik (sRGB, Adobe RGB, DCI-P3)
            
            **Common RGB Color Spaces:**
            - **sRGB:** Standard untuk web dan consumer devices
            - **Adobe RGB:** Gamut lebih luas untuk photography
            - **DCI-P3:** Cinema dan modern displays (iPhone, Mac)
            - **Rec. 2020:** Ultra HD TV broadcasting
            """)
        
        with additional_col2:
            st.success("""
            **Kapan Menggunakan Apa?**
            
            **RGB:**
            - Anything displayed on screens
            - Web development
            - Digital photography
            - Video production
            - Game development
            
            **HSV/HSL:**
            - Color selection interfaces
            - Image adjustments
            - Procedural color generation
            
            **CMYK:**
            - Print design only
            - Brochures, posters
            - Magazine/book publishing
            """)
    
    with tab5:
        st.markdown("#### Pixel & Resolusi")
        
        st.markdown("""
        **Pixel** (picture element) adalah unit terkecil dari gambar digital. 
        Memahami pixel dan resolusi adalah fundamental dalam grafika komputer.
        """)
        
        pixel_col1, pixel_col2 = st.columns(2)
        
        with pixel_col1:
            st.markdown("""
            ### Apa itu Pixel?
            
            **Definisi:**
            Pixel adalah satu titik warna dalam grid 2D yang membentuk gambar digital.
            
            **Komponen Pixel (RGB):**
            ```
            Pixel = (R, G, B)
            Dengan transparansi = (R, G, B, A)
            ```
            
            **Ukuran Data:**
            - 24-bit color: 3 bytes per pixel (RGB)
            - 32-bit color: 4 bytes per pixel (RGBA)
            - 8-bit grayscale: 1 byte per pixel
            
            **Contoh Perhitungan:**
            Full HD image (1920×1080, 24-bit):
            ```
            1920 × 1080 × 3 bytes = 6,220,800 bytes ≈ 6.2 MB
            ```
            
            ### Resolusi
            
            **Definisi:**
            Jumlah pixel dalam dimensi width × height.
            
            **Resolusi Umum:**
            
            **HD (High Definition):**
            - **720p:** 1280 × 720 (0.92 MP)
            - **1080p (Full HD):** 1920 × 1080 (2.07 MP)
            
            **Ultra HD:**
            - **1440p (2K):** 2560 × 1440 (3.68 MP)
            - **4K (UHD):** 3840 × 2160 (8.29 MP)
            - **8K:** 7680 × 4320 (33.18 MP)
            
            **Cinematic:**
            - **2K DCI:** 2048 × 1080
            - **4K DCI:** 4096 × 2160
            
            **Mobile:**
            - **iPhone 15 Pro:** 2796 × 1290 (460 PPI)
            - **iPad Pro:** 2732 × 2048
            
            **VR:**
            - **Quest 3:** 2064 × 2208 per eye
            - **Vision Pro:** 3680 × 3140 per eye
            """)
        
        with pixel_col2:
            st.markdown("""
            ### PPI vs DPI
            
            **PPI (Pixels Per Inch):**
            - Display screens
            - Mengukur pixel density
            - Retina display: 300+ PPI
            - Desktop monitor: 90-110 PPI
            - Phone: 400-500 PPI
            
            **DPI (Dots Per Inch):**
            - Printers
            - Mengukur ink dot density
            - Standard print: 300 DPI
            - High-end print: 600-1200 DPI
            
            **Calculation:**
            ```
            PPI = √(width² + height²) / diagonal_inches
            ```
            
            ### Aspect Ratio
            
            **Definisi:**
            Rasio width terhadap height.
            
            **Umum:**
            - **16:9** - HD, modern monitors, TV
            - **16:10** - Professional monitors
            - **21:9** - Ultrawide monitors
            - **4:3** - Old monitors, iPads
            - **1:1** - Instagram square
            - **9:16** - Vertical video (TikTok, Stories)
            
            ### Frame Rate
            
            **FPS (Frames Per Second):**
            Berapa kali gambar di-refresh per detik.
            
            - **24 FPS:** Cinema standard
            - **30 FPS:** TV, console games
            - **60 FPS:** Smooth gaming
            - **120 FPS:** High-end gaming
            - **144 FPS:** Competitive esports
            - **240+ FPS:** Professional esports
            
            **Frame Time:**
            ```
            60 FPS = 16.67 ms per frame
            144 FPS = 6.94 ms per frame
            ```
            """)
        
        st.markdown("---")
        
        st.info("""
        **Persamaan Penting:**
        
        **Ukuran File Raster (uncompressed):**
        ```
        File Size = Width × Height × Bytes Per Pixel
        ```
        
        **Video Bitrate (uncompressed):**
        ```
        Bitrate = Width × Height × Bits Per Pixel × FPS
        
        Example 4K 60fps:
        3840 × 2160 × 24 bits × 60 = 11.9 Gbps (!)
        Compression is essential: H.264, H.265, AV1
        ```
        """)
    
    st.markdown("---")
    
    # --- Image Section (with error handling) --- #
    st.markdown("### Visualisasi Grafika Komputer")
    
    st.markdown("""
    Berikut adalah contoh aplikasi nyata dari konsep-konsep grafika komputer 
    yang telah kita pelajari:
    """)
    
    image_path = "assets/images/IU.jpeg"
    
    try:
        if os.path.exists(image_path):
            image = Image.open(image_path)
            
            # Display with columns
            img_col1, img_col2 = st.columns([2, 1])
            
            with img_col1:
                st.image(image, caption="Contoh Aplikasi Grafika Komputer", use_container_width=True)
            
            with img_col2:
                st.markdown("**Informasi Gambar:**")
                width, height = image.size
                mode = image.mode
                
                st.metric("Resolusi", f"{width} × {height} px")
                st.metric("Mode Warna", mode)
                
                megapixels = (width * height) / 1_000_000
                st.metric("Megapixels", f"{megapixels:.2f} MP")
                
                if mode == "RGB":
                    file_size = width * height * 3 / (1024 * 1024)
                    st.metric("Ukuran (raw)", f"{file_size:.2f} MB")
        else:
            st.warning(f"⚠️ Gambar tidak ditemukan di: `{image_path}`")
            st.info("""
            **Tips Struktur Folder:**
            ```
            uts-grafkom/
            ├── assets/
            │   └── images/
            │       └── IU.jpeg
            └── pages/
                └── 2_Week1_Pengantar.py
            ```
            
            Pastikan path relatif sesuai dengan struktur folder Anda.
            """)
    except Exception as e:
        st.error(f"❌ Error memuat gambar: {e}")
        st.info("Gambar akan ditampilkan setelah masalah dependency atau path teratasi.")
    
    # --- Footer --- #
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>💡 <strong>Reminder:</strong> Konsep-konsep dasar ini akan terus muncul di materi selanjutnya!</p>
        <p>Minggu 1: Pengantar Grafika Komputer | © 2025 Grafika Komputer</p>
    </div>
    """, unsafe_allow_html=True)

# Entry point
if __name__ == "__main__":
    show_week1()