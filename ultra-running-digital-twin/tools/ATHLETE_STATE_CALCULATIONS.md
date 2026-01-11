# Athlete State Pane - Calculation Methodology

## Overview
The Athlete State pane answers the question: **"What version of you is turning up?"** by analyzing your comprehensive digital twin profile to assess readiness, capabilities, and potential limiting factors for the target race.

## Data Source
All calculations MUST use data from your uploaded Digital Twin Profile JSON file (`simbarashe_enhanced_profile_v3_3.json`), not simplified CTL inputs.

---

## 1. VO₂ Proxy Calculation

### Current Implementation (INCOMPLETE)
```javascript
const baseVO2 = 45;
const ctlFactor = Math.pow(ctlCurrent / 100, 0.3);
const effectiveVO2 = baseVO2 * ctlFactor * fitness;
```

**Problem**: Uses generic baseline and simple CTL scaling, ignoring actual race performance data.

### Proper Implementation (REQUIRED)
```javascript
// Extract from profile
const baseline_race = profile.fitness_baseline.baseline_race; // UTMB 2025
const recent_races = profile.athlete_info.racing_experience.race_history;
const fitness_level = profile.fitness_baseline.fitness_progression_targets;

// Calculate effective VO₂ from race performance
// Use GAP (Grade-Adjusted Pace) from recent races
// UTMB: 178km, 10267m, 38:04:32 = 4.67 km/h average
// Ultra Snowdonia: 58km, 2025m, 10:47:49 = 5.38 km/h average

// Estimate VO₂max from race performance using Daniels formula
// VO₂max ≈ speed_m/min * (0.2 + 0.9 * grade_fraction) + 3.5
// For ultras, use median_gap_speed_kmh from profile.performance_by_gradient.overall_metrics
const median_gap = profile.performance_by_gradient.overall_metrics.median_gap_speed_kmh; // 5.34 km/h
const vo2_estimate = (median_gap * 1000 / 60) * 0.2 + 3.5; // Simplified for ultra endurance

// Apply current fitness multiplier
const current_fitness = getCurrentFitnessLevel(); // From race date and training plan
const effectiveVO2 = vo2_estimate * current_fitness;
```

### Rating Categories
- **Novice**: <40 ml/kg/min
- **Recreational**: 40-48 ml/kg/min
- **Competitive**: 48-55 ml/kg/min
- **Elite**: 55-62 ml/kg/min
- **World-Class**: >62 ml/kg/min

For ultra-endurance athletes, VO₂max is less important than durability and efficiency.

---

## 2. Durability Score Calculation

### Current Implementation (INCOMPLETE)
```javascript
const durabilityScore = Math.min(100, Math.max(0, 30 + (ctlCurrent - 80) * 0.7));
```

**Problem**: Linear scaling from CTL only, no consideration of race history, training consistency, or validated performance degradation.

### Proper Implementation (REQUIRED)
```javascript
// Extract validated durability metrics from profile
const race_history = profile.athlete_info.racing_experience.race_history;
const fatigue_model = profile.model_parameters.critical_multipliers.fatigue_per_km; // 0.998
const fatigue_inflection = profile.model_parameters.thresholds.fatigue_inflection_km_sub80; // 58km

// Calculate durability from actual race performance
// UTMB 178km: Finished strong at 38h = excellent ultra durability
// Arc 42km: 4:23 = 9.6 km/h average, no major slowdown

// Durability metric: How much does pace decay over distance?
// Formula: pace_at_X_km / pace_at_start_km

// For UTMB:
const utmb_splits = analyzeRaceSplits(race_history.find(r => r.race === "UTMB 2025"));
// First 50km: ~5.5 km/h, Last 50km: ~4.2 km/h
// Decay rate = 4.2/5.5 = 0.76 (24% slowdown over 178km)

// Normalize to 100km for comparison
const decay_per_km = Math.pow(0.76, 1/178); // Per-km decay
const decay_at_100km = Math.pow(decay_per_km, 100); // 0.86 = 14% decay at 100km

// Durability Score (0-100 scale)
// 100 = no decay, 0 = complete failure
// 14% decay at 100km = 86 score (excellent for first ultra)
const durabilityScore = decay_at_100km * 100;

// Adjust for fitness progression
// Higher fitness = better durability due to lower relative effort
const fitness_adjustment = Math.min(1.2, current_fitness / baseline_fitness);
const adjusted_durability = Math.min(100, durabilityScore * fitness_adjustment);
```

