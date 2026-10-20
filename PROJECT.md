# FootIQ — Global Football Data Engineering, Analytics & Machine Learning Platform

**Document:** `PROJECT.md`  
**Version:** 1.0 (comprehensive project blueprint)  
**Date:** 20 October 2026  
**Status:** Proposed architecture; implementation audit pending  
**Existing project:** `world-cup-prediction-model`  
**Academic deliverables:** Data Engineering mini project; Machine Learning mini project; optional literature survey/research paper

> **Truth and scope legend:** **EXISTING (reported)** = described from the existing World Cup project, but not independently verified against its source code here. **PLANNED** = to be implemented. **CONDITIONAL** = dependent on data access, license, provider coverage, or experiment results. Examples and proposed performance targets are not measured outcomes. The 30-page *Define Football ML Project* document is an original proposal, not evidence that those features were already implemented.

---

## 1. Executive summary

**FootIQ** is a full-stack football intelligence system combining automated football data ingestion, data quality validation, a PostgreSQL analytical warehouse, time-safe feature engineering, supervised and unsupervised machine learning, international match outcome prediction, player scouting, team performance analysis, and World Cup tournament simulation. Users will explore a React web interface powered by FastAPI. Apache Airflow will orchestrate scheduled batch/incremental data updates, with Docker Compose providing a reproducible local environment.

Rather than replacing an existing functioning model, FootIQ **extends the existing Python World Cup prediction research pipeline**. That system reportedly includes a trained international 90-minute win/draw/loss ensemble, confidence/abstention gates, a separate goal-based World Cup simulator, historical datasets, scripts, tests, and CSV/Markdown reports. The engineering objective is to preserve its reproducible outputs while replacing ad hoc file-oriented updates with structured, auditable data workflows.

The same shared platform produces **two distinct assessed projects**:

1. **Data Engineering:** *Global Football Data Engineering & Analytics Pipeline* — extraction, validation, normalization, incremental upserts, PostgreSQL warehouse, Airflow DAGs, source freshness, quality monitoring, SQL analytics, and an operational dashboard.
2. **Machine Learning:** *Football Performance Analytics and Match Outcome Prediction Using Machine Learning* — leakage-safe match classification, calibrated ensemble predictions, player performance modeling (where reliable targets exist), player clustering/similarity, dimensionality reduction, evaluation dashboards, and World Cup simulation.
3. **Optional research paper:** *Comparative Analysis of Machine Learning and Ensemble Models for Football Match Outcome Prediction Using Leakage-Safe Feature Engineering* — controlled comparison of feature representations, algorithms, time splits, calibration, and confidence filtering.

**Primary scope:** international football worldwide for historical match prediction and World Cup analysis; expand **club football** initially to the Premier League, La Liga, Bundesliga, Serie A, and Ligue 1 for team/player analytics, contingent on coverage and permissions. A club-match predictor is **not automatically validated** by the international-team model and must be separately trained/evaluated before release.

---

## 2. Background and existing assets

### 2.1 Original FootIQ concept (from the supplied PDF)

The original ML proposal, prepared for a three-member student team (Bhanu, Neilsen, Preeti), was a **Football Performance Analytics & Match Prediction System**, branded **FootIQ**. It proposed:

- Player performance analysis and prediction.
- Player similarity and clustering.
- Team performance analytics.
- Win/draw/loss match prediction.
- ML analytics dashboard for model comparisons, PCA/t-SNE/UMAP and clustering quality.
- React frontend and FastAPI backend, using Python/Pandas/scikit-learn/XGBoost.
- Supervised model comparison (Logistic Regression, KNN, SVM, Decision Tree, Random Forest, XGBoost), regression (Linear/Ridge/Lasso), clustering (K-Means, DBSCAN, hierarchical), and dimensionality reduction.
- A focused literature survey/research paper on **leakage-safe match outcome prediction**, not an overly broad paper claiming novelty across every module.

The PDF recommended separating match-level and player-level datasets; its suggestions included Football-Data.co.uk for club results and StatsBomb Open Data for player/event analysis. These are **design recommendations**, not verified current coverage or licensing.

### 2.2 Reported World Cup prediction baseline

| Existing asset | Reported detail | Integration approach |
|---|---|---|
| Historical results | 49,296 international matches, Nov 1872–2 Jun 2026 | Preserve source snapshots; audit exact row count/schema |
| Training sample | 25,235 matches, 4 Jan 2000–2 Jun 2026 | Reproduce filter and chronological split |
| Match model | v2.7 weighted ensemble: 50% Gradient Boosting, 30% Elo, 20% Logistic Regression, 0% Poisson | Keep artifacts, feature contract, calibration |
| Public prediction filter | v2.7 agreement gate; v2.8 confidence gate | Preserve abstention/“Pass” logic |
| Tournament simulation | Goal-model-based Monte Carlo; 50,000 runs; v2.13 completed-result locking | Keep distinct from 1X2 ensemble |
| StatsBomb archive | Metadata and processed summaries for 128 World Cup matches from 2018/2022 | Do not assume full raw events/360 are present |
| World Cup fixtures | OpenFootball 2026 structure, 104 fixtures, 48 teams | Verify revision and competition rules |
| Supplemental data | Public squad profiles, rankings, GDP/population references, API-Football, Open-Meteo/NWS | Track source, timestamp, value, and availability |
| Output format | CSV/Markdown reports, manual Python script runs | Retain for reproducibility; add DB/API/UI |
| Tests | 28 reported passing tests | Re-run before any refactor |

**Interpretation safeguards:** Archived group-stage validation (34/52) and knockout advancement validation (25/30) must **not** be presented as 1X2 match accuracy. A final retrain on all available history is **not** a new out-of-sample performance claim. The public confidence gate may choose “Pass” for every fixture; abstention is valid, not a failure.

### 2.3 Existing repository, as seen in the screenshot

```text
world-cup-prediction-model/
├── .venv/
├── data/
├── docs/
├── outputs/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── README_SHARE.md
├── requirements-share.txt
├── SHARE_MANIFEST.sha256
└── project reference PDFs
```

**Not yet audited:** exact file tree below `data/` and `scripts/`, artifact formats, schemas, external service contracts, test reproducibility, and original provider licensing. No plan below should be treated as a statement that these proposed directories or features already exist.

### 2.4 Core integration decision

Maintain separate concepts for:

- **National-team matches** versus **club matches**.
- **90-minute outcome** versus **extra-time/penalty shootout advancement**.
- **Match 1X2 classifier** versus **goal model used by the tournament simulator**.
- **Historical feature availability** versus **information discovered after a match**.
- **Descriptive player score** versus **independently validated future player-performance prediction**.
- **Data refresh** versus **ML retraining**.

