"""
Implementasi Algoritma Pengisian Poligon.

Berisi implementasi dari algoritma Scanline Fill, Flood Fill, dan Boundary Fill.
Karena kompleksitas pelacakan performa pada algoritma rekursif dan berbasis stack,
@performance_tracker mungkin tidak secara akurat menangkap semua operasi,
tapi tetap memberikan gambaran waktu eksekusi.
"""

import numpy as np
from typing import List, Tuple, Dict, Any
from collections import deque
from utils.helpers import performance_tracker

Point = Tuple[int, int]
Color = Tuple[int, int, int]

# Catatan: Untuk aplikasi nyata, data gambar akan di-pass sebagai argumen (misal, numpy array)
# Di sini, kita akan mensimulasikan canvas dengan dictionary atau numpy array jika diperlukan.

@performance_tracker
def scanline_fill(polygon_vertices: List[Point], fill_color: Color, **kwargs) -> List[Point]:
    """
    Mengisi poligon menggunakan algoritma Scanline Fill.
    Asumsi poligon sederhana (tidak memotong diri sendiri).

    Complexity:
        Time: O(H * E) di mana H adalah tinggi dan E adalah jumlah tepi.
        Space: O(E) atau O(W) tergantung implementasi.

    Args:
        polygon_vertices (List[Point]): Daftar titik sudut poligon.
        fill_color (Color): Warna isian (tidak digunakan secara langsung, tapi penting untuk konsep).
        **kwargs: Untuk performance tracker.

    Returns:
        List[Point]: Daftar piksel yang diisi.
    """
    pixels = []
    op_counter = kwargs.get('operation_counter', {'count': 0})

    if not polygon_vertices:
        return []

    # Temukan y_min dan y_max dari poligon
    y_coords = [p[1] for p in polygon_vertices]
    y_min, y_max = min(y_coords), max(y_coords)
    op_counter['count'] += len(y_coords) * 2

    # Proses setiap baris pindai (scanline)
    for y in range(y_min, y_max + 1):
        intersections = []
        num_vertices = len(polygon_vertices)
        p1 = polygon_vertices[num_vertices - 1]

        for i in range(num_vertices):
            p2 = polygon_vertices[i]
            op_counter['count'] += 1

            # Pastikan tepi tidak horizontal dan memotong scanline
            if p1[1] != p2[1] and min(p1[1], p2[1]) <= y < max(p1[1], p2[1]):
                # Hitung titik potong x menggunakan interpolasi linear
                x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                intersections.append(int(x_intersection))
                op_counter['count'] += 7 # Operasi aritmatika

            p1 = p2

        # Urutkan titik potong dan isi piksel di antaranya
        intersections.sort()
        op_counter['count'] += len(intersections) * np.log(len(intersections)) if intersections else 0

        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                x_start, x_end = intersections[i], intersections[i+1]
                for x in range(x_start, x_end + 1):
                    pixels.append((x, y))
                    op_counter['count'] += 1

    return pixels

@performance_tracker
def flood_fill_4(canvas: np.ndarray, seed_point: Point, fill_color: Color, target_color: Color, **kwargs) -> List[Point]:
    """
    Mengisi area dengan algoritma Flood Fill (4 arah) menggunakan stack.

    Complexity:
        Time: O(W * H) dalam kasus terburuk.
        Space: O(W * H) dalam kasus terburuk.

    Args:
        canvas (np.ndarray): Array 2D yang merepresentasikan canvas.
        seed_point (Point): Titik awal pengisian.
        fill_color (Color): Warna baru untuk mengisi.
        target_color (Color): Warna yang akan diganti.
        **kwargs: Untuk performance tracker.

    Returns:
        List[Point]: Daftar piksel yang diisi.
    """
    pixels = []
    op_counter = kwargs.get('operation_counter', {'count': 0})
    height, width = canvas.shape[:2]
    
    if (seed_point[1] < 0 or seed_point[1] >= height or 
        seed_point[0] < 0 or seed_point[0] >= width):
        return []

    if tuple(canvas[seed_point[1], seed_point[0]]) != target_color:
        return []

    stack = deque([seed_point])

    while stack:
        x, y = stack.pop()
        op_counter['count'] += 1

        if (y < 0 or y >= height or x < 0 or x >= width or 
            tuple(canvas[y, x]) != target_color):
            continue

        canvas[y, x] = fill_color
        pixels.append((x, y))
        op_counter['count'] += 1

        # Tambahkan tetangga (4 arah)
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
        op_counter['count'] += 4

    return pixels

@performance_tracker
def boundary_fill_4(canvas: np.ndarray, seed_point: Point, fill_color: Color, boundary_color: Color, **kwargs) -> List[Point]:
    """
    Mengisi area dengan algoritma Boundary Fill (4 arah) menggunakan stack.

    Complexity:
        Time: O(W * H) dalam kasus terburuk.
        Space: O(W * H) dalam kasus terburuk.

    Args:
        canvas (np.ndarray): Array 2D yang merepresentasikan canvas.
        seed_point (Point): Titik awal pengisian.
        fill_color (Color): Warna baru untuk mengisi.
        boundary_color (Color): Warna batas area.
        **kwargs: Untuk performance tracker.

    Returns:
        List[Point]: Daftar piksel yang diisi.
    """
    pixels = []
    op_counter = kwargs.get('operation_counter', {'count': 0})
    height, width = canvas.shape[:2]

    if (seed_point[1] < 0 or seed_point[1] >= height or 
        seed_point[0] < 0 or seed_point[0] >= width):
        return []

    stack = deque([seed_point])

    while stack:
        x, y = stack.pop()
        op_counter['count'] += 1

        current_color = tuple(canvas[y, x])
        if (y < 0 or y >= height or x < 0 or x >= width or 
            current_color == boundary_color or current_color == fill_color):
            continue

        canvas[y, x] = fill_color
        pixels.append((x, y))
        op_counter['count'] += 1

        # Tambahkan tetangga (4 arah)
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
        op_counter['count'] += 4

    return pixels