### Key Factors
1. **Race distance experience**: Longer races = validated durability
2. **Pace degradation rate**: Slower decay = higher score
3. **Current fitness**: Higher fitness = better durability
4. **Recovery capability**: From `profile.physiological_profile.recovery_characteristics`

---

## 3. Pace Decay Projection

### Current Implementation (INCOMPLETE)
```javascript
const basePaceDecay = {
  '4h': 0,
  '8h': 100 - durabilityScore * 0.15,
  '12h': 100 - durabilityScore * 0.25,
  '12plus': 100 - durabilityScore * 0.40
};
```

**Problem**: Generic time-based decay, no race-specific calibration, ignores terrain and environmental factors.

### Proper Implementation (REQUIRED)
```javascript
// Use validated fatigue model from profile
const fatigue_per_km = profile.model_parameters.critical_multipliers.fatigue_per_km; // 0.998
const fatigue_inflection_km = profile.model_parameters.thresholds.fatigue_inflection_km_sub80; // 58km
const fatigue_slope_mult = profile.model_parameters.thresholds.fatigue_slope_multiplier_sub80; // 0.7

// Calculate expected pace at different distances
function calculatePaceAtDistance(distance_km, base_speed, profile) {
  let fatigue_multiplier = 1.0;

  if (distance_km <= fatigue_inflection_km) {
    // Linear decay before inflection
    fatigue_multiplier = Math.pow(fatigue_per_km, distance_km);
  } else {
    // Accelerated decay after inflection
    const pre_inflection_fatigue = Math.pow(fatigue_per_km, fatigue_inflection_km);
    const post_inflection_km = distance_km - fatigue_inflection_km;
    const post_inflection_fatigue = Math.pow(
      fatigue_per_km * fatigue_slope_mult,
      post_inflection_km
    );
    fatigue_multiplier = pre_inflection_fatigue * post_inflection_fatigue;
  }

  return base_speed * fatigue_multiplier;
}

// Convert distance to time based on expected pace
// For time horizons, estimate distance covered
const base_speed = getExpectedSpeed(profile, course_conditions);

// 4h: ~25-30km (depends on terrain)
const dist_4h = estimateDistanceAtTime(4, base_speed, course);
const pace_4h = calculatePaceAtDistance(dist_4h, base_speed, profile);

// 8h: ~50-60km
const dist_8h = estimateDistanceAtTime(8, base_speed, course);
const pace_8h = calculatePaceAtDistance(dist_8h, base_speed, profile);

// Display as percentage of baseline
const decay_4h = (pace_4h / base_speed * 100).toFixed(0);
const decay_8h = (pace_8h / base_speed * 100).toFixed(0);
```

### Factors Affecting Decay
1. **Distance-based fatigue**: From validated model
2. **Terrain technical factor**: Slower on technical = more fatigue
3. **Temperature**: Heat accelerates decay
4. **Altitude**: Hypoxia compounds fatigue
5. **Nutrition execution**: Poor nutrition = faster decay
6. **Respiratory incidents**: Can trigger sudden degradation

---

## 4. Downhill Resilience Index

### Current Implementation (INCOMPLETE)
```javascript
const descentTolerance = durabilityScore * 15; // Up to 1500m at max durability
const downhillResilience = Math.min(100, (descentTolerance / Math.max(totalDescent, 1)) * 100);
```

**Problem**: Generic tolerance calculation, ignores validated descending strength from race data.

