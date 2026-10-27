# Reliability-Aware Sheaf Consistency for UAV-Swarm Anomaly Detection

Research prototype for the university assignment *HW1 – From Curiosity to Scientific Discovery*.

**Research question.** Can reliability-aware sheaf neural networks distinguish genuine UAV position anomalies from
communication-induced information loss more robustly than conventional graph-based approaches under dynamic and unreliable
network conditions?

The repository contains a configurable 2-D swarm simulator with fault and communication injection, five learned detectors
(GCN, GAT, GCN with dropped links, an NSD-style sheaf baseline, and the proposed RA-SCM) plus five ablations, two non-learned
physics baselines, a reproducible training/evaluation pipeline, a Streamlit dashboard, a literature package, and the report.
**The hypothesis is tested, not assumed** — see `results/tables/results_summary.md` and the report for what actually happened,
including negative results.

> **Scope warning.** Everything here is *simulation*. No claim is made about real UAV performance. Literature
> coverage has limits stated in `literature/search_log.md` (IEEE Xplore / ACM DL were not queried through their own search
> interfaces).

<!-- RESULTS:START -->
## Results at a glance (5 seeds, simulation only)

| PR-AUC | iid 0% | iid 30% | iid 50% | burst 30% | burst 50% | rx-burst 30% | targeted 30% |
|:--|--:|--:|--:|--:|--:|--:|--:|
| Physics (naive) | 0.894 ±.025 | 0.863 ±.029 | 0.804 ±.033 | 0.605 ±.056 | 0.519 ±.057 | 0.389 ±.047 | 0.779 ±.035 |
| Physics (AoI-aware) | 0.894 ±.025 | 0.891 ±.024 | 0.888 ±.023 | 0.885 ±.023 | 0.877 ±.022 | 0.885 ±.029 | 0.890 ±.021 |
| GCN | 0.960 ±.019 | 0.958 ±.018 | 0.951 ±.016 | 0.919 ±.024 | 0.889 ±.023 | 0.929 ±.029 | 0.961 ±.016 |
| GCN (drop lost) | 0.965 ±.014 | 0.959 ±.016 | 0.949 ±.019 | 0.953 ±.015 | 0.939 ±.023 | 0.907 ±.020 | 0.986 ±.005 |
| GAT | 0.968 ±.016 | 0.963 ±.020 | 0.956 ±.021 | 0.929 ±.027 | 0.909 ±.021 | 0.943 ±.018 | 0.968 ±.018 |
| NSD-style sheaf | 0.968 ±.019 | 0.967 ±.016 | 0.959 ±.016 | 0.937 ±.012 | 0.907 ±.014 | 0.948 ±.016 | 0.968 ±.016 |
| **RA-SCM** | 0.974 ±.019 | 0.975 ±.018 | 0.975 ±.019 | 0.972 ±.020 | 0.967 ±.026 | 0.958 ±.022 | 0.988 ±.007 |

*PR-AUC, mean ± 95% t-interval over seeds; chance = 0.094. Full tables: `results/tables/results_summary.md`.*

* **Pre-specified hypothesis (RA-SCM beats the best capacity-matched conventional GNN under packet loss): not supported.**
  H1 met in 1 of 6 decision conditions (≥4 required); the interval contains 0 in 4 (≥3 falsifies).
  The practical margin (≥0.02) is reached only under 50% burst loss (+0.028 [+0.013, +0.043]).
* RA-SCM beats the age-aware physics baseline in all decision conditions (e.g. 50% bursts: +0.090 [+0.059, +0.121]).
* A consistency test that ignores staleness collapses under bursty loss (0.519 PR-AUC at 50% bursts vs 0.894 without loss).
* Ablations: the communication-reliability inputs carry the benefit (+0.088 [+0.051, +0.125] when removed at 50% bursts); learned sheaf maps show no measurable benefit.
* Not validated on any real data; see Limitations.

| model | parameters | ms per swarm step, N=5 / 10 / 20 | train time per seed [min] |
|:--|--:|:--|--:|
| Physics (naive) | 0 | 0.02 / 0.02 / 0.02 | 0.0 |
| Physics (AoI-aware) | 0 | 0.02 / 0.02 / 0.02 | 0.0 |
| GCN | 17425 | 0.02 / 0.03 / 0.08 | 1.1 |
| GCN (drop lost) | 17425 | 0.02 / 0.03 / 0.08 | 0.9 |
| GAT | 17585 | 0.02 / 0.05 / 0.14 | 1.6 |
| NSD-style sheaf | 17729 | 0.05 / 0.18 / 0.71 | 5.8 |
| **RA-SCM** | 17571 | 0.05 / 0.18 / 0.76 | 9.7 |
| − reliability info | 17377 | 0.05 / 0.17 / 0.72 | 9.6 |
| − reliability weights | 17377 | 0.05 / 0.17 / 0.71 | 7.8 |
| − sheaf maps (F = I) | 16515 | 0.04 / 0.13 / 0.52 | 5.9 |
| − temporal (GRU) | 11043 | 0.04 / 0.17 / 0.75 | 9.0 |
| − maps − weights (MPNN-E) | 16321 | 0.04 / 0.12 / 0.47 | 4.8 |
<!-- RESULTS:END -->

## Status of every component

