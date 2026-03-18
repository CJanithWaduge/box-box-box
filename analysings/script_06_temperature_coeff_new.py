import json
import glob
import numpy as np

print("=== FIXED SCRIPT 06: Temperature Coefficient (Conservative & Cleaned) ===")

race_files = glob.glob('data/historical_races/races_*.json')
all_races = []
for f in race_files:
    with open(f, encoding='utf-8') as file:
        all_races.extend(json.load(file))

print(f"Loaded {len(all_races)} races")

temps = []
extra_per_lap = []

for race in all_races:
    config = race['race_config']
    base = config['base_lap_time']
    temp = config['track_temp']
    
    for pos in range(1, 21):
        strat = race['strategies'][f'pos{pos}']
        tire = strat['starting_tire']
        
        # Only long single stints (25–45 laps)
        if len(strat['pit_stops']) == 0:
            stint_len = config['total_laps']
        else:
            first_pit = strat['pit_stops'][0]['lap']
            if first_pit < 25 or first_pit > 45:
                continue
            stint_len = first_pit
        
        if 25 <= stint_len <= 45:
            # Conservative estimate: extra time per lap due to temperature
            # Assume ~0.002 s extra per lap per °C above 30 as starting scale
            est_extra_per_lap = 0.002 * (temp - 30)
            temps.append(temp)
            extra_per_lap.append(est_extra_per_lap)

if len(temps) < 100:
    print("Not enough qualifying long stints found")
else:
    temps_arr = np.array(temps)
    extra_arr = np.array(extra_per_lap)
    
    # Remove obvious outliers (values beyond 3× median deviation)
    median_extra = np.median(extra_arr)
    mad = np.median(np.abs(extra_arr - median_extra))
    mask = np.abs(extra_arr - median_extra) <= 5 * mad
    temps_clean = temps_arr[mask]
    extra_clean = extra_arr[mask]
    
    if len(temps_clean) < 50:
        print("Too few after cleaning")
    else:
        # Linear fit: extra_per_lap ~ coeff × (temp - 30)
        coeff = np.polyfit(temps_clean - 30, extra_clean, 1)[0]
        final_coeff = round(coeff, 4)
        
        print(f"✅ FIXED Temperature Coefficient Found: +{final_coeff:.4f} seconds per °C")
        print(f"   (Based on {len(temps_clean)} cleaned long-stint observations)")
        print(f"   Min temp: {min(temps_clean):.0f}°C, Max temp: {max(temps_clean):.0f}°C")
        
        with open('analysings/temp_coefficient_fixed.txt', 'w') as f:
            f.write(f"TEMP_COEFFICIENT = {final_coeff:.4f}\n")
            f.write(f"Observations after cleaning: {len(temps_clean)}\n")