---

## 3. Problem statement

Football data is scattered across historical match archives, competition feeds, player-event repositories, squad records, rankings, and third-party APIs. The sources vary in format, update frequency, naming conventions, completeness, and rights of use. As a result, it is difficult to maintain reliable cross-source analytics, generate up-to-date team/player features, or produce reproducible and leakage-safe predictions. FootIQ addresses these challenges by building a documented, automated football data pipeline and warehouse, developing statistically sound ML components, and exposing source-aware analytics and predictions through a user-facing application.

### 3.1 Project objectives

**Data Engineering objectives**

1. Ingest historical and new match/player/fixture data from permitted sources.
2. Preserve raw source snapshots, retrieval timestamps, hashes, and provenance.
3. Normalize competitions, teams, players, match statuses, scores, and provider IDs.
4. Load curated data into PostgreSQL with idempotent upserts and correction history.
5. Schedule workflows with Airflow, retries, monitoring, and freshness reporting.
6. Generate SQL analytics and reproducible point-in-time feature datasets.
7. Demonstrate data quality, incremental processing, failure recovery, and operational observability.

**ML objectives**

1. Reproduce the existing international 1X2 ensemble and evaluate it on historical holdouts.
2. Compare supervised algorithms and football-specific feature representations.
3. Estimate calibrated match outcome probabilities and support confidence-based abstention.
4. Analyze player performance with normalized, position-aware statistics.
5. Build player clustering and nearest-neighbor similarity recommendations.
6. Train player regression only if an independent and temporally valid target exists.
7. Preserve and integrate the existing World Cup simulator.
8. Document leakage controls, dataset coverage, reproducibility, and model limitations.

**Application objectives**

1. Provide a responsive React interface and typed/documented FastAPI routes.
2. Show match predictions, team trends, player comparisons, simulations, and evaluation metrics.
3. Display data freshness, source coverage, model versions, and uncertainty.
4. Provide separate, clear demonstrations for the DE and ML academic evaluations.

---

## 4. Scope, priorities, and non-goals

### 4.1 Must-have MVP

- Historical international match backfill into PostgreSQL.
- Canonical teams, matches, competitions, source IDs, and ingestion run tables.
- Reliable incremental fixture/result updates for **supported** competitions.
- Data quality checks, correction handling, and Airflow DAGs.
- Existing international ensemble integrated with time-safe warehouse features.
- Existing World Cup simulator accessible through a documented interface.
- Selected club league result analytics and a viable player data subset.
- Player clustering/similarity on a sufficiently complete and comparable cohort.
- React/FastAPI app with Teams, Players, Match Predictor, World Cup, ML Analytics, and Pipeline Health pages.
- Automated tests and reproducible setup/documentation.

### 4.2 Should-have

- Club-team analytics for all five named leagues.
- Position-aware player profiles with per-90 metrics and similarity explanations.
- Chronological comparison of multiple match classifiers.
- Calibration, abstention-coverage, and model evaluation dashboards.
- Independent player performance regression where a valid target is available.
- Source freshness alerts and historical correction replay.

### 4.3 Could-have, only if justified

- A separately trained club match outcome predictor.
- Apache Spark event-processing benchmark on sufficiently large event data.
- Player xG/xA, detailed tactical visualizations, and 360 data if permitted.
- Squad-aware pre-match features with reliable historical availability.
- Live match event streaming via Kafka if a true event feed and use case exist.
- Public hosting, mobile/PWA, multilingual UI, advanced model monitoring.

### 4.4 Explicit non-goals

- Guaranteed real-time coverage of every country, league, player, and competition.
- Fabricated or silently estimated missing player statistics.
- Guaranteed accurate predictions or gambling recommendations.
- Automatic retraining after every new match.
- Treating post-match statistics as pre-match model inputs.
- Implementing every syllabus algorithm as a separate production feature.
- Overwriting the current model/repository before its baseline is verified.

---

## 5. Users and functional requirements

### 5.1 Personas

- **Fan:** browses teams, players, fixtures, probabilities, and World Cup scenarios.
- **Student analyst:** compares model metrics, feature importance, and player clusters.
- **Data engineer:** inspects DAG status, source freshness, duplicates, and corrections.
- **Faculty evaluator:** runs repeatable DE and ML demonstrations, checks evidence and reports.
- **Maintainer/admin:** configures providers, runs backfills, reviews unresolved identities, promotes models.

### 5.2 User stories and acceptance

| ID | User story | Expected behavior |
|---|---|---|
| FR-01 | Search a national team or club | Show entity type, competition context, recent results and available metrics |
| FR-02 | Compare two teams | Use comparable windows and label missing statistics |
| FR-03 | View a match prediction | Show 1X2 probabilities, timestamp, model version, confidence/Pass |
| FR-04 | Inspect a player | Show appearances, minutes, per-90 statistics and source coverage |
| FR-05 | Find similar players | Return comparable-role neighbors, distances, cluster labels and caveats |
| FR-06 | Inspect tournament scenarios | Show locked results, simulation seed, runs, and advancement probabilities |
| FR-07 | Explore model evaluation | Show chronological splits, baselines, calibration and confusion matrix |
| FR-08 | Monitor ingestion | Show source status, DAG runs, freshness, row changes and errors |
| FR-09 | Re-run a historical batch | Produce no duplicate canonical facts; record a new audit run |
| FR-10 | Correct a historical result | Record the correction and rebuild affected downstream chronological features |

---

## 6. Dataset strategy: historical, current, player, and context

### 6.1 Source inventory

