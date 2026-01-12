# Digital Ultra Twin - Tools

Browser-based and command-line tools for ultra-running race prediction.

## 🎯 Tools Overview

### 1. `digital_twin_ultra_v2.html` - Interactive Race Prediction Tool
**Main browser-based prediction system with 6 analysis panes**

#### Features
- **Outcome Forecast**: Monte Carlo simulation with finish time distribution (P10-P90)
- **Course Interaction**: Terrain analysis, elevation visualization, athlete-course matching
- **Athlete State**: Fitness snapshot, VO₂ max, pace decay, durability metrics
- **Respiratory Risk**: Temperature-based asthma risk modeling with management protocols
- **Execution Risk**: Self-sabotage analysis (pacing errors, aid station creep, failure patterns)
- **Decision Triggers**: Tactical framework (pace caps, fuel timing, walk/run rules, abort criteria)

#### Usage
```bash
# Open in browser
open digital_twin_ultra_v2.html

# Or use a local server
python3 -m http.server 8000
# Navigate to: http://localhost:8000/digital_twin_ultra_v2.html
```

**Input:**
1. Upload athlete profile JSON (`../data/profiles/simbarashe_enhanced_profile_v3_3.json`)
2. Upload course profile JSON (`../data/courses/arc_25_course_profile_v1_1_ENHANCED.json`)
3. Set parameters: fitness level, temperature, conditions
4. Click "Run Analysis"

**Output:**
- 6 interactive panes with detailed predictions
- Finish time distributions with confidence intervals
- Risk assessments and tactical recommendations
- Segment-by-segment breakdowns

---

### 2. `run_prediction.js` - Command Line Prediction Runner
**Node.js script for automated predictions**

#### Features
- All 6 analysis panes from browser tool
- Command-line output with formatted tables
- Scriptable for batch predictions
- Validation against historical results

#### Usage
```bash
node run_prediction.js \
  --athlete=../data/profiles/simbarashe_enhanced_profile_v3_3.json \
  --course=../data/courses/arc_25_course_profile_v1_1_ENHANCED.json \
  --fitness=1.15 \
  --temp=6
```

**Parameters:**
- `--athlete`: Path to athlete profile JSON (required)
- `--course`: Path to course profile JSON (required)
- `--fitness`: Fitness multiplier (default: 1.15)
- `--temp`: Average temperature in Celsius (default: 6)
- `--conditions`: Weather conditions (default: "dry")

**Example Output:**
```
================================================================================
DIGITAL TWIN ULTRA - RACE PREDICTION
================================================================================

Athlete: Simbarashe
Race: Arc of Attrition 25 (40km)
Fitness: 1.15 (CTL: 138)
Conditions: 6°C, dry

PREDICTED FINISH TIME DISTRIBUTION:
  P10 (Best case):      4:37:40
  P25 (Strong day):     4:52:46
  P50 (Expected):       5:09:20 ⟵ Most likely
  P75 (Tough day):      5:25:55
  P90 (Survival mode):  5:41:01

⚡ Early Pacing Deviation Risk: 30% (LOW)
⏱️  Aid Station Dwell Time Creep: 2.7 min
🌙 Night Cognitive Load Index: 0%
⚠️  Previous Failure Pattern Overlap: 0%

[... Full tactical framework, segment breakdown, and athlete state ...]
```

---

### 3. `course_profile_builder.html` - Interactive Course Profile Creator
**HTML form for building course profile JSON files**

#### Features
- Interactive form with all course profile fields
- Dynamic aid station creation (add/remove unlimited entries)
- Dynamic key segments (add/remove sections)
- JSON generation with validation
- Copy to clipboard or download as file
- Pre-loads with one aid station and segment for easier start

#### Usage
```bash
open course_profile_builder.html
```

**Workflow:**
1. Fill in course metadata (race name, distance, elevation, region, course type)
2. Set environment profile (temperature, altitude, wind, precipitation)
3. Define terrain profile (surface mix, technicality, runnability)
4. Add aid stations:
   - Click "+ Add Aid Station"
   - Fill in: name, distance, elevation, type
   - Set features: crew access, drop bag, full aid, medical
   - Add stop times, cutoffs, crew instructions, notes
5. Add key segments:
   - Click "+ Add Segment"
   - Fill in: name, distance range, difficulty, challenges, strategy
6. Click "Generate JSON"
7. Copy to clipboard or download file

