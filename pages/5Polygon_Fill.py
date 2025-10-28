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
from utils.helpers import load_css
from algorithms.polygon_fill import scanline_fill, flood_fill_4, boundary_fill_4

st.set_page_config(**PAGE_CONFIG)

# Memuat CSS kustom
try:
    load_css("assets/styles/custom.css")
except Exception as e:
    st.warning(f"⚠️ CSS kustom tidak dimuat: {e}")

# --- Hero Section --- #
st.markdown("""
    <div class="header-container">
        <h1>🎨 Algoritma Pengisian Poligon</h1>
        <p class="subtitle">Teknik Mengisi Area Tertutup dengan Berbagai Metode</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Alternative Manual Input ---
with st.expander("⌨️ **Input Manual (Alternatif)**", expanded=False):
    st.markdown("""
    Jika canvas bermasalah, Anda dapat input vertices dan seed point secara manual.
    """)
    
    manual_col1, manual_col2 = st.columns(2)
    
    with manual_col1:
        st.markdown("**📐 Input Poligon Manual:**")
        
        # Predefined shapes
        shape_choice = st.selectbox(
            "Pilih bentuk predefined:",
            ["Custom", "Segitiga", "Persegi", "Pentagon", "Bintang"]
        )
        
        if shape_choice == "Segitiga":
            st.session_state.polygon_vertices = [(100, 50), (200, 200), (50, 200)]
            st.success("✅ Segitiga loaded")
        elif shape_choice == "Persegi":
            st.session_state.polygon_vertices = [(50, 50), (200, 50), (200, 200), (50, 200)]
            st.success("✅ Persegi loaded")
        elif shape_choice == "Pentagon":
            import math
            center_x, center_y, radius = 150, 150, 80
            angles = [i * 2 * math.pi / 5 - math.pi/2 for i in range(5)]
            st.session_state.polygon_vertices = [
                (int(center_x + radius * math.cos(a)), int(center_y + radius * math.sin(a)))
                for a in angles
            ]
            st.success("✅ Pentagon loaded")
        elif shape_choice == "Bintang":
            import math
            center_x, center_y = 150, 150
            outer_r, inner_r = 80, 30
            points = []
            for i in range(10):
                angle = i * math.pi / 5 - math.pi / 2
                r = outer_r if i % 2 == 0 else inner_r
                points.append((int(center_x + r * math.cos(angle)), int(center_y + r * math.sin(angle))))
            st.session_state.polygon_vertices = points
            st.success("✅ Bintang loaded")
        
        if shape_choice == "Custom":
            vertices_input = st.text_area(
                "Input vertices (format: x1,y1 x2,y2 x3,y3):",
                placeholder="100,50 200,200 50,200"
            )
            if st.button("Load Custom Vertices"):
                try:
                    pairs = vertices_input.strip().split()
                    vertices = [tuple(map(int, p.split(','))) for p in pairs]
                    if len(vertices) >= 3:
                        st.session_state.polygon_vertices = vertices
                        st.success(f"✅ {len(vertices)} vertices loaded!")
                    else:
                        st.error("Minimal 3 vertices diperlukan")
                except:
                    st.error("Format salah! Gunakan: x1,y1 x2,y2 x3,y3")
    
    with manual_col2:
        st.markdown("**📍 Input Seed Point Manual:**")
        seed_x = st.number_input("Seed X:", min_value=0, max_value=CANVAS_WIDTH, value=150)
        seed_y = st.number_input("Seed Y:", min_value=0, max_value=CANVAS_HEIGHT, value=150)
        
        if st.button("Set Seed Point"):
            st.session_state.seed_point = (int(seed_x), int(seed_y))
            st.success(f"✅ Seed: ({seed_x}, {seed_y})")

st.markdown("---")

# --- Introduction Section --- #
intro_col1, intro_col2 = st.columns([3, 2])

with intro_col1:
    st.markdown("### 🎯 Tujuan Pembelajaran")
    st.markdown("""
    Pada minggu ini, Anda akan mempelajari berbagai algoritma untuk mengisi 
    area tertutup (poligon) dengan warna tertentu:
    
    - **📐 Scanline Fill** - Algoritma berbasis scanline untuk poligon konveks dan konkaf
    - **🌊 Flood Fill** - Algoritma rekursif untuk mengisi area berdasarkan seed point
    - **🎯 Boundary Fill** - Algoritma untuk mengisi area berdasarkan warna batas
    - **⚡ Optimasi & Performa** - Memahami trade-off antara ketiga algoritma
    
    Setiap algoritma memiliki kasus penggunaan spesifik dalam grafika komputer, 
    dari rendering poligon hingga paint bucket tools.
    """)

with intro_col2:
    st.info("""
    ### 📌 Petunjuk Penggunaan
    
    **Langkah-langkah:**
    
    1. **Pilih algoritma** di sidebar
    2. **Pilih warna** isian dan batas
    3. **Gambar poligon** di canvas
    4. **Pilih seed point** (untuk flood/boundary)
    5. **Klik proses** untuk melihat hasil
    6. **Bandingkan** metrik performa
    
    *Mode polygon untuk menggambar, mode point untuk seed!*
    """)

st.markdown("---")

# --- Theory Section --- #
with st.expander("📚 **Teori: Algoritma Pengisian Poligon**", expanded=False):
    st.markdown("""
    ### Apa itu Polygon Filling?
    
    **Polygon filling** adalah proses mengisi area interior dari poligon tertutup 
    dengan warna atau pola tertentu. Ini adalah operasi fundamental dalam:
    
    - Rendering 2D graphics
    - UI/UX design (button fills, shapes)
    - Image editing (paint bucket tool)
    - Game development (terrain rendering)
    - CAD systems (area calculations)
    """)
    
    # Tabs untuk setiap algoritma
    algo_tab1, algo_tab2, algo_tab3 = st.tabs([
        "📐 Scanline Fill", "🌊 Flood Fill", "🎯 Boundary Fill"
    ])
    
    with algo_tab1:
        tab_col1, tab_col2 = st.columns([2, 1])
        
        with tab_col1:
            st.markdown("""
            ### Scanline Fill Algorithm
            
            **Konsep:**
            Mengisi poligon dengan memindai (scan) setiap horizontal line 
            dari atas ke bawah, menentukan interseksi dengan edges poligon.
            
            **Algoritma:**
            1. Buat **Edge Table (ET)** - daftar edges sorted by y_min
            2. Buat **Active Edge Table (AET)** - edges yang intersect scanline current
            3. Untuk setiap scanline (y = y_min to y_max):
               - Update AET (add edges, remove finished edges)
               - Sort AET berdasarkan x-intersection
               - Fill pixels antara pairs of intersections
               - Increment y, update x-intersections
            
            **Karakteristik:**
            - ✅ Efisien untuk poligon besar
            - ✅ Bekerja untuk poligon konkaf dan konveks
            - ✅ Tidak memerlukan seed point
            - ✅ Predictable memory usage
            - ❌ Kompleks untuk diimplementasikan
            - ❌ Sulit handle special cases (horizontal edges)
            
            **Kompleksitas:**
            - Time: O(n × m) di mana n = edges, m = scanlines
            - Space: O(n) untuk edge tables
            
            **Kasus Penggunaan:**
            - Rendering filled polygons dalam graphics API
            - Area yang sudah didefinisikan dengan vertices
            - Professional graphics software
            - Hardware rasterization
            """)
        
        with tab_col2:
            st.markdown("""
            **📊 Contoh:**
            
            Triangle vertices:
            ```
            (10, 20)
            (50, 60)
            (30, 80)
            ```
            
            **Edge Table:**
            ```
            y=20: [(10,20)→(50,60)]
            y=60: [(50,60)→(30,80)]
            y=20: [(10,20)→(30,80)]
            ```
            
            **Scanline y=40:**
            - Intersections: x=20, x=35
            - Fill pixels (20,40) to (35,40)
            """)
            
            st.success("""
            **✅ Keuntungan:**
            
            - Sangat efisien untuk polygon rendering
            - Tidak stack overflow
            - Consistent performance
            """)
    
    with algo_tab2:
        tab_col1, tab_col2 = st.columns([2, 1])
        
        with tab_col1:
            st.markdown("""
            ### Flood Fill Algorithm
            
            **Konsep:**
            Dimulai dari seed point, mengisi semua pixel yang terhubung 
            dan memiliki warna yang sama dengan target color.
            
            **Algoritma (4-connected):**
            ```
            function floodFill(x, y, fillColor, targetColor):
                if outOfBounds(x, y) or pixel(x,y) != targetColor:
                    return
                
                setPixel(x, y, fillColor)
                
                floodFill(x+1, y, fillColor, targetColor)  // Right
                floodFill(x-1, y, fillColor, targetColor)  // Left
                floodFill(x, y+1, fillColor, targetColor)  // Down
                floodFill(x, y-1, fillColor, targetColor)  // Up
            ```
            
            **Variasi:**
            - **4-connected:** Check 4 neighbors (N, S, E, W)
            - **8-connected:** Check 8 neighbors (includes diagonals)
            
            **Karakteristik:**
            - ✅ Sangat sederhana untuk dipahami
            - ✅ Bekerja untuk area irregular shape
            - ✅ Tidak perlu definisi vertices
            - ✅ Cocok untuk paint bucket tools
            - ❌ Rekursif - bisa stack overflow untuk area besar
            - ❌ Performa tidak predictable
            - ❌ Memerlukan target color matching
            
            **Optimasi:**
            - **Iterative approach:** Gunakan queue/stack eksplisit
            - **Scanline flood fill:** Kombinasi dengan scanline untuk efisiensi
            
            **Kompleksitas:**
            - Time: O(n) di mana n = pixels dalam area
            - Space: O(n) untuk recursion stack (worst case)
            
            **Kasus Penggunaan:**
            - Paint programs (bucket fill tool)
            - Game map flood (territory marking)
            - Image segmentation
            - Maze solving algorithms
            """)
        
        with tab_col2:
            st.markdown("""
            **📊 Contoh:**
            
            Seed point: (25, 25)
            Target color: Black
            Fill color: Red
            
            **Execution:**
            ```
            Start: (25, 25)
            Check: (26, 25) ✓
            Check: (24, 25) ✓
            Check: (25, 26) ✓
            Check: (25, 24) ✓
            ... continues ...
            ```
            
            **4-connected:**
            ```
               N
             W[*]E
               S
            ```
            
            **8-connected:**
            ```
             NW N NE
             W [*] E
             SW S SE
            ```
            """)
            
            st.warning("""
            **⚠️ Perhatian:**
            
            - Stack overflow untuk area sangat besar
            - Harus exact color match
            - Anti-aliased edges problematic
            """)
    
    with algo_tab3:
        tab_col1, tab_col2 = st.columns([2, 1])
        
        with tab_col1:
            st.markdown("""
            ### Boundary Fill Algorithm
            
            **Konsep:**
            Mirip dengan flood fill, tetapi berhenti ketika menemukan 
            **boundary color** tertentu, bukan mencocokkan target color.
            
            **Algoritma (4-connected):**
            ```
            function boundaryFill(x, y, fillColor, boundaryColor):
                currentColor = getPixel(x, y)
                
                if outOfBounds(x, y) or 
                   currentColor == boundaryColor or 
                   currentColor == fillColor:
                    return
                
                setPixel(x, y, fillColor)
                
                boundaryFill(x+1, y, fillColor, boundaryColor)
                boundaryFill(x-1, y, fillColor, boundaryColor)
                boundaryFill(x, y+1, fillColor, boundaryColor)
                boundaryFill(x, y-1, fillColor, boundaryColor)
            ```
            
            **Perbedaan dengan Flood Fill:**
            - **Flood Fill:** Cari pixels dengan warna **sama** seperti seed
            - **Boundary Fill:** Cari pixels yang **bukan** boundary color
            
            **Karakteristik:**
            - ✅ Bekerja dengan multi-colored interior
            - ✅ Lebih fleksibel untuk outline-based shapes
            - ✅ Tidak perlu matching target color
            - ❌ Masih rekursif (stack overflow risk)
            - ❌ Boundary harus closed dan single color
            - ❌ Gaps in boundary = leak fill
            
            **Kompleksitas:**
            - Time: O(n) di mana n = pixels dalam area
            - Space: O(n) untuk recursion stack
            
            **Kasus Penggunaan:**
            - Coloring book apps (outline-based)
            - Technical drawings dengan defined borders
            - CAD outline filling
            - Cartoon/cel shading
            """)
        
        with tab_col2:
            st.markdown("""
            **📊 Contoh:**
            
            Seed: (25, 25)
            Boundary color: Green
            Fill color: Yellow
            
            **Execution:**
            ```
            (25,25): Not green ✓ Fill
            (26,25): Not green ✓ Fill
            (27,25): GREEN ✗ Stop
            ```
            
            **Interior:**
            ```
            GGGGGGGG
            G......G  ← Fill area
            G..S...G  ← Seed here
            G......G
            GGGGGGGG
            ```
            """)
            
            st.error("""
            **⚠️ Critical:**
            
            Boundary HARUS:
            - Completely closed
            - Single color
            - No gaps/antialiasing
            
            Jika ada gap → LEAK!
            """)

st.markdown("---")

# --- Comparison Section --- #
with st.expander("⚖️ **Perbandingan Algoritma**", expanded=False):
    comp_col1, comp_col2, comp_col3 = st.columns(3)
    
    with comp_col1:
        st.markdown("""
        **📐 Scanline Fill**
        
        **Best For:**
        - Poligon dengan vertices terdefinisi
        - Rendering profesional
        - Large-scale polygons
        - Predictable performance
        
        **Avoid When:**
        - Shape tidak didefinisikan dengan vertices
        - Need interactive editing
        - Simple implementations needed
        """)
    
    with comp_col2:
        st.markdown("""
        **🌊 Flood Fill**
        
        **Best For:**
        - Paint bucket tools
        - User-interactive filling
        - Irregular/freeform shapes
        - Small to medium areas
        
        **Avoid When:**
        - Very large areas (stack overflow)
        - Need guaranteed performance
        - Anti-aliased edges present
        """)
    
    with comp_col3:
        st.markdown("""
        **🎯 Boundary Fill**
        
        **Best For:**
        - Outline-based drawings
        - Coloring book apps
        - Defined boundaries
        - Multi-colored interiors
        
        **Avoid When:**
        - Boundaries have gaps
        - Anti-aliased boundaries
        - Very large areas
        """)
    
    st.markdown("---")
    
    comparison_table = """
    | Feature | Scanline | Flood Fill | Boundary Fill |
    |---------|----------|------------|---------------|
    | **Input Required** | Vertices | Seed + Target Color | Seed + Boundary Color |
    | **Complexity** | O(n×m) | O(pixels) | O(pixels) |
    | **Stack Risk** | ❌ No | ✅ Yes | ✅ Yes |
    | **Polygon Type** | Any closed | Any shape | Any closed |
    | **Implementation** | Complex | Simple | Simple |
    | **Performance** | Consistent | Variable | Variable |
    | **Memory Usage** | Predictable | Variable | Variable |
    | **Best Use** | Rendering | Interactive | Outlines |
    """
    
    st.markdown(comparison_table)

st.markdown("---")

# --- Session State Management ---
if 'polygon_vertices' not in st.session_state:
    st.session_state.polygon_vertices = []
if 'seed_point' not in st.session_state:
    st.session_state.seed_point = None
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

# --- Sidebar Controls ---
st.sidebar.markdown("### 🎛️ Pengaturan Poligon")

algo_choice = st.sidebar.selectbox(
    "Pilih Algoritma Fill",
    ["Scanline Fill", "Flood Fill", "Boundary Fill"],
    help="Pilih metode pengisian yang ingin digunakan"
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🎨 Pengaturan Warna")

fill_color_hex = st.sidebar.color_picker("Warna Isian", "#FF4B4B", help="Warna untuk mengisi area")
fill_color_rgb = tuple(int(fill_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

boundary_color_hex = st.sidebar.color_picker("Warna Batas", "#00C853", help="Warna outline poligon")
boundary_color_rgb = tuple(int(boundary_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📊 Status Saat Ini")
st.sidebar.metric("Titik Poligon", len(st.session_state.polygon_vertices))

if st.session_state.polygon_vertices:
    st.sidebar.success("✅ Poligon tersimpan")
    with st.sidebar.expander("Lihat Vertices"):
        for i, v in enumerate(st.session_state.polygon_vertices[:5]):
            st.sidebar.code(f"V{i}: {v}")
        if len(st.session_state.polygon_vertices) > 5:
            st.sidebar.caption(f"... dan {len(st.session_state.polygon_vertices) - 5} lainnya")
else:
    st.sidebar.warning("⚠️ Belum ada poligon")

if st.session_state.seed_point:
    st.sidebar.success("✅ Seed tersimpan")
    st.sidebar.code(f"Seed: {st.session_state.seed_point}")
else:
    st.sidebar.warning("⚠️ Seed belum dipilih")

st.sidebar.markdown("---")

# Debug toggle
st.session_state.debug_mode = st.sidebar.checkbox("🐛 Debug Mode", st.session_state.debug_mode)

if st.sidebar.button("🔄 Reset Semua", use_container_width=True):
    st.session_state.polygon_vertices = []
    st.session_state.seed_point = None
    st.rerun()

st.sidebar.markdown("---")

# --- Algorithm Info in Sidebar ---
if algo_choice == "Scanline Fill":
    st.sidebar.info("""
    **📐 Scanline Fill**
    
    ✅ Tidak perlu seed point
    ✅ Efisien untuk poligon besar
    ⚠️ Butuh poligon tertutup
    """)
elif algo_choice == "Flood Fill":
    st.sidebar.info("""
    **🌊 Flood Fill**
    
    ✅ Perlu seed point
    ✅ Bekerja untuk bentuk irregular
    ⚠️ Risk stack overflow
    """)
else:
    st.sidebar.info("""
    **🎯 Boundary Fill**
    
    ✅ Perlu seed point
    ✅ Outline-based filling
    ⚠️ Boundary harus closed
    """)

# --- Main Content Area ---
st.markdown("### 🎨 Canvas Interaktif")

# Instructions based on algorithm
if algo_choice == "Scanline Fill":
    st.info("""
    📝 **Instruksi Scanline Fill:**
    1. Pilih mode **polygon** di bawah
    2. Klik untuk menambah titik poligon
    3. Klik titik pertama untuk menutup poligon
    4. Klik **Mulai Proses Pengisian**
    """)
else:
    st.info("""
    📝 **Instruksi Flood/Boundary Fill:**
    1. Pilih mode **polygon** → gambar poligon tertutup
    2. Pilih mode **point** → klik di dalam poligon untuk seed point
    3. Klik **Mulai Proses Pengisian**
    """)

# --- Canvas untuk Input --- #
canvas_col1, canvas_col2 = st.columns([2, 1])

with canvas_col1:
    st.markdown("#### 📥 Canvas Input")
    
    drawing_mode = st.radio(
        "Mode Canvas:", 
        ('polygon', 'point'), 
        horizontal=True,
        help="Polygon untuk menggambar, Point untuk seed"
    )
    
    canvas_result = setup_canvas(
        drawing_mode=drawing_mode,
        stroke_color=boundary_color_hex,
        stroke_width=3,
        key="polygon_canvas"
    )

with canvas_col2:
    st.markdown("#### 📋 Info Canvas")
    
    if drawing_mode == 'polygon':
        st.success("🖌️ Mode: Gambar Poligon")
        st.caption("Klik untuk menambah vertex")
    else:
        st.success("📍 Mode: Pilih Seed")
        st.caption("Klik di dalam poligon")
    
    st.markdown("---")
    
    st.markdown("**🎨 Warna Preview:**")
    st.color_picker("Fill", fill_color_hex, disabled=True, label_visibility="collapsed")
    st.color_picker("Boundary", boundary_color_hex, disabled=True, label_visibility="collapsed")

# --- Logika untuk memproses input canvas ---
if canvas_result.json_data and canvas_result.json_data["objects"]:
    # Debug: tampilkan semua objects
    all_objects = canvas_result.json_data["objects"]
    
    if st.session_state.debug_mode:
        st.info(f"🐛 **Debug:** Canvas memiliki {len(all_objects)} object(s)")
        with st.expander("Debug: Object Details"):
            for i, obj in enumerate(all_objects):
                st.json({
                    f"Object {i}": {
                        "type": obj.get('type', 'unknown'),
                        "keys": list(obj.keys())[:5]
                    }
                })
    
    # Cari polygon objects untuk disimpan sebagai vertices
    polygon_objects = [obj for obj in all_objects if obj.get('type') == 'polygon']
    if polygon_objects and drawing_mode == 'polygon':
        last_polygon = polygon_objects[-1]
        # Extract vertices dari path
        if 'path' in last_polygon:
            st.session_state.polygon_vertices = [(int(p[1]), int(p[2])) for p in last_polygon['path']]
            st.success(f"✅ Poligon dengan **{len(st.session_state.polygon_vertices)} titik** tersimpan!")
    
    # Cari point/circle untuk seed point
    if drawing_mode == 'point':
        last_obj = all_objects[-1]
        obj_type = last_obj.get('type', '')
        
        if obj_type == 'circle':
            # Canvas menggunakan circle untuk point
            x = int(last_obj.get('left', 0) + last_obj.get('radius', 0))
            y = int(last_obj.get('top', 0) + last_obj.get('radius', 0))
            st.session_state.seed_point = (x, y)
            st.success(f"✅ Seed point: **{st.session_state.seed_point}**")
        elif obj_type == 'path':
            # Kadang point dijadikan path
            if 'path' in last_obj and len(last_obj['path']) > 0:
                first_point = last_obj['path'][0]
                x, y = int(first_point[1]), int(first_point[2])
                st.session_state.seed_point = (x, y)
                st.success(f"✅ Seed point: **{st.session_state.seed_point}**")

# Display current state for user awareness
if st.session_state.polygon_vertices or st.session_state.seed_point:
    state_col1, state_col2 = st.columns(2)
    
    with state_col1:
        if st.session_state.polygon_vertices:
            st.info(f"📐 **Poligon aktif:** {len(st.session_state.polygon_vertices)} vertices")
        else:
            st.warning("📐 **Belum ada poligon**")
    
    with state_col2:
        if st.session_state.seed_point:
            st.info(f"📍 **Seed aktif:** {st.session_state.seed_point}")
        else:
            st.warning("📍 **Belum ada seed**")

st.markdown("---")

# --- Eksekusi Algoritma & Tampilan Hasil ---
st.markdown("### 📊 Hasil Pengisian")

process_col1, process_col2, process_col3 = st.columns([1, 1, 1])

with process_col2:
    process_button = st.button(
        "⚡ Mulai Proses Pengisian", 
        use_container_width=True, 
        type="primary"
    )

if process_button:
    # Validation
    if not st.session_state.polygon_vertices:
        st.error("❌ Gambar sebuah poligon terlebih dahulu!")
    elif algo_choice != "Scanline Fill" and not st.session_state.seed_point:
        st.error(f"❌ {algo_choice} memerlukan seed point! Gunakan mode 'point' untuk memilih.")
    else:
        with st.spinner("🔄 Memproses pengisian..."):
            # Buat canvas dasar (numpy array) untuk algoritma
            base_img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "black")
            draw = ImageDraw.Draw(base_img)
            
            # Gambar outline poligon
            if len(st.session_state.polygon_vertices) > 2:
                draw.polygon(st.session_state.polygon_vertices, outline=boundary_color_rgb, width=2)
            
            canvas_np = np.array(base_img)
            
            filled_pixels = []
            metrics = {}
            
            try:
                if algo_choice == "Scanline Fill":
                    result = scanline_fill(st.session_state.polygon_vertices, fill_color_rgb)
                    filled_pixels = result.get("result", [])
                    metrics = {
                        'name': 'Scanline Fill', 
                        'time': result['execution_time_ms'], 
                        'ops': result['operations']
                    }
                    
                elif algo_choice == "Flood Fill":
                    seed_x, seed_y = st.session_state.seed_point
                    target_color = tuple(canvas_np[seed_y, seed_x])
                    result = flood_fill_4(canvas_np.copy(), st.session_state.seed_point, fill_color_rgb, target_color)
                    filled_pixels = result.get("result", [])
                    metrics = {
                        'name': 'Flood Fill (4-connected)', 
                        'time': result['execution_time_ms'], 
                        'ops': result['operations']
                    }
                    
                elif algo_choice == "Boundary Fill":
                    result = boundary_fill_4(canvas_np.copy(), st.session_state.seed_point, fill_color_rgb, boundary_color_rgb)
                    filled_pixels = result.get("result", [])
                    metrics = {
                        'name': 'Boundary Fill (4-connected)', 
                        'time': result['execution_time_ms'], 
                        'ops': result['operations']
                    }
                
                if filled_pixels:
                    # Gambar hasil
                    result_img = base_img.copy()
                    draw_result = ImageDraw.Draw(result_img)
                    draw_result.point(filled_pixels, fill=fill_color_rgb)
                    
                    # Display results
                    result_col1, result_col2 = st.columns([2, 1])
                    
                    with result_col1:
                        st.markdown("#### 📤 Hasil Visualisasi")
                        st.image(result_img, caption=f"Hasil dari {algo_choice}", use_container_width=True)
                    
                    with result_col2:
                        st.markdown("#### 📊 Metrik Performa")
                        show_performance_metrics(metrics['name'], metrics['time'], metrics['ops'])
                        
                        st.markdown("---")
                        st.metric("Pixel Terisi", f"{len(filled_pixels):,}")
                        
                        if st.session_state.polygon_vertices:
                            poly_area = len(st.session_state.polygon_vertices)
                            st.metric("Vertices", poly_area)
                    
                    st.success(f"✅ Pengisian selesai! **{len(filled_pixels):,} pixel** telah diisi dengan {algo_choice}")
                    st.balloons()
                    
                else:
                    st.warning("⚠️ Tidak ada piksel yang diisi. Periksa:")
                    st.markdown("""
                    - Apakah seed point berada **di dalam** poligon?
                    - Apakah poligon **tertutup** dengan benar?
                    - Apakah warna target/boundary sudah sesuai?
                    """)
                    
            except Exception as e:
                st.error(f"❌ Error saat memproses: {str(e)}")
                st.info("💡 Tip: Coba dengan poligon yang lebih sederhana atau seed point yang berbeda")

st.markdown("---")

# --- Code Implementation Section ---
st.markdown("### 💻 Implementasi Kode")

with st.expander("📝 **Lihat Kode Implementasi Algoritma**", expanded=False):
    st.markdown("""
    Berikut adalah implementasi lengkap dari ketiga algoritma pengisian poligon.
    Perhatikan perbedaan pendekatan antara scanline (iteratif dengan edge table) 
    dan flood/boundary fill (rekursif dengan stack).
    """)
    
    st.markdown("---")
    
    try:
        with open("algorithms/polygon_fill.py", "r") as f:
            code_content = f.read()
            st.code(code_content, language="python")
    except FileNotFoundError:
        st.warning("⚠️ File `algorithms/polygon_fill.py` tidak ditemukan")
        st.markdown("**Contoh implementasi:**")
        st.code("""
def scanline_fill(vertices, fill_color):
    '''Scanline fill algorithm untuk poligon'''
    # Build edge table
    # Process each scanline
    # Fill between intersection pairs
    pass

def flood_fill_4(image, seed, fill_color, target_color):
    '''4-connected flood fill algorithm'''
    if outOfBounds(seed) or getPixel(seed) != target_color:
        return
    
    setPixel(seed, fill_color)
    flood_fill_4(image, (seed[0]+1, seed[1]), fill_color, target_color)
    flood_fill_4(image, (seed[0]-1, seed[1]), fill_color, target_color)
    flood_fill_4(image, (seed[0], seed[1]+1), fill_color, target_color)
    flood_fill_4(image, (seed[0], seed[1]-1), fill_color, target_color)

def boundary_fill_4(image, seed, fill_color, boundary_color):
    '''4-connected boundary fill algorithm'''
    current = getPixel(seed)
    if outOfBounds(seed) or current == boundary_color or current == fill_color:
        return
    
    setPixel(seed, fill_color)
    boundary_fill_4(image, (seed[0]+1, seed[1]), fill_color, boundary_color)
    boundary_fill_4(image, (seed[0]-1, seed[1]), fill_color, boundary_color)
    boundary_fill_4(image, (seed[0], seed[1]+1), fill_color, boundary_color)
    boundary_fill_4(image, (seed[0], seed[1]-1), fill_color, boundary_color)
        """, language='python')

st.markdown("---")

# --- Summary --- #
st.success("""
✅ **Ringkasan Minggu 4: Algoritma Pengisian Poligon**

**Konsep Utama:**
- Tiga pendekatan berbeda untuk polygon filling: Scanline, Flood Fill, Boundary Fill
- **Scanline Fill:** Efisien, berbasis vertices, predictable performance
- **Flood Fill:** Sederhana, rekursif, cocok untuk interactive tools
- **Boundary Fill:** Outline-based, flexible untuk multi-colored interiors

**Pertimbangan Praktis:**
- ✅ Pilih scanline untuk rendering profesional dan poligon besar
- ✅ Gunakan flood fill untuk paint bucket dan interactive editing
- ✅ Boundary fill untuk coloring book dan outline-based applications
- ⚠️ Rekursif algorithms risk stack overflow untuk area sangat besar

**Selanjutnya:** Minggu 5 - Model Warna & Pencahayaan →
""")

# --- Footer --- #
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>💡 <strong>Tips:</strong> Coba semua algoritma dengan poligon yang sama untuk membandingkan hasil dan performa!</p>
    <p>Minggu 4: Algoritma Pengisian Poligon | © 2025 Grafika Komputer</p>
</div>
""", unsafe_allow_html=True)