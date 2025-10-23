"""
Implementasi Algoritma Penggambaran Lingkaran.

Berisi implementasi dari algoritma Lingkaran Midpoint (juga dikenal sebagai
varian dari algoritma Bresenham untuk lingkaran).
"""

from typing import List, Tuple, Dict, Any
from utils.helpers import performance_tracker

Point = Tuple[int, int]

def _plot_circle_points(xc: int, yc: int, x: int, y: int, pixels: List[Point], op_counter: Dict[str, int]):
    """
    Mencerminkan titik-titik di 8 oktan lingkaran.
    """
    points_to_add = [
        (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
    ]
    pixels.extend(points_to_add)
    op_counter['count'] += 16 # 8 penambahan/pengurangan * 2
    op_counter['count'] += 1  # 1 extend call

@performance_tracker
def midpoint_circle(xc: int, yc: int, r: int, **kwargs) -> List[Point]:
    """
    Menghasilkan titik-titik untuk sebuah lingkaran menggunakan algoritma Midpoint.

    Complexity:
        Time: O(r)
        Space: O(1) untuk generator, O(r) untuk list hasil

    Args:
        xc, yc (int): Koordinat pusat lingkaran.
        r (int): Jari-jari lingkaran.
        **kwargs: Digunakan untuk menerima 'operation_counter'.

    Returns:
        List[Point]: Daftar titik (x, y) yang membentuk lingkaran.
    """
    pixels = []
    op_counter = kwargs.get('operation_counter', {'count': 0})

    if r <= 0:
        return []

    x = 0
    y = r
    p = 1 - r  # Parameter keputusan awal
    op_counter['count'] += 1 # 1 pengurangan

    # Plot titik awal di setiap oktan
    _plot_circle_points(xc, yc, x, y, pixels, op_counter)

    while x < y:
        x += 1
        op_counter['count'] += 1 # 1 penambahan

        if p < 0:
            p += 2 * x + 1
            op_counter['count'] += 3 # 1 perkalian, 2 penambahan
        else:
            y -= 1
            p += 2 * (x - y) + 1
            op_counter['count'] += 5 # 1 pengurangan, 1 perkalian, 2 penambahan, 1 pengurangan

        _plot_circle_points(xc, yc, x, y, pixels, op_counter)

    return list(set(pixels)) # Hapus duplikat jika ada

# Algoritma Bresenham untuk lingkaran pada dasarnya identik dengan Midpoint
# jadi kita bisa membuat alias atau wrapper jika diperlukan.
bresenham_circle = midpoint_circle
