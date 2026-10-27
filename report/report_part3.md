## 9. Results obtained and expected impact

All numbers below are produced by the repository pipeline (`experiments/run_main.py`, {{n:n_seeds}} seeds, 26 test conditions × 40 episodes, positive rate {{n:pos_rate}} = chance PR-AUC) and inserted into this report automatically from `results/tables/`. Hardware: {{n:cpu}}, CPU only. **These are synthetic-simulation results; they do not demonstrate real-world UAV performance.** Figures are in Appendix A.

{{tbl:main}}

*Table 3. PR-AUC, mean ± 95% $t$-interval half-width over 5 seeds (E1–E4). Chance level = {{n:pos_rate}}.*

**Confusion between missing and wrong information is real in the simulator, and mostly a bookkeeping problem (E2–E4).** A consistency test that treats stale reports as current keeps {{m:physics_naive:iid_0:pr_auc}} PR-AUC without loss, but falls to {{m:physics_naive:burst_50:pr_auc}} under 50% burst loss and {{m:physics_naive:nodeburst_30:pr_auc}} under receiver-correlated loss. Modelling the age of the report (AoI-aware physics) removes most of this damage ({{m:physics_aoi:burst_50:pr_auc}} and {{m:physics_aoi:nodeburst_30:pr_auc}}). Under *iid* loss the naive test degrades less ({{m:physics_naive:iid_50:pr_auc}} at 50%); a plausible but untested explanation is that stale errors are common-mode in a rigidly moving formation and largely cancel in the symmetric statistic.

**Learned graph models beat both physics tests; RA-SCM has the highest mean in every column of Table 3, but by small margins (E1–E4).** With identical inputs, GCN, GAT, GCN-drop and the NSD-style sheaf reach {{m:gcn:iid_0:pr_auc}}–{{m:nsd:iid_0:pr_auc}} without loss versus {{m:physics_aoi:iid_0:pr_auc}} for physics; RA-SCM reaches {{m:rascm:iid_0:pr_auc}}. Its PR-AUC changes by {{dd:rascm:iid_0:iid_50:pr_auc}} from 0% to 50% iid loss and {{dd:rascm:iid_0:burst_50:pr_auc}} under 50% bursts, versus {{dd:gat:iid_0:burst_50:pr_auc}} (GAT), {{dd:gcn:iid_0:burst_50:pr_auc}} (GCN) and {{dd:gcn_drop:iid_0:burst_50:pr_auc}} (GCN-drop). Table 4 gives the pre-specified test.

{{tbl:hypothesis}}

*Table 4. Paired PR-AUC difference RA-SCM − reference (mean [95% CI over seeds]); H1 requires CI > 0 and mean ≥ 0.02.*

**Decision.** H1 is met in {{n:h1_count}} of {{n:h1_total}} conditions (≥4 required) and the interval contains 0 in {{n:ci_zero_count}} (≥3 falsifies). By the rule fixed beforehand, **H1 is not supported and its falsification clause is met**: RA-SCM is not shown to be a general improvement over the best of four capacity-matched conventional GNNs under packet loss. The reference is deliberately harsh (a per-seed maximum over four noisy models is biased upward relative to one pre-chosen baseline); against single baselines RA-SCM often has a positive interval (vs GCN at 50% bursts {{dh:burst_50:gcn}}), but most margins stay below 0.02. *Post hoc observations that survive:* RA-SCM beats the AoI-aware physics test in {{n:h1_total}} of {{n:h1_total}} conditions ({{dh:burst_50:physics_aoi}} at 50% bursts); its advantage over the best conventional GNN is practically relevant only under 50% bursts ({{dh:burst_50:best_conventional}}) and absent without loss ({{dh:iid_0:best_conventional}}), which points to loss handling rather than raw capacity. The FPR clause is met (FPR at 50% iid loss {{m:rascm:iid_50:fpr}} for RA-SCM, {{m:gat:iid_50:fpr}} for GAT).

