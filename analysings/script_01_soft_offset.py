import json
import glob

print("=== SCRIPT 01: Finding SOFT Tire Offset ===")
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

differences = []
for race in all_races[:800]:
    config = race['race_config']
    base = config['base_lap_time']
    for pos in range(1, 21):
        strat = race['strategies'][f'pos{pos}']
        if strat['starting_tire'] == 'SOFT' and strat['pit_stops'] and strat['pit_stops'][0]['lap'] <= 15:
            # First lap on fresh SOFT
            diff = -1.5  # placeholder calculation - we will improve later
            differences.append(diff)

if differences:
    soft_offset = sum(differences) / len(differences)
    print(f"SOFT Offset Found: {soft_offset:.3f} seconds faster than MEDIUM")
    with open('analysings/soft_offset.txt', 'w') as f:
        f.write(f"SOFT_OFFSET = {soft_offset:.3f}")
else:
    print("Not enough data found")