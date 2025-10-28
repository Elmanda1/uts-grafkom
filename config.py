import os
from typing import Dict, Any

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

PAGE_CONFIG: Dict[str, Any] = {
    "page_title": "Belajar Grafika Komputer",
    "page_icon": "🎨",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'https://github.com/yourusername/grafika-komputer',
        'Report a bug': "https://github.com/yourusername/grafika-komputer/issues",
        'About': """
        ## Aplikasi Pembelajaran Grafika Komputer
        
        Aplikasi interaktif untuk mempelajari konsep-konsep fundamental 
        dalam grafika komputer dengan visualisasi real-time.
        
        **Versi:** 1.0.0  
        **Dibuat dengan:** Streamlit + Python
        """
    }
}

# ============================================================================
# CANVAS SETTINGS
# ============================================================================

CANVAS_WIDTH: int = 800
CANVAS_HEIGHT: int = 600
CANVAS_BACKGROUND_COLOR = "#0E1117"
CANVAS_STROKE_COLOR = "#FF4B4B"
CANVAS_FILL_COLOR = "rgba(255, 75, 75, 0.3)"
CANVAS_STROKE_WIDTH = 3

# ============================================================================
# COLOR SCHEMES
# ============================================================================

DEFAULT_COLORS: Dict[str, str] = {
    "background": "#0E1117",
    "background_dark": "#1E2128",
    "background_darker": "#1a1f2b",
    "card_bg": "#262730",
    
    "primary": "#FF4B4B",
    "primary_hover": "#FF6B6B",
    "secondary": "#1E88E5",
    "accent": "#00C853",
    
    "border": "#424242",
    "grid": "#333333",
    "text": "#FAFAFA",
    "text_secondary": "#A0A0A0",
    
    "success": "#00D084",
    "warning": "#FFA726",
    "error": "#FF4B4B",
    "info": "#4A9EFF",
    
    # Algorithm comparison colors
    "algo1": "#4A9EFF",  # Blue - Algoritma pertama
    "algo2": "#FF4B4B",  # Red - Algoritma kedua
    "algo3": "#00D084",  # Green - Algoritma ketiga
}

# Alias untuk backward compatibility
COLORS = DEFAULT_COLORS

# ============================================================================
# PATHS
# ============================================================================

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Assets paths
ASSETS_PATH: Dict[str, str] = {
    "styles": os.path.join(BASE_DIR, "assets", "styles", "custom.css"),
    "data": os.path.join(BASE_DIR, "assets", "data", "sample_objects.json"),
    "images": os.path.join(BASE_DIR, "assets", "images"),
    "fonts": os.path.join(BASE_DIR, "assets", "fonts"),
}

# ============================================================================
# ALGORITHM COMPLEXITIES
# ============================================================================

ALGORITHM_COMPLEXITIES: Dict[str, Dict[str, str]] = {
    # Line Drawing Algorithms
    "DDA": {
        "time": "O(max(|dx|, |dy|))",
        "space": "O(1)",
        "description": "Digital Differential Analyzer",
        "pros": "Sederhana, mudah diimplementasikan",
        "cons": "Menggunakan floating-point (lambat), rounding error"
    },
    "Bresenham Line": {
        "time": "O(max(|dx|, |dy|))",
        "space": "O(1)",
        "description": "Bresenham's Line Algorithm",
        "pros": "Hanya integer arithmetic (cepat), akurat",
        "cons": "Sedikit lebih kompleks dari DDA"
    },
    
    # Circle Drawing Algorithms
    "Midpoint Circle": {
        "time": "O(r)",
        "space": "O(1)",
        "description": "Midpoint Circle Algorithm",
        "pros": "Efisien, hanya integer, 8-way symmetry",
        "cons": "Hanya untuk lingkaran"
    },
    "Bresenham Circle": {
        "time": "O(r)",
        "space": "O(1)",
        "description": "Bresenham's Circle Algorithm",
        "pros": "Sangat efisien, integer-only",
        "cons": "Lebih kompleks dari Midpoint"
    },
    
    # Polygon Filling Algorithms
    "Scanline Fill": {
        "time": "O(n × h)",  # n = edges, h = height
        "space": "O(n)",
        "description": "Scanline Fill Algorithm",
        "pros": "Efisien untuk poligon kompleks, konsisten",
        "cons": "Membutuhkan sorting"
    },
    "Flood Fill": {
        "time": "O(W × H)",
        "space": "O(W × H)",
        "description": "Flood Fill (4-connected)",
        "pros": "Sederhana, bisa fill area irregular",
        "cons": "Rekursif (stack overflow risk), lambat"
    },
    "Boundary Fill": {
        "time": "O(W × H)",
        "space": "O(W × H)",
        "description": "Boundary Fill Algorithm",
        "pros": "Flexible boundary color",
        "cons": "Sama dengan Flood Fill"
    },
    
    # Shading Models
    "Flat Shading": {
        "time": "O(P)",  # P = jumlah poligon
        "space": "O(1)",
        "description": "Flat Shading Model",
        "pros": "Sangat cepat, memory efficient",
        "cons": "Terlihat faceted, tidak smooth"
    },
    "Gouraud Shading": {
        "time": "O(P + V)",  # V = jumlah vertex
        "space": "O(V)",
        "description": "Gouraud Shading (Intensity Interpolation)",
        "pros": "Smooth appearance, cukup cepat",
        "cons": "Specular highlights tidak akurat"
    },
    "Phong Shading": {
        "time": "O(P × F)",  # F = jumlah fragmen/piksel
        "space": "O(F)",
        "description": "Phong Shading (Normal Interpolation)",
        "pros": "Kualitas tertinggi, specular akurat",
        "cons": "Paling lambat, computationally expensive"
    },
}

