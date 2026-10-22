"""World Cup simulation: thin wrapper around the existing v2.13 simulator (scripts/simulate_live_tournament_v213.py).

The simulator is the v2.3 team-power / Monte Carlo engine with completed results locked. It is NOT the v2.7 match ensemble.
This wrapper never writes files (the simulator's own main() does; it is not called). Must run with `python -X utf8` on Windows.
"""
import sys
import time

import config as C

SCRIPTS = C.ROOT / "scripts"
DEFAULT_SIMS = 5000
MAX_SIMS = 50000   # the simulator's own default


class SimulationError(RuntimeError):
    pass


def run(simulations: int = DEFAULT_SIMS) -> dict:
    if not sys.flags.utf8_mode:
        raise SimulationError("start Python with `-X utf8` (the existing simulator reads CSVs with the Windows default encoding otherwise)")
    simulations = max(100, min(int(simulations), MAX_SIMS))
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import simulate_live_tournament_v213 as sim

    original = sim.V213_CONFIG["simulations"]
    sim.V213_CONFIG["simulations"] = simulations
    t = time.time()
    try:
        rows, metadata, group_tables, resolved_r32 = sim.run_live_tournament()
    finally:
        sim.V213_CONFIG["simulations"] = original
    return dict(
        simulations=simulations, seconds=round(time.time() - t, 1), seed=sim.V213_CONFIG["seed"], engine=sim.V213_CONFIG["base_engine"],
        note="Tournament state is the archived 2026 state held in the repo (completed results locked), not live odds. "
             "The team-power engine is separate from the v2.7 match model.",
        metadata=metadata,
        title_odds=[{k: r[k] for k in ("live_title_rank", "team", "group", "qualify_knockout_pct", "round_of_16_pct", "quarter_final_pct",
                                         "semi_final_pct", "final_pct", "champion_pct") if k in r} for r in rows],
        group_tables={g: [{k: t_[k] for k in ("team", "played", "points", "goal_diff", "goals_for") if k in t_} for t_ in tab] for g, tab in group_tables.items()},
    )
