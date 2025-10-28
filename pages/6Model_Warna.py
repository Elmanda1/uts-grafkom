"""
Halaman Minggu 5: Model Warna dan Pencahayaan.

Menyediakan alat interaktif untuk konversi model warna (RGB, HSV, CMYK)
dan eksplorasi model pencahayaan Phong dasar.
"""

import streamlit as st
import numpy as np

from config import PAGE_CONFIG
from algorithms.color_models import (
    rgb_to_hsv, hsv_to_rgb,
    rgb_to_cmyk, cmyk_to_rgb,
    calculate_phong_lighting
)
from utils.helpers import load_css

st.set_page_config(**PAGE_CONFIG)

# Memuat CSS kustom
try:
    load_css("assets/styles/custom.css")
except Exception as e:
    st.warning(f"⚠️ CSS kustom tidak dimuat: {e}")

# --- Hero Section --- #
st.markdown("""
    <div class="header-container">
        <h1>Model Warna & Pencahayaan</h1>
        <p class="subtitle">Eksplorasi konversi model warna dan pencahayaan Phong interaktif</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Introduction Section --- #
intro_col1, intro_col2 = st.columns([3, 2])

with intro_col1:
    ### Tujuan Pembelajaran
    st.markdown("""
    Pada minggu ini, Anda akan mempelajari konsep fundamental tentang 
    model warna dan pencahayaan dalam grafika komputer:
    
    - **Model Warna RGB** - Representasi warna berbasis Red, Green, Blue
    - **Model Warna HSV** - Representasi warna berbasis Hue, Saturation, Value
    - **Model Warna CMYK** - Representasi warna untuk printing
    - **Model Pencahayaan Phong** - Simulasi pencahayaan realistis
    
    Memahami konversi antar model warna dan cara cahaya berinteraksi dengan objek 3D.
    """)

with intro_col2:
    st.info("""
    ### 📌 Petunjuk Penggunaan
    
    **Langkah-langkah:**
    
    1. Pilih **warna** menggunakan color picker
    2. Lihat **konversi otomatis** ke HSV & CMYK
    3. Atur **parameter pencahayaan** Phong
    4. Amati **efek visual** pada bola 3D
    5. Eksplorasi **berbagai kombinasi**
    
    *Geser slider untuk melihat perubahan real-time!*
    """)

st.markdown("---")

# --- Sidebar Kontrol--- #
st.sidebar.markdown("### Pengaturan")
section_choice = st.sidebar.selectbox(
    "Pilih Bagian",
    ["Konverter Model Warna", "Model Pencahayaan Phong", "Keduanya"],
    help="Pilih bagian yang ingin Anda eksplorasi"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Informasi")

# --- Konsep Section --- #
with st.expander("**Konsep: Model Warna & Pencahayaan**", expanded=False):
    concept_col1, concept_col2 = st.columns(2)
    
    with concept_col1:
        st.markdown("""
        **Model Warna**
        
        Model warna adalah cara merepresentasikan dan memanipulasi warna:
        
        - **RGB**: Additive color model (layar)
        - **HSV**: Intuitif untuk pemilihan warna
        - **CMYK**: Subtractive color model (printer)
        
        Setiap model memiliki kegunaan spesifik dalam aplikasi grafika.
        
        **Konversi:** RGB ↔ HSV ↔ CMYK
        """)
    
    with concept_col2:
        st.markdown("""
        **Model Pencahayaan Phong**
        
        Phong adalah model pencahayaan lokal yang mengkombinasikan:
        
        - **Ambient**: Cahaya dasar lingkungan
        - **Diffuse**: Refleksi cahaya tersebar
        - **Specular**: Pantulan mengkilap
        
        Formula: **I = Ia + Id + Is**
        
        **Digunakan untuk:** Rendering realistis objek 3D
        """)

st.markdown("---")

# --- Bagian 1: Konverter Model Warna ---
if section_choice in ["Konverter Model Warna", "Keduanya"]:
    st.markdown("### Konverter Model Warna Interaktif")
    st.info("👇 Pilih warna menggunakan color picker untuk melihat konversi otomatis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Input Warna (RGB)")
        # Menggunakan color picker untuk input RGB yang mudah
        hex_color = st.color_picker("Pilih warna", "#FF4B4B")
        r, g, b = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        # Tampilkan kotak warna input
        st.markdown(f"""
        <div style="width:100%; height: 100px; background-color: rgb({r}, {g}, {b}); border: 2px solid white; border-radius: 10px; margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**RGB Values:** `R={r}, G={g}, B={b}`")
        st.markdown(f"**Hex Code:** `{hex_color}`")

    with col2:
        st.markdown("#### Hasil Konversi")
        
        # Konversi ke HSV
        h, s, v = rgb_to_hsv((r, g, b))
        st.markdown("**Model HSV (Hue, Saturation, Value)**")
        st.markdown(f"- **Hue:** `{h:.1f}°` (0-360°)")
        st.markdown(f"- **Saturation:** `{s:.2f}` (0-1)")
        st.markdown(f"- **Value:** `{v:.2f}` (0-1)")

        st.markdown("---")

        # Konversi ke CMYK
        c, m, y, k = rgb_to_cmyk((r, g, b))
        st.markdown("**Model CMYK (Cyan, Magenta, Yellow, Key)**")
        st.markdown(f"- **Cyan:** `{c:.2f}` (0-1)")
        st.markdown(f"- **Magenta:** `{m:.2f}` (0-1)")
        st.markdown(f"- **Yellow:** `{y:.2f}` (0-1)")
        st.markdown(f"- **Key (Black):** `{k:.2f}` (0-1)")

    # Verifikasi konversi
    with st.expander("**Verifikasi Konversi Balik**", expanded=False):
        ver_col1, ver_col2 = st.columns(2)
        
        with ver_col1:
            hsv_rgb = hsv_to_rgb((h, s, v))
            st.markdown("**HSV → RGB:**")
            st.markdown(f"`{hsv_rgb}`")
            if hsv_rgb == (r, g, b):
                st.success("✅ Konversi akurat!")
            else:
                st.warning(f"⚠️ Selisih kecil: {abs(hsv_rgb[0]-r)}, {abs(hsv_rgb[1]-g)}, {abs(hsv_rgb[2]-b)}")
        
        with ver_col2:
            cmyk_rgb = cmyk_to_rgb((c, m, y, k))
            st.markdown("**CMYK → RGB:**")
            st.markdown(f"`{cmyk_rgb}`")
            if cmyk_rgb == (r, g, b):
                st.success("✅ Konversi akurat!")
            else:
                st.warning(f"⚠️ Selisih kecil: {abs(cmyk_rgb[0]-r)}, {abs(cmyk_rgb[1]-g)}, {abs(cmyk_rgb[2]-b)}")

    st.markdown("---")

