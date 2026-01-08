#!/usr/bin/env python3
"""
Basic Race Prediction Example

This example shows how to run a simple single-race prediction using the digital twin.
"""

import sys
import json
sys.path.append('..')

from src.digital_twin_v32_simulator import DigitalTwinV32, EnvironmentalConditions, NutritionStrategy


def main():
    print("="*80)
    print("BASIC RACE PREDICTION EXAMPLE")
    print("="*80)
    
    # Load elevation profile
    print("\n1. Loading elevation profile...")
    with open('../data/elevation/chianti_elevation_profile.json', 'r') as f:
        profile_data = json.load(f)
        elevation_profile = profile_data['profile']

    print(f"   ✓ Loaded: {profile_data['total_distance_km']:.1f} km, "
          f"{profile_data['total_elevation_gain_m']:.0f}m gain")
    
    # Initialize simulator
    print("\n2. Initializing Digital Twin simulator...")
    simulator = DigitalTwinV32(
        athlete_profile_path='../data/profiles/simbarashe_enhanced_profile_v3_3.json',
        course_profile_path='../data/courses/chianti_74k_course_profile_v1_3_FINAL.json'
    )
    print("   ✓ Simulator initialized")
    
    # Define scenario
    print("\n3. Setting up race scenario...")
    scenario = {
        'environment': EnvironmentalConditions(
            temperature_celsius=14,  # Optimal temperature
            altitude_m=400,          # Average altitude
            humidity_pct=60,
            precipitation='dry'
        ),
        'nutrition': NutritionStrategy(
            calories_per_hour=270,   # Aggressive fueling
            fluid_ml_per_hour=550,   # Adequate hydration
            electrolytes_mg_per_hour=500
        ),
        'fitness_level': 1.15       # Arc 2025 fitness level
    }
    
    print(f"   ✓ Temperature: {scenario['environment'].temperature_celsius}°C")
    print(f"   ✓ Fitness level: {scenario['fitness_level']}")
    
    # Run simulation
    print("\n4. Running race simulation...")
    result = simulator.simulate_race(
        elevation_profile=elevation_profile,
        scenario=scenario,
        pacing_strategy='race_mode'
    )
    print("   ✓ Simulation complete")
    
    # Display results
    print("\n" + "="*80)
    print("RACE PREDICTION RESULTS")
    print("="*80)
    
    print(f"\n📊 FINISH TIME: {result['summary']['total_time_formatted']}")
    print(f"   Total time: {result['summary']['total_time_hours']:.2f} hours")
    print(f"   Moving time: {result['summary']['moving_time_hours']:.2f} hours")
    print(f"   Aid station time: {result['summary']['aid_station_time_hours']*60:.1f} minutes")
    
    print(f"\n🏃 PERFORMANCE:")
    print(f"   Average speed: {result['summary']['average_speed_kmh']:.2f} km/h")
    print(f"   Hiking percentage: {result['summary']['hiking_percentage']:.1f}%")
    print(f"   Technical multiplier: {result['summary']['technical_multiplier']:.3f}")
    
    print(f"\n🫁 RESPIRATORY:")
    print(f"   Incidents: {result['summary']['respiratory_incidents']}")
    print(f"   Worst impact: {result['summary']['worst_respiratory_impact']:.2%}")
    
    # Segment analysis (first 10km, last 10km)
    print(f"\n📈 SEGMENT BREAKDOWN:")
    print(f"   {'Distance':<10} {'Elevation':<12} {'Gradient':<10} {'Speed':<10} {'Cum. Time':<12}")
    print(f"   {'-'*10} {'-'*12} {'-'*10} {'-'*10} {'-'*12}")
    
    # First 5 segments
    for seg in result['segments'][:5]:
        print(f"   {seg['distance_km']:>7.1f} km {seg['elevation_m']:>9.0f} m "
              f"{seg['gradient_pct']:>7.1f}%  {seg['final_speed_kmh']:>7.2f} "
              f"{seg['cumulative_time_hours']:>7.2f}h")
    
    print(f"   {'...':<10} {'...':<12} {'...':<10} {'...':<10} {'...':<12}")
    
    # Last 5 segments
    for seg in result['segments'][-5:]:
        print(f"   {seg['distance_km']:>7.1f} km {seg['elevation_m']:>9.0f} m "
              f"{seg['gradient_pct']:>7.1f}%  {seg['final_speed_kmh']:>7.2f} "
              f"{seg['cumulative_time_hours']:>7.2f}h")
    
    print("\n" + "="*80)
    print("✓ Prediction complete!")
    print("="*80)


if __name__ == "__main__":
    main()
