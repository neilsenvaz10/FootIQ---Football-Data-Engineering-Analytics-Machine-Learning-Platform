# World Cup Model v2.3 Backtest

V2.3 tests the manager-weight reduction, neutral historical market layer, and explicit extra-time/penalty knockout randomness.

## Match Metrics

| Year | Brier | Log loss | Pick accuracy | Draw picks | Draw pick accuracy | Actual draws |
|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 0.1797 | 0.9204 | 47.92% | 9 | 0.0% | 9 |
| 2022 | 0.2111 | 1.0655 | 43.75% | 11 | 18.18% | 10 |

## v2.2 vs v2.3

| Year | Metric | v2.2 | v2.3 | Delta |
|---:|---|---:|---:|---:|
| 2018 | group_match_brier | 0.1785 | 0.1797 | 0.0012 |
| 2018 | group_match_log_loss | 0.9153 | 0.9204 | 0.0051 |
| 2018 | pick_accuracy_pct | 47.92 | 47.92 | 0.0 |
| 2022 | group_match_brier | 0.2117 | 0.2111 | -0.0006 |
| 2022 | group_match_log_loss | 1.0738 | 1.0655 | -0.0083 |
| 2022 | pick_accuracy_pct | 45.83 | 43.75 | -2.08 |

## Champion Test

| Year | Champion | Rank | Champion probability |
|---:|---|---:|---:|
| 2018 | France | 8 | 6.63% |
| 2022 | Argentina | 3 | 12.61% |

## Honest Interpretation

- Historical market score is neutral for every team, so this does not test the 2026 market-sanity layer.
- The test is mainly about whether the v2.3 reweighting and randomness module preserve or improve calibration.
- Any v2.3 gains/losses should be treated as directional until we add broader historical tournaments and proper historical manager/lineup feeds.
