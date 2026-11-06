---
title: "Supplementary Material: Literature Search, Matrix and Gap Analysis"
lang: en
---

<p class="author">Mehmet Ünlü (040230253) · EHB 420E Artificial Neural Networks · HW1 – From Curiosity to Scientific Discovery ·
supplement to the report "Reliability-Aware Sheaf Consistency for Distinguishing UAV Position Anomalies from Communication Failures"</p>

Contents: S1 search protocol and log · S2 comparative literature matrix · S3 critical synthesis, gap verification and originality ledger.


## S1. Literature search protocol and log


**Search periods:** round 1 on 27 October 2026; round 2 (pre-submission check) on 6 November 2026. **Searcher:** the project author with AI assistance (round 1: Claude Sonnet 5.5; round 2: Claude Opus 5.5; see the AI-assistance declaration in the report).

### What was actually searched (and what was not)

| Channel | How it was used | Limitation |
|---|---|---|
| General web search tool (US-only index) | 22 keyword queries, listed below | not a bibliographic database; ranking is opaque; no date/venue filters |
| arXiv API (`export.arxiv.org/api/query?id_list=...`) | metadata (authors, dates, comment/venue field) of every arXiv-hosted item | metadata only |
| Crossref REST API | DOI, venue, volume, pages for every item that has a DOI; in round 2 also keyword search restricted to IEEE (member 263) and ACM (member 320) records | some items have no DOI (ICLR, PMLR); IEEE records carry no abstracts |
| OpenAlex API (round 2) | 14 title/abstract and full-text keyword queries from 2018 on; abstracts of IEEE/ACM records | relevance ranking; indexing of 2026 proceedings may lag |
| Semantic Scholar API (round 2) | 5 boolean bulk queries from 2018 on | relevance endpoint rate-limited (HTTP 429) |
| Publisher / proceedings pages (NeurIPS proceedings, PMLR, AAAI OJS, Springer, MDPI/PMC) | confirm venue and bibliographic data | – |
| Full-text reading | Round 1 (AI-assisted): Dang et al. 2023, Bi et al. 2024, Mykytyn et al. 2023 (key sections); Joslyn et al. 2020 and Hanks et al. 2025 (partly). Round 2 (AI-assisted): Hansen & Gebhart 2020, Bodnar et al. 2022, Barbero et al. 2022, Hansen & Ghrist 2019, Hernández & Sánchez-Soto 2026, Kipf & Welling 2017, Veličković et al. 2018, Deng & Hooi 2021, Tolstaya et al. 2020, Kargar Tasooji & Parasuraman 2025, Vijay et al. 2025, Park & Yoo 2026, Tariq et al. 2026, Tariq & Shaukat 2026 | all other entries: **abstract-level reading only** (evidence level per entry in the matrix) |
| IEEE Xplore, ACM DL, Scopus, Web of Science native search | **not queried through their own search interfaces** (no access in this environment). In round 2 IEEE/ACM records were searched through Crossref (member filter), OpenAlex and Semantic Scholar | remaining threat to the gap claim: native-interface searches (e.g. through the ITU library) could still find items these indexes rank low |

### Keywords (combined with AND/OR as shown in the query list)

* Sheaf learning: *sheaf neural network*, *neural sheaf diffusion*, *cellular sheaf*, *sheaf Laplacian*, *restriction map*, *connection Laplacian*, *nonlinear sheaf diffusion*, *temporal / dynamic sheaf*
* Graph anomaly detection: *graph neural network anomaly detection multivariate time series*, *sensor fault detection GNN*, *missing data / unreliable edges*
* UAV reliability: *GPS spoofing detection UAV swarm*, *cooperative localization spoofing / fault*, *position spoofing swarm formation*, *packet loss multi-robot GNN*
* Communication models: *Gilbert–Elliott burst loss*
* Robust/uncertainty-aware GNNs: *robust GCN variance attention*, *edge reliability weighting*

### Query log (all executed 2026-10-27)

1. Neural Sheaf Diffusion: A Topological Perspective on Heterophily and Oversmoothing in GNNs
2. Sheaf Neural Networks Hansen Gebhart arXiv 2012.06333
3. Sheaf Neural Networks with Connection Laplacians Barbero
4. sheaf neural network anomaly detection multi-agent sensor fusion consistency
5. Nonlinear Sheaf Diffusion in Graph Neural Networks OR "Sheaf diffusion goes nonlinear" adaptive sheaf Laplacians
6. Graph neural network GPS spoofing detection UAV swarm cooperative localization
7. Graph Neural Network-Based Anomaly Detection in Multivariate Time Series Deng Hooi AAAI 2021
8. graph neural networks multi-robot communication packet loss robustness decentralized controllers
9. sheaf neural network dynamic graph temporal sheaf spatiotemporal time-varying restriction maps
10. sheaf-theoretic multi-agent distributed coordination consensus sheaf Laplacian robots Hanks
11. GNN sensor fault detection missing data unreliable edges edge reliability weighting graph anomaly detection robust to missing observations
12. UAV swarm GPS spoofing detection relative distance consistency swarm formation deep learning
13. Gilbert-Elliott burst packet loss model Elliott 1963 estimates of error rates for codes on burst-noise channels
14. Semi-Supervised Classification with Graph Convolutional Networks Kipf Welling / Graph Attention Networks
15. Toward a spectral theory of cellular sheaves Hansen Ghrist
16. Sheaf Hypergraph Networks OR Sheaf Attention Networks OR Cooperative Sheaf Neural Networks OR sheaf neural networks missing data time series
17. "sheaf" "anomaly detection" graph neural network sensor network OR swarm OR UAV  *(gap check)*
18. sheaf Laplacian cooperative localization multi-robot relative measurements restriction maps spoofing OR fault  *(gap check)*
19. Filling the G_ap_s: Multivariate Time Series Imputation by Graph Neural Networks
20. Robust Graph Convolutional Networks Against Adversarial Attacks Zhu KDD 2019
21. "cellular sheaf" OR "sheaf cohomology" false data injection attack detection networked systems consensus  *(gap check)*
22. sheaf Laplacian weighted by uncertainty OR reliability OR covariance "packet loss" OR "communication failure" OR "missing edges"  *(gap check)*

### Inclusion criteria
1. Directly about at least one of: sheaf-based learning/diffusion/sensor integration; GNN-based anomaly or spoofing detection; UAV/multi-robot swarm position consistency, spoofing or cooperative localisation; GNN behaviour under missing/unreliable data or communication; burst-loss channel models used in the simulator.
2. Bibliographic data verifiable in an independent record (arXiv API, Crossref, publisher page).
3. Peer-reviewed, **or** a clearly labelled preprint/workshop paper that is the only/primary source for a specific idea. Status is recorded in the matrix and the bibliography.
4. English language, 1960–2026 (foundational channel models and GCN/GAT are older; sheaf learning is 2019+).

### Exclusion criteria
* Patents, blog/skill/playbook pages, and aggregator summaries as sources of claims (they appeared in the search results and were used only to find primary sources).
* Items for which bibliographic data could not be confirmed.
* UAV-swarm work on intrusion detection by federated learning, single-UAV spoofing detectors using radio fingerprints/cellular signals, and GNSS signal-authentication schemes — relevant context but not about swarm-level geometric consistency under unreliable communication.
* Results that appeared only as aggregator summaries with numbers not found on the primary page (e.g. benchmark F1 values on third-party leaderboards).
* Items from low-visibility or unrefereed venues when a peer-reviewed source covers the same idea (round 2).

### Items found but not included in the matrix (context only)
* *Sheaf Graph Neural Networks via PAC-Bayes Spectral Optimization* (arXiv:2508.00357; arXiv comment: AAAI 2026, acceptance not verified): node-level certified confidence intervals, **not** edge reliability; only the abstract page was read.
* *From Classical to Topological Neural Networks Under Uncertainty* (arXiv:2602.10266): book chapter; no sheaf/anomaly/communication content in the abstract.
* *Sheaf-Theoretic Planning* (arXiv:2605.01879): categorical planning report, no learning/anomaly detection in the abstract.
* Resilient collaborative localisation under spoofed radio measurements, fault-tolerant cooperative localisation by covariance union, and the Chinese J. Aeronautics 2022 paper on GNSS faults in swarms were seen as snippets in round 1. **Resolved in round 2:** the last is Chen et al. 2022 (now in the matrix and the report); the first is Karstensen & Galeazzi, arXiv:2511.21432 (ideal links, one scenario; screened, not cited); the covariance-union line is Uhlmann 2003 (Information Fusion 4(3), metadata only) and Wang et al. 2021 (IEEE RA-L 6(4), abstract only), screened but not cited.

