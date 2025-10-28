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
        <h1>Algoritma Penggambaran Garis</h1>
        <p class="subtitle">Visualisasi dan perbandingan algoritma DDA vs Bresenham</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Introduction Section --- #
intro_col1, intro_col2 = st.columns([3, 2])

with intro_col1:
    st.markdown("### Tujuan Pembelajaran")
    st.markdown("""
    Pada minggu ini, Anda akan mempelajari dua algoritma fundamental untuk 
    menggambar garis pada layar raster:
    
    - **Algoritma DDA (Digital Differential Analyzer)** - Pendekatan berbasis increment
    - **Algoritma Bresenham** - Pendekatan berbasis decision parameter
    
    Kedua algoritma ini mengkonversi representasi matematis garis (persamaan linear) 
    menjadi kumpulan pixel diskrit pada layar.
    """)

with intro_col2:
    st.info("""
    ### Petunjuk Penggunaan
    
    **Langkah-langkah:**
    
    1. Pilih **algoritma** dari sidebar
    2. **Klik dua titik** di canvas
    3. Amati **hasil visualisasi**
    4. Bandingkan **performa** algoritma
    5. Pelajari **kode implementasi**
    
    *Gunakan mode perbandingan untuk melihat perbedaan!*
    """)

st.markdown("---")