### Proper Implementation (REQUIRED)
```javascript
// This athlete is a STRONG descender - use profile data
const downhill_rating = profile.performance_by_gradient.steep_downhill.strength_rating; // "excellent"
const downhill_speed = profile.performance_by_gradient.steep_downhill.base_speed_kmh; // 5.92 km/h
const moderate_downhill_speed = profile.performance_by_gradient.moderate_downhill.base_speed_kmh; // 6.96 km/h

// Compare to typical ultra runner
const typical_steep_downhill = 4.5; // km/h
const typical_moderate_downhill = 5.5; // km/h

// Strength index (>1.0 = better than average)
const steep_strength = downhill_speed / typical_steep_downhill; // 1.31 = 31% faster
const moderate_strength = moderate_downhill_speed / typical_moderate_downhill; // 1.26 = 26% faster

// Calculate resilience based on course descent profile
const course_descent_breakdown = analyzeDescent(course);
// { total: 3500m, steep: 1200m, moderate: 1800m, gentle: 500m }

// Weighted resilience score
// Steep descents cause more eccentric damage per meter
const steep_load = course_descent_breakdown.steep * 2.0;
const moderate_load = course_descent_breakdown.moderate * 1.0;
const gentle_load = course_descent_breakdown.gentle * 0.5;
const total_eccentric_load = steep_load + moderate_load + gentle_load;

// Athlete tolerance (higher for strong descenders)
const base_tolerance = 3000; // Average runner handles 3000m equivalent
const athlete_tolerance = base_tolerance * steep_strength; // 3930m equivalent

// Resilience index
const downhillResilience = Math.min(100, (athlete_tolerance / total_eccentric_load) * 100);

// Confidence modifier based on race history
if (profile.athlete_info.racing_experience.strengths.includes("Descending on steep technical sections")) {
  // Boost confidence for validated strength
  downhillResilience *= 1.1;
}
```

### Key Insights from Profile
- **Steep downhill**: 5.92 km/h (excellent) - 31% faster than average
- **Technical descending**: Listed as core strength
- **UK mountain experience**: Familiar with technical descents
- **Snowdonia**: Maintained pace despite twisted ankle on technical terrain

---

## 5. Quad Destruction Index (Eccentric Load)

### Current Implementation (PARTIALLY CORRECT)
```javascript
const gradientMultiplier = Math.abs(seg.grad) < 10 ? 1.0 :
                            Math.abs(seg.grad) < 20 ? 2.0 : 3.0;
eccentricLoadIndex += Math.abs(elevChange) * gradientMultiplier;
```

**Status**: Methodology is correct, but interpretation needs athlete context.

### Enhanced Implementation
```javascript
// Current calculation is good, enhance with athlete resilience
const quadDestructionIndex = eccentricLoadIndex / 1000;

// Adjust for athlete downhill strength
const athlete_downhill_resilience = getDownhillResilience(profile);
const adjusted_index = quadDestructionIndex / athlete_downhill_resilience;

// Warning thresholds (adjusted for strong descender)
// Normal athlete: >8 = extreme, >5 = high
// Strong descender: >10 = extreme, >7 = high
let warningColor, warningText;
if(adjusted_index > 10) {
  warningColor = '#dc2626';
  warningText = 'EXTREME - Even for strong descender, significant quad stress';
} else if(adjusted_index > 7) {
  warningColor = '#f59e0b';
  warningText = 'HIGH - Manageable with downhill strength but train accordingly';
} else if(adjusted_index > 4) {
  warningColor = '#3b82f6';
  warningText = 'MODERATE - Well within capability for strong descender';
} else {
  warningColor = '#10b981';
  warningText = 'LOW - Minimal eccentric stress for this profile';
}
```

### Training Recommendations
Based on profile, athlete handles technical descents well but should still train:
- Eccentric strength (squats, step-downs)
- Downhill running volume
- Quad endurance on steep terrain

---

## 6. Heat & Altitude Adaptation

### Current Implementation (INCOMPLETE)
```javascript
// Heat: Simple temperature thresholds
if(avgTemp > 25) heatAdaptation = 'HEAT STRESS';

// Altitude: Simple elevation thresholds
if(maxElevation > 2500) altitudeAdaptation = 'HIGH ALTITUDE';
```

**Problem**: Generic thresholds ignore athlete-specific tolerances and critical respiratory factors.

### Proper Implementation (REQUIRED)

