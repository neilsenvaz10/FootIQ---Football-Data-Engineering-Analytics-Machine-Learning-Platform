# World Cup Model v1

This is the first working MVP prediction engine built from the collected public/open data.

## What It Uses

- Prototype international Elo from 49k+ historical matches.
- Recent form from each team's last 5 and last 10 matches.
- A championship-ceiling adjustment so participant-level teams do not get unrealistic title odds.
- Host advantage for Mexico, Canada, and USA based on match venue.
- StatsBomb open tactical/event adjustment where 2018/2022 World Cup data exists.
- Optional player-availability/replacement-gap override support.

## What It Does Not Yet Have

- Licensed live injury feed.
- Confirmed or expected lineups.
- Paid squad-quality/player-minute feed.
- Paid odds feed.
- Full tracking-data tactical layer.

## Important Product Choice

The model does not headline exact scores. It uses internal goal simulation only to build group tables and tournament paths.

## Top Title Odds

| Rank | Team | Champion % | Final % | Semi % | Tier |
|---:|---|---:|---:|---:|---|
| 1 | Spain | 22.98% | 33.90% | 47.83% | Tier 1 contender |
| 2 | Argentina | 17.39% | 28.25% | 41.12% | Tier 1 contender |
| 3 | France | 13.41% | 22.13% | 37.11% | Tier 1 contender |
| 4 | England | 6.47% | 13.03% | 24.14% | Tier 1 contender |
| 5 | Brazil | 5.21% | 10.83% | 21.54% | Tier 1 contender |
| 6 | Colombia | 4.83% | 10.41% | 19.43% | Tier 1 contender |
| 7 | Portugal | 3.21% | 7.69% | 15.53% | Tier 1 contender |
| 8 | Netherlands | 2.98% | 7.00% | 15.51% | Tier 1 contender |
| 9 | Germany | 2.87% | 6.72% | 15.67% | Tier 2 dark horse |
| 10 | Ecuador | 2.77% | 6.51% | 15.22% | Tier 2 dark horse |
| 11 | Japan | 2.28% | 5.68% | 13.44% | Tier 2 dark horse |
| 12 | Morocco | 2.05% | 5.13% | 12.37% | Tier 2 dark horse |

## Model Caveat

This is a v1 probability engine, not a final betting product. The outputs are useful for iteration, backtesting, and dashboard design; commercial confidence requires live licensed feeds and calibration.
