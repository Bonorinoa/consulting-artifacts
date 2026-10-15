#!/usr/bin/env python3
"""Silicus TA 2.0 — retrieval index integrity audit (offline, API-free).

WHAT THIS IS
    A release-decision audit of the persisted page index. It answers: "can the
    retrieval layer be relied on to put the right page in front of the model?"

WHY IT IS OFFLINE
    Query embedding needs the Mistral API. This audit uses ONLY the stored
    page embeddings, so anyone can reproduce it with the repo alone, no key,
    no network. It is deliberately limited to index-level claims.

FROZEN PROTOCOL (declared before results, not tuned after)
    Corpus      : every course in data/, each audited independently.
    Unit        : one page = one stored 1024-d embedding (L2-normalised).
    Test        : page-as-query. Each page's own embedding queries its own
                  course. This is the strongest available proxy for
                  "does the index retrieve the page an answer actually lives on".
    Metrics     : self-recall@1, self-recall@10, MRR, near-duplicate pairs.
    Near-dup    : cosine similarity >= 0.99 between two DISTINCT pages.
                  Rationale: two pages that close cannot be disambiguated by
                  citation, so a citation to either is not verifiable.
    Verdict     : no threshold is fitted. The question is only whether the
                  index is internally faithful and whether collisions exist.

CLAIMS THIS AUDIT DOES **NOT** MAKE
    - It does not measure answer quality (no generation).
    - It does not measure user-query retrieval (no query embeddings).
    - Self-recall is an UPPER bound on real retrieval quality: a real question
      is never as close to a page as that page's own text.
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path("/tmp/silicus")
NEAR_DUP = 0.99


def load(course_parquet: Path) -> tuple[np.ndarray, pd.DataFrame]:
    df = pd.read_parquet(course_parquet)
    mat = np.vstack([np.asarray(v, dtype=np.float64) for v in df["embedding"]])
    # guard: embeddings should already be unit-norm; normalise defensively
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    mat = mat / np.where(norms == 0, 1.0, norms)
    return mat, df


def audit(path: Path) -> dict:
    mat, df = load(path)
    sims = mat @ mat.T                       # cosine similarity, unit-norm rows
    np.fill_diagonal(sims, -np.inf)          # exclude self for duplicate scan
    order = np.argsort(-mat @ mat.T, axis=1)  # ranking incl. self
    self_rank = np.array([int(np.where(order[i] == i)[0][0]) + 1 for i in range(len(mat))])

    dup_pairs = int((np.triu(sims, k=1) >= NEAR_DUP).sum())
    top1 = sims.argmax(axis=1)
    top1_sim = sims.max(axis=1)

    return {
        "course": path.parent.name,
        "pages": int(len(df)),
        "files": int(df["filename"].nunique()),
        "self_recall_at_1": round(float((self_rank == 1).mean()), 4),
        "self_recall_at_10": round(float((self_rank <= 10).mean()), 4),
        "mrr": round(float((1.0 / self_rank).mean()), 4),
        "worst_self_rank": int(self_rank.max()),
        "pages_not_in_own_top10": int((self_rank > 10).sum()),
        "near_duplicate_pairs_at_0.99": dup_pairs,
        "top1_is_never_self": int((top1 != np.arange(len(mat))).sum()),
        "top1_similarity_median": round(float(np.median(top1_sim)), 4),
        "top1_similarity_p10": round(float(np.percentile(top1_sim, 10)), 4),
        "filename_collision_examples": [
            [df["filename"].iloc[i], int(df["page_number"].iloc[i]),
             df["filename"].iloc[j], int(df["page_number"].iloc[j]),
             round(float(sims[i, j]), 4)]
            for i, j in zip(*np.where(np.triu(sims, k=1) >= NEAR_DUP))
        ][:5],
    }


def separation(results: dict[str, tuple[np.ndarray, pd.DataFrame]]) -> dict:
    """Can ANY global similarity threshold separate in-corpus from off-corpus?"""
    names = sorted(results)
    within, cross = [], []
    for a in names:
        ma, _ = results[a]
        for i in range(len(ma)):
            pass
        w = (ma @ ma.T)
        np.fill_diagonal(w, np.nan)
        within.append(np.nanmax(w, axis=1))
    for a in names:
        ma, _ = results[a]
        for b in names:
            if a == b:
                continue
            mb, _ = results[b]
            cross.append((ma @ mb.T).max(axis=1))
    within_all = np.concatenate(within)
    cross_all = np.concatenate(cross)
    return {
        "within_course_top_neighbour_min": round(float(within_all.min()), 4),
        "within_course_top_neighbour_p10": round(float(np.percentile(within_all, 10)), 4),
        "off_corpus_max_similarity_p90": round(float(np.percentile(cross_all, 90)), 4),
        "off_corpus_max_similarity_max": round(float(cross_all.max()), 4),
        "separable_by_single_threshold": bool(
            within_all.min() > np.percentile(cross_all, 90)
        ),
    }


def main() -> None:
    files = sorted(glob.glob(str(DATA / "data" / "*" / "*_pages.parquet")))
    results: dict[str, tuple[np.ndarray, pd.DataFrame]] = {}
    rows = []
    for f in files:
        p = Path(f)
        results[p.parent.name] = load(p)
        rows.append(audit(p))

    out = {"protocol": {"near_dup_threshold": NEAR_DUP,
                        "test": "page-as-query, within-course, stored embeddings only"},
           "per_course": rows,
           "separation": separation(results),
           "totals": {
               "courses": len(rows),
               "pages": sum(r["pages"] for r in rows),
               "near_duplicate_pairs": sum(r["near_duplicate_pairs_at_0.99"] for r in rows),
           }}

    print(json.dumps(out, indent=2))
    (DATA / "silicus_index_audit.json").write_text(json.dumps(out, indent=2))
    print("\nwritten:", DATA / "silicus_index_audit.json")


if __name__ == "__main__":
    main()