# ============================================================================
# ALGORITHM SETTINGS
# ============================================================================

# Line drawing algorithms
LINE_ALGORITHMS = {
    "DDA": "Digital Differential Analyzer",
    "Bresenham": "Bresenham's Line Algorithm"
}

# Circle drawing algorithms
CIRCLE_ALGORITHMS = {
    "Midpoint": "Midpoint Circle Algorithm",
    "Bresenham": "Bresenham's Circle Algorithm"
}

# Polygon filling algorithms
FILL_ALGORITHMS = {
    "Scanline": "Scanline Fill Algorithm",
    "Flood": "Flood Fill Algorithm (4-connected)",
    "Boundary": "Boundary Fill Algorithm"
}

# Shading models
SHADING_MODELS = {
    "Flat": "Flat Shading",
    "Gouraud": "Gouraud Shading",
    "Phong": "Phong Shading"
}

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

# Plotly default settings
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'grafika_komputer_plot',
        'height': 800,
        'width': 1200,
        'scale': 2
    }
}

PLOTLY_LAYOUT = {
    'plot_bgcolor': DEFAULT_COLORS["background_dark"],
    'paper_bgcolor': DEFAULT_COLORS["background_dark"],
    'font': {'color': DEFAULT_COLORS["text"]},
    'xaxis': {
        'gridcolor': DEFAULT_COLORS["grid"],
        'zeroline': True,
        'zerolinecolor': DEFAULT_COLORS["border"]
    },
    'yaxis': {
        'gridcolor': DEFAULT_COLORS["grid"],
        'zeroline': True,
        'zerolinecolor': DEFAULT_COLORS["border"]
    },
    'showlegend': True,
    'hovermode': 'closest'
}

# Grid settings
GRID_SIZE = 20
GRID_COLOR = "#333"
SHOW_GRID = True

# ============================================================================
# TRANSFORMATION SETTINGS
# ============================================================================

TRANSFORM_DEFAULTS = {
    'translation': {'tx': 0, 'ty': 0},
    'rotation': {'angle': 0, 'cx': 0, 'cy': 0},
    'scale': {'sx': 1.0, 'sy': 1.0, 'cx': 0, 'cy': 0},
    'shear': {'shx': 0.0, 'shy': 0.0}
}

TRANSFORM_LIMITS = {
    'translation': {'min': -200, 'max': 200},
    'rotation': {'min': -180, 'max': 180},
    'scale': {'min': 0.1, 'max': 3.0},
    'shear': {'min': -2.0, 'max': 2.0}
}

# ============================================================================
# 3D VISUALIZATION SETTINGS
# ============================================================================

CAMERA_SETTINGS = {
    'eye': {'x': 1.5, 'y': 1.5, 'z': 1.5},
    'center': {'x': 0, 'y': 0, 'z': 0},
    'up': {'x': 0, 'y': 0, 'z': 1}
}

