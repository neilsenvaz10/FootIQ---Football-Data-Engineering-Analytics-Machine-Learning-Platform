# World Cup Model v2.3

V2.3 is a bias-control and realism upgrade on v2.2.

## What changed

- Manager quality weight reduced from 15% to 3%.
- Unknown/manual-required managers are neutralized to 65 rather than treated as weak.
- Squad/player impact is increased to 32%.
- Availability/injury impact is increased to 7%.
- A light 5% market sanity layer is added for current top-six public outright odds.
- Knockout resolution now separates 90 minutes, extra time, and penalties.
- Group and knockout simulations include small performance-noise terms to represent match-to-match variance.

## v2.3 Weights

| Layer | Weight |
|---|---:|
| elo_score | 30% |
| squad_score | 32% |
| recent_form_score | 10% |
| tactical_score | 10% |
| availability_score | 7% |
| market_score | 5% |
| ceiling_score | 3% |
| manager_score | 3% |

## Draw Output

- 90-minute model draw picks in group stage: 11.
- Public draw leans: 5.
- Draw-risk/no-edge calls: 6.

## Top Title Odds

| Rank | Team | Champion % | Final % | Semi % |
|---:|---|---:|---:|---:|
| 1 | France | 11.85% | 18.69% | 29.45% |
| 2 | Spain | 10.56% | 17.55% | 29.04% |
| 3 | Argentina | 8.91% | 15.45% | 26.53% |
| 4 | Brazil | 7.13% | 12.79% | 21.61% |
| 5 | England | 6.53% | 12.09% | 21.34% |
| 6 | Germany | 5.42% | 10.45% | 18.54% |
| 7 | Colombia | 4.99% | 9.96% | 19.33% |
| 8 | Portugal | 4.32% | 8.75% | 17.37% |
| 9 | Japan | 3.97% | 8.18% | 15.42% |
| 10 | Turkey | 3.69% | 7.58% | 15.27% |
| 11 | Ecuador | 3.45% | 7.04% | 13.75% |
| 12 | Morocco | 3.42% | 7.17% | 13.75% |

## Biggest Changes vs v2.2

| Team | v2.2 % | v2.3 % | Change | Power change |
|---|---:|---:|---:|---:|
| Argentina | 11.89% | 8.91% | -2.98 | -1.122 |
| France | 14.47% | 11.85% | -2.62 | -0.157 |
| Spain | 11.59% | 10.56% | -1.03 | 0.462 |
| Brazil | 8.15% | 7.13% | -1.02 | -0.959 |
| Norway | 1.9% | 2.65% | 0.75 | 0.408 |
| Germany | 6.14% | 5.42% | -0.72 | -1.403 |
| Canada | 0.61% | 1.31% | 0.7 | -0.093 |
| Colombia | 5.66% | 4.99% | -0.67 | -1.165 |
| Belgium | 2.71% | 3.3% | 0.59 | -0.147 |
| Switzerland | 1.47% | 1.98% | 0.51 | -0.524 |
| Turkey | 3.2% | 3.69% | 0.49 | -0.316 |
| Ecuador | 2.96% | 3.45% | 0.49 | -0.47 |

## Honest Caveat

The market layer currently uses a light top-six public prior, not a full paid odds feed. Teams without a market input receive a neutral market score, so this is a sanity check rather than a bookmaker-cloning layer.
