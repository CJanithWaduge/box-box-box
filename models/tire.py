#!/usr/bin/env python3
"""
models/tire.py - Core Tire class for the Box Box Box F1 Race Simulator

The Tire class encapsulates the performance characteristics and degradation
behaviour of each tire compound. It is designed for direct integration with
the RaceCar class in a deterministic lap-by-lap simulation.
"""

from typing import Literal

VALID_COMPOUNDS: set[str] = {"SOFT", "MEDIUM", "HARD"}


class Tire:
    """
    Represents a single tire compound with its offset and wear rate.
    """

    def __init__(self, compound_type: Literal["SOFT", "MEDIUM", "HARD"]) -> None:
        """
        The tire is instantiated with a validated compound type.
        The offset (O_c) and wear rate (W_c) are assigned based on
        the compound as defined in the reverse-engineered model.
        """
        # The compound type is validated to ensure only permitted values
        # are accepted (prevents downstream simulation errors).
        if compound_type not in VALID_COMPOUNDS:
            raise ValueError(
                f"The compound '{compound_type}' is invalid. "
                f"Only SOFT, MEDIUM, or HARD are permitted."
            )

        self.compound_type: Literal["SOFT", "MEDIUM", "HARD"] = compound_type

        # The offset and wear rate constants are assigned according to
        # the compound-specific values derived from historical analysis.
        if compound_type == "SOFT":
            self.offset: float = -0.5
            self.wear_rate: float = 0.08
        elif compound_type == "MEDIUM":
            self.offset: float = 0.0
            self.wear_rate: float = 0.05
        else:  # HARD
            self.offset: float = 0.8
            self.wear_rate: float = 0.03

    def get_total_delta(self, age: int) -> float:
        """
        The total time delta for the current tire age is calculated.
        Formula: Total Delta = Offset + (Wear Rate × Age)
        This value is added to the base lap time in the simulation.
        """
        # The degradation penalty is computed deterministically using
        # the pre-assigned offset and per-lap wear rate.
        return self.offset + (self.wear_rate * age)

    def __repr__(self) -> str:
        """The tire is represented in a concise, readable format."""
        return (
            f"Tire(compound='{self.compound_type}', "
            f"offset={self.offset:+.1f}s, "
            f"wear_rate={self.wear_rate:.2f}s/lap)"
        )