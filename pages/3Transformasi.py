"""
Halaman Minggu 2: Transformasi Geometri 2D.

Menyediakan antarmuka interaktif untuk menerapkan transformasi 2D
(translasi, rotasi, skala, shear) pada objek dengan visualisasi real-time.
"""

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import plotly.graph_objects as go

from config import PAGE_CONFIG, CANVAS_WIDTH, CANVAS_HEIGHT
from utils.helpers import load_css

try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except ImportError:
    CANVAS_AVAILABLE = False

from algorithms.transformations import (
    create_translation_matrix,
    create_rotation_matrix,
    create_scale_matrix,
    create_shear_matrix,
    apply_transformation,
    combine_transformations
)

st.set_page_config(**PAGE_CONFIG)

# Memuat CSS kustom
try:
    load_css("assets/styles/custom.css")
except Exception as e:
    st.warning(f"⚠️ CSS kustom tidak dimuat: {e}")

def show_week2():
    """
    Menampilkan halaman transformasi 2D dengan interface modern.
    """
    
    # --- Hero Section --- #
    st.markdown("""
        <div class="header-container">
            <h1>🔄 Transformasi Geometri 2D</h1>
            <p class="subtitle">Manipulasi Objek dengan Matriks Transformasi</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Introduction Section --- #
    intro_col1, intro_col2 = st.columns([3, 2])
    
    with intro_col1:
        st.markdown("### 🎯 Tujuan Pembelajaran")
        st.markdown("""
        Pada minggu ini, Anda akan mempelajari konsep fundamental transformasi geometri 
        dalam grafika komputer 2D:
        
        - **📐 Transformasi Dasar** - Translation, Rotation, Scaling, Shearing
        - **🔢 Matriks Transformasi** - Representasi matematis menggunakan koordinat homogen
        - **🎮 Aplikasi Interaktif** - Visualisasi real-time dengan parameter yang dapat diubah
        - **🔗 Transformasi Komposit** - Menggabungkan beberapa transformasi sekaligus
        
        Semua transformasi menggunakan **matriks 3×3** dan **koordinat homogen** untuk 
        memudahkan komputasi dan kombinasi transformasi.
        """)
    
    with intro_col2:
        st.info("""
        ### 📌 Petunjuk Penggunakan
        
        **Langkah-langkah:**
        
        1. Pilih **mode demo** (Canvas/Visualization)
        2. Pilih **jenis transformasi** di sidebar
        3. Sesuaikan **parameter** transformasi
        4. Amati **hasil real-time**
        5. Pelajari **matriks** yang terbentuk
        
        *Eksplorasi berbagai kombinasi transformasi!*
        """)
    
    st.markdown("---")
    
    # --- Theory Section --- #
    with st.expander("📚 **Teori: Transformasi 2D & Koordinat Homogen**", expanded=False):
        theory_col1, theory_col2 = st.columns([2, 1])
        
        with theory_col1:
            st.markdown("""
            ### Apa itu Transformasi Geometri?
            
            **Transformasi geometri** adalah operasi matematika yang mengubah posisi, ukuran, 
            atau orientasi dari suatu objek dalam ruang koordinat. Dalam grafika komputer 2D, 
            transformasi direpresentasikan menggunakan **matriks 3×3** dengan **koordinat homogen**.
            
            ### Mengapa Koordinat Homogen?
            
            Koordinat homogen memungkinkan kita untuk merepresentasikan **semua jenis transformasi** 
            (termasuk translasi) sebagai perkalian matriks tunggal:
            
            **Konversi ke Homogen:**
            - Titik (x, y) → (x, y, 1)
            
            **Formula Transformasi:**
            ```
            [x']   [a  b  tx]   [x]
            [y'] = [c  d  ty] × [y]
            [1 ]   [0  0   1]   [1]
            ```
            
            **Keuntungan:**
            - ✅ Semua transformasi dalam satu format
            - ✅ Mudah digabungkan (komposisi)
            - ✅ Efisien untuk komputasi
            """)
        
        with theory_col2:
            st.markdown("""
            ### 🔑 Jenis Transformasi
            
            **1. Translation** 📍
            Memindahkan objek
            
            **2. Rotation** 🔄
            Memutar objek
            
            **3. Scaling** 📏
            Mengubah ukuran
            
            **4. Shearing** ↗️
            Menggeser diagonal
            
            **5. Composite** 🔗
            Kombinasi transformasi
            """)
        
        st.markdown("---")
        
        # Tabs untuk setiap transformasi
        trans_tab1, trans_tab2, trans_tab3, trans_tab4 = st.tabs([
            "📍 Translasi", "🔄 Rotasi", "📏 Skala", "↗️ Shear"
        ])
        
        with trans_tab1:
            tab_col1, tab_col2 = st.columns([2, 1])
            
            with tab_col1:
                st.markdown("""
                ### Translasi (Translation)
                
                **Memindahkan** objek dari satu posisi ke posisi lain tanpa mengubah 
                bentuk, ukuran, atau orientasinya.
                
                **Parameter:**
                - `tx`: perpindahan horizontal (sumbu X)
                - `ty`: perpindahan vertikal (sumbu Y)
                
                **Matriks Translasi:**
                ```
                [1   0   tx]
                [0   1   ty]
                [0   0    1]
                ```
                
                **Rumus Transformasi:**
                - `x' = x + tx`
                - `y' = y + ty`
                - `1' = 1` (koordinat homogen tetap)
                
                **Sifat-sifat:**
                - Mempertahankan bentuk dan ukuran
                - Tidak mengubah sudut
                - Komutatif: T(a,b) × T(c,d) = T(c,d) × T(a,b)
                """)
            
            with tab_col2:
                st.markdown("**📊 Contoh:**")
                st.code("Point: (100, 100)")
                st.code("tx = 50, ty = 30")
                st.code("Result: (150, 130)")
                
                st.success("✅ Objek bergeser 50px ke kanan dan 30px ke bawah")
        
        with trans_tab2:
            tab_col1, tab_col2 = st.columns([2, 1])
            
            with tab_col1:
                st.markdown("""
                ### Rotasi (Rotation)
                
                **Memutar** objek terhadap suatu titik pivot dengan sudut tertentu.
                
                **Parameter:**
                - `θ` (theta): sudut rotasi dalam derajat
                - `(cx, cy)`: titik pusat rotasi (pivot point)
                
                **Matriks Rotasi (terhadap origin):**
                ```
                [cos(θ)  -sin(θ)   0]
                [sin(θ)   cos(θ)   0]
                [  0        0      1]
                ```
                
                **Rotasi terhadap titik (cx, cy):**
                
                Memerlukan 3 langkah (transformasi komposit):
                1. **Translasi ke origin:** T(-cx, -cy)
                2. **Rotasi:** R(θ)
                3. **Translasi kembali:** T(cx, cy)
                
                **Matriks Komposit:**
                ```
                M = T(cx,cy) × R(θ) × T(-cx,-cy)
                ```
                
                **Catatan Penting:**
                - Sudut **positif** = counter-clockwise (berlawanan jarum jam)
                - Sudut **negatif** = clockwise (searah jarum jam)
                - Mempertahankan ukuran dan bentuk
                """)
            
            with tab_col2:
                st.markdown("**📊 Contoh:**")
                st.code("Angle: 45°")
                st.code("Pivot: (0, 0)")
                st.code("cos(45°) ≈ 0.707")
                st.code("sin(45°) ≈ 0.707")
                
                st.info("💡 Rotasi 90° mengubah (x,y) menjadi (-y,x)")
        
        with trans_tab3:
            tab_col1, tab_col2 = st.columns([2, 1])
            
            with tab_col1:
                st.markdown("""
                ### Skala (Scaling)
                
                **Memperbesar atau memperkecil** ukuran objek.
                
                **Parameter:**
                - `sx`: faktor skala horizontal (sumbu X)
                - `sy`: faktor skala vertikal (sumbu Y)
                - `(cx, cy)`: titik pusat skala
                
                **Matriks Skala (terhadap origin):**
                ```
                [sx   0   0]
                [ 0  sy   0]
                [ 0   0   1]
                ```
                
                **Jenis-jenis Skala:**
                
                **1. Uniform Scaling:** `sx = sy`
                - Proporsi objek tetap
                - Contoh: sx = sy = 2 (perbesar 2x)
                
                **2. Non-uniform Scaling:** `sx ≠ sy`
                - Proporsi objek berubah
                - Contoh: sx = 2, sy = 0.5 (lebar 2x, tinggi 0.5x)
                
                **3. Scaling Factor:**
                - `s > 1`: Memperbesar
                - `s = 1`: Tidak berubah
                - `0 < s < 1`: Memperkecil
                - `s < 0`: Pencerminan (reflection)
                
                **Skala terhadap titik (cx, cy):**
                Sama seperti rotasi, gunakan transformasi komposit.
                """)
            
            with tab_col2:
                st.markdown("**📊 Contoh:**")
                st.code("sx = 2.0 (2x lebar)")
                st.code("sy = 1.5 (1.5x tinggi)")
                st.code("Point (10,20)")
                st.code("Result (20,30)")
                
                st.warning("⚠️ sx atau sy negatif = reflection")
        
        with trans_tab4:
            tab_col1, tab_col2 = st.columns([2, 1])
            
            with tab_col1:
                st.markdown("""
                ### Shear (Geser/Miring)
                
                **Menggeser** objek secara diagonal, menciptakan efek miring atau parallelogram.
                
                **Parameter:**
                - `shx`: shear horizontal (geser X berdasarkan Y)
                - `shy`: shear vertikal (geser Y berdasarkan X)
                
                **Matriks Shear:**
                ```
                [1    shx   0]
                [shy   1    0]
                [0     0    1]
                ```
                
                **Rumus Transformasi:**
                - `x' = x + shx × y`
                - `y' = shy × x + y`
                
                **Interpretasi:**
                - **shx ≠ 0:** Titik bergeser horizontal berdasarkan posisi Y
                - **shy ≠ 0:** Titik bergeser vertikal berdasarkan posisi X
                
                **Aplikasi Praktis:**
                - Efek italic pada teks
                - Simulasi perspektif sederhana
                - Transformasi persegi → parallelogram
                - Efek visual dinamis
                
                **Catatan:**
                - Mengubah sudut tetapi mempertahankan kesejajaran
                - Tidak mempertahankan sudut siku-siku
                """)
            
            with tab_col2:
                st.markdown("**📊 Contoh:**")
                st.code("shx = 0.5")
                st.code("shy = 0.0")
                st.code("Point (10, 20)")
                st.code("x' = 10 + 0.5×20 = 20")
                st.code("y' = 0×10 + 20 = 20")
                st.code("Result: (20, 20)")
                
                st.info("💡 Membuat efek 'miring' pada objek")
    
    st.markdown("---")
    
    # --- Interactive Demo Section --- #
    st.markdown("### 🎮 Demo Interaktif")
    
    # Mode selection with better styling
    demo_col1, demo_col2 = st.columns([3, 1])
    
    with demo_col1:
        st.markdown("""
        Pilih mode demo untuk memulai eksplorasi transformasi geometri:
        - **Canvas Drawing**: Gambar bentuk bebas dan terapkan transformasi
        - **Predefined Shapes**: Visualisasi transformasi pada bentuk geometris standar
        """)
    
    with demo_col2:
        demo_mode = st.selectbox(
            "Mode Demo",
            ["📊 Predefined Shapes", "🖌️ Canvas Drawing"],
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    if demo_mode == "🖌️ Canvas Drawing":
        if not CANVAS_AVAILABLE:
            st.error("❌ **Module 'streamlit-drawable-canvas' tidak tersedia**")
            st.code("pip install streamlit-drawable-canvas", language="bash")
            st.info("💡 Module ini diperlukan untuk mode Canvas Drawing. Gunakan mode Predefined Shapes sebagai alternatif.")
        else:
            show_canvas_mode()
    else:
        show_visualization_mode()
    
    st.markdown("---")
    
    # --- Composite Transformation Section --- #
    with st.expander("🔗 **Transformasi Komposit (Advanced)**", expanded=False):
        st.markdown("""
        ### Menggabungkan Beberapa Transformasi
        
        Dalam aplikasi grafika komputer yang sesungguhnya, kita sering perlu menerapkan 
        **beberapa transformasi sekaligus** pada objek yang sama. Keuntungan menggunakan 
        representasi matriks adalah kita dapat **menggabungkan** transformasi dengan cara 
        **mengalikan matriks-matriks** tersebut.
        """)
        
        comp_theory_col1, comp_theory_col2 = st.columns(2)
        
        with comp_theory_col1:
            st.markdown("""
            **💡 Konsep Dasar:**
            
            Misalkan kita ingin menerapkan transformasi T₁, kemudian T₂, lalu T₃:
            
            ```
            Point' = T₃ × T₂ × T₁ × Point
            ```
            
            Kita dapat menggabungkan matriks terlebih dahulu:
            
            ```
            M_combined = T₃ × T₂ × T₁
            Point' = M_combined × Point
            ```
            
            **Keuntungan:**
            - ✅ Hanya satu kali perkalian matriks per titik
            - ✅ Lebih efisien untuk banyak titik
            - ✅ Dapat disimpan dan digunakan ulang
            """)
        
        with comp_theory_col2:
            st.markdown("""
            **⚠️ Urutan Sangat Penting!**
            
            Perkalian matriks **tidak komutatif**:
            ```
            A × B ≠ B × A
            ```
            
            Contoh:
            - Rotasi → Translasi ≠ Translasi → Rotasi
            - Urutan dibaca dari **kanan ke kiri**
            
            **Contoh Rotasi terhadap Titik:**
            ```
            1. T(-cx, -cy)  : Pindah ke origin
            2. R(θ)         : Rotasi
            3. T(cx, cy)    : Kembalikan
            
            M = T(cx,cy) × R(θ) × T(-cx,-cy)
            ```
            """)
        
        st.markdown("---")
        
        # Demo composite
        st.markdown("#### 📐 Kalkulator Transformasi Komposit")
        st.info("💡 Eksplorasi bagaimana urutan transformasi mempengaruhi hasil akhir")
        
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        with comp_col1:
            st.markdown("**🔵 Transformasi 1:**")
            t1_type = st.selectbox("Jenis", ["Translasi", "Rotasi", "Skala", "Shear"], key="t1")
            
            if t1_type == "Translasi":
                t1_tx = st.number_input("tx", value=50.0, key="t1tx")
                t1_ty = st.number_input("ty", value=30.0, key="t1ty")
                m1 = create_translation_matrix(t1_tx, t1_ty)
                st.caption(f"T({t1_tx}, {t1_ty})")
                
            elif t1_type == "Rotasi":
                t1_angle = st.number_input("Sudut (°)", value=45.0, key="t1angle")
                m1 = create_rotation_matrix(t1_angle, 0, 0)
                st.caption(f"R({t1_angle}°)")
                
            elif t1_type == "Skala":
                t1_sx = st.number_input("sx", value=1.5, key="t1sx")
                t1_sy = st.number_input("sy", value=1.5, key="t1sy")
                m1 = create_scale_matrix(t1_sx, t1_sy, 0, 0)
                st.caption(f"S({t1_sx}, {t1_sy})")
            else:
                t1_shx = st.number_input("shx", value=0.5, key="t1shx")
                t1_shy = st.number_input("shy", value=0.0, key="t1shy")
                m1 = create_shear_matrix(t1_shx, t1_shy)
                st.caption(f"Sh({t1_shx}, {t1_shy})")
        
        with comp_col2:
            st.markdown("**🟢 Transformasi 2:**")
            t2_type = st.selectbox("Jenis", ["Translasi", "Rotasi", "Skala", "Shear"], key="t2")
            
            if t2_type == "Translasi":
                t2_tx = st.number_input("tx", value=20.0, key="t2tx")
                t2_ty = st.number_input("ty", value=-10.0, key="t2ty")
                m2 = create_translation_matrix(t2_tx, t2_ty)
                st.caption(f"T({t2_tx}, {t2_ty})")
                
            elif t2_type == "Rotasi":
                t2_angle = st.number_input("Sudut (°)", value=-30.0, key="t2angle")
                m2 = create_rotation_matrix(t2_angle, 0, 0)
                st.caption(f"R({t2_angle}°)")
                
            elif t2_type == "Skala":
                t2_sx = st.number_input("sx", value=0.8, key="t2sx")
                t2_sy = st.number_input("sy", value=0.8, key="t2sy")
                m2 = create_scale_matrix(t2_sx, t2_sy, 0, 0)
                st.caption(f"S({t2_sx}, {t2_sy})")
            else:
                t2_shx = st.number_input("shx", value=0.0, key="t2shx")
                t2_shy = st.number_input("shy", value=0.3, key="t2shy")
                m2 = create_shear_matrix(t2_shx, t2_shy)
                st.caption(f"Sh({t2_shx}, {t2_shy})")
        
        with comp_col3:
            st.markdown("**🟡 Transformasi 3:**")
            t3_type = st.selectbox("Jenis", ["Translasi", "Rotasi", "Skala", "Shear"], key="t3")
            
            if t3_type == "Translasi":
                t3_tx = st.number_input("tx", value=10.0, key="t3tx")
                t3_ty = st.number_input("ty", value=20.0, key="t3ty")
                m3 = create_translation_matrix(t3_tx, t3_ty)
                st.caption(f"T({t3_tx}, {t3_ty})")
                
            elif t3_type == "Rotasi":
                t3_angle = st.number_input("Sudut (°)", value=15.0, key="t3angle")
                m3 = create_rotation_matrix(t3_angle, 0, 0)
                st.caption(f"R({t3_angle}°)")
                
            elif t3_type == "Skala":
                t3_sx = st.number_input("sx", value=1.2, key="t3sx")
                t3_sy = st.number_input("sy", value=1.2, key="t3sy")
                m3 = create_scale_matrix(t3_sx, t3_sy, 0, 0)
                st.caption(f"S({t3_sx}, {t3_sy})")
            else:
                t3_shx = st.number_input("shx", value=0.2, key="t3shx")
                t3_shy = st.number_input("shy", value=0.0, key="t3shy")
                m3 = create_shear_matrix(t3_shx, t3_shy)
                st.caption(f"Sh({t3_shx}, {t3_shy})")
        
        # Combine matrices
        m_combined = combine_transformations([m1, m2, m3])
        
        st.markdown("---")
        st.markdown("#### 📊 Hasil Transformasi Komposit")
        
        result_col1, result_col2 = st.columns([2, 1])
        
        with result_col1:
            st.markdown("**Matriks Gabungan (M₃ × M₂ × M₁):**")
            df_combined = pd.DataFrame(
                np.round(m_combined, 4),
                columns=['Column 1', 'Column 2', 'Column 3'],
                index=['Row 1', 'Row 2', 'Row 3']
            )
            st.dataframe(df_combined, use_container_width=True)
        
        with result_col2:
            st.markdown("**Urutan Eksekusi:**")
            st.code(f"1️⃣ {t1_type}")
            st.code(f"2️⃣ {t2_type}")
            st.code(f"3️⃣ {t3_type}")
            
            st.success("✅ Matriks siap digunakan untuk transformasi!")
        
        st.info("""
        💡 **Interpretasi:** Matriks gabungan ini merepresentasikan efek kumulatif dari 
        ketiga transformasi. Anda dapat menggunakan satu matriks ini untuk mentransformasi 
        seluruh objek sekaligus, yang jauh lebih efisien daripada menerapkan tiga 
        transformasi secara terpisah untuk setiap titik.
        """)
    
    st.markdown("---")
    
    # --- Summary --- #
    st.success("""
    ✅ **Ringkasan Minggu 2: Transformasi Geometri 2D**
    
    **Konsep Utama:**
    - Transformasi 2D direpresentasikan menggunakan **matriks 3×3** dengan **koordinat homogen**
    - Empat transformasi dasar: **Translation, Rotation, Scaling, Shearing**
    - Transformasi dapat **digabungkan** dengan perkalian matriks (urutan sangat penting!)
    - Rotasi dan skala terhadap titik sembarang menggunakan **transformasi komposit**
    
    **Keuntungan Matriks:**
    - ✅ Representasi uniform untuk semua transformasi
    - ✅ Mudah digabungkan dan dikombinasikan
    - ✅ Efisien untuk komputasi grafika
    - ✅ Standar industri dalam computer graphics
    
    **Selanjutnya:** Minggu 3 - Algoritma Garis (DDA & Bresenham) →
    """)
    
    # --- Footer --- #
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>💡 <strong>Tips:</strong> Coba kombinasikan berbagai transformasi untuk memahami efek komposit!</p>
        <p>Minggu 2: Transformasi Geometri 2D | © 2025 Grafika Komputer</p>
    </div>
    """, unsafe_allow_html=True)