| Source | Intended information | Current state | Update mechanism | Important limitation |
|---|---|---|---|---|
| Existing international results archive | Dates, teams, score, tournament, venue/context | **EXISTING (reported)** | One-time backfill + scheduled reconciliation | Confirm original license, data quality, and latest coverage |
| StatsBomb Open Data | Matches, lineups, events, selected 360 data | **PARTIAL EXISTING** (processed metadata); expansion planned | Release check and allowed JSON ingestion | Not complete across all competitions/players; attribution required |
| OpenFootball | Fixtures, results, competition structure | **EXISTING (reported)** | File/repository version diff | Coverage and corrections depend on maintainers |
| Football-Data.co.uk | Domestic league match results and some match statistics | **PLANNED** | Seasonal CSV backfill + scheduled checks | Columns/coverage vary by league and season; review terms |
| API-Football | Fixtures, statuses, results, player stats, lineups, squads | **PARTIALLY USED (reported)**; expansion planned | API polling with quotas and cursors | Coverage, historical access, rate limits, pricing, and reuse rights vary |
| Public squad tables | Squad membership and basic profiles | **EXISTING (reported)** | Authorized feed or documented manual snapshot | Unreliable for automatic worldwide transfer coverage |
| FIFA rankings | National-team ranking snapshots | **EXISTING (reported)** | On official release | Historical snapshot must predate the prediction |
| Open-Meteo / NWS | Forecast/weather context | **EXISTING (reported)** | Fixture-based refresh | Forecast availability, venue coordinates, and temporal cutoff |
| World Bank indicators | Country-level context | **EXISTING (reported)** | Annual/as published | Experimental; avoid spurious or ethically questionable inference |
| Additional licensed player source | Club season/player stats where open data is insufficient | **CONDITIONAL** | Contract/provider-specific | Required for broad current player coverage |

**Source URLs for investigation (not blanket permission to redistribute):**

- StatsBomb Open Data: https://github.com/statsbomb/open-data
- OpenFootball: https://github.com/openfootball
- Football-Data.co.uk: https://www.football-data.co.uk/
- API-Football: https://www.api-football.com/
- Open-Meteo: https://open-meteo.com/
- FIFA: https://www.fifa.com/
- World Bank: https://data.worldbank.org/

### 6.2 Coverage strategy

**International layer:** retain worldwide national-team historical results, 2026 World Cup fixtures and results, and national-team match predictions. Label men's/women's, senior/youth, friendly/competitive, and regulation-time semantics correctly based on actual source coverage.

**Club layer:** start with five European top divisions for selected seasons and available players; do not claim every player metric exists for every season. Preserve club and national-team identities separately. Club match prediction remains conditional on a separately evaluated model.

**Player layer:** StatsBomb events provide rich analysis for selected competitions, but not universal coverage. Where event-level data is absent, display available match/season aggregates only. Show source coverage by player, season, competition, and metric. A missing tackle count is **unknown**, not necessarily zero.

### 6.3 Provenance contract

Each dataset/provider must have a record of:

- Publisher, URL, access method, licensing/terms, attribution.
- Competition/season/gender/level coverage.
- Earliest/latest record and latest provider update.
- Retrieval timestamp, original file hash, schema version, API parameters.
- Redistribution and caching restrictions.
- Allowed update frequency, API quota and cost.
- Known missing fields, quirks, corrections, and quality tests.

**Never commit** credentials, personal tokens, proprietary provider payloads, or files whose redistribution is disallowed. Keep raw snapshots in appropriately ignored/local storage, with a reproducible manifest.

---

## 7. Automatic data updates: exact behavior

### 7.1 Proposed schedule (not yet deployed)

| Job | Suggested cadence | Outcome |
|---|---|---|
| Fixture discovery | Every 6 hours | New, postponed, rescheduled, and changed fixtures |
| Matchday status | Every 15–30 minutes, within provider quota | Kickoff/live/final status and score |
| Final-result reconciliation | On confirmed final + next day | Official 90-minute result and corrections |
| Player match statistics | After final and next-day recheck | New appearance/event records |
| Squad/transfer refresh | Daily or weekly | Effective-dated player-team memberships |
| Public repository updates | Weekly | Newly released match/event/fixture files |
| Elo/form feature rebuild | After accepted result changes | Updated team ratings and rolling features |
| Player profile aggregates | Daily | Per-90 and season aggregates |
| Clustering refresh | Weekly or after adequate new sample | New cluster/similarity version |
| Prediction refresh | On fixture/feature changes | Future-match probabilities and gate decisions |
| Model candidate retraining | Monthly/manual, evaluation-gated | Candidate artifact, never automatic blind promotion |
| World Cup simulations | After relevant confirmed results/rules changes | New versioned simulation snapshot |
| Data quality monitor | Daily and after ingestion | Freshness, missingness, duplicates, anomalies |

Actual cadence must be reconciled with API plan quotas, costs, and provider terms before deployment.

### 7.2 Match lifecycle example

1. Airflow queries a fixture source and receives a provider-specific fixture ID.
2. The extractor saves the raw response, retrieval timestamp, provider, hash, and run ID.
3. The normalizer converts date/time to UTC, maps competition and team IDs, and records match status.
4. Validation checks score format, status, identities, season, and duplicates.
5. The loader upserts the canonical fixture; a retry does not create a second match.
6. On official **final** status, regulation-time result becomes eligible for match-outcome facts.
7. Any extra time, penalties, and advancement winner are stored **separately**.
8. Chronological Elo/form features are updated. A correction to an older result triggers replay of dependent later features.
9. Future fixture predictions are regenerated with the current **pre-kickoff-available** feature snapshot.
10. The dashboard displays result, model version, feature timestamp, source, and last refresh.
11. A follow-up reconciliation detects amended scores/statistics and records change history.

### 7.3 Player lifecycle example

1. Resolve player using stable canonical ID and source-ID mapping; never rely on name alone.
2. Fetch match appearance, minutes, role/position, and available actions.
3. Validate against match/team context; insert/update appearance and event facts.
4. Recompute player season and per-90 aggregates with minutes thresholds.
5. Preserve transfer history using `valid_from`/`valid_to` membership records.
6. Refresh similarity/clustering on a controlled cadence; version resulting profiles.
7. Mark unavailable event metrics as unavailable rather than inventing them.

### 7.4 Reliability and correction policy

- **Idempotency:** unique provider/source keys and deterministic canonical mappings.
- **Retries:** exponential backoff and API quota awareness; no uncontrolled retry storms.
- **Quarantine:** unresolved entities and malformed records do not silently contaminate gold tables.
- **Correction log:** track previous/new values, source, retrieval time, affected features.
- **Watermarks:** incremental extraction cursors per provider and competition.
- **Late data:** bounded lookback windows and replay jobs.
- **Freshness:** separate `source_updated_at`, `fetched_at`, `processed_at`, `data_as_of`.
- **Failure behavior:** retain last verified values, display staleness, and do not claim live status.
- **Reproducibility:** historical source snapshots must support reconstructing what was known at prediction time.

---

## 8. High-level system architecture

