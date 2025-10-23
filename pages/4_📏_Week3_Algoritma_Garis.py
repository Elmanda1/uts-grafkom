"""
Halaman Minggu 3: Algoritma Penggambaran Garis.

Visualisasi dan perbandingan interaktif antara algoritma garis DDA dan Bresenham.
Pengguna dapat memilih dua titik di canvas untuk menggambar garis.
"""

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw

from config import PAGE_CONFIG, CANVAS_WIDTH, CANVAS_HEIGHT
from utils.canvas_utils import setup_canvas, get_canvas_data
from utils.code_viewer import show_code, compare_algorithms, show_performance_metrics
from algorithms.line_algorithms import dda_line, bresenham_line

st.set_page_config(**PAGE_CONFIG)
st.title("📏 Minggu 3: Algoritma Penggambaran Garis")
st.markdown("--- ")
st.info("Klik dua titik pada canvas untuk menentukan awal dan akhir garis.")

# --- Sidebar Kontrol---
st.sidebar.header("Pengaturan Garis")
algo_choice = st.sidebar.selectbox(
    "Pilih Algoritma",
    ["Bresenham", "DDA", "Keduanya untuk Perbandingan"]
)

# --- Canvas --- #
col1, col2 = st.columns(2)
with col1:
    st.subheader("Canvas Input")
    canvas_result = setup_canvas(
        drawing_mode='line',
        stroke_color='cyan',
        key="line_canvas",
        width=CANVAS_WIDTH // 2,
    )

# --- Logika & Visualisasi --- #
if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
    # Ambil object terakhir yang digambar (garis)
    last_object = canvas_result.json_data["objects"][-1]
    if last_object["type"] == 'line':
        x1, y1 = int(last_object['left']), int(last_object['top'])
        x2, y2 = int(x1 + last_object['width']), int(y1 + last_object['height'])

        st.sidebar.markdown(f"**Titik A:** `({x1}, {y1})`")
        st.sidebar.markdown(f"**Titik B:** `({x2}, {y2})`")

        # Buat gambar kosong untuk visualisasi hasil
        img = Image.new("RGB", (CANVAS_WIDTH // 2, CANVAS_HEIGHT), color="black")
        draw = ImageDraw.Draw(img)

        # Menjalankan algoritma dan menampilkan hasil
        metrics_to_compare = []

        def run_and_draw(algorithm, name, color):
            """Helper untuk menjalankan algoritma, menggambar, dan menyimpan metrik."""
            result = algorithm(x1, y1, x2, y2)
            pixels = result.get("result", [])
            if pixels:
                draw.point(pixels, fill=color)
            
            metrics = {
                'name': name,
                'time': result.get('execution_time_ms', 0),
                'ops': result.get('operations', 0)
            }
            metrics_to_compare.append(metrics)
            return result, pixels

        if algo_choice == "Bresenham" or algo_choice == "Keduanya untuk Perbandingan":
            bres_result, _ = run_and_draw(bresenham_line, "Bresenham Line", "#FF4B4B") # Merah
            if algo_choice != "Keduanya untuk Perbandingan":
                with col2:
                    st.subheader("Hasil Algoritma")
                    st.image(img, caption="Garis oleh Bresenham")
                    show_performance_metrics(
                        "Bresenham Line", 
                        bres_result['execution_time_ms'], 
                        bres_result['operations']
                    )

        if algo_choice == "DDA" or algo_choice == "Keduanya untuk Perbandingan":
            dda_result, _ = run_and_draw(dda_line, "DDA", "#00C853") # Hijau
            if algo_choice != "Keduanya untuk Perbandingan":
                with col2:
                    st.subheader("Hasil Algoritma")
                    st.image(img, caption="Garis oleh DDA")
                    show_performance_metrics(
                        "DDA",
                        dda_result['execution_time_ms'],
                        dda_result['operations']
                    )
        
        if algo_choice == "Keduanya untuk Perbandingan":
            with col2:
                st.subheader("Hasil Perbandingan")
                st.image(img, caption="Merah: Bresenham, Hijau: DDA")
                compare_algorithms(metrics_to_compare)

# --- Tampilan Kode --- #
st.markdown("--- ")
st.header("Implementasi Kode")

with st.expander("Lihat Kode Algoritma Garis"):
    st.code("""
@performance_tracker
 ... (Implementasi DDA) ...
    """, language='python')
    st.code("""
@performance_tracker
 ... (Implementasi Bresenham) ...
    """, language='python')
    # Sebaiknya muat kode dari file untuk konsistensi
    with open("algorithms/line_algorithms.py", "r") as f:
        st.code(f.read(), language="python")
