# World Cup Model v1 Backtest

Backtest tournaments: 2018 and 2022.

The test is leak-free for team strength: ratings/form are taken only from matches before each tournament start date. Tactical priors are only used when historical StatsBomb World Cup data existed before that tournament; 2018 has no open tactical prior, 2022 can use 2018.

## Group Match Metrics

| Year | Variant | Brier | Log Loss | Favorite Accuracy | Win Picks | Win Pick Accuracy | Avoid Picks | Avoid Accuracy | Passes |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | model_v1 | 0.1849 | 0.9415 | 58.33% | 24 | 70.83% | 9 | 55.56% | 0 |
| 2018 | elo_only | 0.1889 | 0.9585 | 56.25% | 21 | 71.43% | 8 | 75.0% | 0 |
| 2022 | model_v1 | 0.2096 | 1.0685 | 47.92% | 26 | 57.69% | 5 | 80.0% | 0 |
| 2022 | elo_only | 0.2091 | 1.058 | 52.08% | 22 | 54.55% | 7 | 71.43% | 0 |

## Champion Backtest

| Year | Variant | Champion | Rank | Probability | Top 5? | Top 10? |
|---:|---|---|---:|---:|---|---|
| 2018 | elo_only | France | 5 | 6.25% | True | True |
| 2018 | model_v1 | France | 5 | 5.9% | True | True |
| 2022 | elo_only | Argentina | 2 | 20.29% | True | True |
| 2022 | model_v1 | Argentina | 2 | 21.48% | True | True |

## Top 5 Title Odds By Tournament

### 2018 model_v1

| Rank | Team | Champion % | Final % | Semi % |
|---:|---|---:|---:|---:|
| 1 | Brazil | 28.73% | 40.53% | 55.23% |
| 2 | Spain | 14.05% | 24.61% | 41.63% |
| 3 | Germany | 11.48% | 21.66% | 35.67% |
| 4 | Argentina | 6.64% | 13.87% | 27.5% |
| 5 | France | 5.9% | 12.3% | 25.37% |

### 2018 elo_only

| Rank | Team | Champion % | Final % | Semi % |
|---:|---|---:|---:|---:|
| 1 | Brazil | 23.88% | 34.48% | 48.57% |
| 2 | Spain | 12.77% | 21.44% | 37.24% |
| 3 | Germany | 12.11% | 21.21% | 34.1% |
| 4 | Argentina | 7.09% | 13.89% | 26.64% |
| 5 | France | 6.25% | 12.5% | 24.18% |

### 2022 model_v1

| Rank | Team | Champion % | Final % | Semi % |
|---:|---|---:|---:|---:|
| 1 | Brazil | 27.72% | 37.85% | 54.27% |
| 2 | Argentina | 21.48% | 32.14% | 52.76% |
| 3 | Netherlands | 9.7% | 18.37% | 35.02% |
| 4 | Spain | 8.77% | 16.02% | 27.31% |
| 5 | Belgium | 5.14% | 11.84% | 20.86% |

### 2022 elo_only

| Rank | Team | Champion % | Final % | Semi % |
|---:|---|---:|---:|---:|
| 1 | Brazil | 24.12% | 34.44% | 49.91% |
| 2 | Argentina | 20.29% | 30.58% | 49.33% |
| 3 | Spain | 7.37% | 13.94% | 24.16% |
| 4 | Netherlands | 7.22% | 14.37% | 27.89% |
| 5 | Belgium | 6.29% | 12.6% | 22.0% |

## Read

The useful question is not whether the model picked the exact champion. The useful questions are whether the champion was among serious contenders, whether probabilities were calibrated, whether group qualification odds were sane, and whether the layered model improves on Elo-only.

## Interpretation

- The model passed the broad contender test: France 2018 and Argentina 2022 were both top-5 title teams before the tournament.
- The layered model improved 2018 group-stage Brier/log-loss versus Elo-only, but did not improve 2022. That means the v1 weights are not yet reliable enough.
- The selected win-pick layer is promising: 70.83% in 2018 and 57.69% in 2022, for 64.0% combined across 50 selected win picks.
- The model currently passes on zero matches. That is a product problem. We need stricter no-edge/pass thresholds.
- Brazil is too dominant in both historical pre-tournament simulations. The championship ceiling and/or rating-to-goal scale likely needs calibration.

## Next Calibration Tasks

1. Tune the rating-to-probability scale so top teams do not receive exaggerated title odds.
2. Rework the public verdict thresholds so close matches can become real passes.
3. Tune recent-form and ceiling weights against 2014/2018/2022 if we can add 2014 fixtures/groups.
4. Evaluate selected-pick accuracy at different confidence thresholds, not just all favorite calls.
5. Add squad-quality data before expecting the model to spot injury-driven changes.
