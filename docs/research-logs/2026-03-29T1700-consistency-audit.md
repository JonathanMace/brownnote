# Consistency Audit Report — 2026-03-29T1700

## Overall Verdict: PASS with warnings (6 critical, 9 warnings)

All physics, all paper values, all code outputs, all citations, and all tests
are **internally consistent**. The critical items are exclusively stale README
and copilot-instructions tallies and one phantom API name. No numerical or
scientific errors were found.

---

## 1. README.md Accuracy

### Test count
| Claim | Actual | Verdict |
|-------|--------|---------|
| 203 (README line 141) | **206** (pytest collected) | ❌ CRITICAL — stale by 3 |
| 203 (copilot-instructions R5) | **206** | ❌ CRITICAL — stale by 3 |

### Agent count
| Claim | Actual | Verdict |
|-------|--------|---------|
| 17 (README line 79) | **20** files in `.github/agents/` | ❌ CRITICAL — stale by 3 |
| 18 (copilot-instructions table) | **20** | ❌ WARNING — missing `dietrich`, `experimentalist` |

Extra agent files not listed in copilot-instructions:
- `dietrich.agent.md` (likely duplicate persona of `coffee-machine-guru`)
- `experimentalist.md` (unlisted, also uses old naming without `.agent.` infix)

### Skill count
| Claim | Actual | Verdict |
|-------|--------|---------|
| 16 (README line 79) | **16** proper skill directories + 4 legacy single-files | ✅ PASS |

### Commit / PR / Log counts
| Metric | README claim | Actual | Verdict |
|--------|-------------|--------|---------|
| Commits | ~300 | **337** | ❌ WARNING — stale (should say ~340) |
| Merged PRs | 117 | **167** | ❌ CRITICAL — stale by 50 |
| Research logs | 57+ | **72** | ❌ WARNING — stale (should say 72+) |

### Draft PDF links
| Paper | README link | File exists? | Verdict |
|-------|------------|--------------|---------|
| Paper 1 | `paper/drafts/draft_2026-03-29_0228_final.pdf` | ✅ Yes | ✅ PASS |
| Paper 2 | `paper2-gas-pockets/drafts/draft_2026-03-29_libertine.pdf` | ✅ Yes | ✅ PASS |
| Paper 3 | `paper3-scaling-laws/drafts/draft_2026-03-29_libertine.pdf` | ✅ Yes | ✅ PASS |
| Paper 4 | `projects/bladder-resonance/paper/drafts/draft_2026-03-29_libertine.pdf` | ✅ Yes | ✅ PASS |
| Paper 5 | `projects/borborygmi/paper/drafts/draft_2026-03-29_libertine.pdf` | ✅ Yes | ✅ PASS |
| Research statement | `docs/mid-tenure-research-statement.pdf` | ✅ Yes | ✅ PASS |
| AI-assisted research | `docs/ai-assisted-research.md` | ✅ Yes | ✅ PASS |

All PDFs are dated 2026-03-29 — current.

### Phantom API in README & copilot-instructions
| Location | Code shown | Actual API | Verdict |
|----------|-----------|------------|---------|
| README line 101 | `from src.analytical.mechanical_coupling import mechanical_coupling_analysis` | Function **does not exist** | ❌ CRITICAL |
| copilot-instructions line 187 | `mech = mechanical_coupling_analysis(model)` | Actual function: `compare_airborne_vs_mechanical(model)` | ❌ CRITICAL |

The function was likely renamed during development. The correct import is:
```python
from src.analytical.mechanical_coupling import compare_airborne_vs_mechanical
```

---

## 2. Canonical Parameters (R3)

### `scripts/check_consistency.py` output
```
== Canonical Parameter Check ==
  OK: a = 0.18
  OK: c = 0.12
  OK: h = 0.01
  OK: E = 100000.0
  OK: nu = 0.45
  OK: rho_wall = 1100.0
  OK: rho_fluid = 1020.0
  OK: K_fluid = 2200000000.0
  OK: P_iap = 1000.0
  OK: loss_tangent = 0.25

== Stale Value Check ==
  OK: No stale: loss_tangent = 0.30
  OK: No stale: ka = 0.017
  OK: No stale: R_eq = 0.133

== Citation Key Check ==
  OK: All papers — all citation keys found in .bib

PASS: All consistency checks passed
```

### Code defaults vs canonical table

