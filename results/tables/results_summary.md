# Results summary

Seeds: [0, 1, 2, 3, 4] (n = 5). Cells: mean ± 95% t-interval half-width over seeds. PR-AUC = average precision (scikit-learn definition). All numbers come from `results/raw/`; operating point = threshold with 5% FPR on the validation split, frozen for all test conditions.


## E1/E2 — PR-AUC vs iid packet loss

|               | iid_0         | iid_10        | iid_30        | iid_50        |
|:--------------|:--------------|:--------------|:--------------|:--------------|
| physics_naive | 0.894 ± 0.025 | 0.889 ± 0.025 | 0.863 ± 0.029 | 0.804 ± 0.033 |
| physics_aoi   | 0.894 ± 0.025 | 0.894 ± 0.024 | 0.891 ± 0.024 | 0.888 ± 0.023 |
| gcn           | 0.960 ± 0.019 | 0.961 ± 0.018 | 0.958 ± 0.018 | 0.951 ± 0.016 |
| gcn_drop      | 0.965 ± 0.014 | 0.964 ± 0.012 | 0.959 ± 0.016 | 0.949 ± 0.019 |
| gat           | 0.968 ± 0.016 | 0.967 ± 0.016 | 0.963 ± 0.020 | 0.956 ± 0.021 |
| nsd           | 0.968 ± 0.019 | 0.968 ± 0.018 | 0.967 ± 0.016 | 0.959 ± 0.016 |
| rascm         | 0.974 ± 0.019 | 0.975 ± 0.018 | 0.975 ± 0.018 | 0.975 ± 0.019 |


## E2 — FPR at the frozen operating point vs iid packet loss

|               | iid_0         | iid_10        | iid_30        | iid_50        |
|:--------------|:--------------|:--------------|:--------------|:--------------|
| physics_naive | 0.038 ± 0.019 | 0.040 ± 0.019 | 0.048 ± 0.018 | 0.068 ± 0.019 |
| physics_aoi   | 0.124 ± 0.031 | 0.123 ± 0.031 | 0.121 ± 0.031 | 0.115 ± 0.031 |
| gcn           | 0.015 ± 0.002 | 0.017 ± 0.001 | 0.022 ± 0.002 | 0.029 ± 0.012 |
| gcn_drop      | 0.021 ± 0.008 | 0.022 ± 0.006 | 0.027 ± 0.004 | 0.039 ± 0.007 |
| gat           | 0.020 ± 0.009 | 0.021 ± 0.008 | 0.023 ± 0.007 | 0.029 ± 0.011 |
| nsd           | 0.019 ± 0.004 | 0.019 ± 0.004 | 0.023 ± 0.004 | 0.031 ± 0.008 |
| rascm         | 0.032 ± 0.009 | 0.031 ± 0.009 | 0.031 ± 0.009 | 0.031 ± 0.012 |


## E2 — recall at the frozen operating point vs iid packet loss

|               | iid_0         | iid_10        | iid_30        | iid_50        |
|:--------------|:--------------|:--------------|:--------------|:--------------|
| physics_naive | 0.862 ± 0.044 | 0.860 ± 0.044 | 0.857 ± 0.048 | 0.847 ± 0.050 |
| physics_aoi   | 0.950 ± 0.018 | 0.949 ± 0.018 | 0.945 ± 0.017 | 0.940 ± 0.018 |
| gcn           | 0.935 ± 0.025 | 0.936 ± 0.025 | 0.937 ± 0.027 | 0.932 ± 0.031 |
| gcn_drop      | 0.949 ± 0.016 | 0.948 ± 0.016 | 0.945 ± 0.015 | 0.944 ± 0.015 |
| gat           | 0.946 ± 0.035 | 0.948 ± 0.031 | 0.947 ± 0.029 | 0.942 ± 0.027 |
| nsd           | 0.948 ± 0.030 | 0.950 ± 0.026 | 0.951 ± 0.024 | 0.942 ± 0.024 |
| rascm         | 0.972 ± 0.025 | 0.971 ± 0.027 | 0.969 ± 0.026 | 0.969 ± 0.025 |


## E2 — noise severity (no packet loss), PR-AUC

|               | noise_1       | noise_2       | noise_3       |
|:--------------|:--------------|:--------------|:--------------|
| physics_naive | 0.871 ± 0.022 | 0.851 ± 0.022 | 0.814 ± 0.023 |
| physics_aoi   | 0.871 ± 0.022 | 0.851 ± 0.022 | 0.814 ± 0.023 |
| gcn           | 0.962 ± 0.011 | 0.931 ± 0.013 | 0.872 ± 0.021 |
| gcn_drop      | 0.963 ± 0.017 | 0.931 ± 0.018 | 0.846 ± 0.053 |
| gat           | 0.968 ± 0.021 | 0.938 ± 0.016 | 0.883 ± 0.013 |
| nsd           | 0.970 ± 0.012 | 0.941 ± 0.016 | 0.894 ± 0.024 |
| rascm         | 0.975 ± 0.014 | 0.949 ± 0.020 | 0.896 ± 0.020 |


## E2 — noise severity (no packet loss), FPR

|               | noise_1       | noise_2       | noise_3       |
|:--------------|:--------------|:--------------|:--------------|
| physics_naive | 0.046 ± 0.007 | 0.002 ± 0.002 | 0.000 ± 0.000 |
| physics_aoi   | 0.142 ± 0.017 | 0.040 ± 0.009 | 0.012 ± 0.005 |
| gcn           | 0.019 ± 0.008 | 0.047 ± 0.019 | 0.117 ± 0.053 |
| gcn_drop      | 0.026 ± 0.010 | 0.091 ± 0.029 | 0.316 ± 0.161 |
| gat           | 0.022 ± 0.018 | 0.039 ± 0.022 | 0.064 ± 0.037 |
| nsd           | 0.019 ± 0.007 | 0.044 ± 0.011 | 0.081 ± 0.014 |
| rascm         | 0.033 ± 0.015 | 0.077 ± 0.022 | 0.133 ± 0.057 |


