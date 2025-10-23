"""
Utilitas untuk Streamlit Drawable Canvas.

Berisi fungsi-fungsi untuk setup, konfigurasi, dan interaksi dengan
komponen streamlit-drawable-canvas.
"""

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from typing import Dict, Any, Optional

from config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_COLORS

def setup_canvas(
    drawing_mode: str,
    stroke_width: int = 2,
    stroke_color: str = DEFAULT_COLORS["primary"],
    background_color: str = DEFAULT_COLORS["background"],
    key: str = "canvas",
    height: int = CANVAS_HEIGHT,
    width: int = CANVAS_WIDTH,
    initial_drawing: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Mengkonfigurasi dan menampilkan komponen streamlit-drawable-canvas.

    Args:
        drawing_mode (str): Mode menggambar (e.g., 'freedraw', 'line', 'rect', 'circle', 'transform').
        stroke_width (int): Lebar goresan (stroke).
        stroke_color (str): Warna goresan.
        background_color (str): Warna latar belakang canvas.
        key (str): Kunci unik untuk komponen canvas.
        height (int): Tinggi canvas.
        width (int): Lebar canvas.
        initial_drawing (Optional[Dict]): Data gambar awal untuk dimuat ke canvas.

    Returns:
        Any: Objek hasil dari st_canvas yang berisi data gambar.
    """
    # Validasi input dasar
    if not isinstance(stroke_width, int) or stroke_width <= 0:
        stroke_width = 2
        st.warning("Lebar goresan tidak valid, diatur ke default (2).")

    # Menampilkan canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Warna isian default (untuk poligon, dll)
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=background_color,
        background_image=None,  # Bisa ditambahkan jika perlu
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode=drawing_mode,
        initial_drawing=initial_drawing,
        key=key,
    )
    return canvas_result

def get_canvas_data(canvas_result: Any) -> Optional[Dict[str, Any]]:
    """
    Mengekstrak data (geometri) dari hasil canvas.

    Args:
        canvas_result (Any): Objek hasil dari st_canvas.

    Returns:
        Optional[Dict[str, Any]]: Dictionary JSON dari data gambar jika tersedia.
    """
    if canvas_result is not None and canvas_result.json_data is not None:
        return canvas_result.json_data
    return None

def export_canvas_to_image(canvas_result: Any):
    """
    Menyediakan tombol untuk mengunduh isi canvas sebagai gambar PNG.

    Args:
        canvas_result (Any): Objek hasil dari st_canvas.
    """
    if canvas_result.image_data is not None:
        try:
            st.download_button(
                label="🖼️ Unduh sebagai PNG",
                data=canvas_result.image_data.tobytes(),
                file_name="hasil_canvas.png",
                mime="image/png",
            )
        except Exception as e:
            st.error(f"Gagal membuat tombol unduh: {e}")
    else:
        st.info("Tidak ada gambar untuk diunduh. Silakan gambar sesuatu di canvas.")
