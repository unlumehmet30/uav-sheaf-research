# Compliance checklist

Legend: ✅ done and verified · ⚠️ done with a stated limitation · ❌ not done. "Evidence" gives the file or section.
This file was written by the AI assistant that built the project; the author must re-check each line before submission.

## A. HW1 assignment ("From Curiosity to Scientific Discovery")

| # | Requirement | Status | Evidence / remark |
|---|---|---|---|
| 1 | Choose ONE AI research problem | ✅ | UAV position anomaly vs communication failure (Report §1–2) |
| 2 | Problem discovery: precise problem, how discovered, why interested, who is affected, evidence, why unsolved, root cause vs symptom | ✅ ⚠️ | Report §1–2. Evidence of existence = literature statements + our *simulation* result; no field data |
| 3 | Intensive literature review: ≥10 publications critically compared | ✅ | 20 matrix entries + 2 channel-model papers (Report §3, `literature/literature_matrix.md`, Table 1) |
| 3a | Which methods succeed/fail, conditions, why | ✅ | Report §3 "Comparative analysis"; matrix columns |
| 3b | Assumptions, biases, dataset limits, contradictions | ✅ | Report §3; `literature/gap_analysis.md` §2 |
| 3c | Reproducibility; could the gap reflect an incomplete search? | ✅ ⚠️ | Search protocol and its limits in §3 and `literature/search_log.md`. **IEEE Xplore / ACM DL not queried natively; most items abstract-level** |
| 4 | Research gap: one precise gap, supporting publications, why it matters | ✅ | Report §4 |
| 5 | Novel solution: approach, reasoning, new vs combination vs application, simpler alternatives, weakest assumption | ✅ | Report §5 (originality ledger in `literature/gap_analysis.md` §5); weakest assumption: Gaussian sensor model / authors' simulator (§7, Reflection 5) |
| 6 | Feasibility: data, equipment, software, expertise, time, funding; design, baselines, metrics; ethics; what is beyond capability | ✅ | Report §6–7 |
| 7 | Validation: falsifiable hypothesis, success criteria, what disproves, bias/overfitting/alternatives/reproducibility, negative results | ✅ | Report §8; executed in §9 |
| 8 | Impact: who benefits, harms, new questions | ✅ | Report §9 "Expected scientific impact" |
| 9 | Required sections: title, abstract (200–250 words), introduction, problem statement, critical review, gap, solution, methodology, feasibility/limitations, expected results/impact, references | ✅ | Report; abstract = 242 words (counted by script) |
| 10 | Length 5–8 pages excluding references and optional visuals | ⚠️ | ≈7.8 pages main text on A4, 10 pt, 17 mm margins (references ≈0.8 page, appendix figures 3 pages; total PDF 12 pages). **If the course requires 11–12 pt, ≈1–1.5 pages must be cut** (candidates: Table 1, Table 5, Section 9 "Other experiments") |
| 11 | Databases, keywords, inclusion/exclusion documented | ✅ | Report §3; `literature/search_log.md` |
| 12 | Do not fabricate citations | ✅ ⚠️ | All 22 records checked against arXiv API / Crossref / publisher pages (one wrongly recalled DOI was caught and corrected). Details not read in full text are flagged in the matrix |
| 13 | Researcher's reflection: all five questions | ✅ | Report §11 |
| 14 | Academic integrity: explain AI assistance per course policy | ⚠️ | AI-assistance paragraph present; **author must insert the course-policy reference** and verify claims |
| 15 | Bonus: clear diagram / prototype / visual | ✅ | Figure A1 (architecture), Figures A2–A9, working Streamlit dashboard |
| – | Placeholders to fill by the author | ⚠️ | name, course/instructor (report header), policy reference |

## B. Evaluation criteria (self-assessment, not a grade)