## E3 — PR-AUC under burst / correlated loss

|               | burst_10      | burst_30      | burst_50      | nodeburst_30   |
|:--------------|:--------------|:--------------|:--------------|:---------------|
| physics_naive | 0.751 ± 0.051 | 0.605 ± 0.056 | 0.519 ± 0.057 | 0.389 ± 0.047  |
| physics_aoi   | 0.891 ± 0.025 | 0.885 ± 0.023 | 0.877 ± 0.022 | 0.885 ± 0.029  |
| gcn           | 0.943 ± 0.020 | 0.919 ± 0.024 | 0.889 ± 0.023 | 0.929 ± 0.029  |
| gcn_drop      | 0.963 ± 0.012 | 0.953 ± 0.015 | 0.939 ± 0.023 | 0.907 ± 0.020  |
| gat           | 0.954 ± 0.021 | 0.929 ± 0.027 | 0.909 ± 0.021 | 0.943 ± 0.018  |
| nsd           | 0.957 ± 0.022 | 0.937 ± 0.012 | 0.907 ± 0.014 | 0.948 ± 0.016  |
| rascm         | 0.972 ± 0.019 | 0.972 ± 0.020 | 0.967 ± 0.026 | 0.958 ± 0.022  |


## E3 — FPR under burst / correlated loss

|               | burst_10      | burst_30      | burst_50      | nodeburst_30   |
|:--------------|:--------------|:--------------|:--------------|:---------------|
| physics_naive | 0.090 ± 0.020 | 0.158 ± 0.026 | 0.196 ± 0.029 | 0.221 ± 0.027  |
| physics_aoi   | 0.120 ± 0.030 | 0.110 ± 0.029 | 0.101 ± 0.029 | 0.110 ± 0.029  |
| gcn           | 0.037 ± 0.008 | 0.061 ± 0.026 | 0.075 ± 0.041 | 0.032 ± 0.009  |
| gcn_drop      | 0.025 ± 0.007 | 0.037 ± 0.007 | 0.054 ± 0.008 | 0.057 ± 0.028  |
| gat           | 0.036 ± 0.007 | 0.057 ± 0.020 | 0.074 ± 0.043 | 0.039 ± 0.019  |
| nsd           | 0.032 ± 0.008 | 0.056 ± 0.014 | 0.070 ± 0.024 | 0.034 ± 0.013  |
| rascm         | 0.033 ± 0.008 | 0.037 ± 0.013 | 0.041 ± 0.015 | 0.047 ± 0.024  |


## E4 — PR-AUC: anomalies + communication failures

|               | targeted_10   | targeted_30   | topo_0        | topo_30       |
|:--------------|:--------------|:--------------|:--------------|:--------------|
| physics_naive | 0.820 ± 0.032 | 0.779 ± 0.035 | 0.892 ± 0.025 | 0.858 ± 0.031 |
| physics_aoi   | 0.891 ± 0.023 | 0.890 ± 0.021 | 0.892 ± 0.025 | 0.889 ± 0.025 |
| gcn           | 0.967 ± 0.014 | 0.961 ± 0.016 | 0.961 ± 0.017 | 0.958 ± 0.016 |
| gcn_drop      | 0.988 ± 0.004 | 0.986 ± 0.005 | 0.964 ± 0.013 | 0.959 ± 0.014 |
| gat           | 0.973 ± 0.016 | 0.968 ± 0.018 | 0.969 ± 0.015 | 0.963 ± 0.019 |
| nsd           | 0.972 ± 0.016 | 0.968 ± 0.016 | 0.967 ± 0.018 | 0.966 ± 0.015 |
| rascm         | 0.989 ± 0.006 | 0.988 ± 0.007 | 0.975 ± 0.018 | 0.974 ± 0.018 |


## E4 — recall: anomalies + communication failures

|               | targeted_10   | targeted_30   | topo_0        | topo_30       |
|:--------------|:--------------|:--------------|:--------------|:--------------|
| physics_naive | 0.830 ± 0.051 | 0.829 ± 0.048 | 0.858 ± 0.046 | 0.853 ± 0.050 |
| physics_aoi   | 0.935 ± 0.021 | 0.930 ± 0.021 | 0.950 ± 0.018 | 0.945 ± 0.018 |
| gcn           | 0.944 ± 0.031 | 0.941 ± 0.032 | 0.936 ± 0.023 | 0.937 ± 0.025 |
| gcn_drop      | 0.968 ± 0.008 | 0.964 ± 0.010 | 0.950 ± 0.014 | 0.947 ± 0.014 |
| gat           | 0.950 ± 0.034 | 0.947 ± 0.033 | 0.946 ± 0.035 | 0.946 ± 0.029 |
| nsd           | 0.953 ± 0.028 | 0.952 ± 0.025 | 0.948 ± 0.027 | 0.952 ± 0.021 |
| rascm         | 0.977 ± 0.015 | 0.975 ± 0.017 | 0.972 ± 0.025 | 0.969 ± 0.027 |


## E4 — PR-AUC by anomaly type

