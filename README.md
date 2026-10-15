# Consulting Artifacts

Public, reproducible deliverables from an independent research-methods consulting practice
(measurement and inference for empirical research). Each artifact is a method demonstration —
an audit, a reduction curve, a novelty check, or the design work behind them — with its protocol
stated before its results and its boundary made explicit.

## Why this exists

The practice sells *decisions*, not methods: which measure to build, which measure is
load-bearing, and whether a number survives the assumption it depends on. A claim is only as
good as the evidence behind it, so every deliverable here is built to be checked — frozen
criteria, thresholds scanned rather than tuned, negative results reported, and a stated limit.
These are **Class A advisory demonstrations**, not independent assurance and not certification.

## What's here

| Path | What it is |
|---|---|
| `01-fit-to-rely/` | A release-decision audit of a deployed retrieval index (`Silicus-TA-2.0`). Verdict: fit for in-corpus Q&A with a human checking citations; **not** fit as an unsupervised source of verified citations. Fully offline and reproducible. |
| `02-midstream/` | The reduction curve: which measurement is load-bearing. Re-runs `cvprofiles` over menu subsets with the network and β held fixed, and reports how the headline range `[L,U]` responds. |
| `scripts/` | The audit scripts: `audit_index.py` (integrity + separability), `ambiguity.py` (citation collisions + gate check), `reduction_curve.py` (the midstream curve). |
| `novelty-audit-2026-09-12.md` | Adversarial novelty audit of "construct-identified inference": every component piece predates it; the *conjunction* (menu + nomological restrictions → `M*` → `[L,U](β | M*)` + software) was not found in print. |
| `sketches/` | Three design variants for presenting the audit (coverage/allocate, missing-first, protocol/commit), each with its trade-offs. |
| `page/` | The `/consulting` page mockups (`consulting-v1/-v2/-v3.html`) and the Lovable briefs that shipped them. |
| `demo-shapes.html`, `downstream-options.html` | Design explorations for the three stage demos. |

## Reproduce the audit

The `01-fit-to-rely` audit is offline and API-free — no key, no network. From this repo:

```bash
git clone https://github.com/Cognitio-EDU/Silicus-TA-2.0
git -C Silicus-TA-2.0 checkout 4c58084     # audited revision
uv venv .eval --python 3.11 && uv pip install --python .eval/bin/python pandas pyarrow
.eval/bin/python scripts/audit_index.py    # integrity + separability
.eval/bin/python scripts/ambiguity.py      # citation collisions + gate check
```

## Verify it works

```bash
.eval/bin/python scripts/audit_index.py    # expects self-recall@1 = 1.000 (706/706), MRR = 1.000
```

The audit's own verdict is in `01-fit-to-rely/artifact.md`; the raw numbers are in
`silicus_index_audit.json` and `ambiguity_register.json`.

## Deeper documentation

- `01-fit-to-rely/artifact.md` — the full audit: decision, findings, verdict, and boundary.
- `novelty-audit-2026-09-12.md` — the novelty claim, decomposed and verified against prior art.
- Each `sketches/*/README.md` — the design stance and trade-offs for that variant.
- `page/LOVABLE_CONSULTING_PROMPT.md` — the brief behind the `/consulting` page.
