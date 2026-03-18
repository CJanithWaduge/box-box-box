# Box Box Box – F1 Race Strategy Prediction Challenge  
**Documentation**

## Objective
The challenge required prediction of finishing positions for 20 drivers in unseen test races. Predictions were to be based solely on provided race configurations and tire strategies. The underlying simulation logic was not disclosed and had to be reverse-engineered from 30,000 historical races.

## Data Understanding & Initial Exploration
Historical race data consisting of 30,000 complete records was examined. Each record contained race configuration parameters (track, total laps, base lap time, pit lane time, track temperature), driver strategies (starting tire compound, pit stop schedule), and actual finishing positions.

Initial analysis scripts were developed to extract recurring patterns:
- Distribution of starting tire compounds
- Typical stint lengths per compound
- Correlation between strategy choices and final positions
- Influence of track temperature on outcomes

Patterns indicated that SOFT compounds produced faster early laps but rapid degradation, while HARD compounds offered durability at the cost of pace. Temperature appeared to modulate degradation behavior.

## Reverse-Engineering of the Simulation Model
The simulation was determined to be purely time-based with no driver interaction or random elements. Total race time for each driver was concluded to be the sum of individual lap times plus pit-lane penalties.

The lap-time equation was hypothesized as follows:

lap_time = base_lap_time  
         + tire_offset[tire]  
         + tire_degradation[tire] × (tire_age − 1)  
         + temperature_coefficient × (track_temp − 30)

Pit-lane time was applied after completion of the specified pit lap (on old tires), after which tire compound and age were reset.

## Parameter Discovery Process
Seven unknown parameters were identified:

1. Offset for SOFT compound  
2. Offset for HARD compound  
3. Degradation rate for SOFT  
4. Degradation rate for MEDIUM  
5. Degradation rate for HARD  
6. Temperature coefficient  
7. Pit timing rule (confirmed as post-lap application)

Dedicated analysis scripts were created for initial estimates:

- Separate scripts calculated offsets and degradation rates using first-lap comparisons and linear regression on long stints.
- Temperature coefficient was estimated via regression on average lap-time differences in long-stint races across temperature ranges.

Iterative global optimization was performed using differential evolution (scipy.optimize):

- Multiple versions (V1–V5) were executed with progressively tighter bounds and refined starting points.
- Objective function minimized the number of mismatches between predicted and actual finishing orders across sampled historical races.
- Best result achieved: 40 perfect matches out of 500 races (8.0%).

Final parameters used for submission:

- SOFT offset: −2.4843  
- HARD offset: +1.8397  
- SOFT degradation: 0.1851 s/lap  
- MEDIUM degradation: 0.0519 s/lap  
- HARD degradation: 0.0262 s/lap  
- Temperature coefficient: 0.0051 s/°C

## Simulator Implementation
A deterministic lap-by-lap simulator was implemented in `solution/race_simulator.py`:

- Input read from stdin in JSON format  
- Each driver simulated independently  
- Lap times calculated with full floating-point precision  
- Pit stops applied after the designated lap  
- Drivers sorted by total race time  
- Output written to stdout as required JSON structure

## Local Validation & Testing
A custom comparison script (`test_compare.py`) was developed to:

- Execute the simulator against each test input  
- Compare predicted and expected finishing positions  
- Report per-test accuracy (correct positions out of 20)  
- Calculate final score as percentage of races with perfect 20/20 match

Latest run with V5 parameters produced 3/100 full matches (3.0%).

## File Structure

box-box-box/
├── analysings/-------------------->Analysis & optimization scripts
│   ├── discover_patterns.py
│   ├── script_01_* ... script_07_*
│   └── optimize_parameters_v*.py
├── solution/
│   ├── race_simulator.py---------->Main submission
│   └── run_command.txt
├── test_compare.py---------------->Local validation tool
├── data/-------------------------->Provided dataset (not included in repo)
└── README.md / PROJECT_DOCUMENTATION.md


## Technologies & Libraries Used

- Python 3  
- json (standard library)  
- numpy, scipy (optimization & numerical computation)  
- glob, pathlib (file handling)

## Observations

- Tire compound choice and stint length were found to be the dominant factors.  
- Degradation rates followed expected hierarchy: SOFT > MEDIUM > HARD.  
- Temperature effect was small but consistently positive.  
- Full-order matching remained challenging due to accumulation of small timing differences.  
- Iterative refinement steadily increased historical match rate.

Project completed and submitted within the allotted time frame.