def show_canvas_mode():
    """Mode menggambar di canvas dengan drawable canvas."""
    
    st.markdown("#### 🖌️ Mode Canvas Drawing")
    st.info("🎨 **Instruksi:** Gambar bentuk bebas di canvas, simpan, pilih transformasi, lalu terapkan untuk melihat hasilnya!")
    
    # Sidebar controls
    st.sidebar.markdown("### 🎛️ Kontrol Transformasi")
    
    transform_type = st.sidebar.selectbox(
        "Jenis Transformasi",
        ["Translasi", "Rotasi", "Skala", "Shear"],
        help="Pilih jenis transformasi yang ingin diterapkan"
    )
    
    # Initialize session state
    if 'transform_params' not in st.session_state:
        st.session_state.transform_params = {
            'tx': 0.0, 'ty': 0.0,
            'angle': 0.0,
            'sx': 1.0, 'sy': 1.0,
            'shx': 0.0, 'shy': 0.0
        }
    
    params = st.session_state.transform_params
    
    # Parameter controls
    st.sidebar.markdown(f"#### Parameter {transform_type}")
    st.sidebar.markdown("---")
    
    if transform_type == "Translasi":
        params['tx'] = st.sidebar.slider("Translasi X (tx)", -200, 200, int(params['tx']), help="Perpindahan horizontal")
        params['ty'] = st.sidebar.slider("Translasi Y (ty)", -200, 200, int(params['ty']), help="Perpindahan vertikal")
        st.sidebar.info(f"📍 Perpindahan: ({params['tx']}, {params['ty']}) piksel")
        
    elif transform_type == "Rotasi":
        params['angle'] = st.sidebar.slider("Sudut (°)", -180, 180, int(params['angle']), help="Sudut rotasi dalam derajat")
        st.sidebar.caption("Pusat rotasi: centroid objek")
        st.sidebar.info(f"🔄 Rotasi: {params['angle']}° {'CCW' if params['angle'] > 0 else 'CW' if params['angle'] < 0 else 'none'}")
        
    elif transform_type == "Skala":
        params['sx'] = st.sidebar.slider("Skala X (sx)", 0.1, 3.0, float(params['sx']), 0.1, help="Faktor skala horizontal")
        params['sy'] = st.sidebar.slider("Skala Y (sy)", 0.1, 3.0, float(params['sy']), 0.1, help="Faktor skala vertikal")
        uniform = st.sidebar.checkbox("Uniform Scaling", value=(params['sx'] == params['sy']))
        if uniform:
            params['sy'] = params['sx']
        st.sidebar.caption("Pusat skala: centroid objek")
        st.sidebar.info(f"📏 Skala: {params['sx']}x × {params['sy']}x")
        
    else:  # Shear
        params['shx'] = st.sidebar.slider("Shear X (shx)", -2.0, 2.0, float(params['shx']), 0.1, help="Geser horizontal berdasarkan Y")
        params['shy'] = st.sidebar.slider("Shear Y (shy)", -2.0, 2.0, float(params['shy']), 0.1, help="Geser vertikal berdasarkan X")
        st.sidebar.info(f"↗️ Shear: X={params['shx']}, Y={params['shy']}")
    
    st.sidebar.markdown("---")
    
    # Canvas layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("##### 🎨 Canvas Menggambar")
        
        canvas_result = st_canvas(
            fill_color="rgba(255, 75, 75, 0.3)",
            stroke_width=3,
            stroke_color="#FF4B4B",
            background_color="#1E2128",
            height=CANVAS_HEIGHT,
            width=CANVAS_WIDTH,
            drawing_mode="freedraw",
            key="transform_canvas",
        )
    
    with col2:
        st.markdown("##### 📊 Matriks Transformasi")
        
        # Calculate matrix based on type
        if transform_type == "Translasi":
            matrix = create_translation_matrix(params['tx'], params['ty'])
        elif transform_type == "Rotasi":
            matrix = create_rotation_matrix(params['angle'], 0, 0)
        elif transform_type == "Skala":
            matrix = create_scale_matrix(params['sx'], params['sy'], 0, 0)
        else:
            matrix = create_shear_matrix(params['shx'], params['shy'])
        
        df_matrix = pd.DataFrame(
            np.round(matrix, 3),
            columns=['C1', 'C2', 'C3'],
            index=['R1', 'R2', 'R3']
        )
        st.dataframe(df_matrix, use_container_width=True)
        
        st.markdown("---")
        st.markdown("**💾 Status:**")
        if 'original_drawing' in st.session_state:
            st.success("✅ Bentuk tersimpan")
        else:
            st.warning("⚠️ Belum ada bentuk")
    
    # Action buttons
    st.markdown("---")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("💾 Simpan Bentuk", use_container_width=True, type="primary"):
            if canvas_result.json_data and canvas_result.json_data["objects"]:
                st.session_state.original_drawing = canvas_result.json_data
                st.success("✅ Bentuk berhasil disimpan!")
                st.balloons()
            else:
                st.warning("⚠️ Silakan gambar sesuatu terlebih dahulu!")
    
    with btn_col2:
        if st.button("⚡ Terapkan Transformasi", use_container_width=True):
            if 'original_drawing' in st.session_state:
                st.success(f"✅ {transform_type} berhasil diterapkan!")
                st.info(f"💡 Transformasi {transform_type} telah diaplikasikan pada objek")
            else:
                st.warning("⚠️ Simpan bentuk terlebih dahulu!")
    
    with btn_col3:
        if st.button("🔄 Reset Semua", use_container_width=True):
            st.session_state.transform_params = {
                'tx': 0.0, 'ty': 0.0, 'angle': 0.0,
                'sx': 1.0, 'sy': 1.0, 'shx': 0.0, 'shy': 0.0
            }
            if 'original_drawing' in st.session_state:
                del st.session_state.original_drawing
            st.rerun()


