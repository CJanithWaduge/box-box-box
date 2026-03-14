#!/usr/bin/env python3
"""
models/race_car.py - Core RaceCar class for the Box Box Box F1 Race Simulator

The RaceCar class simulates one driver's deterministic progress lap-by-lap.
It composes a Tire instance and accumulates total race time according to
the exact requirements of the challenge.
"""

from typing import List
from models.tire import Tire


class RaceCar:
    """
    Represents a single driver and their tire strategy in the virtual-lane simulation.
    """

    def __init__(
        self,
        driver_id: str,
        starting_compound: str,
        strategy: List[int]
    ) -> None:
        """
        The RaceCar instance is initialised with the required driver identifier,
        starting tire compound and list of planned pit-stop laps.
        The Tire object is created and stored as an attribute for degradation logic.
        """
        # The driver identifier and strategy list are stored directly.
        self.driver_id: str = driver_id
        self.strategy: List[int] = strategy

        # The Tire object is instantiated and assigned as an attribute.
        # This enables compound-specific offset and wear calculations.
        self.tire: Tire = Tire(starting_compound)

        # Cumulative time and current tire age are initialised to zero.
        self.total_time: float = 0.0
        self.tire_age: int = 0

    def run_lap(self, lap_number: int, base_lap_time: float) -> None:
        """
        A single lap is processed for the driver.
        The lap time is calculated, the pit-stop condition is evaluated,
        and the total_time and tire_age are updated accordingly.
        """
        # The current lap time is calculated using the base lap time
        # plus the total delta from the current tire age.
        current_lap_time: float = (
            base_lap_time + self.tire.get_total_delta(self.tire_age)
        )

        # The strategy list is checked to determine whether a pit stop
        # occurs on this lap.
        if lap_number in self.strategy:
            # When a pit stop is triggered, the lap time is added together
            # with the fixed 22.0 s pit-lane penalty and the tire age
            # is reset for the new stint.
            self.total_time += current_lap_time + 22.0
            self.tire_age = 0
        else:
            # When no pit stop occurs, the lap time is added to the cumulative
            # total and the tire age is incremented by one lap.
            self.total_time += current_lap_time
            self.tire_age += 1

    def get_total_time(self) -> float:
        """
        The driver's cumulative race time is returned.
        This value is used by the RaceSimulator to determine finishing order.
        """
        return self.total_time

    def __repr__(self) -> str:
        """A concise string representation of the RaceCar is provided."""
        return (
            f"RaceCar(driver_id='{self.driver_id}', "
            f"compound='{self.tire.compound_type}', "
            f"total_time={self.total_time:.3f}s, "
            f"tire_age={self.tire_age})"
        )