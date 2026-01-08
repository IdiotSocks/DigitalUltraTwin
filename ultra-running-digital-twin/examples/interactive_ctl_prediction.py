#!/usr/bin/env python3
"""
Interactive Race Prediction with CTL Fitness Tracking

This script allows you to:
1. Input your current CTL from Training Peaks
2. Calculate predicted race-day fitness based on training progression
3. Run race prediction with the selected fitness level
"""

import sys
import json
from datetime import datetime
sys.path.append('..')

from src.digital_twin_v32_simulator import DigitalTwinV32, EnvironmentalConditions, NutritionStrategy
from src.ctl_fitness_tracker import CTLFitnessTracker, interactive_ctl_input


def main():
    print("="*80)
    print("INTERACTIVE RACE PREDICTION WITH CTL FITNESS TRACKING")
    print("="*80)

    # Initialize CTL tracker
    print("\n1. Loading CTL fitness tracker...")
    tracker = CTLFitnessTracker(data_file='../data/fitness/ctl_history.json')

    # Show CTL history summary
    summary = tracker.get_ctl_summary()
    if summary:
        print(f"   ✓ Loaded {summary['total_records']} CTL records")
        print(f"   📊 Latest: CTL {summary['latest_ctl']:.1f} on {summary['latest_date']}")
        print(f"   📈 Range: {summary['min_ctl']:.1f} - {summary['max_ctl']:.1f}")
    else:
        print("   ℹ️  No CTL history found. You can still enter values manually.")

    # Load elevation profile
    print("\n2. Loading elevation profile...")
    with open('../data/elevation/chianti_elevation_profile.json', 'r') as f:
        profile_data = json.load(f)
        elevation_profile = profile_data['profile']

    print(f"   ✓ Loaded: {profile_data['total_distance_km']:.1f} km, "
          f"{profile_data['total_elevation_gain_m']:.0f}m gain")

    # Initialize simulator
    print("\n3. Initializing Digital Twin simulator...")
    simulator = DigitalTwinV32(
        athlete_profile_path='../data/profiles/simbarashe_enhanced_profile_v3_3.json',
        course_profile_path='../data/courses/chianti_74k_course_profile_v1_3_FINAL.json'
    )
    print("   ✓ Simulator initialized")

    # Interactive CTL/fitness input
    print("\n4. Setting up race scenario...")

    # Race date for Chianti Ultra Trail (example: March 8, 2026)
    race_date = input("\nEnter race date (YYYY-MM-DD) or press Enter for 2026-03-08: ").strip()
    if not race_date:
        race_date = '2026-03-08'

    print(f"   Race date: {race_date}")

    # Get fitness level using interactive input
    fitness_level = interactive_ctl_input(tracker, race_date)

    # Environmental conditions
    print("\n📍 Environmental Conditions:")
    temp_input = input("   Temperature (°C) or press Enter for 14°C: ").strip()
    temperature = float(temp_input) if temp_input else 14.0

    precip_input = input("   Precipitation (dry/light_rain/wet) or press Enter for dry: ").strip()
    precipitation = precip_input if precip_input in ['dry', 'light_rain', 'wet'] else 'dry'

    # Nutrition strategy
    print("\n🍽️  Nutrition Strategy:")
    cal_input = input("   Calories per hour or press Enter for 270: ").strip()
    calories_per_hour = float(cal_input) if cal_input else 270.0

    fluid_input = input("   Fluid ml per hour or press Enter for 550: ").strip()
    fluid_ml_per_hour = float(fluid_input) if fluid_input else 550.0

    scenario = {
        'environment': EnvironmentalConditions(
            temperature_celsius=temperature,
            altitude_m=400,
            humidity_pct=60,
            precipitation=precipitation
        ),
        'nutrition': NutritionStrategy(
            calories_per_hour=calories_per_hour,
            fluid_ml_per_hour=fluid_ml_per_hour,
            electrolytes_mg_per_hour=500
        ),
        'fitness_level': fitness_level
    }

    print(f"\n   ✓ Temperature: {scenario['environment'].temperature_celsius}°C")
    print(f"   ✓ Precipitation: {scenario['environment'].precipitation}")
    print(f"   ✓ Fitness level: {scenario['fitness_level']:.3f}")
    print(f"   ✓ Nutrition: {scenario['nutrition'].calories_per_hour:.0f} cal/hr, "
          f"{scenario['nutrition'].fluid_ml_per_hour:.0f} ml/hr")

    # Pacing strategy
    print("\n🏃 Pacing Strategy:")
    print("   1. Conservative")
    print("   2. Moderate")
    print("   3. Aggressive")
    print("   4. Even")
    print("   5. Race mode (aggressive throughout)")

    pacing_input = input("\nSelect pacing (1-5) or press Enter for race mode: ").strip()
    pacing_map = {
        '1': 'conservative',
        '2': 'moderate',
        '3': 'aggressive',
        '4': 'even',
        '5': 'race_mode'
    }
    pacing_strategy = pacing_map.get(pacing_input, 'race_mode')

    # Run simulation
    print("\n5. Running race simulation...")
    result = simulator.simulate_race(
        elevation_profile=elevation_profile,
        scenario=scenario,
        pacing_strategy=pacing_strategy
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
    print(f"   Pacing strategy: {pacing_strategy}")

    print(f"\n💪 FITNESS:")
    print(f"   Fitness multiplier: {result['summary']['fitness_level']:.3f}")
    equivalent_ctl = tracker.fitness_to_ctl(result['summary']['fitness_level'])
    print(f"   Equivalent CTL: {equivalent_ctl:.1f}")

    print(f"\n🫁 RESPIRATORY:")
    print(f"   Incidents: {result['summary']['respiratory_incidents']}")
    print(f"   Worst impact: {result['summary']['worst_respiratory_impact']:.2%}")

    # Segment analysis
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

    # Option to save CTL record
    save_input = input("\nSave this prediction to CTL history? (y/n): ").strip().lower()
    if save_input == 'y':
        today = datetime.now().strftime('%Y-%m-%d')
        notes = input("Add notes (optional): ").strip()

        tracker.add_ctl_record(
            date=today,
            ctl=equivalent_ctl,
            event_name=f"Prediction for {race_date}",
            notes=notes if notes else f"Predicted finish: {result['summary']['total_time_formatted']}"
        )
        tracker.save_history('../data/fitness/ctl_history.json')
        print("✓ Saved to CTL history")

    print("\n" + "="*80)
    print("✓ Prediction complete!")
    print("="*80)


if __name__ == "__main__":
    main()
