"""
Halaman Minggu 4: Polygon Fill Algorithms.

Menyediakan antarmuka interaktif untuk mempelajari dan membandingkan
algoritma pengisian polygon (Even-Odd, Winding/Non-zero, Scanline Sampling),
dengan visualisasi real-time dan mode Canvas untuk menggambar sendiri.
"""

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import plotly.graph_objects as go
from math import sqrt
import math

# -------------------------
# Page configuration
# -------------------------
PAGE_CONFIG = {
    "page_title": "Polygon Fill Algorithms",
    "page_icon": "🔷",
    "layout": "wide"
}

# Optional canvas import (streamlit-drawable-canvas)
try:
    from streamlit_drawable_canvas import st_canvas
    CANVAS_AVAILABLE = True
except ImportError:
    CANVAS_AVAILABLE = False
except Exception:
    CANVAS_AVAILABLE = False

st.set_page_config(**PAGE_CONFIG)

# -------------------------
# Optional CSS loader
# -------------------------
def load_css(path="assets/styles/custom.css"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        # ignore missing css
        pass

load_css()

# -------------------------
# Geometry helpers
# -------------------------
def is_left(p0, p1, p2):
    """Cross product to determine if p2 is left of p0->p1"""
    return (p1[0]-p0[0])*(p2[1]-p0[1]) - (p2[0]-p0[0])*(p1[1]-p0[1])

def point_in_polygon_evenodd(x, y, poly):
    """Ray casting algorithm — Even-Odd rule."""
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        # check if edge intersects horizontal ray to the right of (x,y)
        if ((y1 > y) != (y2 > y)):
            # compute intersection x coordinate
            xint = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xint:
                inside = not inside
    return inside

def point_in_polygon_winding(x, y, poly):
    """Winding number algorithm (non-zero rule)."""
    wn = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % n]
        if y1 <= y:
            if y2 > y:  # upward crossing
                if is_left((x1, y1), (x2, y2), (x, y)) > 0:
                    wn += 1
        else:
            if y2 <= y:  # downward crossing
                if is_left((x1, y1), (x2, y2), (x, y)) < 0:
                    wn -= 1
    return wn != 0

def raster_fill_samples(poly, method="Even-Odd", sample=2):
    """
    Sample points inside polygon bounding box with grid spacing = sample.
    Returns list of sample centers considered inside.
    """
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    if len(xs) == 0 or len(ys) == 0:
        return []
    minx, maxx = int(np.floor(min(xs))), int(np.ceil(max(xs)))
    miny, maxy = int(np.floor(min(ys))), int(np.ceil(max(ys)))
    pts = []
    for yy in range(miny, maxy + 1, sample):
        for xx in range(minx, maxx + 1, sample):
            cx = xx + 0.5
            cy = yy + 0.5
            if method == "Even-Odd":
                inside = point_in_polygon_evenodd(cx, cy, poly)
            elif method == "Winding (Non-zero)":
                inside = point_in_polygon_winding(cx, cy, poly)
            else:
                # default to even-odd for sampling
                inside = point_in_polygon_evenodd(cx, cy, poly)
            if inside:
                pts.append((cx, cy))
    return pts

def closed_np(poly):
    """Return numpy array with closed polygon (last == first)."""
    arr = np.array(poly)
    if arr.shape[0] == 0:
        return arr
    if not np.allclose(arr[0], arr[-1]):
        arr = np.vstack([arr, arr[0]])
    return arr