### Round 2 query log (6 November 2026)

All run 2026-11-06. OpenAlex 'ta' = filter title_and_abstract.search; 'fulltext' = search parameter. Crossref = query.bibliographic, relevance-ranked, so its totals count any-term matches. Semantic Scholar = /paper/search/bulk (boolean; the relevance endpoint returned HTTP 429). Hits = total reported by the index; screened = titles read, with abstracts read for every title that looked relevant.

* Q1 OpenAlex fulltext: 'UAV swarm GPS spoofing detection graph neural network packet loss' | from_publication_date:2018-01-01 | hits 237 | titles screened 50 (top 50 by relevance), abstracts read 5
* Q2 OpenAlex ta: (UAV OR drone OR multi-UAV) AND swarm AND (spoofing OR "position anomaly" OR "false data injection") AND ("graph neural network" OR GNN OR "graph attention" OR "graph convolutional") | from 2018-01-01 | hits 9 | screened 9, abstracts 6
* Q3 OpenAlex ta: ("cooperative localization" OR "collaborative localization" OR "cooperative positioning") AND (spoofing OR fault OR anomaly OR "false data injection" OR outlier) AND ("packet loss" OR "communication failure" OR "communication delay" OR "intermittent communication" OR "age of information" OR "unreliable communication" OR "communication loss") | from 2018-01-01 | hits 7 | screened 7, abstracts 3
* Q4 OpenAlex ta: (UAV OR drone OR multi-UAV OR "multi-robot" OR swarm) AND (spoofing OR "position anomaly" OR "fault detection" OR "anomaly detection" OR "false data injection") AND ("packet loss" OR "packet dropout" OR "communication failure" OR "intermittent communication" OR "age of information" OR "unreliable communication" OR "communication delay") AND ("graph neural network" OR GNN OR "deep learning" OR "neural network" OR learning) | from 2018-01-01 | hits 9 | screened 9, abstracts 5
* Q5 OpenAlex ta: (UAV OR drone OR multi-UAV OR "multi-robot" OR swarm OR "multi-agent") AND (GPS OR GNSS) AND (spoofing OR anomaly OR fault) AND ("inter-UAV" OR "relative distance" OR "relative position" OR ranging OR UWB OR "relative measurement" OR "range measurement") | from 2018-01-01 | hits 232 | titles screened 50 (top 50), abstracts 14
* Q6 OpenAlex ta: sheaf AND (UAV OR drone OR swarm OR "multi-robot" OR "multi-agent" OR localization OR "sensor network") AND (anomaly OR fault OR spoofing OR consistency OR attack OR outlier) | from 2018-01-01 | hits 43 | screened 43, abstracts 4
* Q7 OpenAlex ta: ("graph neural network" OR GNN OR "graph attention" OR "message passing") AND ("multi-robot" OR "multi-UAV" OR swarm OR "multi-agent") AND ("packet loss" OR "packet drop" OR "communication delay" OR "communication failure" OR "age of information" OR "intermittent communication" OR "lossy communication") | from 2018-01-01 | hits 46 | screened 46, abstracts 2 (most hits are AoI/routing MARL, not detection)
* Q8 OpenAlex ta: ("age of information" OR "stale information" OR "outdated information" OR "delayed measurements") AND (spoofing OR "anomaly detection" OR "fault detection" OR "misbehavior detection" OR "false data") AND (UAV OR drone OR swarm OR "multi-robot" OR vehicle OR platoon OR V2X) | from 2018-01-01 | hits 4 | screened 4, abstracts 2
* Q9 OpenAlex ta: ("graph neural network" OR GNN OR "graph attention" OR "graph convolutional") AND ("misbehavior detection" OR "position falsification" OR "position spoofing" OR "GPS spoofing" OR "GNSS spoofing" OR "location spoofing") | from 2018-01-01 | hits 21 | screened 21, abstracts 5
* Q10 OpenAlex ta: (swarm OR multi-UAV OR "UAV formation" OR "drone fleet" OR "multi-robot") AND (spoofing OR "false data injection" OR "position anomaly" OR "position falsification") AND ("packet loss" OR "packet dropout" OR "communication loss" OR "link failure" OR "link loss" OR "message loss" OR "communication failure" OR "missing measurements") | from 2018-01-01 | hits 14 | screened 14, abstracts 4
* Q11 OpenAlex ta: ("graph neural network" OR GNN OR "graph attention" OR "message passing neural" OR "graph convolutional" OR "sheaf neural") AND ("cooperative localization" OR "collaborative localization" OR "cooperative positioning" OR "relative localization" OR "network localization") AND (fault OR outlier OR anomaly OR spoofing OR attack OR malicious OR Byzantine) | from 2018-01-01 | hits 2 | screened 2, abstracts 2
* Q12 OpenAlex ta: (swarm OR multi-UAV OR "multi-robot" OR "UAV formation" OR "UAV network") AND spoofing AND (jamming OR "packet loss" OR "communication failure" OR "link failure") AND (distinguish OR discriminate OR differentiate OR "root cause" OR classify OR classification OR diagnosis OR isolate) | from 2018-01-01 | hits 23 | screened 23, abstracts 2
* Q13 OpenAlex ta: ("spatio-temporal graph" OR "graph neural network" OR GNN OR "graph attention" OR "graph convolutional") AND (UAV OR drone OR swarm OR "multi-robot" OR "multi-agent") AND ("anomaly detection" OR "fault detection" OR "fault diagnosis" OR "attack detection") AND ("packet loss" OR delay OR latency OR missing OR "communication constraints" OR "communication failure" OR "link quality") | from 2018-01-01 | hits 39 | screened 39 (mostly single-UAV sensor fault diagnosis or IoT), abstracts 0 beyond titles already seen
* Q14 OpenAlex fulltext: 'GNSS spoofing detection UAV swarm age of information packet loss relative distance consistency' | from 2018-01-01 | hits 41 | screened 41, abstracts 1
* C1 Crossref, member 263 (IEEE): 'UAV swarm GPS spoofing detection graph neural network packet loss' | from-pub-date:2018 | hits 88,323 (any-term relevance) | screened top 50; abstracts for 6 candidates fetched from OpenAlex by DOI (Crossref IEEE records carry no abstracts)
* C2 Crossref, member 263 (IEEE): 'multi-robot cooperative localization fault detection learning packet loss communication failure' | from-pub-date:2018 | hits 151,621 | screened top 50; abstracts for 8 fetched from OpenAlex
* C3 Crossref, member 263 (IEEE): 'drone swarm position anomaly detection graph neural network intermittent communication delay' | from-pub-date:2018 | hits 125,402 | screened top 50 (dominated by generic network-traffic GNN anomaly detection); 1 abstract fetched
* C4 Crossref, member 320 (ACM): 'UAV drone swarm GPS spoofing position anomaly detection graph neural network' | from-pub-date:2018 | hits 8,401 | screened top 50; abstracts for 4 fetched from OpenAlex
* C5 Crossref, member 320 (ACM): 'multi-robot swarm fault detection learning unreliable communication packet loss localization' | from-pub-date:2018 | hits 8,369 | screened top 50; no relevant hit
* S1 Semantic Scholar bulk: (UAV | drone | swarm | "multi-robot" | "multi-agent") + (spoofing | "false data injection" | "position anomaly" | "fault detection") + ("graph neural network" | GNN | "graph attention" | "graph convolutional" | sheaf) + ("packet loss" | "communication failure" | "communication delay" | "age of information" | "intermittent communication" | "unreliable communication" | "communication constraints" | "missing data") | year 2018- | hits 1 | screened 1 (ZT-GAT)
* S2 Semantic Scholar bulk: (UAV | drone | swarm | "multi-robot" | "multi-UAV" | "cooperative localization") + (spoofing | "position anomaly" | "fault detection" | "false data injection" | "anomaly detection") + ("packet loss" | "communication failure" | "age of information" | "intermittent communication" | "unreliable communication" | "communication loss" | "packet dropout") | year 2018- | hits 20 | screened 20, abstracts 1
* S3 Semantic Scholar bulk: (UAV | drone | swarm | "multi-robot" | "multi-UAV") + (GPS | GNSS) + spoofing + ("graph neural network" | GNN | "graph attention" | "graph convolutional" | "deep learning" | learning) | year 2018- | hits 157 | titles screened 120 of 157, abstracts 6
* S4 Semantic Scholar bulk: ("cooperative localization" | "collaborative localization" | "relative localization" | "cooperative navigation" | "integrity monitoring") + (swarm | "multi-robot" | "multi-UAV" | "multi-agent") + (spoofing | fault | outlier | anomaly | "false data injection") + ("packet loss" | "communication failure" | "communication delay" | "age of information" | intermittent | "unreliable communication" | "limited connectivity" | asynchronous) | year 2018- | hits 5 | screened 5, abstracts 2
* S5 Semantic Scholar bulk: sheaf + (UAV | drone | swarm | robot | "multi-robot" | localization | "sensor network" | "multi-agent") + (anomaly | fault | spoofing | consistency | outlier | attack | "packet loss") | year 2018- | hits 11 | screened 11 (no new item beyond Q6)
* Verification: Crossref `/works/<DOI>` for all DOI-bearing candidates (and, in the final check, all 31 DOI-bearing references of the report); arXiv API `id_list` query for 2608.06885, 2507.06750 and 2605.13500; DataCite /dois/10.5281/zenodo.20768967. Full-text sections were read for arXiv:2605.13500 (SpliTech 2026) and arXiv:2507.06750 (IROS 2025). The Springer full text of ZT-GAT was not retrievable.

