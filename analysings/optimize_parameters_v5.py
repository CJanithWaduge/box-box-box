import json
import glob
import numpy as np
from scipy.optimize import differential_evolution

print("=== PARAMETER OPTIMIZER V5 – Final Refinement ===")

race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

races = all_races[:500]  # 500 races – good balance
print(f"Using {len(races)} historical races")

def lap_time(base, tire, age, temp, params):
    os, oh, ds, dm, dh, tc = params
    offset = {"SOFT": os, "MEDIUM": 0.0, "HARD": oh}
    deg = {"SOFT": ds, "MEDIUM": dm, "HARD": dh}
    return base + offset[tire] + deg[tire] * (age - 1) + tc * (temp - 30)

def total_time(config, strategy, params):
    base = config["base_lap_time"]
    pit = config["pit_lane_time"]
    temp = config["track_temp"]
    laps = config["total_laps"]
    total = 0.0
    tire = strategy["starting_tire"]
    age = 0
    pit_map = {p["lap"]: p["to_tire"] for p in strategy.get("pit_stops", [])}
    for lap in range(1, laps + 1):
        age += 1
        total += lap_time(base, tire, age, temp, params)
        if lap in pit_map:
            total += pit
            tire = pit_map[lap]
            age = 0
    return total

def loss(params):
    errors = 0
    for race in races:
        config = race["race_config"]
        times = []
        for i in range(1, 21):
            strat = race["strategies"][f"pos{i}"]
            t = total_time(config, strat, params)
            times.append((strat["driver_id"], t))
        predicted = [d[0] for d in sorted(times, key=lambda x: x[1])]
        if predicted != race["finishing_positions"]:
            errors += 1
    return errors

# Tighter bounds around V4 best
bounds = [
    (-2.60, -2.45),  # SOFT offset
    (1.75, 1.90),    # HARD offset
    (0.185, 0.205),  # SOFT deg
    (0.050, 0.065),  # MEDIUM deg
    (0.025, 0.040),  # HARD deg
    (0.0030, 0.0060) # temp coeff
]

print("Starting V5 optimization (10–25 min)...")
result = differential_evolution(
    loss,
    bounds,
    workers=1,
    popsize=20,
    maxiter=70,
    tol=0.001,
    mutation=(0.3, 0.8),
    recombination=0.9
)

best_params = result.x
matches = len(races) - result.fun
print(f"\nBest parameters found (V5):")
print(f"SOFT offset:     {best_params[0]:.4f}")
print(f"HARD offset:     {best_params[1]:.4f}")
print(f"SOFT deg:        {best_params[2]:.4f}")
print(f"MEDIUM deg:      {best_params[3]:.4f}")
print(f"HARD deg:        {best_params[4]:.4f}")
print(f"Temp coeff:      {best_params[5]:.4f}")
print(f"Perfect matches: {matches}/{len(races)} ({matches/len(races)*100:.1f}%)")