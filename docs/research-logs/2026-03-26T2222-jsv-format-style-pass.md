# Research Log: 2026-03-26T2222 — JSV Format Compliance + Style Pass

## What was done

### JSV Format Compliance
- Switched to `\documentclass[review]{elsarticle}` (single-column, double-spaced)
- Added line numbering (`lineno` package) — required by JSV for review
- Added Highlights section (5 items, each <85 chars)
- Switched bibliography to `elsarticle-num` (pure numerical `[1]` style)
- Added Data Availability, CRediT, and Competing Interest statements
- Fixed all `\cite{}` references throughout

### Parameter Consistency Fix (Reviewer B F1)
- Identified code defaults ≠ paper parameters: code had E=0.5, a=0.15, h=0.015 vs paper's E=0.1, a=0.18, h=0.01
- Established CANONICAL parameter set and recomputed all tables
- Canonical f₂ = 4.0 Hz (not 4.4 Hz as previously claimed)
- Energy-consistent displacement at 120 dB: 0.014 μm (not 0.14 μm)
- SPL for PIEZO threshold: 158 dB (not 137 dB) — even stronger for our argument

### Style Pass
- Rewrote introduction: active voice, narrative hook, subtle humor
- Rewrote Section 4 (coupling): vivid prose, "kicks open the door" etc.
- Rewrote conclusion: "half-truth" framing, wry closing lines
- Updated abstract with correct numbers and better flow (201 words)
- Title updated: "Implications for the Existence of the Brown Note"

### UQ Integration
- Monte Carlo N=10,000 results integrated into Section 3
- Key finding: f₂ = 7.5 ± 4.2 Hz (90% CI: 3.3–15.5 Hz)
- Sobol: E dominates with S_T = 0.86

### Subagent Results Received
- **UQ Monte Carlo**: Complete — f₂ = 7.5±4.2 Hz, E dominates (S_T=0.86)
- **Discussion Writer**: Complete — expanded to 345 lines, 5 subsections
- **Figures v3**: Complete — 8 camera-ready figures (PNG+PDF)
- **Reviewer B R3**: Complete — MAJOR REVISION, 0 fatal, 1 near-fatal (param mismatch, now fixed)
- **FEA Modal**: Still running
- **Rayleigh-Ritz**: Still running (long computation)

## Paper Status
- **25 pages** in JSV review format
- Abstract: 201 words ✓
- Keywords: 6 ✓
- Highlights: 5 ✓
- Line numbers: ✓
- All citations resolved: ✓
- Compiled PDF snapshot: `2026-03-26T2222-paper-snapshot.pdf`

## Critical Assessment
The parameter consistency fix is important — Reviewer B was right that we were
quoting numbers from inconsistent parameter sets. The energy-consistent
displacement (0.014 μm at 120 dB) is even more devastating for the brown note
than previously thought. 158 dB is in the "building collapse" range.

The writing is now more engaging. The tone walks a line between serious physics
and wry acknowledgment of the subject matter — appropriate for JSV, which does
publish papers with personality.

## Next Steps
1. Integrate FEA results when agents complete (boundary condition validation)
2. Address remaining Reviewer B R3 issues (theory/empirical gap)
3. Add figure references throughout paper body
4. Write research log for next iteration
