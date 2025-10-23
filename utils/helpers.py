"""
File Helper untuk Fungsi-Fungsi Umum.

Berisi fungsi-fungsi bantuan yang digunakan di berbagai bagian aplikasi,
termasuk decorator untuk melacak performa, fungsi untuk memuat CSS, dll.
"""

import time
import streamlit as st
from functools import wraps
from typing import Callable, Any, Dict

def performance_tracker(func: Callable) -> Callable:
    """
    Decorator untuk mengukur waktu eksekusi dan menghitung operasi dasar.

    Args:
        func (Callable): Fungsi yang akan diukur performanya.

    Returns:
        Callable: Wrapper yang mengembalikan hasil fungsi beserta metrik performa.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        """
        Wrapper internal.
        """
        # Inisialisasi penghitung operasi (jika ada)
        operation_count = 0
        kwargs['operation_counter'] = {'count': 0}

        # Mengukur waktu eksekusi
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        execution_time_ms = (end_time - start_time) * 1000
        operation_count = kwargs['operation_counter']['count']

        # Menghapus counter dari kwargs sebelum dikembalikan
        del kwargs['operation_counter']

        # Mengembalikan dictionary yang berisi hasil dan metrik
        return {
            "result": result,
            "execution_time_ms": execution_time_ms,
            "operations": operation_count,
        }

    return wrapper

def load_css(file_path: str):
    """
    Memuat file CSS kustom ke dalam aplikasi Streamlit.

    Args:
        file_path (str): Path menuju file CSS.
    """
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"File CSS tidak ditemukan di path: {file_path}")
    except Exception as e:
        st.error(f"Gagal memuat CSS: {e}")

def get_session_state(variable_name: str, default_value: Any) -> Any:
    """
    Mengambil nilai dari session state atau menginisialisasi dengan nilai default.

    Args:
        variable_name (str): Nama variabel di session state.
        default_value (Any): Nilai default jika variabel belum ada.

    Returns:
        Any: Nilai dari session state.
    """
    if variable_name not in st.session_state:
        st.session_state[variable_name] = default_value
    return st.session_state[variable_name]
