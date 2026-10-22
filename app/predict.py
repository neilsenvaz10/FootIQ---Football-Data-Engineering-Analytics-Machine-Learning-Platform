"""Match-outcome prediction using the EXISTING frozen models. Nothing is trained or modified here.

Club competitions  -> club v1 (primary) and club v2-r1 (shown separately), both via the feature code the project already uses
                      for inference (FootIQ_Club_Model_Development_v2/_scripts/d11_prospective_logger.py -> make_predictions).
International       -> the v2.7 ensemble artifact (data/model_artifacts/v27/live_match_model.pkl), with the same feature
                      construction as scripts/build_live_predictions_v27.py applied to a single pair.

Every result carries the competition's validation badge from config.py.
"""
import os
import sys
import threading
from functools import lru_cache

import numpy as np
import pandas as pd

import config as C
import analytics

DEV = C.ROOT / "FootIQ_Club_Model_Development_v2" / "_scripts"
PREP_BUILD = C.ROOT / "FootIQ_ML_Training_Preparation" / "_build"
SCRIPTS = C.ROOT / "scripts"
V_UNIVERSE = PREP_BUILD / "work" / "V_universe.pkl"
V27_ARTIFACT = C.ROOT / "data" / "model_artifacts" / "v27" / "live_match_model.pkl"


class PredictionError(ValueError):
    """Raised for user-facing problems (unknown team, missing data)."""


def _base(key: str) -> dict:
    comp = C.BY_KEY[key]
    return dict(competition_key=key, competition=comp["name"], validation_badge=comp["badge"], validation_basis=comp["basis"])


# ------------------------------------------------------------------------------------------------ club
@lru_cache(maxsize=1)
def _club_runtime():
    if not V_UNIVERSE.exists():
        raise PredictionError(f"club history file missing: {V_UNIVERSE.relative_to(C.ROOT)} (needed for feature construction)")
    for p in (str(DEV), str(PREP_BUILD)):
        if p not in sys.path:
            sys.path.insert(0, p)
    import d11_prospective_logger as lg  # noqa: E402  (existing project code; importing it writes nothing)

    V = pd.read_pickle(V_UNIVERSE)
    tier = V.groupby("competition_id").tier.first()
    return lg, V, tier


@lru_cache(maxsize=1)
def _club_state():
    """Replay all history ONCE with the project's own state machines (same loop as v2_features.build / feature_contract.build_features),
    then answer any number of fixtures from the final state. Parity with make_predictions is checked in tests/test_miniproject.py."""
    import json

    lg, V, tier = _club_runtime()
    import v2_features as vf
    import feature_contract as fc

    meta = json.load(open(os.path.join(lg.WORK, "features_v2_meta.json")))["elo2_params"]
    st2, st1 = vf.V2State((meta["K"], meta["HA"], meta["season_regression"])), fc.ClubState()
    base = lg.universe_frame(V)
    for dt, g in base.sort_values(["dt", "record_id"], kind="mergesort").groupby("dt", sort=True):
        rows = list(g.itertuples())
        st2.apply_day(dt.toordinal(), [dict(h=r.h, a=r.a, comp=r.comp, season=r.season, ctype=r.ctype, regular=r.regular, rated=r.rated, gh=r.gh, ga=r.ga) for r in rows])
        st1.apply_day(dt, [dict(home=r.h, away=r.a, completed=True, rated=r.rated, gh=r.gh, ga=r.ga) for r in rows])
    return st2, st1, vf, fc


_BUILD_LOCK = threading.Lock()   # lru_cache does not stop two threads building the 30 s state at once


def _club_probs(h, a, comp_id, season, dt, tier):
    lg, V, tiers = _club_runtime()
    with _BUILD_LOCK:
        st2, st1, vf, fc = _club_state()
    from v2_models import add_derived

    f2 = st2.features(h, a, comp_id, season, dt.toordinal(), tier)
    F = pd.DataFrame([f2])
    pH, pD, pA = vf.poisson_probs(F.lambda_home.fillna(1.4).values, F.lambda_away.fillna(1.1).values)
    nanrow = (F.lambda_home.isna() | F.lambda_away.isna()).values
    F["poisson_pH"], F["poisson_pD"], F["poisson_pA"] = np.where(nanrow, np.nan, pH), np.where(nanrow, np.nan, pD), np.where(nanrow, np.nan, pA)
    F["exp_goal_diff"] = F.lambda_home - F.lambda_away
    F2 = add_derived(F)
    F1 = pd.DataFrame([st1.features(h, a, dt, tier)])
    v2m, v1m, v1prep, v1elo = _club_models()
    return (v2m["model"].predict_proba(v2m["prep"].transform(F2, True))[0], lg.v1_proba(v1m, v1prep, F1)[0],
            lg.v1_elo_proba(v1elo, F1.elo_diff.values)[0], int(F2.home_n_prior.iloc[0]), int(F2.away_n_prior.iloc[0]), bool(F1.pair_connected_asof.iloc[0]))