# --- Sidebar Kontrol--- #
st.sidebar.markdown("### Pengaturan Garis")
algo_choice = st.sidebar.selectbox(
    "Pilih Algoritma",
    ["Bresenham", "DDA", "Keduanya untuk Perbandingan"],
    help="Pilih algoritma yang ingin Anda visualisasikan"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Informasi Koordinat")

# --- Konsep Section --- #
with st.expander("**Konsep: Algoritma Garis**", expanded=False):
    concept_col1, concept_col2 = st.columns(2)
    
    with concept_col1:
        st.markdown("""
        **Algoritma DDA**
        
        Digital Differential Analyzer menggunakan pendekatan increment untuk 
        menggambar garis. Prinsip kerjanya:
        
        - Menghitung increment (Δx dan Δy)
        - Menggunakan operasi floating-point
        - Pembulatan untuk setiap pixel
        - Lebih intuitif namun kurang efisien
        
        **Kompleksitas:** O(max(|Δx|, |Δy|))
        """)
    
    with concept_col2:
        st.markdown("""
        **Algoritma Bresenham**
        
        Bresenham menggunakan decision parameter berbasis integer untuk 
        menentukan pixel mana yang harus dinyalakan:
        
        - Hanya menggunakan operasi integer
        - Tidak ada pembulatan floating-point
        - Lebih cepat dan akurat
        - Standar industri untuk rasterisasi garis
        
        **Kompleksitas:** O(max(|Δx|, |Δy|))
        """)

st.markdown("---")

# --- Canvas Section --- #
st.markdown("### Canvas Interaktif")
st.info("Klik **dua titik** pada canvas di bawah ini untuk menggambar garis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Canvas Input")
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
        
        # Hitung panjang garis
        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        st.sidebar.markdown(f"**Panjang Garis:** `{length:.2f} px`")

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
            bres_result, bres_pixels = run_and_draw(bresenham_line, "Bresenham", "#FF4B4B")
            if algo_choice != "Keduanya untuk Perbandingan":
                with col2:
                    st.markdown("#### Hasil Algoritma Bresenham")
                    st.image(img, caption="Garis menggunakan Algoritma Bresenham")

                    st.markdown("##### Metrik Performa")
                    show_performance_metrics(
                        "Bresenham Line", 
                        bres_result['execution_time_ms'], 
                        bres_result['operations']
                    )
                    
                    st.success(f"**{len(bres_pixels)} pixel** telah digambar")

        if algo_choice == "DDA" or algo_choice == "Keduanya untuk Perbandingan":
            dda_result, dda_pixels = run_and_draw(dda_line, "DDA", "#00C853")
            if algo_choice != "Keduanya untuk Perbandingan":
                with col2:
                    st.markdown("#### Hasil Algoritma DDA")
                    st.image(img, caption="Garis menggunakan Algoritma DDA")

                    st.markdown("##### Metrik Performa")
                    show_performance_metrics(
                        "DDA",
                        dda_result['execution_time_ms'],
                        dda_result['operations']
                    )
                    
                    st.success(f"**{len(dda_pixels)} pixel** telah digambar")
        
        if algo_choice == "Keduanya untuk Perbandingan":
            with col2:
                st.markdown("#### Hasil Perbandingan")
                st.image(img, caption="🔴 Merah: Bresenham | 🟢 Hijau: DDA")
                
                st.markdown("##### Perbandingan Metrik")
                compare_algorithms(metrics_to_compare)
                
                # Analisis tambahan
                st.markdown("##### Analisis")
                
                analysis_col1, analysis_col2 = st.columns(2)
                with analysis_col1:
                    time_diff = abs(bres_result['execution_time_ms'] - dda_result['execution_time_ms'])
                    faster = "Bresenham" if bres_result['execution_time_ms'] < dda_result['execution_time_ms'] else "DDA"
                    st.metric("Selisih Waktu", f"{time_diff:.4f} ms", f"{faster} lebih cepat")
                
                with analysis_col2:
                    ops_diff = abs(bres_result['operations'] - dda_result['operations'])
                    efficient = "Bresenham" if bres_result['operations'] < dda_result['operations'] else "DDA"
                    st.metric("Selisih Operasi", f"{ops_diff}", f"{efficient} lebih efisien")

else:
    with col2:
        st.markdown("#### Hasil Visualisasi")
        st.info("Silakan gambar garis di canvas sebelah kiri untuk melihat hasil visualisasi")

st.markdown("---")

# --- Perbandingan Detail --- #
with st.expander("**Perbandingan Mendalam: DDA vs Bresenham**", expanded=False):
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown("""
        **Kelebihan DDA:**
        - ✅ Lebih mudah dipahami dan diimplementasikan
        - ✅ Cocok untuk tujuan pembelajaran
        - ✅ Logika yang straightforward
        
        **Kekurangan DDA:**
        - ❌ Menggunakan floating-point (lebih lambat)
        - ❌ Memerlukan pembulatan (rounding error)
        - ❌ Kurang efisien untuk hardware
        """)
    
    with comp_col2:
        st.markdown("""
        **Kelebihan Bresenham:**
        - ✅ Hanya menggunakan operasi integer
        - ✅ Lebih cepat dan efisien
        - ✅ Tidak ada rounding error
        - ✅ Standar industri grafika
        
        **Kekurangan Bresenham:**
        - ❌ Lebih kompleks untuk dipelajari
        - ❌ Implementasi lebih rumit
        """)

st.markdown("---")

# --- Implementasi Kode --- #
st.markdown("### Implementasi Kode")

with st.expander("**Lihat Kode Implementasi Algoritma**", expanded=False):
    st.markdown("""
    Berikut adalah implementasi lengkap dari kedua algoritma garis. 
    Perhatikan perbedaan penggunaan operasi floating-point di DDA 
    vs operasi integer di Bresenham.
    """)
    
    st.markdown("---")
    
    # Muat kode dari file untuk konsistensi
    try:
        with open("algorithms/line_algorithms.py", "r") as f:
            code_content = f.read()
            st.code(code_content, language="python")
    except FileNotFoundError:
        st.warning("⚠️ File `algorithms/line_algorithms.py` tidak ditemukan")
        st.markdown("**Contoh implementasi:**")
        st.code("""
@performance_tracker
def dda_line(x1, y1, x2, y2):
    '''Algoritma DDA untuk menggambar garis'''
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    
    x_increment = dx / steps
    y_increment = dy / steps
    
    pixels = []
    x, y = x1, y1
    
    for _ in range(steps + 1):
        pixels.append((round(x), round(y)))
        x += x_increment
        y += y_increment
    
    return pixels

@performance_tracker
def bresenham_line(x1, y1, x2, y2):
    '''Algoritma Bresenham untuk menggambar garis'''
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    pixels = []
    x, y = x1, y1
    
    while True:
        pixels.append((x, y))
        if x == x2 and y == y2:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    
    return pixels
        """, language='python')

st.markdown("---")

# --- Resources Section --- #
with st.expander("**Sumber Belajar Tambahan**", expanded=False):
    resource_col1, resource_col2 = st.columns(2)
    
    with resource_col1:
        st.markdown("""
        **Referensi Teoritis:**
        - Computer Graphics: Principles and Practice (Foley et al.)
        - Bresenham's Line Algorithm (1965 paper)
        - Digital Differential Analyzer techniques
        """)
    
    with resource_col2:
        st.markdown("""
        **Tutorial Online:**
        - Wikipedia: Line Drawing Algorithms
        - GeeksforGeeks: Bresenham's Line Algorithm
        - Khan Academy: Rasterization
        """)

# --- Footer --- #
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>💡 <strong>Tips:</strong> Coba gambar garis dengan berbagai kemiringan untuk melihat perbedaan kedua algoritma!</p>
    <p>Minggu 3: Algoritma Penggambaran Garis | © 2025 Grafika Komputer</p>
</div>
""", unsafe_allow_html=True)