# Is this retrieval layer fit to rely on?
### A release-decision audit of a deployed course-assistant index

**Disclosure.** Demonstration with public code. The system audited is one I built
(`Cognitio-EDU/Silicus-TA-2.0`, audited revision `4c58084`). This is an advisory
self-audit, **not** independent assurance, and not a certification. Everything below
is reproducible offline from the repository — no API key, no network.

---

## 1. The decision

Can this deployed assistant be relied on to put the page an answer actually lives on
in front of the model — and to supply a citation a reader can verify?

Not "is RAG good." The concrete question: **if a student reads a bracketed page
citation and opens that page, will it support the claim?**

---

## 2. What a wrong answer costs

The expensive failure is not an obviously bad answer — it is a fluent one with a
plausible citation. A student cannot audit a 1024-dimension similarity score; they
trust the citation. So the failure is silent, and it propagates into coursework.

A second cost is quieter: if near-neighbour pages crowd the retrieved window, the
second and third relevant documents never reach the model. Answer quality drops
without any visible error.

---

## 3. What existed before this audit

`Silicus-TA-2.0` is a Streamlit RAG assistant: students chat with course PDFs,
professors manage the corpus. Page text is OCR'd, embedded with `mistral-embed`
(1024-d, L2-normalised) and committed as parquet. Retrieval takes the **top 10**
pages by cosine similarity and injects them into the prompt as "Course excerpts,"
with the instruction to cite pages in brackets.

**The repository shipped no retrieval evaluation of any kind.** That gap is the
reason for this audit.

---

## 4. The frozen question

Declared before results were computed, so the criteria could not drift:

| | |
|---|---|
| **Corpus** | all 4 courses, 706 pages, 20 + 11 + 5 + 5 files |
| **Test A (integrity)** | page-as-query: does each page retrieve *itself* first within its own course? |
| **Test B (citation)** | how many distinct page pairs score high enough that a reader could confuse them? |
| **Test C (abstention)** | can one similarity threshold separate on-corpus from off-corpus pages? |
| **No fitting** | thresholds are *scanned and reported*, never tuned to produce a verdict |

---

## 5. Findings

### 5.1 The index itself is sound

Every one of the 706 pages retrieves itself at rank 1.

```
self-recall@1   = 1.000   (706 / 706)
MRR             = 1.000
pages failing to self-retrieve in own top-10 = 0
```

No corruption, no collapsed vectors, no truncation. Any failure below is about
*relevance*, not about the index being broken.

> Process note: three hypotheses of "broken index" were tested and **falsified** before
> this conclusion — lossy persisted embeddings (they are intact 1024-d float32, unit
> norm), and a sort-direction inversion in the retrieval call (`scipy.spatial.distance.cosine`
> returns *distance*, so `1 - cosine` is similarity and both call sites sort correctly).
> The negative results are the reason the positive one is trustworthy.

### 5.2 Citations are effectively unambiguous

Distinct-page pairs at or above a similarity threshold:

| Course | pages | ≥0.99 | ≥0.95 | ≥0.93 | ≥0.90 |
|---|---:|---:|---:|---:|---:|
| econ101 | 149 | 0 | 0 | 22 | 179 |
| econ167 | 338 | 0 | 2 | 36 | 263 |
| econ57 | 122 | 0 | 7 | 24 | 91 |
| math387 | 97 | 0 | 0 | 9 | 76 |

No pair reaches 0.99. At ≥0.95 there are 9 pairs in 706 pages, and 8 of the 9 are
*within a single file* — repeated or summary slides — which the `[file – p.N]`
citation format already disambiguates.

The first genuinely cross-file collisions appear at ≥0.93, and they are
**adjacent lectures on one topic**, which is what you would expect:

- `13 - Liquidity Preference & LM Curve p.4` ↔ `14 - IS-LM curve p.1` — 0.949
- `14 - IS-LM curve p.7` ↔ `16 - Mundell-Fleming Model p.2` — 0.948
- `Lecture_2.pdf p.2` ↔ `Lecture_3.pdf p.2` — 0.952

