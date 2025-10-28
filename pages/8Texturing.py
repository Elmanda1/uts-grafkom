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
from utils.helpers import load_css

st.set_page_config(**PAGE_CONFIG)

# Memuat CSS kustom
try:
    load_css("assets/styles/custom.css")
except Exception as e:
    st.warning(f" CSS kustom tidak dimuat: {e}")

# --- Hero Section --- #
st.markdown("""
    <div class="header-container">
        <h1>Pemetaan Tekstur</h1>
        <p class="subtitle">Eksplorasi texture mapping, koordinat UV, dan filtering untuk detail permukaan 3D</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Introduction Section --- #
intro_col1, intro_col2 = st.columns([3, 2])

with intro_col1:
    st.markdown("###  Tujuan Pembelajaran")
    st.markdown("""
    Pada minggu ini, Anda akan mempelajari konsep fundamental tentang 
    texture mapping dalam grafika komputer 3D:
    
    - **Texture Mapping** - Menambahkan detail visual ke permukaan 3D
    - **Koordinat UV** - Sistem koordinat 2D untuk pemetaan tekstur
    - **Texture Filtering** - Metode sampling untuk kualitas rendering
    - **UV Unwrapping** - Proses membuka model 3D ke bidang 2D
    
    Texture mapping adalah teknik penting untuk membuat objek 3D terlihat realistis 
    tanpa menambah kompleksitas geometri.
    """)

with intro_col2:
    st.info("""
    ###  Petunjuk Penggunaan
    
    **Langkah-langkah:**
    
    1. Lihat **tekstur default** atau upload custom
    2. Pilih **metode filtering** tekstur
    3. Amati **UV mapping** pada tekstur
    4. Lihat **hasil 3D** dengan tekstur
    5. Putar objek untuk lihat **detail tekstur**
    
    *Upload gambar sendiri untuk tekstur custom!*
    """)

st.markdown("---")

# --- Fungsi Bantuan & State ---
@st.cache_data
def load_textured_object(file_path: str):
    """
    Memuat data objek yang sudah memiliki koordinat UV.
    Menangani JSON dengan komentar (// ...).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Baca file dan hapus komentar
            content = f.read()
            # Hapus komentar // (single line)
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                # Cari posisi //
                comment_pos = line.find('//')
                if comment_pos != -1:
                    # Ambil bagian sebelum komentar
                    line = line[:comment_pos]
                cleaned_lines.append(line)
            cleaned_content = '\n'.join(cleaned_lines)
            
            # Parse JSON
            data = json.loads(cleaned_content)
        
        vertices = np.array([v['position'] for v in data["vertices"]])
        uvs = np.array([v['uv'] for v in data["vertices"]])
        polygons = data["polygons"]
        return vertices, uvs, polygons
    except FileNotFoundError:
        st.error(f"❌ File tidak ditemukan: {file_path}")
        return None, None, None
    except json.JSONDecodeError as e:
        st.error(f"❌ Error parsing JSON: {e}")
        st.error(f"Pastikan file JSON valid (tanpa komentar atau gunakan format yang benar)")
        return None, None, None
    except Exception as e:
        st.error(f"❌ Gagal memuat data objek: {e}")
        return None, None, None

def create_checkerboard_texture(size=64, checker_size=8):
    """Membuat tekstur checkerboard sebagai fallback"""
    img = Image.new('RGB', (size, size))
    pixels = img.load()
    for i in range(size):
        for j in range(size):
            if (i // checker_size % 2) == (j // checker_size % 2):
                pixels[i, j] = (255, 0, 255)  # Magenta
            else:
                pixels[i, j] = (0, 0, 0)  # Hitam
    return img

def create_default_cube():
    """Membuat data cube default jika file tidak ditemukan"""
    vertices = np.array([
        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5],
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
        [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5],
        [0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5],
        [-0.5, -0.5, 0.5], [-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5]
    ])
    
    uvs = np.array([
        [0, 0], [1, 0], [1, 1], [0, 1],
        [1, 0], [0, 0], [0, 1], [1, 1],
        [0, 1], [1, 1], [1, 0], [0, 0],
        [0, 0], [1, 0], [1, 1], [0, 1],
        [0, 0], [1, 0], [1, 1], [0, 1],
        [1, 0], [0, 0], [0, 1], [1, 1]
    ])
    
    polygons = [
        [0, 1, 2], [0, 2, 3],
        [4, 5, 6], [4, 6, 7],
        [8, 9, 10], [8, 10, 11],
        [12, 13, 14], [12, 14, 15],
        [16, 17, 18], [16, 18, 19],
        [20, 21, 22], [20, 22, 23]
    ]
    
    return vertices, uvs, polygons

# Initialize texture state
if 'texture_image' not in st.session_state:
    # Load default texture
    try:
        st.session_state.texture_image = Image.open("assets/images/IU.jpeg")
        st.session_state.texture_source = "Default (IU.jpeg)"
    except FileNotFoundError:
        st.warning("⚠️ File tekstur default tidak ditemukan. Menggunakan checkerboard.")
        st.session_state.texture_image = create_checkerboard_texture()
        st.session_state.texture_source = "Checkerboard (Fallback)"

# --- Sidebar Kontrol --- #
st.sidebar.markdown("###  Pengaturan Tekstur")

# Opsi upload tekstur
uploaded_file = st.sidebar.file_uploader(
    " Unggah Tekstur Kustom", 
    type=["png", "jpg", "jpeg"],
    help="Upload gambar PNG/JPG untuk digunakan sebagai tekstur"
)
if uploaded_file is not None:
    st.session_state.texture_image = Image.open(uploaded_file)
    st.session_state.texture_source = f"Custom ({uploaded_file.name})"
    st.sidebar.success(" Tekstur kustom berhasil dimuat!")

# Reset to default
if st.sidebar.button(" Reset ke Default"):
    try:
        st.session_state.texture_image = Image.open("assets/images/IU.jpeg")
        st.session_state.texture_source = "Default (IU.jpeg)"
    except FileNotFoundError:
        st.session_state.texture_image = create_checkerboard_texture()
        st.session_state.texture_source = "Checkerboard (Fallback)"
    st.sidebar.success(" Tekstur direset!")

st.sidebar.markdown("---")
st.sidebar.markdown("###  Filter Tekstur")

# Opsi filtering
texture_filtering = st.sidebar.selectbox(
    "Metode Filtering",
    ["Nearest Neighbor", "Bilinear", "Trilinear (Simulasi)"],
    help="Pilih metode filtering untuk sampling tekstur"
)

# Texture info
st.sidebar.markdown("---")
st.sidebar.markdown("###  Informasi Tekstur")
texture_width, texture_height = st.session_state.texture_image.size
st.sidebar.markdown(f"**Sumber:** `{st.session_state.texture_source}`")
st.sidebar.markdown(f"**Resolusi:** `{texture_width} × {texture_height}px`")
st.sidebar.markdown(f"**Format:** `{st.session_state.texture_image.mode}`")
st.sidebar.markdown(f"**Filter:** `{texture_filtering}`")

# Preview tekstur
st.sidebar.markdown("---")
st.sidebar.markdown("###  Preview Tekstur")
st.sidebar.image(st.session_state.texture_image, caption="Tekstur Saat Ini", use_column_width=True)

# --- Konsep Section --- #
with st.expander("**Konsep: Texture Mapping**", expanded=False):
    concept_col1, concept_col2, concept_col3 = st.columns(3)
    
    with concept_col1:
        st.markdown("""
        ** Texture Mapping**
        
        Proses menambahkan detail ke permukaan 3D:
        
        - Membungkus gambar 2D ke objek 3D
        - Menambah detail tanpa geometri kompleks
        - Efisien untuk rendering real-time
        - Dapat berupa warna, normal, displacement
        
        **Jenis Texture:**
        - Diffuse (albedo/color)
        - Normal map
        - Specular map
        - Displacement map
        
        **Kegunaan:** Membuat permukaan realistis
        """)
    
    with concept_col2:
        st.markdown("""
        ** Koordinat UV**
        
        Sistem koordinat 2D untuk pemetaan:
        
        - **U:** Sumbu horizontal (0-1)
        - **V:** Sumbu vertikal (0-1)
        - Setiap vertex punya koordinat UV
        - Mapping 3D → 2D space
        
        **UV Unwrapping:**
        - Proses membuka model 3D
        - Seperti membuka kardus
        - Minimalisir distorsi
        - Optimasi penggunaan space
        
        **Kegunaan:** Kontrol tepat pemetaan
        """)
    
    with concept_col3:
        st.markdown("""
        ** Texture Filtering**
        
        Metode sampling tekstur:
        
        **Nearest Neighbor:**
        - Paling cepat
        - Hasil blocky/pixelated
        - Bagus untuk pixel art
        
        **Bilinear:**
        - Interpolasi 2×2 pixels
        - Lebih halus
        - Sedikit blur
        
        **Trilinear:**
        - Menggunakan mipmaps
        - Anti-aliasing lebih baik
        
        **Kegunaan:** Balance kualitas-performa
        """)

st.markdown("---")

# --- Main Content --- #
st.markdown("###  Visualisasi Texture Mapping")
st.info(" Lihat bagaimana tekstur 2D dipetakan ke objek 3D menggunakan koordinat UV")

# Load object data
vertices, uvs, polygons = load_textured_object("assets/data/sample_objects.json")

# Fallback ke default cube jika gagal load
if vertices is None or uvs is None or polygons is None:
    st.warning(" File tidak ditemukan. Menggunakan cube default.")
    vertices, uvs, polygons = create_default_cube()

if uvs is not None and vertices is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("####  UV Mapping pada Tekstur")
        st.markdown("Garis cyan menunjukkan bagaimana poligon 3D 'dibuka' pada tekstur 2D")
        
        # Gambar UV map di atas tekstur
        uv_map_img = st.session_state.texture_image.copy().convert("RGBA")
        draw = ImageDraw.Draw(uv_map_img)
        img_width, img_height = uv_map_img.size

        # Draw UV wireframe
        for poly in polygons:
            # Ambil koordinat UV untuk setiap vertex di poligon
            poly_uvs = [
                (uvs[i][0] * img_width, (1 - uvs[i][1]) * img_height) 
                for i in poly
            ]
            # Gambar garis yang menghubungkan UVs
            draw.line(poly_uvs + [poly_uvs[0]], fill="cyan", width=2)
            
            # Draw vertex points
            for uv in poly_uvs:
                draw.ellipse(
                    [uv[0]-3, uv[1]-3, uv[0]+3, uv[1]+3],
                    fill="yellow",
                    outline="cyan"
                )

        st.image(uv_map_img, caption="UV Wireframe pada Tekstur", use_column_width=True)
        
        st.markdown("---")
        st.markdown("** Informasi UV:**")
        st.markdown(f"- **Jumlah Vertices:** `{len(uvs)}`")
        st.markdown(f"- **Jumlah Polygons:** `{len(polygons)}`")
        st.markdown(f"- **UV Range:** U ∈ [0,1], V ∈ [0,1]")
        
        # UV statistics
        u_coords = uvs[:, 0]
        v_coords = uvs[:, 1]
        st.markdown(f"- **U min/max:** `{u_coords.min():.3f}` / `{u_coords.max():.3f}`")
        st.markdown(f"- **V min/max:** `{v_coords.min():.3f}` / `{v_coords.max():.3f}`")

    with col2:
        st.markdown("####  Hasil Objek 3D dengan Tekstur")
        st.markdown(f"Rendering dengan **{texture_filtering}** filtering")
        
        # Buat mesh 3D dengan Plotly
        fig = go.Figure(data=[go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=[p[0] for p in polygons],
            j=[p[1] for p in polygons],
            k=[p[2] for p in polygons],
            # Plotly tidak support langsung texture mapping dengan UV
            # Ini adalah limitasi dari Plotly, biasanya butuh WebGL custom
            facecolor=['rgb(200,200,200)'] * len(polygons),  # Placeholder
            name='Textured Object',
            showscale=False,
            lighting=dict(
                ambient=0.5,
                diffuse=0.8,
                specular=0.3,
                roughness=0.5
            )
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
            font_color="white",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        ℹ**Catatan:** Plotly memiliki keterbatasan dalam texture mapping. 
        Untuk hasil yang lebih akurat, gunakan WebGL atau game engine seperti Unity/Unreal.
        """)
        
        st.markdown("---")
        st.markdown("** Kontrol:**")
        st.markdown("-  **Drag:** Rotasi objek")
        st.markdown("-  **Scroll:** Zoom in/out")
        st.markdown("-  **Right-drag:** Pan view")

else:
    st.error("""
     **Data objek tidak ditemukan!**
    
    Pastikan file `assets/data/sample_objects.json` ada dan berisi:
    - Vertices dengan posisi 3D
    - Koordinat UV untuk setiap vertex
    - Definisi polygons
    """)

st.markdown("---")

# --- Perbandingan Filtering --- #
with st.expander(" **Perbandingan Metode Filtering**", expanded=False):
    st.markdown("### Karakteristik Setiap Metode Filtering")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        st.markdown("""
        ** Nearest Neighbor**
        
        **Cara Kerja:**
        - Ambil 1 pixel terdekat
        - Tidak ada interpolasi
        - Paling sederhana
        
        **Kelebihan:**
        -  Sangat cepat
        -  Tajam dan crisp
        -  Cocok untuk pixel art
        -  Minimal overhead
        
        **Kekurangan:**
        -  Blocky saat zoom in
        -  Pixelated appearance
        -  Aliasing artifacts
        
        **Use Case:**
        - Retro/pixel art games
        - UI elements
        - Text rendering
        """)
    
    with filter_col2:
        st.markdown("""
        ** Bilinear Filtering**
        
        **Cara Kerja:**
        - Sample 4 pixel terdekat
        - Interpolasi linear 2D
        - Weighted average
        
        **Kelebihan:**
        -  Lebih halus
        -  Mengurangi pixelation
        -  Balance speed-quality
        -  Widely supported
        
        **Kekurangan:**
        -  Sedikit blur
        -  Moiré patterns
        -  Aliasing pada jarak jauh
        
        **Use Case:**
        - Most 3D games
        - Real-time rendering
        - General purpose
        """)
    
    with filter_col3:
        st.markdown("""
        ** Trilinear Filtering**
        
        **Cara Kerja:**
        - Menggunakan mipmaps
        - Interpolasi antar mipmap levels
        - Bilinear pada 2 levels
        
        **Kelebihan:**
        -  Kualitas terbaik
        -  Mengurangi aliasing
        -  Better at distance
        -  Smooth LOD transition
        
        **Kekurangan:**
        -  Lebih lambat
        -  Memerlukan memory (mipmaps)
        -  Masih ada blur
        
        **Use Case:**
        - High-quality rendering
        - AAA games
        - Distant surfaces
        """)
    
    st.markdown("---")
    st.markdown("### Perbandingan Visual")
    
    comparison_col1, comparison_col2 = st.columns(2)
    
    with comparison_col1:
        st.markdown("""
        ** Performa (Relatif):**
        
        | Method | Speed | Memory | Quality |
        |--------|-------|--------|---------|
        | Nearest | High | Low | Fair |
        | Bilinear | Medium | Low | Good |
        | Trilinear | Low | High | Very Good |
        | Anisotropic | Low | High | Excellent |
        """)
    
    with comparison_col2:
        st.markdown("""
        ** Rekomendasi Penggunaan:**
        
        - **Mobile/Low-end:** Nearest or Bilinear
        - **Desktop/Console:** Bilinear or Trilinear
        - **High-end PC:** Trilinear or Anisotropic
        - **Pixel Art:** Always Nearest
        - **UI/Text:** Nearest or special filters
        - **Distant Terrain:** Trilinear mandatory
        """)

st.markdown("---")

# --- Penjelasan Konsep Detail --- #
st.markdown("###  Penjelasan Konsep Detail")

concept_detail_col1, concept_detail_col2 = st.columns(2)

with concept_detail_col1:
    st.markdown("""
    ####  Texture Mapping
    
    **Definisi:**
    Proses menambahkan detail permukaan, warna, atau tekstur ke model 3D dengan 
    membungkus gambar 2D (tekstur) ke permukaan model.
    
    **Mengapa Penting?**
    - Menambah detail visual tanpa geometri kompleks
    - Efisien untuk memory dan performa
    - Memungkinkan variasi tinggi dengan poly count rendah
    - Essential untuk rendering realistis
    
    **Jenis-jenis Texture Maps:**
    
    1. **Diffuse/Albedo Map:** Warna dasar permukaan
    2. **Normal Map:** Simulasi detail permukaan (bumps)
    3. **Specular Map:** Kontrol refleksi mengkilap
    4. **Roughness Map:** Tingkat kekasaran permukaan
    5. **Ambient Occlusion:** Shadow detail halus
    6. **Displacement Map:** Actual geometry modification
    7. **Emissive Map:** Area yang memancarkan cahaya
    
    **Pipeline:**
    ```
    3D Model → UV Unwrap → Texture Paint → 
    Apply Texture → Rendering
    ```
    """)

with concept_detail_col2:
    st.markdown("""
    ####  Koordinat UV
    
    **Definisi:**
    Sistem koordinat 2D (U, V) yang digunakan untuk memetakan tekstur ke permukaan 3D.
    Setiap vertex pada model 3D diberi koordinat UV (0-1 range) yang menunjuk ke 
    posisi pada tekstur.
    
    **Konvensi:**
    - **U:** Sumbu horizontal (kiri ke kanan, 0 → 1)
    - **V:** Sumbu vertikal (bawah ke atas, 0 → 1)
    - Origin (0,0) biasanya di kiri bawah
    - (1,1) di kanan atas
    
    **UV Unwrapping:**
    Proses membuka model 3D ke dalam bidang 2D, seperti membuka kardus:
    
    1. **Seam Marking:** Tentukan di mana "memotong" model
    2. **Unwrapping:** Buka model ke 2D plane
    3. **Optimization:** Minimalisir distorsi
    4. **Packing:** Atur UV islands efisien
    
    **Challenges:**
    - Minimalisir distorsi (stretching/compression)
    - Menghindari seams yang visible
    - Optimasi texture space usage
    - Handle complex geometry
    
    **Tools:** Blender, Maya, 3ds Max, Substance Painter
    """)

st.markdown("---")

# --- Texture Filtering Detail --- #
with st.expander("**Detail Texture Filtering**", expanded=False):
    st.markdown("### Bagaimana Texture Filtering Bekerja")
    
    filtering_col1, filtering_col2 = st.columns(2)
    
    with filtering_col1:
        st.markdown("""
        ** Nearest Neighbor (Point Sampling)**
        
        **Algoritma:**
        ```python
        def nearest_neighbor(u, v, texture):
            # Konversi UV (0-1) ke pixel coordinates
            x = int(u * texture.width)
            y = int(v * texture.height)
            
            # Clamp ke batas texture
            x = clamp(x, 0, texture.width - 1)
            y = clamp(y, 0, texture.height - 1)
            
            # Return pixel color
            return texture[x, y]
        ```
        
        **Karakteristik:**
        - 1 texture lookup per pixel
        - Tidak ada blending
        - O(1) complexity
        - Hasil: Sharp, pixelated
        
        **Kapan Menggunakan:**
        - Pixel art games (Minecraft, Terraria)
        - Retro aesthetic
        - UI rendering crisp
        - Debug/wireframe modes
        """)
        
        st.markdown("""
        ** Bilinear Filtering**
        
        **Algoritma:**
        ```python
        def bilinear(u, v, texture):
            # Floating point coordinates
            x = u * texture.width - 0.5
            y = v * texture.height - 0.5
            
            # Integer parts
            x0 = int(floor(x))
            y0 = int(floor(y))
            x1 = x0 + 1
            y1 = y0 + 1
            
            # Fractional parts (weights)
            fx = x - x0
            fy = y - y0
            
            # Sample 4 pixels
            c00 = texture[x0, y0]
            c10 = texture[x1, y0]
            c01 = texture[x0, y1]
            c11 = texture[x1, y1]
            
            # Interpolate horizontally
            c0 = lerp(c00, c10, fx)
            c1 = lerp(c01, c11, fx)
            
            # Interpolate vertically
            return lerp(c0, c1, fy)
        ```
        
        **Karakteristik:**
        - 4 texture lookups per pixel
        - Linear interpolation
        - O(1) complexity
        - Hasil: Smooth, slightly blurry
        """)
    
    with filtering_col2:
        st.markdown("""
        ** Trilinear Filtering**
        
        **Konsep Mipmaps:**
        - Pre-computed texture pyramid
        - Setiap level = 1/4 resolusi sebelumnya
        - Level 0: Full resolution
        - Level n: 1×1 pixel
        
        **Algoritma:**
        ```python
        def trilinear(u, v, lod, mipmaps):
            # LOD = Level of Detail
            # Determine mipmap levels
            level0 = int(floor(lod))
            level1 = level0 + 1
            
            # Fraction between levels
            frac = lod - level0
            
            # Bilinear on level 0
            color0 = bilinear(u, v, mipmaps[level0])
            
            # Bilinear on level 1
            color1 = bilinear(u, v, mipmaps[level1])
            
            # Interpolate between levels
            return lerp(color0, color1, frac)
        ```
        
        **Karakteristik:**
        - 8 texture lookups per pixel (4+4)
        - Smooth LOD transitions
        - Requires mipmap generation
        - Memory: +33% (1 + 1/4 + 1/16 + ...)
        - Hasil: Best quality at distance
        
        **LOD Calculation:**
        ```
        LOD = log2(max(du/dx, dv/dy))
        ```
        Berdasarkan rate of change UV coordinates.
        """)
        
        st.markdown("""
        **Advanced: Anisotropic Filtering**
        
        **Problem:** Bilinear/Trilinear assumes isotropic (circular) sampling.
        Pada permukaan miring, butuh elongated (elliptical) sampling.
        
        **Solution:**
        - Sample multiple times dengan offset
        - Typically 2×, 4×, 8×, 16× AF
        - Much better quality on angles
        - More expensive (multiple bilinear samples)
        
        **Visual Improvement:**
        - Textures at steep angles stay sharp
        - Reduces blur on floors/walls
        - Essential for racing games
        """)

st.markdown("---")

# --- UV Unwrapping Techniques --- #
with st.expander(" **Teknik UV Unwrapping**", expanded=False):
    st.markdown("### Strategi Unwrapping untuk Berbagai Objek")
    
    unwrap_col1, unwrap_col2 = st.columns(2)
    
    with unwrap_col1:
        st.markdown("""
        ** Cube/Box Unwrapping:**
        ```
        +---+---+---+---+
        | T | F | B | B |
        +---+---+---+---+
        | L | R | Bo|   |
        +---+---+---+---+
        ```
        (T=Top, F=Front, B=Back, L=Left, R=Right, Bo=Bottom)
        
        - 6 faces unwrapped separately
        - Minimal distortion
        - Easy to texture
        - Good for buildings, boxes
        
        ** Sphere Unwrapping:**
        - **Cylindrical:** Good for poles (Earth globes)
        - **Cubic:** 6 faces like cube
        - **Equirectangular:** Panorama style
        - **Challenge:** Poles have distortion
        
        ** Character Unwrapping:**
        - **Symmetry:** Mirror left-right untuk save space
        - **Seams:** Hidden areas (under arms, back)
        - **Face:** Special attention, separate island
        - **Hands/Feet:** Can be mirrored
        
        **Best Practices:**
        1. Hide seams in natural creases
        2. Straighten important edges
        3. Maximize texture space usage
        4. Consider texel density (uniform detail)
        5. Test for stretching (checkerboard pattern)
        """)
    
    with unwrap_col2:
        st.markdown("""
        ** Unwrapping Methods:**
        
        **1. Planar Projection:**
        - Project from one direction (X, Y, or Z)
        - Simple but lots of distortion
        - Good for flat surfaces
        
        **2. Cylindrical Projection:**
        - Wrap around one axis
        - Good for bottles, arms, legs
        - Distortion at top/bottom
        
        **3. Spherical Projection:**
        - Wrap around sphere
        - Good for balls, heads
        - Pole distortion
        
        **4. Smart UV Project:**
        - Automatic island creation
        - Minimize distortion
        - May create many seams
        
        **5. Unwrap (Manual Seams):**
        - Mark seams yourself
        - Most control
        - Best results
        - Time-consuming
        
        **6. Conformal Unwrap:**
        - Preserve angles
        - Minimize area distortion
        - Math-heavy (LSCM algorithm)
        
        **Texture Packing:**
        - Arrange UV islands efficiently
        - Leave padding for mipmaps
        - Group similar-density islands
        - Rotate for better fit
        """)

st.markdown("---")

# --- Implementasi Kode --- #
st.markdown("###  Implementasi Kode")

with st.expander(" **Lihat Kode Implementasi Texture Sampling**", expanded=False):
    st.markdown("""
    Berikut adalah implementasi manual texture sampling untuk educational purposes.
    Dalam praktik, GPU melakukan ini secara hardware-accelerated.
    """)
    
    st.markdown("---")
    
    code_col1, code_col2 = st.columns(2)
    
    with code_col1:
        st.markdown("**Nearest Neighbor Sampling:**")
        st.code("""
def sample_texture_nearest(texture, u, v):
    '''
    Sample tekstur menggunakan nearest neighbor
    
    Args:
        texture: PIL Image object
        u, v: UV coordinates (0-1)
    
    Returns:
        (r, g, b) tuple
    '''
    width, height = texture.size
    
    # Convert UV to pixel coordinates
    x = int(u * width)
    y = int((1 - v) * height)  # Flip V
    
    # Clamp to texture bounds
    x = max(0, min(x, width - 1))
    y = max(0, min(y, height - 1))
    
    # Get pixel color
    return texture.getpixel((x, y))


def wrap_uv(u, v, mode='repeat'):
    '''
    Handle UV coordinates outside [0,1] range
    
    Args:
        u, v: UV coordinates
        mode: 'repeat', 'clamp', 'mirror'
    
    Returns:
        Wrapped (u, v)
    '''
    if mode == 'repeat':
        u = u % 1.0
        v = v % 1.0
    elif mode == 'clamp':
        u = max(0, min(u, 1))
        v = max(0, min(v, 1))
    elif mode == 'mirror':
        u = abs(u % 2.0 - 1.0)
        v = abs(v % 2.0 - 1.0)
    
    return u, v
        """, language="python")
    
    with code_col2:
        st.markdown("**Bilinear Filtering:**")
        st.code("""
def lerp(a, b, t):
    '''Linear interpolation'''
    return a + t * (b - a)


def sample_texture_bilinear(texture, u, v):
    '''
    Sample tekstur menggunakan bilinear filtering
    
    Args:
        texture: PIL Image object
        u, v: UV coordinates (0-1)
    
    Returns:
        (r, g, b) tuple
    '''
    width, height = texture.size
    pixels = texture.load()
    
    # Convert to pixel space
    x = u * width - 0.5
    y = (1 - v) * height - 0.5
    
    # Get integer coordinates
    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    x1 = x0 + 1
    y1 = y0 + 1
    
    # Clamp
    x0 = max(0, min(x0, width - 1))
    x1 = max(0, min(x1, width - 1))
    y0 = max(0, min(y0, height - 1))
    y1 = max(0, min(y1, height - 1))
    
    # Get fractional part (weights)
    fx = x - int(x)
    fy = y - int(y)
    
    # Sample 4 corners
    c00 = pixels[x0, y0]
    c10 = pixels[x1, y0]
    c01 = pixels[x0, y1]
    c11 = pixels[x1, y1]
    
    # Interpolate each channel
    result = []
    for i in range(len(c00)):
        # Horizontal interpolation
        top = lerp(c00[i], c10[i], fx)
        bot = lerp(c01[i], c11[i], fx)
        # Vertical interpolation
        final = lerp(top, bot, fy)
        result.append(int(final))
    
    return tuple(result)
        """, language="python")
    
    st.markdown("---")
    st.markdown("**Mipmap Generation:**")
    st.code("""
def generate_mipmaps(texture, max_levels=None):
    '''
    Generate mipmap pyramid untuk texture
    
    Args:
        texture: PIL Image object
        max_levels: Maximum number of levels (None = auto)
    
    Returns:
        List of mipmap levels (PIL Images)
    '''
    mipmaps = [texture]
    width, height = texture.size
    
    # Calculate max levels if not specified
    if max_levels is None:
        max_levels = int(np.log2(max(width, height))) + 1
    
    current = texture
    for level in range(1, max_levels):
        # Stop if too small
        if current.width <= 1 and current.height <= 1:
            break
        
        # Calculate new size (half)
        new_width = max(1, current.width // 2)
        new_height = max(1, current.height // 2)
        
        # Downsample using high-quality filter
        current = current.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )
        
        mipmaps.append(current)
    
    return mipmaps


def sample_texture_trilinear(mipmaps, u, v, lod):
    '''
    Sample texture using trilinear filtering
    
    Args:
        mipmaps: List of mipmap levels
        u, v: UV coordinates (0-1)
        lod: Level of detail (float)
    
    Returns:
        (r, g, b) interpolated color
    '''
    # Clamp LOD to valid range
    lod = max(0, min(lod, len(mipmaps) - 1))
    
    # Get two nearest mipmap levels
    level0 = int(np.floor(lod))
    level1 = min(level0 + 1, len(mipmaps) - 1)
    frac = lod - level0
    
    # Bilinear sample from both levels
    color0 = sample_texture_bilinear(mipmaps[level0], u, v)
    color1 = sample_texture_bilinear(mipmaps[level1], u, v)
    
    # Interpolate between levels
    result = []
    for i in range(len(color0)):
        final = lerp(color0[i], color1[i], frac)
        result.append(int(final))
    
    return tuple(result)


def calculate_lod(dudx, dudy, dvdx, dvdy, texture_size):
    '''
    Calculate Level of Detail for trilinear filtering
    
    Args:
        dudx, dudy: Partial derivatives of u
        dvdx, dvdy: Partial derivatives of v
        texture_size: (width, height) of texture
    
    Returns:
        LOD value (float)
    '''
    width, height = texture_size
    
    # Calculate texture space derivatives
    dudx_tex = dudx * width
    dudy_tex = dudy * width
    dvdx_tex = dvdx * height
    dvdy_tex = dvdy * height
    
    # Calculate footprint
    px = np.sqrt(dudx_tex**2 + dvdx_tex**2)
    py = np.sqrt(dudy_tex**2 + dvdy_tex**2)
    
    # LOD is log2 of max footprint
    lod = np.log2(max(px, py))
    
    return max(0, lod)
    """, language="python")

st.markdown("---")

# --- Real-World Applications --- #
with st.expander(" **Aplikasi Texture Mapping di Dunia Nyata**", expanded=False):
    st.markdown("### Penggunaan dalam Berbagai Industri")
    
    app_col1, app_col2 = st.columns(2)
    
    with app_col1:
        st.markdown("""
        ** Video Games:**
        
        **Real-time Rendering:**
        - Character skins & clothing details
        - Environment textures (walls, floors, terrain)
        - Prop details (furniture, objects)
        - Particle effects textures
        
        **Optimization Techniques:**
        - Texture atlases (combine multiple textures)
        - Texture streaming (load on demand)
        - Mipmaps for LOD management
        - Compression (DXT, ASTC, BCn formats)
        
        **Examples:**
        - **The Last of Us:** Highly detailed character textures
        - **Minecraft:** Iconic pixel-art block textures
        - **Cyberpunk 2077:** 8K texture packs available
        
        ---
        
        ** Film & Animation:**
        
        **High-Quality Rendering:**
        - 4K-8K texture resolution
        - Multiple texture maps per material
        - Displacement for micro-detail
        - UDIM workflows (multiple texture tiles)
        
        **Examples:**
        - **Pixar/Disney:** Character fur, skin, clothing
        - **Marvel VFX:** Realistic superhero suits
        - **Avatar:** Alien world texturing
        
        ---
        
        ** Architecture & Visualization:**
        
        **Photorealistic Rendering:**
        - Building materials (wood, concrete, metal)
        - Interior design visualization
        - Landscaping textures
        - Product visualization
        
        **Tools:** V-Ray, Corona, Unreal Engine 5
        """)
    
    with app_col2:
        st.markdown("""
        ** Automotive & Product Design:**
        
        **Virtual Prototyping:**
        - Car paint & material simulation
        - Interior fabrics and leather
        - Metal finishes (chrome, brushed)
        - Product packaging visualization
        
        **Benefits:**
        - Reduce physical prototyping costs
        - Quick design iterations
        - Marketing material generation
        
        ---
        
        ** Mapping & GIS:**
        
        **Geospatial Visualization:**
        - Satellite imagery texture mapping
        - Terrain elevation with textures
        - Urban 3D modeling (Google Earth)
        - Virtual tours and navigation
        
        **Data:**
        - Aerial photography
        - Satellite data (Landsat, Sentinel)
        - Street-level imagery
        
        ---
        
        ** VR/AR Applications:**
        
        **Immersive Experiences:**
        - 360° panorama textures
        - Environment mapping for reflections
        - Real-time texture streaming
        - Hand-tracked interaction objects
        
        **Challenges:**
        - High resolution for close viewing
        - Performance constraints (mobile VR)
        - Stereoscopic considerations
        
        ---
        
        ** Digital Art & NFTs:**
        
        **Generative Art:**
        - Procedural texture generation
        - AI-generated textures
        - Unique variations for NFTs
        - Style transfer techniques
        """)

st.markdown("---")

# --- Advanced Topics --- #
with st.expander(" **Topik Lanjutan: Advanced Texturing**", expanded=False):
    st.markdown("### Teknik Texturing Modern")
    
    advanced_col1, advanced_col2 = st.columns(2)
    
    with advanced_col1:
        st.markdown("""
        ** Physically Based Rendering (PBR):**
        
        **Material Model:**
        - **Albedo/Base Color:** Pure color (no lighting baked)
        - **Metallic:** Is it metal? (0=dielectric, 1=metal)
        - **Roughness:** Surface microsurface detail
        - **Normal:** Simulated bumps and dents
        - **Ambient Occlusion:** Crevice darkening
        - **Height/Displacement:** Actual geometry modification
        
        **Why PBR?**
        - Consistent across lighting conditions
        - Physically accurate energy conservation
        - Easier to author realistic materials
        - Industry standard (Unreal, Unity, etc.)
        
        **Workflow:**
        ```
        Scan/Photo → Process in Substance → 
        PBR Maps → Import to Engine → 
        Looks great everywhere!
        ```
        
        ---
        
        ** Procedural Texturing:**
        
        **Node-Based Generation:**
        - No image files needed
        - Infinite resolution
        - Parametric control
        - Variation without memory cost
        
        **Techniques:**
        - Perlin/Simplex noise
        - Voronoi cells
        - Fractals (for terrain)
        - Mathematical patterns
        
        **Tools:**
        - Substance Designer
        - Blender Shader Nodes
        - Houdini
        - MaterialX
        
        **Use Cases:**
        - Organic materials (wood, marble)
        - Terrain generation
        - Sci-fi tech panels
        - Infinite variations
        """)
    
    with advanced_col2:
        st.markdown("""
        ** Texture Compression:**
        
        **Why Compress?**
        - Reduce memory usage (VRAM critical)
        - Faster loading times
        - Bandwidth savings (streaming)
        - More textures in scene
        
        **Common Formats:**
        - **DXT/BCn (Desktop):** Block compression, 4:1 or 6:1
        - **ASTC (Mobile):** Flexible block sizes, excellent quality
        - **ETC2 (Mobile):** OpenGL ES standard
        - **PVRTC (iOS):** PowerVR specific
        
        **Trade-offs:**
        - Lossy compression = artifacts
        - Fixed compression ratio
        - Hardware decompression (fast)
        
        ---
        
        ** Virtual Texturing:**
        
        **Mega Textures (id Tech):**
        - One huge texture for entire world
        - Stream only visible parts
        - Unique texturing everywhere
        - Used in Rage, Wolfenstein
        
        **Problems:**
        - Massive storage requirements
        - Complex streaming system
        - Authoring workflow challenges
        
        ---
        
        ** AI-Generated Textures:**
        
        **Modern Approaches:**
        - **Neural Style Transfer:** Apply art styles
        - **GANs:** Generate novel textures
        - **Diffusion Models:** Text-to-texture
        - **Super-resolution:** Upscale textures
        
        **Tools:**
        - DALL-E, Midjourney, Stable Diffusion
        - Topaz Gigapixel AI
        - Nvidia Texture Tools Exporter
        
        **Future:**
        - Real-time AI upscaling (DLSS-like for textures)
        - Procedural + AI hybrid
        - Text prompt → full material
        """)
    
    st.markdown("---")
    st.markdown("### Normal Mapping: Fake Detail Without Geometry")
    
    normal_col1, normal_col2 = st.columns(2)
    
    with normal_col1:
        st.markdown("""
        ** Normal Maps Explained:**
        
        **Concept:**
        - Store surface normal direction in RGB
        - R = X direction (red)
        - G = Y direction (green)  
        - B = Z direction (blue, usually pointing "out")
        - Typically looks bluish-purple
        
        **How It Works:**
        ```
        1. Store high-poly normals in texture
        2. Apply to low-poly model
        3. Lighting calculations use perturbed normals
        4. Result: Appears high-poly!
        ```
        
        **Benefits:**
        - Massive poly count reduction
        - Detail without performance cost
        - Can be baked from high-poly sculpts
        
        **Types:**
        - **Tangent Space:** Most common, portable
        - **Object Space:** Less common, RGB all over
        - **World Space:** Rarely used
        """)
    
    with normal_col2:
        st.markdown("""
        ** Creating Normal Maps:**
        
        **From High-Poly:**
        1. Sculpt high-detail model (ZBrush, Blender)
        2. Create low-poly version
        3. UV unwrap low-poly
        4. Bake high → low (capture details)
        5. Result: Normal map texture
        
        **From Height Map:**
        ```python
        # Pseudo-code
        for each pixel (x, y):
            height_left = heightmap[x-1, y]
            height_right = heightmap[x+1, y]
            height_up = heightmap[x, y-1]
            height_down = heightmap[x, y+1]
            
            dx = height_right - height_left
            dy = height_down - height_up
            
            normal = normalize((-dx, -dy, 1))
            normal_map[x,y] = normal * 0.5 + 0.5
        ```
        
        **Tools:**
        - Substance Designer/Painter
        - CrazyBump
        - xNormal
        - Knald
        - Blender baking
        """)

st.markdown("---")

# --- Performance Tips --- #
with st.expander("**Optimasi Performa Texturing**", expanded=False):
    st.markdown("### Best Practices untuk Efisiensi")
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        st.markdown("""
        ** Texture Optimization:**
        
        **1. Resolution Management:**
        ```
        - Hero assets: 2K-4K
        - Props: 1K-2K
        - Background: 512-1K
        - Tiny objects: 256-512
        ```
        Gunakan resolusi sesuai importance!
        
        **2. Texture Atlases:**
        - Combine multiple textures → 1 file
        - Reduce draw calls (major performance win)
        - Better for mobile/web
        - Tools: TexturePacker, Sprite Packer
        
        **3. Compression:**
        - Always use compressed formats in production
        - DXT/BCn for desktop
        - ASTC for mobile (best quality/size)
        - Test visually (some textures compress poorly)
        
        **4. Mipmaps:**
        - Auto-generate in engine
        - Saves bandwidth
        - Prevents aliasing
        - Small memory cost (+33%)
        
        **5. Streaming:**
        - Load high-res only when close
        - Unload distant textures
        - Async loading (no hitches)
        - Virtual texturing for massive worlds
        """)
    
    with perf_col2:
        st.markdown("""
        ** Common Performance Pitfalls:**
        
        **1. Uncompressed Textures:**
        ```
        Bad:  4K RGBA uncompressed = 64 MB
        Good: 4K DXT5 compressed = 10.67 MB
        Savings: 83% reduction!
        ```
        
        **2. No Mipmaps:**
        - Texture aliasing (shimmering)
        - Cache thrashing
        - Wasted memory bandwidth
        - Always enable for 3D!
        
        **3. Too Many Texture Switches:**
        - Each texture bind = GPU state change
        - Use atlases to batch
        - Sort by material/texture
        
        **4. Non-Power-of-Two (NPOT):**
        - Some hardware slower with NPOT
        - Mipmaps may not work
        - Use POT when possible (256, 512, 1024, 2K, 4K)
        
        **5. Forgetting Alpha:**
        - If no transparency, use RGB not RGBA
        - Save 25% memory
        - Faster sampling
        
        **6. Excessive Anisotropic Filtering:**
        - 16× AF everywhere is overkill
        - Use 4× for most, 8× for important
        - Disable for UI/particles
        
        **Profiling Tools:**
        - RenderDoc (frame capture)
        - PIX (DirectX)
        - Xcode Instruments (Metal)
        - Chrome DevTools (WebGL)
        """)

# --- Footer --- #
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p> <strong>Tips:</strong> Upload tekstur sendiri dan lihat bagaimana UV mapping mempengaruhi hasil akhir!</p>
    <p>Minggu 7: Pemetaan Tekstur | © 2025 Grafika Komputer</p>
</div>
""", unsafe_allow_html=True)