```text
Historical CSV/JSON    StatsBomb/OpenFootball    Club CSV feeds    Football APIs    Weather
       \                     |                      |               |              /
        +--------------------+----------------------+---------------+-------------+
                                             |
                                  Apache Airflow DAGs
                                             |
                       Extract -> Validate -> Normalize -> Resolve IDs
                                             |
                            Raw snapshots + ingestion manifests
                                             |
                              PostgreSQL staging / silver
                                             |
                       Canonical matches / teams / players / events
                                             |
                             Gold analytics + feature snapshots
                               /                |               \
                         SQL analytics    ML inference/train   World Cup simulator
                               \                |               /
                                +----------- FastAPI ---------+
                                              |
                                         React FootIQ
                                              |
                              Fans / Analysts / DE and ML demos
```

**Environment:** Docker Compose for PostgreSQL, Airflow, backend, and optional Streamlit pipeline-monitoring app; React/Vite development server. Airflow metadata must be isolated from football analytical schemas/databases.

**Design boundary:** Airflow orchestrates reusable Python modules; ETL business logic must be independently callable and testable without Airflow.

---

## 9. Data warehouse and schema design

### 9.1 Layers

- **Bronze/raw:** immutable or versioned provider files/responses with checksums and extraction metadata.
- **Silver/staging:** typed normalized rows, validated identities, deduplicated records, provider mappings, quality flags.
- **Gold/marts:** analytics-ready facts/dimensions, historical ratings, player per-90 aggregates, model feature snapshots, predictions.

These are **logical** layers; they may be implemented as PostgreSQL schemas plus raw files/object storage.

### 9.2 Proposed tables

| Table | Fields (illustrative) | Constraint/usage |
|---|---|---|
| `sources` | `source_id, name, url, license, terms_checked_at` | Provenance |
| `ingestion_runs` | `run_id, source_id, start_at, end_at, status, counts, error` | Operations |
| `raw_objects` | `object_id, source_id, external_key, fetched_at, sha256, storage_uri` | Versioned raw snapshots |
| `competitions` | `competition_id, name, type, country, gender, level` | National/club and competition scope |
| `seasons` | `season_id, competition_id, label, start_at, end_at` | Competition seasons |
| `teams` | `team_id, name, team_type, country_code` | National vs club |
| `players` | `player_id, display_name, birth_date_nullable, nationality_nullable` | Stable player identity |
| `provider_entity_ids` | `source_id, entity_type, external_id, canonical_id, confidence` | Provider mapping |
| `player_team_memberships` | `player_id, team_id, valid_from, valid_to, source_id` | Effective-dated transfer history |
| `matches` | `match_id, competition_id, season_id, kickoff_utc, side_a_id, side_b_id, status, venue_id` | Canonical match |
| `match_results` | `match_id, regulation_a/b, extra_time_a/b, penalties_a/b, advancing_team_id` | Do not mix score semantics |
| `team_match_stats` | `match_id, team_id, shots, possession, passes, fouls, ...` | Nullable if not covered |
| `player_appearances` | `match_id, player_id, team_id, minutes, position, goals, assists, ...` | Unique appearance |
| `player_events` | `source_event_id, match_id, player_id, event_type, time, x, y, payload` | Conditional event coverage |
| `team_ratings_history` | `team_id, match_id, elo_before, elo_after, rating_version` | Replayable chronology |
| `team_feature_snapshots` | `team_id, cutoff_utc, feature_version, rolling_form, rest_days, ...` | Point-in-time features |
| `player_feature_snapshots` | `player_id, cutoff_utc, scope, feature_version, per90_metrics` | Player analytics/ML |
| `predictions` | `fixture_id, predicted_at, model_version, p_a, p_draw, p_b, decision` | Sum to 1; audit |
| `simulation_runs` | `run_id, created_at, seed, iterations, model_version, fixture_snapshot` | Reproducible tournaments |
| `model_registry` | `version, dataset_hash, train_cutoff, metrics_uri, artifact_uri, status` | Model lineage |
| `quality_checks` | `run_id, table_name, check_name, passed, details` | Quality history |

### 9.3 Analytics marts/views

- `mart_team_form`: rolling 5/10 results, goals, strength of opposition, cutoff.
- `mart_team_head_to_head`: dated prior meetings, explicitly descriptive.
- `mart_player_per90`: goals/assists/shots/passes/defensive actions, minutes thresholds.
- `mart_competition_results`: league/tournament statistics, with competition semantics.
- `mart_prediction_performance`: versioned prediction versus observed 90-minute outcome.
- `mart_source_freshness`: last successful sync, lag, quality, and source coverage.

### 9.4 Database integrity rules

- Provider source keys unique per entity type; canonical match identity resolved carefully.
- Team A and Team B must differ; valid competition/season foreign keys.
- Nonnegative score integers; nullable scores before completion.
- Player minutes nonnegative and consistent with competition/match type.
- Preserve corrections instead of silently rewriting historical provenance.
- Index competition/season, kickoff, team-match, player-match, external IDs, and feature cutoff.
- Use `EXPLAIN ANALYZE` and realistic benchmark datasets before claiming index speedups.

---

## 10. Airflow DAGs and ETL modules

### 10.1 Proposed DAGs

| DAG | Core tasks | Trigger |
|---|---|---|
| `historical_backfill` | discover → fetch → hash → parse → validate → map → load → audit | Manual/batch |
| `fixture_refresh` | API poll → snapshot → normalize → upsert → QA | 6-hour schedule |
| `result_reconciliation` | final-score fetch → corrections → upsert → feature replay | Matchdays |
| `player_stats_refresh` | fetch appearances/events → validate → load → aggregates | Daily/post-match |
| `open_data_sync` | source revision diff → allowed downloads → parse → load | Weekly |
| `feature_snapshot_build` | select cutoff → rolling features → leakage tests → publish | Data-dependent |
| `prediction_refresh` | load approved model → features → infer → calibrate → gate → persist | Fixture/feature-dependent |
| `quality_monitor` | freshness → duplicates → coverage → anomalies → alert | Daily |
| `candidate_model_training` | snapshot → split → train → evaluate → register | Manual/monthly gated |

### 10.2 Quality checks

- Required keys, valid dates/time zones, expected status values.
- Duplicate canonical fixtures and provider IDs.
- Score and match status consistency; shootout separation.
- Missing values and schema drift by provider/season.
- Unresolved player/team identity and conflicting provider data.
- API quota errors, stale data, and unexpected row-count changes.
- Feature observation time and **availability time** not later than prediction cutoff.
- Probability outputs finite, each in `[0,1]`, summing approximately to 1.
- Deterministic backfill/replay results and correction lineage.

### 10.3 Proposed ETL package layout

```text
pipelines/
├── extract/           # provider adapters, pagination, caching, quotas
├── normalize/         # timezones, score semantics, units, schemas
├── validate/          # required fields, ranges, schemas
├── identity/          # team/player/provider ID resolution
├── load/              # transactions, staging, upserts
├── reconcile/         # amended scores and late-arriving facts
├── features/          # cutoff-aware team/player features
└── quality/           # tests, freshness, completeness
```