Additional round-2 queries on classical cooperative localisation (OpenAlex, Crossref and arXiv API; resilient collaborative localisation under spoofing, detectability of GNSS faults in swarms, fault detection and exclusion in multi-robot localisation, cooperative localisation with packet loss or delay, AoI combined with fault/anomaly detection) and reference chasing in arXiv:2507.06750 and arXiv:2511.21432.

### Round 2: screening decisions

**Added to the report and the matrix:** Chen et al. 2022; He et al. 2024; Kargar Tasooji & Parasuraman 2025; Cao et al. 2026; Ou et al. 2023; Vijay et al. 2025; Michieletto et al. 2023; Park & Yoo 2026 (preprint); Sophia et al. 2026; Pan et al. 2026; Tariq et al. 2026 (Sci. Rep.); Tariq & Shaukat 2026 (Front. Commun. Netw.); Moustafa & Abdelghany 2026; and the foundational sources Kaul et al. 2012, Sinopoli et al. 2004, Julier & Uhlmann 1997, Willsky 1976, Brown 1992, Kerns et al. 2014, Tippenhauer et al. 2011, Hayat et al. 2016.

**Screened, not cited** (reason in brackets): Mitra et al. 2019, Autonomous Robots (resilient estimation of an external process); Chang et al. 2022, IEEE T-RO (CI-based localisation under missing links/observations, no erroneous data); Wang et al. 2021, IEEE RA-L (covariance-union fault tolerance, no loss model); Kargar Tasooji & Marquez 2022, IEEE Access (DoS + false-data-injection resilient estimation); Qu et al. 2017, IEEE Access (UAV fault-tolerant cooperative positioning, no loss model); Causa & Fasano 2023, PLANS and Gipson & Leishman 2022, IEEE TAES (fault detection and exclusion, no loss model); Olawoye & Gross 2026, Applied Sciences (distributed fault isolation for ranging-based localisation); Liu et al. 2026, IEEE TIM (parity-vector GNSS fault detection with relative ranging); Mughal et al. 2026, IEEE IoT-J (network intrusion detection); You et al. 2026, Drones (delay/loss diagnosis on the communication side only); Alamleh & Pulatov 2026, SpliTech (non-learned link-quality and staleness weighting of range constraints); Voitovych & Bychkov 2026 (conference proceedings, hand-designed guard statistics); Almekhyal et al. 2026 (single-UAV learned detectors with injected packet loss); Abima et al. 2026, ACM (relay-risk score, paired Monte Carlo); Fan et al. 2023, MILCOM and Gu et al. 2025, ICPADS (swarm spoofing detection/defence without loss model); Poornima 2026 and Cui 2026 (low-visibility venues); preprints and software (Coulibaly et al. 2026, TRUST-V; Tariq et al. PINN-CMA software; Karstensen & Galeazzi 2025); Moreau 2026 and Pasupuleti 2025 (weak venues, not detection of position anomalies). Only abstracts were read for most of these.

**Effect on the gap:** the gap was narrowed (report Section 4). Joint handling of link failures and faulty measurements exists in model-based cooperative localisation, and learned graph swarm detectors have been run under simulated loss; what remains unaddressed in the sources read is loss/AoI as a *controlled, stratified* confounder of position-consistency detection, compared against a standalone age-aware physics baseline.