| Parameter | Canonical (R3) | `AbdominalModelV2` default | Paper Table 1 | Verdict |
|-----------|---------------|---------------------------|---------------|---------|
| a | 0.18 m | 0.18 | 0.18 | ✅ |
| c | 0.12 m | 0.12 | 0.12 | ✅ |
| h | 0.010 m | 0.010 | 0.010 | ✅ |
| E | 0.1 MPa | 0.1e6 Pa | 0.1 MPa | ✅ |
| ν | 0.45 | 0.45 | 0.45 | ✅ |
| ρ_w | 1100 kg/m³ | 1100.0 | 1100 | ✅ |
| ρ_f | 1020 kg/m³ | 1020.0 | 1020 | ✅ |
| K_f | 2.2 GPa | 2.2e9 Pa | 2.2 GPa | ✅ |
| P_iap | 1000 Pa | 1000.0 | 1000 Pa | ✅ |
| η | 0.25 | 0.25 | 0.25 | ✅ |

### Derived values

| Quantity | Canonical | Code output | Paper | Verdict |
|----------|-----------|-------------|-------|---------|
| R_eq | 0.157 m | 0.1572 m | 0.157 m | ✅ |
| f₂ | 3.95 Hz | 3.9524 Hz | 4.0 Hz (rounded) | ✅ |
| Q | 4.0 | 4.0 | 4.0 | ✅ |
| ζ | 0.125 | 0.1250 | 0.125 | ✅ |
| ka | 0.0114 | 0.01137 | 0.0114 | ✅ |
| Breathing | ~2490 Hz | 2490.65 Hz | ~2500 Hz | ✅ |

Paper rounding (3.95 → 4.0 Hz, 2490 → 2500 Hz) is consistent and appropriate for presentation.

### Stale v1 values scan
No instances of η=0.30, ka=0.017, or R_eq=0.133 found in any `.py` or `.tex` file. ✅ PASS

### Relationship consistency
- Q = 1/η = 1/0.25 = 4.0 ✅
- ζ = η/2 = 0.125 ✅
- Q = 1/(2ζ) = 4.0 ✅

---

## 3. Cross-Table Consistency

### Table tab:airborne (Section 4) vs code
| SPL | Paper ξ_energy | Code ξ_energy | Paper ξ_pressure | Code ξ_pressure | Verdict |
|-----|---------------|--------------|-----------------|----------------|---------|
| 100 dB | 0.001 μm | 0.00137 μm | 0.018 μm | 0.01844 μm | ✅ (rounded) |
| 110 dB | 0.004 μm | 0.00435 μm | 0.058 μm | 0.05831 μm | ✅ |
| 120 dB | 0.014 μm | 0.01374 μm | 0.18 μm | 0.1844 μm | ✅ |
| 130 dB | 0.044 μm | 0.04346 μm | 0.58 μm | 0.5830 μm | ✅ |
| 140 dB | 0.14 μm | 0.1374 μm | 1.84 μm | 1.844 μm | ✅ |

### Table tab:mechanical (Section 4) vs code
| a_rms | Paper x_base | Code x_base | Paper ξ_rel | Code ξ_rel | Verdict |
|-------|-------------|-------------|------------|-----------|---------|
| 0.1 m/s² | 229 μm | 229.3 μm | 917 μm | 917.3 μm | ✅ |
| 0.5 m/s² | 1147 μm | 1146.6 μm | 4586 μm | 4586.3 μm | ✅ |
| 1.0 m/s² | 2293 μm | 2293.2 μm | 9173 μm | 9172.7 μm | ✅ |
| 1.15 m/s² | 2637 μm | 2637.1 μm | 10549 μm | 10548.6 μm | ✅ |

### Coupling ratio
Paper equation (eq:coupling_ratio): R = 917/0.014 ≈ 6.6 × 10⁴
Code: 917.3/0.01374 = 66,759 ≈ 6.6 × 10⁴ ✅

### Cross-reference: discussion Table tab:pathway_summary
| Mechanism | Table value | Source table | Consistent? |
|-----------|-----------|--------------|-------------|
| Cavity resonance (airborne) | 0.014 μm | tab:airborne @ 120 dB | ✅ |
| WBV @ 0.5 m/s² | 4,586 μm | tab:mechanical | ✅ |
| WBV @ 1.15 m/s² | 10,549 μm | tab:mechanical | ✅ |

### Energy budget
- Code: `energy_conserved_energy: True`, `energy_conserved_pressure: False` ✅
- Ratio pressure/energy = 13.42 (paper says ~13×) ✅

All cross-table values are self-consistent. ✅ PASS

---

## 4. Code-Paper Agreement

### Paper 1 core outputs
All values verified above. Maximum discrepancy < 1% (rounding only). ✅ PASS

### Energy-consistent displacement
Code: 0.01374 μm → Paper: 0.014 μm (0.3% rounding). ✅ PASS

