import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dmc_colors import ciede2000, find_nearest, load_dmc_database, rgb_to_lab


def test_load_database():
    db = load_dmc_database()
    assert len(db) > 400
    names = {d.dmc for d in db}
    assert "310" in names
    assert "blanc" in names
    assert "ecru" in names


def test_rgb_to_lab_black():
    L, a, b = rgb_to_lab(0, 0, 0)
    assert L < 1.0


def test_rgb_to_lab_white():
    L, a, b = rgb_to_lab(255, 255, 255)
    assert L > 99.0


def test_ciede2000_identical():
    lab = rgb_to_lab(128, 64, 32)
    assert ciede2000(lab, lab) < 0.001


def test_ciede2000_different():
    black = rgb_to_lab(0, 0, 0)
    white = rgb_to_lab(255, 255, 255)
    assert ciede2000(black, white) > 50


def test_find_nearest_black():
    dmc = find_nearest(0, 0, 0)
    assert dmc.dmc == "310"


def test_find_nearest_white():
    dmc = find_nearest(252, 251, 248)
    assert dmc.dmc == "blanc"


def test_find_nearest_with_exclude():
    dmc = find_nearest(0, 0, 0, exclude={"310"})
    assert dmc.dmc != "310"
