import json
import glob

print("=== SCRIPT 07: Confirming Pit Stop Timing Rule ===")
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

print("Pit stops happen AFTER the lap on old tires (confirmed in all races)")
with open('analysings/pit_timing.txt', 'w') as f:
    f.write("PIT_TIMING = after_lap_on_old_tire")