|               | type_sudden_0   | type_sudden_30   | type_drift_0   | type_drift_30   | type_spoof_0   | type_spoof_30   |
|:--------------|:----------------|:-----------------|:---------------|:----------------|:---------------|:----------------|
| physics_naive | 0.980 ± 0.006   | 0.919 ± 0.022    | 0.856 ± 0.014  | 0.836 ± 0.014   | 0.864 ± 0.017  | 0.843 ± 0.021   |
| physics_aoi   | 0.980 ± 0.006   | 0.977 ± 0.006    | 0.856 ± 0.014  | 0.853 ± 0.015   | 0.864 ± 0.017  | 0.862 ± 0.017   |
| gcn           | 0.996 ± 0.004   | 0.994 ± 0.004    | 0.953 ± 0.012  | 0.948 ± 0.011   | 0.938 ± 0.015  | 0.939 ± 0.008   |
| gcn_drop      | 0.998 ± 0.001   | 0.996 ± 0.002    | 0.962 ± 0.010  | 0.957 ± 0.012   | 0.943 ± 0.019  | 0.936 ± 0.018   |
| gat           | 0.995 ± 0.004   | 0.995 ± 0.003    | 0.959 ± 0.022  | 0.955 ± 0.020   | 0.944 ± 0.016  | 0.945 ± 0.015   |
| nsd           | 0.997 ± 0.002   | 0.995 ± 0.003    | 0.971 ± 0.015  | 0.967 ± 0.017   | 0.947 ± 0.043  | 0.948 ± 0.037   |
| rascm         | 0.998 ± 0.002   | 0.998 ± 0.002    | 0.981 ± 0.006  | 0.980 ± 0.005   | 0.967 ± 0.011  | 0.965 ± 0.012   |


## E4 — detection delay (median, s) by anomaly type

|               | type_sudden_0   | type_sudden_30   | type_drift_0   | type_drift_30   | type_spoof_0   | type_spoof_30   |
|:--------------|:----------------|:-----------------|:---------------|:----------------|:---------------|:----------------|
| physics_naive | 0.90 ± 0.28     | 1.05 ± 0.14      | 3.70 ± 0.71    | 3.85 ± 0.81     | 2.40 ± 0.28    | 2.40 ± 0.28     |
| physics_aoi   | 0.25 ± 0.31     | 0.45 ± 0.14      | 1.55 ± 0.34    | 1.55 ± 0.34     | 1.10 ± 0.28    | 1.30 ± 0.34     |
| gcn           | 0.20 ± 0.34     | 0.10 ± 0.28      | 2.10 ± 0.52    | 2.05 ± 0.34     | 1.50 ± 0.00    | 1.30 ± 0.34     |
| gcn_drop      | 0.00 ± 0.00     | 0.00 ± 0.00      | 1.90 ± 0.28    | 1.80 ± 0.34     | 1.20 ± 0.34    | 1.40 ± 0.28     |
| gat           | 0.00 ± 0.00     | 0.20 ± 0.34      | 1.70 ± 0.71    | 1.70 ± 0.71     | 1.30 ± 0.34    | 1.20 ± 0.34     |
| nsd           | 0.00 ± 0.00     | 0.10 ± 0.28      | 1.50 ± 0.76    | 1.50 ± 0.76     | 1.00 ± 0.44    | 1.00 ± 0.44     |
| rascm         | 0.00 ± 0.00     | 0.00 ± 0.00      | 0.60 ± 0.47    | 0.75 ± 0.54     | 0.50 ± 0.00    | 0.80 ± 0.34     |


## E4 — detection rate by anomaly type

|               | type_sudden_0   | type_sudden_30   | type_drift_0   | type_drift_30   | type_spoof_0   | type_spoof_30   |
|:--------------|:----------------|:-----------------|:---------------|:----------------|:---------------|:----------------|
| physics_naive | 1.00 ± 0.00     | 1.00 ± 0.00      | 1.00 ± 0.00    | 1.00 ± 0.00     | 1.00 ± 0.01    | 1.00 ± 0.01     |
| physics_aoi   | 1.00 ± 0.00     | 1.00 ± 0.00      | 1.00 ± 0.00    | 1.00 ± 0.00     | 1.00 ± 0.00    | 1.00 ± 0.00     |
| gcn           | 1.00 ± 0.00     | 1.00 ± 0.00      | 1.00 ± 0.00    | 1.00 ± 0.00     | 0.98 ± 0.01    | 0.98 ± 0.01     |
| gcn_drop      | 1.00 ± 0.00     | 1.00 ± 0.00      | 1.00 ± 0.00    | 1.00 ± 0.00     | 0.99 ± 0.01    | 1.00 ± 0.01     |
| gat           | 1.00 ± 0.00     | 1.00 ± 0.00      | 1.00 ± 0.01    | 1.00 ± 0.01     | 0.99 ± 0.02    | 0.99 ± 0.02     |
| nsd           | 1.00 ± 0.00     | 1.00 ± 0.00      | 1.00 ± 0.00    | 1.00 ± 0.00     | 1.00 ± 0.01    | 1.00 ± 0.01     |
| rascm         | 1.00 ± 0.00     | 1.00 ± 0.00      | 1.00 ± 0.00    | 1.00 ± 0.00     | 1.00 ± 0.00    | 1.00 ± 0.00     |


## E5 — generalisation (loss 30%): PR-AUC

