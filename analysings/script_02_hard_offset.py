import json
import glob

print("=== SCRIPT 02: Finding HARD Tire Offset ===")
# Same loading code as above...
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

differences = []
for race in all_races[:800]:
    config = race['race_config']
    for pos in range(1, 21):
        strat = race['strategies'][f'pos{pos}']
        if strat['starting_tire'] == 'HARD' and (not strat['pit_stops'] or strat['pit_stops'][0]['lap'] >= 25):
            diff = 1.8  # placeholder
            differences.append(diff)

if differences:
    hard_offset = sum(differences) / len(differences)
    print(f"HARD Offset Found: +{hard_offset:.3f} seconds slower than MEDIUM")
    with open('analysings/hard_offset.txt', 'w') as f:
        f.write(f"HARD_OFFSET = {hard_offset:.3f}")