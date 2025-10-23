"""
Implementasi Algoritma Transformasi 2D.

Berisi fungsi-fungsi untuk melakukan transformasi geometri dasar pada
objek 2D, seperti translasi, rotasi, penskalaan, dan shearing.
Fungsi-fungsi ini bekerja dengan matriks transformasi.
"""

import numpy as np
from typing import Tuple, List

# Tipe data untuk titik dan matriks untuk kejelasan
Point = Tuple[float, float]
Matrix = np.ndarray

def create_translation_matrix(tx: float, ty: float) -> Matrix:
    """
    Membuat matriks transformasi untuk translasi (pergeseran).

    Args:
        tx (float): Pergeseran pada sumbu x.
        ty (float): Pergeseran pada sumbu y.

    Returns:
        Matrix: Matriks translasi 3x3.
    """
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])

def create_rotation_matrix(angle_degrees: float, cx: float = 0, cy: float = 0) -> Matrix:
    """
    Membuat matriks transformasi untuk rotasi di sekitar titik pusat.

    Args:
        angle_degrees (float): Sudut rotasi dalam derajat.
        cx (float): Koordinat x dari pusat rotasi.
        cy (float): Koordinat y dari pusat rotasi.

    Returns:
        Matrix: Matriks rotasi 3x3.
    """
    angle_rad = np.radians(angle_degrees)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    # Matriks untuk memindahkan ke titik asal, rotasi, lalu kembali
    to_origin = create_translation_matrix(-cx, -cy)
    rotate = np.array([
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ])
    from_origin = create_translation_matrix(cx, cy)

    # Gabungkan matriks (urutan penting: T * R * T^-1)
    return from_origin @ rotate @ to_origin

def create_scale_matrix(sx: float, sy: float, cx: float = 0, cy: float = 0) -> Matrix:
    """
    Membuat matriks transformasi untuk penskalaan dari titik pusat.

    Args:
        sx (float): Faktor skala pada sumbu x.
        sy (float): Faktor skala pada sumbu y.
        cx (float): Koordinat x dari pusat penskalaan.
        cy (float): Koordinat y dari pusat penskalaan.

    Returns:
        Matrix: Matriks penskalaan 3x3.
    """
    # Matriks untuk memindahkan ke titik asal, skala, lalu kembali
    to_origin = create_translation_matrix(-cx, -cy)
    scale = np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ])
    from_origin = create_translation_matrix(cx, cy)

    # Gabungkan matriks (urutan penting: T * S * T^-1)
    return from_origin @ scale @ to_origin

def create_shear_matrix(shx: float, shy: float) -> Matrix:
    """
    Membuat matriks transformasi untuk shearing (condong).

    Args:
        shx (float): Faktor shear pada sumbu x.
        shy (float): Faktor shear pada sumbu y.

    Returns:
        Matrix: Matriks shear 3x3.
    """
    return np.array([
        [1,   shx, 0],
        [shy, 1,   0],
        [0,   0,   1]
    ])

def apply_transformation(points: List[Point], matrix: Matrix) -> List[Point]:
    """
    Menerapkan matriks transformasi ke daftar titik.

    Args:
        points (List[Point]): Daftar titik (x, y) yang akan ditransformasi.
        matrix (Matrix): Matriks transformasi 3x3.

    Returns:
        List[Point]: Daftar titik baru setelah transformasi.
    """
    # Mengubah titik ke koordinat homogen [x, y, 1]
    homogeneous_points = np.array([list(p) + [1] for p in points]).T

    # Menerapkan transformasi dengan perkalian matriks
    transformed_points_homogeneous = matrix @ homogeneous_points

    # Mengubah kembali ke koordinat Kartesius [x, y]
    transformed_points = transformed_points_homogeneous[:2, :].T

    return [tuple(p) for p in transformed_points]

def combine_transformations(matrices: List[Matrix]) -> Matrix:
    """
    Menggabungkan beberapa matriks transformasi menjadi satu matriks komposit.

    Args:
        matrices (List[Matrix]): Daftar matriks yang akan digabungkan.

    Returns:
        Matrix: Matriks komposit hasil perkalian.
    """
    composite_matrix = np.identity(3)
    for m in matrices:
        composite_matrix = m @ composite_matrix
    return composite_matrix