def warm_up():
    """Optional: build the cached club state at server start (about 30 s) so the first request is fast."""
    with _BUILD_LOCK:
        _club_state()
        _club_models()


@lru_cache(maxsize=1)
def _club_models():
    return _club_runtime()[0].load_models()


def club_data_end() -> str:
    _, V, _ = _club_runtime()
    return str(V.match_date.max())[:10]


def _entity(key: str, team: str) -> str:
    d = analytics.matches()
    d = d[d.competition_key == key]
    for col_name, col_id in (("home", "home_entity_id"), ("away", "away_entity_id")):
        hit = d.loc[d[col_name] == team, col_id]
        if len(hit):
            return hit.iloc[-1]
    raise PredictionError(f"'{team}' has no matches in {C.BY_KEY[key]['name']} in the dataset")


def predict_club(key: str, home: str, away: str, date: str | None = None) -> dict:
    if home == away:
        raise PredictionError("home and away team must differ")
    comp = C.BY_KEY[key]
    lg, V, tier = _club_runtime()
    h, a = _entity(key, home), _entity(key, away)
    last = V.dt.max()
    dt = pd.Timestamp(date) if date else last + pd.Timedelta(days=1)
    if dt <= last:
        raise PredictionError(f"date must be after the last result in the data ({last.date()}); features only use earlier matches")
    season = analytics.seasons(key)[0]
    p2, p1, pe, n_h, n_a, connected = _club_probs(h, a, comp["source_id"], season, dt, tier.get(comp["source_id"], np.nan))
    rec = dict(v1_p_home=p1[0], v1_p_draw=p1[1], v1_p_away=p1[2], p_home=p2[0], p_draw=p2[1], p_away=p2[2], v1_elo_p_home=pe[0], v1_elo_p_draw=pe[1],
               v1_elo_p_away=pe[2], home_n_prior=n_h, away_n_prior=n_a, eligible_dataset_v1_1_rule=bool(n_h >= 5 and n_a >= 5 and connected))
    notes = []
    if rec["home_n_prior"] < 5 or rec["away_n_prior"] < 5:
        notes.append("Fewer than 5 earlier rated matches for at least one team: low-history prediction.")
    if not rec["eligible_dataset_v1_1_rule"] and not notes:
        notes.append("The two teams are not connected in the rating graph at this date; treat ratings as less comparable.")
    if comp["badge"] == C.NOT_VALIDATED:
        notes.append("This competition is NOT validated: the club models were evaluated on domestic leagues only. Probabilities are indicative.")
    trio = lambda m, *k: dict(model=m, **{n: float(rec[x]) for n, x in zip(("home", "draw", "away"), k)})  # noqa: E731
    return dict(**_base(key), home=home, away=away, date=str(dt.date()), data_through=str(last.date()),
                primary=trio("Club v1 (frozen multinomial logistic regression)", "v1_p_home", "v1_p_draw", "v1_p_away"),
                secondary=trio("Club v2-r1 (frozen candidate; development-validated only, no unbiased evaluation)", "p_home", "p_draw", "p_away"),
                elo_only=trio("Elo-only mapping (v1 baseline)", "v1_elo_p_home", "v1_elo_p_draw", "v1_elo_p_away"),
                history=dict(home_prior_matches=rec["home_n_prior"], away_prior_matches=rec["away_n_prior"]), notes=notes)


# ------------------------------------------------------------------------------------------------ international
@lru_cache(maxsize=1)
def _intl_runtime():
    import pickle

    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import build_live_predictions_v27 as v27  # noqa: E402
    import build_worldcup_model_v2 as v2  # noqa: E402
    import model_bakeoff_v26 as v26  # noqa: E402

    with open(V27_ARTIFACT, "rb") as fh:
        artifact = pickle.load(fh)
    elo = v27.load_lookup(v27.PROCESSED / "team_elo_latest.csv", "team", normalize_key=True)
    form = v27.load_lookup(v27.PROCESSED / "team_recent_form_latest.csv", "team", normalize_key=True)
    asof = max(r.get("last_match_date", "") for r in elo.values())
    return v27, v2, v26, artifact, elo, form, asof


