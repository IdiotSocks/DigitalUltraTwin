"""
Ultra-Running Digital Twin
A Monte Carlo simulation-based model for ultra-running race performance prediction.

Version: 3.3.0
"""

from .digital_twin_v32_simulator import (
    DigitalTwinV32,
    TerrainSegment,
    EnvironmentalConditions,
    NutritionStrategy
)

from .monte_carlo_runner import (
    run_monte_carlo_simulations,
    create_default_weather_scenarios,
    analyze_results
)

__version__ = "3.3.0"
__author__ = "Simbarashe"
__all__ = [
    "DigitalTwinV32",
    "TerrainSegment",
    "EnvironmentalConditions",
    "NutritionStrategy",
    "run_monte_carlo_simulations",
    "create_default_weather_scenarios",
    "analyze_results",
]
