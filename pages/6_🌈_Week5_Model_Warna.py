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

st.set_page_config(**PAGE_CONFIG)
st.title("🌈 Minggu 5: Model Warna & Pencahayaan")
st.markdown("--- ")

# --- Bagian 1: Konverter Model Warna ---
st.header("1. Konverter Model Warna Interaktif")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Warna (RGB)")
    # Menggunakan color picker untuk input RGB yang mudah
    hex_color = st.color_picker("Pilih warna", "#FF4B4B")
    r, g, b = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    # Tampilkan kotak warna input
    st.markdown(f"""
    <div style="width:100%; height: 50px; background-color: rgb({r}, {g}, {b}); border: 1px solid white; border-radius: 5px;">
    </div>
    """, unsafe_allow_html=True)
    st.write(f"**RGB:** `({r}, {g}, {b})`")

with col2:
    st.subheader("Hasil Konversi")
    # Konversi ke HSV
    h, s, v = rgb_to_hsv((r, g, b))
    st.write(f"**HSV:** `({h:.1f}°, {s:.2f}, {v:.2f})`")

    # Konversi ke CMYK
    c, m, y, k = rgb_to_cmyk((r, g, b))
    st.write(f"**CMYK:** `({c:.2f}, {m:.2f}, {y:.2f}, {k:.2f})`")

    # Konversi balik untuk verifikasi
    hsv_rgb = hsv_to_rgb((h, s, v))
    cmyk_rgb = cmyk_to_rgb((c, m, y, k))
    st.write(f"<small><i>(Verifikasi HSV -> RGB: {hsv_rgb})</i></small>", unsafe_allow_html=True)
    st.write(f"<small><i>(Verifikasi CMYK -> RGB: {cmyk_rgb})</i></small>", unsafe_allow_html=True)


# --- Bagian 2: Demo Pencahayaan Phong ---
st.markdown("--- ")
st.header("2. Demo Model Pencahayaan Phong")
st.info("Geser slider untuk melihat bagaimana komponen Ambient, Diffuse, dan Specular mempengaruhi warna akhir bola.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Pengaturan Pencahayaan")
    light_color_hex = st.color_picker("Warna Cahaya", "#FFFFFF")
    light_color = tuple(int(light_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    st.markdown("**Properti Material**")
    ka = st.slider("Koefisien Ambient (ka)", 0.0, 1.0, 0.1, 0.05)
    kd = st.slider("Koefisien Diffuse (kd)", 0.0, 1.0, 0.7, 0.05)
    ks = st.slider("Koefisien Specular (ks)", 0.0, 1.0, 0.5, 0.05)
    shininess = st.slider("Shininess (kilau)", 1, 256, 32)

    st.markdown("**Posisi Cahaya**")
    light_x = st.slider("Posisi X Cahaya", -2.0, 2.0, 1.0, 0.1)
    light_y = st.slider("Posisi Y Cahaya", -2.0, 2.0, 1.0, 0.1)
    light_z = st.slider("Posisi Z Cahaya", -2.0, 2.0, 1.0, 0.1)

with col2:
    st.subheader("Visualisasi pada Bola")
    
    # Simulasi bola 3D sederhana
    size = 200
    sphere_img = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Pengaturan scene
    light_pos = np.array([light_x, light_y, light_z])
    camera_pos = np.array([0, 0, 2]) # Kamera di depan bola
    material = {'ka': ka, 'kd': kd, 'ks': ks, 'shininess': shininess}

    # Loop melalui setiap piksel di gambar
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

    st.image(sphere_img, caption="Bola dengan pencahayaan Phong", use_column_width=True)
