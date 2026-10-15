#!/usr/bin/env python3
"""The reduction curve: which measurement is load-bearing?

Re-runs cvprofiles over menu subsets with the network and beta held FIXED, and
reports how the headline range [L,U] responds. No engine changes — this is
repeat invocation of the published API, which is exactly what an interactive
demo would do live.

Protocol (frozen before results):
  corpus  : evals/wvs_gps_preferences/data/inputs (41 units, 7 measures)
  baseline: full menu
  probe   : for each measure m, drop m from scores + roles.measures, keep
            network.yaml and beta.yaml byte-identical, re-run
  metric  : width = U - L, and its change vs baseline
  note    : every subset gets a FRESH out_dir (reusing one silently unlinks
            layer artifacts — documented in USER_GUIDE)
"""
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import pandas as pd

from cvprofiles.pipeline import run_profile

SRC = Path(
    "/Users/bonorinoa/Hermes/Projects/cvprofiles/evals/wvs_gps_preferences/data/inputs"
)
OUT = Path("/tmp/cvp_reduction")
OUT.mkdir(parents=True, exist_ok=True)


def prepare() -> Path:
    """Copy the frozen inputs into a scratch dir we can slice."""
    work = Path(tempfile.mkdtemp(prefix="cvp_reduction_"))
    for f in ("scores.csv", "roles.json", "network.yaml", "beta.yaml", "score_manifest.json"):
        src = SRC / f
        if src.exists():
            shutil.copy(src, work / f)
    return work


def run(work: Path, scores: Path, roles: Path, label: str) -> dict:
    out_dir = Path(tempfile.mkdtemp(prefix=f"run_{label}_"))  # fresh per run
    res = run_profile(
        scores=scores,
        roles=roles,
        network=work / "network.yaml",
        beta=work / "beta.yaml",
        out_dir=out_dir,
        title=f"reduction probe: {label}",
        write_parquet=False,
    )
    rng = json.loads((out_dir / "range.json").read_text())
    adm = json.loads((out_dir / "admissible.json").read_text())
    L, U = rng.get("L"), rng.get("U")
    return {
        "label": label,
        "empty": bool(rng.get("empty")),
        "L": L,
        "U": U,
        "width": (None if (L is None or U is None) else round(U - L, 4)),
        "n_admissible": len(adm.get("M_star", adm.get("admissible", [])) or []),
    }


def main() -> None:
    work = prepare()
    df = pd.read_csv(work / "scores.csv")
    roles = json.loads((work / "roles.json").read_text())
    measures = list(roles["measures"])
    print(f"corpus: {len(df)} units, {len(measures)} measures\n")

    base = run(work, work / "scores.csv", work / "roles.json", "full")
    print(f"BASELINE (full menu): L={base['L']}  U={base['U']}  width={base['width']}  "
          f"|M*|={base['n_admissible']}\n")

    rows = []
    for m in measures:
        d = work / f"drop_{m}"
        d.mkdir(exist_ok=True)
        keep = [c for c in df.columns if c != m]
        df[keep].to_csv(d / "scores.csv", index=False)
        r = dict(roles)
        r["measures"] = [x for x in roles["measures"] if x != m]
        (d / "roles.json").write_text(json.dumps(r, indent=2))
        try:
            rows.append(run(work, d / "scores.csv", d / "roles.json", f"drop:{m}"))
        except Exception as exc:  # RestrictError and friends
            rows.append({"label": f"drop:{m}", "empty": None, "L": None, "U": None,
                         "width": None, "n_admissible": None,
                         "error": f"{type(exc).__name__}: {str(exc)[:90]}"})

    rows.sort(key=lambda r: (r["width"] is None, r["width"] or 0))

    print(f"{'dropped measure':<20} {'L':>9} {'U':>9} {'width':>8} {'Δwidth':>8} {'|M*|':>5}")
    print("-" * 66)
    for r in rows:
        if r.get("error"):
            print(f"{r['label'][5:]:<20} {'—':>9} {'—':>9} {'—':>8} {'—':>8} {'—':>5}  {r['error']}")
            continue
        dw = (None if (r["width"] is None or base["width"] is None)
              else round(r["width"] - base["width"], 4))
        print(f"{r['label'][5:]:<20} {str(r['L']):>9} {str(r['U']):>9} "
              f"{str(r['width']):>8} {str(dw):>8} {str(r['n_admissible']):>5}")

    (OUT / "reduction_curve.json").write_text(
        json.dumps({"baseline": base, "subsets": rows}, indent=2)
    )
    print(f"\nwritten: {OUT / 'reduction_curve.json'}")


if __name__ == "__main__":
    main()