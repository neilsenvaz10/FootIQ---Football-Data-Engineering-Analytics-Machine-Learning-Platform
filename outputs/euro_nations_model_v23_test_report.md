# Euro 2024 + UEFA Nations League v2.3-lite Test

This test uses the v2.3 model shape without 2026 player, manager, or market leakage.

## Method

- Team strength is built from pre-event Elo, recent form, tactical prior where available, proxy squad score, neutral manager score, neutral market score, and neutral availability.
- Euro 2024 uses the official 24-team group format, best-third qualification matrix, and knockout bracket.
- UEFA Nations League uses the four-team 2025 finals bracket: Germany vs Portugal and Spain vs France, then final.
- Exact score is not a product prediction; score sampling is used internally for tournament simulation.

## Euro 2024

- 90-minute match Brier: 0.216
- 90-minute log loss: 1.0748
- 90-minute pick accuracy: 52.78%
- Draw picks: 22 / actual draws: 14

| Rank | Team | Champion % | Final % | Power |
|---:|---|---:|---:|---:|
| 1 | Germany | 9.09% | 15.96% | 84.671 |
| 2 | Spain | 7.75% | 14.04% | 85.442 |
| 3 | Belgium | 7.27% | 13.43% | 84.88 |
| 4 | Netherlands | 7.04% | 12.79% | 84.202 |
| 5 | Croatia | 6.35% | 12.12% | 83.589 |
| 6 | Austria | 6.21% | 11.51% | 83.624 |
| 7 | Portugal | 5.32% | 10.13% | 81.889 |
| 8 | France | 5.22% | 10.32% | 82.188 |

## UEFA Nations League 2025 Finals

- 90-minute match Brier: 0.2289
- 90-minute log loss: 1.1278
- 90-minute pick accuracy: 33.33%
- Draw picks: 3 / actual draws: 1

| Rank | Team | Champion % | Final % | Power |
|---:|---|---:|---:|---:|
| 1 | Germany | 29.52% | 55.07% | 86.06 |
| 2 | Spain | 26.34% | 52.38% | 85.562 |
| 3 | France | 22.09% | 47.62% | 83.625 |
| 4 | Portugal | 22.07% | 44.93% | 83.625 |

## Honest Read

- This is a better architecture test than the 2018/2022 World Cup backtest because Euro 2024 and Nations League are closer to the current player era.
- It is still v2.3-lite, not full v2.3, because historical verified player-impact and market feeds are not attached yet.
- The output should be read as a contender-pool and calibration test, not proof the model can nail exact champions.
