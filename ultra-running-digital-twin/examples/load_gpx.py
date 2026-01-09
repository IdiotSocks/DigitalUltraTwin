#!/usr/bin/env python3
"""
Load and analyze a new GPX file for race predictions

Usage:
    python3 load_gpx.py path/to/race.gpx [output_name]
"""

import sys
import json
import os
sys.path.append('..')

from src.gpx_parser import parse_gpx_file, smooth_elevation_profile
from src.digital_twin_v32_simulator import DigitalTwinV32, EnvironmentalConditions, NutritionStrategy
from src.ctl_fitness_tracker import CTLFitnessTracker


def analyze_gpx(gpx_path: str, output_name: str = None):
    """
    Load GPX file, create elevation profile, and run prediction
    """
    print("="*80)
    print("GPX FILE ANALYZER")
    print("="*80)

    # Check if file exists
    if not os.path.exists(gpx_path):
        print(f"\n❌ Error: File not found: {gpx_path}")
        return

    print(f"\n1. Parsing GPX file: {gpx_path}")

    # Parse GPX file
    try:
        data = parse_gpx_file(gpx_path, simplify_interval_km=1.0)
    except Exception as e:
        print(f"❌ Error parsing GPX file: {e}")
        return

    profile = data['profile']
    metadata = data['metadata']

    print(f"   ✓ Parsed successfully")
    print(f"   📊 Distance: {metadata['total_distance_km']:.2f} km")
    print(f"   📈 Elevation gain: {metadata['total_elevation_gain_m']:.0f} m")
    print(f"   📍 Original points: {metadata['num_points']}")
    print(f"   📍 Simplified points: {metadata['num_simplified_points']}")

    # Optional: smooth the elevation profile
    smooth_input = input("\n   Smooth elevation data? (y/n, default=n): ").strip().lower()
    if smooth_input == 'y':
        profile = smooth_elevation_profile(profile, window_size=3)
        print("   ✓ Applied smoothing")

    # Save elevation profile
    if output_name is None:
        output_name = os.path.splitext(os.path.basename(gpx_path))[0]

    output_file = f"../data/elevation/{output_name}_elevation_profile.json"

    output_data = {
        "race": output_name.replace('_', ' ').title(),
        "total_distance_km": metadata['total_distance_km'],
        "total_elevation_gain_m": metadata['total_elevation_gain_m'],
        "profile": profile
    }

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"\n2. Saved elevation profile to: {output_file}")

    # Ask if user wants to run a prediction
    run_prediction = input("\n   Run race prediction? (y/n, default=y): ").strip().lower()

    if run_prediction != 'n':
        print("\n" + "="*80)
        print("RUNNING RACE PREDICTION")
        print("="*80)

        # Initialize simulator (using existing athlete profile)
        print("\n3. Initializing Digital Twin...")
        try:
            simulator = DigitalTwinV32(
                athlete_profile_path='../data/profiles/simbarashe_enhanced_profile_v3_3.json',
                course_profile_path='../data/courses/chianti_74k_course_profile_v1_3_FINAL.json'
            )
            print("   ✓ Simulator initialized")
        except Exception as e:
            print(f"   ⚠️  Could not load course profile, using defaults")
            print(f"   Error: {e}")
            return

        # Get fitness level
        tracker = CTLFitnessTracker(data_file='../data/fitness/ctl_history.json')

        print("\n4. Setting up scenario...")
        fitness_input = input("   Enter fitness level (e.g., 1.0) or CTL (e.g., 120) or press Enter for 1.0: ").strip()

        if fitness_input:
            try:
                value = float(fitness_input)
                if value > 10:  # Assume it's CTL
                    fitness = tracker.ctl_to_fitness(value)
                    print(f"   CTL {value:.0f} → Fitness {fitness:.3f}")
                else:  # Assume it's fitness
                    fitness = value
            except ValueError:
                fitness = 1.0
                print("   Using default fitness: 1.0")
        else:
            fitness = 1.0

        # Set up scenario
        scenario = {
            'environment': EnvironmentalConditions(
                temperature_celsius=14,
                altitude_m=400,
                humidity_pct=60,
                precipitation='dry'
            ),
            'nutrition': NutritionStrategy(
                calories_per_hour=270,
                fluid_ml_per_hour=550,
                electrolytes_mg_per_hour=500
            ),
            'fitness_level': fitness
        }

        # Run simulation
        print("\n5. Running simulation...")
        result = simulator.simulate_race(
            elevation_profile=profile,
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
        print(f"   Fitness level: {result['summary']['fitness_level']:.3f}")

        print(f"\n🫁 RESPIRATORY:")
        print(f"   Incidents: {result['summary']['respiratory_incidents']}")

        # Segment summary
        print(f"\n📈 SEGMENT SUMMARY (every 10km):")
        print(f"   {'Distance':<12} {'Elevation':<12} {'Speed':<12} {'Cum. Time':<12}")
        print(f"   {'-'*12} {'-'*12} {'-'*12} {'-'*12}")

        for i, seg in enumerate(result['segments']):
            if i % 10 == 0 or i == len(result['segments']) - 1:
                print(f"   {seg['distance_km']:>7.1f} km {seg['elevation_m']:>9.0f} m "
                      f"{seg['final_speed_kmh']:>7.2f} km/h {seg['cumulative_time_hours']:>7.2f}h")

        print("\n" + "="*80)

    print("\n✅ Analysis complete!")
    print(f"   Elevation profile saved: {output_file}")
    print(f"   You can now use this profile with interactive_ctl_prediction.py")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 load_gpx.py path/to/race.gpx [output_name]")
        print("\nExample:")
        print("  python3 load_gpx.py ~/Downloads/utmb_2026.gpx utmb_2026")
        sys.exit(1)

    gpx_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None

    analyze_gpx(gpx_path, output_name)


if __name__ == "__main__":
    main()
