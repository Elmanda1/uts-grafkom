"""
Komponen untuk Menampilkan Kode dan Metrik Performa.

Berisi fungsi-fungsi untuk menampilkan blok kode dengan syntax highlighting,
metrik performa (waktu eksekusi, kompleksitas), dan perbandingan antar algoritma.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any

from config import ALGORITHM_COMPLEXITIES

def show_code(function_name: str, code_string: str):
    """
    Menampilkan blok kode yang bisa di-expand/collapse dengan syntax highlighting.

    Args:
        function_name (str): Nama fungsi atau judul untuk blok kode.
        code_string (str): String yang berisi kode Python untuk ditampilkan.
    """
    with st.expander(f"Lihat Kode: {function_name}", expanded=False):
        st.code(code_string, language='python')
        # st.code() secara internal sudah cukup baik, tombol copy ada by default.

def show_performance_metrics(
    algorithm_name: str,
    execution_time_ms: float,
    operations: int,
    extra_metrics: Dict[str, Any] = None
):
    """
    Menampilkan tabel metrik performa untuk sebuah algoritma.

    Args:
        algorithm_name (str): Nama algoritma.
        execution_time_ms (float): Waktu eksekusi dalam milidetik.
        operations (int): Jumlah operasi dasar atau piksel yang digambar.
        extra_metrics (Dict[str, Any], optional): Metrik tambahan (misal: memori).
    """
    st.subheader(f"Metrik Performa: {algorithm_name}")

    # Mengambil data kompleksitas dari config
    complexity = ALGORITHM_COMPLEXITIES.get(algorithm_name, {"time": "N/A", "space": "N/A"})

    data = {
        "Metrik": [
            "Waktu Eksekusi (ms)",
            "Kompleksitas Waktu (Big O)",
            "Kompleksitas Ruang (Big O)",
            "Jumlah Operasi/Piksel"
        ],
        "Nilai": [
            f"{execution_time_ms:.4f}",
            complexity['time'],
            complexity['space'],
            f"{operations:,}"
        ]
    }

    if extra_metrics:
        for key, value in extra_metrics.items():
            data["Metrik"].append(key)
            data["Nilai"].append(value)

    df = pd.DataFrame(data)
    st.table(df.set_index("Metrik"))

def compare_algorithms(algo_metrics: List[Dict[str, Any]]):
    """
    Membuat tabel perbandingan untuk beberapa metrik algoritma.

    Args:
        algo_metrics (List[Dict[str, Any]]): List dari dictionary, di mana setiap
            dictionary berisi metrik untuk satu algoritma.
            Contoh: [{'name': 'DDA', 'time': 0.1, 'ops': 100}, ...]
    """
    if not algo_metrics or len(algo_metrics) < 2:
        st.info("Membutuhkan setidaknya dua algoritma untuk dibandingkan.")
        return

    st.subheader("Perbandingan Algoritma")

    # Menyiapkan data untuk DataFrame
    data_for_df = {}
    headers = ["Metrik"] + [m['name'] for m in algo_metrics]

    # Inisialisasi data
    data_for_df["Metrik"] = [
        "Waktu Eksekusi (ms)",
        "Jumlah Operasi/Piksel",
        "Kompleksitas Waktu",
        "Kompleksitas Ruang"
    ]

    for metric in algo_metrics:
        name = metric['name']
        complexity = ALGORITHM_COMPLEXITIES.get(name, {"time": "N/A", "space": "N/A"})
        data_for_df[name] = [
            f"{metric.get('time', 0):.4f}",
            f"{metric.get('ops', 0):,}",
            complexity['time'],
            complexity['space']
        ]

    df = pd.DataFrame(data_for_df)
    st.table(df.set_index("Metrik"))
