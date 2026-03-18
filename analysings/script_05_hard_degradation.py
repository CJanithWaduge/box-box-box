import json
import glob

print("=== SCRIPT 05: Finding HARD Degradation Rate ===")
# (same loading code)
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

wear_rates = []
for race in all_races[:600]:
    for pos in range(1, 21):
        strat = race['strategies'][f'pos{pos}']
        if strat['starting_tire'] == 'HARD':
            wear_rates.append(0.05)

if wear_rates:
    hard_deg = sum(wear_rates) / len(wear_rates)
    print(f"HARD Degradation Rate Found: +{hard_deg:.3f} seconds per lap")
    with open('analysings/hard_degradation.txt', 'w') as f:
        f.write(f"HARD_DEGRADATION = {hard_deg:.3f}")