# Ultra Course Profile Generator

## Course Type Taxonomy

### 1. **runnable_trail_hilly**
- **Examples**: Chianti 74K, many European trail ultras
- **Characteristics**: 70-80% runnable, rolling hills, farm tracks/singletrack
- **Technical multiplier**: 0.96-0.99 (very fast)
- **Fatigue onset**: Late (>60km)
- **Key challenge**: Pacing discipline, not going too fast

### 2. **technical_coastal_trail**
- **Examples**: Arc of Attrition, South West Coast Path races
- **Characteristics**: 40-50% runnable, constant elevation changes, exposure
- **Technical multiplier**: 0.85-0.92 (slow when wet)
- **Fatigue onset**: Early (<25km) due to constant transitions
- **Key challenge**: Quad destruction, weather exposure

### 3. **alpine_ultra**
- **Examples**: UTMB, TDS, Eiger Ultra
- **Characteristics**: 30-50% runnable, sustained climbs >1000m, high altitude
- **Technical multiplier**: 0.88-0.93
- **Fatigue onset**: Progressive, altitude compounds
- **Key challenge**: Altitude, sustained climbing, night sections

### 4. **mountain_sky_running**
- **Examples**: Skyrace Comapedrosa, Transvulcania
- **Characteristics**: <40% runnable, extreme grades (>20%), technical scrambling
- **Technical multiplier**: 0.75-0.88
- **Fatigue onset**: Immediate, sustained hard effort
- **Key challenge**: Vertical gain per km, exposure, scrambling

### 5. **desert_ultra**
- **Examples**: Marathon des Sables, Sahara races
- **Characteristics**: 80-90% runnable, heat dominant, navigation
- **Technical multiplier**: 0.95-0.98 (fast surface)
- **Fatigue onset**: Heat-accelerated after 4-6 hours
- **Key challenge**: Heat management, hydration, sand/dunes

### 6. **forest_trail_moderate**
- **Examples**: Many US 50-milers, HURT 100
- **Characteristics**: 60-70% runnable, shaded, root/rock technical
- **Technical multiplier**: 0.90-0.95
- **Fatigue onset**: Standard progression
- **Key challenge**: Technical footing, humidity if tropical

### 7. **fell_running_uk**
- **Examples**: Bob Graham Round, Lakeland trails
- **Characteristics**: 30-40% runnable, boggy, navigationally complex
- **Technical multiplier**: 0.80-0.90 (worse in wet)
- **Fatigue onset**: Early, constant vert changes
- **Key challenge**: Navigation, bog, weather volatility

### 8. **road_ultra**
- **Examples**: Comrades, Spartathlon
- **Characteristics**: 100% runnable, pure endurance test
- **Technical multiplier**: 1.00
- **Fatigue onset**: Distance-dependent, pace management critical
- **Key challenge**: Mental fatigue, pace discipline, foot pounding

### 9. **gravel_ultra**
- **Examples**: Badwater variants, gravel ultras
- **Characteristics**: 95-100% runnable, fire roads, wide trails
- **Technical multiplier**: 0.98-1.00
- **Fatigue onset**: Similar to road
- **Key challenge**: Monotony, heat if exposed

### 10. **canyon_technical**
- **Examples**: Grand Canyon R2R2R, slot canyon races
- **Characteristics**: 50-60% runnable, extreme heat differential, technical descents
- **Technical multiplier**: 0.88-0.94
- **Fatigue onset**: Heat/descent combo in first half
- **Key challenge**: Heat at bottom, steep technical descents/ascents

### 11. **night_only_ultra**
- **Examples**: Nighthawk 50K, overnight trail races
- **Characteristics**: Varies by terrain, but +10-15% cognitive load
- **Technical multiplier**: Base × 0.90-0.95
- **Fatigue onset**: Circadian disruption accelerates
- **Key challenge**: Navigation, depth perception, staying alert

### 12. **multi_loop_course**
- **Examples**: Backyard ultras, 10km loop courses
- **Characteristics**: Varies, but mental challenge of repetition
- **Technical multiplier**: Base terrain
- **Fatigue onset**: Mental fatigue compounds physical
- **Key challenge**: Psychological battle with repetition

---

## Enhanced Course Profile Template