def show_visualization_mode():
    """Mode visualisasi dengan predefined shapes menggunakan Plotly."""
    
    st.markdown("#### 📊 Mode Visualisasi dengan Bentuk Predefined")
    st.info("🎯 **Mode Visualisasi:** Lihat efek transformasi pada bentuk geometris standar dengan perbandingan before/after")
    
    # Sidebar controls
    st.sidebar.markdown("### 🎛️ Kontrol Visualisasi")
    
    # Shape selection
    shape_type = st.sidebar.selectbox(
        "Pilih Bentuk",
        ["Persegi", "Segitiga", "Pentagon", "Rumah", "Bintang"],
        help="Pilih bentuk geometris untuk divisualisasikan"
    )
    
    transform_type = st.sidebar.selectbox(
        "Jenis Transformasi",
        ["Translasi", "Rotasi", "Skala", "Shear", "Komposit"],
        help="Pilih jenis transformasi yang ingin diterapkan"
    )
    
    st.sidebar.markdown(f"#### Parameter {transform_type}")
    st.sidebar.markdown("---")
    
    # Get shape points
    if shape_type == "Persegi":
        points = np.array([[-50, -50], [50, -50], [50, 50], [-50, 50], [-50, -50]])
    elif shape_type == "Segitiga":
        points = np.array([[0, -60], [52, 30], [-52, 30], [0, -60]])
    elif shape_type == "Pentagon":
        angles = np.linspace(0, 2*np.pi, 6)
        points = np.column_stack([50*np.cos(angles), 50*np.sin(angles)])
    elif shape_type == "Bintang":
        angles = np.linspace(0, 2*np.pi, 11)
        radii = np.array([50, 20] * 5 + [50])
        points = np.column_stack([radii*np.cos(angles), radii*np.sin(angles)])
    else:  # Rumah
        points = np.array([
            [-50, 0], [50, 0], [50, 40], [0, 70], [-50, 40], [-50, 0]
        ])
    
    # Transform parameters
    if transform_type == "Translasi":
        tx = st.sidebar.slider("Translasi X (tx)", -150, 150, 80, help="Perpindahan horizontal")
        ty = st.sidebar.slider("Translasi Y (ty)", -150, 150, 60, help="Perpindahan vertikal")
        matrix = create_translation_matrix(tx, ty)
        st.sidebar.info(f"📍 Total perpindahan: √({tx}² + {ty}²) = {np.sqrt(tx**2 + ty**2):.1f} px")
        
    elif transform_type == "Rotasi":
        angle = st.sidebar.slider("Sudut (°)", -180, 180, 45, help="Sudut rotasi")
        cx, cy = 0, 0  # Center of shape
        matrix = create_rotation_matrix(angle, cx, cy)
        st.sidebar.caption("🎯 Pusat rotasi: origin (0, 0)")
        st.sidebar.info(f"🔄 Arah: {'Counter-clockwise' if angle > 0 else 'Clockwise' if angle < 0 else 'Tidak ada rotasi'}")
        
    elif transform_type == "Skala":
        col_sx, col_sy = st.sidebar.columns(2)
        with col_sx:
            sx = st.slider("sx", 0.1, 3.0, 1.5, 0.1, key="viz_sx")
        with col_sy:
            sy = st.slider("sy", 0.1, 3.0, 1.5, 0.1, key="viz_sy")
        
        uniform = st.sidebar.checkbox("Uniform Scaling", value=(sx == sy))
        if uniform:
            sy = sx
        
        matrix = create_scale_matrix(sx, sy, 0, 0)
        
        area_factor = sx * sy
        st.sidebar.info(f"📏 Luas berubah: {area_factor:.2f}x")
        if sx == sy:
            st.sidebar.success("✅ Proporsi dipertahankan")
        else:
            st.sidebar.warning("⚠️ Proporsi berubah")
        
    elif transform_type == "Shear":
        shx = st.sidebar.slider("Shear X (shx)", -1.0, 1.0, 0.5, 0.1, help="Geser horizontal")
        shy = st.sidebar.slider("Shear Y (shy)", -1.0, 1.0, 0.0, 0.1, help="Geser vertikal")
        matrix = create_shear_matrix(shx, shy)
        
        if shx != 0:
            st.sidebar.info(f"↗️ Horizontal shear: {abs(shx)}")
        if shy != 0:
            st.sidebar.info(f"↗️ Vertical shear: {abs(shy)}")
        
    else:  # Komposit
        st.sidebar.markdown("**🔵 Step 1: Rotasi**")
        angle = st.sidebar.slider("Rotasi (°)", -180, 180, 30, key="comp_rot")
        
        st.sidebar.markdown("**🟢 Step 2: Skala**")
        scale = st.sidebar.slider("Skala Uniform", 0.5, 2.0, 1.2, 0.1, key="comp_scale")
        
        st.sidebar.markdown("**🟡 Step 3: Translasi**")
        tx = st.sidebar.slider("tx", -150, 150, 100, key="comp_tx")
        ty = st.sidebar.slider("ty", -150, 150, 50, key="comp_ty")
        
        m1 = create_rotation_matrix(angle, 0, 0)
        m2 = create_scale_matrix(scale, scale, 0, 0)
        m3 = create_translation_matrix(tx, ty)
        matrix = combine_transformations([m1, m2, m3])
        
        st.sidebar.markdown("---")
        st.sidebar.success("✅ Urutan: Rotasi → Skala → Translasi")
    
    st.sidebar.markdown("---")
    
    # Apply transformation
    transformed_points = apply_transformation(points.tolist(), matrix)
    
    # Visualization
    viz_col1, viz_col2 = st.columns([3, 1])
    
    with viz_col1:
        st.markdown("##### 📊 Grafik Perbandingan")
        
        fig = go.Figure()
        
        # Original shape
        fig.add_trace(go.Scatter(
            x=points[:, 0], y=points[:, 1],
            mode='lines+markers',
            name='Original',
            line=dict(color='#4A9EFF', width=3),
            marker=dict(size=10, symbol='circle'),
            fill='toself',
            fillcolor='rgba(74, 158, 255, 0.2)'
        ))
        
        # Transformed shape
        transformed_array = np.array(transformed_points)
        fig.add_trace(go.Scatter(
            x=transformed_array[:, 0], y=transformed_array[:, 1],
            mode='lines+markers',
            name='Transformed',
            line=dict(color='#FF4B4B', width=3),
            marker=dict(size=10, symbol='diamond'),
            fill='toself',
            fillcolor='rgba(255, 75, 75, 0.2)'
        ))
        
        # Add origin point
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            name='Origin',
            marker=dict(size=15, color='#00C853', symbol='x')
        ))
        
        fig.update_layout(
            xaxis=dict(
                range=[-200, 200], 
                zeroline=True, 
                gridcolor='#333',
                title='X Axis'
            ),
            yaxis=dict(
                range=[-200, 200], 
                zeroline=True, 
                gridcolor='#333',
                title='Y Axis',
                scaleanchor='x',
                scaleratio=1
            ),
            plot_bgcolor='#1E2128',
            paper_bgcolor='#1E2128',
            font=dict(color='white', size=12),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(30, 33, 40, 0.8)',
                bordercolor='#444',
                borderwidth=1
            ),
            height=500,
            hovermode='closest',
            title=dict(
                text=f'{transform_type} pada {shape_type}',
                x=0.5,
                xanchor='center'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with viz_col2:
        st.markdown("##### 📐 Matriks")
        
        df_matrix = pd.DataFrame(
            np.round(matrix, 4),
            columns=['C1', 'C2', 'C3'],
            index=['R1', 'R2', 'R3']
        )
        st.dataframe(df_matrix, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("**📍 Sample Point:**")
        sample_idx = len(points) // 2
        orig_pt = points[sample_idx]
        trans_pt = transformed_points[sample_idx]
        
        st.code(f"Before:\n({orig_pt[0]:.1f}, {orig_pt[1]:.1f})")
        st.code(f"After:\n({trans_pt[0]:.1f}, {trans_pt[1]:.1f})")
        
        # Calculate displacement
        displacement = np.sqrt((trans_pt[0] - orig_pt[0])**2 + (trans_pt[1] - orig_pt[1])**2)
        st.metric("Displacement", f"{displacement:.1f} px")
    
    # Statistics section
    st.markdown("---")
    st.markdown("##### 📈 Statistik Transformasi")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        # Calculate centroid
        orig_centroid = np.mean(points[:-1], axis=0)
        trans_centroid = np.mean(transformed_array[:-1], axis=0)
        centroid_shift = np.sqrt(np.sum((trans_centroid - orig_centroid)**2))
        st.metric("Pergeseran Centroid", f"{centroid_shift:.1f} px")
    
    with stat_col2:
        # Number of vertices
        num_vertices = len(points) - 1
        st.metric("Jumlah Vertex", num_vertices)
    
    with stat_col3:
        # Bounding box area change
        orig_area = (points[:, 0].max() - points[:, 0].min()) * (points[:, 1].max() - points[:, 1].min())
        trans_area = (transformed_array[:, 0].max() - transformed_array[:, 0].min()) * (transformed_array[:, 1].max() - transformed_array[:, 1].min())
        area_ratio = trans_area / orig_area if orig_area > 0 else 0
        st.metric("Rasio Luas BB", f"{area_ratio:.2f}x")
    
    with stat_col4:
        # Average distance from origin
        avg_dist_orig = np.mean(np.sqrt(points[:, 0]**2 + points[:, 1]**2))
        avg_dist_trans = np.mean(np.sqrt(transformed_array[:, 0]**2 + transformed_array[:, 1]**2))
        st.metric("Rata-rata Jarak", f"{avg_dist_trans:.1f} px", f"{avg_dist_trans - avg_dist_orig:+.1f}")


# Entry point
if __name__ == "__main__":
    show_week2()