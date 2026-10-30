
## 11. Researcher's reflection

**1. The Skeptic — "this research is unnecessary."** In our controlled simulation a consistency test that treats stale reports as current falls from {{m:physics_naive:iid_0:pr_auc}} to {{m:physics_naive:burst_50:pr_auc}} PR-AUC under bursty loss ({{m:physics_naive:nodeburst_30:pr_auc}} under receiver-correlated loss), while the swarm detectors we reviewed assume reliable delivery or trust the communication topology. So the confusion is real *in simulation*. The expert is partly right, though: an age-aware test restores most of the loss ({{m:physics_aoi:burst_50:pr_auc}}) and a plain GAT with the same inputs reaches {{m:gat:burst_50:pr_auc}}; the sheaf machinery is not what fixes the problem. What is necessary is the controlled evaluation, not the architecture.

**2. The Failure — "after a year the hypothesis is wrong."** By our own pre-specified rule it is already wrong in its strong form. What remains: a reproducible benchmark with paired seeds and an age-aware control; the finding that the reliability channel carries the benefit ({{da:burst_50:rascm_no_rel}} when removed) while learned sheaf maps show none; the identifiability limit for small swarms (5 UAVs: {{m:rascm:gen_n5:pr_auc}}); the failure of mixed-condition thresholds under noise shift; tested code and a dashboard.

**3. The Originality — "remove everything borrowed."** Sheaf Laplacians, NSD-style layers, GCN/GAT, uncertainty weighting, Gilbert–Elliott loss and physical consistency tests are all borrowed. What is ours: (a) framing the task as *confounded evidence* (missing versus wrong) with explicit observability conditions; (b) delayed-message semantics that make every architecture read only communicated information, so comparisons cannot leak; (c) the protocol — loss, burst and targeted-blackout confounding, frozen operating point, paired seeds, age-aware physics control, component ablations; (d) the empirical findings, including the negative ones. We do not claim a new algorithm.

**4. The Reality — €500, one computer, three months.** The experiments reported here ran on one CPU laptop ({{n:wall_min_per_seed}} min of training per seed, five seeds in parallel) and cost no hardware money. With €500 the most meaningful addition is calibration: measure real packet-loss traces (ESP32 boards, ≈€60), UWB ranging and GNSS noise (≈€250) and re-run E1–E4 with fitted parameters. The first month would go to literature and tests, the second to the simulator and baselines, the third to experiments and writing.

**5. The Intellectual Honesty — "strongest argument against."** A 20-line age-aware physics test or a plain GAT with the same inputs does nearly as well, learned sheaf maps add nothing measurable, and the simulator and baselines were written by the same people who designed the proposed model. I would change my mind if, on measured loss and sensor noise, RA-SCM beat the best conventional GNN by ≥0.02 with an interval above 0 in at least four conditions *and* the identity-map ablation fell behind by ≥0.01 — or, in the opposite direction, if the age-aware physics test matched the learned models on real traces.

**AI assistance (declared as required by the academic-integrity section of the HW1 brief).** An AI model (Claude Sonnet 5.5 via Claude Code) was used for literature-search queries, code, experiment orchestration, figures and drafting. Bibliographic records were machine-checked against the arXiv API, Crossref and publisher pages; full-text reading covered key sections of three UAV papers only, the rest at abstract level plus background knowledge, as flagged in the literature matrix. All numbers in this report are inserted from result files produced by the repository code. The author remains responsible for verifying every claim and citation before submission.

<div class="pagebreak"></div>

## Appendix A. Figures (optional visuals, not counted in the page limit)

![**Figure A1.** Architecture and information flow. Simulator ground truth never crosses the observation barrier; RA-SCM consumes node and edge features and reads neighbour states from the time of the last delivered packet.](figures/fig_architecture.png){width=100%}

![**Figure A2.** PR-AUC versus packet loss (mean ± 95% interval over 5 seeds); top: full range, bottom: zoom on the learned models.](figures/fig_pr_auc_vs_loss.png){width=86%}

![**Figure A3.** Paired PR-AUC difference RA-SCM − reference with 95% intervals (blue: pre-specified H1 criterion met).](figures/fig_hypothesis_forest.png){width=88%}

![**Figure A4.** Ablations: paired PR-AUC difference full RA-SCM − ablated variant.](figures/fig_ablation.png){width=70%}

![**Figure A5.** False-positive rate at the threshold frozen on validation data (dotted line: 5% target).](figures/fig_fpr_vs_loss.png){width=75%}

![**Figure A6.** PR-AUC under changed swarm size, unseen trajectory and unseen formation (loss 30%).](figures/fig_generalization.png){width=80%}

![**Figure A7.** Precision–recall curves (seed 0) for four conditions.](figures/fig_pr_curves.png){width=100%}

![**Figure A8.** Median detection delay by anomaly type, without loss and with 30% loss (detected UAVs only).](figures/fig_delay.png){width=85%}

![**Figure A9.** Amortised CPU inference time and parameter counts.](figures/fig_latency.png){width=80%}
