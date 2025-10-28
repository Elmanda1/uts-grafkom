"""
algorithms/transformations.py

Implementasi algoritma transformasi geometri 2D menggunakan matriks.
"""

import numpy as np
from typing import List, Tuple

def create_translation_matrix(tx: float, ty: float) -> np.ndarray:
    """
    Membuat matriks translasi 2D.
    
    Args:
        tx: Perpindahan di sumbu X
        ty: Perpindahan di sumbu Y
    
    Returns:
        Matriks 3x3 untuk translasi
    """
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)


def create_rotation_matrix(angle_deg: float, cx: float = 0, cy: float = 0) -> np.ndarray:
    """
    Membuat matriks rotasi 2D terhadap titik (cx, cy).
    
    Args:
        angle_deg: Sudut rotasi dalam derajat (counter-clockwise)
        cx: X coordinate dari pusat rotasi
        cy: Y coordinate dari pusat rotasi
    
    Returns:
        Matriks 3x3 untuk rotasi
    """
    # Convert ke radian
    angle_rad = np.radians(angle_deg)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    
    # Rotasi terhadap origin
    rotation = np.array([
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ], dtype=float)
    
    # Jika pusat rotasi bukan origin, gunakan composite transformation
    if cx != 0 or cy != 0:
        # T(cx, cy) × R(θ) × T(-cx, -cy)
        t1 = create_translation_matrix(-cx, -cy)
        t2 = create_translation_matrix(cx, cy)
        rotation = combine_transformations([t1, rotation, t2])
    
    return rotation


def create_scale_matrix(sx: float, sy: float, cx: float = 0, cy: float = 0) -> np.ndarray:
    """
    Membuat matriks skala 2D terhadap titik (cx, cy).
    
    Args:
        sx: Faktor skala di sumbu X
        sy: Faktor skala di sumbu Y
        cx: X coordinate dari pusat skala
        cy: Y coordinate dari pusat skala
    
    Returns:
        Matriks 3x3 untuk skala
    """
    # Skala terhadap origin
    scale = np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ], dtype=float)
    
    # Jika pusat skala bukan origin
    if cx != 0 or cy != 0:
        # T(cx, cy) × S(sx, sy) × T(-cx, -cy)
        t1 = create_translation_matrix(-cx, -cy)
        t2 = create_translation_matrix(cx, cy)
        scale = combine_transformations([t1, scale, t2])
    
    return scale


def create_shear_matrix(shx: float, shy: float) -> np.ndarray:
    """
    Membuat matriks shear 2D.
    
    Args:
        shx: Faktor shear di sumbu X (x' = x + shx * y)
        shy: Faktor shear di sumbu Y (y' = y + shy * x)
    
    Returns:
        Matriks 3x3 untuk shear
    """
    return np.array([
        [1,   shx, 0],
        [shy, 1,   0],
        [0,   0,   1]
    ], dtype=float)


def create_reflection_matrix(axis: str = 'x') -> np.ndarray:
    """
    Membuat matriks refleksi (pencerminan) 2D.
    
    Args:
        axis: Sumbu refleksi ('x', 'y', atau 'origin')
    
    Returns:
        Matriks 3x3 untuk refleksi
    """
    if axis == 'x':
        # Refleksi terhadap sumbu X
        return np.array([
            [1,  0, 0],
            [0, -1, 0],
            [0,  0, 1]
        ], dtype=float)
    elif axis == 'y':
        # Refleksi terhadap sumbu Y
        return np.array([
            [-1, 0, 0],
            [0,  1, 0],
            [0,  0, 1]
        ], dtype=float)
    else:  # origin
        # Refleksi terhadap origin (180° rotation)
        return np.array([
            [-1,  0, 0],
            [0,  -1, 0],
            [0,   0, 1]
        ], dtype=float)


