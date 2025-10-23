"""
Halaman Minggu 1: Pengantar Grafika Komputer.

Berisi materi tekstual mengenai sejarah, aplikasi, dan konsep dasar
dalam grafika komputer.
"""

import streamlit as st
from config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)

def show_week1():
    st.title("📚 Minggu 1: Pengantar Grafika Komputer")
    st.markdown("--- ")

    st.header("1. Sejarah Singkat Grafika Komputer")
    st.markdown(
        """
        Grafika komputer dimulai pada awal 1950-an dengan munculnya komputer digital pertama. 
        Beberapa tonggak penting:
        - **1951:** Komputer Whirlwind di MIT menampilkan data secara visual di layar CRT.
        - **1963:** Ivan Sutherland menciptakan **Sketchpad**, program yang dianggap sebagai cikal bakal CAD (Computer-Aided Design). Sketchpad memungkinkan pengguna menggambar titik, garis, dan lingkaran secara interaktif dengan *light pen*.
        - **1970-an:** Perkembangan algoritma fundamental seperti algoritma garis Bresenham, algoritma z-buffer untuk visibilitas, dan model pencahayaan Phong.
        - **1980-an:** Munculnya workstation grafis dari Silicon Graphics (SGI) dan popularitas film-film dengan CGI (Computer-Generated Imagery) seperti *Tron* (1982).
        - **1990-an:** Akselerasi grafis 3D menjadi umum di PC dengan munculnya kartu grafis seperti seri Voodoo dari 3dfx dan GeForce dari NVIDIA. Film *Toy Story* (1995) menjadi film panjang pertama yang sepenuhnya dibuat dengan CGI.
        - **2000-an hingga sekarang:** Perkembangan pesat dalam real-time rendering, GPGPU (General-Purpose computing on Graphics Processing Units), dan fotorealisme.
        """
    )

    st.header("2. Aplikasi Grafika Komputer")
    st.markdown(
        """
        Grafika komputer ada di mana-mana. Beberapa bidang aplikasi utamanya adalah:
        - **Hiburan:** Film, video game, serial animasi.
        - **Desain:** CAD/CAM untuk rekayasa, arsitektur, dan desain produk.
        - **Visualisasi Ilmiah dan Data:** Simulasi fluida, visualisasi data medis (MRI, CT scan), visualisasi data statistik.
        - **Pelatihan dan Simulasi:** Simulator penerbangan, simulator medis untuk pelatihan operasi.
        - **Antarmuka Pengguna (GUI):** Hampir semua sistem operasi modern dan aplikasi menggunakan grafika 2D/3D untuk interaksi.
        - **Virtual Reality (VR) dan Augmented Reality (AR):** Menciptakan lingkungan imersif untuk berbagai keperluan.
        """
    )

    st.header("3. Konsep Dasar")
    st.markdown(
        """
        Beberapa konsep fundamental yang akan kita pelajari:
        - **Raster vs Vektor:**
            - **Grafik Raster (Bitmap):** Gambar direpresentasikan sebagai grid piksel. Cocok untuk foto dan gambar kompleks. Contoh: JPEG, PNG, BMP.
            - **Grafik Vektor:** Gambar direpresentasikan oleh objek-objek geometris (garis, kurva, poligon) yang didefinisikan oleh persamaan matematika. Dapat diskalakan tanpa kehilangan kualitas. Contoh: SVG, font.
        - **Pipeline Grafika (Rendering Pipeline):** Serangkaian langkah yang mengubah model 3D menjadi gambar 2D di layar. Secara umum terdiri dari:
            1.  **Application Stage:** Logika aplikasi, deteksi tabrakan, dll (CPU).
            2.  **Geometry Processing:** Transformasi, proyeksi, dan pencahayaan (GPU).
            3.  **Rasterization:** Mengubah primitif geometri menjadi fragmen (calon piksel).
            4.  **Fragment Processing:** Menentukan warna akhir setiap fragmen (per-pixel shading, texturing).
            5.  **Per-Fragment Operations:** Z-buffering (uji kedalaman), blending, dll.
        - **Sistem Koordinat:** Penggunaan berbagai sistem koordinat (lokal, dunia, pandangan, proyeksi) untuk memanipulasi dan menampilkan objek.
        - **Model Warna:** Cara merepresentasikan warna secara digital, seperti RGB, HSV, dan CMYK.
        """
    )

    st.image("assets/images/IU.jpeg", 
             caption="Contoh Aplikasi Grafika Komputer.")

if __name__ == "__main__":
    show_week1()
