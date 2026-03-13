# 🏎️ Comprehensive Strategic Roadmap: Box Box Box F1 Simulator

**Project Objective:** To develop a 100% deterministic, independent-lane F1 race simulation engine in Python. The engine must reverse-engineer hidden telemetry constants (tire wear, temperature coefficients, compound offsets) from 30,000 historical data points and use them to accurately predict the exact 1st–20th finishing order for 100 blind test cases.

---

## Phase 1: Environment Setup & Requirement Audit
**Goal:** Establish a stable development environment and completely map out the system constraints based on official documentation.

* **Task 1.1: Workspace Initialization**
    * Create project directory: `box-box-box-f1`.
    * Initialize a Python Virtual Environment (`python -m venv venv`) to isolate dependencies.
    * Create standard SE directory structure: `/data`, `/docs`, `/solution`, `/scripts`.
* **Task 1.2: Regulatory Deep-Dive**
    * Audit `PROBLEM_STATEMENT.md` and `regulations.md`.
    * *Crucial Findings to Enforce:* 1. No car-to-car interaction (simulations are 20 isolated time-trials).
        2. Equal driver/car parity (only tire strategy changes the outcome).
        3. Tire age MUST increment *before* lap calculation (Lap 1 on fresh tires = Age 1).
* **Task 1.3: I/O Pipeline Setup**
    * Create a dummy `race_simulator.py` script that reads a JSON from `stdin` and safely parses it using Python's `sys.stdin.read()` and `json.loads()`.
* **Deliverable:** A running Python environment capable of reading test cases without crashing.

---

## Phase 2: Data Mining & Reverse Engineering (The Core Challenge)
**Goal:** We have the inputs and the final answers in the 30,000 historical races. We must write analytical scripts to extract the exact floating-point constants used by the judges' hidden formula.

* **Task 2.1: Build the Data Extraction Script (`scripts/analyzer.py`)**
    * Write a Python script to iterate through `races_00000-01999.json`.
    * Calculate the exact lap-by-lap times by reverse-calculating the final total times based on strategy. (Since cars don't interact, we can deduce lap times if we isolate specific stints).
* **Task 2.2: Isolate Compound Offsets ($O_c$)**
    * *Method:* Find races with the exact same `track`, `track_temp`, and `base_lap_time`. Compare a driver starting on **SOFT** vs a driver starting on **MEDIUM** vs **HARD**.
    * *Output:* Exact time difference (in seconds) between the three compounds.
* **Task 2.3: Isolate Base Degradation Rate ($D$)**
    * *Method:* Look at a single driver's stint on a specific compound. Calculate the time difference between Lap 1 (Age 1) and Lap 2 (Age 2). 
    * *Output:* The constant floating-point value that represents seconds lost per lap of tire age.
* **Task 2.4: Isolate Temperature Coefficient ($S_t$)**
    * *Method:* Find two races on the *same track* with the *same strategies*, but different `track_temp` values. Measure how the Degradation Rate changes per degree Celsius.
    * *Output:* The multiplier formula for `track_temp`.
* **Deliverable:** A documented list of exact mathematical constants required to build the engine.

---

## Phase 3: Simulator Engine Implementation
**Goal:** Build the actual production code that will be evaluated by the `test_runner.sh`.

* **Task 3.1: Architecture Layout (`solution/race_simulator.py`)**
    * Implement the main `simulate_race(race_data)` function.
    * Create a state-tracking dictionary for all 20 drivers: `total_time` (float), `current_tire` (string), `tire_age` (integer).
* **Task 3.2: The Core Simulation Loop**
    * Loop 1: `for driver in strategies:` (Process all 20 drivers one by one).
    * Loop 2: `for lap in range(1, total_laps + 1):`
* **Task 3.3: Pit Stop & Age Logic**
    * *Step A:* Check if the current lap exists in the driver's `pit_stops` array.
    * *Step B:* If True -> Add `pit_lane_time` to `total_time`, update `current_tire`, and set `tire_age = 0`.
    * *Step C:* Increment `tire_age += 1` (Fulfilling the "Age 1" regulation).
* **Task 3.4: Time Calculation & Accumulation**
    * Apply the reverse-engineered formula: 
        `Lap Time = base_lap_time + Compound_Offset + (tire_age * Degradation * Temp_Multiplier)`
    * Add `Lap Time` to the driver's `total_time`.
* **Task 3.5: Sorting and Output formatting**
    * Sort the 20 drivers based on their final `total_time` in ascending order.
    * Construct the final JSON object: `{"race_id": "...", "finishing_positions": ["D001", ...]}`.
    * Print to `sys.stdout` using `json.dumps()`.
* **Deliverable:** A fully functional simulation script.

---

## Phase 4: Calibration, Testing & QA
**Goal:** Ensure the simulator hits 100% accuracy against the provided test cases.

* **Task 4.1: Unit Testing**
    * Pipe `test_001.json` into the script: `cat data/test_cases/inputs/test_001.json | python solution/race_simulator.py`.
    * Compare the output string strictly against `data/test_cases/expected_outputs/test_001.json`.
* **Task 4.2: Float Precision Calibration**
    * *Risk:* Floating-point math in Python can cause microscopic rounding errors (e.g., `82.0000000001` vs `81.9999999999`).
    * *Fix:* Implement Python's `round(time, 4)` at the final stage before sorting if drivers have incredibly close finish times, or ensure the constants derived in Phase 2 have high precision.
* **Task 4.3: Batch Testing**
    * Execute `./test_runner.sh` (using Git Bash or WSL).
    * Review the console output to check the percentage score (Target: >95%).
    * Debug specific failed test cases by printing lap-by-lap logs to `stderr` (which won't break the JSON output expectation).
* **Deliverable:** A verified 100% pass rate on local testing.

---

## Phase 5: Finalization & Deployment
**Goal:** Prepare the codebase for final evaluation and submission.

* **Task 5.1: Code Cleanup (Refactoring)**
    * Remove all `print()` debugging statements.
    * Ensure all variables use clean, PEP-8 standard naming conventions (e.g., `calculate_lap_time`, `driver_id`).
    * Add docstrings to all functions explaining the mathematical logic.
* **Task 5.2: Run Command Configuration**
    * Ensure `solution/run_command.txt` strictly contains exactly: `python solution/race_simulator.py`.
* **Task 5.3: Final Submission Check**
    * Review `SUBMISSION_GUIDE.md` one last time.
    * Zip the contents / Push to the remote repository as instructed.
* **Deliverable:** Final, production-ready codebase deployed successfully.