| Criterion (points) | Where addressed | Weak points |
|---|---|---|
| Problem significance and originality (15) | §1, §2, §5 ledger | originality is mainly the protocol and the negative-leaning finding, not an algorithm |
| Depth and critical quality of review (25) | §3, matrix, gap analysis | 3 full-text reads only; IEEE/ACM coverage; classical cooperative-localisation fault-tolerance literature not reviewed |
| Research-gap justification (15) | §4, search log | "not found", not "does not exist" |
| Novel solution and scientific reasoning (20) | §5 | sheaf-specific component showed no benefit (reported) |
| Feasibility, design and validation (15) | §6–8, repository | synthetic data only; 5 seeds |
| Clarity and scientific writing (10) | whole report | dense; 10 pt |
| Bonus (+10) | Fig. A1, dashboard | – |

## C. Master-prompt deliverables

| Deliverable | Status | Evidence |
|---|---|---|
| A. Literature package (sources, matrix, gap, references) | ✅ ⚠️ | `literature/`, `report/references.bib` |
| B. Source code: simulator, injection, baselines, proposed model, training, evaluation, tests | ✅ | `src/`, `experiments/`, `tests/` (89 tests pass, none skipped) |
| C. Experimental results: reproducible outputs, tables, plots, ablations, limitations | ✅ | `results/raw`, `results/tables`, `report/figures` |
| D. Interactive prototype using the real pipeline | ✅ | `app.py` (checked with Streamlit AppTest and in a browser) |
| E. Academic report, editable + PDF | ✅ | `report/report.docx`, `report/report.pdf`, `report/report.html`, sources `report/report_part*.md` |
| F. Reproducibility documentation | ✅ | `README.md`, `configs/`, `requirements.txt`, `results/env.json` |
| G. Compliance checklist | ✅ | this file |

### Simulator / experiment requirements

| Requirement | Status | Note |
|---|---|---|
| 5/10/20 UAVs, dynamic graph, noise, seeds, real/measured/reported separation | ✅ | `src/simulation`, tests |
| 9 scenarios (normal, Gaussian noise, sudden, drift, spoof-like, iid loss, burst loss, combined, topology change) | ✅ | `experiments/conditions.py` |
| Loss levels 0/10/30/50% | ✅ | |
| Labels / comm-failure masks separate; no leakage | ✅ | `tests/test_features.py` |
| Baselines 1–4 + proposed | ✅ ⚠️ | physics (two variants), GCN (+drop variant), GAT, NSD-style (own re-implementation, not original code), RA-SCM |
| Training: configs, train/val/test, episode-level split, seeds, checkpoints, logs, runtime | ✅ | `configs/`, `results/logs`, `results/checkpoints` (seed 0 committed) |
| ≥5 seeds | ✅ | seeds 0–4 |
| Metrics: PR-AUC primary; precision, recall, F1, FPR, delay, ROC-AUC, latency, params, memory | ✅ ⚠️ | memory = process-RSS delta (approximate, mostly ≈0 for these tiny models) |
| CIs; consistent operating point | ✅ | t-intervals over seeds; 5%-FPR threshold frozen on validation |
| Ablations (reliability, sheaf maps, temporal, uncertainty weights) | ✅ | E6 |
| Experiments 1–7 | ✅ | `experiments/conditions.py`, report §6, §9 |
| Dashboard: swarm view (truth vs prediction, active/lost links), controls, PR curves, comparison, FPR, performance vs loss, scores over time, latency | ✅ ⚠️ | latency table is in the results tab expander; PR curve for the chosen scenario is computed live |
| Bi et al. (2024) detector; covariance-intersection localisation | ❌ | not implemented; disclosed |
| Real-world / hardware validation | ❌ | not available; disclosed |

## D. Known issues and honest caveats

1. The pre-specified hypothesis was **not supported** and its falsification clause was met; the report says so.
2. The decision rule's per-condition part was fixed in code before the main runs; the aggregation over conditions was written down during baseline training and before any RA-SCM result was inspected (report §8).
3. Physics thresholds calibrated on the validation mixture are poorly calibrated (FPR ≈0.12 at no loss); PR-AUC is unaffected.
4. Learning-rate grid: GCN and GCN-drop chose the grid edge (0.03); RA-SCM diverged at 0.03, so its optimum is interior.
5. Ablation statements are exploratory (no pre-set thresholds).
6. Not run: GAT with edge features; real-data calibration.
