from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
_table_cache: dict[str, OlympusEntry] | None = None


@dataclass
class OlympusEntry:
    number: str
    name_ja: str | None = None


def load_conversion_table() -> dict[str, OlympusEntry]:
    global _table_cache
    if _table_cache is not None:
        return _table_cache
    path = _DATA_DIR / "dmc_to_olympus.json"
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    table: dict[str, OlympusEntry] = {}
    for dmc, val in raw.items():
        if isinstance(val, dict):
            table[dmc] = OlympusEntry(
                number=str(val.get("oly", "")),
                name_ja=val.get("name_ja") or None,
            )
        else:
            table[dmc] = OlympusEntry(number=str(val), name_ja=None)
    _table_cache = table
    return table


def dmc_to_olympus(dmc_number: str) -> OlympusEntry | None:
    return load_conversion_table().get(dmc_number)


def dmc_to_olympus_str(dmc_number: str) -> str | None:
    entry = dmc_to_olympus(dmc_number)
    return entry.number if entry else None