# -------------------------
# Visualization helpers
# -------------------------
def pil_fill_image(poly_points, fill_color_hex, border_color_hex, width=700, height=500):
    """Create PIL image showing filled polygon (pixel-perfect using PIL)."""
    img = Image.new("RGBA", (width, height), (15, 23, 32, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    # convert colors
    def hex_to_rgba(h, a=255):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

    fill_rgba = hex_to_rgba(fill_color_hex, 200)
    border_rgba = hex_to_rgba(border_color_hex, 255)
    # draw polygon
    try:
        draw.polygon(poly_points, fill=fill_rgba, outline=border_rgba)
    except Exception:
        # fallback: if points not in right format
        pts = [(float(x), float(y)) for x, y in poly_points]
        draw.polygon(pts, fill=fill_rgba, outline=border_rgba)
    return img

def show_fill_visualization(poly_points, algorithm, sample, fill_color, border_color, title="Hasil Fill"):
    """
    Show PIL preview (pixel fill) and a Plotly sampling comparison below.
    """
    if not poly_points or len(poly_points) < 3:
        st.warning("Polygon belum lengkap atau tidak valid untuk divisualisasikan.")
        return

    # PIL image (pixel-perfect fill)
    img = pil_fill_image(poly_points, fill_color, border_color, width=700, height=500)
    st.markdown(f"##### {title}")
    st.image(img, width=350)
    # small gap
    st.markdown("---")
    st.markdown("##### Perbandingan dengan Sampling Grid (visualisasi titik sample)")
    show_fill_plotly(poly_points, algorithm, sample, fill_color, border_color, title=f"Sampling ({algorithm})")

# -------------------------
# Canvas mode (fixed)
# -------------------------
def show_canvas_mode():
    st.markdown("#### 🖌️ Mode Canvas Drawing")
    st.info("Gambar polygon pada canvas (gunakan mode polygon/free draw), lalu tekan **'Simpan Bentuk'** untuk menyimpan dan menerapkan fill.")

    # Sidebar controls
    st.sidebar.markdown("### Kontrol Canvas")
    algo = st.sidebar.selectbox("Pilih Algoritma", ["Even-Odd", "Winding (Non-zero)", "Scanline Sampling"])
    sample = st.sidebar.slider("Sampling Resolution (px)", 1, 10, 3, help="Lebih kecil = lebih halus tapi lebih lambat")
    fill_color = st.sidebar.color_picker("Warna Fill", "#FF4B4B")
    border_color = st.sidebar.color_picker("Warna Border", "#4A9EFF")

    # ensure reset_flag exists
    if 'reset_flag' not in st.session_state:
        st.session_state.reset_flag = False

    col_left, col_right = st.columns([3, 1])
    canvas_result = None
    with col_left:
        st.markdown("##### Canvas")
        if not CANVAS_AVAILABLE:
            st.error("Module `streamlit-drawable-canvas` tidak tersedia. Install: `pip install streamlit-drawable-canvas`")
            st.info("Sebagai alternatif, gunakan mode Predefined Shapes.")
        else:
            canvas_result = st_canvas(
                stroke_width=3,
                stroke_color=border_color,
                background_color="#0f1720",
                height=500,
                width=700,
                drawing_mode="polygon",
                key=f"poly_canvas_{st.session_state.reset_flag}"
            )

    with col_right:
        st.markdown("##### Kontrol & Aksi")
        st.write(f"Algoritma: **{algo}**")
        st.write(f"Sampling: **{sample}px**")
        st.markdown("---")

        # Save shape button
        if st.button("💾 Simpan Bentuk", use_container_width=True):
            if not CANVAS_AVAILABLE:
                st.warning("Canvas tidak tersedia.")
            else:
                if canvas_result and canvas_result.json_data:
                    json_data = canvas_result.json_data
                    objects = json_data.get("objects", [])
                    found = None
                    for obj in objects:
                        obj_type = obj.get("type", "")
                        if obj_type in ("polygon", "path", "polyline", "line"):
                            pts = []
                            # prefer points
                            if "points" in obj and isinstance(obj["points"], list):
                                try:
                                    pts = [(float(p.get("x")), float(p.get("y"))) for p in obj["points"] if "x" in p and "y" in p]
                                except Exception:
                                    pts = []
                            # fallback to path (SVG-like)
                            elif "path" in obj and isinstance(obj["path"], list):
                                for cmd in obj["path"]:
                                    if isinstance(cmd, (list, tuple)) and len(cmd) >= 3:
                                        # cmd format: ["M", x, y] or ["L", x, y]
                                        try:
                                            x = float(cmd[1]); y = float(cmd[2])
                                            pts.append((x, y))
                                        except Exception:
                                            continue
                            # fallback line coords
                            elif all(k in obj for k in ("x1", "y1", "x2", "y2")):
                                try:
                                    pts = [(float(obj["x1"]), float(obj["y1"])), (float(obj["x2"]), float(obj["y2"]))]
                                except Exception:
                                    pts = []
                            if len(pts) >= 3:
                                found = pts
                                break
                    if found:
                        st.session_state.polygon_canvas = found
                        st.success("✅ Bentuk berhasil disimpan ke session state.")
                    else:
                        st.warning("⚠️ Tidak menemukan polygon yang valid pada canvas. Pastikan menggunakan mode polygon atau free draw.")
                else:
                    st.warning("⚠️ Canvas kosong atau data tidak tersedia. Coba gambar lagi dan pastikan kamu menekan 'Stop drawing' (kalau ada) sebelum menyimpan.")

        # Apply fill button
        if st.button("🎨 Terapkan Fill", use_container_width=True):
            if 'polygon_canvas' in st.session_state:
                st.session_state.last_algo = algo
                st.session_state.last_sample = sample
                st.success("🎨 Fill diterapkan — scroll ke bawah untuk melihat hasil.")
            else:
                st.warning("⚠️ Simpan bentuk terlebih dahulu sebelum menerapkan fill.")

        # Reset canvas button
        if st.button("🗑️ Reset Canvas", use_container_width=True):
            if 'polygon_canvas' in st.session_state:
                del st.session_state['polygon_canvas']
            # flip flag to force new canvas key
            st.session_state.reset_flag = not st.session_state.reset_flag
            st.rerun()

    # Visualize result if saved
    if 'polygon_canvas' in st.session_state:
        st.markdown("---")
        poly = st.session_state.polygon_canvas
        show_fill_visualization(poly, st.session_state.get('last_algo', algo), st.session_state.get('last_sample', sample), fill_color, border_color, title="Canvas: Hasil Fill")

# -------------------------
# Predefined shapes mode
# -------------------------
def show_visualization_mode():
    st.markdown("#### Mode Visualisasi dengan Bentuk Predefined")
    st.info("Pilih bentuk polygon yang sudah tersedia lalu bandingkan algoritma fill-nya.")

    st.sidebar.markdown("### Kontrol Visualisasi")
    shape_type = st.sidebar.selectbox("Pilih Bentuk", ["Persegi", "Segitiga", "Pentagon", "Bintang", "Rumah"])
    algo = st.sidebar.selectbox("Algoritma Fill", ["Even-Odd", "Winding (Non-zero)", "Scanline Sampling"])
    sample = st.sidebar.slider("Sampling (px)", 1, 8, 3)
    fill_color = st.sidebar.color_picker("Warna Fill", "#FF4B4B")
    border_color = st.sidebar.color_picker("Warna Border", "#4A9EFF")

    # Construct shapes (centered around origin)
    if shape_type == "Persegi":
        pts = [(-60, -60), (60, -60), (60, 60), (-60, 60)]
    elif shape_type == "Segitiga":
        pts = [(0, -80), (70, 40), (-70, 40)]
    elif shape_type == "Pentagon":
        angles = np.linspace(0, 2 * np.pi, 6)[:-1]
        pts = [(50 * np.cos(a), 50 * np.sin(a)) for a in angles]
    elif shape_type == "Bintang":
        angles = np.linspace(0, 2 * np.pi, 11)
        radii = [50, 20] * 5 + [50]
        pts = [(r * np.cos(a), r * np.sin(a)) for r, a in zip(radii, angles)]
    else:  # Rumah
        pts = [(-50, 0), (50, 0), (50, 40), (0, 70), (-50, 40)]

    # translate/scale for view
    tx = st.sidebar.slider("Translasi X", -150, 150, 0)
    ty = st.sidebar.slider("Translasi Y", -150, 150, 0)
    scale = st.sidebar.slider("Skala", 0.5, 2.0, 1.0, 0.1)
    pts = [(p[0] * scale + tx, p[1] * scale + ty) for p in pts]

    # compute & show
    if st.sidebar.button("Compute Fill"):
        st.session_state.viz_poly = pts
        st.session_state.viz_algo = algo
        st.session_state.viz_sample = sample
        st.session_state.viz_fill = fill_color
        st.session_state.viz_border = border_color

    if 'viz_poly' in st.session_state:
        show_fill_visualization(st.session_state.viz_poly, st.session_state.viz_algo, st.session_state.viz_sample, st.session_state.viz_fill, st.session_state.viz_border, title=f"{st.session_state.viz_algo} pada {shape_type}")
    else:
        show_fill_visualization(pts, algo, sample, fill_color, border_color, title=f"Preview: {shape_type}")

# -------------------------
# Plotly sampling visualizer + stats
# -------------------------
def show_fill_plotly(poly_points, algorithm, sample, fill_color, border_color, title="Hasil Fill"):
    """Visualize sample points + polygon boundary and show statistics."""
    if not poly_points or len(poly_points) < 3:
        st.warning("Polygon tidak valid untuk visualisasi.")
        return

    closed = closed_np(poly_points)
    filled_pts = raster_fill_samples(poly_points, method=algorithm, sample=sample)
    filled_arr = np.array(filled_pts) if len(filled_pts) > 0 else np.empty((0, 2))
    poly_arr = np.array(poly_points)

    fig = go.Figure()

    # filled samples as small squares
    if filled_arr.size > 0:
        fig.add_trace(go.Scatter(
            x=filled_arr[:, 0], y=filled_arr[:, 1],
            mode='markers',
            marker=dict(size=max(1, int(6 / max(1, sample))), symbol='square'),
            name='Filled samples',
            marker_color=fill_color,
            hoverinfo='skip'
        ))

    # polygon boundary
    fig.add_trace(go.Scatter(
        x=closed[:, 0], y=closed[:, 1],
        mode='lines+markers',
        name='Polygon boundary',
        line=dict(color=border_color, width=3),
        marker=dict(size=8),
        fill='none'
    ))

    # origin marker
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        name='Origin', marker=dict(size=12, symbol='x', color='#00C853')
    ))

    fig.update_layout(
        title=dict(text=title, x=0.5),
        plot_bgcolor='#1E2128',
        paper_bgcolor='#1E2128',
        font=dict(color='white'),
        xaxis=dict(range=[-250, 250], zeroline=True, gridcolor='#333', title='X Axis'),
        yaxis=dict(range=[-250, 250], zeroline=True, gridcolor='#333', title='Y Axis', scaleanchor='x', scaleratio=1),
        height=520,
        showlegend=True,
        legend=dict(bgcolor='rgba(30, 33, 40, 0.8)', bordercolor='#444', borderwidth=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Stats
    xs = poly_arr[:, 0]; ys = poly_arr[:, 1]
    bbox = (float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max()))
    orig_area_bb = (xs.max() - xs.min()) * (ys.max() - ys.min())
    fill_count = len(filled_pts)
    est_area = fill_count * (sample ** 2)

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    stat_col1.metric("Bounding box", f"{bbox}")
    stat_col2.metric("Filled samples", f"{fill_count}")
    stat_col3.metric("Est. area (approx)", f"{est_area:.0f} px²")
    stat_col4.metric("BB area", f"{orig_area_bb:.0f} px²")

    # show sample before/after
    sample_idx = len(poly_points) // 2
    orig_pt = poly_points[sample_idx]
    nearest = None
    if fill_count > 0:
        dists = [sqrt((fp[0] - orig_pt[0]) ** 2 + (fp[1] - orig_pt[1]) ** 2) for fp in filled_pts]
        nearest = filled_pts[int(np.argmin(dists))]
    st.markdown("---")
    st.markdown("**Sample point**")
    st.code(f"Before: {orig_pt}")
    st.code(f"Algorithm: {algorithm}")
    if nearest is not None:
        st.code(f"Nearest filled sample: ({nearest[0]:.1f}, {nearest[1]:.1f})")
    else:
        st.code("No filled sample found (maybe polygon small or sampling coarse).")

# -------------------------
# Page main
# -------------------------
def show_polygon_fill_page():
    st.markdown("""
        <div class="header-container">
            <h1>Polygon Fill Algorithms</h1>
            <p class="subtitle">Even-Odd • Winding (Non-zero) • Scanline Sampling — Visualisasi Interaktif</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Intro
    intro_col1, intro_col2 = st.columns([3, 2])
    with intro_col1:
        st.markdown("### Tujuan Pembelajaran")
        st.markdown("""
        Pada halaman ini Anda akan:
        - Memahami perbedaan aturan **Even-Odd** dan **Winding (Non-zero)**.
        - Melihat bagaimana **scanline sampling** dapat digunakan sebagai pendekatan raster sederhana.
        - Mencoba menggambar polygon sendiri atau memilih bentuk predefined.
        - Membandingkan hasil fill secara visual dan statistik.
        """)
    with intro_col2:
        st.info("""
        **Petunjuk Penggunaan**
        1. Pilih mode (Canvas/Visualization)
        2. Pilih algoritma fill di sidebar
        3. Sesuaikan sampling dan warna
        4. Simpan bentuk (jika di Canvas) lalu terapkan fill
        """)

    st.markdown("---")

    # theory
    with st.expander("**Teori: Even-Odd vs Winding & Scanline Sampling**", expanded=False):
        theory_col1, theory_col2 = st.columns([2, 1])
        with theory_col1:
            st.markdown("""
            **Even-Odd (Ray casting)**  
            Menghitung berapa kali sinar ke kanan dari titik memotong sisi polygon.  
            - Jika jumlah potongan ganjil → inside  
            - Jika genap → outside

            **Winding (Non-zero)**  
            Menghitung jumlah crossing dengan memperhatikan arah (up/down).  
            - Jika winding number ≠ 0 → inside
            """)
        with theory_col2:
            st.markdown("""
            **Scanline Sampling**  
            Pendekatan raster sederhana: sampling grid di dalam bounding-box dan uji point-in-polygon untuk tiap sampel.

            **Catatan:** Untuk produksi/gambar final gunakan scanline span filling atau algoritma rasterisasi pixel-perfect.
            """)
    st.markdown("---")

    # Demo selection
    demo_col1, demo_col2 = st.columns([3, 1])
    with demo_col1:
        st.markdown("### Demo Interaktif")
        st.markdown("""
        Pilih mode demo untuk memulai eksplorasi transformasi geometri:
        - **Canvas Drawing**: Gambar bentuk bebas dan terapkan fill
        - **Predefined Shapes**: Visualisasi transformasi pada bentuk geometris standar
        """)
    with demo_col2:
        demo_mode = st.selectbox("Mode Demo", ["Predefined Shapes", "Canvas Drawing"], label_visibility="collapsed")

    st.markdown("---")

    if demo_mode == "Canvas Drawing":
        show_canvas_mode()
    else:
        show_visualization_mode()

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>💡 <strong>Tips:</strong> Coba kombinasi sampling yang berbeda untuk melihat trade-off akurasi vs performa.</p>
        <p>Polygon Fill Algorithms | © 2025 Grafika Komputer</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Entry
# -------------------------
if __name__ == "__main__":
    show_polygon_fill_page()