**Verdict on 5.2: acceptable.** Citations identify a page. The residual risk is
top-10 crowding, not a reader being misled about *which* page was meant.

### 5.3 The substantive finding: similarity is not a relevance signal, so there is no abstention gate

For each page, its strongest neighbour **inside** its course versus **outside** it:

| | min | p10 | median | p90 | max |
|---|---:|---:|---:|---:|---:|
| best on-corpus neighbour | 0.751 | 0.863 | **0.909** | — | 0.977 |
| best **off**-corpus neighbour | 0.742 | 0.788 | **0.828** | 0.879 | **0.950** |

The distributions overlap almost completely. The worst case is decisive:

> **33 of 706 pages (4.7%) are more similar to a page in a *different* course than to
> any page in their own.**

`separable_by_single_threshold = false`.

An off-topic page scores 0.83 at the median. That number carries almost no
information about whether the page is relevant — page-level embeddings of
dense course notes largely encode *register* ("this is a dense academic page"),
not topic.

**Consequence for the system as shipped:** retrieval applies **no threshold** — it
takes 10 pages unconditionally and labels them "Course excerpts." Since similarity
cannot supply a relevance gate, the entire abstention burden falls on the generator's
prompt instruction ("If not, say you are unsure"). A student in econ101 who asks an
econ167 question still receives ten econ101 pages, presented as evidence, with an
instruction to cite.

---

## 6. Decision

**Fit for in-corpus question answering with a human able to check the citation.
Not fit as an unsupervised source of verified citations.**

The failure mode is not corruption — it is *confidence without signal*: the system
always looks like it retrieved something relevant, because 0.83 never looks like
"no match."

Recommended remediation, cheapest first:

1. **Measure abstention before tuning it.** Embed a labelled query set (in-corpus
   and off-corpus) — the missing measurement, and the reason no threshold exists today.
2. **Do not gate on raw cosine.** The overlap above says a cutoff will either admit
   off-corpus content or reject legitimate pages. If a gate is needed, calibrate it
   against the labelled set, not against intuition.
3. **Consider a reranker or hybrid BM25 + dense retrieval** for the top-10 window.
   Lexical overlap (formula names, "Mundell-Fleming") discriminates where the
   embedding does not.
4. **Surface the score in the UI.** A student seeing "best match 0.61" learns
   something the current interface hides.

---

## 7. Boundary — what this does not establish

- **No generation was run.** Nothing here measures whether answers are correct.
- **No user queries were embedded.** Self-retrieval is a *consistency* test and an
  **upper bound** on real retrieval quality: a real question is never as close to a
  page as that page's own text.
- **The negative control is weak, and this cuts against my own finding.** "Off-corpus"
  here means *a neighbouring course* — math notes against econ notes. Two STEM
  course-note corpora resemble each other, so 0.828 is an inflated floor. Against a
  genuinely unrelated corpus the separation would look better, and I have not tested
  that. Treat 5.3 as "similarity does not separate *course-note corpora*," which is
  the realistic case for this tool, not as "similarity never works."
- **One revision, one embedding model, four courses.** Not a benchmark.

---

## 8. Reproducing this

```bash
git clone https://github.com/Cognitio-EDU/Silicus-TA-2.0
git -C Silicus-TA-2.0 checkout 4c58084     # audited revision
uv venv .eval --python 3.11 && uv pip install --python .eval/bin/python pandas pyarrow
.eval/bin/python scripts/audit_index.py    # integrity + separability
.eval/bin/python scripts/ambiguity.py      # citation collisions + gate check
```

Artifacts in this folder: `silicus_index_audit.json`, `ambiguity_register.json`,
`AUDITED_COMMIT.txt`.

*Prepared as a demonstration of an evaluation method — frozen criteria, a scan rather
than a fit, negative results reported, and the boundary stated. The method transfers
to any retrieval-backed system; only the corpus changes.*
