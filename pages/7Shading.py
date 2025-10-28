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
        <h1>💡 Teknik Shading</h1>
        <p class="subtitle">Perbandingan visual teknik Flat, Gouraud, dan Phong Shading pada objek 3D</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Introduction Section --- #
intro_col1, intro_col2 = st.columns([3, 2])

with intro_col1:
    st.markdown("### 🎯 Tujuan Pembelajaran")
    st.markdown("""
    Pada minggu ini, Anda akan mempelajari tiga teknik shading fundamental 
    dalam grafika komputer untuk rendering objek 3D:
    
    - **Flat Shading** - Satu warna per poligon (tercepat)
    - **Gouraud Shading** - Interpolasi warna dari vertex (cepat & halus)
    - **Phong Shading** - Interpolasi normal per pixel (paling realistis)
    
    Setiap teknik memiliki trade-off antara kualitas visual dan performa komputasi.
    """)

with intro_col2:
    st.info("""
    ### 📌 Petunjuk Penggunaan
    
    **Langkah-langkah:**
    
    1. Pilih **teknik shading** dari sidebar
    2. Atur **parameter pencahayaan**
    3. Sesuaikan **posisi cahaya** (XYZ)
    4. Putar **objek 3D** dengan mouse
    5. Bandingkan **hasil visual**
    
    *Klik dan drag untuk merotasi objek 3D!*
    """)

st.markdown("---")

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

