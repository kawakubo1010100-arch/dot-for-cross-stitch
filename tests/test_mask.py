import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from PIL import Image
from io import BytesIO

from logic import prepare_source, generate_pattern, MASK_VALUE
from background_editor import (
    flood_fill_toggle, auto_mask_edges, toggle_pixel,
    mask_to_png_bytes, png_bytes_to_mask,
)


def _make_test_image(w: int = 40, h: int = 30) -> bytes:
    img = Image.new("RGB", (w, h))
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            if x < w // 2:
                pixels[x, y] = (255, 0, 0)
            else:
                pixels[x, y] = (0, 0, 255)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_prepare_source_resizes():
    image_bytes = _make_test_image(800, 600)
    src = prepare_source(image_bytes, max_dim=300)
    h, w = src.shape
    assert max(h, w) == 300


def test_prepare_source_no_resize_small():
    image_bytes = _make_test_image(100, 80)
    src = prepare_source(image_bytes, max_dim=300)
    assert src.shape == (80, 100)


def test_generate_pattern_basic():
    image_bytes = _make_test_image()
    src = prepare_source(image_bytes)
    pattern = generate_pattern(
        source=src,
        width_stitches=20,
        max_colors=4,
    )
    assert pattern.width_stitches == 20


def test_mask_excludes_pixels():
    image_bytes = _make_test_image()
    src = prepare_source(image_bytes)
    h, w = src.shape
    src.mask[:, : w // 2] = True

    pattern = generate_pattern(
        source=src,
        width_stitches=20,
        max_colors=4,
    )

    masked_count = (pattern.grid == MASK_VALUE).sum()
    assert masked_count > 0


def test_full_mask_returns_empty_pattern():
    image_bytes = _make_test_image()
    src = prepare_source(image_bytes)
    src.mask[:, :] = True

    pattern = generate_pattern(
        source=src,
        width_stitches=10,
        max_colors=4,
    )
    assert len(pattern.colors) == 0


def test_flood_fill_toggle():
    pixels = np.zeros((10, 10, 3), dtype=np.uint8)
    pixels[:, :5] = (255, 0, 0)
    pixels[:, 5:] = (0, 0, 255)
    mask = np.zeros((10, 10), dtype=bool)

    new_mask = flood_fill_toggle(pixels, mask, 2, 2, tolerance=0)
    assert new_mask[:, :5].all()
    assert not new_mask[:, 5:].any()

    new_mask = flood_fill_toggle(pixels, new_mask, 2, 2, tolerance=0)
    assert not new_mask.any()


def test_auto_mask_edges():
    pixels = np.zeros((10, 10, 3), dtype=np.uint8)
    pixels[:, :] = (200, 200, 200)
    pixels[3:7, 3:7] = (50, 50, 50)
    mask = np.zeros((10, 10), dtype=bool)

    result = auto_mask_edges(pixels, mask, tolerance=10)
    assert result[0, 0]
    assert result[9, 9]
    assert not result[5, 5]


def test_toggle_pixel():
    mask = np.zeros((5, 5), dtype=bool)
    new_mask = toggle_pixel(mask, 2, 3)
    assert new_mask[3, 2] == True
    new_mask = toggle_pixel(new_mask, 2, 3)
    assert new_mask[3, 2] == False


def test_mask_png_roundtrip():
    mask = np.zeros((20, 30), dtype=bool)
    mask[5:15, 10:20] = True
    png_bytes = mask_to_png_bytes(mask)
    restored = png_bytes_to_mask(png_bytes, (20, 30))
    assert restored is not None
    assert (restored == mask).all()


def test_i18n_translations():
    from i18n import t, TRANSLATIONS
    assert t("title", "ja") == "クロスステッチ図案メーカー"
    assert t("title", "en") == "Cross Stitch Pattern Maker"
    for key in TRANSLATIONS["ja"]:
        assert key in TRANSLATIONS["en"], f"Missing English translation for: {key}"


def test_i18n_fallback():
    from i18n import t
    assert t("nonexistent_key", "ja") == "nonexistent_key"
    assert t("title", "fr") == "Cross Stitch Pattern Maker"


def test_olympus_nested_format():
    from olympus_convert import dmc_to_olympus
    entry = dmc_to_olympus("310")
    assert entry is not None
    assert entry.number == "900"
    if entry.name_ja:
        assert isinstance(entry.name_ja, str)
