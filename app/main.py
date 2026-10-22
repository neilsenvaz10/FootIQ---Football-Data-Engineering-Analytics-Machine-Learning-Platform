"""FootIQ mini-project API + static page.

    .venv\\Scripts\\python.exe -X utf8 -m uvicorn main:app --app-dir app --port 8000
then open http://127.0.0.1:8000
"""
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import analytics
import config as C
import predict
import worldcup_sim

STATIC = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_):
    # build the club-prediction state in the background so the first prediction is fast (about 30 s)
    threading.Thread(target=lambda: _safe(predict.warm_up), daemon=True).start()
    yield


def _safe(fn):
    try:
        fn()
    except Exception as exc:  # noqa: BLE001  (warm-up failure must not stop the dashboard)
        print("warm-up failed:", exc)


app = FastAPI(title="FootIQ mini-project", version="1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC), name="static")


def _comp(key: str) -> dict:
    if key not in C.BY_KEY:
        raise HTTPException(404, f"unknown competition '{key}'")
    return C.BY_KEY[key]


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/competitions")
def competitions():
    audit = {a["competition_key"]: a for a in analytics.audit()}
    return [dict(key=c["key"], name=c["name"], group=c["group"], badge=c["badge"], basis=c["basis"], **{k: audit[c["key"]][k] for k in (
        "rows", "seasons", "first_date", "last_date", "sources", "licences")}) for c in C.COMPETITIONS]


@app.get("/api/competitions/{key}/seasons")
def seasons(key: str):
    _comp(key)
    return analytics.seasons(key)


@app.get("/api/competitions/{key}/teams")
def teams(key: str):
    _comp(key)
    return analytics.teams(key)


@app.get("/api/competitions/{key}/coverage")
def coverage(key: str):
    _comp(key)
    return analytics.season_coverage(key)


@app.get("/api/competitions/{key}/dashboard")
def dashboard(key: str, season: str):
    comp = _comp(key)
    if season not in analytics.seasons(key):
        raise HTTPException(404, f"no data for season '{season}'")
    return dict(competition=comp["name"], badge=comp["badge"], season=season, summary=analytics.summary(key, season),
                standings=analytics.standings(key, season) if comp["group"] == "Domestic league" else None,
                results=analytics.recent_results(key, season))


@app.get("/api/team")
def team(key: str, team: str, opponent: str | None = None):
    _comp(key)
    out = dict(form=analytics.team_form(key, team))
    if opponent:
        out["head_to_head"] = analytics.head_to_head(key, team, opponent)
    return out


@app.get("/api/predict")
def predict_match(key: str, home: str, away: str, date: str | None = None, venue: str | None = Query(None, pattern="^(neutral|home)$")):
    _comp(key)
    try:
        return predict.predict(key, home, away, date, venue)
    except predict.PredictionError as exc:
        raise HTTPException(422, str(exc)) from exc


@app.get("/api/worldcup/simulate")
def simulate(simulations: int = Query(worldcup_sim.DEFAULT_SIMS, ge=100, le=worldcup_sim.MAX_SIMS)):
    try:
        return worldcup_sim.run(simulations)
    except worldcup_sim.SimulationError as exc:
        raise HTTPException(500, str(exc)) from exc
