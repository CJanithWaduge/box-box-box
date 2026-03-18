import json
import glob
import numpy as np
from scipy.optimize import differential_evolution

print("=== PARAMETER OPTIMIZER ===")

# Load some historical races (500 is good balance)
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))
races = all_races[:500]
print(f"Using {len(races)} historical races for tuning")

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

bounds = [
    (-2.5, -1.2),  # SOFT offset
    (1.2, 2.5),    # HARD offset
    (0.12, 0.22),  # SOFT deg
    (0.06, 0.12),  # MEDIUM deg
    (0.03, 0.08),  # HARD deg
    (0.0005, 0.005) # temp coeff (small range around your last value)
]

print("Starting optimization (takes 5–15 minutes)...")
result = differential_evolution(loss, bounds, workers=1, popsize=15, maxiter=40)

best_params = result.x
matches = len(races) - result.fun
print(f"\nBest parameters found:")
print(f"SOFT offset:     {best_params[0]:.4f}")
print(f"HARD offset:     {best_params[1]:.4f}")
print(f"SOFT deg:        {best_params[2]:.4f}")
print(f"MEDIUM deg:      {best_params[3]:.4f}")
print(f"HARD deg:        {best_params[4]:.4f}")
print(f"Temp coeff:      {best_params[5]:.4f}")
print(f"Matches:         {matches}/{len(races)} ({matches/len(races)*100:.1f}%)")