**Note:** one OpenAlex response contained text addressed to automated agents (a request to register an API key with the user's e-mail); it was ignored.



<div class="pagebreak"></div>

## S2. Comparative literature matrix


Status: P = peer-reviewed, W = workshop paper, X = arXiv preprint. Evidence: FT = key sections of the full text read (section, table or equation numbers are given where a detail comes from the full text), AB = abstract/metadata page only. Full-text details were checked in an AI-assisted pre-submission check on 6 November 2026 (see the AI-assistance declaration in the report).

### Hansen & Gebhart 2020, Sheaf Neural Networks, arXiv:2012.06333

`hansen2020sheaf` · status **W** · evidence **FT**

* **Research question:** Can the diffusion step of a GCN be generalised from the graph Laplacian to a sheaf Laplacian?
* **Method:** Replace graph diffusion by sheaf-Laplacian diffusion with vector-space stalks and restriction maps.
* **Data / conditions:** Synthetic semi-supervised node classification on signed graphs.
* **Metrics:** Node-classification accuracy.
* **Main findings:** Sheaf networks outperform Kipf–Welling GCN in the synthetic signed-graph setting (abstract).
* **Assumptions:** The sheaf is hand-built from signed edge weights because standard datasets lack obvious sheaf structure (Sec. 4); learning the sheaf from data is listed only as future work (Sec. 5). The paper makes no claim about heterophily or oversmoothing.
* **Weaknesses / reproducibility:** Synthetic data only; workshop paper; no real benchmark; no dynamic graphs.
* **Relation to RA-SCM:** Origin of sheaf-based message passing. We reuse the sheaf-Laplacian operator, not any result.

### Bodnar et al. 2022, Neural Sheaf Diffusion, NeurIPS (arXiv:2202.04579)

`bodnar2022neural` · status **P** · evidence **FT**

* **Research question:** How does the (implicit trivial) sheaf of a GNN explain heterophily and oversmoothing, and can learning the sheaf fix both?
* **Method:** Learn restriction maps from node features of the two endpoints of an edge; discretised sheaf diffusion layers; theory on linear separability and asymptotic behaviour.
* **Data / conditions:** Nine node-classification benchmarks ordered by edge homophily h = 0.11–0.81: Texas, Wisconsin, Film, Squirrel, Chameleon, Cornell (heterophilic, h ≤ 0.30) and Citeseer, Pubmed, Cora (homophilic); 10 fixed 48/32/20 % splits of Pei et al. (Sec. 6, Table 1); plus a synthetic linear-separation experiment (Fig. 5).
* **Metrics:** Mean test accuracy ± standard deviation over the 10 fixed splits (Sec. 6, Table 1); baseline figures are copied from Yan et al., Lingam et al. and Zhu et al. on the same splits, not re-run.
* **Main findings:** Competitive (NeurIPS/arXiv abstract) or state-of-the-art (ICLR 2022 GTRL workshop abstract) results on heterophilic graphs; full text: first on 5 of 6 heterophilic benchmarks, second on Chameleon, top three on 8/9 datasets (Sec. 6, Table 1); non-trivial sheaves give control over diffusion limits.
* **Assumptions:** Static graph; maps conditioned on node features only; no edge features, measurement noise or missing edges; homophily/heterophily as the task structure.
* **Weaknesses / reproducibility:** Fixed benchmark splits; cost grows with stalk dimension; claims concern node classification, not detection of local inconsistencies; wording of the headline claim differs between venues (see search record).
* **Relation to RA-SCM:** Baseline 4 (NSD-style sheaf) is an NSD-style implementation of this idea in our dense framework. RA-SCM adds edge-conditioned maps, translation term, reliability weights and temporal state.

### Barbero et al. 2022, Sheaf NNs with Connection Laplacians (PMLR 196)

`barbero2022connection` · status **W** · evidence **FT** (Table 1, Sec. 5)

* **Research question:** Is it necessary to learn the sheaf, or can restriction maps be computed from geometry?
* **Method:** Orthogonal restriction maps aligning neighbouring local tangent spaces (manifold assumption), not learned.
* **Data / conditions:** Node-classification benchmarks (abstract-level only).
* **Metrics:** Accuracy.
* **Main findings:** By the authors' conclusion (Sec. 5), matches or beats the learned-sheaf models of Bodnar et al. on most datasets; Table 1 shows Conn-NSD best only on Texas and Film and clearly below learned NSD on Squirrel (45.19 vs 56.34), Chameleon (65.21 vs 68.68) and Cora (83.74 vs 87.30). The abstract claims only 'promising results with less computational overhead'.
* **Assumptions:** Data lie on a low-dimensional manifold; features are sufficient to estimate tangent spaces.
* **Weaknesses / reproducibility:** Workshop paper; assumption is unverified for sensor data; static graphs.
* **Relation to RA-SCM:** Partly contradicts the need for learned maps (vs NSD) and motivates physically-derived maps; our physics baseline is the extreme 'fixed map' case.

### Zaghen et al. 2024, Nonlinear Sheaf Diffusion (PMLR 251)

`zaghen2024nonlinear` · status **W** · evidence **AB**

* **Research question:** Can a learned nonlinearity inside the sheaf Laplacian capture antagonistic or bounded-confidence interactions?
* **Method:** Nonlinear sheaf Laplacian with an adaptive learned function.
* **Data / conditions:** Synthetic community-detection dataset.
* **Metrics:** Node-classification accuracy.
* **Main findings:** Beats linear sheaf networks and common GNN baselines on the synthetic task (abstract).
* **Assumptions:** Synthetic opinion-dynamics-like interactions.
* **Weaknesses / reproducibility:** Synthetic only, workshop paper.
* **Relation to RA-SCM:** A robust (bounded) nonlinear aggregator could resist large anomalous residuals; not implemented here.

### Hansen & Ghrist 2019, Toward a spectral theory of cellular sheaves, J. Appl. Comput. Topol. 3(4)

`hansen2019spectral` · status **P** · evidence **FT**

* **Research question:** What are the spectral properties of the sheaf Laplacian and how do they relate to cohomology and graph structure?
* **Method:** Hodge-type Laplacian of cellular sheaves; interlacing, sparsification, effective resistance, synchronisation (abstract).
* **Data / conditions:** Theory.
* **Metrics:** n/a
* **Main findings:** Foundations of sheaf Laplacian spectra; links kernel to global sections.
* **Assumptions:** Finite regular cell complexes with finite-dimensional stalks (Sec. 3.3); a weighted sheaf puts inner products on stalks, which fix the adjoint δ* and so the Laplacian Δ = δ*δ + δδ* (Secs 3.1–3.2); scaling an edge stalk's inner product changes the weight given to discrepancies over that edge (Sec. 3.5).
* **Weaknesses / reproducibility:** No learning or noisy data.
* **Relation to RA-SCM:** Justifies treating reliability weights as a choice of inner product on edge stalks (L_w = δᵀWδ) rather than a new operator.

### Robinson 2017, Sheaves are the canonical data structure for sensor integration, Information Fusion 36

`robinson2017sheaves` · status **P** · evidence **AB**

* **Research question:** What mathematical structure can represent heterogeneous information sources faithfully and expose inconsistency?
* **Method:** Sheaves of sensor data; consistency radius, constrained fusion, cohomology for 'blind spots'.
* **Data / conditions:** Expository, illustrative examples.
* **Metrics:** n/a
* **Main findings:** Sheaves give a sensor-agnostic consistency measure, fusion method and blind-spot detection (abstract).
* **Assumptions:** Sensor relationships must be specified by the modeller; exact data model.
* **Weaknesses / reproducibility:** Expository; no learning, no quantitative evaluation of detection.
* **Relation to RA-SCM:** Conceptual foundation of the inconsistency measure r_ij and of the identifiability discussion.

### Joslyn et al. 2020, A sheaf theoretical approach to uncertainty quantification of heterogeneous geolocation information, Sensors 20(12)

`joslyn2020sheaf` · status **P** · evidence **FT(partial)**

* **Research question:** How can the agreement among heterogeneous geolocation sensors be quantified?
* **Method:** Sheaf over a simplicial complex of sensors; ε-consistency radius and consistency filtration; comparison with a Kalman-filter dynamic linear model.
* **Data / conditions:** Field experiment: 12 GPS collars (6 stationary decoy collars and 6 active collars on three wild black bears; twelve locating sessions), four sensor types (collar GPS, VHF, text report, vehicle GPS), 16 observations per 2-h session (Secs 3.2, 5).
* **Metrics:** Consistency radius (m) and filtration.
* **Main findings:** Radius decreases as the VHF error shrinks when the team approaches; largest discrepancy VHF vs collar GPS at the analysed instant (464.5 m).
* **Assumptions:** Sensor relationships and coordinate conversions specified in advance; time slices analysed independently.
* **Weaknesses / reproducibility:** The radius alone does not say which measurement is wrong; the consistency filtration attributes disagreement to sensors (Sec. 4, 5.1), but the authors state that neither reports which measurements are trustworthy (Conclusion); small case study; no learning, no dynamics, no communication or missing-data model.
* **Relation to RA-SCM:** Closest prior use of sheaf consistency for geolocation fusion; shows that consistency can flag and attribute disagreement, but not separate missing from wrong data — the ambiguity we study.

### Hanks et al. 2025, Distributed multi-agent coordination over cellular sheaves, arXiv:2504.02049

`hanks2025distributed` · status **X** · evidence **FT(partial)**

* **Research question:** Can heterogeneous multi-agent coordination (consensus, formation, flocking) be cast over cellular sheaves?
* **Method:** Nonlinear homological programs on sheaves; ADMM with a local nonlinear sheaf heat equation.
* **Data / conditions:** Simulations with three planar double-integrator vehicles; a UAV/USV/UUV case study described but not simulated.
* **Metrics:** Convergence of simulated goals.
* **Main findings:** Consensus, formation and flocking solved in the examples.
* **Assumptions:** Fixed undirected topology; no packet loss, delay or failures modelled; convex potentials.
* **Weaknesses / reproducibility:** Tiny simulations; preprint; learning/GNN integration listed only as future work.
* **Relation to RA-SCM:** Shows sheaves for multi-agent *control* under reliable fixed topology — contrasts with our time-varying unreliable network.

### Ribeiro et al. 2026, Cooperative Sheaf Neural Networks, ICLR 2026 (arXiv:2507.00647)

`ribeiro2025cooperative` · status **P** (ICLR 2026 poster, OpenReview AHpexliCTM) · evidence **AB**

* **Research question:** How to extend sheaf networks to directed graphs?
* **Method:** Cooperative sheaf Laplacian with a pair of learned maps per node [abstract-level].
* **Data / conditions:** not extracted
* **Metrics:** not extracted
* **Main findings:** not extracted
* **Assumptions:** Directed message flow.
* **Weaknesses / reproducibility:** Not read beyond abstract.
* **Relation to RA-SCM:** Directed links resemble asymmetric packet delivery; not used.

### Asif et al. 2026, Temporal Sheaf NNs with Dynamic Orthogonal Transport, arXiv:2606.10071

`asif2026temporal` · status **X** · evidence **AB**

* **Research question:** Can time-varying node frames improve temporal link prediction?
* **Method:** Per-node time-varying orthogonal frames (Householder products), transport before comparison, geometric-residual decoder, causal computation.
* **Data / conditions:** TGB v2 and DGB temporal-graph benchmarks.
* **Metrics:** Link-prediction metrics (abstract: 'matches or beats strong prior methods on most tasks').
* **Main findings:** Gains attributed to dynamic frames, orthogonal transport and geometric-residual decoder (ablations).
* **Assumptions:** Event streams, no measurement noise or missing observation semantics.
* **Weaknesses / reproducibility:** Preprint; peer review not indicated; task is link prediction.
* **Relation to RA-SCM:** Closest sheaf + dynamic-graph work; confirms that dynamic sheaves are of current interest but for a different task. Not anomaly detection, not reliability-aware.

### Hernández & Sánchez-Soto 2026, The Sheaf Laplacian: data fusion and consensus in distributed sensing networks, arXiv:2606.19529

`hernandez2026sheaf` · status **X** · evidence **FT**

* **Research question:** Is the sheaf Laplacian a suitable mechanism for data fusion and consensus in distributed sensing?
* **Method:** Sheaf-theoretic framework; Sec. 7 proposes the sheaf Dirichlet energy and a spectral variant as anomaly scores and localises a faulty node from per-edge energy contributions (Sec. 7.3).
* **Data / conditions:** None (conceptual paper, 10 pp.); drone swarms named as an application (Sec. 1).
* **Metrics:** None.
* **Main findings:** Proposes Dirichlet-energy anomaly detection and faulty-node localisation; no evaluation.
* **Assumptions:** Fixed maps; packet loss, intermittent links and topology changes named as challenges (Sec. 2.1) but not modelled inside the detector.
* **Weaknesses / reproducibility:** No experiments, no loss model, no learning.
* **Relation to RA-SCM:** An unweighted, loss-free ancestor of our AoI-aware physics baseline; it contradicts any claim that sheaf work ignores anomaly detection.

### Kipf & Welling 2017, GCN, ICLR

`kipf2017semi` · status **P** · evidence **FT**

* **Research question:** Scalable semi-supervised learning on graphs.
* **Method:** Localised first-order approximation of spectral graph convolutions with the renormalisation trick Â = D̃^-1/2 Ã D̃^-1/2, Ã = A + I, D̃ = degree matrix of Ã (Sec. 2, Eqs 2 and 8).
* **Data / conditions:** Citation networks Citeseer, Cora, Pubmed and the NELL knowledge-graph dataset; splits of Yang et al. (2016) (citation networks: 20 labels per class), 500 validation and 1,000 test nodes (Secs 5.1–5.2, Table 1).
* **Metrics:** Classification accuracy (%), mean of 100 runs with random weight initialisations; wall-clock training time (Sec. 6.1, Table 2).
* **Main findings:** Outperforms related methods by a significant margin (abstract): 70.3 / 81.5 / 79.0 / 66.0 % on Citeseer / Cora / Pubmed / NELL vs best baselines 69.1 / 75.7 / 77.2 / 61.9 % (Table 2).
* **Assumptions:** Undirected graph without native edge features; implicit locality and equal weight of self-loop and neighbours (Sec. 7.2); single static graph, transductive node classification (Sec. 4.2). The label-homophily assumption is stated for Laplacian regularisation (Sec. 1), which GCN replaces.
* **Weaknesses / reproducibility:** Degrades with depth: best at 2–3 layers, hard to train beyond 7 layers without residual connections (App. B); full-batch memory grows linearly with graph size (Sec. 7.2); single static graph; below an MLP on heterophilic graphs in NSD's Table 1 (e.g. Texas 55.1 vs 80.8 %).
* **Relation to RA-SCM:** Baseline 2 (GCN).

### Veličković et al. 2018, GAT, ICLR

`velickovic2018graph` · status **P** · evidence **FT**

* **Research question:** Learn neighbour weights by attention.
* **Method:** Masked self-attention over first-order neighbourhoods (LeakyReLU scores, softmax-normalised), K heads concatenated or averaged in the output layer (Sec. 2.1).
* **Data / conditions:** Transductive: Cora, Citeseer, Pubmed citation networks (20 labels per class, 500 validation / 1,000 test nodes); inductive: PPI, 20 / 2 / 2 train / val / test graphs with test graphs unseen, 121 multi-labels (Sec. 3.1).
* **Metrics:** Transductive: mean accuracy ± s.d. over 100 runs; inductive: micro-averaged F1 on the two unseen test graphs, mean of 10 runs (Sec. 3.4, Tables 2–3).
* **Main findings:** Achieves or matches state of the art on all four benchmarks (Tables 2–3): +1.5 / +1.6 points over the best GCN on Cora / Citeseer (83.0 / 72.5 %), equal to GCN on Pubmed (79.0 %); PPI micro-F1 0.973 vs 0.768 (best GraphSAGE) and 0.934 (constant-attention GAT).
* **Assumptions:** Attention scores computed from node features only, a^T[Wh_i ‖ Wh_j] (Sec. 2.1).
* **Weaknesses / reproducibility:** Attention is not a calibrated reliability weight; no edge features (left to future work, Sec. 4).
* **Relation to RA-SCM:** Baseline 3 (GAT).

### Deng & Hooi 2021, Graph neural network-based anomaly detection in multivariate time series, AAAI 35(5)

`deng2021graph` · status **P** · evidence **FT**

* **Research question:** Detect anomalies in multivariate sensor time series when inter-sensor relationships are unknown.
* **Method:** Learn a sensor graph from embedding similarity; graph-attention forecasting; deviation score; attention-based explanation.
* **Data / conditions:** SWaT (51 sensors) and WADI (127 sensors) water-treatment testbeds: two weeks of normal operation for training, test sets with staged attacks (11.97 % / 5.99 % anomalous); 10-s median downsampling, first 2160 samples dropped (Sec. 4.1, Table 1).
* **Metrics:** Precision, recall and F1 over test time ticks, chosen for class imbalance (Sec. 4.3, Table 2).
* **Main findings:** Detects anomalies more accurately than baselines and helps root-cause identification (abstract): F1 0.81 on SWaT and 0.57 on WADI with precision ≈ 0.98–0.99 but recall 0.40–0.68 (Table 2; part of the baseline numbers taken from Li et al. 2019).
* **Assumptions:** Same fixed N sensors in training and test, training data assumed normal, one complete N-dimensional reading per time tick (Sec. 3.1); no missing-data or communication model; single fixed threshold = max of the SMA-smoothed score on validation data (Secs 3.6, 4.3), so reported F1 is tied to this rule (alternatives such as EVT mentioned, not evaluated).
* **Weaknesses / reproducibility:** F1 depends on threshold rule; no missing-data semantics; static learned graph.
* **Relation to RA-SCM:** Representative of graph-based sensor anomaly detection; we add missingness/staleness as a first-class confound and a dynamic physical graph.

### Dang, Karakoc & Jäntti 2023, GNN-based GPS spoofing detection for cellular-connected UAV swarm, IEEE VTC-Spring

`dang2023graphic` · status **P** · evidence **FT**

* **Research question:** Detect GPS spoofing in a UAV swarm using a GNN.
* **Method:** GCN (SimGNN-style) + GRU compare the swarm GPS topology (distances) with the communication topology (free-space path loss); threshold on predicted graph-edit similarity.
* **Data / conditions:** Own Python/TensorFlow simulator with 6, 8 and 10 UAVs, wind and GPS noise, a spoofing attacker; no real data.
* **Metrics:** Accuracy (>90% for 10 UAVs), computation time (<10 ms vs ≈16 s for exact GED).
* **Main findings:** Accuracy decreases as GPS error grows; GRU converges faster than LSTM.
* **Assumptions:** Spoofing does not affect swarm/BS communication; communication topology reflects true geometry (path-loss); path loss is a reliable reference.
* **Weaknesses / reproducibility:** Simulation only; accuracy without class balance or PR-AUC; communication treated as trustworthy ground reference, packet loss/staleness not modelled although the text acknowledges environmental effects on the communication topology.
* **Relation to RA-SCM:** Closest GNN spoof-detector for swarms; it uses the channel as *independent evidence*, whereas we treat the channel as an *unreliable* source and test robustness to it.

### Mykytyn et al. 2023, GPS-spoofing attack detection mechanism for UAV swarms, MECO (arXiv:2301.12766)

`mykytyn2023gps` · status **P** · evidence **FT**

* **Research question:** Detect single- and multi-transmitter GPS spoofing in a swarm without extra hardware beyond ranging.
* **Method:** Compare GPS-derived inter-UAV distances with IR-UWB ranging; flag if the discrepancy exceeds a threshold (with timestamp tolerance).
* **Data / conditions:** None — the text states this is the initial stage and that detection and false-positive rates will be presented later.
* **Metrics:** None reported.
* **Main findings:** Qualitative argument that the mechanism is simple and low-cost.
* **Assumptions:** Ranging available and synchronised with GPS timestamps; thresholds from sensor accuracy.
* **Weaknesses / reproducibility:** No empirical results in the version read; thresholding only.
* **Relation to RA-SCM:** Defines the independent-ranging principle used by our physics baseline and by the identifiability condition.

### Bi et al. 2024, Detection and mitigation of position spoofing attacks on cooperative UAV swarm formations, IEEE TIFS 19

`bi2024detection` · status **P** · evidence **FT(partial)**

* **Research question:** Identify malicious UAVs that falsify reported positions (distributed, collusion, mixed attacks).
* **Method:** Localisation-feasibility problem with reported positions + pairwise distance measurements; semidefinite relaxation; two algorithms exploiting neighbour proximity.
* **Data / conditions:** Matlab simulations of swarms with Gaussian position and ranging noise.
* **Metrics:** Detection success rate (up to +65%, +55%, +51% vs benchmarks).
* **Main findings:** Outperforms benchmarks against the three attack types in simulation.
* **Assumptions:** All UAVs report positions and range neighbours; reports and measurements are received (no packet loss appears in the text); snapshot (non-temporal) formulation.
* **Weaknesses / reproducibility:** Convex-relaxation cost; no temporal evidence; no unreliable-communication model; no learning.
* **Relation to RA-SCM:** Strongest model-based competitor in principle (not re-implemented here — disclosed). Its feasibility test is the identifiability principle we use; communication unreliability would convert 'infeasible' into 'missing'.

### Tolstaya et al. 2020, Learning decentralized controllers for robot swarms with GNNs, CoRL (PMLR 100)

`tolstaya2020learning` · status **P** · evidence **FT**

* **Research question:** Learn local controllers for large teams with limited communication.
* **Method:** Aggregation GNNs on time-varying communication graphs, imitation of a centralised controller.
* **Data / conditions:** Simulated flocking with a changing communication graph.
* **Metrics:** Control performance (abstract).
* **Main findings:** Multi-hop information from distant teammates helps more when the communication radius is small or speeds are high (abstract).
* **Assumptions:** Each communication exchange adds one step of delay (k-hop information is k steps old, Secs 2–3, 'Delayed Aggregation GNNs'); no packet loss or link failure.
* **Weaknesses / reproducibility:** Control, not detection; delivery failures not modelled.
* **Relation to RA-SCM:** Evidence that GNNs on dynamic swarm graphs are practical; its delayed information structure is the precursor of our delayed-message semantics.

### Cini, Marisca & Alippi 2022, GRIN: multivariate time-series imputation by GNNs, ICLR

`cini2022filling` · status **P** · evidence **AB**

* **Research question:** Reconstruct missing values in sensor-network time series.
* **Method:** Bidirectional spatio-temporal message passing recurrent GNN.
* **Data / conditions:** Real-world sensor benchmarks (abstract-level).
* **Metrics:** MAE (improvements often >20% over prior state of the art, abstract).
* **Main findings:** Graph-aware imputation beats non-graph imputers.
* **Assumptions:** Missingness is the only data defect (no adversarial or drifting values).
* **Weaknesses / reproducibility:** Does not separate missing from corrupted data; imputation, not detection.
* **Relation to RA-SCM:** Shows graphs help with *missing* data; our problem is the confusion between missing and *corrupted* data.

### Zhu et al. 2019, Robust GCNs against adversarial attacks, KDD

`zhu2019robust` · status **P** · evidence **AB**

* **Research question:** Make GCNs robust to adversarially perturbed graphs.
* **Method:** Gaussian node representations; variance-based attention reduces the weight of nodes with high variance.
* **Data / conditions:** Three benchmark citation graphs.
* **Metrics:** Node-classification accuracy.
* **Main findings:** Substantial accuracy gains against several attack strategies (abstract).
* **Assumptions:** Variance reflects attack influence.
* **Weaknesses / reproducibility:** Variance is learned, not tied to a physical reliability variable.
* **Relation to RA-SCM:** Prior art for uncertainty-weighted aggregation against *corrupted* (adversarial) inputs, not missing data: reliability *weighting* is **not** new in GNNs; our weights use explicit communication metadata (age, delivery, link quality).


---

### Round 2 additions (pre-submission check, 6 November 2026)

The entries below were added after the IEEE/ACM-oriented search of round 2 (see S1). Every record was confirmed on Crossref or the arXiv API; content statements come from the abstract (AB) or from the stated full-text sections (FT).

### Chen, Meng, Li & Liao 2022, Cooperative fault detection and recovery in the GNSS positioning of mobile agent swarms based on relative distance measurements, Chinese J. Aeronautics 35(5)

`chen2022cooperative` · status **P** · evidence **AB** (publisher PDF not accessible)

* **Method:** Noncentral χ² test of each edge (reported versus measured distance), maximum-likelihood identification of the faulty vertex, distance-based recovery; detectability and recoverability related to the structure of the relative-measurement network.
* **Data / conditions:** Simulation of a swarm crossing a GNSS spoofing zone.
* **Assumptions:** Current, delivered measurements; no packet loss, delay or staleness mentioned.
* **Relation to RA-SCM:** Direct model-based predecessor of our physics baseline; our AoI-aware variant adds an age-dependent covariance.

### He, Shan & Huang 2024, Robust Cooperative Localization With Failed Communication and Biased Measurements, IEEE RA-L 9(3)

`he2024robust` · status **P** · evidence **AB**

* **Method:** Decentralised CL that decouples measurement from communication; other robots' states propagated by an approximate motion model during outages; M-estimation down-weights biased measurements. Simulation.
* **Relation to RA-SCM:** Handles failed communication and faulty measurements *jointly*, but as robust estimation scored by localisation error, not as detection; not UAV-specific, not learned.

### Kargar Tasooji & Parasuraman 2025, Distributed Fault-Tolerant Multi-Robot Cooperative Localization in Adversarial Environments, IROS 2025

`kargartasooji2025distributed` · status **P** · evidence **FT** (arXiv:2507.06750, Sec. III-B, Eq. 8)

* **Method:** Distributed cubature Kalman filter; innovation-norm gate discards manipulated measurements; binary per-link success indicator in jammed zones (prediction-only on failure); adaptive event-triggered communication. Robotarium ground robots.
* **Metrics:** Localisation error (MSLE) and communication rate; detection itself is not scored (no ROC/AUC/F1, no seeds).
* **Relation to RA-SCM:** Closest classical work combining attacks and link failure; link loss is ridden through, not distinguished from attacks.

### Cao, Zhao, Wu, Wang & Gong 2026, Quality-Aware Distributed State Estimation for Multi-UAV Cooperative Localization Under Communication and Navigation Constraints, Drones 10(6)

`cao2026quality` · status **P** · evidence **AB**

* **Method:** Per-neighbour multiplicative quality score from freshness (AoI), accuracy (covariance trace) and link reliability (packet loss, channel noise); AND-gate excludes neighbours degraded in both AoI and covariance; quality-squared information update with covariance-intersection fallback; theorems on soft attenuation of single-axis faults.
* **Metrics:** Position RMSE in Monte Carlo runs (3–50 UAVs).
* **Relation to RA-SCM:** Closest model-based analogue of AoI- and link-quality-driven weighting; an estimator, not a detector, with no learned or graph comparison.

### Ou, Liang & Lam 2023, FPECMV: Learning-Based Fault-Tolerant Collaborative Localization Under Limited Connectivity, IROS 2023

`ou2023fpecmv` · status **P** · evidence **AB**

* **Method:** CNN-based confidence evaluation and a fault-isolation module using randomly occurring relative measurements, for CL with limited or discontinued observation and communication; BULLET simulation and physical robots (21.0% localisation improvement).
* **Relation to RA-SCM:** Learned fault handling under limited connectivity, but judged on localisation accuracy, ground robots, no controlled loss model.

### Vijay et al. 2025, Range-Based Multi-Robot Integrity Monitoring For Cyberattacks and Faults: An Anchor-Free Approach, IEEE RA-L 10(3)

`vijay2025range` · status **P** · evidence **FT** (arXiv:2408.11155, Sec. III-B)

* **Method:** Inter-robot ranges detect and identify attacked or faulty robots and reconstruct their errors (sequential convex programming + ADMM); PX4-SITL/Gazebo under GNSS spoofing and real Crazyflie UAVs.
* **Assumptions:** Synchronous communication between neighbours (Sec. III-B).
* **Relation to RA-SCM:** Strongest model-based range-consistency detector found; delivery assumed.

### Michieletto, Formaggio, Cenedese & Tomasin 2023, Robust Localization for Secure Navigation of UAV Formations Under GNSS Spoofing Attack, IEEE T-ASE 20(4)

`michieletto2023robust` · status **P** · evidence **AB**

* **Method:** Information-theoretic threshold test of consistency between inertial, relative-ranging and GNSS data, then reliability-based fusion; numerical validation.
* **Relation to RA-SCM:** Multimodal consistency testing for formations; no communication-loss model.

### Park & Yoo 2026, Rigid-Covert GNSS Spoofing of UAV Swarms, arXiv:2608.06885

`park2026rigid` · status **X** · evidence **FT**

* **Main findings:** A common, slowly varying offset of the whole swarm preserves all pairwise distances and is unobservable to relative-only detectors (distance-verification and SDP baselines near chance AUC over 200 seeds); anchor-based detection floor and recovery (simulation, SITL, Gazebo). Ranging packet loss is swept only for recovery.
* **Relation to RA-SCM:** Formal support for our identifiability statement; RA-SCM inherits this blind spot.

### Sophia et al. 2026, Zero-trust graph-attentive intelligence for Byzantine-resilient UAV swarms under communication constraints, Discover Electronics 3(1)

`sophia2026zerotrust` · status **P** · evidence **AB** (Springer full text not retrievable)

* **Method:** 8-head GAT with a zero-trust layer (behavioural scoring, attestation, neighbourhood analysis); UAVSwarm data with a Byzantine and communication overlay (spoofing, replay, Sybil, gradient poisoning; 5–33% corrupted nodes).
* **Metrics:** Byzantine F1 96.8% (model-level comparison; 92.83% mean over 12 attack × corruption conditions), trust accuracy, consensus latency, packet delivery ratio.
* **Relation to RA-SCM:** Learned graph detector for swarms in which communication is a bandwidth constraint and an outcome, not a modelled confounder of position-consistency evidence; no physics baseline.

### Pan et al. 2026, Satellite-Aided Multi-UAV Secure Collaborative Localization via Spatio-Temporal Anomaly Detection and Diagnosis, Drones 10(1)

`pan2026satellite` · status **P** · evidence **AB**

* **Method:** GAT with a time-attention VAE on multidimensional ranging sequences detects false ranging data from malicious UAVs; diagnosis by anomaly scoring; KNN correction (simulation; +25.9% localisation accuracy).
* **Relation to RA-SCM:** Closest learned graph detector on relative (ranging) data; delivery of measurements assumed.

### Tariq, Ahanger & Shaukat 2026, Tri-stream multi-model architecture for real-time detection of BeiDou signal manipulation in UAV swarms, Scientific Reports 16

`tariq2026tristream` · status **P** · evidence **FT** (PMC full text)

* **Method:** Kalman-residual tracking plus CNN/LSTM/GNN fusion and a transformer-based language model; software-in-the-loop simulation (97 ± 0.6% detection accuracy).
* **Conditions:** Simulator with per-packet delay, burst-capable packet drop, bandwidth caps, freshness-window gating and jamming; paired t-tests over matched seeds. Inter-UAV ranging is not used.
* **Relation to RA-SCM:** A learned graph swarm detector run under modelled loss (sensitivity to delay and loss is mentioned but not shown); no loss-stratified results and no physics-only arm are reported.

### Tariq & Shaukat 2026, Mission-aware BeiDou spoofing defense in UAV swarms with LLM-assisted context validation, Frontiers in Communications and Networks 7

`tariq2026mission` · status **P** · evidence **FT**

* **Method:** OrbitGuardNet: transformer encoders, GNNs and Kalman-residual analysis with LLM context validation; UWB inter-UAV ranging; simulation and pilot flights with three UAVs (software-injected spoofing).
* **Conditions:** Gilbert–Elliott channel with delays and bursty loss (Sec. 2.1.3); paired t-tests; packet loss named as a future test condition, not varied.
* **Relation to RA-SCM:** Closest learned work; lacks loss as a controlled confounder and a standalone age-aware physics baseline.

### Moustafa & Abdelghany 2026, Finite-Trace Cellular Sheaves for Validation and Estimation of Hybrid Dynamical Systems, IEEE Control Systems Letters 10

`moustafa2026finite` · status **P** · evidence **AB**

* **Method:** Finite-trace cellular sheaf with affine restriction maps for hybrid and networked executions with partial and non-simultaneous data; convex best-section estimator; per-cell residual scores localise model inconsistency; demonstrated on a DC microgrid and a linearised drone pose graph (corrupted-observation localisation).
* **Relation to RA-SCM:** Non-learned sheaf fault localisation with affine maps; no packet-loss or AoI model.

### Foundational and context sources (round 2)

| Key | Work | Status / evidence | Used for |
|---|---|---|---|
| `kaul2012realtime` | Kaul, Yates & Gruteser 2012, Real-time status: how often should one update?, IEEE INFOCOM | P / AB | definition of age of information |
| `sinopoli2004kalman` | Sinopoli et al. 2004, Kalman filtering with intermittent observations, IEEE TAC 49(9) | P / AB | lost packets as intermittent observations |
| `julier1997nondivergent` | Julier & Uhlmann 1997, covariance intersection, ACC | P / AB | fusion under unknown correlation (no detection) |
| `willsky1976survey` | Willsky 1976, failure detection in dynamic systems, Automatica 12(6) | P / AB | residual-based fault detection |
| `brown1992baseline` | Brown 1992, a baseline GPS RAIM scheme, Navigation 39(3) | P / AB | GPS integrity monitoring |
| `kerns2014unmanned` | Kerns et al. 2014, UAV capture via GPS spoofing, J. Field Robotics 31(4) | P / AB | field evidence of UAV spoofing |
| `tippenhauer2011requirements` | Tippenhauer et al. 2011, requirements for GPS spoofing attacks, ACM CCS | P / AB | spoofing several receivers |
| `hayat2016survey` | Hayat, Yanmaz & Muzaffar 2016, UAV networks survey, IEEE COMST 18(4) | P / AB | intermittent UAV links |
| `gilbert1960capacity` | Gilbert 1960, capacity of a burst-noise channel, Bell Syst. Tech. J. 39(5) | P / AB | Gilbert–Elliott burst-loss model (round 1) |
| `elliott1963estimates` | Elliott 1963, error rates on burst-noise channels, Bell Syst. Tech. J. 42(5) | P / AB | Gilbert–Elliott burst-loss model (round 1) |


<div class="pagebreak"></div>

## S3. Critical synthesis, gap verification and originality ledger


*Established findings are separated from the project's interpretations. "Interpretation" paragraphs are our reading, not results of the cited papers.*

### 1. What the literature establishes

1. **Sheaf learning.** Replacing the graph Laplacian by a sheaf Laplacian generalises diffusion: hand-built sheaves beat GCN on synthetic signed graphs (Hansen & Gebhart 2020), and maps learned from node features are competitive on heterophilic node classification and control oversmoothing in theory (Bodnar et al. 2022). Whether restriction maps must be *learned* is contested: by the authors' conclusion, computed orthogonal maps match or beat learned ones on most datasets, though they trail on Squirrel and Chameleon (Barbero et al. 2022, Table 1 and Sec. 5).
2. **Sheaves for sensor consistency (non-learned).** Robinson (2017) and Joslyn et al. (2020) use sheaf-valued sensor data, a consistency radius and a consistency filtration to *flag* disagreement between heterogeneous sensors. Joslyn et al. attribute disagreement to sensors with a consistency filtration but state that neither radius nor filtration says which measurements are trustworthy. Hernández & Sánchez-Soto (2026, full text) propose the sheaf Dirichlet energy as an anomaly score with faulty-node localisation, without experiments; Moustafa & Abdelghany (2026) localise corrupted observations with finite-trace sheaves.
3. **Sheaves for multi-agent control.** Hanks et al. (2025) solve consensus/formation/flocking with nonlinear sheaf Laplacians and ADMM under a fixed topology, without packet loss or fault detection.
4. **Sheaves + time.** Temporal sheaf networks exist for link prediction (Asif et al. 2026, preprint).
5. **GNN-based swarm spoofing detection.** Dang et al. (2023) use GCN+GRU on the GPS-vs-communication topology (simulation, accuracy-based). Model-based swarm detectors use reported positions plus pairwise ranging (Mykytyn et al. 2023, thresholds, no results in the version read; Bi et al. 2024, semidefinite feasibility, simulation).
6. **GNNs and missing data.** Graph imputation handles missing sensor values (Cini et al. 2022); uncertainty-weighted (variance-based) attention exists as a defence against adversarially corrupted graphs, not missing data (Zhu et al. 2019); graph anomaly detectors for sensors assume complete synchronous observations (Deng & Hooi 2021).

7. **Classical and recent cooperative localisation (round 2).** Failed links, packet loss and AoI are handled *together with* faulty or attacked measurements by robust estimation: M-estimation with motion-model propagation (He et al. 2024), an innovation gate under jamming (Kargar Tasooji & Parasuraman 2025), learned confidence with fault isolation (Ou et al. 2023), an AoI × covariance × link-quality score (Cao et al. 2026). They are scored by localisation error, not as detectors. Model-based swarm detectors (Chen et al. 2022; Michieletto et al. 2023; Vijay et al. 2025) assume delivered data. Learned graph swarm spoofing detectors have been simulated with delay and bursty loss (Tariq et al. 2026; Tariq & Shaukat 2026) but without loss as a controlled factor or a physics-only arm.

### 2. Contradictions, methodological differences, transfer risks

* **Learned vs computed maps** (Bodnar vs Barbero): different evidence about whether learning the sheaf is necessary; both on node-classification benchmarks. *Interpretation:* for a swarm the maps are partly *known physics*, so the question moves from "learn or compute" to "which part of the map is known".
* **What counts as independent evidence differs across swarm papers:** UWB ranging (Mykytyn), pairwise range measurements (Bi), communication path loss (Dang). Dang et al. treat the communication topology as a trustworthy reference; Bi et al. assume reports and measurements arrive. *Interpretation:* none of the three treats communication unreliability as a confounder of the inconsistency signal.
* **Metrics are not comparable:** accuracy (Dang), detection success rate (Bi), none (Mykytyn), F1 under a threshold protocol (Deng & Hooi). None reports precision–recall area or false-positive behaviour under loss.
* **Benchmark transfer:** sheaf results concern heterophily/oversmoothing in node classification; they do not show an advantage for detecting local inconsistencies on a physically constrained swarm graph. This is an assumption we must test, not a transferable result.
* **Data limitations:** almost all UAV-swarm evidence in the retrieved set is simulation-only (exceptions: mixed-reality Crazyflie flights in Vijay et al. 2025, a three-UAV pilot in Tariq & Shaukat 2026); Joslyn et al.'s field study is the only real-data sheaf application and is a small case study.
* **Reproducibility:** only Park & Yoo (2026) state released code in the sections read (not systematically checked); Mykytyn et al. report no experimental numbers at all in the version read.

### 3. Gap verification (questions from the project brief)

| Question | Finding (within the search coverage declared in S1) |
|---|---|
| Has reliability-aware sheaf modelling been studied for this task? | No such study was found: four gap-check queries (sheaf+anomaly detection; sheaf+cooperative localisation; sheaf+false-data-injection; sheaf+reliability/packet loss) returned no matching paper. The 2026 preprint arXiv:2606.19529 was read in full in round 2: it proposes a sheaf Dirichlet-energy anomaly score with faulty-node localisation, without experiments or a loss model. |
| Do comparable GNN methods already incorporate communication reliability? | Partly in other forms: variance/uncertainty-weighted aggregation (Zhu et al.), attention weights (GAT), imputation for missing values (GRIN). Model-based cooperative localisation does use AoI, packet loss and link quality as weights (Cao et al. 2026; He et al. 2024; Kargar Tasooji & Parasuraman 2025), and learned swarm detectors have been simulated under loss (Tariq et al. 2026; Tariq & Shaukat 2026); none uses link metadata in a detector evaluated with loss as a controlled factor against an age-aware physics test. |
| Are there simpler approaches that address the same problem? | Yes — a statistical consistency test that inflates residual variance with the age of the last report (an *age-aware physics detector*). This is implemented here as the strongest simple competitor. Classical cooperative-localisation fault tolerance (covariance intersection/union, robust M-estimation, innovation gates; reviewed in round 2) is another family, **not** implemented. |
| Could the apparent gap come from incomplete coverage? | Yes, but less so after round 2: IEEE/ACM records were searched through Crossref, OpenAlex and Semantic Scholar, not through the native interfaces. The gap is therefore stated as "not found", not "does not exist". |
| Does sheaf modelling give a plausible theoretical advantage? | Plausible, not demonstrated: (i) geometric consistency of reported vs measured relative position is naturally an edge-wise comparison in a shared edge space; (ii) node-specific restriction maps can absorb formation rotation/scale differences; (iii) a weighted sheaf Laplacian offers a principled place for precision weights. Against it: a physics test already implements (i) exactly, and generic edge-conditioned message passing can learn (i)–(iii) without sheaf structure. |
| When might it give no improvement? | If the age-aware physics detector is near-optimal (then learned models cannot add information); if restriction maps collapse to identity (then RA-SCM = edge-conditioned MPNN); if packet loss only affects data that the temporal model already carries; if anomalies are fully common-mode (unobservable). |

### 4. Gap statement (revised after round 2, evidence-supported)

> Model-based cooperative localisation already tolerates failed links, packet loss and AoI together with faulty measurements, and learned graph detectors of swarm spoofing have been run in simulators that include packet loss. Within the sources we could access, however, no study reports how detectors of UAV position anomalies, learned graph- or sheaf-based ones in particular, built on the consistency of reported positions with inter-UAV relative measurements, perform when **iid loss, burst loss and AoI are controlled and results are stratified by condition**, compared against **a standalone age-aware physical-consistency baseline**.

The round-1 supporting sentences "existing swarm detectors assume reliable delivery" and "existing sheaf work does not address anomaly detection or lossy links" were **withdrawn**: they are contradicted by the round-2 sources listed in item 7 and by Hernández & Sánchez-Soto (2026). Because the question is empirical, the contribution is framed as a *controlled test of a hypothesis*, including the possibility that the answer is negative.

### 5. Originality ledger

| Component | Origin |
|---|---|
| Cellular sheaf, sheaf Laplacian, restriction maps | **Taken** from literature (Hansen & Ghrist 2019; Hansen & Gebhart 2020) |
| Learning restriction maps from endpoint node states, diffusion layer form | **Taken/adapted** from NSD (Bodnar et al. 2022); dense implementation, own code |
| GCN, GAT layers | **Taken** (Kipf & Welling; Veličković et al.), dense re-implementations cross-checked against PyG in unit tests |
| Weighting messages by uncertainty | **Taken** as an idea (Zhu et al. 2019; classical precision weighting) — *not claimed as new* |
| Gilbert–Elliott loss, age-of-information staleness, constant-velocity compensation | **Taken** (Gilbert 1960; Elliott 1963; standard kinematics) |
| Consistency of reported vs measured relative position as the inconsistency measure | **Taken** from swarm fault/spoofing work (Chen et al. 2022 edge χ² tests; Mykytyn et al.; Bi et al.) and sheaf sensor consistency (Robinson; Joslyn et al.) |
| Delayed-message semantics: every layer reads *cached sender embeddings from the time of the last delivered packet*, applied identically to all models | **Adapted** from the delayed information structure of decentralised GNN controllers (Tolstaya et al. 2020: k-hop information is k steps old), extended to lost packets |
| Affine (data-dependent translation) restriction: ρ = F_i x_i − F_j x_j − b_ij, b_ij a second output head of Φ, equivalent to a sheaf on stalks augmented with f constant coordinates | **Adapted** (affine maps are also used, non-learned, by Moustafa & Abdelghany 2026) |
| Receiver-specific reliability weights learned from delivery flag, age and link quality, plus an evidence-mass feature, inside sheaf-style diffusion | **Combined in a new manner** (AoI/link-quality weighting is known from estimation, Cao et al. 2026; the learned combination with sheaf-style diffusion for detection was not found). The implemented layer is receiver-centric and equals a weighted sheaf Laplacian only for symmetric maps and weights |
| Experimental protocol: loss/burst/targeted-blackout as a controlled confound, frozen operating point, paired seeds, age-aware physics control, ablation separating edge-conditioning / sheaf maps / weights / reliability channel / temporal memory | **Proposed** as the genuinely new element (a protocol contribution, not an algorithmic one). Individual elements exist elsewhere (modelled loss and paired seeds in Tariq et al. 2026); their combination was not found in the sources searched |

No component is presented as a new mathematical invention.
