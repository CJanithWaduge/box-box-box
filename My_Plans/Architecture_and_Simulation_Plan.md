# F1 Prediction Engine: A to Z System Architecture & Simulation Plan

## 1. Objective
The primary objective of this phase is the development of an Object-Oriented Programming (OOP) based prediction engine. This engine is designed to forecast race outcomes by calculating the total race duration for each driver, based on track-specific constants, environmental conditions, and strategic variables.

## 2. Mathematical Foundation
The simulation is governed by a deterministic lap-time formula. Each lap time is calculated as follows:

**Formula:**
$$LapTime = BaseTime + O_c + (W_c \times Age) + PitPenalty$$

- **BaseTime:** The fundamental track speed (e.g., 84.5s for Suzuka).
- **$O_c$ (Compound Offset):** The inherent speed delta of a tire compound (e.g., -0.5s for SOFT).
- **$W_c$ (Wear Rate):** The linear degradation coefficient representing the time loss per lap.
- **Age:** The cumulative number of laps completed on the current tire set.
- **PitPenalty:** A fixed temporal penalty of 22 seconds added during a pit stop event.

---

## 3. Object-Oriented Programming (OOP Layered) Structure
The system is partitioned into three core classes to ensure modularity and scalability:

### A. Class: `Tire`
Each tire compound is represented as an object with the following properties:
- **Attributes:** `compound_type`, `offset`, `wear_rate`.
- **Functionality:** The time loss due to degradation is calculated based on the current age of the tire.

### B. Class: `RaceCar`
Individual driver profiles are instantiated as objects to track real-time progress.
- **Attributes:** `driver_id`, `current_tire` (Object), `strategy` (List of pit-stop laps), `total_time`.
- **Functionality:** Cumulative race time is incremented lap-by-lap, accounting for tire aging and strategy execution.

### C. Class: `RaceSimulator`
The orchestration of the entire simulation is managed by this central class.
- **Attributes:** `track_base_time`, `total_laps`, `track_temperature`.
- **Functionality:** Iterative simulation of all drivers over the full race distance is executed, followed by the generation of a final leaderboard based on the lowest aggregate time.

---

## 4. Execution Workflow (The Simulation Loop)
The simulation process is carried out in the following sequential stages:

1. **Initialization:** Track constants, temperature data, and driver strategies are ingested into the system.
2. **Iteration:** A lap-by-lap loop is executed for the entire race duration.
3. **Wear Update:** At the conclusion of each lap, the `Age` attribute is incremented, increasing the time required for the subsequent lap.
4. **Pit Stop Logic:** If a pit stop is scheduled in the driver's strategy, a 22-second penalty is applied, and the tire object is reset (Age = 0).
5. **Final Aggregation:** Upon race completion, total times are compared, and the final finishing positions (P1 to P20) are determined.

## 5. Strategic Value
This architecture allows for the simulation of 'What-if' scenarios. Adjustments to track temperature or pit-stop timing can be made to observe the impact on finishing positions, providing a powerful tool for race strategy optimization.