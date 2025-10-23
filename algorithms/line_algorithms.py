"""
Implementasi Algoritma Penggambaran Garis.

Berisi implementasi dari algoritma DDA (Digital Differential Analyzer)
dan algoritma Garis Bresenham. Kedua fungsi dihiasi dengan @performance_tracker
untuk mengukur performa secara otomatis.
"""

from typing import List, Tuple, Dict, Any
from utils.helpers import performance_tracker

Point = Tuple[int, int]

@performance_tracker
def dda_line(x1: int, y1: int, x2: int, y2: int, **kwargs) -> List[Point]:
    """
    Menghasilkan titik-titik untuk sebuah garis menggunakan algoritma DDA.

    Complexity:
        Time: O(max(|dx|, |dy|))
        Space: O(1) untuk generator, O(N) untuk list hasil (N = panjang garis)

    Args:
        x1, y1 (int): Koordinat titik awal.
        x2, y2 (int): Koordinat titik akhir.
        **kwargs: Digunakan untuk menerima 'operation_counter'.

    Returns:
        List[Point]: Daftar titik (x, y) yang membentuk garis.
    """
    pixels = []
    op_counter = kwargs.get('operation_counter', {'count': 0})

    dx = x2 - x1
    dy = y2 - y1
    op_counter['count'] += 2 # 2 pengurangan

    steps = max(abs(dx), abs(dy))
    op_counter['count'] += 2 # 2 abs

    if steps == 0:
        pixels.append((x1, y1))
        op_counter['count'] += 1 # 1 append
        return pixels

    x_increment = dx / steps
    y_increment = dy / steps
    op_counter['count'] += 2 # 2 pembagian

    x, y = float(x1), float(y1)

    for _ in range(steps + 1):
        pixels.append((round(x), round(y)))
        x += x_increment
        y += y_increment
        op_counter['count'] += 4 # 2 pembulatan, 2 penambahan, 1 append

    return pixels

@performance_tracker
def bresenham_line(x1: int, y1: int, x2: int, y2: int, **kwargs) -> List[Point]:
    """
    Menghasilkan titik-titik untuk sebuah garis menggunakan algoritma Bresenham.
    Hanya menggunakan operasi integer.

    Complexity:
        Time: O(max(|dx|, |dy|))
        Space: O(1) untuk generator, O(N) untuk list hasil (N = panjang garis)

    Args:
        x1, y1 (int): Koordinat titik awal.
        x2, y2 (int): Koordinat titik akhir.
        **kwargs: Digunakan untuk menerima 'operation_counter'.

    Returns:
        List[Point]: Daftar titik (x, y) yang membentuk garis.
    """
    pixels = []
    op_counter = kwargs.get('operation_counter', {'count': 0})

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    op_counter['count'] += 4 # 2 pengurangan, 2 abs

    # Tentukan arah penambahan/pengurangan
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    op_counter['count'] += 2 # 2 perbandingan

    # Parameter keputusan
    err = dx - dy
    op_counter['count'] += 1 # 1 pengurangan

    x, y = x1, y1

    while True:
        pixels.append((x, y))
        op_counter['count'] += 1 # 1 append

        if x == x2 and y == y2:
            break

        e2 = 2 * err
        op_counter['count'] += 1 # 1 perkalian

        # Pindah horizontal
        if e2 > -dy:
            err -= dy
            x += sx
            op_counter['count'] += 2 # 1 pengurangan, 1 penambahan

        # Pindah vertikal
        if e2 < dx:
            err += dx
            y += sy
            op_counter['count'] += 2 # 1 penambahan, 1 penambahan

    return pixels
