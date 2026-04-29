from __future__ import annotations

import numpy as np

SYMBOL_POOL: list[str] = [
    "■", "×", "◆", "△", "●", "★", "▲", "□", "○", "◇",
    "▽", "♦", "♠", "♣", "♥", "⊕", "⊗", "⊞", "▣", "◉",
    "⊠", "⊡", "◎", "▪", "▫", "◘", "◙", "⬟", "⬡", "⊙",
]


def assign_symbols(
    grid: np.ndarray, n_colors: int
) -> list[str]:
    valid = grid[grid >= 0]
    if len(valid) == 0 or n_colors == 0:
        return []
    counts = np.bincount(valid.ravel(), minlength=n_colors)
    ranked = np.argsort(-counts)
    symbols = [""] * n_colors
    for rank, color_idx in enumerate(ranked):
        if rank < len(SYMBOL_POOL):
            symbols[color_idx] = SYMBOL_POOL[rank]
        else:
            symbols[color_idx] = str(rank)
    return symbols
