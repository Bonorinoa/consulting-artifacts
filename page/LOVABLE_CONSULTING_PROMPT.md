# New page: `/consulting`

## Read this first — how I want you to work

I care about the outcome, not about you following my notes literally. So:

1. **Before writing code, give me a short plan** (5–10 lines) and **flag anything you would do
   differently.** If you have a better idea for the visualization, the animation, or the copy,
   say so and propose it. The design below is a considered starting point, not a constraint.
2. If you disagree with a *structural* decision (the three stages, the split layout), make the
   case — but tell me rather than silently changing it.
3. Otherwise, build it.

**The single thing to optimize for is attention.** The most common failure here is a page that
is *complete* — every section filled, every stage explained — and therefore unreadable. More
content feels thorough and it costs you the visitor. Be ruthless:

- If a sentence can be cut without losing the offer, cut it.
- One idea per screen-area. Do not explain what the diagram already shows.
- Whitespace is not wasted space. Short lines are not incomplete lines.
- If you find yourself adding a section to be safe, don't.

Assume the visitor gives this page about fifteen seconds before deciding to read or leave.

---

## What this is

A new page on my existing personal site, in the **Academic** visual world. It is the
consulting / services page: **independent review at three stages of an empirical research
pipeline.**

Reference implementation (study I built to test the layout — match its feel, and improve on it):
`~/Hermes/Projects/consulting-artifacts/page/consulting-v3.html`

## The structure

A **split panel**: clickable stage choices on the left, the detail for the selected one on the
right. Three stages:

| # | Stage | Scope line |
|---|---|---|
| 01 | Upstream | define the construct · generate measures · process data |
| 02 | **Midstream** (default selected) | specification & multiverse analysis · admissible set M\* |
| 03 | Downstream | estimand · estimator · identified range [L,U] · robustness |

Midstream is selected on first paint, so the lead offer is readable **without a click**.

## Copy — use verbatim, then improve if you can

Panel elements, in order, for each stage: **kicker → headline → one body paragraph → reduction
line → Evidence row.** That is the whole panel. Do not add a subtitle, a second paragraph, a
bullet list, or a "how it works" block.

**02 · midstream** *(default)*
- Headline: Is our measure entitled to the claim we're making?
- Body: Construct validity as partial identification: the admissible measurement set M\*, and the range of conclusions your assumptions actually permit. An empty set is a finding.
- Reduction: **The reduction:** which measure is load-bearing — remove it and the conclusion moves — and which to drop.
- Evidence: Construct-Identified Inference · cvprofiles (open source) · Interactive demo — in build

**01 · upstream**
- Headline: We need to measure something we can't observe yet
- Body: I define the construct, propose candidate measures, and build the processing chain — with provenance on every transformation, so a reviewer can see where each number came from.
- Reduction: **The reduction:** which measure is worth building first.

**03 · downstream**
- Headline: Is the number defensible — and what do we do?
- Body: Estimand, estimator, estimate, then the robustness work — including an explicit statement of what the evidence does not establish.
- Reduction: **The reduction:** what to collect next to shrink the range.

Header:
- Kicker: `§ Independent review`
- Title: `Consulting`
- Lede: Independent review at three stages of an empirical pipeline — criteria *frozen before the result*, so the finding is one you can act on.

Below the split, one CTA: **Describe a decision** — with the note *Twenty minutes. Deadline and
cost of being wrong, not a pitch deck.*

Then a short **How I work** band carrying this line, which is the thesis of the whole page:
> "It is useless to quantify uncertainty without a strategy to reduce it."

Then a fixed **three-item** writing rail (Substack / Journal / Column — three, never a
carousel), then a short intake form (What decision? / Deadline / Cost of being wrong / optional
email), then the footer.

## Visual cues

Use the site's existing Academic tokens — **do not invent a palette.**

- Paper `hsl(38 44% 94%)`, paper-deep `hsl(36 36% 86%)`, ink `hsl(24 40% 8%)`,
  muted ink `hsl(28 18% 28%)`, rule `hsl(36 24% 72%)`, accent oxblood `hsl(11 56% 27%)`
- Type: **Fraunces** for display and body; **Geist Mono** for kickers, numbers, and the small
  uppercase labels. Radius 2px. Hairline rules at 1px.
- Kickers are mono, ~11px, uppercase, letter-spaced ~0.2em, oxblood.
- Plates: hairline border, 2px radius, mono stage number in oxblood, serif stage name, muted
  scope line. Selected plate gets an oxblood border and an offset hard shadow
  (`5px 5px 0 0 hsl(11 56% 27% / .16)`); unselected drop to ~50% opacity.
- The split: `grid-template-columns: minmax(290px,.86fr) 1.14fr`, one shared border, left pane
  on a paper-deep wash with a hairline divider.

**The one piece of motion.** Consecutive stage plates are joined by a short **dashed vertical
connector** in the gap between them, aligned near the left, under the numbers. It has two layers
and this distinction matters:

- **The connection is always visible** — a faint dashed line, ~40% opacity. The three stages must
  read as one pipeline in a static frame, under `prefers-reduced-motion`, and if the animation
  never runs.
- **A small glint travels down it, intermittently** — bright, ~4px, fading in and out, visible
  for roughly 10% of a ~7s cycle, staggered ~1.1s between the two gaps so the pulse appears to
  move 01 → 02 → 03. It should suggest information propagating between stages.

If you have a better way to express "these three are one pipeline, and something moves between
them," use it. Keep it subtle: this is the only motion on the page.

Under `prefers-reduced-motion`, keep the dashed connection and remove the glint.

## Hard constraints (do not break the rest of the site)

- Use the **Academic** world (`useWorld('academic')`). Do not add a new `data-world`.
- Do not restyle the landing page, `/academic`, or `/build`.
- Do not add a third FolioCard to the landing page — the two-volume layout stays. At most one
  quiet serif line under the folios linking to `/consulting`.
- Do not add a third option to the `ModeToggle` pill.
- Add `/consulting` to the sitemap.
- No prices, no booking calendars, no testimonials block, no newsletter signup.
- Do not invent client names, logos, metrics, or outcomes. Where a warrant does not exist yet,
  the link says **"in build"** and is not clickable.
- No orbs, blobs, or particle effects. No graph/physics library — this is a fixed layout.
- Keep it light and fast: no heavy dependencies.

## Definition of done

- `/consulting` renders in the Academic tokens; Midstream selected on load with the full lead
  copy visible without a click.
- Clicking a stage swaps the right panel; nothing else on the page moves.
- The dashed connector is visible between stages, with the glint animating subtly.
- The page reads as **deliberately sparse**. If you can remove something and it still works,
  remove it.
- Then tell me what you changed from this brief, and why.
