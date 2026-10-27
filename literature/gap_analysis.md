# Critical synthesis, gap verification and originality ledger

*Established findings are separated from the project's interpretations. "Interpretation" paragraphs are our reading, not results of the cited papers.*

## 1. What the literature establishes

1. **Sheaf learning.** Replacing the graph Laplacian by a sheaf Laplacian with vector-space stalks and restriction maps gives message passing that can represent heterophilic relations and avoid the oversmoothing limit of ordinary diffusion (Hansen & Gebhart 2020; Bodnar et al. 2022). Evidence is node-classification benchmarks plus theory. Whether restriction maps must be *learned* is contested: computed orthogonal maps match or beat learned ones on most benchmark datasets in the authors' own report (Barbero et al. 2022, abstract).
2. **Sheaves for sensor consistency (non-learned).** Robinson (2017) and Joslyn et al. (2020) use sheaf-valued sensor data, a consistency radius and a consistency filtration to *flag* disagreement between heterogeneous sensors. Joslyn et al. state that the radius does not say which measurement is wrong.
3. **Sheaves for multi-agent control.** Hanks et al. (2025) solve consensus/formation/flocking with nonlinear sheaf Laplacians and ADMM under a fixed topology, without packet loss or fault detection.
4. **Sheaves + time.** Temporal sheaf networks exist for link prediction (Asif et al. 2026, preprint).
5. **GNN-based swarm spoofing detection.** Dang et al. (2023) use GCN+GRU on the GPS-vs-communication topology (simulation, accuracy-based). Model-based swarm detectors use reported positions plus pairwise ranging (Mykytyn et al. 2023, thresholds, no results in the version read; Bi et al. 2024, semidefinite feasibility, simulation).
6. **GNNs and missing data.** Graph imputation handles missing sensor values (Cini et al. 2022); uncertainty-weighted aggregation exists as a robustness device (Zhu et al. 2019); graph anomaly detectors for sensors assume complete synchronous observations (Deng & Hooi 2021).

## 2. Contradictions, methodological differences, transfer risks

* **Learned vs computed maps** (Bodnar vs Barbero): different evidence about whether learning the sheaf is necessary; both on node-classification benchmarks. *Interpretation:* for a swarm the maps are partly *known physics*, so the question moves from "learn or compute" to "which part of the map is known".
* **What counts as independent evidence differs across swarm papers:** UWB ranging (Mykytyn), pairwise range measurements (Bi), communication path loss (Dang). Dang et al. treat the communication topology as a trustworthy reference; Bi et al. assume reports and measurements arrive. *Interpretation:* none of the three treats communication unreliability as a confounder of the inconsistency signal.
* **Metrics are not comparable:** accuracy (Dang), detection success rate (Bi), none (Mykytyn), F1 under a threshold protocol (Deng & Hooi). None reports precision–recall area or false-positive behaviour under loss.
* **Benchmark transfer:** sheaf results concern heterophily/oversmoothing in node classification; they do not show an advantage for detecting local inconsistencies on a physically constrained swarm graph. This is an assumption we must test, not a transferable result.
* **Data limitations:** all UAV-swarm GNN/model-based evidence in the retrieved set is simulation-only; Joslyn et al.'s field study is the only real-data sheaf application and is a small case study.
* **Reproducibility:** none of the retrieved UAV-spoofing papers states released code in the sections read (not systematically checked); Mykytyn et al. report no experimental numbers at all in the version read.

## 3. Gap verification (questions from the project brief)

