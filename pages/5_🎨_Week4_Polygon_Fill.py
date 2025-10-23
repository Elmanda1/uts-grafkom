"""
Halaman Minggu 4: Algoritma Pengisian Poligon.

Memungkinkan pengguna untuk menggambar poligon, memilih titik awal (seed),
dan menerapkan algoritma pengisian yang berbeda.
"""

import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import random

from config import PAGE_CONFIG, CANVAS_WIDTH, CANVAS_HEIGHT
from utils.canvas_utils import setup_canvas
from utils.code_viewer import show_code, compare_algorithms, show_performance_metrics
from algorithms.polygon_fill import scanline_fill, flood_fill_4, boundary_fill_4

st.set_page_config(**PAGE_CONFIG)
st.title("🎨 Minggu 4: Algoritma Pengisian Poligon")
st.markdown("--- ")

# --- Sidebar & State Management ---
st.sidebar.header("Pengaturan Poligon")

# Session state untuk menyimpan poligon dan seed
if 'polygon_vertices' not in st.session_state:
    st.session_state.polygon_vertices = []
if 'seed_point' not in st.session_state:
    st.session_state.seed_point = None

algo_choice = st.sidebar.selectbox(
    "Pilih Algoritma Fill",
    ["Scanline Fill", "Flood Fill", "Boundary Fill"]
)
fill_color_hex = st.sidebar.color_picker("Pilih Warna Isian", "#FF4B4B")
fill_color_rgb = tuple(int(fill_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

boundary_color_hex = st.sidebar.color_picker("Pilih Warna Batas", "#00C853")
boundary_color_rgb = tuple(int(boundary_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

# --- Canvas untuk Input --- #
st.subheader("1. Gambar Poligon & Pilih Seed")
st.info("Mode `polygon`: Klik untuk menambah titik, klik titik pertama untuk menutup. Mode `point`: Klik untuk memilih seed point.")

drawing_mode = st.radio("Mode Canvas:", ('polygon', 'point'), horizontal=True)

canvas_result = setup_canvas(
    drawing_mode=drawing_mode,
    stroke_color=boundary_color_hex,
    stroke_width=3,
    key="polygon_canvas"
)

# --- Logika untuk memproses input canvas ---
if canvas_result.json_data and canvas_result.json_data["objects"]:
    last_obj = canvas_result.json_data["objects"][-1]
    if drawing_mode == 'polygon' and last_obj['type'] == 'polygon':
        st.session_state.polygon_vertices = [(p[1], p[2]) for p in last_obj['path']]
        st.success(f"Poligon dengan {len(st.session_state.polygon_vertices)} titik disimpan.")
    elif drawing_mode == 'point' and last_obj['type'] == 'point':
        st.session_state.seed_point = (int(last_obj['left']), int(last_obj['top']))
        st.success(f"Seed point diatur ke {st.session_state.seed_point}")

if st.sidebar.button("Reset Poligon & Seed"):
    st.session_state.polygon_vertices = []
    st.session_state.seed_point = None
    st.experimental_rerun()

st.sidebar.write("**Status Saat Ini:**")
st.sidebar.write(f"- Titik Poligon: `{len(st.session_state.polygon_vertices)}`")
st.sidebar.write(f"- Seed Point: `{st.session_state.seed_point}`")

# --- Eksekusi Algoritma & Tampilan Hasil ---
st.markdown("--- ")
st.subheader("2. Hasil Pengisian")

if st.button("Mulai Proses Pengisian"):
    if not st.session_state.polygon_vertices:
        st.warning("Gambar sebuah poligon terlebih dahulu.")
    else:
        # Buat canvas dasar (numpy array) untuk algoritma
        base_img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "black")
        draw = ImageDraw.Draw(base_img)
        draw.polygon(st.session_state.polygon_vertices, outline=boundary_color_rgb, width=2)
        canvas_np = np.array(base_img)

        filled_pixels = []
        metrics = {}

        if algo_choice == "Scanline Fill":
            if not st.session_state.polygon_vertices:
                st.error("Scanline Fill memerlukan poligon tertutup.")
            else:
                result = scanline_fill(st.session_state.polygon_vertices, fill_color_rgb)
                filled_pixels = result.get("result", [])
                metrics = {'name': 'Scanline', 'time': result['execution_time_ms'], 'ops': result['operations']}

        elif algo_choice == "Flood Fill":
            if not st.session_state.seed_point:
                st.error("Flood Fill memerlukan seed point.")
            else:
                target_color = tuple(canvas_np[st.session_state.seed_point[1], st.session_state.seed_point[0]])
                result = flood_fill_4(canvas_np.copy(), st.session_state.seed_point, fill_color_rgb, target_color)
                filled_pixels = result.get("result", [])
                metrics = {'name': 'Flood Fill', 'time': result['execution_time_ms'], 'ops': result['operations']}

        elif algo_choice == "Boundary Fill":
            if not st.session_state.seed_point:
                st.error("Boundary Fill memerlukan seed point.")
            else:
                result = boundary_fill_4(canvas_np.copy(), st.session_state.seed_point, fill_color_rgb, boundary_color_rgb)
                filled_pixels = result.get("result", [])
                metrics = {'name': 'Boundary Fill', 'time': result['execution_time_ms'], 'ops': result['operations']}

        if filled_pixels:
            # Gambar hasil
            result_img = base_img.copy()
            draw_result = ImageDraw.Draw(result_img)
            if filled_pixels:
                 draw_result.point(filled_pixels, fill=fill_color_rgb)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(result_img, caption=f"Hasil dari {algo_choice}")
            with col2:
                show_performance_metrics(metrics['name'], metrics['time'], metrics['ops'])
        else:
            st.warning("Tidak ada piksel yang diisi. Periksa seed point atau algoritma.")

# --- Tampilan Kode ---
st.markdown("--- ")
st.header("Implementasi Kode")
with open("algorithms/polygon_fill.py", "r") as f:
    show_code("Algoritma Polygon Fill", f.read())