---

## 11. Machine Learning design

### 11.1 International match prediction

**Task:** predict regulation-time 1X2: Side A win, draw, Side B win. For neutral fixtures, do not incorrectly label Side A as a home team. Penalty-shootout winners and extra-time advancement are separate outcomes.

**Existing ensemble (reported):** 50% Gradient Boosting + 30% Elo-derived probabilities + 20% Logistic Regression. Verify how the Elo component generates class probabilities and how the blend is calibrated. Keep the existing v2.7/v2.8 artifacts and decision gates.

**Pre-match features (subject to availability):**

- Elo before kickoff, Elo difference.
- Rolling last 5/10 results and goal statistics, computed only from earlier matches.
- Opponent-strength-adjusted form and competition context.
- Rest days and neutral/home context.
- Prior head-to-head information (with caution about sample size).
- Squad availability only from timestamped pre-match sources.
- Forecast weather only as known before prediction; never observed post-match weather for historical pre-match inference.

**Candidate comparison models:** frequency baseline, Elo-only, Logistic Regression, KNN, SVM, Decision Tree, Random Forest, Gradient Boosting, XGBoost. Optional Naive Bayes and AdaBoost for syllabus experiments. Do not claim all are currently trained.

**Evaluation:** chronological train/validation/test; optionally rolling-origin backtests; train-only imputation, scaling, encoding, PCA/feature selection, hyperparameter tuning, and calibration. Metrics: accuracy, balanced accuracy, macro F1, class precision/recall, confusion matrix, multiclass log loss, Brier score, calibration plots, and abstention coverage/selective risk.

**Confidence:** preserve “Pass” as a legitimate output; report both full-fixture performance and published-pick performance with their different denominators.

### 11.2 Club match prediction — separate track

The existing international model must not be presented as a validated Premier League or La Liga predictor. A club predictor would require its own training rows, season-aware features, league context, chronological validation, and performance report. Until then, club pages provide **analytics**, not unsupported predictive probabilities.

### 11.3 Player performance analytics and regression

**Descriptive metrics:** minutes, starts, goals, assists, shots, passing, defensive actions, xG/xA when available, and per-90 versions. Filter or flag players below a minimum minutes threshold; normalize by role and competition context.

**Regression decision gate:** only train a performance predictor after selecting a defensible, independently observed and temporally separated target (e.g., a provider rating for a future match, future multi-match contributions, or future minutes). A hand-crafted same-match weighted score is a **descriptive index**, not independently validated predictive ML.

**Candidate regression models:** Linear Regression, Ridge, Lasso; compare to historical-average baseline. Metrics: MAE, RMSE, residual analysis, time/season holdouts, and role-specific error.

### 11.4 Player clustering and similarity

- Construct player feature vectors from sufficiently complete comparable statistics.
- Use per-90 metrics, minimum playing time, role-specific cohorts, missingness policies.
- Scale features appropriately and inspect correlation/outliers.
- Compare K-Means, DBSCAN, optional hierarchical clustering.
- Evaluate silhouette, Davies–Bouldin, stability, and football interpretability.
- Use PCA for component analysis; t-SNE or UMAP for **visualization**, not proof that clusters are objectively real.
- Recommend nearest players using scaled-feature distance/cosine similarity within comparable cohorts; a shared cluster alone is not a complete similarity measure.
- Label archetypes such as “attacking creator” as analyst interpretations, not ground truth.

### 11.5 World Cup simulation

Keep the existing separate goal-based Monte Carlo simulator, reportedly 50,000 runs. Support completed-result locking, competition rules, groups, knockout brackets, advancement and champion probabilities. Store simulation seed, iterations, model version, fixture snapshot, ruleset, and cutoff. Do not equate advancement success with match 1X2 accuracy.

### 11.6 Feature refresh versus retraining

**New result → data update → Elo/form refresh → prediction refresh** using the currently approved model. **Retraining** happens only on a controlled schedule or manual request, producing a candidate artifact that is evaluated against the current model and promoted only if justified. Maintain rollback support and artifact hashes.

### 11.7 Model registry

Record model version, feature version, dataset snapshot/hash, training cutoff, code revision, hyperparameters, preprocessing pipeline, calibration method, metrics, serialization format, and deployment state. Never compare scores from different test periods without stating the differences.

---

## 12. Research and literature survey plan

**Working title:** *Comparative Analysis of Machine Learning and Ensemble Models for Football Match Outcome Prediction Using Leakage-Safe Feature Engineering*.

**Central research question:** How do football-specific feature engineering, dimensionality reduction/selection, and ensemble learning influence out-of-time football 1X2 prediction performance?

**Subquestions:**

- RQ1: Do pre-match engineered football features outperform basic pre-match statistics?
- RQ2: Does PCA improve or harm prediction relative to the full engineered feature set?
- RQ3: Which classifiers produce the best calibrated probabilities, not just top-1 accuracy?
- RQ4: How do chronological and random splits differ, and what leakage risks arise?
- RQ5: How does abstention affect coverage and selective accuracy?

**Experiment matrix:**

| Experiment | Feature representation | Evaluation |
|---|---|---|
| E1 | Minimal pre-match baseline | Same chronological holdout |
| E2 | E1 + Elo/form/opposition/rest | Same chronological holdout |
| E3 | E2 + train-fitted PCA | Same chronological holdout |
| E4 | E2 + train-fitted feature selection | Same chronological holdout |

Compare a controlled subset of Logistic Regression, KNN/SVM, Decision Tree, Random Forest, Gradient Boosting/XGBoost, and Elo baseline using the same time splits and tuning budgets. Record confidence intervals where feasible, calibration, data cutoffs, and ablation effects.

**Literature survey outline:** football prediction problem; Elo/Poisson statistical models; classification and ensembles; football-specific features; player/event data; PCA/feature selection; temporal leakage; calibration and abstention; limitations of public datasets; identified research gap.

**Research integrity:** original PDF citations are leads, not a verified bibliography. Check primary papers and accurate bibliographic metadata before final submission. Do not claim novelty merely from combining common tools; emphasize reproducible comparative evidence.

---

## 13. Backend and frontend

### 13.1 Technology stack

