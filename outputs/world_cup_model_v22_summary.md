# World Cup Model v2.2

V2.2 keeps the Player Impact Rating v2.1 team layer and recalibrates the 90-minute 1/X/2 engine.

## What changed

- Base goal rate lowered from 1.18 to 1.15.
- Power-to-goal scale widened from 43 to 62.0, reducing overconfident side separation.
- Draw risk is now a first-class match state instead of being buried under side picks.
- Public draw language is conservative: most draw calls are framed as draw risk/no strong edge, not certainty.

## Draw Output

- 90-minute model draw picks in group stage: 14.
- Public draw leans: 3.
- Draw-risk/no-edge calls: 11.

## Top Title Odds

| Rank | Team | Champion % | Final % | Semi % |
|---:|---|---:|---:|---:|
| 1 | France | 14.47% | 22.67% | 34.38% |
| 2 | Argentina | 11.89% | 20.01% | 32.97% |
| 3 | Spain | 11.59% | 19.65% | 33.08% |
| 4 | Brazil | 8.15% | 14.51% | 24.54% |
| 5 | England | 6.71% | 12.75% | 22.93% |
| 6 | Germany | 6.14% | 12.03% | 21.29% |
| 7 | Colombia | 5.66% | 11.41% | 22.28% |
| 8 | Japan | 4.2% | 8.68% | 16.75% |
| 9 | Portugal | 3.84% | 8.39% | 17.63% |
| 10 | Morocco | 3.42% | 7.5% | 14.82% |
| 11 | Turkey | 3.2% | 7.19% | 16.09% |
| 12 | Netherlands | 3.06% | 6.93% | 14.1% |

## Biggest Changes vs v2.1

| Team | v2.1 % | v2.2 % | Change |
|---|---:|---:|---:|
| France | 18.25% | 14.47% | -3.78 |
| Argentina | 13.98% | 11.89% | -2.09 |
| Spain | 13.54% | 11.59% | -1.95 |
| Ecuador | 2.15% | 2.96% | 0.81 |
| Brazil | 8.95% | 8.15% | -0.8 |
| Mexico | 2.19% | 2.89% | 0.7 |
| Netherlands | 2.41% | 3.06% | 0.65 |
| Norway | 1.27% | 1.9% | 0.63 |
| Japan | 3.61% | 4.2% | 0.59 |
| Morocco | 2.89% | 3.42% | 0.53 |

## Honest Caveat

This fixes the no-draw behavior in the public match layer, but it does not magically make exact draw calls easy. The backtest shows draw-aware calibration improves probability quality while hard draw picks remain difficult.