# --- Sidebar Kontrol --- #
st.sidebar.markdown("### ⚙️ Pengaturan Shading")
shading_type = st.sidebar.selectbox(
    "Pilih Teknik Shading",
    ["Flat", "Gouraud", "Phong (Simulasi)"],
    help="Pilih metode shading yang ingin divisualisasikan"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Pengaturan Cahaya")

light_color_hex = st.sidebar.color_picker("Warna Cahaya", "#FFFFFF")
light_color = tuple(int(light_color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

st.sidebar.markdown("**Posisi Cahaya (XYZ)**")
light_pos = np.array([
    st.sidebar.slider("📍 Light X", -5.0, 5.0, 2.0, 0.1),
    st.sidebar.slider("📍 Light Y", -5.0, 5.0, 2.0, 0.1),
    st.sidebar.slider("📍 Light Z", -5.0, 5.0, 5.0, 0.1)
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Properti Material")

material = {
    'ka': st.sidebar.slider("🌙 Ambient (ka)", 0.0, 1.0, 0.1, 0.05, 
                            help="Cahaya lingkungan dasar"),
    'kd': st.sidebar.slider("☀️ Diffuse (kd)", 0.0, 1.0, 0.7, 0.05,
                            help="Refleksi cahaya tersebar"),
    'ks': st.sidebar.slider("✨ Specular (ks)", 0.0, 1.0, 0.5, 0.05,
                            help="Pantulan mengkilap"),
    'shininess': st.sidebar.slider("💎 Shininess", 1, 256, 32,
                                   help="Tingkat kilau permukaan")
}

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Informasi")
st.sidebar.markdown(f"**Teknik:** `{shading_type}`")
st.sidebar.markdown(f"**Cahaya:** `RGB{light_color}`")
st.sidebar.markdown(f"**Posisi:** `({light_pos[0]:.1f}, {light_pos[1]:.1f}, {light_pos[2]:.1f})`")

# --- Konsep Section --- #
with st.expander("📖 **Konsep: Teknik Shading**", expanded=False):
    concept_col1, concept_col2, concept_col3 = st.columns(3)
    
    with concept_col1:
        st.markdown("""
        **🔷 Flat Shading**
        
        Teknik paling sederhana dan tercepat:
        
        - Satu warna per poligon
        - Normal dihitung per face
        - Tampilan "faceted" atau kotak-kotak
        - Sangat cepat untuk dihitung
        
        **Kompleksitas:** O(n) per poligon
        
        **Digunakan untuk:** Low-poly art, wireframe preview
        """)
    
    with concept_col2:
        st.markdown("""
        **🔶 Gouraud Shading**
        
        Interpolasi warna dari vertex:
        
        - Hitung pencahayaan di vertex
        - Interpolasi linear di permukaan
        - Lebih halus dari Flat Shading
        - Balance antara kualitas & performa
        
        **Kompleksitas:** O(n) per vertex
        
        **Digunakan untuk:** Real-time rendering, games
        """)
    
    with concept_col3:
        st.markdown("""
        **🔸 Phong Shading**
        
        Teknik paling realistis:
        
        - Interpolasi normal per pixel
        - Pencahayaan per fragment
        - Highlight specular akurat
        - Paling intensif komputasi
        
        **Kompleksitas:** O(n) per pixel
        
        **Digunakan untuk:** High-quality rendering, film
        """)

st.markdown("---")

# --- Logika Utama & Visualisasi ---
st.markdown("### 🎨 Visualisasi Objek 3D")
st.info(f"🎭 Menampilkan objek dengan **{shading_type} Shading** - Klik dan drag untuk merotasi")

# Memuat data objek (misal: kubus atau teapot)
vertices, polygons = load_object_data("assets/data/sample_objects.json")

if vertices and polygons:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📤 Hasil Rendering 3D")
        
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
            font_color="white",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
        st.success(f"✨ Rendering dengan **{shading_type}** berhasil!")
    
    with col2:
        st.markdown("#### 📊 Statistik Objek")
        
        st.metric("Total Vertices", len(vertices))
        st.metric("Total Poligon", len(polygons))
        st.metric("Total Edges", len(polygons) * 3)
        
        st.markdown("---")
        st.markdown("#### 🎮 Kontrol Interaktif")
        st.markdown("""
        **Mouse Controls:**
        - 🖱️ **Drag**: Rotasi objek
        - 🔍 **Scroll**: Zoom in/out
        - 🤏 **Right-drag**: Pan kamera
        
        **Tips:**
        - Coba rotasi untuk lihat efek shading
        - Ubah posisi cahaya untuk hasil berbeda
        """)
        
        st.markdown("---")
        st.markdown("#### ⚡ Performa")
        
        # Estimasi kompleksitas
        if shading_type == "Flat":
            complexity = len(polygons)
            complexity_text = "Rendah"
            color = "green"
        elif shading_type == "Gouraud":
            complexity = len(vertices)
            complexity_text = "Sedang"
            color = "orange"
        else:
            complexity = len(polygons) * 1000  # Estimasi pixel
            complexity_text = "Tinggi"
            color = "red"
        
        st.markdown(f"**Kompleksitas:** :{color}[{complexity_text}]")
        st.markdown(f"**Kalkulasi:** ~{complexity:,} operasi")

else:
    st.error("""
    ⚠️ **Data objek tidak ditemukan!**
    
    Pastikan file `assets/data/sample_objects.json` ada dan valid.
    File harus berisi struktur JSON dengan vertices dan polygons.
    """)

st.markdown("---")

# --- Perbandingan Detail --- #
with st.expander("⚖️ **Perbandingan Mendalam: Flat vs Gouraud vs Phong**", expanded=False):
    st.markdown("### Analisis Komparatif")
    
    comp_col1, comp_col2, comp_col3 = st.columns(3)
    
    with comp_col1:
        st.markdown("""
        **🔷 Flat Shading**
        
        **Kelebihan:**
        - ✅ Tercepat untuk dihitung
        - ✅ Sederhana & efisien memori
        - ✅ Cocok untuk low-poly art
        - ✅ Ideal untuk wireframe preview
        
        **Kekurangan:**
        - ❌ Tampilan "faceted" kasar
        - ❌ Tidak ada gradasi halus
        - ❌ Kurang realistis
        
        **Use Case:** Prototype, stylized art
        """)
    
    with comp_col2:
        st.markdown("""
        **🔶 Gouraud Shading**
        
        **Kelebihan:**
        - ✅ Lebih halus dari Flat
        - ✅ Performa masih bagus
        - ✅ Standar untuk real-time rendering
        - ✅ Balance kualitas-kecepatan
        
        **Kekurangan:**
        - ❌ Highlight specular tidak akurat
        - ❌ Mach banding effect
        - ❌ Detail hilang di tengah polygon
        
        **Use Case:** Games, real-time apps
        """)
    
    with comp_col3:
        st.markdown("""
        **🔸 Phong Shading**
        
        **Kelebihan:**
        - ✅ Paling realistis
        - ✅ Highlight specular akurat
        - ✅ Detail tinggi per pixel
        - ✅ Standar industri high-end
        
        **Kekurangan:**
        - ❌ Paling lambat
        - ❌ Intensif komputasi
        - ❌ Memerlukan hardware kuat
        
        **Use Case:** Film, high-quality rendering
        """)

st.markdown("---")

# --- Penjelasan Teknik --- #
st.markdown("### 📚 Penjelasan Teknik Shading")

technique_col1, technique_col2 = st.columns(2)

with technique_col1:
    st.markdown("""
    #### 🔍 Cara Kerja Setiap Teknik
    
    **1. Flat Shading**
    - Model pencahayaan diterapkan **sekali per poligon**
    - Menggunakan normal rata-rata dari face
    - Seluruh poligon diwarnai dengan satu warna solid
    - Hasil: Tampilan "faceted" atau kotak-kotak
    - Kecepatan: Sangat cepat ⚡⚡⚡
    
    **2. Gouraud Shading**
    - Model pencahayaan diterapkan pada **setiap vertex**
    - Warna di vertex diinterpolasi linear di permukaan
    - Menghasilkan gradasi halus antar vertex
    - Hasil: Lebih halus, tapi kehilangan detail specular
    - Kecepatan: Cepat ⚡⚡
    
    **3. Phong Shading**
    - **Vektor normal** diinterpolasi di permukaan
    - Model pencahayaan diterapkan **per pixel/fragment**
    - Menggunakan normal yang telah diinterpolasi
    - Hasil: Paling realistis dengan highlight akurat
    - Kecepatan: Lambat ⚡
    """)

with technique_col2:
    st.markdown("""
    #### 📐 Formula Matematika
    
    **Interpolasi Gouraud:**
    ```
    C = αC₁ + βC₂ + γC₃
    α + β + γ = 1 (barycentric)
    ```
    
    **Interpolasi Phong:**
    ```
    N = αN₁ + βN₂ + γN₃
    N' = normalize(N)
    C = Phong(N')
    ```
    
    **Phong Lighting Model:**
    ```
    I = Ia + Id + Is
    Ia = ka × Ilight
    Id = kd × Ilight × (N · L)
    Is = ks × Ilight × (R · V)^shininess
    ```
    
    **Dimana:**
    - C = Color, N = Normal, I = Intensity
    - L = Light direction, V = View direction
    - R = Reflection direction
    - α, β, γ = Barycentric coordinates
    """)

st.markdown("---")

# --- Implementasi Kode --- #
st.markdown("### 💻 Implementasi Kode")

with st.expander("📝 **Lihat Kode Implementasi Shading**", expanded=False):
    st.markdown("""
    Berikut adalah implementasi lengkap dari ketiga teknik shading. 
    Perhatikan perbedaan dalam cara menghitung dan mengaplikasikan warna 
    pada setiap teknik.
    """)
    
    st.markdown("---")
    
    code_col1, code_col2 = st.columns(2)
    
    with code_col1:
        st.markdown("**Flat Shading Implementation:**")
        st.code("""
def flat_shading(polygon, vertices, light_color, 
                 light_position, camera_position, material):
    '''Flat shading: satu warna per poligon'''
    # Ambil vertex dari polygon
    v1 = vertices[polygon[0]]['position']
    v2 = vertices[polygon[1]]['position']
    v3 = vertices[polygon[2]]['position']
    
    # Hitung face normal
    edge1 = v2 - v1
    edge2 = v3 - v1
    face_normal = np.cross(edge1, edge2)
    face_normal = face_normal / np.linalg.norm(face_normal)
    
    # Hitung centroid polygon
    centroid = (v1 + v2 + v3) / 3
    
    # Aplikasikan Phong lighting sekali
    color = calculate_phong_lighting(
        light_color, light_position, 
        camera_position, centroid, 
        face_normal, material
    )
    
    return color
        """, language="python")
    
    with code_col2:
        st.markdown("**Gouraud Shading Implementation:**")
        st.code("""
def gouraud_shading(polygon, vertices, light_color,
                   light_position, camera_position, material):
    '''Gouraud shading: interpolasi warna vertex'''
    # Hitung warna di setiap vertex
    vertex_colors = []
    for vertex_idx in polygon:
        v = vertices[vertex_idx]
        color = calculate_phong_lighting(
            light_color, light_position,
            camera_position, v['position'],
            v['normal'], material
        )
        vertex_colors.append(color)
    
    # Return warna vertex untuk interpolasi
    # (Interpolasi dilakukan oleh rasterizer)
    return vertex_colors
        """, language="python")
    
    # Muat kode lengkap dari file
    try:
        st.markdown("---")
        st.markdown("**Kode Lengkap dari File:**")
        with open("algorithms/shading.py", "r") as f:
            code_content = f.read()
            st.code(code_content, language="python")
    except FileNotFoundError:
        st.warning("⚠️ File `algorithms/shading.py` tidak ditemukan")

st.markdown("---")

# --- Resources Section --- #
with st.expander("📚 **Sumber Belajar Tambahan**", expanded=False):
    resource_col1, resource_col2 = st.columns(2)
    
    with resource_col1:
        st.markdown("""
        **Referensi Teoritis:**
        - Computer Graphics: Principles and Practice (Foley et al.)
        - Real-Time Rendering (Akenine-Möller et al.)
        - Gouraud Shading (1971)
        - Phong Shading (1975)
        - Interactive Computer Graphics (Angel & Shreiner)
        """)
    
    with resource_col2:
        st.markdown("""
        **Tutorial Online:**
        - LearnOpenGL: Lighting & Shading
        - Scratchapixel: Introduction to Shading
        - Wikipedia: Shading Techniques
        - Khan Academy: 3D Graphics
        - Shader Toy: Interactive Shading Demos
        """)

# --- Footer --- #
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>💡 <strong>Tips:</strong> Bandingkan ketiga teknik dengan mengubah parameter yang sama untuk melihat perbedaan kualitas visual!</p>
    <p>Minggu 6: Teknik Shading | © 2025 Grafika Komputer</p>
</div>
""", unsafe_allow_html=True)