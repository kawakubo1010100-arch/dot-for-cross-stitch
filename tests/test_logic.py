import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from PIL import Image
from io import BytesIO

from logic import process_image, _estimate_thread_length, prepare_source, generate_pattern


def _make_test_image(w: int = 40, h: int = 30, n_colors: int = 4) -> bytes:
    img = Image.new("RGB", (w, h))
    pixels = img.load()
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    for y in range(h):
        for x in range(w):
            pixels[x, y] = colors[(x // (w // n_colors)) % n_colors]
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_process_image_basic():
    image_bytes = _make_test_image()
    pattern = process_image(
        image_bytes=image_bytes,
        width_stitches=20,
        max_colors=4,
        fabric_count=14,
        strand_count=3,
        title="テスト",
    )
    assert pattern.grid.shape[1] == 20
    assert len(pattern.colors) == 4
    assert len(pattern.symbols) == 4
    assert len(pattern.thread_lengths) == 4
    assert pattern.fabric_count == 14


def test_finished_size():
    image_bytes = _make_test_image()
    pattern = process_image(
        image_bytes=image_bytes,
        width_stitches=28,
        max_colors=4,
        fabric_count=14,
    )
    w_cm, h_cm = pattern.finished_size_cm
    assert abs(w_cm - 5.1) < 0.2


def test_thread_length_estimation():
    length = _estimate_thread_length(100, 14, 3)
    assert length > 0
    assert length == round(length * 2) / 2


def test_color_count_respected():
    image_bytes = _make_test_image(n_colors=4)
    pattern = process_image(
        image_bytes=image_bytes,
        width_stitches=20,
        max_colors=2,
    )
    unique = len(np.unique(pattern.grid))
    assert unique <= 2
