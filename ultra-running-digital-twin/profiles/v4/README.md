# Digital Ultra Twin v4.0 - Modular Architecture

## Overview

Version 4.0 introduces a modular file architecture that separates concerns and enables safer iteration, clearer simulations, and future automation.

## File Structure

### Core Files (Required)

1. **athlete_state.json** - Slow-changing athlete truth
   - Physiology (VO2max, HR zones, running economy)
   - Respiratory profile
   - Technical skill
   - Injury history

2. **performance_model.json** - Performance parameters
   - Gradient speeds with distributions (p10, mean, p90)
   - Terrain multipliers
   - Environmental penalties
   - Fatigue model
   - Calibration factors

3. **failure_model.json** - Realistic failure modes
   - Respiratory incidents
   - Nutrition failures (bonking, GI distress)
   - Musculoskeletal risks
   - Probabilities and impacts

### Supporting Files (Optional)

4. **race_context_*.json** - Event-specific disposable files
   - Race details
   - Expected conditions
   - Goals and strategy
   - Risk flags

5. **uncertainty.json** - Variance and confidence levels
   - Physiological uncertainties
   - Performance variances
   - Environmental forecast errors

6. **counter_hypotheses.json** - Falsifiable claims
   - Model assumptions
   - Evidence for/against
   - Disproving criteria

## Key Improvements Over v3

### 1. Clean Separation of Concerns
- **v3**: Monolithic JSON with mixed concerns
- **v4**: Modular files with single responsibilities

### 2. Speed Loading Fixed
- **v3**: `performance_by_gradient.{category}.speed_kmh` (inconsistent)
- **v4**: `gradient_speeds.{category}.kmh.mean` (explicit structure)

### 3. Probabilistic Modeling
- p10/mean/p90 distributions for all speeds
- Failure mode probabilities
- Uncertainty quantification

### 4. Falsifiability
- Counter-hypotheses explicitly stated
- Disproving criteria defined
- Evidence tracking built-in

## Usage

### Loading in Tools

```javascript
// Load all required files
const athleteState = await loadJSON('athlete_state.json');
const performanceModel = await loadJSON('performance_model.json');
const failureModel = await loadJSON('failure_model.json');

// Optional: load race context
const raceContext = await loadJSON('race_context_chianti74k.json');

// Access speeds correctly
const flatSpeed = performanceModel.gradient_speeds.flat.kmh.mean;  // 6.62
const techSkill = athleteState.technical_skill.relative_percentile_gain;  // 15
```

### Calibration Workflow

1. Run races and collect data
2. Update `performance_model.json` calibration section
3. Adjust gradient speeds if needed
4. Leave `athlete_state.json` stable unless physiological changes

### Race Planning Workflow

1. Create new `race_context_<race>.json`
2. Load athlete + performance + failure models
3. Run Monte Carlo simulations
4. Output predictions with uncertainty bands

## Migration from v3

To convert a v3 profile to v4:

1. **athlete_state.json** ← v3: `athlete_info`, `respiratory_profile`, `technical_terrain_capability`
2. **performance_model.json** ← v3: `performance_by_gradient`, `calibration`
3. **failure_model.json** ← New structure (extract from v3 narrative)
4. **race_context_*.json** ← v3: individual race from `race_history`

## File Locations

```
profiles/v4/
├── athlete_state.json              # Core: slow-changing truth
├── performance_model.json          # Core: speeds and calibration
├── failure_model.json              # Core: failure probabilities
├── uncertainty.json                # Optional: variance model
├── counter_hypotheses.json         # Optional: falsifiable claims
├── race_context_arc25.json         # Disposable: event-specific
├── race_context_chianti74k.json    # Disposable: event-specific
└── README.md                        # This file
```

## Version History

- **v4.0** (2026-01-22): Modular architecture, probabilistic modeling
- **v3.0** (2025-01-15): Monolithic profile with calibration
- **v2.0** (2024-06-01): Basic digital twin
- **v1.0** (2023-12-01): Initial model

## Next Steps

1. Update web tools to load v4 files
2. Add multi-file loader UI
3. Implement failure mode simulation
4. Add prediction uncertainty bands
5. Create v3 → v4 migration tool
