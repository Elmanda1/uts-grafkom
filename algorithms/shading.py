"""
Implementasi Teknik Shading.

Berisi fungsi-fungsi untuk menerapkan teknik shading yang berbeda pada
permukaan objek 3D, yaitu Flat, Gouraud, dan Phong shading.
"""

import numpy as np
from typing import List, Tuple, Dict

from algorithms.color_models import calculate_phong_lighting

# Tipe data untuk kejelasan
Vector3D = np.ndarray
Polygon = List[int] # List of vertex indices
Vertex = Dict[str, Vector3D] # e.g., {'position': vec, 'normal': vec}

def flat_shading(polygon: Polygon, vertices: List[Vertex], **kwargs) -> Tuple[float, float, float]:
    """
    Menghitung warna untuk satu poligon menggunakan Flat Shading.
    Pencahayaan dihitung sekali untuk seluruh poligon.

    Args:
        polygon (Polygon): Indeks-indeks vertex yang membentuk poligon.
        vertices (List[Vertex]): Daftar semua vertex dalam objek.
        **kwargs: Argumen pencahayaan (light_color, light_position, etc.).

    Returns:
        Tuple[float, float, float]: Warna RGB tunggal untuk poligon tersebut.
    """
    # Ambil posisi vertex dari poligon
    poly_vertices_pos = [vertices[i]['position'] for i in polygon]

    # Hitung titik pusat (centroid) dan normal rata-rata poligon
    centroid = np.mean(poly_vertices_pos, axis=0)
    
    # Normal poligon bisa dihitung dari cross product dua sisi, atau rata-rata normal vertex
    # Kita gunakan rata-rata normal vertex untuk konsistensi
    poly_normals = [vertices[i]['normal'] for i in polygon]
    face_normal = np.mean(poly_normals, axis=0)
    face_normal /= np.linalg.norm(face_normal)

    # Hitung pencahayaan di centroid
    color = calculate_phong_lighting(
        point_position=centroid,
        point_normal=face_normal,
        **kwargs
    )
    return color

def gouraud_shading(polygon: Polygon, vertices: List[Vertex], **kwargs) -> List[Tuple[float, float, float]]:
    """
    Menghitung warna untuk setiap vertex poligon menggunakan Gouraud Shading.
    Warna di dalam poligon kemudian diinterpolasi oleh rasterizer (GPU/software).

    Args:
        polygon (Polygon): Indeks-indeks vertex yang membentuk poligon.
        vertices (List[Vertex]): Daftar semua vertex dalam objek.
        **kwargs: Argumen pencahayaan.

    Returns:
        List[Tuple[float, float, float]]: Daftar warna RGB untuk setiap vertex poligon.
    """
    vertex_colors = []
    for vertex_index in polygon:
        vertex = vertices[vertex_index]
        # Hitung pencahayaan di setiap vertex
        color = calculate_phong_lighting(
            point_position=vertex['position'],
            point_normal=vertex['normal'],
            **kwargs
        )
        vertex_colors.append(color)
    
    return vertex_colors

def phong_shading_vectors(polygon: Polygon, vertices: List[Vertex]) -> Tuple[List[Vector3D], List[Vector3D]]:
    """
    Menyiapkan vektor normal untuk Phong Shading.
    Normal diinterpolasi di seluruh permukaan poligon oleh rasterizer,
    dan pencahayaan dihitung per-piksel.

    Fungsi ini hanya mengembalikan normal di setiap vertex. Perhitungan warna
    sebenarnya terjadi di fragment shader (disimulasikan di rasterizer).

    Args:
        polygon (Polygon): Indeks-indeks vertex yang membentuk poligon.
        vertices (List[Vertex]): Daftar semua vertex dalam objek.

    Returns:
        Tuple[List[Vector3D], List[Vector3D]]: Daftar posisi vertex dan normal vertex.
    """
    poly_positions = [vertices[i]['position'] for i in polygon]
    poly_normals = [vertices[i]['normal'] for i in polygon]
    
    return poly_positions, poly_normals

# Dalam simulasi software, kita bisa membuat fungsi yang menginterpolasi
# normal dan menghitung warna per piksel, tapi itu sangat intensif.
# Untuk tujuan demo, kita bisa menyederhanakannya.