#### Heat Adaptation
```javascript
// Extract validated temperature tolerances
const temp_optimal = profile.environmental_tolerances.temperature.optimal_range_c; // [12, 16]
const temp_thresholds = profile.environmental_tolerances.temperature;

const avgTemp = (startTemp + finishTemp) / 2;

// Use athlete-specific thresholds
if (avgTemp >= temp_thresholds.extreme_heat_c) { // 25°C
  heatAdaptation = '🔥 EXTREME HEAT - Performance severely degraded, consider DNS';
  heatColor = '#7f1d1d';
} else if (avgTemp >= temp_thresholds.heat_threshold_c) { // 22°C
  heatAdaptation = '⚠️ HEAT STRESS - Significant slowdown expected, heat acclimation critical';
  heatColor = '#dc2626';
} else if (avgTemp >= temp_thresholds.warm_acceptable_c) { // 18°C
  heatAdaptation = '⚡ Warm - Some heat stress, manage effort';
  heatColor = '#f59e0b';
} else if (avgTemp >= temp_optimal[0] && avgTemp <= temp_optimal[1]) { // 12-16°C
  heatAdaptation = '✓ OPTIMAL CONDITIONS - Peak performance possible';
  heatColor = '#10b981';
} else {
  // Cold conditions - CHECK RESPIRATORY PROFILE
  checkRespiratoryRisk(avgTemp, profile);
}
```

#### Respiratory Risk Assessment (CRITICAL)
```javascript
function checkRespiratoryRisk(avgTemp, profile) {
  const respiratory = profile.respiratory_profile;

  // This athlete has exercise-induced asthma - cold is PRIMARY limiter
  if (avgTemp <= respiratory.temperature_thresholds.extreme_danger_c) { // 5°C
    return {
      status: '🚨 EXTREME RESPIRATORY DANGER - DNS strongly recommended',
      color: '#7f1d1d',
      performance_multiplier: respiratory.cold_impact_validated["8_degrees_c"].performance_multiplier, // 0.8
      incident_probability: '90%+',
      mitigation: 'Race extremely risky. If racing, carry inhaler, conservative first 25km'
    };
  } else if (avgTemp <= respiratory.temperature_thresholds.high_risk_c) { // 8°C
    return {
      status: '⚠️ HIGH RESPIRATORY RISK - Conservative pacing essential',
      color: '#dc2626',
      performance_multiplier: 0.8,
      incident_probability: '60-70%',
      mitigation: 'Inhaler accessible, conservative km 3-25, monitor breathing closely'
    };
  } else if (avgTemp <= respiratory.temperature_thresholds.moderate_risk_c) { // 10°C
    return {
      status: '⚡ MODERATE RESPIRATORY RISK - Manage carefully',
      color: '#f59e0b',
      performance_multiplier: 0.88,
      incident_probability: '30-40%',
      mitigation: 'Warm-up thoroughly, use buff/gaiter, control HR in early km'
    };
  } else if (avgTemp <= respiratory.temperature_thresholds.low_risk_c) { // 12°C
    return {
      status: '⚠️ LOW RESPIRATORY RISK - Minor precautions',
      color: '#3b82f6',
      performance_multiplier: 0.93,
      incident_probability: '15-20%',
      mitigation: 'Standard warm-up, inhaler on hand'
    };
  } else {
    return {
      status: '✓ OPTIMAL RESPIRATORY CONDITIONS',
      color: '#10b981',
      performance_multiplier: 0.95,
      incident_probability: '<10%',
      mitigation: 'Minimal respiratory impact expected'
    };
  }
}
```

