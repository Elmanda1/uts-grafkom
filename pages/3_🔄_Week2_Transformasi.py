"""
Halaman Minggu 2: Transformasi Geometri 2D.

Menyediakan antarmuka interaktif untuk menerapkan transformasi 2D
(translasi, rotasi, skala, shear) pada objek yang digambar di canvas.
"""

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

from config import PAGE_CONFIG, CANVAS_WIDTH, CANVAS_HEIGHT
from utils.canvas_utils import setup_canvas, get_canvas_data
from algorithms.transformations import (
    create_translation_matrix,
    create_rotation_matrix,
    create_scale_matrix,
    create_shear_matrix,
    apply_transformation,
    combine_transformations
)

st.set_page_config(**PAGE_CONFIG)
st.title("🔄 Minggu 2: Transformasi Geometri 2D")
st.markdown("--- ")

st.info("Gambar sebuah bentuk (misal: persegi atau segitiga) di canvas, lalu terapkan transformasi dari sidebar.")

# --- Sidebar untuk Kontrol --- #
st.sidebar.header("Kontrol Transformasi")

# Pilihan mode transformasi
transform_type = st.sidebar.selectbox(
    "Pilih Jenis Transformasi",
    ["Translasi", "Rotasi", "Skala", "Shear"]
)

# Inisialisasi parameter di session state
if 'transform_params' not in st.session_state:
    st.session_state.transform_params = {
        'tx': 0.0, 'ty': 0.0,
        'angle': 0.0, 'cx': 0.0, 'cy': 0.0,
        'sx': 1.0, 'sy': 1.0,
        'shx': 0.0, 'shy': 0.0
    }

params = st.session_state.transform_params

# Tampilkan slider berdasarkan pilihan
if transform_type == "Translasi":
    params['tx'] = st.sidebar.slider("Translasi X (tx)", -100, 100, int(params['tx']))
    params['ty'] = st.sidebar.slider("Translasi Y (ty)", -100, 100, int(params['ty']))
elif transform_type == "Rotasi":
    params['angle'] = st.sidebar.slider("Sudut Rotasi (derajat)", -180, 180, int(params['angle']))
    st.sidebar.markdown("_*Pusat rotasi (cx, cy) diambil dari pusat objek_.")
elif transform_type == "Skala":
    params['sx'] = st.sidebar.slider("Skala X (sx)", 0.1, 3.0, float(params['sx']), 0.1)
    params['sy'] = st.sidebar.slider("Skala Y (sy)", 0.1, 3.0, float(params['sy']), 0.1)
    st.sidebar.markdown("_*Pusat skala (cx, cy) diambil dari pusat objek_.")
elif transform_type == "Shear":
    params['shx'] = st.sidebar.slider("Shear X (shx)", -1.0, 1.0, float(params['shx']), 0.1)
    params['shy'] = st.sidebar.slider("Shear Y (shy)", -1.0, 1.0, float(params['shy']), 0.1)

# --- Canvas dan Logika Transformasi --- #
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Canvas Interaktif")
    # Setup canvas untuk menggambar bebas
    canvas_result = setup_canvas(
        drawing_mode="freedraw",
        stroke_width=3,
        key="transform_canvas"
    )

# Inisialisasi session state untuk menyimpan gambar asli
if 'original_drawing' not in st.session_state:
    st.session_state.original_drawing = None
if 'transformed_drawing' not in st.session_state:
    st.session_state.transformed_drawing = None

# Tombol untuk menyimpan gambar asli
if st.button("Simpan Bentuk Asli"):
    drawing_data = get_canvas_data(canvas_result)
    if drawing_data and drawing_data["objects"]:
        st.session_state.original_drawing = drawing_data
        st.session_state.transformed_drawing = drawing_data # Reset saat menyimpan
        st.success("Bentuk asli berhasil disimpan!")
    else:
        st.warning("Silakan gambar sesuatu terlebih dahulu.")

# Tombol untuk menerapkan transformasi
if st.button("Terapkan Transformasi"):
    if st.session_state.original_drawing:
        original_data = st.session_state.original_drawing
        transformed_data = {"version": original_data["version"], "objects": []}
        
        all_points = []
        for obj in original_data["objects"]:
            if obj['type'] == 'path':
                for path_segment in obj['path']:
                    if path_segment[0] == 'Q': # Quadratic curve
                        all_points.append(path_segment[1:3])
                        all_points.append(path_segment[3:5])
                    elif path_segment[0] == 'L': # Line
                        all_points.append(path_segment[1:3])
                    elif path_segment[0] == 'M': # Move
                        all_points.append(path_segment[1:3])

        if not all_points:
            st.warning("Tidak ada titik yang bisa ditransformasi.")
        else:
            # Hitung pusat objek untuk rotasi dan skala
            center_x = np.mean([p[0] for p in all_points])
            center_y = np.mean([p[1] for p in all_points])

            # Buat matriks transformasi
            matrix = np.identity(3)
            if transform_type == "Translasi":
                matrix = create_translation_matrix(params['tx'], params['ty'])
            elif transform_type == "Rotasi":
                matrix = create_rotation_matrix(params['angle'], center_x, center_y)
            elif transform_type == "Skala":
                matrix = create_scale_matrix(params['sx'], params['sy'], center_x, center_y)
            elif transform_type == "Shear":
                matrix = create_shear_matrix(params['shx'], params['shy'])

            # Terapkan transformasi ke setiap objek
            for obj in original_data["objects"]:
                new_obj = obj.copy()
                if obj['type'] == 'path':
                    new_path = []
                    for path_segment in obj['path']:
                        segment_type = path_segment[0]
                        points = np.array(path_segment[1:]).reshape(-1, 2).tolist()
                        transformed_points = apply_transformation(points, matrix)
                        flat_points = [coord for point in transformed_points for coord in point]
                        new_path.append([segment_type] + flat_points)
                    new_obj['path'] = new_path
                transformed_data["objects"].append(new_obj)
            
            st.session_state.transformed_drawing = transformed_data
            st.success(f"Transformasi {transform_type} diterapkan.")
            
            # Tampilkan matriks di kolom kedua
            with col2:
                st.subheader("Matriks Transformasi")
                st.code(np.round(matrix, 2), language='text')

    else:
        st.warning("Simpan bentuk asli terlebih dahulu sebelum menerapkan transformasi.")

# Tombol Reset
if st.button("Reset Transformasi"):
    st.session_state.transformed_drawing = st.session_state.original_drawing
    st.success("Transformasi di-reset ke bentuk asli.")

# Tampilkan canvas kedua dengan hasil transformasi
with col1:
    st.subheader("Hasil Transformasi")
    if st.session_state.transformed_drawing:
        st_canvas(
            initial_drawing=st.session_state.transformed_drawing,
            key="transformed_canvas",
            height=CANVAS_HEIGHT,
            width=CANVAS_WIDTH,
            drawing_mode='static' # Hanya untuk tampilan
        )
    else:
        st.info("Hasil transformasi akan muncul di sini.")
