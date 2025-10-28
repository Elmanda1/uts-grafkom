"""
Halaman Minggu 7: Pemetaan Tekstur (Texturing).

Demo dasar mengenai konsep pemetaan tekstur (texture mapping),
termasuk visualisasi koordinat UV dan efek filtering.
"""

import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import plotly.graph_objects as go
import json

from config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)
st.title("🖼️ Minggu 7: Pemetaan Tekstur")
st.markdown("--- ")

# --- Fungsi Bantuan & State ---
@st.cache_data
def load_textured_object(file_path: str):
    """
    Memuat data objek yang sudah memiliki koordinat UV.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        vertices = np.array([v['position'] for v in data["vertices"]])
        uvs = np.array([v['uv'] for v in data["vertices"]])
        polygons = data["polygons"]
        return vertices, uvs, polygons
    except Exception as e:
        st.error(f"Gagal memuat data objek: {e}")
        return None, None, None

if 'texture_image' not in st.session_state:
    # Load default texture
    try:
        st.session_state.texture_image = Image.open("assets/images/IU.jpeg")
    except FileNotFoundError:
        st.error("File tekstur default 'assets/images/IU.jpeg' tidak ditemukan.")
        # Buat texture checkerboard sebagai fallback
        img = Image.new('RGB', (64, 64))
        pixels = img.load()
        for i in range(64):
            for j in range(64):
                if (i // 8 % 2) == (j // 8 % 2):
                    pixels[i, j] = (255, 0, 255) # Magenta
                else:
                    pixels[i, j] = (0, 0, 0) # Hitam
        st.session_state.texture_image = img

# --- Sidebar Kontrol ---
st.sidebar.header("Pengaturan Tekstur")

# Opsi upload tekstur
uploaded_file = st.sidebar.file_uploader("Unggah Tekstur Kustom (PNG/JPG)", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    st.session_state.texture_image = Image.open(uploaded_file)
    st.sidebar.success("Tekstur kustom berhasil dimuat!")

# Opsi filtering
texture_filtering = st.sidebar.selectbox(
    "Filter Tekstur",
    ["Nearest Neighbor", "Bilinear"]
)

st.sidebar.image(st.session_state.texture_image, caption="Tekstur Saat Ini", use_column_width=True)

# --- Tampilan Utama ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Visualisasi UV Mapping")
    st.info("Ini adalah bagaimana model 3D 'dibuka' ke dalam ruang 2D untuk dipetakan dengan tekstur.")
    
    vertices, uvs, polygons = load_textured_object("assets/data/sample_objects.json")

    if uvs is not None:
        # Gambar UV map di atas tekstur
        uv_map_img = st.session_state.texture_image.copy().convert("RGBA")
        draw = ImageDraw.Draw(uv_map_img)
        img_width, img_height = uv_map_img.size

        for poly in polygons:
            # Ambil koordinat UV untuk setiap vertex di poligon
            poly_uvs = [(uvs[i][0] * img_width, (1 - uvs[i][1]) * img_height) for i in poly]
            # Gambar garis yang menghubungkan UVs
            draw.line(poly_uvs + [poly_uvs[0]], fill="cyan", width=2)

        st.image(uv_map_img, caption="Peta UV pada Tekstur", use_column_width=True)

with col2:
    st.subheader("Hasil Objek 3D dengan Tekstur")
    if vertices is not None:
        # Buat mesh 3D dengan Plotly
        fig = go.Figure(data=[go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=[p[0] for p in polygons],
            j=[p[1] for p in polygons],
            k=[p[2] for p in polygons],
            # Map koordinat UV ke vertex
            vertexcolor=None, # Akan diganti oleh tekstur
            uv=uvs,
            texture=st.session_state.texture_image,
            name='object',
            showscale=False
        )])

        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(title='X', backgroundcolor="rgb(20, 24, 30)"),
                yaxis=dict(title='Y', backgroundcolor="rgb(20, 24, 30)"),
                zaxis=dict(title='Z', backgroundcolor="rgb(20, 24, 30)"),
                camera_eye=dict(x=1.8, y=1.8, z=1.8)
            ),
            paper_bgcolor="#0E1117",
            font_color="white"
        )
        # Opsi filtering di Plotly tidak secara langsung didukung via API, 
        # ini lebih ke properti WebGL. Tampilan akan default ke linear.
        st.plotly_chart(fig, use_container_width=True)

st.markdown("--- ")
st.header("Penjelasan Konsep")
st.markdown("""
- **Texture Mapping:** Proses menambahkan detail permukaan, warna, atau tekstur ke model 3D. Ini dilakukan dengan membungkus gambar 2D (tekstur) ke permukaan model.

- **Koordinat UV:** Untuk memetakan gambar 2D ke objek 3D, setiap vertex pada model 3D diberi koordinat 2D (U, V) yang sesuai dengan titik pada gambar tekstur. U adalah sumbu horizontal (0 hingga 1) dan V adalah sumbu vertikal (0 hingga 1).

- **Texture Filtering:** Saat tekstur ditampilkan di layar, satu piksel di layar mungkin tidak cocok persis dengan satu piksel di tekstur. Filtering menentukan warna piksel layar berdasarkan piksel tekstur di sekitarnya.
    - **Nearest Neighbor:** Metode paling sederhana dan cepat. Warna piksel diambil dari piksel tekstur terdekat. Hasilnya tajam dan `blocky` saat diperbesar.
    - **Bilinear Filtering:** Mengambil sampel 4 piksel tekstur terdekat dan menginterpolasi warnanya. Hasilnya lebih halus dan tidak terlalu `blocky`, tetapi bisa terlihat sedikit buram.
    - **Trilinear & Anisotropic Filtering:** Metode yang lebih canggih untuk mengatasi artefak seperti *Moiré patterns* dan meningkatkan kualitas pada permukaan yang dilihat dari sudut ekstrem.
""")