| Component | Status |
|---|---|
| Simulator (truth / measured / reported separation, 5/10/20 UAVs, formations, trajectories, seeds) | implemented, unit-tested |
| Anomaly injection (sudden, drift, spoof-like group offset, mixed) | implemented, unit-tested |
| Communication (iid, Gilbert–Elliott burst, receiver-correlated burst, targeted blackout, link blockage) | implemented, unit-tested |
| Leakage barrier (`Observation`) and causal feature construction | implemented, unit-tested (hidden-field substitution test, future-perturbation test) |
| GCN, GAT layers | implemented, **cross-checked numerically against PyTorch Geometric** `GCNConv` / `GATConv` |
| Sheaf layer (NSD-style, weighted, affine) | implemented; Laplacian identity, explicit-coboundary equality, PSD and zero-weight tests |
| RA-SCM + 5 ablations | implemented, tested for shape, causality and ablation behaviour |
| Physics baselines (naive / AoI-aware) | implemented, unit-tested |
| Training / evaluation pipeline, 5 seeds, paired statistics | implemented; results in `results/` |
| Dashboard (`app.py`) | implemented; runs on the real pipeline; checked headlessly with Streamlit `AppTest` |
| Bi et al. (2024) semidefinite detector, covariance-intersection cooperative localisation | **not implemented** (discussed as limitation) |
| Real-flight / hardware data | **not available**; simulation only |

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate        # Python >= 3.11 (developed with 3.13.5)
pip install -r requirements.txt
```

PyTorch Geometric is optional (only needed by the two cross-check tests; they are skipped if it is absent).

## Run

All commands are run from the repository root.

```bash
# 1. unit tests (simulation, fault injection, graph construction, metrics, models)
python -m pytest -q

# 2. hyper-parameter selection (learning rate only; separate tuning seed + 'tune' split, never touches test data)
python -m experiments.tune --epochs 15
python -m experiments.tune --epochs 15 --extra-lrs 0.03     # optional grid extension (merges into results/tables/tuning.csv)

# 3. main experiments: one process per evaluation seed (training + all test conditions)
for s in 0 1 2 3 4; do python -m experiments.run_main --seed $s & done; wait

# 4. aggregate, statistics, figures, latency
python -m experiments.latency
python -m experiments.aggregate
python -m experiments.make_figures
python -m experiments.update_readme        # refreshes the 'Results at a glance' block from results/tables
python report/build.py                      # report.html / report.pdf (needs Chrome) / report.docx (needs pandoc >= 2.11)

# 5. dashboard
streamlit run app.py
```

`python -m experiments.run_main --seed 0 --models physics_naive physics_aoi gcn rascm --quick` runs a few-minute smoke test
that is **not** used for any reported number.

## Reproducibility notes

* Every random quantity is a function of `(config, seed)`; independent `SeedSequence` streams make episodes that differ only in the
  packet-loss level share trajectories, sensor noise and anomaly schedules (paired comparisons).
* Train / validation / test / tuning episodes come from disjoint integer seed ranges (`src/graph/dataset.py`, tested).
* Per-seed outputs: `results/raw/metrics_seed*.csv`, `results/raw/curves_seed*.json`, `results/logs/*.json` (training histories),
  checkpoints in `results/checkpoints/`.
* Environment of the reported run: `results/env.json` (CPU only, Apple M1, torch 2.6.0, Python 3.13.5).
* Hyper-parameters: `configs/default.yaml`, learning rates in `configs/tuned_lr.yaml` (selected on the tuning split only).
* Models are capacity-matched: GCN/GAT/GCN-drop/NSD widths are chosen so that their parameter count is within 10% of RA-SCM
  (checked by a test). Ablations are *removals* and therefore have fewer parameters; counts are reported.
* All learned models see the same raw information. GCN/GAT/NSD receive edge information as neighbourhood statistics appended to
  the node vector (they have no edge-feature input); RA-SCM and its ablations consume edge features directly. The MPNN-E control
  (no sheaf maps, no weights) isolates this difference.
* Operating point: for every model the detection threshold is the 5%-false-positive-rate point on the pooled validation split,
  then frozen for all test conditions.

## Repository layout

```
configs/        default.yaml (all simulation + training settings), tuned_lr.yaml (output of tuning)
src/simulation  swarm dynamics, episode generation (real / measured / reported states)
src/anomalies   anomaly schedules      src/communication  loss processes
src/graph       observation -> tensors (features.py), datasets and seed discipline (dataset.py)
src/models      dense GCN / GAT / sheaf layers, detectors + ablations, physics baselines
src/training    trainer         src/evaluation  metrics, runtime helpers
src/visualization  Plotly figure builders used by app.py
experiments/    tune.py, run_main.py, conditions.py (the 7 experiments), aggregate.py, latency.py, make_figures.py
tests/          pytest suite     literature/  search log, matrix, bibliography analysis
report/         report sources, figures, references.bib      app.py  Streamlit dashboard
```

## Limitations (short form; details in the report)

Synthetic sensors and a lightweight kinematic model; one hand-designed channel family; 5 seeds (t-intervals with 4 degrees of
freedom are wide); a single simulator authored by the same people who design the proposed model (risk of benchmark bias);
physics baselines use the simulator's nominal sensor specifications; learned models see 10-UAV training swarms only; latency is
amortised CPU throughput, not embedded-hardware latency.

## AI-assistance statement

The research design, code and text of this repository were produced with substantial assistance from an AI model
(Claude Sonnet 5.5 via Claude Code). The author is responsible for verifying every claim and citation. Details: see the
*AI assistance* paragraph in the report.