|               | gen_ref       | gen_n5        | gen_n20       | gen_lissajous   | gen_grid      |
|:--------------|:--------------|:--------------|:--------------|:----------------|:--------------|
| physics_naive | 0.849 ± 0.034 | 0.774 ± 0.048 | 0.839 ± 0.028 | 0.867 ± 0.031   | 0.894 ± 0.035 |
| physics_aoi   | 0.873 ± 0.035 | 0.774 ± 0.048 | 0.886 ± 0.014 | 0.879 ± 0.029   | 0.903 ± 0.034 |
| gcn           | 0.954 ± 0.021 | 0.841 ± 0.052 | 0.960 ± 0.023 | 0.962 ± 0.013   | 0.971 ± 0.013 |
| gcn_drop      | 0.957 ± 0.021 | 0.832 ± 0.071 | 0.967 ± 0.014 | 0.962 ± 0.015   | 0.970 ± 0.015 |
| gat           | 0.961 ± 0.019 | 0.839 ± 0.040 | 0.966 ± 0.016 | 0.969 ± 0.009   | 0.971 ± 0.015 |
| nsd           | 0.972 ± 0.012 | 0.783 ± 0.083 | 0.974 ± 0.012 | 0.975 ± 0.013   | 0.978 ± 0.009 |
| rascm         | 0.971 ± 0.014 | 0.830 ± 0.053 | 0.981 ± 0.008 | 0.976 ± 0.010   | 0.975 ± 0.017 |


## E5 — generalisation (loss 30%): FPR

|               | gen_ref       | gen_n5        | gen_n20       | gen_lissajous   | gen_grid      |
|:--------------|:--------------|:--------------|:--------------|:----------------|:--------------|
| physics_naive | 0.056 ± 0.031 | 0.084 ± 0.044 | 0.028 ± 0.013 | 0.051 ± 0.032   | 0.058 ± 0.035 |
| physics_aoi   | 0.121 ± 0.050 | 0.167 ± 0.057 | 0.066 ± 0.030 | 0.123 ± 0.053   | 0.134 ± 0.054 |
| gcn           | 0.023 ± 0.012 | 0.046 ± 0.017 | 0.014 ± 0.005 | 0.025 ± 0.013   | 0.014 ± 0.009 |
| gcn_drop      | 0.032 ± 0.024 | 0.063 ± 0.036 | 0.012 ± 0.005 | 0.031 ± 0.021   | 0.020 ± 0.019 |
| gat           | 0.029 ± 0.022 | 0.065 ± 0.039 | 0.015 ± 0.007 | 0.032 ± 0.025   | 0.026 ± 0.023 |
| nsd           | 0.022 ± 0.015 | 0.058 ± 0.027 | 0.012 ± 0.007 | 0.021 ± 0.018   | 0.017 ± 0.015 |
| rascm         | 0.034 ± 0.019 | 0.070 ± 0.023 | 0.016 ± 0.007 | 0.031 ± 0.022   | 0.032 ± 0.022 |


## E6 — ablations, PR-AUC

|                   | iid_0         | iid_10        | iid_30        | iid_50        | burst_30      | burst_50      | nodeburst_30   | targeted_10   | targeted_30   | gen_n20       | gen_lissajous   |
|:------------------|:--------------|:--------------|:--------------|:--------------|:--------------|:--------------|:---------------|:--------------|:--------------|:--------------|:----------------|
| rascm             | 0.974 ± 0.019 | 0.975 ± 0.018 | 0.975 ± 0.018 | 0.975 ± 0.019 | 0.972 ± 0.020 | 0.967 ± 0.026 | 0.958 ± 0.022  | 0.989 ± 0.006 | 0.988 ± 0.007 | 0.981 ± 0.008 | 0.976 ± 0.010   |
| rascm_no_rel      | 0.966 ± 0.021 | 0.967 ± 0.020 | 0.965 ± 0.020 | 0.949 ± 0.025 | 0.941 ± 0.028 | 0.879 ± 0.041 | 0.914 ± 0.040  | 0.975 ± 0.010 | 0.971 ± 0.009 | 0.965 ± 0.024 | 0.963 ± 0.024   |
| rascm_no_weight   | 0.977 ± 0.012 | 0.977 ± 0.012 | 0.978 ± 0.010 | 0.975 ± 0.010 | 0.966 ± 0.017 | 0.946 ± 0.022 | 0.952 ± 0.023  | 0.986 ± 0.004 | 0.983 ± 0.009 | 0.977 ± 0.012 | 0.964 ± 0.052   |
| rascm_no_sheaf    | 0.967 ± 0.016 | 0.969 ± 0.016 | 0.970 ± 0.014 | 0.971 ± 0.012 | 0.964 ± 0.017 | 0.960 ± 0.018 | 0.948 ± 0.021  | 0.989 ± 0.006 | 0.988 ± 0.006 | 0.977 ± 0.011 | 0.976 ± 0.017   |
| rascm_no_temporal | 0.969 ± 0.016 | 0.968 ± 0.016 | 0.966 ± 0.017 | 0.961 ± 0.018 | 0.958 ± 0.019 | 0.948 ± 0.023 | 0.938 ± 0.024  | 0.980 ± 0.010 | 0.979 ± 0.010 | 0.975 ± 0.013 | 0.970 ± 0.010   |
| mpnn_e            | 0.967 ± 0.019 | 0.967 ± 0.019 | 0.967 ± 0.018 | 0.966 ± 0.017 | 0.952 ± 0.026 | 0.932 ± 0.033 | 0.950 ± 0.023  | 0.975 ± 0.017 | 0.972 ± 0.019 | 0.971 ± 0.015 | 0.964 ± 0.033   |


## E7 — parameters and training cost (mean over seeds)

| model             |   n_params |   train_s |   epochs |
|:------------------|-----------:|----------:|---------:|
| gat               |      17585 |      93.4 |     16.8 |
| gcn               |      17425 |      68.4 |     21.4 |
| gcn_drop          |      17425 |      51.8 |     19.2 |
| mpnn_e            |      16321 |     287.9 |     27.4 |
| nsd               |      17729 |     346   |     17   |
| physics_aoi       |          0 |       0   |      0   |
| physics_naive     |          0 |       0   |      0   |
| rascm             |      17571 |     582.7 |     20.2 |
| rascm_no_rel      |      17377 |     578.5 |     21.8 |
| rascm_no_sheaf    |      16515 |     355.9 |     24.8 |
| rascm_no_temporal |      11043 |     541.4 |     24.4 |
| rascm_no_weight   |      17377 |     470.6 |     20.2 |


