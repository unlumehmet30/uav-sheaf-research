# Literature search protocol and log

**Search periods:** round 1 on 27 October 2026; round 2 (pre-submission check) on 6 November 2026. **Searcher:** the project author with AI assistance (round 1: Claude Sonnet 5.5; round 2: Claude Opus 5.5; see the AI-assistance declaration in the report).

## What was actually searched (and what was not)

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
* Items from low-visibility or unrefereed venues when a peer-reviewed source covers the same idea (round 2).

## Items found but not included in the matrix (context only)
* *Sheaf Graph Neural Networks via PAC-Bayes Spectral Optimization* (arXiv:2508.00357; arXiv comment: AAAI 2026, acceptance not verified): node-level certified confidence intervals, **not** edge reliability; only the abstract page was read.
* *From Classical to Topological Neural Networks Under Uncertainty* (arXiv:2602.10266): book chapter; no sheaf/anomaly/communication content in the abstract.
* *Sheaf-Theoretic Planning* (arXiv:2605.01879): categorical planning report, no learning/anomaly detection in the abstract.
* Resilient collaborative localisation under spoofed radio measurements, fault-tolerant cooperative localisation by covariance union, and the Chinese J. Aeronautics 2022 paper on GNSS faults in swarms were seen as snippets in round 1. **Resolved in round 2:** the last is Chen et al. 2022 (now in the matrix and the report); the first is Karstensen & Galeazzi, arXiv:2511.21432 (ideal links, one scenario; screened, not cited); the covariance-union line is Uhlmann 2003 (Information Fusion 4(3), metadata only) and Wang et al. 2021 (IEEE RA-L 6(4), abstract only), screened but not cited.

## Round 2 query log (6 November 2026)

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

## Round 2: screening decisions

**Added to the report and the matrix:** Chen et al. 2022; He et al. 2024; Kargar Tasooji & Parasuraman 2025; Cao et al. 2026; Ou et al. 2023; Vijay et al. 2025; Michieletto et al. 2023; Park & Yoo 2026 (preprint); Sophia et al. 2026; Pan et al. 2026; Tariq et al. 2026 (Sci. Rep.); Tariq & Shaukat 2026 (Front. Commun. Netw.); Moustafa & Abdelghany 2026; and the foundational sources Kaul et al. 2012, Sinopoli et al. 2004, Julier & Uhlmann 1997, Willsky 1976, Brown 1992, Kerns et al. 2014, Tippenhauer et al. 2011, Hayat et al. 2016.

**Screened, not cited** (reason in brackets): Mitra et al. 2019, Autonomous Robots (resilient estimation of an external process); Chang et al. 2022, IEEE T-RO (CI-based localisation under missing links/observations, no erroneous data); Wang et al. 2021, IEEE RA-L (covariance-union fault tolerance, no loss model); Kargar Tasooji & Marquez 2022, IEEE Access (DoS + false-data-injection resilient estimation); Qu et al. 2017, IEEE Access (UAV fault-tolerant cooperative positioning, no loss model); Causa & Fasano 2023, PLANS and Gipson & Leishman 2022, IEEE TAES (fault detection and exclusion, no loss model); Olawoye & Gross 2026, Applied Sciences (distributed fault isolation for ranging-based localisation); Liu et al. 2026, IEEE TIM (parity-vector GNSS fault detection with relative ranging); Mughal et al. 2026, IEEE IoT-J (network intrusion detection); You et al. 2026, Drones (delay/loss diagnosis on the communication side only); Alamleh & Pulatov 2026, SpliTech (non-learned link-quality and staleness weighting of range constraints); Voitovych & Bychkov 2026 (conference proceedings, hand-designed guard statistics); Almekhyal et al. 2026 (single-UAV learned detectors with injected packet loss); Abima et al. 2026, ACM (relay-risk score, paired Monte Carlo); Fan et al. 2023, MILCOM and Gu et al. 2025, ICPADS (swarm spoofing detection/defence without loss model); Poornima 2026 and Cui 2026 (low-visibility venues); preprints and software (Coulibaly et al. 2026, TRUST-V; Tariq et al. PINN-CMA software; Karstensen & Galeazzi 2025); Moreau 2026 and Pasupuleti 2025 (weak venues, not detection of position anomalies). Only abstracts were read for most of these.

**Effect on the gap:** the gap was narrowed (report Section 4). Joint handling of link failures and faulty measurements exists in model-based cooperative localisation, and learned graph swarm detectors have been run under simulated loss; what remains unaddressed in the sources read is loss/AoI as a *controlled, stratified* confounder of position-consistency detection, compared against a standalone age-aware physics baseline.

**Note:** one OpenAlex response contained text addressed to automated agents (a request to register an API key with the user's e-mail); it was ignored.

