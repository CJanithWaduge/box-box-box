# 📑 Algorithm Specification: Deterministic Race Engine

## 1. Mathematical Foundation
A deterministic linear model is utilized to calculate race outcomes. Since no car-to-car interaction exists, the total race time is derived from the sum of discrete lap times and pit lane penalties.

### 1.1 The Lap Time Formula
For any given lap, the lap time is calculated using the following formula:

**Lap Time = Base Lap Time + Compound Offset + (Tire Age × Wear Rate × Thermal Scalar)**

**Parameter Definitions:**

| Parameter | Name | Description |
|-----------|------|------------|
| **Lap Time** | Lap Time | The total time (in seconds) for completing the current lap |
| **Base Lap Time** | Base Lap Time | The baseline track speed provided in the input data |
| **Compound Offset** | Tire Compound Offset | Constant time penalty or bonus based on tire type (SOFT, MEDIUM, or HARD) |
| **Tire Age** | Tire Age | How many laps the current tire set has been used |
| **Wear Rate** | Tire Wear Rate | How many seconds are lost per lap due to tire degradation (specific to each compound) |
| **Thermal Scalar** | Temperature Multiplier | A multiplier based on track temperature that increases or decreases tire wear |

---

## 2. Step-by-Step Execution Logic

### Step 1: Data Ingestion and Preparation
1.  The JSON payload is read from `stdin`.
2.  Global race constants (`base_lap_time`, `pit_lane_time`, `track_temp`) are extracted.
3.  A collection of 20 driver strategy objects is initialized.

### Step 2: Driver-Specific Initialization
For each of the 20 drivers, a state-tracking record is created:
1.  The `total_race_time` is initialized to `0.0`.
2.  The `current_tire` is assigned from the `starting_tire` field.
3.  The `tire_age` is set to `0`.
4.  A mapping of pit stop laps and their corresponding `to_tire` compounds is stored.

### Step 3: The Lap Simulation Loop
The simulation proceeds through a loop from Lap 1 to the `total_laps` value:

**3.1 Pit Stop Check:**
* At the start of the lap, the pit stop schedule is checked.
* If a pit stop is scheduled for the current lap index:
    * The `pit_lane_time` is added to the `total_race_time`.
    * The `current_tire` is updated to the new compound.
    * The `tire_age` is reset to `0`.

**3.2 Tire Age Increment (Regulation 4.2):**
* The `tire_age` is incremented by `1`.
* *Implementation Note:* This ensures that Lap 1 (or the first lap after a pit stop) is always calculated with an age of `1`.

**3.3 Calculation and Accumulation:**
* The lap time is calculated using the formula defined in Section 1.1.
* The resulting value is added to the `total_race_time`.

### Step 4: Final Classification
1.  After all laps are completed for all drivers, the list of drivers is sorted.
2.  An **ascending sort** is performed based on the `total_race_time` (the lowest time occupies the 1st position).
3.  The `driver_id` values are extracted in their sorted order into a flat array.

---

## 3. Parameter Derivation (Reverse Engineering)
The following constants are required for the formula to function. These are derived from the historical dataset provided in `data/historical_races/`:

| Parameter | Derivation Method |
| :--- | :--- |
| **Compound Offset** | Isolated by comparing Lap 1 times of different compounds on the same track at the same temperature. |
| **Wear Rate** | Calculated by measuring the difference between consecutive lap times (for example: Time of Lap 2 - Time of Lap 1) on a single tire stint. |
| **Thermal Scalar** | Identified by analyzing how wear rate increases across different races at the same track with varying track temperatures. |

---

## 4. Complexity and Precision
* **Time Complexity:** The algorithm processes each of 20 drivers through all laps. The complexity scales as: 20 drivers × Number of laps. So if there are 50 laps, the algorithm performs roughly 1,000 operations.
* **Numerical Precision:** All time-based calculations are maintained as high-precision floating-point numbers. No rounding is applied to intermediate lap times to prevent cumulative drift.