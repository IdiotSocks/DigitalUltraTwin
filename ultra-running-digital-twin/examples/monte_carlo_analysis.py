#!/usr/bin/env python3
"""
Monte Carlo Analysis Example

Run 200 simulations and analyze results statistically.
"""

import sys
import json
sys.path.append('..')

from src.monte_carlo_runner import run_monte_carlo_simulations, analyze_results


def main():
    print("="*80)
    print("MONTE CARLO SIMULATION ANALYSIS")
    print("="*80)
    
    # Load elevation profile
    print("\n1. Loading elevation profile...")
    with open('../data/elevation/chianti_elevation_profile.json', 'r') as f:
        elevation_profile = json.load(f)['profile']
    print("   ✓ Profile loaded")
    
    # Run simulations
    print("\n2. Running 200 Monte Carlo simulations...")
    print("   This may take a few minutes...")
    
    results_df = run_monte_carlo_simulations(
        elevation_profile=elevation_profile,
        athlete_profile_path='../data/profiles/simbarashe_enhanced_profile_v3_3.json',
        course_profile_path='../data/courses/chianti_74k_course_profile_v1_3_FINAL.json',
        num_simulations=200,
        fitness_range=(1.0, 1.20),
        verbose=True
    )
    
    print("\n3. Analyzing results...")
    analysis = analyze_results(
        results_df,
        target_min_hours=10.0,
        target_max_hours=11.0
    )
    
    # Display analysis
    print("\n" + "="*80)
    print("STATISTICAL ANALYSIS")
    print("="*80)
    
    print(f"\n📊 FINISH TIME DISTRIBUTION:")
    print(f"   Mean: {analysis['time_statistics']['mean']:.2f} hours")
    print(f"   Median: {analysis['time_statistics']['median']:.2f} hours")
    print(f"   Std Dev: {analysis['time_statistics']['std']:.2f} hours")
    print(f"   Min: {analysis['time_statistics']['min']:.2f} hours")
    print(f"   Max: {analysis['time_statistics']['max']:.2f} hours")
    
    print(f"\n📈 PERCENTILES:")
    print(f"   P10 (fast): {analysis['time_statistics']['p10']:.2f} hours")
    print(f"   P25: {analysis['time_statistics']['p25']:.2f} hours")
    print(f"   P50 (median): {analysis['time_statistics']['median']:.2f} hours")
    print(f"   P75: {analysis['time_statistics']['p75']:.2f} hours")
    print(f"   P90 (slow): {analysis['time_statistics']['p90']:.2f} hours")
    
    print(f"\n🫁 RESPIRATORY IMPACT:")
    print(f"   Mean incidents: {analysis['respiratory_statistics']['mean_incidents']:.1f}")
    print(f"   Median incidents: {analysis['respiratory_statistics']['median_incidents']:.0f}")
    print(f"   Max incidents: {analysis['respiratory_statistics']['max_incidents']:.0f}")
    print(f"   Zero incident rate: {analysis['respiratory_statistics']['zero_incident_rate']:.1%}")
    
    if 'target_achievement' in analysis:
        print(f"\n🎯 TARGET ACHIEVEMENT (10-11 hours):")
        print(f"   Success rate: {analysis['target_achievement']['success_rate']:.1%}")
        print(f"   Successful runs: {analysis['target_achievement']['count']}/{analysis['total_simulations']}")
        if analysis['target_achievement']['mean_fitness_in_target']:
            print(f"   Mean fitness (in target): {analysis['target_achievement']['mean_fitness_in_target']:.2f}")
            print(f"   Mean temp (in target): {analysis['target_achievement']['mean_temp_in_target']:.1f}°C")
    
    # Save results
    output_file = 'monte_carlo_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"\n💾 Results saved to: {output_file}")
    
    print("\n" + "="*80)
    print("✓ Analysis complete!")
    print("="*80)


if __name__ == "__main__":
    main()