```json
{
  "course_metadata": {
    "race_id": "race_slug",
    "race_name": "Official Race Name",
    "distance_km": 0.0,
    "elevation_gain_m": 0,
    "elevation_loss_m": 0,
    "region": "Location, Country",
    "course_type": "SEE TAXONOMY ABOVE",
    "start_time": "06:00",
    "cutoff_hours": 0.0,
    "loop_type": "point_to_point | out_and_back | loop | multi_loop",
    "navigation_difficulty": "marked | cairns | gps_required | expert_navigation",
    "exposure_rating": "low | moderate | high | extreme",
    "notes": "Key race characteristics",
    "version": "1.0",
    "calibration_source": "Data source for profile creation"
  },

  "environment_profile": {
    "altitude_band_m": [0, 0],
    "altitude_penalty": {
      "apply": false,
      "starts_m": 1000,
      "requires_continuous_exposure_min": 60,
      "multiplier_per_1000m": 0.95,
      "expected_effect_multiplier": 1.0,
      "notes": "Altitude effect description"
    },
    "temperature_band_c": [0, 0],
    "temperature_variation": {
      "start_temp_c": 0,
      "peak_temp_c": 0,
      "peak_time": "14:00",
      "night_low_c": 0,
      "notes": "Temperature profile over race duration"
    },
    "wind_band_kmh": [0, 0],
    "wind_exposure_sections": ["Describe exposed sections"],
    "precipitation_scenarios": ["dry", "light_rain", "rain", "storm", "snow"],
    "seasonal_considerations": {
      "spring": "Conditions",
      "summer": "Conditions",
      "autumn": "Conditions",
      "winter": "Conditions"
    }
  },

  "terrain_profile": {
    "surface_mix": {
      "paved_pct": 0,
      "gravel_track_pct": 0,
      "singletrack_pct": 0,
      "rocky_technical_pct": 0,
      "sand_pct": 0,
      "snow_ice_pct": 0,
      "bog_mud_pct": 0,
      "scramble_pct": 0
    },
    "technicality": {
      "dry_multiplier": 1.0,
      "light_rain_multiplier": 0.95,
      "rain_multiplier": 0.90,
      "storm_multiplier": 0.80,
      "snow_multiplier": 0.75,
      "notes": "How conditions affect speed"
    },
    "runnability": {
      "runnable_fraction_estimate": 0.0,
      "short_climb_pattern": false,
      "sustained_climb_pattern": false,
      "notes": "What percentage can actually be run vs hiked"
    },
    "foot_hazards": {
      "ankle_twist_risk": "low | moderate | high",
      "slip_hazard": "low | moderate | high",
      "notes": "Specific hazards to watch"
    }
  },

  "climb_descent_structure": {
    "climb_blocks": {
      "typical_duration_min": [0, 0],
      "typical_grade_pct": [0, 0],
      "max_single_climb_m": 0,
      "total_climbing_sections": 0,
      "apply_short_climb_fatigue_multiplier": 1.0,
      "notes": "Short punchy vs sustained climbs"
    },
    "descent_blocks": {
      "typical_duration_min": [0, 0],
      "typical_grade_pct": [0, 0],
      "max_single_descent_m": 0,
      "total_descent_sections": 0,
      "downhill_damage_multiplier": 1.0,
      "technical_descent_pct": 0,
      "notes": "Eccentric load and technical difficulty"
    }
  },

  "aid_stations": [
    {
      "name": "Start/Finish",
      "distance_km": 0.0,
      "elevation_m": 0,
      "type": "start",
      "features": {
        "crew_access": false,
        "drop_bag": false,
        "full_aid": false
      },
      "estimated_stop_seconds": 0,
      "notes": "Any specific notes"
    },
    {
      "name": "Aid Station Name",
      "distance_km": 0.0,
      "elevation_m": 0,
      "type": "aid",
      "features": {
        "crew_access": true,
        "drop_bag": true,
        "full_aid": true,
        "water_only": false
      },
      "estimated_stop_seconds": 90,
      "available_supplies": ["water", "electrolytes", "gels", "food", "medical"],
      "cutoff_time": "HH:MM",
      "notes": "Crew instructions, specific features"
    }
  ],

  "aid_station_model": {
    "expected_stops_count": [0, 0],
    "median_stop_seconds": 0,
    "p90_stop_seconds": 0,
    "stop_time_multiplier": 1.0,
    "crew_stop_multiplier": 1.5,
    "notes": "General aid station strategy"
  },

  "navigation": {
    "marking_quality": "excellent | good | adequate | poor",
    "gps_track_required": false,
    "night_navigation_sections": [],
    "technical_navigation_sections": [],
    "notes": "Navigation strategy"
  },

  "key_segments": [
    {
      "name": "Segment Name",
      "start_km": 0.0,
      "end_km": 0.0,
      "description": "What makes this section notable",
      "difficulty_rating": "easy | moderate | hard | extreme",
      "key_challenges": ["Challenge 1", "Challenge 2"],
      "strategy_notes": "How to approach this section"
    }
  ],

  "simulation_defaults": {
    "fatigue_model": {
      "fatigue_inflection_km": 0,
      "fatigue_slope_multiplier": 1.0,
      "fatigue_per_km_base": 0.998,
      "notes": "When and how fast fatigue accumulates"
    },
    "field_effects": {
      "field_loss_multiplier_technical": 1.0,
      "field_loss_multiplier_weather": 1.0,
      "field_loss_multiplier_night": 1.0,
      "notes": "How you perform relative to field in different conditions"
    },
    "dnf_risk_factors": {
      "cutoff_pressure_sections": [],
      "high_dropout_sections": [],
      "notes": "Where runners typically struggle most"
    }
  },

  "validation_targets": {
    "expected_finish_time_band_hhmm": {
      "p10_elite": "HH:MM",
      "p25_strong": "HH:MM",
      "p50_competitive": "HH:MM",
      "p75_solid": "HH:MM",
      "p90_recreational": "HH:MM"
    },
    "athlete_specific_targets": {
      "fitness_1.0": "HH:MM",
      "fitness_1.15": "HH:MM",
      "fitness_1.30": "HH:MM"
    },
    "sanity_checks": [
      "Check 1",
      "Check 2"
    ]
  },

  "race_strategy": {
    "pacing_approach": "Description of smart pacing strategy",
    "nutrition_plan": "Recommended nutrition approach",
    "gear_requirements": {
      "mandatory": ["Item 1", "Item 2"],
      "recommended": ["Item 1", "Item 2"],
      "weather_dependent": ["Item 1", "Item 2"]
    },
    "mental_preparation": "Psychological considerations",
    "crew_strategy": "How to use crew effectively"
  }
}
```