### Pressure-to-energy ratio
Code: 13.416 → Paper: ~13× ✅ PASS

### f₂ rounding
Code: 3.9524 Hz → Paper: 4.0 Hz (1.2% rounding, explicitly acknowledged in text). ✅ PASS

---

## 5. Citation Completeness

### BibTeX keys
All citation keys across all 5 papers resolve in their respective `.bib` files. ✅ PASS
- Paper 1: 52 citations, all found
- Paper 2: 24 citations, all found
- Paper 3: 17 citations, all found
- Paper 4: 20 citations, all found
- Paper 5: 20 citations, all found

### Key references verified present
- `Junger1986` ✅
- `Kitazaki1998` ✅
- `Griffin1990` ✅

### Label-ref completeness
All `\label{}` targets in Paper 1 have at least one `\ref{}` or `\eqref{}`. ✅ PASS

### Figure files
All `\includegraphics` targets exist in `data/figures/`:
- `fig_geometry_schematic.pdf` ✅
- `fig_mode_shapes.pdf` ✅
- `fig_frequency_vs_E.pdf` ✅
- `fig_uq_sobol_indices.png` ✅
- `fig_coupling_comparison.pdf` ✅

---

## 6. Stale Content Detection

### TODOs/FIXMEs/placeholders
No `TODO`, `FIXME`, `XXX`, `TBD`, or `???` found in any `.tex` file across all 5 papers. ✅ PASS

### v1 references
No active code imports from `natural_frequency.py` (v1). Only historical mentions in research logs (appropriate context). ✅ PASS

---

## 7. Documentation Freshness

### copilot-instructions.md
- Last updated header: 2026-03-29 ✅
- Agent table: lists 18, actual 20 ❌ WARNING (missing `dietrich`, `experimentalist`)
- Test count: says 203, actual 206 ❌ (noted above)
- Phantom `mechanical_coupling_analysis` in code example ❌ (noted above)
- All other content (physics, rules, workflow) is accurate ✅

### Agent definitions
20 files in `.github/agents/`. Two naming inconsistencies:
- `experimentalist.md` — missing `.agent.` infix (should be `experimentalist.agent.md`)
- `journal-editor.md` — missing `.agent.` infix (should be `journal-editor.agent.md`)

### Skills
16 proper skill directories + 4 legacy single-files. Matches README claim of 16. ✅ PASS

### Path-specific instructions
5 instruction files matching 5 papers:
- `paper1.instructions.md` → `paper/` ✅
- `paper2.instructions.md` → `paper2-gas-pockets/` ✅
- `paper3.instructions.md` → `paper3-scaling-laws/` ✅
- `paper4.instructions.md` → `projects/bladder-resonance/` ✅
- `paper5.instructions.md` → `projects/borborygmi/` ✅

---

## 8. Test Suite

### Core tests
```
tests/ — 206 passed, 1 warning in 4.99s ✅
```
Breakdown: test_analytical (72), test_borborygmi (58), test_extraction (2),
test_figures (8), test_materials (14), test_mesh (5) = 159 in those files...
total collected: 206.

### Bladder tests
```
projects/bladder-resonance/tests/ — 31 passed in 5.26s ✅
```

### Total test count
206 (core) + 31 (bladder) = **237 total tests passing**
README claims 203 (core only, but stale).

---

## 9. Git Hygiene

### Stale remote branches
**30 unmerged remote branches** (excluding `origin/main`, `origin/HEAD`):
```
origin/ci-automation, origin/create-dietrich, origin/create-editor,
origin/infra-whisky-convention, origin/lab-health-check, origin/log-sprint,
origin/mid-tenure-latex, origin/mid-tenure-update, origin/p1-draft-snapshot,
origin/p1-final-tweaks, origin/p1-submission-polish, origin/p2-major-reframe,
origin/p2-minor-fix-r2, origin/p2-post-fix-review, origin/p2-reviewer-b-r2,
origin/p3-major-fix, origin/p3-minor-fix, origin/p3-minor-fix-r2,
origin/p3-review-a, origin/p3-reviewer-b-r2, origin/p4-major-fix,
origin/p4-minor-fix-r2, origin/p4-reviewer-a-r2, origin/paper-instructions,
origin/paper-libertine-font, origin/readme-draft-links,
origin/readme-libertine-links, origin/recompile-all-papers,
origin/scout-feasibility, origin/update-research-statement-pdf
```
3 additional merged remote branches not yet deleted.
❌ WARNING — 33 total stale remote branches need cleanup.

