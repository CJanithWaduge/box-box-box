#!/usr/bin/env python3
"""
Box Box Box - F1 Race Simulator
Final version with exact total race time calculation (10+ decimal precision)
"""

import json
import sys


# ========================== V5 BEST PARAMETERS ==========================
TIRE_OFFSET = {
    "SOFT":   -2.4843,
    "MEDIUM":  0.0000,
    "HARD":    1.8397
}

TIRE_DEGRADATION = {
    "SOFT":   0.1851,
    "MEDIUM": 0.0519,
    "HARD":   0.0262
}

TEMP_COEFFICIENT = 0.0051


def calculate_lap_time(base_lap_time: float, tire: str, age: int, track_temp: int) -> float:
    """
    Calculates exact lap time with 15+ decimal precision (Python float).
    """
    offset = TIRE_OFFSET[tire]
    degradation = TIRE_DEGRADATION[tire] * (age - 1)
    temp_effect = TEMP_COEFFICIENT * (track_temp - 30)

    return base_lap_time + offset + degradation + temp_effect


def simulate_driver_total_time(race_config: dict, strategy: dict) -> float:
    """
    Simulates the entire race for one driver and returns total race time
    with full floating-point precision.
    """
    base = race_config["base_lap_time"]
    pit_time = race_config["pit_lane_time"]
    temp = race_config["track_temp"]
    total_laps = race_config["total_laps"]

    total_time = 0.0
    current_tire = strategy["starting_tire"]
    current_age = 0

    # Create fast lookup for pit stops
    pit_laps = {stop["lap"]: stop["to_tire"] for stop in strategy["pit_stops"]}

    for lap in range(1, total_laps + 1):
        current_age += 1
        lap_time = calculate_lap_time(base, current_tire, current_age, temp)
        total_time += lap_time

        # Pit stop happens AFTER completing the lap
        if lap in pit_laps:
            total_time += pit_time
            current_tire = pit_laps[lap]
            current_age = 0

    return total_time


def main():
    # Read input from stdin (exactly as test_runner expects)
    test_case = json.load(sys.stdin)

    race_id = test_case["race_id"]
    race_config = test_case["race_config"]
    strategies = test_case["strategies"]

    # Calculate exact total race time for all 20 drivers
    driver_results = []

    for i in range(1, 21):
        pos_key = f"pos{i}"
        strategy = strategies[pos_key]
        total_time = simulate_driver_total_time(race_config, strategy)
        driver_results.append((strategy["driver_id"], total_time))

    # Sort by total race time (lowest time = 1st place)
    driver_results.sort(key=lambda x: x[1])

    # Extract only driver IDs in finishing order
    finishing_positions = [driver_id for driver_id, _ in driver_results]

    # Output in exact required format
    output = {
        "race_id": race_id,
        "finishing_positions": finishing_positions
    }

    print(json.dumps(output))


if __name__ == "__main__":
    main()