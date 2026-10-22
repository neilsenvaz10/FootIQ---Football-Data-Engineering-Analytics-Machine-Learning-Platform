"""Mini-project configuration: the 11 competitions, their data sources and prediction status.

Scope is fixed (see docs/mini-project/MINI_PROJECT_PLAN.md). Do not add competitions here.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MINI_DIR = ROOT / "data" / "miniproject"
MATCHES_CSV = MINI_DIR / "matches.csv"
AUDIT_CSV = MINI_DIR / "data_audit.csv"
SEASON_COVERAGE_CSV = MINI_DIR / "season_coverage.csv"

CLUB_SOURCE = ROOT / "FootIQ_ML_Data_Readiness" / "04d_COMBINED_CLUB_MATCHES_v1.0.csv"
CLUB_COVERAGE_MATRIX = ROOT / "FootIQ_ML_Data_Readiness" / "01_COMPETITION_SEASON_COVERAGE_MATRIX.csv"
INTL_RESULTS = ROOT / "data" / "raw" / "international_results" / "results.csv"
WC2026_GROUP = ROOT / "data" / "processed" / "matchday_validation_v210.csv"
WC2026_KO = ROOT / "data" / "processed" / "worldcup_2026_knockout_results_verified.csv"
INTL_SHOOTOUTS = ROOT / "data" / "raw" / "international_results" / "shootouts.csv"

# validation badges shown next to every prediction
VALIDATED = "Validated"
PARTIAL = "Partially validated"
NOT_VALIDATED = "Not validated (indicative only)"

COMPETITIONS = [
    # key, display name, group, source kind, source id, model family, badge, badge explanation
    dict(key="EPL", name="English Premier League", group="Domestic league", kind="club", source_id="england:1-premierleague",
         model="club", badge=VALIDATED,
         basis="Club v1 locked test and forward-holdout results (per-league rows in FootIQ_Club_Model_Baseline_v1/06a_LEAGUE_WISE_METRICS.csv). Previously inspected, not new evidence."),
    dict(key="LALIGA", name="La Liga", group="Domestic league", kind="club", source_id="espana:1-liga", model="club", badge=VALIDATED,
         basis="Club v1 locked test and forward-holdout results. Previously inspected, not new evidence."),
    dict(key="BUNDESLIGA", name="Bundesliga", group="Domestic league", kind="club", source_id="deutschland:1-bundesliga", model="club", badge=VALIDATED,
         basis="Club v1 locked test and forward-holdout results. Previously inspected, not new evidence."),
    dict(key="SERIEA", name="Serie A", group="Domestic league", kind="club", source_id="italy:1-seriea", model="club", badge=VALIDATED,
         basis="Club v1 locked test and forward-holdout results. Previously inspected, not new evidence."),
    dict(key="LIGUE1", name="Ligue 1", group="Domestic league", kind="club", source_id="europe/france:fr1", model="club", badge=VALIDATED,
         basis="Club v1 locked test and forward-holdout results. Previously inspected, not new evidence."),
    dict(key="WC", name="FIFA World Cup", group="International", kind="intl", source_id="FIFA World Cup", model="intl", badge=VALIDATED,
         basis="Full 2026 tournament validation (data/processed/worldcup_full_validation_summary_2026-07-19.csv) and the v2.6 chronological test."),
    dict(key="UCL", name="UEFA Champions League", group="Continental club", kind="club", source_id="champions-league:cl", model="club", badge=NOT_VALIDATED,
         basis="Club models were evaluated on domestic leagues only; no continental-competition metric exists. Cross-league Elo is not comparable."),
    dict(key="UEL", name="UEFA Europa League", group="Continental club", kind="club", source_id="champions-league:el", model="club", badge=NOT_VALIDATED,
         basis="Same as the Champions League: no continental-competition validation."),
    dict(key="UECL", name="UEFA Conference League", group="Continental club", kind="club", source_id="champions-league:conf", model="club", badge=NOT_VALIDATED,
         basis="Same as the Champions League: no continental-competition validation."),
    dict(key="UNL", name="UEFA Nations League", group="International", kind="intl", source_id="UEFA Nations League", model="intl", badge=PARTIAL,
         basis="International model validated on pooled internationals 2023-26 and the 2025 UNL finals bracket; no competition-specific accuracy figure."),
    dict(key="COPA", name="Copa América", group="International", kind="intl", source_id="Copa América", model="intl", badge=PARTIAL,
         basis="International model validated on pooled internationals 2023-26; no Copa América-specific accuracy figure."),
]
BY_KEY = {c["key"]: c for c in COMPETITIONS}
