# 🎨 Aplikasi Pembelajaran Grafika Komputer Interaktif

Selamat datang di proyek Aplikasi Pembelajaran Grafika Komputer! Aplikasi web ini dibangun menggunakan Python dan Streamlit untuk menyediakan platform yang interaktif dan mudah digunakan untuk mempelajari konsep-konsep inti grafika komputer.

## 🌟 Deskripsi Proyek

Aplikasi ini dirancang sebagai alat bantu visual bagi mahasiswa atau siapa saja yang tertarik untuk memahami dasar-dasar grafika komputer. Setiap topik disajikan dalam "minggu" terpisah, lengkap dengan penjelasan teoretis, demo interaktif, perbandingan algoritma, dan cuplikan kode implementasi.

## ✨ Fitur Utama

- **Visualisasi Real-time:** Lihat hasil dari setiap algoritma secara langsung di kanvas.
- **Kontrol Interaktif:** Sesuaikan parameter menggunakan slider, pemilih warna, dan input lainnya.
- **Perbandingan Algoritma:** Analisis performa *side-by-side* (waktu eksekusi, kompleksitas) untuk algoritma alternatif.
- **Code Viewer:** Lihat implementasi Python dari setiap algoritma dengan *syntax highlighting*.
- **Demo 2D & 3D:** Mulai dari transformasi 2D, algoritma garis, hingga shading 3D.
- **Desain Responsif:** Dapat diakses dengan baik di desktop maupun perangkat mobile.

## 🛠️ Teknologi yang Digunakan

- **Framework:** [Streamlit](https://streamlit.io/)
- **Bahasa:** Python 3.9+
- **Library Utama:**
  - `numpy`: Untuk operasi numerik dan matriks.
  - `Pillow`: Untuk manipulasi gambar.
  - `plotly`: Untuk visualisasi 3D interaktif.
  - `pandas`: Untuk menampilkan tabel data dan metrik.
  - `streamlit-drawable-canvas`: Untuk input menggambar interaktif.

## 📂 Struktur Proyek

Struktur proyek diatur untuk modularitas dan kemudahan navigasi.

```
grafika-komputer-app/
├── app.py                  # Entry point utama aplikasi
├── requirements.txt        # Daftar dependensi Python
├── README.md               # File ini
├── config.py               # Konfigurasi & konstanta
├── utils/                  # Modul utilitas (helpers, canvas, code viewer)
├── pages/                  # Setiap file .py di sini menjadi halaman di aplikasi
│   ├── 1_🏠_Home.py
│   └── ... (file untuk setiap minggu)
├── algorithms/             # Implementasi inti dari semua algoritma grafika
│   ├── line_algorithms.py
│   └── ...
├── assets/                 # File statis (CSS, data, gambar)
│   ├── styles/custom.css
│   └── data/sample_objects.json
└── demos/                  # Komponen demo yang dapat digunakan kembali
```

## 🚀 Instalasi dan Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di lingkungan lokal Anda.

**1. Clone Repository**

```bash
git clone <URL_REPOSITORY_ANDA>
cd grafika-komputer-app
```

**2. Buat dan Aktifkan Virtual Environment (Dianjurkan)**

```bash
# Untuk Windows
python -m venv venv
.\venv\Scripts\activate

# Untuk macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instal Dependensi**

Pastikan Anda berada di direktori root `grafika-komputer-app` dan jalankan:

```bash
pip install -r requirements.txt
```

**4. Jalankan Aplikasi Streamlit**

Setelah instalasi selesai, jalankan perintah berikut:

```bash
streamlit run app.py
```

Aplikasi sekarang akan terbuka secara otomatis di browser default Anda. Jika tidak, buka browser dan arahkan ke `http://localhost:8501`.

## 👥 Tim Pengembang & Pembagian Tugas

- **Person 1: Foundation & Week 1-2**
  - `app.py`, `config.py`, `utils/`, `pages/1_Home`, `pages/2_Pengantar`, `pages/3_Transformasi`, `algorithms/transformations.py`.

- **Person 2: Week 3-4 (Line & Polygon Algorithms)**
  - `pages/4_Algoritma_Garis`, `pages/5_Polygon_Fill`, `algorithms/line_algorithms.py`, `algorithms/circle_algorithms.py`, `algorithms/polygon_fill.py`, `demos/interactive_line.py`, `demos/interactive_polygon.py`.

- **Person 3: Week 5-6 (Color & Lighting)**
  - `pages/6_Model_Warna`, `pages/7_Shading`, `algorithms/color_models.py`, `algorithms/shading.py`, `demos/color_picker.py`, `demos/shading_demo.py`.

- **Person 4: Week 7, Documentation & Assets**
  - `pages/8_Texturing`, `README.md`, `requirements.txt`, `assets/`.

## 📸 Screenshot (Placeholder)

*(Anda dapat menambahkan screenshot dari aplikasi yang berjalan di sini)*

![Screenshot Aplikasi](assets/images/IU.jpeg)
![Screenshot Demo Garis](placeholder.png)

---

Proyek ini dibuat untuk memenuhi tugas mata kuliah Grafika Komputer. Semoga bermanfaat!