# --- Bagian 2: Demo Pencahayaan Phong ---
if section_choice in ["Model Pencahayaan Phong", "Keduanya"]:
    st.markdown("### Model Pencahayaan Phong")
    st.info("Geser slider untuk melihat bagaimana komponen Ambient, Diffuse, dan Specular mempengaruhi warna akhir bola")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Pengaturan Pencahayaan")
        
        st.markdown("**Warna Cahaya**")
        light_color_hex = st.color_picker("Pilih Warna Cahaya", "#FFFFFF")
        light_color = tuple(int(light_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        st.markdown("---")
        st.markdown("**Properti Material**")
        ka = st.slider("Koefisien Ambient (ka)", 0.0, 1.0, 0.1, 0.05, 
                      help="Cahaya lingkungan dasar")
        kd = st.slider("Koefisien Diffuse (kd)", 0.0, 1.0, 0.7, 0.05,
                      help="Refleksi cahaya tersebar")
        ks = st.slider("Koefisien Specular (ks)", 0.0, 1.0, 0.5, 0.05,
                      help="Pantulan mengkilap")
        shininess = st.slider("Shininess (kilau)", 1, 256, 32,
                             help="Tingkat kilau permukaan")

        st.markdown("---")
        st.markdown("**Posisi Cahaya (XYZ)**")
        light_x = st.slider("Posisi X", -2.0, 2.0, 1.0, 0.1)
        light_y = st.slider("Posisi Y", -2.0, 2.0, 1.0, 0.1)
        light_z = st.slider("Posisi Z", -2.0, 2.0, 1.0, 0.1)

        # Info sidebar
        st.sidebar.markdown(f"**Cahaya:** `RGB{light_color}`")
        st.sidebar.markdown(f"**Posisi:** `({light_x:.1f}, {light_y:.1f}, {light_z:.1f})`")
        st.sidebar.markdown(f"**Material:**")
        st.sidebar.markdown(f"- Ambient: `{ka:.2f}`")
        st.sidebar.markdown(f"- Diffuse: `{kd:.2f}`")
        st.sidebar.markdown(f"- Specular: `{ks:.2f}`")
        st.sidebar.markdown(f"- Shininess: `{shininess}`")

    with col2:
        st.markdown("#### Visualisasi Hasil")
        
        # Simulasi bola 3D sederhana
        size = 300
        sphere_img = np.zeros((size, size, 3), dtype=np.uint8)
        
        # Pengaturan scene
        light_pos = np.array([light_x, light_y, light_z])
        camera_pos = np.array([0, 0, 2]) # Kamera di depan bola
        material = {'ka': ka, 'kd': kd, 'ks': ks, 'shininess': shininess}

        # Progress bar untuk rendering
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Loop melalui setiap piksel di gambar
        total_pixels = size * size
        processed = 0
        
        for i in range(size):
            for j in range(size):
                # Konversi koordinat piksel ke ruang 3D di permukaan bola
                x = (j - size / 2) / (size / 2)
                y = (size / 2 - i) / (size / 2)
                
                z2 = 1.0 - x*x - y*y
                if z2 > 0: # Jika piksel ada di dalam lingkaran bola
                    z = np.sqrt(z2)
                    point_pos = np.array([x, y, z])
                    point_normal = point_pos # Untuk bola, normal sama dengan posisi relatif ke pusat
                    
                    # Hitung warna menggunakan Phong
                    color = calculate_phong_lighting(
                        light_color=light_color,
                        light_position=light_pos,
                        camera_position=camera_pos,
                        point_position=point_pos,
                        point_normal=point_normal,
                        material=material
                    )
                    sphere_img[i, j] = color
                
                processed += 1
            
            # Update progress setiap baris
            if i % 10 == 0:
                progress = int((i / size) * 100)
                progress_bar.progress(progress)
                status_text.text(f"⏳ Rendering... {progress}%")
        
        progress_bar.progress(100)
        status_text.text("Rendering selesai!")
        
        st.image(sphere_img, caption="Bola 3D dengan Model Pencahayaan Phong", use_column_width=True)
        
        st.success("Visualisasi berhasil dibuat!")

    # Analisis Komponen
    with st.expander("**Analisis Komponen Pencahayaan**", expanded=False):
        analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
        
        with analysis_col1:
            st.markdown("**Ambient**")
            ambient_contribution = ka * 100
            st.metric("Kontribusi", f"{ambient_contribution:.1f}%")
            st.markdown("Cahaya dasar yang merata di seluruh permukaan")
        
        with analysis_col2:
            st.markdown("**Diffuse**")
            diffuse_contribution = kd * 100
            st.metric("Kontribusi", f"{diffuse_contribution:.1f}%")
            st.markdown("Refleksi cahaya bergantung pada sudut permukaan")
        
        with analysis_col3:
            st.markdown("**Specular**")
            specular_contribution = ks * 100
            st.metric("Kontribusi", f"{specular_contribution:.1f}%")
            st.markdown(f"Pantulan mengkilap (shininess: {shininess})")

# --- Perbandingan Detail --- #
with st.expander("**Perbandingan Model Warna**", expanded=False):
    comp_col1, comp_col2, comp_col3 = st.columns(3)
    
    with comp_col1:
        st.markdown("""
        **Model RGB:**
        - ✅ Standar untuk display digital
        - ✅ Mudah dipahami (R, G, B)
        - ✅ Additive color mixing
        - ❌ Tidak intuitif untuk pemilihan warna
        
        **Aplikasi:** Monitor, TV, kamera
        """)
    
    with comp_col2:
        st.markdown("""
        **Model HSV:**
        - ✅ Intuitif untuk manusia
        - ✅ Mudah untuk color picking
        - ✅ Memisahkan warna & brightness
        - ❌ Perlu konversi untuk display
        
        **Aplikasi:** Editor grafis, color picker
        """)
    
    with comp_col3:
        st.markdown("""
        **Model CMYK:**
        - ✅ Standar untuk printing
        - ✅ Subtractive color mixing
        - ✅ Akurat untuk reproduksi cetak
        - ❌ Gamut lebih sempit dari RGB
        
        **Aplikasi:** Printer, percetakan
        """)

st.markdown("---")

# --- Implementasi Kode --- #
st.markdown("### Implementasi Kode")

with st.expander("**Lihat Kode Implementasi**", expanded=False):
    st.markdown("""
    Berikut adalah implementasi lengkap dari konversi model warna dan 
    perhitungan pencahayaan Phong. Perhatikan penggunaan rumus matematis 
    untuk transformasi antar model warna.
    """)
    
    st.markdown("---")
    
    # Muat kode dari file untuk konsistensi
    try:
        with open("algorithms/color_models.py", "r") as f:
            code_content = f.read()
            st.code(code_content, language="python")
    except FileNotFoundError:
        st.warning("⚠️ File `algorithms/color_models.py` tidak ditemukan")

# --- Footer --- #
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Tips:</strong> Coba kombinasi berbeda dari parameter material untuk melihat efek pencahayaan yang bervariasi!</p>
    <p>Minggu 5: Model Warna & Pencahayaan | © 2025 Grafika Komputer</p>
</div>
""", unsafe_allow_html=True)