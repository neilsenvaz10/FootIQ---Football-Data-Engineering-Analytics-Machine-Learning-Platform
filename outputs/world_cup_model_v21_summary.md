# World Cup Model v2.1

V2.1 keeps the weighted v2 tournament engine but replaces the seed/proxy squad inputs with Player Impact Rating v2.1 team scores.

## Player Layer

- 1,246 players populated from public squad tables.
- Squad, expected XI, and bench scores are derived from player impact scores.
- Ratings are model-derived and transparent; they are not copied from EA, FIFA, Transfermarkt, or a paid provider.

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
| 1 | France | 18.25% | 27.88% | 41.49% |
| 2 | Argentina | 13.98% | 24.13% | 39.46% |
| 3 | Spain | 13.54% | 23.13% | 39.37% |
| 4 | Brazil | 8.95% | 15.96% | 26.54% |
| 5 | England | 7.01% | 13.82% | 25.96% |
| 6 | Germany | 6.09% | 12.35% | 22.42% |
| 7 | Colombia | 5.68% | 12.42% | 25.26% |
| 8 | Japan | 3.61% | 8.08% | 16.03% |
| 9 | Portugal | 3.43% | 8.33% | 19.4% |
| 10 | Morocco | 2.89% | 6.82% | 14.38% |
| 11 | Turkey | 2.8% | 6.78% | 16.37% |
| 12 | Netherlands | 2.41% | 5.86% | 12.69% |

## Biggest Changes vs v1

| Team | V1 % | V2.1 % | Change |
|---|---:|---:|---:|
| Spain | 22.98% | 13.54% | -9.44 |
| France | 13.41% | 18.25% | 4.84 |
| Brazil | 5.21% | 8.95% | 3.74 |
| Argentina | 17.39% | 13.98% | -3.41 |
| Germany | 2.87% | 6.09% | 3.22 |
| Japan | 2.28% | 3.61% | 1.33 |
| Turkey | 1.53% | 2.8% | 1.27 |
| Colombia | 4.83% | 5.68% | 0.85 |
| Morocco | 2.05% | 2.89% | 0.84 |
| Belgium | 1.59% | 2.39% | 0.8 |

Group-stage no-edge/pass calls in v2.1: 15.

## Honest Caveat

This is a stronger product layer than v2 because player names and derived role scores are now populated. The biggest remaining weakness is that recent club/national minutes are still inferred rather than pulled from a licensed live feed.