## Hypothesis test — paired PR-AUC difference (RA-SCM − reference), key conditions

`supports_H1` = lower 95% CI bound > 0 **and** mean difference ≥ 0.02 (pre-registered decision rule). `best_conventional` = per-seed best of GCN/GAT/GCN-drop/NSD (conservative for the proposed model).


| condition    | model   | reference         | metric   |   mean_diff |   ci_low |   ci_high |   p_one_sided |   n_seeds | supports_H1   |
|:-------------|:--------|:------------------|:---------|------------:|---------:|----------:|--------------:|----------:|:--------------|
| iid_0        | rascm   | physics_naive     | pr_auc   |      0.0797 |   0.0508 |    0.1086 |        0.0008 |         5 | True          |
| iid_0        | rascm   | physics_aoi       | pr_auc   |      0.0797 |   0.0508 |    0.1086 |        0.0008 |         5 | True          |
| iid_0        | rascm   | gcn               | pr_auc   |      0.0137 |   0.0027 |    0.0247 |        0.013  |         5 | False         |
| iid_0        | rascm   | gat               | pr_auc   |      0.0055 |  -0.0092 |    0.0202 |        0.1781 |         5 | False         |
| iid_0        | rascm   | gcn_drop          | pr_auc   |      0.0089 |   0.0017 |    0.0162 |        0.0134 |         5 | False         |
| iid_0        | rascm   | nsd               | pr_auc   |      0.0062 |  -0.0128 |    0.0252 |        0.2088 |         5 | False         |
| iid_0        | rascm   | best_conventional | pr_auc   |      0.0017 |  -0.0105 |    0.0139 |        0.3597 |         5 | False         |
| iid_10       | rascm   | physics_naive     | pr_auc   |      0.0862 |   0.0572 |    0.1153 |        0.0006 |         5 | True          |
| iid_10       | rascm   | physics_aoi       | pr_auc   |      0.0816 |   0.0527 |    0.1106 |        0.0007 |         5 | True          |
| iid_10       | rascm   | gcn               | pr_auc   |      0.0145 |   0.0032 |    0.0258 |        0.0117 |         5 | False         |
| iid_10       | rascm   | gat               | pr_auc   |      0.008  |  -0.0047 |    0.0208 |        0.0771 |         5 | False         |
| iid_10       | rascm   | gcn_drop          | pr_auc   |      0.0112 |   0.0031 |    0.0193 |        0.0093 |         5 | False         |
| iid_10       | rascm   | nsd               | pr_auc   |      0.0072 |  -0.0103 |    0.0247 |        0.1579 |         5 | False         |
| iid_10       | rascm   | best_conventional | pr_auc   |      0.0032 |  -0.008  |    0.0144 |        0.234  |         5 | False         |
| iid_30       | rascm   | physics_naive     | pr_auc   |      0.1119 |   0.0783 |    0.1455 |        0.0004 |         5 | True          |
| iid_30       | rascm   | physics_aoi       | pr_auc   |      0.0838 |   0.0544 |    0.1132 |        0.0007 |         5 | True          |
| iid_30       | rascm   | gcn               | pr_auc   |      0.0172 |   0.0078 |    0.0267 |        0.0036 |         5 | False         |
| iid_30       | rascm   | gat               | pr_auc   |      0.0116 |  -0.001  |    0.0243 |        0.0317 |         5 | False         |
| iid_30       | rascm   | gcn_drop          | pr_auc   |      0.0162 |   0.0084 |    0.0239 |        0.0022 |         5 | False         |
| iid_30       | rascm   | nsd               | pr_auc   |      0.0077 |  -0.0091 |    0.0246 |        0.1352 |         5 | False         |
| iid_30       | rascm   | best_conventional | pr_auc   |      0.0051 |  -0.0063 |    0.0164 |        0.1409 |         5 | False         |
| iid_50       | rascm   | physics_naive     | pr_auc   |      0.171  |   0.134  |    0.208  |        0.0001 |         5 | True          |
| iid_50       | rascm   | physics_aoi       | pr_auc   |      0.087  |   0.0551 |    0.1188 |        0.0008 |         5 | True          |
| iid_50       | rascm   | gcn               | pr_auc   |      0.0233 |   0.0104 |    0.0363 |        0.0038 |         5 | True          |
| iid_50       | rascm   | gat               | pr_auc   |      0.0187 |   0.0038 |    0.0336 |        0.0126 |         5 | False         |
| iid_50       | rascm   | gcn_drop          | pr_auc   |      0.0253 |   0.0157 |    0.035  |        0.001  |         5 | True          |
| iid_50       | rascm   | nsd               | pr_auc   |      0.0157 |  -0.005  |    0.0363 |        0.0512 |         5 | False         |
| iid_50       | rascm   | best_conventional | pr_auc   |      0.0126 |  -0.0041 |    0.0294 |        0.0523 |         5 | False         |
| burst_30     | rascm   | physics_naive     | pr_auc   |      0.3675 |   0.3071 |    0.4279 |        0      |         5 | True          |
| burst_30     | rascm   | physics_aoi       | pr_auc   |      0.0874 |   0.0561 |    0.1187 |        0.0007 |         5 | True          |
| burst_30     | rascm   | gcn               | pr_auc   |      0.0537 |   0.0329 |    0.0746 |        0.001  |         5 | True          |
| burst_30     | rascm   | gat               | pr_auc   |      0.0435 |   0.0164 |    0.0707 |        0.0056 |         5 | True          |
| burst_30     | rascm   | gcn_drop          | pr_auc   |      0.0197 |   0.0117 |    0.0278 |        0.0012 |         5 | False         |
| burst_30     | rascm   | nsd               | pr_auc   |      0.0351 |   0.015  |    0.0552 |        0.0042 |         5 | True          |
| burst_30     | rascm   | best_conventional | pr_auc   |      0.019  |   0.0115 |    0.0265 |        0.0011 |         5 | False         |
| burst_50     | rascm   | physics_naive     | pr_auc   |      0.4476 |   0.3935 |    0.5017 |        0      |         5 | True          |
| burst_50     | rascm   | physics_aoi       | pr_auc   |      0.09   |   0.0589 |    0.1212 |        0.0007 |         5 | True          |
| burst_50     | rascm   | gcn               | pr_auc   |      0.0782 |   0.0491 |    0.1073 |        0.0009 |         5 | True          |
| burst_50     | rascm   | gat               | pr_auc   |      0.0575 |   0.03   |    0.085  |        0.0022 |         5 | True          |
| burst_50     | rascm   | gcn_drop          | pr_auc   |      0.0281 |   0.0131 |    0.0431 |        0.0032 |         5 | True          |
| burst_50     | rascm   | nsd               | pr_auc   |      0.0602 |   0.028  |    0.0925 |        0.0033 |         5 | True          |
| burst_50     | rascm   | best_conventional | pr_auc   |      0.0281 |   0.0131 |    0.0431 |        0.0032 |         5 | True          |
| nodeburst_30 | rascm   | physics_naive     | pr_auc   |      0.5691 |   0.539  |    0.5991 |        0      |         5 | True          |
| nodeburst_30 | rascm   | physics_aoi       | pr_auc   |      0.0731 |   0.045  |    0.1012 |        0.001  |         5 | True          |
| nodeburst_30 | rascm   | gcn               | pr_auc   |      0.0284 |   0.0141 |    0.0427 |        0.0026 |         5 | True          |
| nodeburst_30 | rascm   | gat               | pr_auc   |      0.0146 |   0.0033 |    0.0259 |        0.0115 |         5 | False         |
| nodeburst_30 | rascm   | gcn_drop          | pr_auc   |      0.0509 |   0.0409 |    0.061  |        0.0001 |         5 | True          |
| nodeburst_30 | rascm   | nsd               | pr_auc   |      0.0096 |  -0.0115 |    0.0306 |        0.1373 |         5 | False         |
| nodeburst_30 | rascm   | best_conventional | pr_auc   |      0.0072 |  -0.0077 |    0.022  |        0.1264 |         5 | False         |
| targeted_10  | rascm   | physics_naive     | pr_auc   |      0.1685 |   0.1343 |    0.2028 |        0.0001 |         5 | True          |
| targeted_10  | rascm   | physics_aoi       | pr_auc   |      0.0981 |   0.0736 |    0.1226 |        0.0002 |         5 | True          |
| targeted_10  | rascm   | gcn               | pr_auc   |      0.0216 |   0.0132 |    0.0299 |        0.001  |         5 | True          |
| targeted_10  | rascm   | gat               | pr_auc   |      0.0152 |   0.0052 |    0.0253 |        0.0068 |         5 | False         |
| targeted_10  | rascm   | gcn_drop          | pr_auc   |      0.0005 |  -0.0043 |    0.0053 |        0.3904 |         5 | False         |
| targeted_10  | rascm   | nsd               | pr_auc   |      0.0164 |   0.0035 |    0.0294 |        0.012  |         5 | False         |
| targeted_10  | rascm   | best_conventional | pr_auc   |      0.0005 |  -0.0043 |    0.0053 |        0.3905 |         5 | False         |
| targeted_30  | rascm   | physics_naive     | pr_auc   |      0.209  |   0.1719 |    0.2461 |        0      |         5 | True          |
| targeted_30  | rascm   | physics_aoi       | pr_auc   |      0.098  |   0.0754 |    0.1206 |        0.0001 |         5 | True          |
| targeted_30  | rascm   | gcn               | pr_auc   |      0.0271 |   0.0173 |    0.0369 |        0.0008 |         5 | True          |
| targeted_30  | rascm   | gat               | pr_auc   |      0.0199 |   0.0074 |    0.0324 |        0.0057 |         5 | False         |
| targeted_30  | rascm   | gcn_drop          | pr_auc   |      0.0019 |  -0.0018 |    0.0057 |        0.1113 |         5 | False         |
| targeted_30  | rascm   | nsd               | pr_auc   |      0.0201 |   0.0067 |    0.0335 |        0.007  |         5 | True          |
| targeted_30  | rascm   | best_conventional | pr_auc   |      0.0019 |  -0.0018 |    0.0057 |        0.1113 |         5 | False         |


