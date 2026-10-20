# World Cup Model v2.2 Backtest

V2.2 tests a draw-calibrated 90-minute probability layer while keeping the v2.1 historical team-power layer fixed.

## Match Metrics

| Year | Brier | Log loss | Pick accuracy | Draw picks | Draw pick accuracy | Actual draws |
|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 0.1785 | 0.9153 | 47.92% | 9 | 0.0% | 9 |
| 2022 | 0.2117 | 1.0738 | 45.83% | 9 | 22.22% | 10 |

## v2.1 vs v2.2

| Year | Metric | v2.1 | v2.2 | Delta |
|---:|---|---:|---:|---:|
| 2018 | group_match_brier | 0.1766 | 0.1785 | 0.0019 |
| 2018 | group_match_log_loss | 0.9066 | 0.9153 | 0.0087 |
| 2018 | pick_accuracy_pct | 58.33 | 47.92 | -10.41 |
| 2022 | group_match_brier | 0.2195 | 0.2117 | -0.0078 |
| 2022 | group_match_log_loss | 1.1356 | 1.0738 | -0.0618 |
| 2022 | pick_accuracy_pct | 45.83 | 45.83 | 0.0 |

## Champion Test

| Year | Champion | Rank | Champion probability |
|---:|---|---:|---:|
| 2018 | France | 5 | 7.13% |
| 2022 | Argentina | 3 | 16.23% |

## Honest Interpretation

- v2.2 improves probability calibration versus v2.1 on the combined 2018/2022 group-stage test.
- Exact draw picks remain low precision, so public product language should usually say draw risk/no strong edge rather than sell a draw as a confident pick.
- This version fixes the zero-draw structural bug without changing the player-impact/team-strength layer.
