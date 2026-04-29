from __future__ import annotations

import io

import numpy as np
from PIL import Image
from scipy.ndimage import label


def _flood_select(
    pixels: np.ndarray,
    start_x: int,
    start_y: int,
    tolerance: int,
) -> np.ndarray:
    h, w = pixels.shape[:2]
    target = pixels[start_y, start_x].astype(np.int32)
    diff = np.abs(pixels.astype(np.int32) - target).max(axis=2)
    similar = diff <= tolerance
    labels_arr, _ = label(similar)
    target_label = labels_arr[start_y, start_x]
    if target_label == 0:
        region = np.zeros_like(similar, dtype=bool)
        region[start_y, start_x] = True
        return region
    return labels_arr == target_label


def flood_fill_toggle(
    pixels: np.ndarray,
    mask: np.ndarray,
    x: int,
    y: int,
    tolerance: int = 0,
) -> np.ndarray:
    h, w = pixels.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        return mask.copy()

    region = _flood_select(pixels, x, y, tolerance)
    new_mask = mask.copy()
    if mask[y, x]:
        new_mask &= ~region
    else:
        new_mask |= region
    return new_mask


def flood_fill_add(
    pixels: np.ndarray,
    mask: np.ndarray,
    x: int,
    y: int,
    tolerance: int = 0,
) -> np.ndarray:
    h, w = pixels.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        return mask.copy()
    region = _flood_select(pixels, x, y, tolerance)
    return mask | region


def flood_fill_remove(
    pixels: np.ndarray,
    mask: np.ndarray,
    x: int,
    y: int,
    tolerance: int = 0,
) -> np.ndarray:
    h, w = pixels.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        return mask.copy()
    region = _flood_select(pixels, x, y, tolerance)
    return mask & ~region


def apply_rect(
    mask: np.ndarray,
    x0: int, y0: int, x1: int, y1: int,
    value: bool,
) -> np.ndarray:
    h, w = mask.shape
    x0i, x1i = sorted([int(x0), int(x1)])
    y0i, y1i = sorted([int(y0), int(y1)])
    x0i = max(0, min(w, x0i))
    x1i = max(0, min(w, x1i))
    y0i = max(0, min(h, y0i))
    y1i = max(0, min(h, y1i))
    new_mask = mask.copy()
    new_mask[y0i:y1i, x0i:x1i] = value
    return new_mask


def set_pixel(mask: np.ndarray, x: int, y: int, value: bool) -> np.ndarray:
    h, w = mask.shape
    if not (0 <= x < w and 0 <= y < h):
        return mask.copy()
    new_mask = mask.copy()
    new_mask[y, x] = value
    return new_mask


def auto_mask_edges(
    pixels: np.ndarray,
    mask: np.ndarray,
    tolerance: int = 15,
) -> np.ndarray:
    h, w = pixels.shape[:2]
    new_mask = mask.copy()

    visited = np.zeros((h, w), dtype=bool)
    edge_coords = []
    for x in range(w):
        edge_coords.append((x, 0))
        edge_coords.append((x, h - 1))
    for y in range(h):
        edge_coords.append((0, y))
        edge_coords.append((w - 1, y))

    for x, y in edge_coords:
        if visited[y, x]:
            continue
        region = _flood_select(pixels, x, y, tolerance)
        new_mask |= region
        visited |= region

    return new_mask


def toggle_pixel(mask: np.ndarray, x: int, y: int) -> np.ndarray:
    h, w = mask.shape
    if not (0 <= x < w and 0 <= y < h):
        return mask.copy()
    new_mask = mask.copy()
    new_mask[y, x] = not new_mask[y, x]
    return new_mask


def render_editor_view(
    pixels: np.ndarray,
    mask: np.ndarray,
    scale: int = 4,
) -> Image.Image:
    h, w = pixels.shape[:2]
    img = pixels.copy()
    overlay = np.zeros_like(img)
    overlay[..., 0] = 255
    img_out = np.where(
        mask[..., None],
        (img * 0.3 + overlay * 0.7).astype(np.uint8),
        img,
    )

    pil_img = Image.fromarray(img_out)
    if scale != 1:
        pil_img = pil_img.resize(
            (w * scale, h * scale), Image.NEAREST
        )
    return pil_img


def mask_to_png_bytes(mask: np.ndarray) -> bytes:
    img = Image.fromarray((mask.astype(np.uint8) * 255), mode="L")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def png_bytes_to_mask(
    png_bytes: bytes, expected_shape: tuple[int, int]
) -> np.ndarray | None:
    try:
        img = Image.open(io.BytesIO(png_bytes)).convert("L")
        arr = np.array(img)
        if arr.shape != expected_shape:
            img = img.resize(
                (expected_shape[1], expected_shape[0]), Image.NEAREST
            )
            arr = np.array(img)
        return arr > 127
    except Exception:
        return None


def apply_mask_preview(
    pixels: np.ndarray, mask: np.ndarray
) -> Image.Image:
    img = pixels.copy()
    img[mask] = (255, 255, 255)
    return Image.fromarray(img)
