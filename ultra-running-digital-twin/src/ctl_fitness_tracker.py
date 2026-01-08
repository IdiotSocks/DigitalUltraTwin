#!/usr/bin/env python3
"""
CTL Fitness Tracker

Converts Training Peaks CTL (Chronic Training Load) values to fitness multipliers
and predicts fitness progression to race day.

Based on calibration:
- CTL 120 = fitness 1.0 (UTMB 2025 baseline)
- CTL 138 = fitness 1.15 (Arc 2025)
- CTL 187 = fitness 1.56 (UTMB peak)
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CTLRecord:
    """Represents a CTL measurement at a specific date"""
    date: str  # Format: YYYY-MM-DD
    ctl: float
    event_name: Optional[str] = None
    notes: Optional[str] = None


class CTLFitnessTracker:
    """
    Tracks CTL history and converts to fitness multipliers for race prediction
    """

    # Calibration points from athlete profile
    BASELINE_CTL = 120.0  # UTMB 2025 baseline
    BASELINE_FITNESS = 1.0

    # CTL to fitness conversion rate (from CTL 120->138 = fitness 1.0->1.15)
    CTL_TO_FITNESS_RATE = 0.00833  # Per CTL point

    def __init__(self, data_file: str = None):
        """Initialize tracker with optional data file"""
        self.data_file = data_file
        self.ctl_history: List[CTLRecord] = []

        if data_file:
            self.load_history(data_file)

    def load_history(self, filepath: str):
        """Load CTL history from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.ctl_history = [
                    CTLRecord(**record) for record in data.get('ctl_history', [])
                ]
        except FileNotFoundError:
            print(f"⚠️  No history file found at {filepath}. Starting fresh.")
            self.ctl_history = []

    def save_history(self, filepath: str):
        """Save CTL history to JSON file"""
        data = {
            'ctl_history': [
                {
                    'date': record.date,
                    'ctl': record.ctl,
                    'event_name': record.event_name,
                    'notes': record.notes
                }
                for record in self.ctl_history
            ],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def add_ctl_record(self, date: str, ctl: float, event_name: str = None, notes: str = None):
        """Add a CTL record to history"""
        record = CTLRecord(date=date, ctl=ctl, event_name=event_name, notes=notes)
        self.ctl_history.append(record)
        # Sort by date
        self.ctl_history.sort(key=lambda x: x.date)

    def ctl_to_fitness(self, ctl: float) -> float:
        """
        Convert CTL to fitness multiplier

        Formula: fitness = 1.0 + ((CTL - baseline) * conversion_rate)

        Args:
            ctl: Current CTL value

        Returns:
            Fitness multiplier (e.g., 1.15)
        """
        fitness = self.BASELINE_FITNESS + ((ctl - self.BASELINE_CTL) * self.CTL_TO_FITNESS_RATE)
        return max(0.5, fitness)  # Floor at 0.5 to avoid unrealistic values

    def fitness_to_ctl(self, fitness: float) -> float:
        """
        Convert fitness multiplier back to CTL

        Args:
            fitness: Fitness multiplier (e.g., 1.15)

        Returns:
            Equivalent CTL value
        """
        ctl = self.BASELINE_CTL + ((fitness - self.BASELINE_FITNESS) / self.CTL_TO_FITNESS_RATE)
        return ctl

    def predict_ctl_progression(
        self,
        current_ctl: float,
        current_date: str,
        race_date: str,
        training_plan: str = 'moderate'
    ) -> Dict:
        """
        Predict CTL progression from current date to race day

        Args:
            current_ctl: Current CTL value
            current_date: Today's date (YYYY-MM-DD)
            race_date: Race day (YYYY-MM-DD)
            training_plan: Training intensity ('conservative', 'moderate', 'aggressive')

        Returns:
            Dictionary with progression predictions
        """
        # Parse dates
        current = datetime.strptime(current_date, '%Y-%m-%d')
        race = datetime.strptime(race_date, '%Y-%m-%d')
        days_to_race = (race - current).days
        weeks_to_race = days_to_race / 7

        # CTL gain rates (per week) by training plan
        ctl_gain_rates = {
            'conservative': 2.5,   # Safe progression
            'moderate': 3.5,       # Balanced approach
            'aggressive': 5.0,     # Ambitious but risky
            'maintenance': 0.0,    # Hold current fitness
            'taper': -2.0          # Pre-race taper
        }

        weekly_gain = ctl_gain_rates.get(training_plan, 3.5)

        # Calculate taper period (last 2 weeks)
        taper_weeks = min(2, weeks_to_race)
        build_weeks = max(0, weeks_to_race - taper_weeks)

        # Predict CTL progression
        # Build phase
        ctl_after_build = current_ctl + (build_weeks * weekly_gain)

        # Taper phase (reduce by 2 CTL/week)
        ctl_on_race_day = ctl_after_build + (taper_weeks * -2.0)

        # Convert to fitness
        current_fitness = self.ctl_to_fitness(current_ctl)
        race_day_fitness = self.ctl_to_fitness(ctl_on_race_day)
        peak_fitness = self.ctl_to_fitness(ctl_after_build)

        return {
            'days_to_race': days_to_race,
            'weeks_to_race': weeks_to_race,
            'current_ctl': current_ctl,
            'current_fitness': round(current_fitness, 3),
            'peak_ctl': round(ctl_after_build, 1),
            'peak_fitness': round(peak_fitness, 3),
            'race_day_ctl': round(ctl_on_race_day, 1),
            'race_day_fitness': round(race_day_fitness, 3),
            'ctl_gain_potential': round(ctl_on_race_day - current_ctl, 1),
            'fitness_gain_potential': round(race_day_fitness - current_fitness, 3),
            'training_plan': training_plan,
            'weekly_ctl_gain': weekly_gain,
            'build_weeks': build_weeks,
            'taper_weeks': taper_weeks
        }

    def get_latest_ctl(self) -> Optional[Tuple[str, float]]:
        """Get the most recent CTL record"""
        if not self.ctl_history:
            return None

        latest = self.ctl_history[-1]
        return (latest.date, latest.ctl)

    def get_ctl_summary(self) -> Dict:
        """Get summary statistics of CTL history"""
        if not self.ctl_history:
            return {}

        ctls = [record.ctl for record in self.ctl_history]

        return {
            'total_records': len(self.ctl_history),
            'min_ctl': min(ctls),
            'max_ctl': max(ctls),
            'avg_ctl': sum(ctls) / len(ctls),
            'latest_ctl': self.ctl_history[-1].ctl,
            'latest_date': self.ctl_history[-1].date,
            'date_range': f"{self.ctl_history[0].date} to {self.ctl_history[-1].date}"
        }

    def print_progression_table(self, progression: Dict):
        """Print a formatted progression table"""
        print("\n" + "="*80)
        print("CTL FITNESS PROGRESSION CALCULATOR")
        print("="*80)

        print(f"\n📅 TIMELINE:")
        print(f"   Days to race: {progression['days_to_race']}")
        print(f"   Weeks to race: {progression['weeks_to_race']:.1f}")
        print(f"   Training plan: {progression['training_plan'].title()}")

        print(f"\n📊 CURRENT STATE:")
        print(f"   CTL: {progression['current_ctl']:.1f}")
        print(f"   Fitness multiplier: {progression['current_fitness']:.3f}")

        print(f"\n🎯 PEAK FITNESS (before taper):")
        print(f"   CTL: {progression['peak_ctl']:.1f}")
        print(f"   Fitness multiplier: {progression['peak_fitness']:.3f}")
        print(f"   Build period: {progression['build_weeks']:.1f} weeks @ +{progression['weekly_ctl_gain']} CTL/week")

        print(f"\n🏁 RACE DAY PREDICTION:")
        print(f"   CTL: {progression['race_day_ctl']:.1f}")
        print(f"   Fitness multiplier: {progression['race_day_fitness']:.3f}")
        print(f"   Taper period: {progression['taper_weeks']:.1f} weeks @ -2 CTL/week")

        print(f"\n📈 POTENTIAL GAINS:")
        print(f"   CTL gain: {progression['ctl_gain_potential']:+.1f}")
        print(f"   Fitness gain: {progression['fitness_gain_potential']:+.3f}")

        print("\n" + "="*80)


def interactive_ctl_input(tracker: CTLFitnessTracker, race_date: str) -> float:
    """
    Interactive prompt for CTL input with smart defaults

    Args:
        tracker: CTLFitnessTracker instance
        race_date: Race date (YYYY-MM-DD)

    Returns:
        Selected fitness multiplier
    """
    print("\n" + "="*80)
    print("FITNESS LEVEL INPUT")
    print("="*80)

    # Get latest CTL if available
    latest = tracker.get_latest_ctl()

    print("\n📋 OPTIONS:")
    print("   1. Use current CTL from Training Peaks")
    print("   2. Use predicted race-day fitness (with progression)")
    print("   3. Enter custom fitness multiplier")

    if latest:
        print(f"\n💡 Latest CTL on record: {latest[1]:.1f} ({latest[0]})")
        print(f"   Equivalent fitness: {tracker.ctl_to_fitness(latest[1]):.3f}")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == '1':
        ctl_input = input("\nEnter current CTL from Training Peaks: ").strip()
        try:
            ctl = float(ctl_input)
            fitness = tracker.ctl_to_fitness(ctl)
            print(f"✓ CTL {ctl:.1f} = Fitness {fitness:.3f}")
            return fitness
        except ValueError:
            print("⚠️  Invalid input. Using default fitness 1.0")
            return 1.0

    elif choice == '2':
        ctl_input = input("\nEnter current CTL: ").strip()
        current_date = input("Enter current date (YYYY-MM-DD) or press Enter for today: ").strip()

        if not current_date:
            current_date = datetime.now().strftime('%Y-%m-%d')

        try:
            ctl = float(ctl_input)

            print("\n📚 Training plan options:")
            print("   1. Conservative (2.5 CTL/week)")
            print("   2. Moderate (3.5 CTL/week)")
            print("   3. Aggressive (5.0 CTL/week)")

            plan_choice = input("\nSelect training plan (1-3): ").strip()
            plan_map = {'1': 'conservative', '2': 'moderate', '3': 'aggressive'}
            training_plan = plan_map.get(plan_choice, 'moderate')

            progression = tracker.predict_ctl_progression(ctl, current_date, race_date, training_plan)
            tracker.print_progression_table(progression)

            print(f"\n✓ Using race-day fitness: {progression['race_day_fitness']:.3f}")
            return progression['race_day_fitness']

        except ValueError:
            print("⚠️  Invalid input. Using default fitness 1.0")
            return 1.0

    elif choice == '3':
        fitness_input = input("\nEnter custom fitness multiplier (e.g., 1.15): ").strip()
        try:
            fitness = float(fitness_input)
            equivalent_ctl = tracker.fitness_to_ctl(fitness)
            print(f"✓ Fitness {fitness:.3f} = Equivalent CTL {equivalent_ctl:.1f}")
            return fitness
        except ValueError:
            print("⚠️  Invalid input. Using default fitness 1.0")
            return 1.0

    else:
        print("⚠️  Invalid option. Using default fitness 1.0")
        return 1.0


if __name__ == "__main__":
    # Example usage
    tracker = CTLFitnessTracker()

    # Add sample data
    tracker.add_ctl_record('2025-08-29', 187, 'UTMB 2025', 'Peak fitness')
    tracker.add_ctl_record('2026-01-08', 106, None, 'Current')

    print("CTL to Fitness Conversion Table:")
    print("="*50)
    print(f"{'CTL':<10} {'Fitness Multiplier':<20}")
    print("-"*50)

    for ctl in [80, 100, 106, 120, 138, 150, 187, 200]:
        fitness = tracker.ctl_to_fitness(ctl)
        print(f"{ctl:<10} {fitness:<20.3f}")

    print("\n" + "="*50)

    # Example progression calculation
    progression = tracker.predict_ctl_progression(
        current_ctl=106,
        current_date='2026-01-08',
        race_date='2026-03-08',
        training_plan='moderate'
    )

    tracker.print_progression_table(progression)
