from __future__ import annotations

import math
from dataclasses import dataclass
from io import BytesIO

import numpy as np
from PIL import Image
from sklearn.cluster import MiniBatchKMeans

from dmc_colors import DMCColor, find_nearest_n, rgb_to_lab
from symbols import assign_symbols

MASK_VALUE = -1
SOURCE_MAX_DIM = 300


@dataclass
class SourceData:
    pixels: np.ndarray
    mask: np.ndarray

    @property
    def shape(self) -> tuple[int, int]:
        return (self.pixels.shape[0], self.pixels.shape[1])


@dataclass
class PatternData:
    grid: np.ndarray
    colors: list[DMCColor]
    symbols: list[str]
    thread_lengths: list[float]
    width_stitches: int
    height_stitches: int
    fabric_count: int
    strand_count: int
    title: str
    substitutes: list[bool] = None  # type: ignore
    thread_system: str = "both"

    def __post_init__(self) -> None:
        if self.substitutes is None:
            self.substitutes = [False] * len(self.colors)

    @property
    def canvas_size_cm(self) -> tuple[float, float]:
        w = self.width_stitches / self.fabric_count * 2.54
        h = self.height_stitches / self.fabric_count * 2.54
        return (round(w, 1), round(h, 1))

    @property
    def finished_size_cm(self) -> tuple[float, float]:
        return self.canvas_size_cm

    @property
    def drawn_bbox_stitches(self) -> tuple[int, int]:
        drawn = self.grid >= 0
        if not drawn.any():
            return (0, 0)
        rows = np.any(drawn, axis=1)
        cols = np.any(drawn, axis=0)
        rmin, rmax = int(np.argmax(rows)), int(len(rows) - 1 - np.argmax(rows[::-1]))
        cmin, cmax = int(np.argmax(cols)), int(len(cols) - 1 - np.argmax(cols[::-1]))
        return (cmax - cmin + 1, rmax - rmin + 1)

    @property
    def drawn_size_cm(self) -> tuple[float, float]:
        dw, dh = self.drawn_bbox_stitches
        w = dw / self.fabric_count * 2.54
        h = dh / self.fabric_count * 2.54
        return (round(w, 1), round(h, 1))


def prepare_source(image_bytes: bytes, max_dim: int = SOURCE_MAX_DIM) -> SourceData:
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    w, h = img.size
    if max(w, h) > max_dim:
        if w >= h:
            new_w = max_dim
            new_h = max(1, round(h * max_dim / w))
        else:
            new_h = max_dim
            new_w = max(1, round(w * max_dim / h))
        img = img.resize((new_w, new_h), Image.LANCZOS)
    pixels = np.array(img)
    mask = np.zeros(pixels.shape[:2], dtype=bool)
    return SourceData(pixels=pixels, mask=mask)


def _resize_with_mask(
    source: SourceData,
    width_stitches: int | None,
    height_stitches: int | None,
) -> tuple[np.ndarray, np.ndarray]:
    src_h, src_w = source.shape
    aspect = src_w / src_h

    if width_stitches and height_stitches:
        target_w, target_h = width_stitches, height_stitches
    elif width_stitches:
        target_w = width_stitches
        target_h = max(1, round(width_stitches / aspect))
    elif height_stitches:
        target_h = height_stitches
        target_w = max(1, round(height_stitches * aspect))
    else:
        target_w, target_h = min(80, src_w), min(80, src_h)

    pixel_img = Image.fromarray(source.pixels)
    pixel_img = pixel_img.resize((target_w, target_h), Image.LANCZOS)
    pixels = np.array(pixel_img)

    mask_img = Image.fromarray(source.mask.astype(np.uint8) * 255)
    mask_img = mask_img.resize((target_w, target_h), Image.NEAREST)
    mask = (np.array(mask_img) > 127).astype(bool)

    return pixels, mask


