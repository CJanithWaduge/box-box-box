#!/usr/bin/env python3
"""
scripts/race_simulator.py - Final orchestrator for the Box Box Box F1 Race Simulator

The RaceSimulator class manages multiple RaceCar instances and executes
the full deterministic lap-by-lap race simulation.
"""

from typing import List
from models.race_car import RaceCar


class RaceSimulator:
    """
    Orchestrates the complete race for all drivers using virtual-lane logic.
    """

    def __init__(
        self,
        track_name: str,
        total_laps: int,
        base_lap_time: float
    ) -> None:
        """
        The simulator is initialised with track details and the base lap time.
        The drivers list is initialised as empty.
        """
        # The track identifier, total race distance and base lap time
        # are stored for use during simulation.
        self.track_name: str = track_name
        self.total_laps: int = total_laps
        self.base_lap_time: float = base_lap_time

        # The list of participating RaceCar objects is prepared.
        self.drivers: List[RaceCar] = []

    def add_driver(self, race_car_object: RaceCar) -> None:
        """
        The supplied RaceCar instance is appended to the drivers list.
        """
        # The driver is registered for the simulation.
        self.drivers.append(race_car_object)

    def run_race(self) -> None:
        """
        The full race is executed lap by lap for every driver.
        """
        # Every lap from 1 to total_laps is processed sequentially.
        # For each lap the run_lap method is invoked on all drivers
        # with the current base lap time.
        for lap in range(1, self.total_laps + 1):
            for driver in self.drivers:
                driver.run_lap(lap, self.base_lap_time)

    def display_results(self) -> None:
        """
        The drivers are sorted by cumulative time and the leaderboard
        is printed in the required format.
        """
        # The drivers are sorted in ascending order of total_time
        # (lowest time = first place).
        sorted_drivers: List[RaceCar] = sorted(
            self.drivers, key=lambda car: car.get_total_time()
        )

        # The formatted leaderboard is displayed.
        print(f"\n=== {self.track_name} Race Results ===")
        print(f"{'Rank':<5} {'Driver ID':<12} {'Total Time (s)':<15}")
        print("-" * 40)
        for rank, car in enumerate(sorted_drivers, start=1):
            print(
                f"{rank:<5} {car.driver_id:<12} "
                f"{car.get_total_time():.3f}"
            )


if __name__ == "__main__":
    """
    A complete sample race is demonstrated as required.
    Suzuka circuit, 50 laps, base lap time of 84.5 s.
    Three drivers with different compounds and pit strategies.
    """
    # A simulator instance is created for the demonstration race.
    sim = RaceSimulator(
        track_name="Suzuka",
        total_laps=50,
        base_lap_time=84.5
    )

    # Three drivers with contrasting strategies are instantiated
    # and added to the simulation.
    driver1 = RaceCar("HAM", "SOFT", [18])          # one early stop
    driver2 = RaceCar("VER", "MEDIUM", [22, 42])    # two stops
    driver3 = RaceCar("LEC", "HARD", [])            # no stops

    sim.add_driver(driver1)
    sim.add_driver(driver2)
    sim.add_driver(driver3)

    # The race is simulated.
    sim.run_race()

    # The final leaderboard is displayed.
    sim.display_results()