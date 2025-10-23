"""
Implementasi Konversi Model Warna dan Pencahayaan Dasar.

Berisi fungsi-fungsi untuk konversi antara model warna (RGB, HSV, CMYK)
dan implementasi model pencahayaan dasar (Ambient, Diffuse, Specular)
yang dikenal sebagai model Phong.
"""

import numpy as np
from typing import Tuple

# Tipe data untuk warna
RGB = Tuple[float, float, float]
H_ = Tuple[float, float, float] # HSV atau HSL
CMYK = Tuple[float, float, float, float]
Vector3D = np.ndarray

# --- Konversi Model Warna -----------------------------------------------------

def rgb_to_hsv(rgb: RGB) -> H_:
    """
    Mengkonversi warna dari RGB (0-255) ke HSV (H: 0-360, S: 0-1, V: 0-1).
    """
    r, g, b = [x / 255.0 for x in rgb]
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    # Hitung Hue (H)
    if delta == 0:
        h = 0
    elif max_c == r:
        h = 60 * (((g - b) / delta) % 6)
    elif max_c == g:
        h = 60 * (((b - r) / delta) + 2)
    else: # max_c == b
        h = 60 * (((r - g) / delta) + 4)
    h = h if h >= 0 else h + 360

    # Hitung Saturation (S)
    s = 0 if max_c == 0 else delta / max_c

    # Hitung Value (V)
    v = max_c

    return (h, s, v)

def hsv_to_rgb(hsv: H_) -> RGB:
    """
    Mengkonversi warna dari HSV (H: 0-360, S: 0-1, V: 0-1) ke RGB (0-255).
    """
    h, s, v = hsv
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else: # 300 <= h < 360
        r, g, b = c, 0, x

    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

def rgb_to_cmyk(rgb: RGB) -> CMYK:
    """
    Mengkonversi warna dari RGB (0-255) ke CMYK (0-1).
    """
    r, g, b = [x / 255.0 for x in rgb]

    if r == 0 and g == 0 and b == 0:
        return 0.0, 0.0, 0.0, 1.0

    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)

    return (c, m, y, k)

def cmyk_to_rgb(cmyk: CMYK) -> RGB:
    """
    Mengkonversi warna dari CMYK (0-1) ke RGB (0-255).
    """
    c, m, y, k = cmyk
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return (int(r), int(g), int(b))

# --- Model Pencahayaan Phong --------------------------------------------------

def calculate_phong_lighting(
    light_color: RGB,
    light_position: Vector3D,
    camera_position: Vector3D,
    point_position: Vector3D,
    point_normal: Vector3D,
    material: dict
) -> RGB:
    """
    Menghitung warna akhir sebuah titik menggunakan model pencahayaan Phong.

    Args:
        light_color (RGB): Warna cahaya (intensitas per komponen R,G,B).
        light_position (Vector3D): Posisi sumber cahaya.
        camera_position (Vector3D): Posisi kamera/pengamat.
        point_position (Vector3D): Posisi titik di permukaan objek.
        point_normal (Vector3D): Vektor normal di titik tersebut.
        material (dict): Properti material objek berisi ka, kd, ks, shininess.

    Returns:
        RGB: Warna final titik tersebut dalam format (R, G, B) 0-255.
    """
    # Normalisasi vektor input
    normal = point_normal / np.linalg.norm(point_normal)
    light_dir = light_position - point_position
    light_dir = light_dir / np.linalg.norm(light_dir)
    view_dir = camera_position - point_position
    view_dir = view_dir / np.linalg.norm(view_dir)

    # 1. Komponen Ambient
    ambient = material['ka'] * np.array(light_color)

    # 2. Komponen Diffuse
    diffuse_intensity = max(np.dot(normal, light_dir), 0.0)
    diffuse = material['kd'] * diffuse_intensity * np.array(light_color)

    # 3. Komponen Specular
    reflection_dir = 2 * np.dot(normal, light_dir) * normal - light_dir
    specular_intensity = max(np.dot(view_dir, reflection_dir), 0.0) ** material['shininess']
    specular = material['ks'] * specular_intensity * np.array(light_color)

    # Gabungkan semua komponen
    final_color = ambient + diffuse + specular

    # Clamp nilai warna antara 0 dan 255
    final_color = np.clip(final_color, 0, 255)

    return tuple(final_color.astype(int))