| Layer | Recommended tools | Why |
|---|---|---|
| Frontend | React + Vite + JavaScript, React Router | Interactive application; matches original proposal |
| Backend | Python FastAPI + Pydantic | Native integration with Python ML/ETL |
| Database | PostgreSQL | SQL joins, indexes, constraints, analytics |
| ORM/DB access | SQLAlchemy / psycopg | Transactions, typed access |
| Data transforms | Pandas + NumPy | Practical for current scale |
| Orchestration | Apache Airflow | DAGs, retries, scheduling, logs |
| Visualization | Plotly/Recharts | Trends, calibration, clusters, comparisons |
| DE demo | Optional Streamlit + Plotly | Quick independent ETL/SQL demonstration |
| ML | scikit-learn + existing dependencies; XGBoost if selected | Experiments and deployment |
| Infrastructure | Docker Compose | Reproducible local multi-service environment |
| Testing | pytest, SQL tests, API tests, frontend tests | Functional and regression safety |
| Optional | Spark | Only for meaningful event-data benchmark |
| Deferred | Kafka | Only if actual streaming is implemented |

### 13.2 Planned application pages

1. **Overview:** data coverage, recent matches, supported leagues, upcoming fixtures, latest ingestion timestamp.
2. **Teams:** search, team type, recent form, competition filters, historical trends, head-to-head.
3. **Players:** search, player profile, club history, season and competition statistics, per-90 metrics, data availability.
4. **Similar Players:** nearest-neighbor list, feature radar comparison, cluster interpretation, 2D PCA/t-SNE/UMAP view.
5. **Match Predictor:** fixture selection, three probabilities, timestamp, confidence/Pass, version, data cutoff.
6. **World Cup:** fixture/bracket view, fixed results, stage probabilities, champion probabilities, simulation metadata.
7. **ML Analytics:** algorithm comparisons, chronological splits, confusion matrix, log loss/calibration, feature studies, clustering metrics.
8. **Data Pipeline:** Airflow DAG links/status, source freshness, row counts, errors, quarantine, data quality.

**UI principle:** never display illustrative scores or unavailable stats as genuine results; mark demo/synthetic values visibly. Display “data unavailable” rather than inventing a number.

### 13.3 Proposed API routes

```text
GET  /api/health
GET  /api/data/sources
GET  /api/data/freshness
GET  /api/competitions
GET  /api/teams?query=&type=
GET  /api/teams/{team_id}/matches
GET  /api/teams/{team_id}/analytics
GET  /api/players?query=&competition_id=
GET  /api/players/{player_id}
GET  /api/players/{player_id}/similar
GET  /api/players/{player_id}/performance
GET  /api/fixtures?from=&to=&competition_id=
GET  /api/predictions/{fixture_id}
POST /api/predictions/preview
GET  /api/world-cup/simulations/latest
POST /api/world-cup/simulations          # authenticated/admin
GET  /api/ml/experiments
GET  /api/ml/models
GET  /api/pipeline/runs
GET  /api/pipeline/quality
POST /api/admin/ingestion/run            # authenticated/admin
```

For all API responses, include appropriate `as_of`, `source`, `coverage`, and `model_version` metadata. Protect expensive operations, credentials, admin endpoints, and provider licensing. Document API response shapes and error codes in OpenAPI.

---

## 14. Proposed additive repository structure

**Do not move or delete existing directories until Milestone 1 audit and regression tests finish.**

```text
world-cup-prediction-model/
├── .venv/                         # existing; gitignored
├── data/                          # existing data/model artifacts
├── scripts/                       # existing research/model/simulation scripts
├── outputs/                       # existing reports
├── tests/                         # existing tests; extend
├── docs/
│   ├── architecture/
│   ├── data-sources/
│   ├── experiments/
│   ├── operations/
│   └── demos/
├── pipelines/
│   ├── extract/
│   ├── normalize/
│   ├── validate/
│   ├── identity/
│   ├── load/
│   ├── reconcile/
│   ├── features/
│   └── quality/
├── airflow/
│   └── dags/
├── database/
│   ├── migrations/
│   ├── seeds/
│   ├── sql/
│   └── tests/
├── ml/
│   ├── match/
│   ├── players/
│   ├── clustering/
│   ├── evaluation/
│   └── registry/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   └── schemas/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── api/
│   │   └── charts/
│   └── public/
├── dashboard/                     # optional Streamlit DE demo
├── config/
├── infra/
├── .env.example
├── docker-compose.yml
├── requirements-de.txt
├── PROJECT.md
└── README.md
```

**Migration strategy:** build adapters around existing script functions; compare old versus new predictions on fixed snapshots; refactor only after parity is demonstrated. Keep original CSV/Markdown reports as regression artifacts and a fallback.

---

## 15. Detailed ten-milestone roadmap

### Milestone 1 — Audit and freeze working baseline

**Tasks:** inspect full directory tree; record file hashes, data counts, licenses, model artifacts, dependencies, and current outputs; run existing tests; reproduce a fixed set of predictions and simulations; map current scripts to data sources/features/models; identify missing APIs/credentials.

**Deliverables:** `docs/architecture/CURRENT_STATE.md`, dataset inventory, dependency map, baseline report, blocker/risk register.

**Exit criteria:** working baseline reproducible or exact blockers documented. No destructive refactoring.

### Milestone 2 — Finalize scope, datasets, contracts

**Tasks:** verify provider licenses/quotas/coverage; select seasons/leagues/player cohorts; define 90-minute outcome and tournament semantics; define canonical entity IDs and feature cutoff; design data dictionary, ERD, API contracts, and dataset provenance manifests.

**Deliverables:** source matrix, coverage matrix, schema diagram, API contract, experiment protocol.

**Exit criteria:** each MVP feature has a confirmed source or is explicitly marked conditional/deferred.

### Milestone 3 — Build PostgreSQL warehouse

**Tasks:** create isolated development DB, migrations, raw/staging/gold schemas, constraints, source ID mappings; import historical international matches; add SQL queries and indexes; validate source-to-database row reconciliation.

**Deliverables:** migrations, import runner, initial marts, database tests, data dictionary.

**Exit criteria:** repeat import produces no duplicates; row counts and checksums reconcile; existing data remains unchanged.

### Milestone 4 — Build incremental ETL and quality layer

**Tasks:** implement historical/public/API connectors; normalize identities, time zones and scores; quarantine invalid rows; support correction/replay; load selected club datasets and permitted player data; build quality reports.

**Deliverables:** reusable ETL modules, sample fixtures, validation suite, replay demonstration.

**Exit criteria:** successful clean run, safe rerun, interrupted-run recovery, and correction handling demonstrated.

### Milestone 5 — Airflow and Docker orchestration

