"""
File Konfigurasi Utama untuk Aplikasi Streamlit Grafika Komputer.

File ini berisi semua konstanta, path, dan pengaturan yang digunakan di seluruh aplikasi.
Tujuannya adalah untuk memusatkan konfigurasi agar mudah dikelola dan diubah.
"""

from typing import Dict, Any

# -- Konfigurasi Canvas ---------------------------------------------------------
CANVAS_WIDTH: int = 800
CANVAS_HEIGHT: int = 600

# -- Warna Default --------------------------------------------------------------
# Palet warna yang konsisten untuk digunakan di seluruh visualisasi.
DEFAULT_COLORS: Dict[str, str] = {
    "background": "#0E1117",
    "primary": "#FF4B4B",
    "secondary": "#1E88E5",
    "accent": "#00C853",
    "text": "#FAFAFA",
    "grid": "#424242",
}

# -- Konfigurasi Algoritma ------------------------------------------------------
# Menyimpan kompleksitas Big O untuk berbagai algoritma yang diimplementasikan.
# Ini digunakan untuk ditampilkan di UI dan membandingkan performa.
ALGORITHM_COMPLEXITIES: Dict[str, Dict[str, str]] = {
    "DDA": {"time": "O(max(|dx|, |dy|))", "space": "O(1)"},
    "Bresenham Line": {"time": "O(max(|dx|, |dy|))", "space": "O(1)"},
    "Midpoint Circle": {"time": "O(r)", "space": "O(1)"},
    "Bresenham Circle": {"time": "O(r)", "space": "O(1)"},
    "Scanline Fill": {"time": "O(W * H)", "space": "O(W)"},
    "Flood Fill": {"time": "O(W * H)", "space": "O(W * H)"},
    "Boundary Fill": {"time": "O(W * H)", "space": "O(W * H)"},
    "Flat Shading": {"time": "O(P)", "space": "O(1)"},  # P = jumlah poligon
    "Gouraud Shading": {"time": "O(P + V)", "space": "O(V)"},  # V = jumlah vertex
    "Phong Shading": {"time": "O(P * F)", "space": "O(F)"},  # F = jumlah fragmen/piksel
}

# -- Konfigurasi Halaman (Page Config) ------------------------------------------
# Pengaturan default untuk setiap halaman Streamlit.
PAGE_CONFIG: Dict[str, Any] = {
    "page_title": "Belajar Grafika Komputer",
    "page_icon": "🎨",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# -- Path Aset ------------------------------------------------------------------
# Path relatif ke direktori aset untuk memudahkan akses.
ASSETS_PATH: Dict[str, str] = {
    "styles": "assets/styles/custom.css",
    "data": "assets/data/sample_objects.json",
    "images": "assets/images/",
}

# -- Pengaturan Lainnya ---------------------------------------------------------
# Anda dapat menambahkan konstanta lain di sini sesuai kebutuhan.
# Contoh:
# MAX_POINTS_POLYGON = 20
# DEFAULT_LINE_WIDTH = 2
