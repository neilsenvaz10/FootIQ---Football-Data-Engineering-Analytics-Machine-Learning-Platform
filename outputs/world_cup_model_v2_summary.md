# World Cup Model v2

V2 reduces Elo dominance by converting every feature layer into a 0-100 score before combining them.

## Weighting

| Layer | Weight |
|---|---:|
| elo_score | 30% |
| squad_score | 25% |
| manager_score | 15% |
| recent_form_score | 10% |
| tactical_score | 10% |
| ceiling_score | 5% |
| availability_score | 5% |

## Top Title Odds

| Rank | Team | Champion % | Final % | Semi % |
|---:|---|---:|---:|---:|
| 1 | France | 21.21% | 31.98% | 46.13% |
| 2 | Argentina | 15.06% | 25.74% | 41.8% |
| 3 | Spain | 12.95% | 22.98% | 40.25% |
| 4 | Brazil | 9.89% | 17.58% | 28.94% |
| 5 | England | 8.2% | 16.15% | 29.56% |
| 6 | Colombia | 5.8% | 12.82% | 26.89% |
| 7 | Germany | 5.58% | 11.6% | 21.37% |
| 8 | Portugal | 3.82% | 9.41% | 22.12% |
| 9 | Japan | 2.88% | 6.94% | 14.59% |
| 10 | Morocco | 2.34% | 5.91% | 13.11% |
| 11 | Netherlands | 2.08% | 5.33% | 11.96% |
| 12 | Belgium | 1.9% | 5.72% | 16.1% |

## Biggest Changes vs v1

| Team | V1 % | V2 % | Change |
|---|---:|---:|---:|
| Spain | 22.98% | 12.95% | -10.03 |
| France | 13.41% | 21.21% | 7.8 |
| Brazil | 5.21% | 9.89% | 4.68 |
| Germany | 2.87% | 5.58% | 2.71 |
| Argentina | 17.39% | 15.06% | -2.33 |
| England | 6.47% | 8.2% | 1.73 |
| Colombia | 4.83% | 5.8% | 0.97 |
| Netherlands | 2.98% | 2.08% | -0.9 |
| Ecuador | 2.77% | 1.89% | -0.88 |
| Norway | 1.38% | 0.61% | -0.77 |

Group-stage no-edge/pass calls in v2: 14.

## Honest Caveat

The squad and manager layers are now structurally in the model, but several values are seed/proxy values. For a sellable product, replace them with licensed squad/player ratings and analyst-reviewed manager/formation profiles.
