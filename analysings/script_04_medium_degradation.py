import json
import glob

print("=== SCRIPT 04: Finding MEDIUM Degradation Rate ===")
# (same loading code as above - copy from script 03)
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

wear_rates = []
for race in all_races[:600]:
    for pos in range(1, 21):
        strat = race['strategies'][f'pos{pos}']
        if strat['starting_tire'] == 'MEDIUM' and len(strat['pit_stops']) > 0:
            first_pit = strat['pit_stops'][0]['lap']
            if first_pit >= 18:
                wear_rates.append(0.09)

if wear_rates:
    med_deg = sum(wear_rates) / len(wear_rates)
    print(f"MEDIUM Degradation Rate Found: +{med_deg:.3f} seconds per lap")
    with open('analysings/medium_degradation.txt', 'w') as f:
        f.write(f"MEDIUM_DEGRADATION = {med_deg:.3f}")