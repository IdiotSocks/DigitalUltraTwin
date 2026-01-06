#!/usr/bin/env python3
"""
Monte Carlo simulation runner for ultra-running race predictions
"""

import random
import numpy as np
import pandas as pd
from typing import List, Dict
from .digital_twin_v32_simulator import DigitalTwinV32, EnvironmentalConditions, NutritionStrategy


def run_monte_carlo_simulations(
    elevation_profile: List[Dict],
    athlete_profile_path: str,
    course_profile_path: str,
    num_simulations: int = 200,
    fitness_range: tuple = (0.95, 1.15),
    temperature_scenarios: List[Dict] = None,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Run Monte Carlo simulations with varying conditions.
    
    Args:
        elevation_profile: Course elevation data
        athlete_profile_path: Path to athlete profile JSON
        course_profile_path: Path to course profile JSON
        num_simulations: Number of scenarios to simulate
        fitness_range: (min, max) fitness levels to test
        temperature_scenarios: Custom temperature scenarios (optional)
        verbose: Print progress updates
        
    Returns:
        DataFrame with simulation results
    """
    simulator = DigitalTwinV32(athlete_profile_path, course_profile_path)
    
    # Default temperature scenarios if not provided
    if temperature_scenarios is None:
        temperature_scenarios = create_default_weather_scenarios()
    
    # Pacing strategies to test
    pacing_strategies = [
        'conservative', 'moderate', 'aggressive', 'even', 'negative_split', 'race_mode'
    ]
    
    results = []
    
    if verbose:
        print(f"Running {num_simulations} Monte Carlo simulations...")
        print("="*80)
    
    for sim in range(num_simulations):
        # Select weather scenario
        weather_scenario = random.choice(temperature_scenarios)
        
        # Randomize parameters
        scenario = {
            'environment': EnvironmentalConditions(
                temperature_celsius=weather_scenario['temp_c'],
                altitude_m=random.uniform(
                    simulator.course_profile['environment_profile']['altitude_band_m'][0],
                    simulator.course_profile['environment_profile']['altitude_band_m'][1]
                ),
                humidity_pct=random.uniform(50, 80),
                wind_speed_kmh=random.uniform(0, 20),
                precipitation=weather_scenario.get('precipitation', 'dry')
            ),
            'nutrition': NutritionStrategy(
                calories_per_hour=random.uniform(250, 290),
                fluid_ml_per_hour=random.uniform(500, 650),
                electrolytes_mg_per_hour=random.uniform(450, 600)
            ),
            'fitness_level': random.uniform(fitness_range[0], fitness_range[1]),
            'pollen_level': random.choice(['low', 'low', 'low', 'medium'])
        }
        
        pacing = random.choice(pacing_strategies)
        
        # Run simulation
        result = simulator.simulate_race(elevation_profile, scenario, pacing)
        
        # Store results
        results.append({
            'Simulation': sim + 1,
            'Pacing Strategy': pacing,
            'Finish Time': result['summary']['total_time_formatted'],
            'Time (hours)': result['summary']['total_time_hours'],
            'Moving Time (hours)': result['summary']['moving_time_hours'],
            'Aid Station Time (min)': result['summary']['aid_station_time_hours'] * 60,
            'Avg Speed (km/h)': result['summary']['average_speed_kmh'],
            'Temperature (°C)': scenario['environment'].temperature_celsius,
            'Precipitation': scenario['environment'].precipitation,
            'Fitness Level': scenario['fitness_level'],
            'Calories/hr': scenario['nutrition'].calories_per_hour,
            'Fluids (ml/hr)': scenario['nutrition'].fluid_ml_per_hour,
            'Pollen Level': scenario['pollen_level'],
            'Respiratory Incidents': result['summary']['respiratory_incidents'],
            'Worst Respiratory': result['summary']['worst_respiratory_impact'],
            'Hiking %': result['summary']['hiking_percentage'],
            'Technical Multiplier': result['summary']['technical_multiplier'],
            'Weather Scenario': weather_scenario['name']
        })
        
        if verbose and (sim + 1) % 50 == 0:
            print(f"Completed {sim + 1}/{num_simulations} simulations...")
    
    if verbose:
        print("="*80)
        print(f"✓ {num_simulations} simulations complete")
    
    return pd.DataFrame(results)


def create_default_weather_scenarios(num_scenarios: int = 200) -> List[Dict]:
    """
    Create default weather scenarios for Monte Carlo simulations.
    
    Args:
        num_scenarios: Number of scenarios to generate
        
    Returns:
        List of weather scenario dictionaries
    """
    scenarios = []
    
    # Typical March conditions (40%)
    for _ in range(int(num_scenarios * 0.4)):
        temp = np.random.normal(11, 2.5)
        scenarios.append({
            'name': 'Typical March',
            'temp_c': max(4, min(16, temp)),
            'precipitation': 'dry' if random.random() > 0.25 else 'light_rain'
        })
    
    # Cold scenarios (20%)
    for _ in range(int(num_scenarios * 0.2)):
        temp = np.random.normal(7, 2)
        scenarios.append({
            'name': 'Cold Day',
            'temp_c': max(2, min(10, temp)),
            'precipitation': 'dry'
        })
    
    # Optimal scenarios (30%)
    for _ in range(int(num_scenarios * 0.3)):
        temp = np.random.normal(14, 1.5)
        scenarios.append({
            'name': 'Optimal',
            'temp_c': max(12, min(16, temp)),
            'precipitation': 'dry'
        })
    
    # Warm scenarios (10%)
    for _ in range(int(num_scenarios * 0.1)):
        temp = np.random.normal(17, 2)
        scenarios.append({
            'name': 'Warm Day',
            'temp_c': max(15, min(20, temp)),
            'precipitation': 'dry'
        })
    
    return scenarios


def analyze_results(results_df: pd.DataFrame, target_min_hours: float = None, target_max_hours: float = None) -> Dict:
    """
    Analyze Monte Carlo simulation results.
    
    Args:
        results_df: DataFrame from run_monte_carlo_simulations
        target_min_hours: Minimum target time (optional)
        target_max_hours: Maximum target time (optional)
        
    Returns:
        Dictionary with analysis statistics
    """
    analysis = {
        'total_simulations': len(results_df),
        'time_statistics': {
            'mean': results_df['Time (hours)'].mean(),
            'median': results_df['Time (hours)'].median(),
            'std': results_df['Time (hours)'].std(),
            'min': results_df['Time (hours)'].min(),
            'max': results_df['Time (hours)'].max(),
            'p10': results_df['Time (hours)'].quantile(0.10),
            'p25': results_df['Time (hours)'].quantile(0.25),
            'p75': results_df['Time (hours)'].quantile(0.75),
            'p90': results_df['Time (hours)'].quantile(0.90),
        },
        'respiratory_statistics': {
            'mean_incidents': results_df['Respiratory Incidents'].mean(),
            'median_incidents': results_df['Respiratory Incidents'].median(),
            'max_incidents': results_df['Respiratory Incidents'].max(),
            'zero_incident_rate': (results_df['Respiratory Incidents'] == 0).sum() / len(results_df)
        },
        'pacing_performance': results_df.groupby('Pacing Strategy')['Time (hours)'].agg(['mean', 'std', 'count']).to_dict(),
        'weather_performance': results_df.groupby('Weather Scenario')['Time (hours)'].agg(['mean', 'std', 'count']).to_dict(),
    }
    
    # Target achievement analysis
    if target_min_hours and target_max_hours:
        in_target = results_df[
            (results_df['Time (hours)'] >= target_min_hours) & 
            (results_df['Time (hours)'] <= target_max_hours)
        ]
        
        analysis['target_achievement'] = {
            'count': len(in_target),
            'success_rate': len(in_target) / len(results_df),
            'mean_fitness_in_target': in_target['Fitness Level'].mean() if len(in_target) > 0 else None,
            'mean_temp_in_target': in_target['Temperature (°C)'].mean() if len(in_target) > 0 else None,
        }
    
    return analysis


if __name__ == "__main__":
    print("Monte Carlo simulation runner module loaded successfully")