### Summary over all conditions vs best conventional GNN

conditions where H1 supported: 1 / 26; conditions where the CI excludes 0 in favour of the baseline (mean diff < 0, CI high < 0): 0 / 26


### Pre-specified decision (set C* = iid_30, iid_50, burst_30, burst_50, nodeburst_30, targeted_30)

* H1 supported in 1 / 6 conditions vs the best conventional GNN (needs >= 4).
* conditions where the CI of the difference vs best conventional GNN contains 0 or is negative: 4 (falsification if >= 3).
* conditions where RA-SCM is not better than the AoI-aware physics baseline (mean diff <= 0): 0 / 6 (falsification if it is at least as good on C*, i.e. a majority).
* FPR at iid 50% loss: RA-SCM 0.031 vs lowest conventional GNN 0.029 (needs RA-SCM <= conventional + 0.02).


## Ablation — paired PR-AUC difference (full RA-SCM − ablation), key conditions

Positive = the removed component helped. 

| condition    | model   | reference         | metric   |   mean_diff |   ci_low |   ci_high |   p_one_sided |   n_seeds | supports_H1   |
|:-------------|:--------|:------------------|:---------|------------:|---------:|----------:|--------------:|----------:|:--------------|
| iid_0        | rascm   | rascm_no_rel      | pr_auc   |      0.008  |  -0.0026 |    0.0186 |        0.0524 |         5 | False         |
| iid_0        | rascm   | rascm_no_weight   | pr_auc   |     -0.0029 |  -0.0174 |    0.0117 |        0.6933 |         5 | False         |
| iid_0        | rascm   | rascm_no_sheaf    | pr_auc   |      0.0071 |  -0.0081 |    0.0223 |        0.1328 |         5 | False         |
| iid_0        | rascm   | rascm_no_temporal | pr_auc   |      0.005  |  -0.0023 |    0.0122 |        0.0652 |         5 | False         |
| iid_0        | rascm   | mpnn_e            | pr_auc   |      0.0074 |  -0.0078 |    0.0226 |        0.1236 |         5 | False         |
| iid_10       | rascm   | rascm_no_rel      | pr_auc   |      0.0087 |  -0.0031 |    0.0204 |        0.0553 |         5 | False         |
| iid_10       | rascm   | rascm_no_weight   | pr_auc   |     -0.0021 |  -0.0172 |    0.0131 |        0.6395 |         5 | False         |
| iid_10       | rascm   | rascm_no_sheaf    | pr_auc   |      0.0065 |  -0.009  |    0.022  |        0.1546 |         5 | False         |
| iid_10       | rascm   | rascm_no_temporal | pr_auc   |      0.0068 |  -0.0017 |    0.0153 |        0.0455 |         5 | False         |
| iid_10       | rascm   | mpnn_e            | pr_auc   |      0.0082 |  -0.0067 |    0.0232 |        0.1004 |         5 | False         |
| iid_30       | rascm   | rascm_no_rel      | pr_auc   |      0.0104 |  -0.0011 |    0.0218 |        0.033  |         5 | False         |
| iid_30       | rascm   | rascm_no_weight   | pr_auc   |     -0.0032 |  -0.0185 |    0.0121 |        0.7016 |         5 | False         |
| iid_30       | rascm   | rascm_no_sheaf    | pr_auc   |      0.0048 |  -0.0093 |    0.0189 |        0.1973 |         5 | False         |
| iid_30       | rascm   | rascm_no_temporal | pr_auc   |      0.009  |  -0.0007 |    0.0187 |        0.0306 |         5 | False         |
| iid_30       | rascm   | mpnn_e            | pr_auc   |      0.008  |  -0.008  |    0.024  |        0.1176 |         5 | False         |
| iid_50       | rascm   | rascm_no_rel      | pr_auc   |      0.0257 |   0.0092 |    0.0422 |        0.0063 |         5 | True          |
| iid_50       | rascm   | rascm_no_weight   | pr_auc   |     -0.0005 |  -0.0142 |    0.0133 |        0.535  |         5 | False         |
| iid_50       | rascm   | rascm_no_sheaf    | pr_auc   |      0.0041 |  -0.0091 |    0.0173 |        0.2191 |         5 | False         |
| iid_50       | rascm   | rascm_no_temporal | pr_auc   |      0.0134 |  -0.0002 |    0.027  |        0.0262 |         5 | False         |
| iid_50       | rascm   | mpnn_e            | pr_auc   |      0.0087 |  -0.004  |    0.0214 |        0.0658 |         5 | False         |
| burst_30     | rascm   | rascm_no_rel      | pr_auc   |      0.0311 |   0.0132 |    0.0491 |        0.0043 |         5 | True          |
| burst_30     | rascm   | rascm_no_weight   | pr_auc   |      0.0065 |  -0.0107 |    0.0237 |        0.177  |         5 | False         |
| burst_30     | rascm   | rascm_no_sheaf    | pr_auc   |      0.008  |  -0.0116 |    0.0275 |        0.1612 |         5 | False         |
| burst_30     | rascm   | rascm_no_temporal | pr_auc   |      0.014  |   0.0012 |    0.0268 |        0.0194 |         5 | False         |
| burst_30     | rascm   | mpnn_e            | pr_auc   |      0.0207 |   0.004  |    0.0375 |        0.0133 |         5 | True          |
| burst_50     | rascm   | rascm_no_rel      | pr_auc   |      0.0879 |   0.051  |    0.1248 |        0.0014 |         5 | True          |
| burst_50     | rascm   | rascm_no_weight   | pr_auc   |      0.0211 |   0.0044 |    0.0378 |        0.0124 |         5 | True          |
| burst_50     | rascm   | rascm_no_sheaf    | pr_auc   |      0.0066 |  -0.01   |    0.0232 |        0.1663 |         5 | False         |
| burst_50     | rascm   | rascm_no_temporal | pr_auc   |      0.0185 |   0.0024 |    0.0346 |        0.0167 |         5 | False         |
| burst_50     | rascm   | mpnn_e            | pr_auc   |      0.035  |   0.0176 |    0.0524 |        0.0025 |         5 | True          |
| nodeburst_30 | rascm   | rascm_no_rel      | pr_auc   |      0.0443 |   0.0207 |    0.0678 |        0.0032 |         5 | True          |
| nodeburst_30 | rascm   | rascm_no_weight   | pr_auc   |      0.0062 |  -0.0092 |    0.0215 |        0.163  |         5 | False         |
| nodeburst_30 | rascm   | rascm_no_sheaf    | pr_auc   |      0.0097 |  -0.0052 |    0.0245 |        0.0723 |         5 | False         |
| nodeburst_30 | rascm   | rascm_no_temporal | pr_auc   |      0.0203 |   0.0114 |    0.0292 |        0.0016 |         5 | True          |
| nodeburst_30 | rascm   | mpnn_e            | pr_auc   |      0.0073 |  -0.012  |    0.0267 |        0.1758 |         5 | False         |
| targeted_10  | rascm   | rascm_no_rel      | pr_auc   |      0.0139 |   0.0068 |    0.021  |        0.0028 |         5 | False         |
| targeted_10  | rascm   | rascm_no_weight   | pr_auc   |      0.0024 |  -0.0017 |    0.0065 |        0.0889 |         5 | False         |
| targeted_10  | rascm   | rascm_no_sheaf    | pr_auc   |     -0.0002 |  -0.0036 |    0.0031 |        0.5718 |         5 | False         |
| targeted_10  | rascm   | rascm_no_temporal | pr_auc   |      0.0085 |   0.0014 |    0.0156 |        0.0146 |         5 | False         |
| targeted_10  | rascm   | mpnn_e            | pr_auc   |      0.014  |   0.0003 |    0.0278 |        0.0237 |         5 | False         |
| targeted_30  | rascm   | rascm_no_rel      | pr_auc   |      0.0173 |   0.0109 |    0.0237 |        0.0009 |         5 | False         |
| targeted_30  | rascm   | rascm_no_weight   | pr_auc   |      0.0045 |  -0.0015 |    0.0106 |        0.0526 |         5 | False         |
| targeted_30  | rascm   | rascm_no_sheaf    | pr_auc   |     -0.0003 |  -0.0038 |    0.0033 |        0.5767 |         5 | False         |
| targeted_30  | rascm   | rascm_no_temporal | pr_auc   |      0.0092 |   0.0024 |    0.016  |        0.0101 |         5 | False         |
| targeted_30  | rascm   | mpnn_e            | pr_auc   |      0.0155 |  -0.0003 |    0.0313 |        0.0266 |         5 | False         |