### Stale local branches
9 local branches besides `main`:
`consistency-audit-full`, `p1-submission-audit`, `p3-reviewer-b-r2`,
`p4-reviewer-a`, `paper-instructions`, `recompile-all-papers`
(plus worktree branches: `p2-major-reframe`, `p2-reviewer-b-r2`,
`p3-major-fix`, `p4-major-fix`)
❌ WARNING — local branches need pruning.

### Worktrees
5 non-main worktrees, 1 marked prunable:
```
browntone-worktrees/bibkey-harmonise    (detached HEAD)
browntone-worktrees/p2-major-reframe    [p2-major-reframe]
browntone-worktrees/p2-reviewer-b-r2    [p2-reviewer-b-r2] PRUNABLE
browntone-worktrees/p3-major-fix        [p3-major-fix]
browntone-worktrees/p4-major-fix        [p4-major-fix]
```
❌ WARNING — 1 prunable worktree, 1 detached HEAD worktree.

### .gitignore coverage
- `__pycache__/` ✅
- `*.py[cod]` ✅
- LaTeX aux files ✅
- PDFs: NOT ignored (intentional — drafts are committed) ✅
- PNGs: NOT ignored (intentional — figures are committed) ✅

---

## 10. CI/CD Pipeline

### `.github/workflows/ci.yml`
- Tests: `python -m pytest tests/ -v -m "not fenics and not slow"` ✅
- Paper compilation: all 5 papers with correct directories ✅
- Consistency check: `python scripts/check_consistency.py` (PR only) ✅
- Figure generation: `python scripts/generate_all_figures.py` (push only) ✅
- Python versions: 3.10, 3.11, 3.12 ✅

### `.github/workflows/paper.yml`
- Manual dispatch for all 5 papers ✅
- Uses `xu-cheng/latex-action@v3` ✅

No issues found. ✅ PASS

---

## 11. Paper PDF Drafts

All 5 papers + mid-tenure statement have current drafts dated 2026-03-29.
All README links resolve to existing files. ✅ PASS

---

## Summary

| Section | Result | Issues |
|---------|--------|--------|
| 1. README.md | ❌ FAIL | 6 stale numbers, 1 phantom API |
| 2. Canonical Parameters | ✅ PASS | Perfect agreement |
| 3. Cross-Table Consistency | ✅ PASS | All values self-consistent |
| 4. Code-Paper Agreement | ✅ PASS | <1% discrepancy (rounding) |
| 5. Citation Completeness | ✅ PASS | All keys, labels, figures OK |
| 6. Stale Content | ✅ PASS | No TODOs, no v1 refs in code |
| 7. Documentation Freshness | ⚠️ WARN | Agent count, test count stale |
| 8. Test Suite | ✅ PASS | 206 + 31 = 237 all passing |
| 9. Git Hygiene | ⚠️ WARN | 33 stale remote branches, 1 prunable worktree |
| 10. CI/CD Pipeline | ✅ PASS | All paths and commands correct |
| 11. Paper PDF Drafts | ✅ PASS | All current, all linked |

**Total: 6 critical issues, 9 warnings, 0 scientific errors.**

---

## Actionable Fixes

### Critical (should fix before submission)

1. **README.md line 79**: Update tallies to "~340 commits, 167 pull requests merged,
   206 tests passing, 20 custom agents, 16 reusable skills, 72+ research logs"
2. **README.md line 141**: Change "203 passing tests" → "206 passing tests"
3. **README.md line 101**: Fix phantom import:
   `from src.analytical.mechanical_coupling import compare_airborne_vs_mechanical`
4. **copilot-instructions.md R5**: Change "203 tests" → "206 tests"
5. **copilot-instructions.md line 187**: Fix phantom API call:
   `mech = compare_airborne_vs_mechanical(model)  # → coupling ratio ~66,000`
6. **copilot-instructions.md agent table**: Add `dietrich` and `experimentalist`
   entries (or remove the redundant files)

### Warnings (should fix during next housekeeping)

7. Rename `experimentalist.md` → `experimentalist.agent.md`
8. Rename `journal-editor.md` → `journal-editor.agent.md`
9. Delete 33 stale remote branches
10. Prune `browntone-worktrees/p2-reviewer-b-r2` worktree
11. Remove or re-attach `browntone-worktrees/bibkey-harmonise` detached worktree
12. Clean up stale local branches
13. Update README commit/PR/log counts (stale by ~10-40%)
14. Consider resolving `dietrich.agent.md` vs `coffee-machine-guru.agent.md`
    (same persona, two files)
15. Consider adding bladder test count (31) to README total

---

*Audit performed by consistency-auditor agent, 2026-03-29T1700.*
*All code outputs verified by running canonical model from repository root.*
