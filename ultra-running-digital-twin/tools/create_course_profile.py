#!/usr/bin/env python3
"""
Interactive Course Profile Creator

Creates custom course profile JSON files for race predictions.
"""

import json
from datetime import datetime


def get_input(prompt, default=None, input_type=str):
    """Get user input with optional default value"""
    if default is not None:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "

    value = input(prompt_text).strip()

    if not value and default is not None:
        return default

    try:
        return input_type(value)
    except ValueError:
        print(f"Invalid input, using default: {default}")
        return default


def main():
    print("="*80)
    print("COURSE PROFILE CREATOR")
    print("="*80)
    print("\nThis will guide you through creating a course profile JSON file.")
    print("Press Enter to use default values shown in brackets.\n")

    # Basic info
    print("\n📋 BASIC INFORMATION")
    print("-" * 80)
    race_name = get_input("Race name (e.g., 'UTMB 2026')")
    distance_km = get_input("Total distance (km)", 100, float)
    elevation_gain_m = get_input("Total elevation gain (m)", 5000, float)

    # Terrain
    print("\n🏔️  TERRAIN CHARACTERISTICS")
    print("-" * 80)
    print("Surface types:")
    print("  1. Road")
    print("  2. Smooth trail")
    print("  3. Mixed trail (default)")
    print("  4. Technical trail")
    print("  5. Mountain/Alpine")

    surface_choice = get_input("Select surface type (1-5)", 3, int)
    surface_map = {
        1: "road",
        2: "smooth_trail",
        3: "mixed_trail",
        4: "technical_trail",
        5: "mountain"
    }
    surface_type = surface_map.get(surface_choice, "mixed_trail")

    dry_multiplier = get_input("Dry conditions multiplier (0.95-1.0, higher=faster)", 0.99, float)
    wet_multiplier = get_input("Wet conditions multiplier (0.85-0.95)", 0.93, float)

    # Fatigue
    print("\n💪 FATIGUE MODEL")
    print("-" * 80)
    print("Base fatigue rate: how quickly you slow down")
    print("  0.999 = very slow fatigue (easy course)")
    print("  0.9975 = moderate fatigue (typical)")
    print("  0.995 = fast fatigue (hard course)")

    fatigue_base = get_input("Base fatigue rate", 0.9975, float)
    fatigue_inflection = get_input("Fatigue inflection point (km, where it accelerates)", 50, float)
    fatigue_slope = get_input("Fatigue slope multiplier (1.0-1.5, higher=faster acceleration)", 1.1, float)

    # Field effects
    print("\n🏆 COMPETITIVE ADVANTAGES")
    print("-" * 80)
    print("These represent your athlete's strengths on this terrain type")

    runnable_advantage = get_input("Runnable trail advantage (1.0-1.05, 1.0=none)", 1.02, float)
    climb_advantage = get_input("Short climb advantage (1.0-1.05, 1.0=none)", 1.01, float)

    # Altitude
    print("\n⛰️  ALTITUDE SETTINGS")
    print("-" * 80)
    apply_altitude = get_input("Apply altitude penalty? (y/n)", "n").lower() == 'y'

    if apply_altitude:
        altitude_threshold = get_input("Altitude threshold (m, penalty starts above)", 2000, int)
        altitude_penalty = get_input("Penalty per 1000m (0.95=5% slower)", 0.95, float)
    else:
        altitude_threshold = 3000
        altitude_penalty = 1.0

    # Generate JSON
    course_profile = {
        "metadata": {
            "race_name": race_name,
            "distance_km": distance_km,
            "elevation_gain_m": elevation_gain_m,
            "version": "1.0",
            "created": datetime.now().strftime('%Y-%m-%d'),
            "source": "Course Profile Creator Script"
        },
        "terrain_profile": {
            "surface_type": surface_type,
            "technicality": {
                "dry_multiplier": dry_multiplier,
                "light_rain_multiplier": round((dry_multiplier + wet_multiplier) / 2, 3),
                "wet_multiplier": wet_multiplier,
                "description": f"{surface_type.replace('_', ' ')} terrain"
            }
        },
        "simulation_defaults": {
            "fatigue_model": {
                "fatigue_per_km_base": fatigue_base,
                "fatigue_inflection_km": fatigue_inflection,
                "fatigue_slope_multiplier": fatigue_slope,
                "description": "Course-specific fatigue accumulation"
            },
            "field_effects": {
                "field_loss_multiplier_runnable_trail": runnable_advantage,
                "field_loss_multiplier_short_climbs": climb_advantage,
                "description": "Athlete's competitive advantages on this terrain"
            }
        },
        "environment_profile": {
            "altitude_penalty": {
                "apply": apply_altitude,
                "starts_m": altitude_threshold,
                "multiplier_per_1000m": altitude_penalty,
                "description": "Altitude effects applied" if apply_altitude else "Low altitude race"
            }
        }
    }

    # Display
    print("\n" + "="*80)
    print("GENERATED COURSE PROFILE")
    print("="*80)
    print(json.dumps(course_profile, indent=2))

    # Save
    print("\n" + "="*80)
    filename = race_name.lower().replace(' ', '_') + '_course_profile.json'
    save_path = f"../data/courses/{filename}"

    save = get_input(f"\nSave to {save_path}? (y/n)", "y").lower()

    if save == 'y':
        with open(save_path, 'w') as f:
            json.dump(course_profile, f, indent=2)
        print(f"\n✅ Saved to: {save_path}")
        print("\nYou can now use this profile with:")
        print(f"  simulator = DigitalTwinV32(")
        print(f"      athlete_profile_path='...',")
        print(f"      course_profile_path='{save_path}'")
        print(f"  )")
    else:
        print("\n📋 Copy the JSON above and save it manually.")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
