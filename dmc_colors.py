from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
_dmc_cache: list[DMCColor] | None = None


@dataclass
class DMCColor:
    dmc: str
    name: str
    r: int
    g: int
    b: int

    @property
    def rgb(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)


def load_dmc_database() -> list[DMCColor]:
    global _dmc_cache
    if _dmc_cache is not None:
        return _dmc_cache
    path = _DATA_DIR / "dmc_threads.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    _dmc_cache = [
        DMCColor(dmc=str(d["dmc"]), name=d["name"], r=d["r"], g=d["g"], b=d["b"])
        for d in data
    ]
    return _dmc_cache


def rgb_to_lab(r: int, g: int, b: int) -> tuple[float, float, float]:
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0

    def linearize(c: float) -> float:
        return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92

    rl, gl, bl = linearize(rn), linearize(gn), linearize(bn)

    x = (rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375) / 0.95047
    y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    z = (rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b_val = 200 * (fy - fz)
    return (L, a, b_val)


def ciede2000(
    lab1: tuple[float, float, float],
    lab2: tuple[float, float, float],
) -> float:
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    avg_Lp = (L1 + L2) / 2.0
    C1 = math.sqrt(a1 * a1 + b1 * b1)
    C2 = math.sqrt(a2 * a2 + b2 * b2)
    avg_C = (C1 + C2) / 2.0

    avg_C7 = avg_C ** 7
    G = 0.5 * (1 - math.sqrt(avg_C7 / (avg_C7 + 25 ** 7)))
    a1p = a1 * (1 + G)
    a2p = a2 * (1 + G)

    C1p = math.sqrt(a1p * a1p + b1 * b1)
    C2p = math.sqrt(a2p * a2p + b2 * b2)

    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360

    dLp = L2 - L1
    dCp = C2p - C1p

    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360

    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))

    avg_Lp2 = avg_Lp
    avg_Cp = (C1p + C2p) / 2.0

    if C1p * C2p == 0:
        avg_hp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        avg_hp = (h1p + h2p) / 2.0
    elif h1p + h2p < 360:
        avg_hp = (h1p + h2p + 360) / 2.0
    else:
        avg_hp = (h1p + h2p - 360) / 2.0

    T = (
        1
        - 0.17 * math.cos(math.radians(avg_hp - 30))
        + 0.24 * math.cos(math.radians(2 * avg_hp))
        + 0.32 * math.cos(math.radians(3 * avg_hp + 6))
        - 0.20 * math.cos(math.radians(4 * avg_hp - 63))
    )

    SL = 1 + 0.015 * (avg_Lp2 - 50) ** 2 / math.sqrt(20 + (avg_Lp2 - 50) ** 2)
    SC = 1 + 0.045 * avg_Cp
    SH = 1 + 0.015 * avg_Cp * T

    avg_Cp7 = avg_Cp ** 7
    RT = (
        -2
        * math.sqrt(avg_Cp7 / (avg_Cp7 + 25 ** 7))
        * math.sin(math.radians(60 * math.exp(-(((avg_hp - 275) / 25) ** 2))))
    )

    return math.sqrt(
        (dLp / SL) ** 2
        + (dCp / SC) ** 2
        + (dHp / SH) ** 2
        + RT * (dCp / SC) * (dHp / SH)
    )


def find_nearest(
    r: int, g: int, b: int, exclude: set[str] | None = None
) -> DMCColor:
    db = load_dmc_database()
    lab = rgb_to_lab(r, g, b)
    best: DMCColor | None = None
    best_dist = float("inf")
    for dmc in db:
        if exclude and dmc.dmc in exclude:
            continue
        d = ciede2000(lab, rgb_to_lab(dmc.r, dmc.g, dmc.b))
        if d < best_dist:
            best_dist = d
            best = dmc
    assert best is not None
    return best


def find_nearest_n(
    colors_rgb: list[tuple[int, int, int]],
) -> list[DMCColor]:
    used: set[str] = set()
    result: list[DMCColor] = []
    for r, g, b in colors_rgb:
        dmc = find_nearest(r, g, b, exclude=used)
        used.add(dmc.dmc)
        result.append(dmc)
    return result