#### Altitude Adaptation
```javascript
// Extract altitude tolerances
const altitude_optimal = profile.environmental_tolerances.altitude.optimal_m; // [500, 1500]
const altitude_profile = profile.respiratory_profile.altitude_effect;

const maxElevation = Math.max(...course.map(seg => seg.ele));
const avgElevation = course.reduce((sum, seg) => sum + seg.ele, 0) / course.length;

// Time spent at altitude matters
const time_above_2000m = calculateTimeAtAltitude(course, 2000);

if (maxElevation > 3000) {
  altitudeAdaptation = '⚠️ VERY HIGH ALTITUDE - Acclimatization essential';
  altitudeColor = '#7f1d1d';
  altitude_multiplier = Math.pow(0.95, (maxElevation - 1000) / 1000); // Exponential penalty
} else if (maxElevation > 2500) {
  // From profile: "above_2500m": "Significant - compounds with cold/effort"
  altitudeAdaptation = '⚠️ HIGH ALTITUDE - Pre-acclimatization critical';
  altitudeColor = '#dc2626';
  altitude_multiplier = 0.93; // ~7% penalty
} else if (maxElevation > 2000) {
  altitudeAdaptation = '⚡ Moderate altitude - Some acclimatization beneficial';
  altitudeColor = '#f59e0b';
  altitude_multiplier = 0.95; // 5% penalty (from profile)
} else if (maxElevation > 1500) {
  altitudeAdaptation = '✓ Elevated - Minor hypoxic effect';
  altitudeColor = '#3b82f6';
  altitude_multiplier = 0.98;
} else {
  altitudeAdaptation = '✓ Low altitude - No adaptation needed';
  altitudeColor = '#10b981';
  altitude_multiplier = 1.0;
}

// CRITICAL: Compound altitude with respiratory risk
if (avgTemp < 10 && maxElevation > 2000) {
  showCompoundedRiskWarning('COLD + ALTITUDE = SEVERE RESPIRATORY RISK');
}
```

---

## Summary: What Data Drives Each Metric

| Metric | Current Source | Should Use From Profile |
|--------|---------------|--------------------------|
| **VO₂ Proxy** | Generic 45 + CTL | `performance_by_gradient.overall_metrics.median_gap_speed_kmh` + race performance |
| **Durability** | Linear CTL scaling | `race_history` pace degradation + `model_parameters.critical_multipliers.fatigue_per_km` |
| **Pace Decay** | Generic time-based | `thresholds.fatigue_inflection_km_sub80` + `fatigue_slope_multiplier_sub80` |
| **Downhill Resilience** | CTL × 15 | `performance_by_gradient.steep_downhill.base_speed_kmh` + strength rating |
| **Quad Destruction** | Generic thresholds | Current methodology OK, adjust thresholds for strong descender |
| **Heat Adaptation** | Generic 25°C | `environmental_tolerances.temperature` - athlete-specific thresholds |
| **Altitude Adaptation** | Generic 2500m | `respiratory_profile.altitude_effect` + time-at-altitude consideration |
| **Respiratory Risk** | ❌ NOT CALCULATED | **CRITICAL**: `respiratory_profile.cold_impact_validated` + temperature thresholds |

---

## Critical Missing Elements

### 1. Respiratory Risk Assessment
**HIGHEST PRIORITY** - This is the PRIMARY performance limiter for this athlete.

Should display:
- Current temperature risk level
- Incident probability based on validated data
- Performance multiplier (0.8-0.95)
- Vulnerable zone warning (km 3-25)
- Specific mitigation strategies
- DNS recommendation if conditions too dangerous

### 2. Technical Terrain Advantage
Should display:
- Course technical rating
- Expected competitive advantage (+15 percentile on technical terrain)
- Relative time gain/loss vs field

### 3. Fitness Progression Context
Should display:
- Current fitness level (e.g., 1.15)
- Baseline fitness reference (UTMB 2025 = 1.0)
- Target fitness for this race
- Gap to target

---

## Implementation Priority

1. **Add profile upload interface** - REQUIRED to access real data
2. **Implement respiratory risk assessment** - CRITICAL safety feature
3. **Update durability calculation** - Use validated race data
4. **Update pace decay** - Use validated fatigue model
5. **Update heat/altitude** - Use athlete-specific thresholds
6. **Update downhill resilience** - Reflect validated strength
7. **Add VO₂ proxy** - Use race performance data
8. **Add technical terrain analysis** - Show competitive advantage

## File References

- **Profile**: `/ultra-running-digital-twin/data/profiles/simbarashe_enhanced_profile_v3_3.json`
- **Tool**: `/ultra-running-digital-twin/tools/digital_twin_ultra_v2.html`
- **This Doc**: `/ultra-running-digital-twin/tools/ATHLETE_STATE_CALCULATIONS.md`
