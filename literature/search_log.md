# Literature search protocol and log

**Search period:** 27 October 2026 (single working session). **Searcher:** the project author with AI assistance (Claude Sonnet 5.5, see AI-use statement in the report).

## What was actually searched (and what was not)

| Channel | How it was used | Limitation |
|---|---|---|
| General web search tool (US-only index) | 22 keyword queries, listed below | not a bibliographic database; ranking is opaque; no date/venue filters |
| arXiv API (`export.arxiv.org/api/query?id_list=...`) | metadata (authors, dates, comment/venue field) of every arXiv-hosted item | metadata only |
| Crossref REST API | DOI, venue, volume, pages for every item that has a DOI | some items have no DOI (NeurIPS, ICLR, PMLR) |
| Publisher / proceedings pages (NeurIPS proceedings, PMLR, AAAI OJS, Springer, MDPI/PMC) | confirm venue and bibliographic data | – |
| Full-text reading | Dang et al. 2023, Bi et al. 2024, Mykytyn et al. 2023 (key sections extracted from the PDFs); Joslyn et al. 2020 and Hanks et al. 2025 (via text retrieval, truncated for Joslyn) | all other entries: **abstract-level reading only** plus the author's prior knowledge of GCN/GAT/NSD |
| IEEE Xplore, ACM DL, Scopus, Web of Science native search | **not queried through their own search interfaces** (no access in this environment). IEEE/ACM items were reached through DOIs/Crossref and through preprint mirrors | **coverage of IEEE/ACM conference literature may be incomplete — this is the main threat to the research-gap claim and should be closed by repeating the queries below in those databases before submission** |

## Keywords (combined with AND/OR as shown in the query list)

* Sheaf learning: *sheaf neural network*, *neural sheaf diffusion*, *cellular sheaf*, *sheaf Laplacian*, *restriction map*, *connection Laplacian*, *nonlinear sheaf diffusion*, *temporal / dynamic sheaf*
* Graph anomaly detection: *graph neural network anomaly detection multivariate time series*, *sensor fault detection GNN*, *missing data / unreliable edges*
* UAV reliability: *GPS spoofing detection UAV swarm*, *cooperative localization spoofing / fault*, *position spoofing swarm formation*, *packet loss multi-robot GNN*
* Communication models: *Gilbert–Elliott burst loss*
* Robust/uncertainty-aware GNNs: *robust GCN variance attention*, *edge reliability weighting*

## Query log (all executed 2026-10-27)

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

## Inclusion criteria
1. Directly about at least one of: sheaf-based learning/diffusion/sensor integration; GNN-based anomaly or spoofing detection; UAV/multi-robot swarm position consistency, spoofing or cooperative localisation; GNN behaviour under missing/unreliable data or communication; burst-loss channel models used in the simulator.
2. Bibliographic data verifiable in an independent record (arXiv API, Crossref, publisher page).
3. Peer-reviewed, **or** a clearly labelled preprint/workshop paper that is the only/primary source for a specific idea. Status is recorded in the matrix and the bibliography.
4. English language, 1960–2026 (foundational channel models and GCN/GAT are older; sheaf learning is 2019+).

## Exclusion criteria
* Patents, blog/skill/playbook pages, and aggregator summaries as sources of claims (they appeared in the search results and were used only to find primary sources).
* Items for which bibliographic data could not be confirmed.
* UAV-swarm work on intrusion detection by federated learning, single-UAV spoofing detectors using radio fingerprints/cellular signals, and GNSS signal-authentication schemes — relevant context but not about swarm-level geometric consistency under unreliable communication.
* Results that appeared only as aggregator summaries with numbers not found on the primary page (e.g. benchmark F1 values on third-party leaderboards).

## Items found but not included in the matrix (context only)
* *Sheaf Graph Neural Networks via PAC-Bayes Spectral Optimization* (arXiv:2508.00357; arXiv comment: AAAI 2026, acceptance not verified): node-level certified confidence intervals, **not** edge reliability; only the abstract page was read.
* *From Classical to Topological Neural Networks Under Uncertainty* (arXiv:2602.10266): book chapter; no sheaf/anomaly/communication content in the abstract.
* *Sheaf-Theoretic Planning* (arXiv:2605.01879): categorical planning report, no learning/anomaly detection in the abstract.
* Resilient collaborative localisation under spoofed radio measurements (2025 preprint found via search; not retrieved), fault-tolerant cooperative localisation by covariance union, Chinese J. Aeronautics 2022 paper on detectability/recoverability of GNSS faults in swarms — **found in search snippets only, not verified or read; they suggest that classical cooperative-localisation work on fault/spoof tolerance is a closer competitor than the GNN literature and should be reviewed before submission.**