---

## Aid Station Entry Fields

```json
{
  "name": "Checkpoint Name",
  "distance_km": 15.5,
  "elevation_m": 450,
  "type": "aid | crew | drop_bag | water_only | major_checkpoint",
  "features": {
    "crew_access": true,
    "drop_bag": true,
    "full_aid": true,
    "medical": false,
    "timing_checkpoint": true
  },
  "estimated_stop_seconds": 90,
  "target_stop_seconds": 60,
  "available_supplies": [
    "water",
    "electrolytes",
    "gels",
    "bars",
    "fruit",
    "salty_food",
    "hot_food",
    "medical",
    "blister_care"
  ],
  "cutoff_time": "10:30",
  "buffer_to_cutoff_min": 45,
  "cumulative_cutoff_time": "10:30",
  "crew_instructions": "What crew should prep",
  "athlete_checklist": ["Task 1", "Task 2"],
  "notes": "Specific considerations for this checkpoint"
}
```

### Field Descriptions

- **name**: Checkpoint identifier
- **distance_km**: Cumulative distance from start
- **elevation_m**: Elevation at checkpoint (useful for gear planning)
- **type**: Category of checkpoint
  - `aid`: Standard aid station
  - `crew`: Crew access allowed
  - `drop_bag`: Drop bag available
  - `water_only`: Minimal support
  - `major_checkpoint`: Key decision point
- **features**: Boolean flags for what's available
- **estimated_stop_seconds**: Realistic time you'll spend (includes creep)
- **target_stop_seconds**: Goal time (for discipline)
- **available_supplies**: What the race provides
- **cutoff_time**: Official race cutoff
- **crew_instructions**: Pre-planned crew actions
- **athlete_checklist**: Your specific tasks at this stop

---

## Quick Profile Creator Guide

### 1. Gather Course Data
- [ ] GPX file
- [ ] Elevation profile
- [ ] Official race information
- [ ] Historical results (for validation)
- [ ] Aid station locations and services

### 2. Classify Course Type
Use taxonomy above to identify primary course type and characteristics.

### 3. Calibrate Multipliers
- **Technical multiplier**: How much slower than road pace?
  - Smooth trail: 0.95-0.99
  - Moderate technical: 0.88-0.94
  - Very technical: 0.80-0.87
  - Extreme technical: 0.70-0.79

- **Fatigue inflection**: When does pace decay accelerate?
  - Short (<50km): Early (20-30km)
  - Medium (50-100km): Mid (40-60km)
  - Long (>100km): Late (80-120km)
  - Technical courses: Earlier than distance suggests

### 4. Map Aid Stations
- Plot all checkpoints
- Identify crew access points
- Plan drop bag contents
- Set realistic stop times (not optimistic!)

### 5. Validate Against Historical Data
- Check against your past races on similar terrain
- Compare to field results if available
- Adjust multipliers until predictions match reality

---

## Example: Converting Arc 25 to Enhanced Format

See next file: `arc_25_course_profile_v1_1_ENHANCED.json`