**Output:**
- Properly formatted course profile JSON
- Auto-named file: `{race_id}_course_profile_v1_0.json`
- Ready to use with prediction tools

---

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│  INPUTS                                                      │
├─────────────────────────────────────────────────────────────┤
│  1. Athlete Profile JSON                                    │
│     - Physiological data (VO₂, HR zones, respiratory)       │
│     - Fitness baseline (CTL, training load)                 │
│     - Performance calibration (race results, strengths)     │
│                                                              │
│  2. Course Profile JSON                                     │
│     - Metadata (distance, elevation, course type)           │
│     - Environment (temperature, altitude, wind)             │
│     - Terrain (surface, technicality, runnability)          │
│     - Aid stations (locations, cutoffs, services)           │
│     - Key segments (difficulty, challenges, strategy)       │
│                                                              │
│  3. Race Parameters                                         │
│     - Fitness level (1.0-1.5+)                             │
│     - Temperature (°C)                                      │
│     - Conditions (dry/wet)                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PREDICTION ENGINE                                          │
├─────────────────────────────────────────────────────────────┤
│  • Monte Carlo simulation (500 iterations)                  │
│  • Fatigue modeling (inflection points, decay curves)       │
│  • Respiratory risk assessment                              │
│  • Execution risk analysis                                  │
│  • Tactical decision generation                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUTS                                                     │
├─────────────────────────────────────────────────────────────┤
│  • Finish time distribution (P10, P25, P50, P75, P90)      │
│  • Risk scores (pacing, aid station, night, failure)       │
│  • Tactical framework (pace caps, fuel timing, rules)      │
│  • Segment-by-segment breakdown                            │
│  • Validation against historical results                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧬 Key Calculations

### Outcome Forecast
```javascript
// Validated baseline
baselineTime = validatedArc2025Time * (validatedFitness / 1.0)

// Adjust for current fitness
estimatedMovingTime = baselineTime / currentFitness

// Apply penalties
totalTime = movingTime × (1 + fatiguePenalty) + aidStops + respiratoryPenalty

// Monte Carlo distribution
stdDev = totalTime × 0.08  // 8% variation
P50 = totalTime
P10 = totalTime - 1.28 × stdDev
P90 = totalTime + 1.28 × stdDev
```

### Execution Risk
```javascript
// Early Pacing Deviation Risk
pacingRisk = 50  // baseline
if (strengths.includes("Pacing discipline")) pacingRisk -= 20
if (weaknesses.includes("Going out too fast")) pacingRisk += 25
if (runnability > 0.7) pacingRisk += 15  // runnable terrain tempts

// Aid Station Dwell Time Creep
earlyStopAvg = medianStopSeconds
lateStopAvg = medianStopSeconds × 1.5  // 50% degradation
creepMinutes = totalCreep - targetTotal

// Night Cognitive Load Index
nightLoadIndex = (nightHours / raceDurationHours) × 100

// Failure Pattern Overlap
if (temp <= respiratoryDangerThreshold) failureOverlap += 60
if (courseType matches pastDNFPattern) failureOverlap += 20
```

### Respiratory Risk
```javascript
// Temperature thresholds
if (temp <= 5°C):  penalty = 0.25, risk = "EXTREME", recommendation = "DNS"
if (temp <= 8°C):  penalty = 0.15, risk = "HIGH", recommendation = "Very conservative"
if (temp <= 10°C): penalty = 0.08, risk = "MODERATE", recommendation = "Inhaler ready"
if (temp <= 12°C): penalty = 0.03, risk = "LOW", recommendation = "Normal precautions"
else:              penalty = 0.00, risk = "MINIMAL", recommendation = "Standard"

// Vulnerable zone (km 3-25)
if (inVulnerableZone) applyFullPenalty
else applyHalfPenalty
```

---

## 📁 File Formats

### Athlete Profile JSON Structure
```json
{
  "athlete_info": {
    "name": "Simbarashe",
    "racing_experience": {
      "strengths": ["Pacing discipline", "Technical descending"],
      "weaknesses": ["Cold sensitivity"],
      "past_dnfs": []
    }
  },
  "physiological_profile": {
    "aerobic_capacity": {
      "vo2_max_ml_kg_min": 57,
      "source": "Whoop",
      "rating": "Elite"
    },
    "heart_rate": {
      "zone_2_max": 145,
      "zone_3_max": 155,
      "zone_4_max": 165
    }
  },
  "fitness_baseline": {
    "training_load": {
      "ctl_utmb_2025": 120,
      "ctl_arc_2025": 138
    }
  },
  "respiratory_profile": {
    "temperature_risk_bands": {
      "extreme_danger_c": 5,
      "high_risk_c": 8,
      "moderate_risk_c": 10,
      "low_risk_c": 12
    }
  }
}
```