| Question | Finding (within the search coverage declared in `search_log.md`) |
|---|---|
| Has reliability-aware sheaf modelling been studied for this task? | No such study was found: four gap-check queries (sheaf+anomaly detection; sheaf+cooperative localisation; sheaf+false-data-injection; sheaf+reliability/packet loss) returned no matching paper. One 2026 preprint on sheaf Laplacian data fusion in sensing networks (arXiv:2606.19529) was seen only at abstract level and could contain related content. |
| Do comparable GNN methods already incorporate communication reliability? | Partly in other forms: variance/uncertainty-weighted aggregation (Zhu et al.), attention weights (GAT), imputation for missing values (GRIN). None uses explicit link metadata (age of information, delivery state, link quality) for position-anomaly detection. |
| Are there simpler approaches that address the same problem? | Yes — a statistical consistency test that inflates residual variance with the age of the last report (an *age-aware physics detector*). This is implemented here as the strongest simple competitor. Classical cooperative-localisation fault tolerance (covariance union / intersection, found as search snippets only) is another, **not** implemented. |
| Could the apparent gap come from incomplete coverage? | Yes. IEEE Xplore and ACM DL were not searched with their native interfaces; control/localisation journals were reached only through general web search. The gap is therefore stated as "not found", not "does not exist". |
| Does sheaf modelling give a plausible theoretical advantage? | Plausible, not demonstrated: (i) geometric consistency of reported vs measured relative position is naturally an edge-wise comparison in a shared edge space; (ii) node-specific restriction maps can absorb formation rotation/scale differences; (iii) a weighted sheaf Laplacian offers a principled place for precision weights. Against it: a physics test already implements (i) exactly, and generic edge-conditioned message passing can learn (i)–(iii) without sheaf structure. |
| When might it give no improvement? | If the age-aware physics detector is near-optimal (then learned models cannot add information); if restriction maps collapse to identity (then RA-SCM = edge-conditioned MPNN); if packet loss only affects data that the temporal model already carries; if anomalies are fully common-mode (unobservable). |

## 4. Gap statement (revised, evidence-supported)

> Within the literature we could access, no study evaluates learned graph or sheaf-based detectors of UAV position anomalies **under explicitly modelled communication unreliability (packet loss, burst loss, age of information), against an age-aware physical-consistency baseline, with paired statistics over seeds**. Existing swarm detectors either assume reliable delivery or use the communication topology as trusted evidence; existing sheaf work does not address anomaly detection or unreliable links. Whether a reliability-aware sheaf architecture yields a measurable benefit over (a) capacity-matched GCN/GAT/NSD baselines and (b) the age-aware physics test is therefore an open **empirical** question.

Because the question is empirical, the contribution is framed as a *controlled test of a hypothesis*, including the possibility that the answer is negative.

## 5. Originality ledger

| Component | Origin |
|---|---|
| Cellular sheaf, sheaf Laplacian, restriction maps | **Taken** from literature (Hansen & Ghrist 2019; Hansen & Gebhart 2020) |
| Learning restriction maps from endpoint node states, diffusion layer form | **Taken/adapted** from NSD (Bodnar et al. 2022); dense implementation, own code |
| GCN, GAT layers | **Taken** (Kipf & Welling; Veličković et al.), dense re-implementations cross-checked against PyG in unit tests |
| Weighting messages by uncertainty | **Taken** as an idea (Zhu et al. 2019; classical precision weighting) — *not claimed as new* |
| Gilbert–Elliott loss, age-of-information staleness, constant-velocity compensation | **Taken** (Gilbert 1960; Elliott 1963; standard kinematics) |
| Consistency of reported vs measured relative position as the inconsistency measure | **Taken** in spirit from swarm-spoofing work (Mykytyn et al.; Bi et al.) and sheaf sensor consistency (Robinson; Joslyn et al.) |
| Delayed-message semantics: every layer reads *cached sender embeddings from the time of the last delivered packet*, applied identically to all models | **Adapted** (engineering device so that no model can use un-communicated information) |
| Affine (data-dependent translation) restriction: ρ = F_i x_i − F_j x_j − b(e_ij), equivalent to a sheaf on stalks augmented with a constant coordinate | **Adapted** (a known trick, applied to sheaf diffusion for measurement-parameterised constraints) |
| Reliability weights as a learned inner product on edge stalks, driven by delivery flag, age and link quality, plus an evidence-mass feature | **Combined in a new manner** (components are known; their combination with sheaf diffusion for this task was not found) |
| Experimental protocol: loss/burst/targeted-blackout confound, frozen operating point, paired seeds, age-aware physics control, ablation separating edge-conditioning / sheaf maps / weights / reliability channel / temporal memory | **Proposed** as the genuinely new element of the study (a protocol contribution, not an algorithmic one) |

No component is presented as a new mathematical invention.