def combine_transformations(matrices: List[np.ndarray]) -> np.ndarray:
    """
    Menggabungkan beberapa matriks transformasi.
    
    Transformasi diterapkan dari kanan ke kiri:
    M_final = M_n × ... × M_2 × M_1
    
    Args:
        matrices: List matriks transformasi (urutan dari kiri ke kanan)
    
    Returns:
        Matriks hasil kombinasi
    
    Example:
        >>> # Rotasi 45° lalu translasi (100, 50)
        >>> m1 = create_rotation_matrix(45)
        >>> m2 = create_translation_matrix(100, 50)
        >>> m_combined = combine_transformations([m1, m2])
    """
    if not matrices:
        return np.identity(3)
    
    result = matrices[0]
    for matrix in matrices[1:]:
        result = matrix @ result  # Matrix multiplication
    
    return result


def apply_transformation(points: List[Tuple[float, float]], 
                        matrix: np.ndarray) -> List[Tuple[float, float]]:
    """
    Menerapkan transformasi matriks ke sekumpulan titik.
    
    Args:
        points: List of (x, y) coordinates
        matrix: Matriks transformasi 3x3
    
    Returns:
        List titik yang telah ditransformasi
    
    Example:
        >>> points = [(0, 0), (100, 0), (100, 100)]
        >>> matrix = create_translation_matrix(50, 30)
        >>> transformed = apply_transformation(points, matrix)
        >>> print(transformed)  # [(50, 30), (150, 30), (150, 130)]
    """
    # Convert to homogeneous coordinates
    points_array = np.array(points)
    ones = np.ones((len(points), 1))
    homogeneous = np.hstack([points_array, ones])  # [x, y, 1]
    
    # Apply transformation: P' = M × P^T
    transformed = (matrix @ homogeneous.T).T
    
    # Convert back to 2D coordinates (remove homogeneous coordinate)
    result = transformed[:, :2].tolist()
    
    return result


def apply_transformation_to_point(point: Tuple[float, float], 
                                  matrix: np.ndarray) -> Tuple[float, float]:
    """
    Menerapkan transformasi matriks ke satu titik.
    
    Args:
        point: (x, y) coordinate
        matrix: Matriks transformasi 3x3
    
    Returns:
        Titik yang telah ditransformasi
    """
    # Convert to homogeneous coordinate
    homogeneous = np.array([point[0], point[1], 1])
    
    # Apply transformation
    transformed = matrix @ homogeneous
    
    # Return as tuple (x, y)
    return (transformed[0], transformed[1])


def get_transformation_info(matrix: np.ndarray) -> dict:
    """
    Mengekstrak informasi dari matriks transformasi.
    
    Args:
        matrix: Matriks transformasi 3x3
    
    Returns:
        Dictionary berisi informasi transformasi
    """
    info = {
        'translation': (matrix[0, 2], matrix[1, 2]),
        'has_rotation': not np.allclose(matrix[:2, :2], np.eye(2)),
        'has_scale': False,
        'determinant': np.linalg.det(matrix[:2, :2])
    }
    
    # Check for scaling
    scale_x = np.linalg.norm(matrix[:2, 0])
    scale_y = np.linalg.norm(matrix[:2, 1])
    
    if not np.isclose(scale_x, 1.0) or not np.isclose(scale_y, 1.0):
        info['has_scale'] = True
        info['scale'] = (scale_x, scale_y)
    
    return info


def inverse_transformation(matrix: np.ndarray) -> np.ndarray:
    """
    Menghitung invers dari matriks transformasi.
    
    Berguna untuk "membatalkan" transformasi.
    
    Args:
        matrix: Matriks transformasi 3x3
    
    Returns:
        Matriks invers
    """
    try:
        return np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        raise ValueError("Matriks tidak memiliki invers (singular matrix)")


# ============================================================================
# HELPER FUNCTIONS UNTUK TRANSFORMASI KHUSUS
# ============================================================================

def create_rotation_around_point(angle_deg: float, 
                                 point: Tuple[float, float]) -> np.ndarray:
    """
    Shortcut untuk rotasi terhadap titik tertentu.
    
    Args:
        angle_deg: Sudut rotasi dalam derajat
        point: (x, y) titik pusat rotasi
    
    Returns:
        Matriks transformasi komposit
    """
    return create_rotation_matrix(angle_deg, point[0], point[1])


