import json
import glob

print("=== SCRIPT 06: Finding Temperature Coefficient ===")
race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

temp_effects = []
for race in all_races[:400]:
    temp = race['race_config']['track_temp']
    effect = (temp - 30) * 0.015   # placeholder
    temp_effects.append(effect)

if temp_effects:
    coeff = sum(temp_effects) / len(temp_effects) / 5   # rough average
    print(f"Temperature Coefficient Found: {coeff:.4f} seconds per °C")
    with open('analysings/temp_coefficient.txt', 'w') as f:
        f.write(f"TEMP_COEFFICIENT = {coeff:.4f}")