### Course Profile JSON Structure
```json
{
  "course_metadata": {
    "race_id": "arc_25",
    "race_name": "Arc of Attrition 25",
    "distance_km": 40.0,
    "elevation_gain_m": 2300,
    "course_type": "technical_coastal_trail",
    "start_time": "08:00",
    "cutoff_hours": 12.0
  },
  "environment_profile": {
    "temperature_band_c": [4, 12],
    "altitude_band_m": [0, 300]
  },
  "terrain_profile": {
    "surface_mix": {
      "paved_pct": 15,
      "singletrack_pct": 30,
      "rocky_technical_pct": 40
    },
    "technicality": {
      "dry_multiplier": 0.92,
      "light_rain_multiplier": 0.88
    },
    "runnability": {
      "runnable_fraction_estimate": 0.45
    }
  },
  "aid_stations": [
    {
      "name": "CP2 - Crackington Haven",
      "distance_km": 16.0,
      "elevation_m": 15,
      "type": "crew",
      "features": {
        "crew_access": true,
        "drop_bag": true,
        "full_aid": true,
        "medical": true
      },
      "estimated_stop_seconds": 90,
      "target_stop_seconds": 60,
      "cutoff_time": "11:45",
      "crew_instructions": "Have backup inhaler ready",
      "athlete_checklist": ["Refill", "Blister check", "Layer adjustment"]
    }
  ],
  "simulation_defaults": {
    "fatigue_model": {
      "fatigue_inflection_km": 22,
      "fatigue_slope_multiplier": 1.25
    }
  }
}
```

---

## 🎨 UI Features (Browser Tool)

### Glassmorphism Design
- Frosted glass cards with blur effect
- Gradient backgrounds
- Smooth animations
- Responsive layout

### Interactive Elements
- File upload for athlete/course profiles
- Dropdown selectors for pacing strategy
- Sliders for fitness level
- Temperature input
- Condition toggles

### Analysis Panes
Each pane is collapsible and includes:
- Header with icon and description
- Formatted metrics with units
- Color-coded risk levels (green/yellow/red)
- Explanatory notes and recommendations

---

## 🔧 Customization

### Adding New Course Types
Edit course profile or use builder form. Available types:
1. runnable_trail_hilly
2. technical_coastal_trail
3. alpine_ultra
4. mountain_sky_running
5. desert_ultra
6. forest_trail_moderate
7. fell_running_uk
8. road_ultra
9. gravel_ultra
10. canyon_technical
11. night_only_ultra
12. multi_loop_course

### Tuning Multipliers
Key parameters in course profiles:
- `dry_multiplier`: Terrain speed adjustment (0.75-1.0)
- `fatigue_inflection_km`: When pace decay accelerates
- `fatigue_slope_multiplier`: Decay aggressiveness (0.5-2.0)
- `field_loss_multiplier_technical`: Your performance vs field

---

## 📊 Validation

### Arc 25 Validation
- **Predicted (P50)**: 5:09:20 (with conservative respiratory penalty)
- **Actual**: 4:23:00
- **Error**: +17.6% (includes 15% respiratory safety margin)
- **Without penalties**: ~4:30 predicted vs 4:23 actual = 2.7% error

### Future Validation
- Remove safety margins once respiratory management proven
- Calibrate against more races
- Tune technical multipliers per course type

---

## 🚀 Future Enhancements

- [ ] Weather API integration
- [ ] GPX file import for elevation profiling
- [ ] Live race tracking mode
- [ ] Mobile-responsive design
- [ ] Export predictions to PDF
- [ ] Integration with Strava/TrainingPeaks
- [ ] Multi-race comparison tool
- [ ] Training plan generator

---

## 📝 Notes

- All tools use vanilla JavaScript (no dependencies for browser tools)
- CLI tool requires Node.js (tested with v22.21.1)
- Profiles use comprehensive JSON schemas
- Conservative bias in predictions (better to overestimate than underestimate)

---

**Last Updated:** January 2026
**Version:** 2.0
**Author:** Simbarashe
