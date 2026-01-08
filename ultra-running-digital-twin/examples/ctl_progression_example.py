#!/usr/bin/env python3
"""
CTL Fitness Progression Example

Demonstrates the CTL fitness tracker and progression calculator
"""

import sys
sys.path.append('..')

from src.ctl_fitness_tracker import CTLFitnessTracker


def main():
    print("="*80)
    print("CTL FITNESS PROGRESSION EXAMPLE")
    print("="*80)

    # Initialize tracker with history
    tracker = CTLFitnessTracker(data_file='../data/fitness/ctl_history.json')

    # Show conversion table
    print("\n📊 CTL TO FITNESS CONVERSION TABLE")
    print("="*80)
    print(f"{'CTL':<10} {'Fitness':<15} {'Speed Impact':<20}")
    print("-"*80)

    reference_ctl = 120
    for ctl in [80, 100, 106, 120, 138, 150, 170, 187, 200]:
        fitness = tracker.ctl_to_fitness(ctl)
        speed_impact = (fitness - 1.0) * 100
        marker = " ← Current" if ctl == 106 else " ← UTMB 2025" if ctl == 187 else " ← Baseline" if ctl == 120 else ""
        print(f"{ctl:<10} {fitness:<15.3f} {speed_impact:+.1f}%{marker}")

    print("\n" + "="*80)

    # Example progression scenarios
    scenarios = [
        {
            'name': 'Conservative Build',
            'current_ctl': 106,
            'current_date': '2026-01-08',
            'race_date': '2026-03-08',
            'training_plan': 'conservative'
        },
        {
            'name': 'Moderate Build (Recommended)',
            'current_ctl': 106,
            'current_date': '2026-01-08',
            'race_date': '2026-03-08',
            'training_plan': 'moderate'
        },
        {
            'name': 'Aggressive Build',
            'current_ctl': 106,
            'current_date': '2026-01-08',
            'race_date': '2026-03-08',
            'training_plan': 'aggressive'
        }
    ]

    print("\n🎯 TRAINING SCENARIOS FOR CHIANTI ULTRA (March 8, 2026)")
    print("="*80)

    for scenario in scenarios:
        progression = tracker.predict_ctl_progression(
            current_ctl=scenario['current_ctl'],
            current_date=scenario['current_date'],
            race_date=scenario['race_date'],
            training_plan=scenario['training_plan']
        )

        print(f"\n{scenario['name'].upper()}")
        print("-"*80)
        print(f"   Build: {progression['build_weeks']:.1f} weeks @ +{progression['weekly_ctl_gain']} CTL/week")
        print(f"   Peak CTL: {progression['peak_ctl']:.1f} → Fitness {progression['peak_fitness']:.3f}")
        print(f"   Race Day CTL: {progression['race_day_ctl']:.1f} → Fitness {progression['race_day_fitness']:.3f}")
        print(f"   Total Gain: {progression['ctl_gain_potential']:+.1f} CTL ({progression['fitness_gain_potential']:+.3f} fitness)")

        # Estimate time impact (rough approximation: 1% fitness = 1% speed = 1% time improvement)
        time_improvement_pct = progression['fitness_gain_potential'] * 100
        baseline_time_hours = 10.93  # From basic prediction
        improved_time_hours = baseline_time_hours * (1 - (time_improvement_pct / 100))
        time_saved_minutes = (baseline_time_hours - improved_time_hours) * 60

        print(f"   Estimated time improvement: {time_saved_minutes:.0f} minutes (vs. current fitness)")

    print("\n" + "="*80)
    print("\n💡 RECOMMENDATIONS:")
    print("   • Conservative: Lower injury risk, +19 CTL, ~20 min improvement")
    print("   • Moderate: Balanced approach, +24 CTL, ~26 min improvement")
    print("   • Aggressive: Higher risk, +29 CTL, ~32 min improvement")
    print("\n   Consider your recovery capacity and recent training load!")
    print("="*80)


if __name__ == "__main__":
    main()