LIGHT_SETTINGS = {
    'ambient': 0.3,
    'diffuse': 0.7,
    'specular': 0.9,
    'shininess': 32
}

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Maximum number of points/pixels for visualization
MAX_POINTS = 10000
MAX_PIXELS = 1000000
MAX_POINTS_POLYGON = 20

# Animation settings
ANIMATION_FPS = 30
ANIMATION_DURATION = 2000  # milliseconds

# Line width
DEFAULT_LINE_WIDTH = 2

# ============================================================================
# EDUCATIONAL CONTENT
# ============================================================================

WEEK_TOPICS = {
    1: {
        "title": "Pengantar Grafika Komputer",
        "icon": "📚",
        "difficulty": "Beginner",
        "topics": ["Sejarah", "Aplikasi", "Konsep Dasar", "Pipeline Rendering"]
    },
    2: {
        "title": "Transformasi 2D",
        "icon": "🔄",
        "difficulty": "Beginner",
        "topics": ["Translasi", "Rotasi", "Skala", "Shear", "Matriks"]
    },
    3: {
        "title": "Algoritma Garis & Lingkaran",
        "icon": "📏",
        "difficulty": "Intermediate",
        "topics": ["DDA", "Bresenham Line", "Bresenham Circle", "Midpoint"]
    },
    4: {
        "title": "Polygon Filling",
        "icon": "🎨",
        "difficulty": "Intermediate",
        "topics": ["Scanline", "Flood Fill", "Boundary Fill"]
    },
    5: {
        "title": "Model Warna & Pencahayaan",
        "icon": "🌈",
        "difficulty": "Intermediate",
        "topics": ["RGB", "HSV", "CMYK", "Lighting Models"]
    },
    6: {
        "title": "Shading Models",
        "icon": "💡",
        "difficulty": "Advanced",
        "topics": ["Flat Shading", "Gouraud", "Phong"]
    },
    7: {
        "title": "Texture Mapping",
        "icon": "🖼️",
        "difficulty": "Advanced",
        "topics": ["UV Mapping", "Filtering", "Wrapping"]
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_asset_path(asset_type: str, filename: str = None) -> str:
    """
    Mendapatkan path lengkap untuk asset tertentu.
    
    Args:
        asset_type: Tipe asset ('images', 'styles', 'fonts', 'data')
        filename: Nama file (optional)
    
    Returns:
        Path lengkap ke asset
    """
    base_path = ASSETS_PATH.get(asset_type, BASE_DIR)
    
    if filename:
        return os.path.join(base_path, filename)
    return base_path


def ensure_directories():
    """
    Memastikan semua direktori yang diperlukan ada.
    Membuat direktori jika belum ada.
    """
    directories = [
        "assets/images",
        "assets/styles",
        "assets/fonts",
        "assets/data",
        "algorithms",
        "utils",
        "pages"
    ]
    
    for directory in directories:
        dir_path = os.path.join(BASE_DIR, directory)
        os.makedirs(dir_path, exist_ok=True)


def get_algorithm_info(algo_name: str) -> Dict[str, str]:
    """
    Mendapatkan informasi lengkap tentang algoritma.
    
    Args:
        algo_name: Nama algoritma
    
    Returns:
        Dictionary berisi info kompleksitas dan deskripsi
    """
    return ALGORITHM_COMPLEXITIES.get(algo_name, {
        "time": "N/A",
        "space": "N/A",
        "description": "Unknown Algorithm",
        "pros": "N/A",
        "cons": "N/A"
    })


# Create directories on import
ensure_directories()

# ============================================================================
# DEBUG SETTINGS
# ============================================================================

DEBUG_MODE = False
SHOW_PERFORMANCE_METRICS = True
LOG_TRANSFORMATIONS = False

if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURATION FILE - GRAFIKA KOMPUTER")
    print("=" * 60)
    print(f"\nBase Directory: {BASE_DIR}")
    print(f"\nCanvas Size: {CANVAS_WIDTH}x{CANVAS_HEIGHT}")
    print(f"\nAssets Paths:")
    for key, path in ASSETS_PATH.items():
        print(f"  {key}: {path}")
    print(f"\nTotal Algorithms: {len(ALGORITHM_COMPLEXITIES)}")
    print("\n" + "=" * 60)