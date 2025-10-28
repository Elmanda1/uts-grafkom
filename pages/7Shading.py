"""
Halaman Minggu 6: Teknik Shading.

Membandingkan secara visual teknik shading Flat, Gouraud, dan Phong
pada objek 3D sederhana yang dapat diputar.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import json

from config import PAGE_CONFIG
from algorithms.shading import flat_shading, gouraud_shading
from algorithms.color_models import calculate_phong_lighting

st.set_page_config(**PAGE_CONFIG)
st.title("💡 Minggu 6: Teknik Shading")
st.markdown("--- ")

# --- Fungsi Bantuan untuk Memuat Objek ---
@st.cache_data
def load_object_data(file_path: str):
    """
    Memuat data vertex dan poligon dari file JSON.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Konversi ke numpy array untuk kemudahan kalkulasi
        vertices = [{"position": np.array(v["position"]), "normal": np.array(v["normal"])} for v in data["vertices"]]
        polygons = data["polygons"]
        return vertices, polygons
    except Exception as e:
        st.error(f"Gagal memuat data objek: {e}")
        return [], []

# --- Sidebar Kontrol ---
st.sidebar.header("Pengaturan Shading")
shading_type = st.sidebar.selectbox(
    "Pilih Teknik Shading",
    ["Flat", "Gouraud", "Phong (Simulasi)"]
)

light_color_hex = st.sidebar.color_picker("Warna Cahaya", "#FFFFFF")
light_color = tuple(int(light_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

material = {
    'ka': st.sidebar.slider("Ambient (ka)", 0.0, 1.0, 0.1, 0.05),
    'kd': st.sidebar.slider("Diffuse (kd)", 0.0, 1.0, 0.7, 0.05),
    'ks': st.sidebar.slider("Specular (ks)", 0.0, 1.0, 0.5, 0.05),
    'shininess': st.sidebar.slider("Shininess", 1, 256, 32)
}

light_pos = np.array([
    st.sidebar.slider("Light Pos X", -5.0, 5.0, 2.0, 0.1),
    st.sidebar.slider("Light Pos Y", -5.0, 5.0, 2.0, 0.1),
    st.sidebar.slider("Light Pos Z", -5.0, 5.0, 5.0, 0.1)
])

# --- Logika Utama & Visualisasi Plotly ---
st.subheader(f"Visualisasi: {shading_type} Shading")

# Memuat data objek (misal: kubus atau teapot)
vertices, polygons = load_object_data("assets/data/sample_objects.json")

if vertices and polygons:
    # Ekstrak posisi vertex untuk plotting
    x_coords = [v['position'][0] for v in vertices]
    y_coords = [v['position'][1] for v in vertices]
    z_coords = [v['position'][2] for v in vertices]

    # Argumen pencahayaan
    lighting_args = {
        'light_color': light_color,
        'light_position': light_pos,
        'camera_position': np.array([2, 2, 5]), # Posisi kamera tetap
        'material': material
    }

    # Tentukan warna berdasarkan tipe shading
    face_colors = []
    vertex_colors = None
    lighting_model = None

    if shading_type == "Flat":
        for poly in polygons:
            color = flat_shading(poly, vertices, **lighting_args)
            face_colors.append(f'rgb({color[0]},{color[1]},{color[2]})')
    
    elif shading_type == "Gouraud":
        # Hitung warna di setiap vertex unik
        unique_vertex_colors = []
        for i in range(len(vertices)):
            color = calculate_phong_lighting(
                point_position=vertices[i]['position'],
                point_normal=vertices[i]['normal'],
                **lighting_args
            )
            unique_vertex_colors.append(f'rgb({color[0]},{color[1]},{color[2]})')
        vertex_colors = unique_vertex_colors

    elif shading_type == "Phong (Simulasi)":
        # Plotly mendukung Phong shading secara native
        lighting_model = dict(
            ambient=material['ka'],
            diffuse=material['kd'],
            specular=material['ks'],
            roughness=1.0 - (material['shininess'] / 256.0), # Perkiraan
            fresnel=0.2
        )

    # Buat mesh 3D dengan Plotly
    fig = go.Figure(data=[go.Mesh3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        i=[p[0] for p in polygons],
        j=[p[1] for p in polygons],
        k=[p[2] for p in polygons],
        facecolor=face_colors if shading_type == "Flat" else None,
        vertexcolor=vertex_colors if shading_type == "Gouraud" else None,
        # Untuk Phong, kita serahkan ke Plotly
        lighting=lighting_model if shading_type == "Phong (Simulasi)" else None,
        lightposition=dict(x=light_pos[0], y=light_pos[1], z=light_pos[2]),
        name='object',
        showscale=False
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(title='X', backgroundcolor="rgb(20, 24, 30)"),
            yaxis=dict(title='Y', backgroundcolor="rgb(20, 24, 30)"),
            zaxis=dict(title='Z', backgroundcolor="rgb(20, 24, 30)"),
            camera_eye=dict(x=1.5, y=1.5, z=1.5)
        ),
        paper_bgcolor="#0E1117",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Data objek tidak ditemukan atau gagal dimuat. Pastikan `assets/data/sample_objects.json` ada dan valid.")

st.markdown("--- ")
st.header("Penjelasan Teknik Shading")
st.markdown("""
- **Flat Shading:** Model pencahayaan (misal: Phong) diterapkan **sekali untuk setiap poligon**. Seluruh poligon diwarnai dengan satu warna solid. Hasilnya terlihat `faceted` atau kotak-kotak, tapi sangat cepat untuk dihitung.

- **Gouraud Shading:** Model pencahayaan diterapkan pada **setiap vertex** dari poligon. Warna-warna di vertex ini kemudian diinterpolasi secara linear di seluruh permukaan poligon. Hasilnya lebih halus dari Flat Shading, tapi bisa kehilangan detail highlight specular di tengah poligon.

- **Phong Shading:** **Vektor normal** diinterpolasi secara linear di seluruh permukaan poligon. Model pencahayaan kemudian diterapkan pada **setiap piksel (fragmen)** menggunakan normal yang telah diinterpolasi. Ini adalah metode yang paling realistis dari ketiganya, mampu menghasilkan highlight specular yang akurat, tetapi juga yang paling intensif secara komputasi.
""")
