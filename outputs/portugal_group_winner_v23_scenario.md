# Portugal Group-Winner Scenario v2.3

This is a conditional Monte Carlo scenario using the existing v2.3 World Cup tournament engine.

## First correction

The saved v2.3 model did not call Colombia to beat Portugal in the final group match. It marked Colombia vs Portugal as a draw lean.

| Match | Team 1 win | Draw | Team 2 win | Public call |
|---|---:|---:|---:|---|
| Colombia vs Portugal | 37.08% | 28.35% | 34.56% | Draw lean |

Colombia ranked above Portugal because Colombia had a slightly higher v2.3 power score and a higher simulated chance of winning Group K, not because of one deterministic Portugal loss.

| Team | Power | Group 1st % | Group 2nd % | Champion % |
|---|---:|---:|---:|---:|
| Colombia | 77.042 | 42.73% | 31.17% | 4.99% |
| Portugal | 75.668 | 39.09% | 32.6% | 4.32% |

## What-if condition

- Accepted simulations: 50,000.
- Attempts needed: 127,172.
- Acceptance rate: 39.32%.
- Portugal title chance if it tops Group K: 5.54%.

## Bracket if Portugal is 1K

| Stage | Bracket slot |
|---|---|
| Round of 32 | 1K vs 3D/E/I/J/L |
| Round of 16 | Winner of 1B vs 3E/F/G/I/J |
| Quarter-final | Winner from the 1J/2H/2D/2G side |
| Semi-final | Winner from the W91/W92 branch |
| Final | Winner from the other half of the bracket |

## Conditional Portugal Path

| Stage | Portugal reaches stage | Win if stage reached | Most common opponents |
|---|---:|---:|---|
| Round of 32 | 100.0% | 65.96% | Panama 22.56%; Croatia 17.48%; Ghana 16.0%; England 9.29%; USA 4.5%; Paraguay 4.42%; Australia 4.28%; Turkey 3.35% |
| Round of 16 | 65.96% | 61.8% | Switzerland 26.53%; Canada 22.43%; Egypt 5.99%; Iran 5.76%; Belgium 4.75%; Bosnia & Herzegovina 4.0%; New Zealand 3.37%; Austria 2.36% |
| Quarter-final | 40.76% | 53.69% | Argentina 28.79%; Spain 10.62%; Uruguay 9.51%; Turkey 8.6%; Belgium 8.22%; USA 5.19%; Egypt 5.18%; Paraguay 5.02% |
| Semi-final | 21.89% | 50.54% | Brazil 13.45%; England 13.31%; Mexico 9.48%; France 8.9%; Germany 6.69%; Morocco 6.58%; Norway 6.14%; Ecuador 5.58% |
| Final | 11.06% | 50.05% | France 13.76%; Spain 13.74%; Colombia 6.11%; Germany 6.04%; Japan 5.35%; Brazil 5.19%; Argentina 4.66%; Belgium 4.63% |

## Portugal Finish Distribution

| Outcome | % if Portugal tops group |
|---|---:|
| Eliminated in Round of 32 | 34.04% |
| Eliminated in Round of 16 | 25.2% |
| Eliminated in Quarter-final | 18.88% |
| Eliminated in Semi-final | 10.82% |
| Eliminated in Final | 5.53% |
| Champion | 5.54% |

## Most Common Exact Paths

| Rank | Path | % |
|---:|---|---:|
| 1 | Round of 32: Croatia > eliminated in Round of 32 | 6.68% |
| 2 | Round of 32: Panama > eliminated in Round of 32 | 6.14% |
| 3 | Round of 32: England > eliminated in Round of 32 | 5.12% |
| 4 | Round of 32: Ghana > eliminated in Round of 32 | 3.11% |
| 5 | Round of 32: Panama > Round of 16: Switzerland > eliminated in Round of 16 | 1.82% |
| 6 | Round of 32: USA > eliminated in Round of 32 | 1.61% |
| 7 | Round of 32: Paraguay > eliminated in Round of 32 | 1.59% |
| 8 | Round of 32: Turkey > eliminated in Round of 32 | 1.58% |
| 9 | Round of 32: Ghana > Round of 16: Switzerland > eliminated in Round of 16 | 1.5% |
| 10 | Round of 32: Australia > eliminated in Round of 32 | 1.46% |

## Caveat

This is still the v2.3 tournament simulator, so it uses the v2.3 power model and Poisson knockout engine. It is not yet the v2.6 ensemble/calibration layer.
