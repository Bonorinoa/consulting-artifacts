#!/usr/bin/env python3
"""Silicus TA 2.0 — citation-ambiguity register + relevance-gate separability.

Companion to audit_index.py. Two questions a release decision actually needs:

  Q1 (citation integrity): are there page pairs so close that a bracketed
     citation to one of them does not identify a unique page?
  Q2 (abstention): could a single similarity threshold separate on-corpus from
     off-corpus pages, i.e. does the system have a cheap relevance gate available?

Offline: stored page embeddings only; no API key, no network.
Thresholds are scanned (not fitted) and every pair is reported, so the reader
can judge rather than trust a single cut.
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("/tmp/silicus")
THRESHOLDS = [0.99, 0.97, 0.95, 0.93, 0.90]
EXAMPLES_PER_THRESHOLD = 6


def unit(v):
    v = np.asarray(v, dtype=np.float64)
    n = np.linalg.norm(v)
    return v / (n if n else 1.0)


def main() -> None:
    courses = {}
    for f in sorted(glob.glob(str(DATA / "data" / "*" / "*_pages.parquet"))):
        p = Path(f)
        df = pd.read_parquet(p)
        mat = np.vstack([unit(v) for v in df["embedding"]])
        courses[p.parent.name] = (mat, df)

    # ---- Q1: citation ambiguity, same course, distinct pages ----
    q1 = {}
    for name, (mat, df) in courses.items():
        sims = mat @ mat.T
        iu = np.triu_indices(len(mat), k=1)
        vals = sims[iu]
        entry = {"pages": len(mat), "pairs": int(len(vals))}
        for t in THRESHOLDS:
            mask = vals >= t
            entry[f"pairs_ge_{t}"] = int(mask.sum())
        # examples at the loosest threshold, preferring cross-file pairs
        ex = []
        for t in (0.95, 0.93):
            idx = np.where(vals >= t)[0]
            cross = [
                k for k in idx
                if df["filename"].iloc[iu[0][k]] != df["filename"].iloc[iu[1][k]]
            ]
            ex.append({
                "threshold": t,
                "same_file_pairs": int(len(idx) - len(cross)),
                "cross_file_pairs": int(len(cross)),
                "examples_cross_file": [
                    {
                        "a": f'{df["filename"].iloc[iu[0][k]]} p.{int(df["page_number"].iloc[iu[0][k]])}',
                        "b": f'{df["filename"].iloc[iu[1][k]]} p.{int(df["page_number"].iloc[iu[1][k]])}',
                        "cosine": round(float(vals[k]), 4),
                    }
                    for k in cross[:EXAMPLES_PER_THRESHOLD]
                ],
            })
        entry["examples"] = ex
        q1[name] = entry

    # ---- Q2: is a single similarity threshold a usable relevance gate? ----
    names = sorted(courses)
    within_strongest = {}   # for each page: its best in-course neighbour
    off_best = {}           # for each page: its best out-of-course neighbour
    for a in names:
        ma, _ = courses[a]
        w = ma @ ma.T
        np.fill_diagonal(w, np.nan)
        within_strongest[a] = np.nanmax(w, axis=1)
        best = np.full(len(ma), -np.inf)
        for b in names:
            if a == b:
                continue
            best = np.maximum(best, (ma @ courses[b][0].T).max(axis=1))
        off_best[a] = best

    w_all = np.concatenate([within_strongest[a] for a in names])
    o_all = np.concatenate([off_best[a] for a in names])

    def q(x, p):
        return round(float(np.percentile(x, p)), 4)

    q2 = {
        "on_corpus_best_neighbour": {
            "min": round(float(w_all.min()), 4), "p10": q(w_all, 10),
            "median": q(w_all, 50), "max": round(float(w_all.max()), 4)},
        "off_corpus_best_neighbour": {
            "min": round(float(o_all.min()), 4), "p10": q(o_all, 10),
            "median": q(o_all, 50), "p90": q(o_all, 90), "max": round(float(o_all.max()), 4)},
        "overlap_region": [round(float(o_all.max()), 4), round(float(w_all.min()), 4)],
        "separable_by_single_threshold": bool(
            w_all.min() > o_all.max()
        ),
        "pages_where_offcorpus_beats_oncorpus": int((o_all > w_all).sum()),
        "pages_total": int(len(w_all)),
    }

    out = {"q1_citation_ambiguity": q1, "q2_relevance_gate": q2}
    print(json.dumps(out, indent=2))
    Path("/tmp/silicus_audit/ambiguity_register.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