**Tasks:** Docker Compose services, Airflow DAGs, environment templates, secrets handling, scheduled jobs, retries, logging, freshness monitors, failure injection.

**Deliverables:** runnable local stack, DAG screenshots, operations runbook, pipeline metrics.

**Exit criteria:** end-to-end scheduled ingestion completes; simulated provider failure is visible and recoverable.

### Milestone 6 — Analytics warehouse and player dataset

**Tasks:** SQL marts for team form/head-to-head/player per-90; identify player sample and missingness; build position-aware cohorts; validate competition-level coverage; optional Streamlit DE dashboard.

**Deliverables:** SQL analytics queries, sample dashboard, player feature dataset, quality and coverage report.

**Exit criteria:** SQL metrics match independent test fixtures; incomplete data is correctly labeled.

### Milestone 7 — Integrate and expand ML

**Tasks:** connect existing international model to warehouse feature adapter; regression parity tests; integrate confidence gate and tournament simulator; implement clustering and similarity; attempt player regression only after target validation.

**Deliverables:** versioned model interface, predictions table, similarity results, simulation integration, parity tests.

**Exit criteria:** old/new predictions agree within declared tolerance on fixed inputs; no future leakage.

### Milestone 8 — ML experiments and research evidence

**Tasks:** freeze chronological splits; train controlled candidate models; compare raw/engineered/PCA/selected features; assess calibration, class metrics, cluster quality; build experiment registry and reproducible notebooks/reports.

**Deliverables:** experiment matrix, metrics tables/plots, ablation study, draft literature survey/methodology.

**Exit criteria:** metrics reproducible from frozen datasets; claims distinguish measured results from assumptions.

### Milestone 9 — FastAPI and React application

**Tasks:** implement API contracts; build Overview, Teams, Players, Similar Players, Predictor, World Cup, ML Analytics, Pipeline pages; implement filters, loading/error states, freshness labels, responsive design, and authentication for admin operations.

**Deliverables:** working integrated application, API docs, UI screenshots, smoke tests.

**Exit criteria:** all core pages function against actual DB/model outputs; unsupported data shown transparently.

### Milestone 10 — Final validation, documentation, demos

**Tasks:** integration/performance/security tests, end-to-end replay, API quota simulation, model evaluation audit, Docker setup validation, README, architecture diagrams, two academic reports, research-paper draft, demo scripts.

**Deliverables:** reproducible release candidate, DE report/demo, ML report/demo, optional paper, source/license appendix.

**Exit criteria:** an evaluator can run both distinct demos and trace outputs to sources, code, model versions, and test evidence.

---

## 16. Testing and acceptance plan

### 16.1 Testing layers

| Layer | Tests |
|---|---|
| Extractors | Response parsing, pagination, rate limit, auth failures, malformed payloads |
| Validation | Required fields, score/status consistency, schema drift, missingness |
| Identity | Provider ID resolution, duplicate names, transfer history, manual review |
| Warehouse | Constraints, migrations, upsert idempotence, indexes, correction history |
| Features | Chronological ordering, time cutoff, Elo replay, no post-match leakage |
| Models | Artifact load, probability normalization, calibration, regression parity |
| Clustering | Scaling, reproducibility, role cohort, minimum minutes, missing data |
| Tournament | Fixed results, bracket rules, deterministic seed, probability ranges |
| API | Schema, errors, pagination, security, freshness metadata |
| UI | Search, filters, empty states, stale-data labels, responsive behavior |
| Airflow | DAG import, retries, backfill, partial failures, dependency ordering |
| End-to-end | Historical import → update → feature → prediction → UI |

### 16.2 Proposed measurable criteria (targets, not achieved)

- **Idempotence:** duplicate canonical match count remains zero after repeated identical imports.
- **Traceability:** every displayed match prediction links to feature/model versions and data cutoff.
- **Leakage safety:** automated checks reject future-dated feature observations or availability timestamps.
- **Recovery:** failed source fetch does not corrupt previously verified gold tables.
- **Freshness:** stale sources visibly labeled with last successful sync.
- **ML evidence:** full test sample counts, split dates, class metrics, calibration, and baseline comparison documented.
- **Coverage honesty:** no player statistics fabricated for unsupported leagues/seasons.
- **Reproducibility:** documented Docker setup and fixed-snapshot experiments work on another development machine.

Do not set arbitrary “90% football prediction accuracy” as a pass criterion. Football outcome prediction is uncertain; assess against baselines, calibration, reproducibility, and credible holdouts.

---

## 17. Operational setup and deployment

### 17.1 Local environment

- Python version compatible with existing artifacts (verify during audit).
- Node.js/npm for React.
- Docker Desktop + Compose for services.
- PostgreSQL with separate development/test databases.
- Airflow configured with an isolated metadata database/schema.
- Environment variables for DB credentials, API keys, optional provider limits, model paths, logging, and feature flags.

### 17.2 Example environment variable names (values intentionally omitted)

```dotenv
DATABASE_URL=
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=
API_FOOTBALL_KEY=
API_FOOTBALL_BASE_URL=
FOOTIQ_RAW_DATA_DIR=
FOOTIQ_MODEL_ARTIFACT_DIR=
FOOTIQ_DEFAULT_TIMEZONE=UTC
FOOTIQ_ENABLE_CLUB_PREDICTIONS=false
FOOTIQ_ENABLE_PLAYER_REGRESSION=false
FOOTIQ_LOG_LEVEL=INFO
```

Do not use this example as a claim about the current `.env.example`; it is a proposed future configuration. Never put actual secrets in the document or Git.

### 17.3 Security and reliability

- Use `.gitignore`, least-privilege DB accounts, parameterized SQL, API request timeouts.
- Separate public read endpoints from admin-only ingestion/training/simulation actions.
- Validate API inputs and protect expensive computations with quotas/rate limits.
- Sanitize logs; do not log provider tokens or unnecessary personal data.
- Back up schema and critical curated data; maintain source manifests and migration history.
- Make provider licensing and attribution visible in documentation and UI where required.
- Do not promise 24/7 operation if the project runs on a local student machine.

---

## 18. Team work allocation (proposed, not assigned)

The original PDF suggested Bhanu for match prediction/backend, Neilsen for player performance/feature engineering, and Preeti for clustering/visualization. With the added Data Engineering scope, a revised balanced proposal is:

| Workstream | Lead suggestion | Shared responsibilities |
|---|---|---|
| Match prediction, ensemble evaluation, backend inference | Bhanu | Testing, ML report, integration |
| Data ingestion, PostgreSQL, feature engineering, Airflow | Neilsen | Source review, integration, DE report |
| Player analytics/clustering, visualizations, frontend analytics | Preeti | Dataset quality, evaluation, UI integration |
| Shared | All | Literature survey, architecture, documentation, demo, QA |

