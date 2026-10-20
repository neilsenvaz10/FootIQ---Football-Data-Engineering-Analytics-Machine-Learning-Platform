#!/usr/bin/env python3
"""Download targeted StatsBomb open-data files for men's World Cups."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
OUT = ROOT / "data" / "raw" / "statsbomb"
SEASONS = {
    "2018": 3,
    "2022": 106,
}


def download(url: str, path: Path) -> tuple[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return "skipped", str(path)

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "world-cup-model-prototype/0.1"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            path.write_bytes(response.read())
        time.sleep(0.03)
        return "downloaded", str(path)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "missing", str(path)
        return f"http_{exc.code}", str(path)


def main() -> None:
    match_files: list[Path] = []
    for season_name, season_id in SEASONS.items():
        path = OUT / "matches" / "43" / f"{season_id}.json"
        status, target = download(f"{BASE_URL}/matches/43/{season_id}.json", path)
        print(f"{status}: {season_name} matches -> {target}")
        match_files.append(path)

    match_ids: list[int] = []
    for path in match_files:
        with path.open() as handle:
            for match in json.load(handle):
                match_ids.append(int(match["match_id"]))

    jobs: list[tuple[str, Path]] = []
    for match_id in sorted(set(match_ids)):
        jobs.append((f"{BASE_URL}/events/{match_id}.json", OUT / "events" / f"{match_id}.json"))
        jobs.append((f"{BASE_URL}/lineups/{match_id}.json", OUT / "lineups" / f"{match_id}.json"))
        jobs.append((f"{BASE_URL}/three-sixty/{match_id}.json", OUT / "three-sixty" / f"{match_id}.json"))

    counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(download, url, path) for url, path in jobs]
        for future in as_completed(futures):
            status, _ = future.result()
            counts[status] = counts.get(status, 0) + 1

    print(json.dumps(counts, sort_keys=True))
    print(f"matches: {len(match_ids)}")


if __name__ == "__main__":
    main()
