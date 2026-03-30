#!/usr/bin/env python3
"""CI consistency checks for the Browntone project.

Verifies:
  1. Canonical parameters in code match R3 values
  2. No stale v1 parameter values in source
  3. All \\cite{} keys in .tex files exist in their .bib files
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FAIL = False
ROOT = Path(__file__).resolve().parent.parent


def error(msg: str) -> None:
    global FAIL
    FAIL = True
    print(f"::error::{msg}")


def ok(msg: str) -> None:
    print(f"  OK: {msg}")


# -- 1. Canonical parameter verification --

print("\n== Canonical Parameter Check ==")

sys.path.insert(0, str(ROOT / "src"))
try:
    from analytical.natural_frequency_v2 import AbdominalModelV2

    model = AbdominalModelV2()

    CANONICAL = {
        "a": 0.18,
        "c": 0.12,
        "h": 0.010,
        "E": 0.1e6,
        "nu": 0.45,
        "rho_wall": 1100.0,
        "rho_fluid": 1020.0,
        "K_fluid": 2.2e9,
        "P_iap": 1000.0,
        "loss_tangent": 0.25,
    }

    for param, expected in CANONICAL.items():
        actual = getattr(model, param, None)
        if actual is None:
            error(f"Parameter {param} not found on AbdominalModelV2")
        elif abs(actual - expected) > abs(expected) * 1e-6:
            error(f"Parameter {param}: expected {expected}, got {actual}")
        else:
            ok(f"{param} = {actual}")

except ImportError as exc:
    error(f"Could not import AbdominalModelV2: {exc}")


# -- 2. Stale v1 value scan --

print("\n== Stale Value Check ==")

STALE_PATTERNS = [
    (r"loss_tangent\s*=\s*0\.30\b", "loss_tangent = 0.30 (should be 0.25)"),
    (r"\bka\s*=\s*0\.017\b", "ka = 0.017 (stale v1)"),
    (r"(?i)r_eq\s*=\s*0\.133\b", "R_eq = 0.133 (should be 0.157)"),
]

SEARCH_DIRS = [ROOT / "src", ROOT / "tests"]

for pattern_str, description in STALE_PATTERNS:
    pattern = re.compile(pattern_str)
    found = False
    for search_dir in SEARCH_DIRS:
        if not search_dir.exists():
            continue
        for py_file in search_dir.rglob("*.py"):
            content = py_file.read_text(errors="replace")
            for i, line in enumerate(content.splitlines(), 1):
                if pattern.search(line):
                    rel = py_file.relative_to(ROOT)
                    error(f"Stale value in {rel}:{i} -- {description}")
                    found = True
    if not found:
        ok(f"No stale: {description}")


# -- 3. Citation key check --

print("\n== Citation Key Check ==")

PAPERS = [
    "papers/paper1-brown-note",
    "papers/paper2-gas-pockets",
    "papers/paper3-scaling-laws",
    "papers/paper4-bladder",
    "papers/paper5-borborygmi",
    "papers/paper6-sub-bass",
    "papers/paper7-watermelon",
    "papers/paper8-kac",
]


def extract_cite_keys(tex_dir: Path) -> set[str]:
    """Extract all citation keys from \\cite, \\citep, \\citet commands."""
    keys: set[str] = set()
    for tex_file in tex_dir.rglob("*.tex"):
        content = tex_file.read_text(errors="replace")
        for match in re.finditer(r"\\cite[tp]?\*?\{([^}]+)\}", content):
            for key in match.group(1).split(","):
                stripped = key.strip()
                if stripped:
                    keys.add(stripped)
    return keys


def extract_bib_keys(tex_dir: Path) -> set[str]:
    """Extract all entry keys from .bib files."""
    keys: set[str] = set()
    for bib_file in tex_dir.rglob("*.bib"):
        content = bib_file.read_text(errors="replace")
        for match in re.finditer(r"@\w+\{(\S+?),", content):
            keys.add(match.group(1).strip())
    return keys


for paper_dir_str in PAPERS:
    paper_dir = ROOT / paper_dir_str
    if not paper_dir.exists():
        print(f"  SKIP: {paper_dir_str} not found")
        continue

    cite_keys = extract_cite_keys(paper_dir)
    bib_keys = extract_bib_keys(paper_dir)
    missing = cite_keys - bib_keys

    if missing:
        error(f"[{paper_dir_str}] Missing bib entries: {', '.join(sorted(missing))}")
    else:
        ok(f"[{paper_dir_str}] All {len(cite_keys)} citation keys found in .bib")


# -- Summary --

print()
if FAIL:
    print("FAIL: Consistency checks failed")
    sys.exit(1)
else:
    print("PASS: All consistency checks passed")
    sys.exit(0)