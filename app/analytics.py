"""Dashboard analytics over data/miniproject/matches.csv (pandas only)."""
from functools import lru_cache

import pandas as pd

import config as C


@lru_cache(maxsize=1)
def matches() -> pd.DataFrame:
    if not C.MATCHES_CSV.exists():
        raise FileNotFoundError("data/miniproject/matches.csv is missing - run: python app/prepare_data.py")
    df = pd.read_csv(C.MATCHES_CSV, encoding="utf-8-sig", dtype={"season": str}, keep_default_na=False)
    df["home_goals"] = pd.to_numeric(df.home_goals)
    df["away_goals"] = pd.to_numeric(df.away_goals)
    return df


def audit() -> list[dict]:
    return pd.read_csv(C.AUDIT_CSV, encoding="utf-8-sig", keep_default_na=False).to_dict("records")


def season_coverage(key: str) -> list[dict]:
    d = pd.read_csv(C.SEASON_COVERAGE_CSV, encoding="utf-8-sig", dtype={"season": str})
    return d[d.competition_key == key].fillna("").to_dict("records")


def _sel(key: str, season: str | None = None) -> pd.DataFrame:
    d = matches()
    d = d[d.competition_key == key]
    return d[d.season == season] if season else d


def seasons(key: str) -> list[str]:
    return sorted(_sel(key).season.unique(), reverse=True)


def teams(key: str) -> list[str]:
    d = _sel(key)
    return sorted(set(d.home) | set(d.away))


def summary(key: str, season: str) -> dict:
    d = _sel(key, season)
    n = len(d)
    known = d[d.outcome.isin(["H", "D", "A"])]
    rate = lambda o: round(float((known.outcome == o).mean()), 4) if len(known) else None  # noqa: E731
    return dict(matches=n, goals_per_match=round(float((d.home_goals + d.away_goals).mean()), 3) if n else None,
                home_win_rate=rate("H"), draw_rate=rate("D"), away_win_rate=rate("A"), outcome_basis=d.outcome_basis.iloc[0] if n else "",
                first_date=d.date.min() if n else None, last_date=d.date.max() if n else None)


def standings(key: str, season: str) -> list[dict]:
    """League table from the scored matches in the dataset (3-1-0 points). Only meaningful for round-robin leagues."""
    d = _sel(key, season)
    rows: dict[str, dict] = {}
    for r in d.itertuples():
        for team, gf, ga in ((r.home, r.home_goals, r.away_goals), (r.away, r.away_goals, r.home_goals)):
            t = rows.setdefault(team, dict(team=team, played=0, won=0, drawn=0, lost=0, gf=0, ga=0))
            t["played"] += 1
            t["gf"] += int(gf)
            t["ga"] += int(ga)
            t["won" if gf > ga else "drawn" if gf == ga else "lost"] += 1
    out = []
    for t in rows.values():
        t["gd"] = t["gf"] - t["ga"]
        t["points"] = 3 * t["won"] + t["drawn"]
        out.append(t)
    out.sort(key=lambda t: (-t["points"], -t["gd"], -t["gf"], t["team"]))
    for i, t in enumerate(out, 1):
        t["pos"] = i
    return out


def recent_results(key: str, season: str, limit: int = 30) -> list[dict]:
    d = _sel(key, season).sort_values("date", ascending=False).head(limit)
    return d[["date", "stage", "home", "away", "home_goals", "away_goals", "shootout_winner"]].to_dict("records")


def team_form(key: str, team: str, n: int = 10) -> dict:
    d = _sel(key)
    d = d[(d.home == team) | (d.away == team)].sort_values("date").tail(n)
    out, pts = [], 0
    for r in d.itertuples():
        gf, ga = (r.home_goals, r.away_goals) if r.home == team else (r.away_goals, r.home_goals)
        res = "W" if gf > ga else "D" if gf == ga else "L"
        pts += {"W": 3, "D": 1, "L": 0}[res]
        out.append(dict(date=r.date, opponent=r.away if r.home == team else r.home, venue="H" if r.home == team else "A", gf=int(gf), ga=int(ga), result=res))
    return dict(team=team, last=out, points=pts, played=len(out))


def head_to_head(key: str, a: str, b: str, limit: int = 10) -> dict:
    d = _sel(key)
    d = d[((d.home == a) & (d.away == b)) | ((d.home == b) & (d.away == a))].sort_values("date", ascending=False)
    wa = wb = dr = 0
    for r in d.itertuples():
        ga, gb = (r.home_goals, r.away_goals) if r.home == a else (r.away_goals, r.home_goals)
        wa += ga > gb
        wb += gb > ga
        dr += ga == gb
    return dict(a=a, b=b, meetings=len(d), a_wins=int(wa), b_wins=int(wb), draws=int(dr),
                last=d.head(limit)[["date", "season", "home", "away", "home_goals", "away_goals"]].to_dict("records"))