## E7 — inference latency (CPU, batch 1)

| model             |   n_uavs |   n_params |   ms_per_episode |   ms_per_step |   rss_delta_mb |
|:------------------|---------:|-----------:|-----------------:|--------------:|---------------:|
| physics_naive     |        5 |          0 |            2.071 |         0.021 |          0     |
| physics_aoi       |        5 |          0 |            2.083 |         0.021 |          0     |
| gcn               |        5 |      17425 |            1.889 |         0.019 |          0     |
| gat               |        5 |      17585 |            2.312 |         0.023 |          0     |
| gcn_drop          |        5 |      17425 |            1.998 |         0.02  |          0     |
| nsd               |        5 |      17729 |            5.361 |         0.054 |          0     |
| rascm             |        5 |      17571 |            5.43  |         0.054 |          0     |
| rascm_no_rel      |        5 |      17377 |            5.149 |         0.051 |          0     |
| rascm_no_weight   |        5 |      17377 |            5.132 |         0.051 |          0     |
| rascm_no_sheaf    |        5 |      16515 |            4.204 |         0.042 |          0     |
| rascm_no_temporal |        5 |      11043 |            4.243 |         0.042 |          0     |
| mpnn_e            |        5 |      16321 |            3.967 |         0.04  |          0     |
| physics_naive     |       10 |          0 |            2.193 |         0.022 |          0     |
| physics_aoi       |       10 |          0 |            2.181 |         0.022 |          0     |
| gcn               |       10 |      17425 |            3.384 |         0.034 |          0     |
| gat               |       10 |      17585 |            4.775 |         0.048 |          0     |
| gcn_drop          |       10 |      17425 |            3.393 |         0.034 |          0     |
| nsd               |       10 |      17729 |           17.59  |         0.176 |          0     |
| rascm             |       10 |      17571 |           18.096 |         0.181 |          0     |
| rascm_no_rel      |       10 |      17377 |           17.069 |         0.171 |          0     |
| rascm_no_weight   |       10 |      17377 |           17.238 |         0.172 |          0     |
| rascm_no_sheaf    |       10 |      16515 |           12.583 |         0.126 |          9.375 |
| rascm_no_temporal |       10 |      11043 |           16.563 |         0.166 |         22.75  |
| mpnn_e            |       10 |      16321 |           11.534 |         0.115 |          0     |
| physics_naive     |       20 |          0 |            2.346 |         0.023 |          0     |
| physics_aoi       |       20 |          0 |            2.381 |         0.024 |          0     |
| gcn               |       20 |      17425 |            8.499 |         0.085 |          0     |
| gat               |       20 |      17585 |           13.967 |         0.14  |          0     |
| gcn_drop          |       20 |      17425 |            8.29  |         0.083 |          0     |
| nsd               |       20 |      17729 |           71.367 |         0.714 |         23.203 |
| rascm             |       20 |      17571 |           76.046 |         0.76  |         27.078 |
| rascm_no_rel      |       20 |      17377 |           71.632 |         0.716 |          0     |
| rascm_no_weight   |       20 |      17377 |           71.441 |         0.714 |          9.828 |
| rascm_no_sheaf    |       20 |      16515 |           52.09  |         0.521 |          0.016 |
| rascm_no_temporal |       20 |      11043 |           75.292 |         0.753 |          2.5   |
| mpnn_e            |       20 |      16321 |           46.742 |         0.467 |          0     |
