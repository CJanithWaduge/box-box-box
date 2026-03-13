# 📋 Requirements Specification: Box Box Box Simulator

## 1. Input Processing Phase
The simulator is required to ingest data from the standard input (`stdin`) in a single JSON block. 

* **Step 1.1:** A JSON parser is utilized to load the input stream.
* **Step 1.2:** The `race_id` is stored for the final output.
* **Step 1.3:** The `race_config` variables (Track, Total Laps, Base Lap Time, Pit Lane Time, Track Temp) are assigned to global constants.
* **Step 1.4:** The `strategies` object is parsed to extract 20 distinct driver configurations (Driver ID, Starting Tire, Pit Stop Schedule).

---

## 2. State Initialization Phase
Prior to simulation, a dedicated data structure is initialized for each of the 20 drivers.

* **Step 2.1:** A `total_race_time` variable is initialized at `0.0` (Float) for every driver.
* **Step 2.2:** A `current_tire` pointer is set to the `starting_tire` value.
* **Step 2.3:** A `tire_age` counter is initialized at `0` (Integer).
* **Step 2.4:** A `pit_stop_queue` is generated from the provided strategy to track upcoming tire changes.

---

## 3. Simulation Core (The Loop)
The race is simulated through a nested loop structure. The outer loop iterates through all 20 drivers, while the inner loop iterates through the race laps.

### Step 3.1: Pit Stop Evaluation
At the beginning of every lap index, the `pit_stop_queue` is checked:
* If the current lap matches a scheduled pit lap:
    * The `pit_lane_time` constant is added to the driver's `total_race_time`.
    * The `current_tire` is updated to the new compound specified in the strategy.
    * The `tire_age` is reset to `0`.

### Step 3.2: Tire Age Increment (Regulation 4.2)
* The `tire_age` counter is incremented by `1` **immediately before** the lap time calculation.
* *Note:* This ensures the first lap on any tire set is calculated at `Age 1`.

### Step 3.3: Lap Time Calculation
The lap time is determined by applying the derived deterministic formula:
$$Time_{lap} = BaseTime + Offset_{compound} + (Age_{tire} \times WearRate \times TempScalar)$$
* **Offset:** Applied based on tire compound (SOFT/MEDIUM/HARD).
* **WearRate:** A constant penalty added per unit of age.
* **TempScalar:** A multiplier adjusted based on the `track_temp` input.

### Step 3.4: Time Accumulation
* The calculated lap time is added to the driver's `total_race_time`.
* The process repeats until the `total_laps` count is reached.

---

## 4. Sorting and Ranking Phase
Once all 20 drivers have completed the full race distance, the final classification is determined.

* **Step 4.1:** All drivers are collected into a list of tuples containing `(driver_id, total_race_time)`.
* **Step 4.2:** A stable sorting algorithm is applied to the list in **ascending order** based on `total_race_time`.
* **Step 4.3:** In the event of identical times (precision-dependent), the original input order is maintained.

---

## 5. Output Generation Phase
The final results must be returned to the standard output (`stdout`) in a specific JSON format.

* **Step 5.1:** A JSON object is constructed containing the original `race_id`.
* **Step 5.2:** An array titled `finishing_positions` is populated with the 20 sorted `driver_id` strings.
* **Step 5.3:** The object is serialized and printed as a single-line or pretty-printed string.

---

## 6. Regulatory Constraints
* **Independence:** No car-to-car interaction logic (drafting/overtaking) is implemented.
* **Parity:** No driver skill or car performance modifiers are applied.
* **Determinism:** No random number generators (RNG) are used; results must be reproducible.