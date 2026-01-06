#!/usr/bin/env python3
"""
Sensitivity Analysis Example

Test how different parameters affect race predictions.
"""

import sys
import json
import pandas as pd
sys.path.append('..')

from src.digital_twin_v32_simulator import DigitalTwinV32, EnvironmentalConditions, NutritionStrategy


def main():
    print("="*80)
    print("PARAMETER SENSITIVITY ANALYSIS")
    print("="*80)
    
    # Load profile
    with open('../data/elevation/chianti_elevation_profile.json', 'r') as f:
        elevation_profile = json.load(f)['profile']
    
    simulator = DigitalTwinV32(
        '../data/profiles/simbarashe_enhanced_profile_v3_3.json',
        '../data/courses/chianti_74k_course_profile_v1_3_FINAL.json'
    )
    
    # Test 1: Fitness sensitivity
    print("\n1. FITNESS LEVEL SENSITIVITY")
    print("-" * 80)
    fitness_results = []
    
    for fitness in [1.0, 1.05, 1.10, 1.15, 1.20, 1.25]:
        scenario = {
            'environment': EnvironmentalConditions(temperature_celsius=14),
            'nutrition': NutritionStrategy(),
            'fitness_level': fitness
        }
        result = simulator.simulate_race(elevation_profile, scenario, 'even')
        fitness_results.append({
            'fitness': fitness,
            'time_hours': result['summary']['total_time_hours'],
            'speed_kmh': result['summary']['average_speed_kmh']
        })
        print(f"   Fitness {fitness:.2f}: {result['summary']['total_time_formatted']} "
              f"({result['summary']['average_speed_kmh']:.2f} km/h)")
    
    # Test 2: Temperature sensitivity
    print("\n2. TEMPERATURE SENSITIVITY")
    print("-" * 80)
    temp_results = []
    
    for temp in [6, 8, 10, 12, 14, 16, 18, 20]:
        scenario = {
            'environment': EnvironmentalConditions(temperature_celsius=temp),
            'nutrition': NutritionStrategy(),
            'fitness_level': 1.15
        }
        result = simulator.simulate_race(elevation_profile, scenario, 'even')
        temp_results.append({
            'temperature': temp,
            'time_hours': result['summary']['total_time_hours'],
            'resp_incidents': result['summary']['respiratory_incidents']
        })
        print(f"   {temp:2d}°C: {result['summary']['total_time_formatted']} "
              f"({result['summary']['respiratory_incidents']} resp incidents)")
    
    # Test 3: Pacing strategy sensitivity
    print("\n3. PACING STRATEGY SENSITIVITY")
    print("-" * 80)
    pacing_results = []
    
    strategies = ['conservative', 'moderate', 'even', 'aggressive', 'race_mode']
    scenario = {
        'environment': EnvironmentalConditions(temperature_celsius=14),
        'nutrition': NutritionStrategy(),
        'fitness_level': 1.15
    }
    
    for pacing in strategies:
        result = simulator.simulate_race(elevation_profile, scenario, pacing)
        pacing_results.append({
            'pacing': pacing,
            'time_hours': result['summary']['total_time_hours']
        })
        print(f"   {pacing:15s}: {result['summary']['total_time_formatted']}")
    
    # Summary
    print("\n" + "="*80)
    print("KEY FINDINGS")
    print("="*80)
    
    # Fitness impact
    fitness_df = pd.DataFrame(fitness_results)
    time_range = fitness_df['time_hours'].max() - fitness_df['time_hours'].min()
    print(f"\n📊 FITNESS IMPACT:")
    print(f"   Range (1.0 to 1.25): {time_range:.2f} hours")
    print(f"   Per 0.05 fitness: ~{time_range/5:.2f} hours")
    
    # Temperature impact
    temp_df = pd.DataFrame(temp_results)
    cold_time = temp_df[temp_df['temperature'] == 8]['time_hours'].iloc[0]
    optimal_time = temp_df[temp_df['temperature'] == 14]['time_hours'].iloc[0]
    temp_penalty = cold_time - optimal_time
    print(f"\n🌡️  TEMPERATURE IMPACT:")
    print(f"   8°C vs 14°C: +{temp_penalty*60:.0f} minutes")
    print(f"   Optimal range: 12-16°C")
    
    # Pacing impact
    pacing_df = pd.DataFrame(pacing_results)
    best_pacing = pacing_df.loc[pacing_df['time_hours'].idxmin()]
    worst_pacing = pacing_df.loc[pacing_df['time_hours'].idxmax()]
    print(f"\n🏃 PACING IMPACT:")
    print(f"   Best: {best_pacing['pacing']} ({best_pacing['time_hours']:.2f}h)")
    print(f"   Worst: {worst_pacing['pacing']} ({worst_pacing['time_hours']:.2f}h)")
    print(f"   Difference: {(worst_pacing['time_hours'] - best_pacing['time_hours'])*60:.0f} minutes")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