def create_scale_around_point(sx: float, sy: float, 
                              point: Tuple[float, float]) -> np.ndarray:
    """
    Shortcut untuk skala terhadap titik tertentu.
    
    Args:
        sx: Faktor skala X
        sy: Faktor skala Y
        point: (x, y) titik pusat skala
    
    Returns:
        Matriks transformasi komposit
    """
    return create_scale_matrix(sx, sy, point[0], point[1])


def transform_rectangle(x: float, y: float, width: float, height: float,
                        matrix: np.ndarray) -> List[Tuple[float, float]]:
    """
    Mentransformasi rectangle menjadi 4 titik sudut.
    
    Args:
        x, y: Posisi top-left corner
        width, height: Dimensi rectangle
        matrix: Matriks transformasi
    
    Returns:
        List 4 titik sudut yang telah ditransformasi
    """
    corners = [
        (x, y),                    # Top-left
        (x + width, y),           # Top-right
        (x + width, y + height),  # Bottom-right
        (x, y + height)           # Bottom-left
    ]
    
    return apply_transformation(corners, matrix)


def calculate_bounding_box(points: List[Tuple[float, float]]) -> dict:
    """
    Menghitung bounding box dari sekumpulan titik.
    
    Args:
        points: List of (x, y) coordinates
    
    Returns:
        Dictionary dengan keys: min_x, max_x, min_y, max_y, width, height
    """
    if not points:
        return None
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    return {
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y,
        'width': max_x - min_x,
        'height': max_y - min_y,
        'center': ((min_x + max_x) / 2, (min_y + max_y) / 2)
    }


def calculate_centroid(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Menghitung centroid (titik tengah) dari sekumpulan titik.
    
    Args:
        points: List of (x, y) coordinates
    
    Returns:
        (cx, cy) koordinat centroid
    """
    if not points:
        return (0, 0)
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    return (sum(xs) / len(xs), sum(ys) / len(ys))


# ============================================================================
# DEMO & TESTING FUNCTIONS
# ============================================================================

def demo_transformations():
    """
    Demonstrasi penggunaan fungsi-fungsi transformasi.
    """
    print("=" * 60)
    print("DEMO: Transformasi Geometri 2D")
    print("=" * 60)
    
    # Original points (square)
    square = [(0, 0), (100, 0), (100, 100), (0, 100)]
    print(f"\n Original Square: {square}")
    
    # 1. Translation
    print("\n1. TRANSLASI (50, 30)")
    m_trans = create_translation_matrix(50, 30)
    trans_square = apply_transformation(square, m_trans)
    print(f"   Result: {trans_square}")
    
    # 2. Rotation
    print("\n2. ROTASI 45° (terhadap origin)")
    m_rot = create_rotation_matrix(45)
    rot_square = apply_transformation(square, m_rot)
    print(f"   Result: {[(round(x, 2), round(y, 2)) for x, y in rot_square]}")
    
    # 3. Scaling
    print("\n3. SKALA (1.5, 1.5)")
    m_scale = create_scale_matrix(1.5, 1.5)
    scaled_square = apply_transformation(square, m_scale)
    print(f"   Result: {scaled_square}")
    
    # 4. Shear
    print("\n4. SHEAR (0.5, 0)")
    m_shear = create_shear_matrix(0.5, 0)
    sheared_square = apply_transformation(square, m_shear)
    print(f"   Result: {sheared_square}")
    
    # 5. Composite transformation
    print("\n5. KOMPOSIT: Rotasi 30° → Skala 1.2 → Translasi (100, 50)")
    m1 = create_rotation_matrix(30)
    m2 = create_scale_matrix(1.2, 1.2)
    m3 = create_translation_matrix(100, 50)
    m_composite = combine_transformations([m1, m2, m3])
    composite_square = apply_transformation(square, m_composite)
    print(f"   Result: {[(round(x, 2), round(y, 2)) for x, y in composite_square]}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Run demo
    demo_transformations()