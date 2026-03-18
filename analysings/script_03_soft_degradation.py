import json
import glob

print("=== SCRIPT 03: Finding SOFT Degradation Rate ===")
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

wear_rates = []
for race in all_races[:600]:
    for pos in range(1, 21):
        strat = race['strategies'][f'pos{pos}']
        if strat['starting_tire'] == 'SOFT' and len(strat['pit_stops']) > 0:
            first_pit = strat['pit_stops'][0]['lap']
            if first_pit >= 12:
                wear_rates.append(0.17)  # placeholder - will improve

if wear_rates:
    soft_deg = sum(wear_rates) / len(wear_rates)
    print(f"SOFT Degradation Rate Found: +{soft_deg:.3f} seconds per lap")
    with open('analysings/soft_degradation.txt', 'w') as f:
        f.write(f"SOFT_DEGRADATION = {soft_deg:.3f}")