def predict_intl(key: str, home: str, away: str, date: str | None = None, venue: str | None = None) -> dict:
    """venue: 'neutral' or 'home' (the first team has home advantage). Default: neutral, except Nations League (home/away legs)."""
    if home == away:
        raise PredictionError("teams must differ")
    comp = C.BY_KEY[key]
    v27, v2, v26, artifact, elo, form, asof = _intl_runtime()
    venue = venue or ("home" if key == "UNL" else "neutral")
    h, a = v2.normalize_team(home), v2.normalize_team(away)
    for t, raw in ((h, home), (a, away)):
        if t not in elo or t not in form:
            raise PredictionError(f"no rating/form data for '{raw}' in the international tables")
    fixture_date = v27.parse_date(date) if date else pd.Timestamp(asof).to_pydatetime()
    neutral, home_field = (1, 0) if venue == "neutral" else (0, 1)
    is_comp, is_wc, bucket = v27.tournament_flags(comp["name"])
    safe = v27.safe_float

    def side(t):
        f, e = form[t], elo[t]
        return dict(elo=safe(e.get("elo_rating"), 1500.0), ppg5=safe(f.get("ppg_last_5"), 1.0), ppg10=safe(f.get("ppg_last_10"), 1.0),
                    gd5=v27.avg_total(f, "goal_diff_last_5", "matches_last_5", 0.0), gd10=v27.avg_total(f, "goal_diff_last_10", "matches_last_10", 0.0),
                    ec5=v27.avg_total(f, "elo_change_last_5", "matches_last_5", 0.0), ec10=v27.avg_total(f, "elo_change_last_10", "matches_last_10", 0.0),
                    opp5=safe(f.get("avg_opponent_elo_last_5"), 1500.0), days=v27.days_since(fixture_date, f.get("last_match_date") or e.get("last_match_date")),
                    n=safe(e.get("matches_played"), 0.0))
    H, A = side(h), side(a)
    import math

    row = {
        "fixture_key": "Q1", "team1": home, "team2": away, "home_team": h, "away_team": a, "tournament_bucket": bucket, "neutral": neutral,
        "home_field": home_field, "is_competitive": is_comp, "is_world_cup": is_wc,
        "home_elo_pre": H["elo"], "away_elo_pre": A["elo"], "elo_diff": H["elo"] - A["elo"], "abs_elo_diff": abs(H["elo"] - A["elo"]),
        "elo_avg": (H["elo"] + A["elo"]) / 2.0, "home_recent_ppg5": H["ppg5"], "away_recent_ppg5": A["ppg5"], "recent_ppg5_diff": H["ppg5"] - A["ppg5"],
        "recent_gd5_diff": H["gd5"] - A["gd5"], "recent_elochg5_diff": H["ec5"] - A["ec5"], "recent_oppelo5_diff": H["opp5"] - A["opp5"],
        "recent_ppg10_diff": H["ppg10"] - A["ppg10"], "recent_gd10_diff": H["gd10"] - A["gd10"], "recent_elochg10_diff": H["ec10"] - A["ec10"],
        "rest_days_diff": H["days"] - A["days"], "home_matches_prior_log": math.log1p(H["n"]), "away_matches_prior_log": math.log1p(A["n"]),
        "matches_prior_log_diff": math.log1p(H["n"]) - math.log1p(A["n"]),
    }
    probs = v27.predict_models(artifact, [row])
    p = probs["ensemble"][0]
    rule = artifact["pass_rules"]["ensemble"]
    pick = v26.pick_with_pass(probs["ensemble"], rule["min_confidence"], rule["min_gap"], rule["draw_risk_min"], rule["draw_gap_max"])[0]
    notes = [f"Team ratings and form are as of {asof}; results after that date are not reflected.",
             f"Venue assumption: {'neutral ground' if venue == 'neutral' else home + ' has home advantage'}."]
    if comp["badge"] == C.PARTIAL:
        notes.append("Partially validated: the model was tested on all internationals 2023-26 pooled, not on this competition specifically.")
    return dict(**_base(key), home=home, away=away, date=str(fixture_date.date()), data_through=asof,
                primary=dict(model="International v2.7 ensemble (50% gradient boosting, 30% Elo, 20% logistic; temperature-calibrated)",
                             home=float(p[0]), draw=float(p[1]), away=float(p[2])),
                elo_only=dict(model="Elo formula", home=float(probs["elo_formula"][0][0]), draw=float(probs["elo_formula"][0][1]), away=float(probs["elo_formula"][0][2])),
                gate=dict(public_pick=pick, meaning="'pass' = the project's confidence gate declines to call this match"),
                history=dict(home_prior_matches=int(H["n"]), away_prior_matches=int(A["n"])), notes=notes)


def predict(key: str, home: str, away: str, date: str | None = None, venue: str | None = None) -> dict:
    if key not in C.BY_KEY:
        raise PredictionError(f"unknown competition '{key}'")
    if C.BY_KEY[key]["kind"] == "club":
        return predict_club(key, home, away, date)
    return predict_intl(key, home, away, date, venue)
