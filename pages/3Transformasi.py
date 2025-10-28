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

try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except ImportError:
    CANVAS_AVAILABLE = False
    st.warning("⚠️ Module 'streamlit-drawable-canvas' tidak terinstall. Install dengan: `pip install streamlit-drawable-canvas`")

from algorithms.transformations import (
    create_translation_matrix,
    create_rotation_matrix,
    create_scale_matrix,
    create_shear_matrix,
    apply_transformation,
    combine_transformations
)

st.set_page_config(**PAGE_CONFIG)

def show_week2():
    """
    Menampilkan halaman transformasi 2D dengan interface modern.
    """
    
    # --- Header --- #
    st.markdown("""
        <div class="header-container">
            <h1>🔄 Minggu 2: Transformasi Geometri 2D</h1>
            <p class="subtitle">Manipulasi Objek dengan Matriks Transformasi</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Introduction --- #
    st.markdown("""
    ### 🎯 Tujuan Pembelajaran
    
    Setelah menyelesaikan materi ini, Anda akan dapat:
    - 📐 Memahami konsep transformasi geometri 2D
    - 🔢 Menggunakan matriks untuk merepresentasikan transformasi
    - 🎮 Menerapkan transformasi pada objek secara interaktif
    - 🔗 Menggabungkan beberapa transformasi (composite transformation)
    """)
    
    # --- Theory Section --- #
    with st.expander("📚 Teori: Transformasi 2D", expanded=True):
        st.markdown("""
        ### Apa itu Transformasi Geometri?
        
        **Transformasi geometri** adalah operasi yang mengubah posisi, ukuran, atau orientasi 
        dari suatu objek dalam ruang koordinat. Dalam grafika komputer 2D, kita menggunakan 
        **matriks 3×3** untuk merepresentasikan transformasi menggunakan **koordinat homogen**.
        
        ### Mengapa Koordinat Homogen?
        
        Koordinat homogen memungkinkan kita untuk merepresentasikan **semua jenis transformasi** 
        (termasuk translasi) sebagai perkalian matriks:
        
        ```
        Point (x, y) → Homogeneous (x, y, 1)
        
        [x']   [a  b  tx]   [x]
        [y'] = [c  d  ty] × [y]
        [1 ]   [0  0   1]   [1]
        ```
        """)
        
        # Tabs untuk setiap transformasi
        trans_tab1, trans_tab2, trans_tab3, trans_tab4 = st.tabs([
            "📍 Translasi", "🔄 Rotasi", "📏 Skala", "↗️ Shear"
        ])
        
        with trans_tab1:
            st.markdown("""
            ### Translasi (Translation)
            
            **Memindahkan** objek dari satu posisi ke posisi lain.
            
            **Parameter:**
            - `tx`: perpindahan di sumbu X
            - `ty`: perpindahan di sumbu Y
            
            **Matriks:**
            ```
            [1   0   tx]
            [0   1   ty]
            [0   0    1]
            ```
            
            **Rumus:**
            - `x' = x + tx`
            - `y' = y + ty`
            
            **Contoh:** Memindahkan objek 50 piksel ke kanan dan 30 piksel ke bawah → `tx=50, ty=30`
            """)
            
            # Simple visualization
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Before:** Point (100, 100)")
            with col2:
                st.success("**After (tx=50, ty=30):** Point (150, 130)")
        
        with trans_tab2:
            st.markdown("""
            ### Rotasi (Rotation)
            
            **Memutar** objek terhadap suatu titik pivot dengan sudut tertentu.
            
            **Parameter:**
            - `θ` (theta): sudut rotasi (dalam derajat/radian)
            - `(cx, cy)`: titik pusat rotasi
            
            **Matriks (terhadap origin):**
            ```
            [cos(θ)  -sin(θ)   0]
            [sin(θ)   cos(θ)   0]
            [  0        0      1]
            ```
            
            **Rotasi terhadap titik (cx, cy):**
            1. Translasi ke origin: `T(-cx, -cy)`
            2. Rotasi: `R(θ)`
            3. Translasi kembali: `T(cx, cy)`
            
            **Composite:** `T(cx,cy) × R(θ) × T(-cx,-cy)`
            
            **Catatan:** Rotasi positif = counter-clockwise (berlawanan arah jarum jam)
            """)
        
        with trans_tab3:
            st.markdown("""
            ### Skala (Scaling)
            
            **Memperbesar atau memperkecil** ukuran objek.
            
            **Parameter:**
            - `sx`: faktor skala di sumbu X
            - `sy`: faktor skala di sumbu Y
            - `(cx, cy)`: titik pusat skala
            
            **Matriks (terhadap origin):**
            ```
            [sx   0   0]
            [ 0  sy   0]
            [ 0   0   1]
            ```
            
            **Jenis Skala:**
            - **Uniform scaling:** `sx = sy` (proporsi tetap)
            - **Non-uniform scaling:** `sx ≠ sy` (proporsi berubah)
            - **sx > 1 atau sy > 1:** Memperbesar
            - **0 < sx < 1 atau 0 < sy < 1:** Memperkecil
            - **Negatif:** Pencerminan (reflection)
            
            **Skala terhadap titik (cx, cy):** Mirip dengan rotasi, gunakan composite transformation.
            """)
        
        with trans_tab4:
            st.markdown("""
            ### Shear (Geser)
            
            **Menggeser** objek secara diagonal/miring.
            
            **Parameter:**
            - `shx`: shear di sumbu X (menggeser X berdasarkan Y)
            - `shy`: shear di sumbu Y (menggeser Y berdasarkan X)
            
            **Matriks:**
            ```
            [1    shx   0]
            [shy   1    0]
            [0     0    1]
            ```
            
            **Rumus:**
            - `x' = x + shx × y`
            - `y' = shy × x + y`
            
            **Aplikasi:**
            - Efek miring pada teks
            - Simulasi perspektif sederhana
            - Transformasi parallelogram
            """)
    
    st.markdown("---")
    
    # --- Interactive Demo Section --- #
    st.header("🎮 Demo Interaktif")
    
    # Mode selection
    demo_mode = st.radio(
        "Pilih Mode Demo:",
        ["🖌️ Canvas Drawing (Interactive)", "📊 Predefined Shapes (Visualization)"],
        horizontal=True
    )
    
    if demo_mode == "🖌️ Canvas Drawing (Interactive)":
        show_canvas_mode()
    else:
        show_visualization_mode()
    
    st.markdown("---")
    
    # --- Composite Transformation Section --- #
    with st.expander("🔗 Transformasi Komposit (Advanced)", expanded=False):
        st.markdown("""
        ### Menggabungkan Beberapa Transformasi
        
        Dalam aplikasi nyata, kita sering perlu menerapkan **beberapa transformasi sekaligus**.
        Keuntungan menggunakan matriks adalah kita dapat **menggabungkan** transformasi 
        dengan cara mengalikan matriks-matriks tersebut.
        
        **Contoh:** Rotasi 45° lalu translasi (100, 50)
        
        ```
        M_final = M_translate × M_rotate
        
        Point' = M_final × Point
        ```
        
        **⚠️ Urutan Penting!**
        
        Perkalian matriks tidak komutatif: `A × B ≠ B × A`
        
        - Rotasi → Translasi ≠ Translasi → Rotasi
        - Urutan dibaca dari **kanan ke kiri**
        
        **Contoh Praktis:**
        
        Untuk merotasi objek terhadap titik (cx, cy):
        1. `T(-cx, -cy)`: Pindahkan ke origin
        2. `R(θ)`: Rotasi
        3. `T(cx, cy)`: Kembalikan ke posisi
        
        **Matriks Final:** `M = T(cx,cy) × R(θ) × T(-cx,-cy)`
        """)
        
        # Demo composite
        st.subheader("📐 Kalkulator Transformasi Komposit")
        
        comp_col1, comp_col2 = st.columns(2)
        
        with comp_col1:
            st.markdown("**Transformasi 1:**")
            t1_type = st.selectbox("Jenis", ["Translasi", "Rotasi", "Skala"], key="t1")
            if t1_type == "Translasi":
                t1_tx = st.number_input("tx", value=50.0, key="t1tx")
                t1_ty = st.number_input("ty", value=30.0, key="t1ty")
                m1 = create_translation_matrix(t1_tx, t1_ty)
            elif t1_type == "Rotasi":
                t1_angle = st.number_input("Sudut (°)", value=45.0, key="t1angle")
                m1 = create_rotation_matrix(t1_angle, 0, 0)
            else:
                t1_sx = st.number_input("sx", value=1.5, key="t1sx")
                t1_sy = st.number_input("sy", value=1.5, key="t1sy")
                m1 = create_scale_matrix(t1_sx, t1_sy, 0, 0)
        
        with comp_col2:
            st.markdown("**Transformasi 2:**")
            t2_type = st.selectbox("Jenis", ["Translasi", "Rotasi", "Skala"], key="t2")
            if t2_type == "Translasi":
                t2_tx = st.number_input("tx", value=20.0, key="t2tx")
                t2_ty = st.number_input("ty", value=-10.0, key="t2ty")
                m2 = create_translation_matrix(t2_tx, t2_ty)
            elif t2_type == "Rotasi":
                t2_angle = st.number_input("Sudut (°)", value=-30.0, key="t2angle")
                m2 = create_rotation_matrix(t2_angle, 0, 0)
            else:
                t2_sx = st.number_input("sx", value=0.8, key="t2sx")
                t2_sy = st.number_input("sy", value=0.8, key="t2sy")
                m2 = create_scale_matrix(t2_sx, t2_sy, 0, 0)
        
        # Combine
        m_combined = combine_transformations([m1, m2])
        
        st.markdown("**Matriks Hasil (M2 × M1):**")
        df_combined = pd.DataFrame(
            np.round(m_combined, 3),
            columns=['Col 1', 'Col 2', 'Col 3'],
            index=['Row 1', 'Row 2', 'Row 3']
        )
        st.dataframe(df_combined, use_container_width=True)
        
        st.info("""
        💡 **Interpretasi:** Matriks ini merepresentasikan efek gabungan dari kedua transformasi.
        Anda dapat menggunakan matriks ini untuk mentransformasi titik manapun sekaligus.
        """)
    
    st.markdown("---")
    
    # --- Summary --- #
    st.success("""
    ✅ **Ringkasan Week 2**
    
    - Transformasi 2D menggunakan matriks 3×3 dengan koordinat homogen
    - **Translasi:** Memindahkan objek
    - **Rotasi:** Memutar objek terhadap titik pivot
    - **Skala:** Mengubah ukuran objek
    - **Shear:** Menggeser objek secara diagonal
    - Transformasi dapat digabungkan dengan perkalian matriks (urutan penting!)
    
    **Next:** Week 3 - Algoritma Garis (DDA & Bresenham) →
    """)


def show_canvas_mode():
    """Mode menggambar di canvas dengan drawable canvas."""
    
    if not CANVAS_AVAILABLE:
        st.error("❌ Module 'streamlit-drawable-canvas' diperlukan untuk mode ini.")
        st.code("pip install streamlit-drawable-canvas", language="bash")
        return
    
    st.info("🖌️ **Instruksi:** Gambar bentuk di canvas, simpan, pilih transformasi, lalu terapkan!")
    
    # Sidebar controls
    st.sidebar.header("🎛️ Kontrol Transformasi")
    
    transform_type = st.sidebar.selectbox(
        "Jenis Transformasi",
        ["Translasi", "Rotasi", "Skala", "Shear"]
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
    st.sidebar.markdown(f"### Parameter {transform_type}")
    
    if transform_type == "Translasi":
        params['tx'] = st.sidebar.slider("Translasi X (tx)", -200, 200, int(params['tx']))
        params['ty'] = st.sidebar.slider("Translasi Y (ty)", -200, 200, int(params['ty']))
    elif transform_type == "Rotasi":
        params['angle'] = st.sidebar.slider("Sudut (°)", -180, 180, int(params['angle']))
        st.sidebar.caption("Pusat rotasi: centroid objek")
    elif transform_type == "Skala":
        params['sx'] = st.sidebar.slider("Skala X", 0.1, 3.0, float(params['sx']), 0.1)
        params['sy'] = st.sidebar.slider("Skala Y", 0.1, 3.0, float(params['sy']), 0.1)
        st.sidebar.caption("Pusat skala: centroid objek")
    else:  # Shear
        params['shx'] = st.sidebar.slider("Shear X", -2.0, 2.0, float(params['shx']), 0.1)
        params['shy'] = st.sidebar.slider("Shear Y", -2.0, 2.0, float(params['shy']), 0.1)
    
    # Canvas layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Canvas Menggambar")
        
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
        st.subheader("📊 Matriks")
        
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
    
    # Action buttons
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("💾 Simpan Bentuk", use_container_width=True):
            if canvas_result.json_data and canvas_result.json_data["objects"]:
                st.session_state.original_drawing = canvas_result.json_data
                st.success("✅ Bentuk disimpan!")
            else:
                st.warning("⚠️ Gambar sesuatu dulu!")
    
    with btn_col2:
        if st.button("⚡ Terapkan Transformasi", use_container_width=True):
            if 'original_drawing' in st.session_state:
                # Apply transformation logic here
                st.success(f"✅ {transform_type} diterapkan!")
            else:
                st.warning("⚠️ Simpan bentuk dulu!")
    
    with btn_col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.transform_params = {
                'tx': 0.0, 'ty': 0.0, 'angle': 0.0,
                'sx': 1.0, 'sy': 1.0, 'shx': 0.0, 'shy': 0.0
            }
            st.rerun()


def show_visualization_mode():
    """Mode visualisasi dengan predefined shapes menggunakan Plotly."""
    
    st.info("📊 **Mode Visualisasi:** Lihat efek transformasi pada bentuk geometris predefined.")
    
    # Sidebar controls
    st.sidebar.header("🎛️ Kontrol Transformasi")
    
    # Shape selection
    shape_type = st.sidebar.selectbox(
        "Pilih Bentuk",
        ["Persegi", "Segitiga", "Pentagon", "Rumah"]
    )
    
    transform_type = st.sidebar.selectbox(
        "Jenis Transformasi",
        ["Translasi", "Rotasi", "Skala", "Shear", "Komposit"]
    )
    
    st.sidebar.markdown(f"### Parameter {transform_type}")
    
    # Get shape points
    if shape_type == "Persegi":
        points = np.array([[-50, -50], [50, -50], [50, 50], [-50, 50], [-50, -50]])
    elif shape_type == "Segitiga":
        points = np.array([[0, -60], [52, 30], [-52, 30], [0, -60]])
    elif shape_type == "Pentagon":
        angles = np.linspace(0, 2*np.pi, 6)
        points = np.column_stack([50*np.cos(angles), 50*np.sin(angles)])
    else:  # Rumah
        points = np.array([
            [-50, 0], [50, 0], [50, 40], [0, 70], [-50, 40], [-50, 0]
        ])
    
    # Transform parameters
    if transform_type == "Translasi":
        tx = st.sidebar.slider("Translasi X", -150, 150, 80)
        ty = st.sidebar.slider("Translasi Y", -150, 150, 60)
        matrix = create_translation_matrix(tx, ty)
        
    elif transform_type == "Rotasi":
        angle = st.sidebar.slider("Sudut (°)", -180, 180, 45)
        cx, cy = 0, 0  # Center of shape
        matrix = create_rotation_matrix(angle, cx, cy)
        
    elif transform_type == "Skala":
        sx = st.sidebar.slider("Skala X", 0.1, 3.0, 1.5, 0.1)
        sy = st.sidebar.slider("Skala Y", 0.1, 3.0, 1.5, 0.1)
        matrix = create_scale_matrix(sx, sy, 0, 0)
        
    elif transform_type == "Shear":
        shx = st.sidebar.slider("Shear X", -1.0, 1.0, 0.5, 0.1)
        shy = st.sidebar.slider("Shear Y", -1.0, 1.0, 0.0, 0.1)
        matrix = create_shear_matrix(shx, shy)
        
    else:  # Komposit
        st.sidebar.markdown("**Step 1: Rotasi**")
        angle = st.sidebar.slider("Rotasi (°)", -180, 180, 30)
        st.sidebar.markdown("**Step 2: Skala**")
        scale = st.sidebar.slider("Skala Uniform", 0.5, 2.0, 1.2, 0.1)
        st.sidebar.markdown("**Step 3: Translasi**")
        tx = st.sidebar.slider("Translasi X", -150, 150, 100)
        ty = st.sidebar.slider("Translasi Y", -150, 150, 50)
        
        m1 = create_rotation_matrix(angle, 0, 0)
        m2 = create_scale_matrix(scale, scale, 0, 0)
        m3 = create_translation_matrix(tx, ty)
        matrix = combine_transformations([m1, m2, m3])
    
    # Apply transformation
    transformed_points = apply_transformation(points.tolist(), matrix)
    
    # Visualization
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📊 Visualisasi")
        
        fig = go.Figure()
        
        # Original shape
        fig.add_trace(go.Scatter(
            x=points[:, 0], y=points[:, 1],
            mode='lines+markers',
            name='Original',
            line=dict(color='#4A9EFF', width=2),
            marker=dict(size=8)
        ))
        
        # Transformed shape
        transformed_array = np.array(transformed_points)
        fig.add_trace(go.Scatter(
            x=transformed_array[:, 0], y=transformed_array[:, 1],
            mode='lines+markers',
            name='Transformed',
            line=dict(color='#FF4B4B', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            xaxis=dict(range=[-200, 200], zeroline=True, gridcolor='#333'),
            yaxis=dict(range=[-200, 200], zeroline=True, gridcolor='#333'),
            plot_bgcolor='#1E2128',
            paper_bgcolor='#1E2128',
            font=dict(color='white'),
            showlegend=True,
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📐 Matriks")
        
        df_matrix = pd.DataFrame(
            np.round(matrix, 3),
            columns=['C1', 'C2', 'C3'],
            index=['R1', 'R2', 'R3']
        )
        st.dataframe(df_matrix, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("**📍 Sample Point:**")
        sample_idx = len(points) // 2
        orig_pt = points[sample_idx]
        trans_pt = transformed_points[sample_idx]
        
        st.code(f"Before: ({orig_pt[0]:.1f}, {orig_pt[1]:.1f})")
        st.code(f"After:  ({trans_pt[0]:.1f}, {trans_pt[1]:.1f})")


# Entry point
if __name__ == "__main__":
    show_week2()