Finalize based on actual skills, schedules, and faculty requirements. Ensure each mini-project has a distinct contribution and presentation; confirm institutional policy on reusing datasets or code across courses.

---

## 19. Academic deliverables and demonstration scripts

### 19.1 Data Engineering demonstration (suggested 5–8 minutes)

1. Show raw source sample and provider provenance.
2. Run an Airflow DAG and show task dependencies/logs.
3. Show validation and a deliberately quarantined malformed record.
4. Query PostgreSQL tables and an analytics mart.
5. Re-run the same batch to prove no duplicate canonical match.
6. Simulate a new final match or correction and show downstream feature changes.
7. Open pipeline dashboard showing freshness and row-count metrics.

**Report evidence:** ERD, DAG graph, ETL architecture, SQL queries, source matrix, test results, sample row counts, performance measurements with methodology.

### 19.2 Machine Learning demonstration (suggested 5–8 minutes)

1. Show the historical training dataset and chronological split.
2. Explain Elo/form features and leakage prevention.
3. Compare baseline and candidate classifier metrics and calibration.
4. Predict a fixture, show three probabilities and confidence/Pass logic.
5. Show player similarity/clusters and feature-based explanations.
6. Show World Cup simulation with seed, run count, and locked results.
7. Discuss limitations, missing data, and why model accuracy differs from simulation validation.

**Report evidence:** preprocessing, features, algorithms, splits, metrics, confusion matrix, calibration, clustering evaluation, ablations, reproducibility.

### 19.3 Research paper structure

Abstract → Introduction → Literature Review → Research Gap → Data and Provenance → Leakage-Safe Methodology → Experiments → Results → Discussion → Limitations → Conclusion → References.

---

## 20. Risks, dependencies, and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Player data coverage is incomplete | Player ML may not generalize | Pilot on confirmed competitions; show coverage; defer invalid models |
| API costs/rate limits | Updates may be delayed | Cache, incremental fetch, quota budget, public-data fallback |
| Cross-source entity collisions | Duplicate/wrong matches and players | Stable IDs, mapping table, review queue, provenance |
| Historical corrections | Incorrect Elo and form | Versioned facts, chronological replay, audit logs |
| Temporal leakage | Inflated ML evaluation | Point-in-time snapshots, availability timestamps, chronological splits |
| Domain shift international → club | Misleading club predictions | Separate models and held-out validation |
| Research scope too broad | Unfinished academic work | Focus paper on match prediction; prioritize MVP |
| Airflow/Docker complexity | Setup delays | Start with standalone ETL then orchestrate; documented Compose |
| Data licensing | Redistribution or usage violations | Source terms review, attribution, controlled raw storage |
| Old model artifacts fail to load | Baseline broken | Environment freeze, hashes, compatibility test, rollback |
| Missing provider data | UI misleading | Coverage badges, nullable fields, stale/unavailable states |
| Confidence gate produces no picks | Demo appears empty | Show abstention as model behavior; use archived reproducible examples |

---

## 21. Decision log and unresolved questions

### 21.1 Agreed architectural direction (from prior discussion)

- Reuse the World Cup prediction model rather than start over.
- Create **two separate academic deliverables** from one shared platform.
- Use Python/Pandas, PostgreSQL, Apache Airflow, Docker, SQL, and a dashboard.
- Use React + FastAPI for the final user-facing ML application.
- Include player analysis/clustering and model comparisons from the original PDF.
- Prefer public historical datasets plus permitted API updates.
- Keep Spark optional and avoid Kafka until there is real streaming.
- Preserve the working model and evaluate new pipelines before switching.

### 21.2 Decisions to confirm after audit

1. Exact current dataset source(s), schemas, licenses, and checksum manifests.
2. Available API-Football subscription, coverage, quota, and budget.
3. Which club seasons and StatsBomb competitions contain enough player data.
4. Whether a defensible player regression target exists.
5. Whether club outcome prediction belongs in MVP or later phase.
6. Exact Docker/Python versions and model serialization compatibility.
7. Frontend design/theme, hosting preference, and authentication needs.
8. Timeline, faculty assessment criteria, and team member allocation.
9. Whether research paper is required or optional.
10. Data retention, raw-data sharing, and public deployment restrictions.

---

## 22. Immediate next steps — start here

**Step 1: Capture repository inventory.** From the existing project directory, run in PowerShell:

```powershell
tree /F /A > project_structure.txt
```

Also record Python version, dependency lock/list, test results, dataset manifests, and artifact hashes. Avoid sharing `.env` secrets or private API tokens.

**Step 2: Inspect existing prediction scripts.** Identify data loaders, normalization, Elo, form, calibration, confidence gate, tournament simulator, and report generation. Build an integration map rather than duplicating code.

**Step 3: Validate datasets and provider access.** Confirm 49,296 and 25,235 match counts; check StatsBomb raw events, club result sources, and API-Football capabilities. Produce a source coverage matrix.

**Step 4: Freeze baseline tests.** Reproduce selected existing predictions and simulation outputs with fixed seeds, model artifacts, and snapshots.

**Step 5: Design PostgreSQL schema and ingestion contract.** Only then start implementing warehouse migrations and historical import.

**Development rule:** Do not stage, commit, push, or modify Git history without explicit project-owner instruction. Do not delete/overwrite original datasets or model artifacts. Keep destructive changes behind backups and parity tests.

---

## 23. Definition of done

FootIQ's **Data Engineering deliverable** is complete when a documented pipeline can ingest supported historical/new football records into a validated, queryable PostgreSQL warehouse; Airflow can run and monitor repeatable incremental jobs; corrections and duplicates are handled safely; and SQL/dashboard outputs have source provenance and freshness indicators.

FootIQ's **Machine Learning deliverable** is complete when the existing international match model is reproducibly integrated, historical out-of-time evaluation and calibration are documented, player clustering/similarity operates on a valid dataset, tournament simulation remains reproducible, and a working interface displays predictions with uncertainty and coverage. Player regression and club prediction count as complete only if independently validated.

The **optional research paper** is complete when it reports a clearly framed research question, verified literature, fixed experimental design, leakage-safe time splits, reproducible metrics, limitations, and conclusions that follow from measured results.

**Final principle:** FootIQ should be evaluated for data integrity, reproducibility, sound ML methodology, and usable analytics—not for the number of frameworks listed or unsupported claims of prediction accuracy.
