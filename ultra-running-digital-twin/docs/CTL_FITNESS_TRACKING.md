# CTL Fitness Tracking System

## Overview

The CTL (Chronic Training Load) Fitness Tracking system integrates Training Peaks CTL values with the Digital Twin race prediction engine. This allows you to:

1. **Track fitness over time** using your actual Training Peaks CTL values
2. **Convert CTL to fitness multipliers** for race predictions
3. **Calculate fitness progression** to race day based on training plans
4. **Run interactive predictions** with custom or predicted fitness levels

## Key Concepts

### CTL (Chronic Training Load)

CTL is a rolling 42-day average of your daily training stress score (TSS) from Training Peaks. It represents your long-term fitness level.

### Fitness Multiplier

The Digital Twin uses a fitness multiplier to adjust predicted race speeds. The system converts CTL values to fitness multipliers using calibrated data:

- **CTL 120** = Fitness **1.0** (UTMB 2025 baseline)
- **CTL 138** = Fitness **1.15** (Arc 2025 performance)
- **CTL 187** = Fitness **1.56** (UTMB 2025 peak)

### Conversion Formula

```python
fitness = 1.0 + ((CTL - 120) * 0.00833)
```

## Usage

### 1. Quick Conversion Table

Run the conversion table example:

```bash
cd examples
python3 ctl_progression_example.py
```

This shows:
- CTL to fitness conversions
- Speed impact percentages
- Three training progression scenarios

### 2. Interactive Race Prediction

Run the interactive prediction script:

```bash
cd examples
python3 interactive_ctl_prediction.py
```

This allows you to:
1. Input your current CTL from Training Peaks
2. Choose between current fitness or predicted race-day fitness
3. Select a training plan (conservative/moderate/aggressive)
4. See fitness progression calculations
5. Run race prediction with the selected fitness level

### 3. Programmatic Usage

```python
from src.ctl_fitness_tracker import CTLFitnessTracker

# Initialize tracker
tracker = CTLFitnessTracker(data_file='data/fitness/ctl_history.json')

# Convert CTL to fitness
current_ctl = 106
fitness = tracker.ctl_to_fitness(current_ctl)
print(f"CTL {current_ctl} = Fitness {fitness:.3f}")

# Predict progression to race day
progression = tracker.predict_ctl_progression(
    current_ctl=106,
    current_date='2026-01-08',
    race_date='2026-03-08',
    training_plan='moderate'
)

# Display progression table
tracker.print_progression_table(progression)
```

## Training Plans

### Conservative (2.5 CTL/week)
- **Best for:** Injury recovery, returning from break, cautious approach
- **Risk:** Low
- **Example:** CTL 106 → 118 in 8 weeks

### Moderate (3.5 CTL/week)
- **Best for:** Balanced progression, sustainable build
- **Risk:** Medium
- **Example:** CTL 106 → 124 in 8 weeks

### Aggressive (5.0 CTL/week)
- **Best for:** Experienced athletes, short timeline, high risk tolerance
- **Risk:** High (injury risk)
- **Example:** CTL 106 → 134 in 8 weeks

## CTL History Management

### Data File Location

`data/fitness/ctl_history.json`

### Adding Records

```python
tracker.add_ctl_record(
    date='2026-01-08',
    ctl=106,
    event_name='Current',
    notes='Base training phase'
)

tracker.save_history('data/fitness/ctl_history.json')
```

### Manual Editing

You can also edit `ctl_history.json` directly:

```json
{
  "ctl_history": [
    {
      "date": "2026-01-08",
      "ctl": 106,
      "event_name": "Current",
      "notes": "Base training phase"
    }
  ],
  "last_updated": "2026-01-08 00:00:00"
}
```

## Example: Your Current Scenario

### Current State
- **Date:** January 8, 2026
- **Current CTL:** 106
- **Current Fitness:** 0.88
- **Historical Peak:** CTL 187 (UTMB 2025)

### Race Target
- **Race:** Chianti Ultra Trail 74K
- **Date:** March 8, 2026
- **Weeks to race:** 8.4

### Progression Options

| Training Plan | Race Day CTL | Race Day Fitness | Time Improvement* |
|--------------|--------------|------------------|-------------------|
| Conservative | 118          | 0.98             | ~66 minutes       |
| Moderate     | 124          | 1.04             | ~101 minutes      |
| Aggressive   | 134          | 1.12             | ~153 minutes      |

*Compared to current fitness level (CTL 106)

### Recommended Approach

**Moderate training plan** (3.5 CTL/week):
- Build for 6.4 weeks → Peak CTL 128 (Fitness 1.07)
- Taper for 2 weeks → Race CTL 124 (Fitness 1.04)
- Expected improvement: ~1.7 hours faster than current fitness

## Files

```
ultra-running-digital-twin/
├── src/
│   └── ctl_fitness_tracker.py          # Core CTL tracking module
├── data/
│   └── fitness/
│       └── ctl_history.json             # Your CTL history data
├── examples/
│   ├── interactive_ctl_prediction.py    # Interactive prediction script
│   └── ctl_progression_example.py       # Example scenarios
└── docs/
    └── CTL_FITNESS_TRACKING.md          # This file
```

## Tips

1. **Update CTL regularly:** Add weekly CTL snapshots to track your progression
2. **Be realistic:** Choose a training plan that matches your recovery capacity
3. **Monitor fatigue:** High CTL doesn't help if you're overtrained
4. **Taper properly:** The system assumes a 2-week taper (-2 CTL/week)
5. **Use custom values:** If you know your fitness is different than predicted, use option 3 in the interactive script

## Calibration Notes

The CTL-to-fitness conversion is calibrated against your actual race performances:

- **UTMB 2025** (38:04:32, CTL 187): Used as peak fitness reference
- **Arc of Attrition 2025** (4:23:00, CTL 138): Validated fitness 1.15
- **Base fitness** (CTL 120): UTMB preparation baseline

As you complete more races with known CTL values, you can refine the conversion formula for even more accurate predictions.

## Next Steps

1. Run `ctl_progression_example.py` to see your progression scenarios
2. Use `interactive_ctl_prediction.py` to run predictions with different fitness levels
3. Update `ctl_history.json` with your current Training Peaks CTL
4. Experiment with different training plans to find the optimal approach
