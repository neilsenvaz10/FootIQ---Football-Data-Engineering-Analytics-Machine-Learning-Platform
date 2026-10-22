"""Tests for the mini-project app (data prep, analytics, prediction wrapper, API).

Run:  .venv\\Scripts\\python.exe -X utf8 -m pytest tests/test_miniproject.py -q
The club-prediction tests build the 216k-match history state once (about 20-30 s).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

APP = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP))

import analytics  # noqa: E402
import config as C  # noqa: E402
import predict  # noqa: E402

pytest.importorskip("httpx")
from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)
needs_data = pytest.mark.skipif(not C.MATCHES_CSV.exists(), reason="run app/prepare_data.py first")


@needs_data
def test_matches_schema_and_scope():
    m = analytics.matches()
    assert set(m.competition_key) == {c["key"] for c in C.COMPETITIONS} and len(C.COMPETITIONS) == 11
    assert not m.duplicated(["competition_key", "date", "home", "away", "stage"]).any()
    assert m.home_goals.notna().all() and m.away_goals.notna().all() and (m.home_goals >= 0).all()
    assert m.date.str.match(r"^\d{4}-\d{2}-\d{2}$").all()
    assert (m.source != "").all() and (m.licence != "").all()          # attribution kept on every row


@needs_data
def test_audit_lists_every_competition_with_badge():
    a = analytics.audit()
    assert [r["competition_key"] for r in a] == [c["key"] for c in C.COMPETITIONS]
    badges = {r["competition_key"]: r["validation_badge"] for r in a}
    assert all(badges[k] == C.NOT_VALIDATED for k in ("UCL", "UEL", "UECL"))
    assert all(badges[k] == C.VALIDATED for k in ("EPL", "LALIGA", "BUNDESLIGA", "SERIEA", "LIGUE1", "WC"))
    assert all(badges[k] == C.PARTIAL for k in ("UNL", "COPA"))


@needs_data
def test_standings_are_consistent():
    t = analytics.standings("EPL", "2023-24")
    assert len(t) == 20 and sum(x["played"] for x in t) == 2 * 380
    assert sum(x["gd"] for x in t) == 0 and sum(x["gf"] for x in t) == sum(x["ga"] for x in t)
    assert t[0]["points"] >= t[-1]["points"]


@needs_data
def test_club_names_are_one_to_one_with_entities():
    m = analytics.matches()
    club = m[m.home_entity_id != ""]
    pairs = pd.concat([club[["home", "home_entity_id"]].set_axis(["n", "e"], axis=1), club[["away", "away_entity_id"]].set_axis(["n", "e"], axis=1)]).drop_duplicates()
    assert not pairs.duplicated("e").any()


@needs_data
@pytest.mark.parametrize("key,home,away", [("EPL", "Arsenal FC", "Chelsea FC"), ("UCL", "Manchester City FC", "Real Madrid CF"),
                                           ("WC", "Brazil", "Argentina"), ("COPA", "Brazil", "Argentina"), ("UNL", "Spain", "France")])
def test_predictions_are_probabilities_with_badge(key, home, away):
    r = predict.predict(key, home, away)
    p = r["primary"]
    assert abs(p["home"] + p["draw"] + p["away"] - 1) < 1e-6 and min(p["home"], p["draw"], p["away"]) >= 0
    assert r["validation_badge"] == C.BY_KEY[key]["badge"]
    if key == "UCL":
        assert any("NOT validated" in n for n in r["notes"])


@needs_data
def test_fast_club_path_matches_original_inference_code():
    """The cached-state path must reproduce the project's own make_predictions exactly (same frozen models)."""
    lg, V, tier = predict._club_runtime()
    comp = C.BY_KEY["SERIEA"]
    dt = V.dt.max() + pd.Timedelta(days=1)
    h, a = predict._entity("SERIEA", "Juventus FC"), predict._entity("SERIEA", "AC Milan")
    fx = pd.DataFrame(dict(fixture_id=["T"], dt=[dt], h=[h], a=[a], comp=[comp["source_id"]], season=[analytics.seasons("SERIEA")[0]], tier=[tier[comp["source_id"]]],
                           home_name=["Juventus FC"], away_name=["AC Milan"], kickoff=["x"], kickoff_known=[False]))
    ref = lg.make_predictions(fx, V, "x", "x", "x")[0]
    mine = predict.predict("SERIEA", "Juventus FC", "AC Milan")
    assert np.allclose([mine["primary"][k] for k in ("home", "draw", "away")], [ref["v1_p_home"], ref["v1_p_draw"], ref["v1_p_away"]], atol=1e-9)
    assert np.allclose([mine["secondary"][k] for k in ("home", "draw", "away")], [ref["p_home"], ref["p_draw"], ref["p_away"]], atol=1e-9)


@needs_data
def test_api_errors_are_clean():
    assert client.get("/api/predict", params=dict(key="XXX", home="a", away="b")).status_code == 404
    assert client.get("/api/predict", params=dict(key="EPL", home="Nobody FC", away="Arsenal FC")).status_code == 422
    assert client.get("/api/predict", params=dict(key="EPL", home="Arsenal FC", away="Chelsea FC", date="2020-01-01")).status_code == 422
    assert client.get("/api/predict", params=dict(key="EPL", home="Arsenal FC", away="Arsenal FC")).status_code == 422
    assert client.get("/api/competitions/EPL/dashboard", params=dict(season="1999-00")).status_code == 404


@needs_data
def test_api_dashboard_and_overview():
    assert len(client.get("/api/competitions").json()) == 11
    d = client.get("/api/competitions/LIGUE1/dashboard", params=dict(season="2019-20")).json()
    assert d["standings"] and d["summary"]["matches"] == 279          # known source gap, must stay visible
    cov = [c for c in client.get("/api/competitions/LIGUE1/coverage").json() if c["season"] == "2019-20"][0]
    assert cov["note"] == "incomplete or in progress"
    assert client.get("/api/competitions/UCL/dashboard", params=dict(season="2024-25")).json()["standings"] is None   # no league table for cups


@pytest.mark.skipif(not sys.flags.utf8_mode, reason="existing simulator needs python -X utf8 on Windows")
def test_worldcup_simulation_runs_and_is_a_distribution():
    r = client.get("/api/worldcup/simulate", params=dict(simulations=200)).json()
    assert r["simulations"] == 200
    assert abs(sum(t["champion_pct"] for t in r["title_odds"]) - 100) < 1.0
