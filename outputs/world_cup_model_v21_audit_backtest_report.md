# World Cup Model v2.1 Audit + Backtest

This package audits the sensitive 2026 rankings and runs a v2.1-style historical backtest on 2018 and 2022.

## Sensitive Ranking Audit

| Team | Title rank | Champion % | Group 1st % | Power | Main note |
|---|---:|---:|---:|---:|---|
| Germany | 6 | 6.09% | 55.83% | 79.877 | Higher recent-form/tactical score plus clean Group E winner path. |
| Colombia | 7 | 5.68% | 50.64% | 78.207 | Same group as Portugal but higher power and better group-winner probability. |
| Japan | 8 | 3.61% | 52.07% | 77.402 | Slightly ahead of Netherlands mostly through recent form and Group F winner path. |
| Portugal | 9 | 3.43% | 41.12% | 75.505 | Strong squad, but low recent-form/manager-tactical layers and Group K path pressure. |
| Netherlands | 12 | 2.41% | 44.74% | 75.386 | Strong squad/Elo, but low recent form and second-place risk behind Japan; 2F can meet 1C early. |

## Historical Backtest Metrics

| Year | Brier | Log loss | Favorite accuracy | Matches |
|---:|---:|---:|---:|---:|
| 2018 | 0.1766 | 0.9066 | 58.33% | 48 |
| 2022 | 0.2195 | 1.1356 | 45.83% | 48 |

## Champion Test

| Year | Champion | Rank | Champion probability |
|---:|---|---:|---:|
| 2018 | France | 5 | 7.1% |
| 2022 | Argentina | 3 | 16.66% |

## Honest Interpretation

- The backtest uses historical public squad metadata, not the 2026 player table.
- Manager scores are neutral historical proxies, not hand-rated historical manager data.
- Club level is still a heuristic, so this tests the architecture more than a final commercial-grade data feed.
- If v2.1 proxy does not clearly beat v1 on every metric, that is useful: it tells us which layers need real minutes/role data before production.