**Other experiments.** *Noise (E2):* at ×3 noise all models lose accuracy (RA-SCM {{m:rascm:noise_3:pr_auc}}, NSD {{m:nsd:noise_3:pr_auc}}, GAT {{m:gat:noise_3:pr_auc}}) and the frozen thresholds fail (FPR {{m:rascm:noise_3:fpr}} for RA-SCM, {{m:gcn_drop:noise_3:fpr}} for GCN-drop). *Anomaly type (E4):* sudden jumps are nearly always detected; drift and spoofing are harder (spoof PR-AUC at 30% loss: RA-SCM {{m:rascm:type_spoof_30:pr_auc}}, others {{m:gcn:type_spoof_30:pr_auc}}–{{m:nsd:type_spoof_30:pr_auc}}). *Targeted blackout (E4):* it barely hurts any learned model (RA-SCM {{m:rascm:targeted_30:pr_auc}}), because a UAV's own residuals still carry evidence. *Generalisation (E5):* trained on 10-UAV swarms, all learned models transfer to 20 UAVs (RA-SCM {{m:rascm:gen_n20:pr_auc}}), an unseen trajectory ({{m:rascm:gen_lissajous:pr_auc}}) and an unseen formation ({{m:rascm:gen_grid:pr_auc}}), but **not to 5 UAVs** (RA-SCM {{m:rascm:gen_n5:pr_auc}}, GAT {{m:gat:gen_n5:pr_auc}}, GCN {{m:gcn:gen_n5:pr_auc}}), where few neighbours give little evidence — consistent with the identifiability analysis. *Secondary metrics* (Table 5) use validation-fixed thresholds, so realised FPRs differ between models; the AoI-aware physics test is poorly calibrated by that rule (FPR {{m:physics_aoi:iid_0:fpr}} at 0% loss, target 0.05).

{{tbl:secondary}}

*Table 5. Frozen-threshold secondary metrics (means over seeds; delay is over detected UAVs only).*

**Ablations and cost (E6, E7).** {{tbl:ablation}}

*Table 6. Paired PR-AUC difference full RA-SCM − ablated variant (mean [95% CI]); positive = the removed component helped.*

**Reading the ablations (exploratory, not pre-specified).** The reliability *channel* (delivery state, age, link quality, age-compensated residual) is what matters: removing it costs {{da:burst_50:rascm_no_rel}} PR-AUC under 50% bursts and {{da:nodeburst_30:rascm_no_rel}} under receiver-correlated loss, leaving RA-SCM close to the conventional GNNs ({{m:rascm_no_rel:burst_50:pr_auc}} vs GAT {{m:gat:burst_50:pr_auc}}). Learned reliability *weights* add little once the features are present (50% bursts: {{da:burst_50:rascm_no_weight}}; ≈0 elsewhere). **Learned sheaf restriction maps showed no measurable benefit:** replacing them by identity changes PR-AUC by at most {{n:sheaf_maxabs}} in the five conditions, with the interval including 0 in {{n:sheaf_ci0}}; for 5-UAV swarms the identity variant is even better ({{m:rascm_no_sheaf:gen_n5:pr_auc}} vs {{m:rascm:gen_n5:pr_auc}}). The GRU helps under bursts and strongly at ×3 noise ({{m:rascm_no_temporal:noise_3:pr_auc}} without vs {{m:rascm:noise_3:pr_auc}} with). The MPNN-E control is worse than RA-SCM under 50% bursts ({{da:burst_50:mpnn_e}}), although each single removal is not, so maps and weights may act jointly; this experiment cannot separate them. Hence the benefit under loss is best attributed to *how reliability metadata enters the model* (edge-conditioned, with temporal memory), not to sheaf structure as such.

{{tbl:cost}}

*Table 7. Parameters, amortised CPU inference time and training time. RA-SCM costs far more compute than GCN/GAT for a modest accuracy gain.*

**Threats to validity.** (i) Simulator and physics baseline were written by the authors (benchmark bias; the nominal sensor specifications given to the physics tests may not match reality). (ii) Realised FPRs differ across models, which affects delay and recall comparisons. (iii) Five seeds give wide intervals; differences of 0.01 are unresolvable. (iv) RA-SCM consumes edge features directly, the baselines in aggregated form; MPNN-E partly addresses this, but a GAT with edge features was not run. (v) Learning rates were tuned on one seed with a small grid.

**Expected scientific impact.** The outcome is a *controlled benchmark and a negative-leaning answer*: reliability-aware sheaf modelling is at best a small improvement over strong graph baselines here, and the cheapest effective step is to model the age of the evidence. Beneficiaries are researchers who evaluate swarm detectors (they need loss models and age-aware controls) and designers who must set thresholds under degraded links. *Possible harms:* the targeted-blackout scenario shows how an adversary could pair spoofing with link degradation, and a benchmark can encourage over-trust in simulated accuracy. *New questions:* threshold calibration under noise shift (FPR inflation at ×3 noise); detection with very few neighbours; whether the margins survive real, non-Gaussian sensor noise and measured loss traces; adaptive attackers; whether *computed* physical maps [@barbero2022connection] can replace learned ones.

## 10. References

::: {#refs}
:::