def _quantize_colors(
    pixels: np.ndarray,
    max_colors: int,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    h, w, _ = pixels.shape
    flat = pixels.reshape(-1, 3).astype(np.float64)

    if mask is not None:
        flat_mask = mask.reshape(-1).astype(bool)
        active_idx = np.where(~flat_mask)[0]
    else:
        active_idx = np.arange(len(flat))

    if len(active_idx) == 0:
        grid = np.full((h, w), MASK_VALUE, dtype=np.int32)
        return grid, np.array([], dtype=np.uint8).reshape(0, 3)

    active_flat = flat[active_idx]
    lab_active = np.array(
        [rgb_to_lab(int(r), int(g), int(b)) for r, g, b in active_flat]
    )

    n_clusters = min(max_colors, len(active_idx))
    kmeans = MiniBatchKMeans(
        n_clusters=n_clusters, random_state=42, batch_size=1024, n_init=3
    )
    active_labels = kmeans.fit_predict(lab_active)

    centers_rgb = []
    for ci in range(n_clusters):
        cluster_pixels = active_flat[active_labels == ci]
        if len(cluster_pixels) > 0:
            centers_rgb.append(cluster_pixels.mean(axis=0).astype(int))
        else:
            centers_rgb.append(np.array([128, 128, 128]))

    centers_rgb_arr = np.array(centers_rgb, dtype=np.uint8)

    full_labels = np.full(len(flat), MASK_VALUE, dtype=np.int32)
    full_labels[active_idx] = active_labels
    grid = full_labels.reshape(h, w)
    return grid, centers_rgb_arr


def _estimate_thread_length(
    stitch_count: int, fabric_count: int, strand_count: int
) -> float:
    cell_mm = 25.4 / fabric_count
    per_stitch_mm = 4 * cell_mm * (strand_count / 2)
    total_mm = stitch_count * per_stitch_mm * 1.2
    meters = total_mm / 1000
    return math.ceil(meters * 2) / 2


def generate_pattern(
    source: SourceData,
    width_stitches: int | None = 80,
    height_stitches: int | None = None,
    max_colors: int = 10,
    fabric_count: int = 14,
    strand_count: int = 3,
    title: str = "クロスステッチ図案",
    thread_system: str = "both",
) -> PatternData:
    pixels, mask = _resize_with_mask(source, width_stitches, height_stitches)
    actual_h, actual_w = pixels.shape[:2]

    grid, centers_rgb = _quantize_colors(pixels, max_colors, mask=mask)
    n_actual_colors = len(centers_rgb)

    color_tuples = [(int(c[0]), int(c[1]), int(c[2])) for c in centers_rgb]
    if color_tuples:
        dmc_colors, substitutes = find_nearest_n(
            color_tuples, thread_system=thread_system
        )
    else:
        dmc_colors, substitutes = [], []

    syms = assign_symbols(grid, n_actual_colors)

    thread_lengths = []
    for i in range(n_actual_colors):
        count = int(np.sum(grid == i))
        length = _estimate_thread_length(count, fabric_count, strand_count)
        thread_lengths.append(length)

    return PatternData(
        grid=grid,
        colors=dmc_colors,
        symbols=syms,
        thread_lengths=thread_lengths,
        width_stitches=actual_w,
        height_stitches=actual_h,
        fabric_count=fabric_count,
        strand_count=strand_count,
        title=title,
        substitutes=substitutes,
        thread_system=thread_system,
    )


def process_image(
    image_bytes: bytes,
    width_stitches: int | None = 80,
    height_stitches: int | None = None,
    max_colors: int = 10,
    fabric_count: int = 14,
    strand_count: int = 3,
    title: str = "クロスステッチ図案",
    mask: np.ndarray | None = None,
    pre_resized_pixels: np.ndarray | None = None,
) -> PatternData:
    if pre_resized_pixels is not None:
        pixels = pre_resized_pixels
        actual_h, actual_w = pixels.shape[:2]
    else:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        orig_w, orig_h = img.size
        aspect = orig_w / orig_h
        if width_stitches and height_stitches:
            tw, th = width_stitches, height_stitches
        elif width_stitches:
            tw = width_stitches
            th = max(1, round(width_stitches / aspect))
        elif height_stitches:
            th = height_stitches
            tw = max(1, round(height_stitches * aspect))
        else:
            tw, th = min(80, orig_w), min(80, orig_h)
        img = img.resize((tw, th), Image.LANCZOS)
        actual_w, actual_h = img.size
        pixels = np.array(img)

    grid, centers_rgb = _quantize_colors(pixels, max_colors, mask=mask)
    n_actual_colors = len(centers_rgb)

    color_tuples = [(int(c[0]), int(c[1]), int(c[2])) for c in centers_rgb]
    if color_tuples:
        dmc_colors, substitutes = find_nearest_n(color_tuples)
    else:
        dmc_colors, substitutes = [], []

    syms = assign_symbols(grid, n_actual_colors)

    thread_lengths = []
    for i in range(n_actual_colors):
        count = int(np.sum(grid == i))
        length = _estimate_thread_length(count, fabric_count, strand_count)
        thread_lengths.append(length)

    return PatternData(
        grid=grid,
        colors=dmc_colors,
        symbols=syms,
        thread_lengths=thread_lengths,
        width_stitches=actual_w,
        height_stitches=actual_h,
        fabric_count=fabric_count,
        strand_count=strand_count,
        title=title,
        substitutes=substitutes,
    )
