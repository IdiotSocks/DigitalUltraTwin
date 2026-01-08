#!/usr/bin/env python3
"""
Compare different CTL training scenarios for Chianti Ultra
"""

import sys
import json
sys.path.append('..')

from src.digital_twin_v32_simulator import DigitalTwinV32, EnvironmentalConditions, NutritionStrategy
from src.ctl_fitness_tracker import CTLFitnessTracker

# Load data
with open('../data/elevation/chianti_elevation_profile.json', 'r') as f:
    profile_data = json.load(f)
    elevation_profile = profile_data['profile']

simulator = DigitalTwinV32(
    athlete_profile_path='../data/profiles/simbarashe_enhanced_profile_v3_3.json',
    course_profile_path='../data/courses/chianti_74k_course_profile_v1_3_FINAL.json'
)

tracker = CTLFitnessTracker()

# Base scenario
base_scenario = {
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
    )
}

print("="*80)
print("CHIANTI ULTRA 74K - CTL TRAINING SCENARIO COMPARISON")
print("="*80)
print(f"\nRace: {profile_data['total_distance_km']:.1f} km, {profile_data['total_elevation_gain_m']:.0f}m gain")
print(f"Race Date: March 8, 2026")
print(f"Current Date: January 8, 2026 (8.4 weeks to race)")

scenarios = [
    {
        'name': 'Current Fitness (No Training)',
        'ctl': 106,
        'fitness': tracker.ctl_to_fitness(106),
        'notes': 'If you raced today'
    },
    {
        'name': 'Conservative Training',
        'ctl': 118,
        'fitness': tracker.ctl_to_fitness(118),
        'notes': '+2.5 CTL/week, lower injury risk'
    },
    {
        'name': 'Moderate Training (Recommended)',
        'ctl': 124,
        'fitness': tracker.ctl_to_fitness(124),
        'notes': '+3.5 CTL/week, balanced approach'
    },
    {
        'name': 'Aggressive Training',
        'ctl': 134,
        'fitness': tracker.ctl_to_fitness(134),
        'notes': '+5.0 CTL/week, higher injury risk'
    },
    {
        'name': 'UTMB 2025 Fitness',
        'ctl': 187,
        'fitness': tracker.ctl_to_fitness(187),
        'notes': 'Peak fitness reference'
    }
]

results = []

for scenario in scenarios:
    test_scenario = base_scenario.copy()
    test_scenario['fitness_level'] = scenario['fitness']
    
    result = simulator.simulate_race(
        elevation_profile=elevation_profile,
        scenario=test_scenario,
        pacing_strategy='race_mode'
    )
    
    results.append({
        'name': scenario['name'],
        'ctl': scenario['ctl'],
        'fitness': scenario['fitness'],
        'time': result['summary']['total_time_formatted'],
        'time_hours': result['summary']['total_time_hours'],
        'avg_speed': result['summary']['average_speed_kmh'],
        'notes': scenario['notes']
    })

print("\n" + "="*80)
print("SCENARIO COMPARISON")
print("="*80)
print(f"\n{'Scenario':<35} {'CTL':<8} {'Fitness':<10} {'Time':<12} {'Speed':<10}")
print("-"*80)

baseline_time = results[0]['time_hours']

for r in results:
    time_diff = r['time_hours'] - baseline_time
    time_diff_str = f"({time_diff*60:+.0f} min)" if time_diff != 0 else "(baseline)"
    
    print(f"{r['name']:<35} {r['ctl']:<8.0f} {r['fitness']:<10.3f} {r['time']:<12} {r['avg_speed']:<10.2f}")
    print(f"  {r['notes']:<60} {time_diff_str}")
    print()

print("="*80)
print("\n💡 KEY INSIGHTS:")
print(f"   • Current fitness (CTL 106): {results[0]['time']}")
print(f"   • Moderate training (CTL 124): {results[2]['time']} - saves {(results[0]['time_hours']-results[2]['time_hours'])*60:.0f} minutes")
print(f"   • Aggressive training (CTL 134): {results[3]['time']} - saves {(results[0]['time_hours']-results[3]['time_hours'])*60:.0f} minutes")
print(f"   • UTMB peak (CTL 187): {results[4]['time']} - saves {(results[0]['time_hours']-results[4]['time_hours'])*60:.0f} minutes")
print("\n   Recommendation: Moderate training plan for balanced risk/reward")
print("="*80)
