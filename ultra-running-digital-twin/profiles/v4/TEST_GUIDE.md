# Digital Ultra Twin v4 - Test Guide

## Testing v4 Profile Loading with Arc 25 Prediction

This guide walks through testing the v4 modular profile loading and verifying accurate predictions.

### Test Objective

Verify that the v4 profile loads correctly in the main dashboard and produces an accurate prediction for the Arc of Attrition 25 race.

**Expected Result**: Prediction should be within 5 minutes of actual finish time (4:23).

---

## Test Steps

### 1. Open Main Dashboard

Open `tools/digital_twin_ultra_v3_rich.html` in a web browser.

### 2. Switch to v4 Mode

In the **Fitness** card:
- Click the **"v4 Modular"** button (should turn blue when selected)
- The UI will show three file upload buttons

### 3. Load v4 Profile Files

Upload the following files from `profiles/v4/`:

1. **📋 Athlete State** → `athlete_state.json`
   - Status should show: `✅ athlete_state.json`

2. **⚡ Performance Model** → `performance_model.json`
   - Status should show: `✅ performance_model.json`

3. **⚠️ Failure Model** (Optional) → `failure_model.json`
   - Status should show: `✅ failure_model.json`

### 4. Click "✅ Load v4 Profile"

**Expected Console Output:**
```
🚀 Loading v4 profile...
✅ Loaded steep_downhill: 5.92 km/h
✅ Loaded moderate_downhill: 6.96 km/h
✅ Loaded flat: 6.62 km/h
✅ Loaded moderate_uphill: 4.95 km/h
✅ Loaded steep_uphill: 3.71 km/h
✅ Loaded tech_skill from percentile gain: 1.15
✅ Loaded calibration factors: {...}
✅ Final ATHLETE speeds: {steep_d: 5.92, mod_d: 6.96, flat: 6.62, mod_u: 4.95, steep_u: 3.71}
✅ Final tech_skill: 1.15
```

**Expected Alert:**
```
✅ v4 Profile loaded successfully!

Speeds: {
  "steep_d": 5.92,
  "mod_d": 6.96,
  "flat": 6.62,
  "mod_u": 4.95,
  "steep_u": 3.71
}
```

### 5. Enter Race Parameters

In the **Race Details** card:

| Field | Value |
|-------|-------|
| Distance (km) | 41.6 |
| Total Elevation (m) | 1108 |
| Race Type | `technical_mountain_50_70k` |

### 6. Set Fitness Level

In the **Fitness** card:

| Field | Value |
|-------|-------|
| CTL | 159 |

**Expected**: Fitness multiplier should calculate to approximately **1.315**

### 7. Set Environmental Conditions

In the **Environmental Conditions** card:

| Field | Value |
|-------|-------|
| Temperature | 6°C (midpoint of 4-8°C range) |
| Terrain | `runnable_trail` |

### 8. View Prediction

Click **"⚡ Run Prediction"**

**Expected Prediction**: **4:20 - 4:30** (within 5-7 minutes of actual 4:23 finish)

---

## Verification Checklist

- [ ] v4 files load without errors
- [ ] Speeds display correctly in console (not defaults)
- [ ] Tech skill converts to 1.15x multiplier
- [ ] Calibration factor for `technical_mountain_50_70k` is 1.13
- [ ] CTL 159 converts to fitness ~1.315
- [ ] Prediction is close to actual result (4:23)

---

## Expected Values Summary

### Loaded from v4 Files

| Parameter | Source | Expected Value |
|-----------|--------|----------------|
| Steep Downhill Speed | `performance_model.gradient_speeds.steep_downhill.kmh.mean` | 5.92 km/h |
| Moderate Downhill Speed | `performance_model.gradient_speeds.moderate_downhill.kmh.mean` | 6.96 km/h |
| Flat Speed | `performance_model.gradient_speeds.flat.kmh.mean` | 6.62 km/h |
| Moderate Uphill Speed | `performance_model.gradient_speeds.moderate_uphill.kmh.mean` | 4.95 km/h |
| Steep Uphill Speed | `performance_model.gradient_speeds.steep_uphill.kmh.mean` | 3.71 km/h |
| Technical Skill | `athlete_state.technical_skill.relative_percentile_gain` | 15 → 1.15x |
| Calibration Factor | `performance_model.calibration.by_course_type.technical_mountain_50_70k` | 1.13 |

### Arc 25 Race Details

| Parameter | Value | Source |
|-----------|-------|--------|
| Distance | 41.6 km | race_context_arc25.json |
| Elevation | 1108 m | race_context_arc25.json |
| Actual CTL | 159 | race_context_arc25.json |
| Fitness Multiplier | 1.315 | race_context_arc25.json |
| Actual Finish Time | 4:23:XX | Historical race result |
| Temperature Range | 4-8°C | race_context_arc25.json |

---

## Troubleshooting

### Problem: Speeds still showing defaults

**Symptoms:**
```
✅ Final ATHLETE speeds: {steep_d: 5.92, mod_d: 6.96, flat: 6.62, mod_u: 4.95, steep_u: 3.71}
```
But these are still the template values, not loading from your actual profile.

**Solution:**
1. Check that `performance_model.json` contains your actual calibrated speeds
2. Verify the file structure matches: `gradient_speeds.{category}.kmh.mean`
3. Try the migration tool if migrating from v3

### Problem: Prediction way off (>15 minutes error)

**Possible causes:**
1. **Wrong calibration factor**: Check `performance_model.calibration.by_course_type` has correct race type
2. **Wrong fitness**: Verify CTL to fitness conversion matches your baseline
3. **Wrong race type selected**: Ensure you select the race type that matches your calibrated types

### Problem: Alert doesn't show or files don't load

**Check:**
1. Browser console for JavaScript errors
2. File format is valid JSON
3. Files are in correct v4 structure

---

## Comparison: v3 vs v4 Loading

### v3 (Old) Structure - PROBLEMATIC
```json
{
  "performance_by_gradient": {
    "steep_downhill": {
      "speed_kmh": 5.92  // ← Inconsistent property name
    }
  }
}
```

**Issues:**
- Property name `speed_kmh` was inconsistent
- Sometimes `kmh`, sometimes `mean`, sometimes `speed`
- Loading failed silently → defaulted to template speeds
- No way to know if loading succeeded

### v4 (New) Structure - RELIABLE
```json
{
  "gradient_speeds": {
    "steep_downhill": {
      "kmh": {
        "mean": 5.92,    // ← Explicit, unambiguous
        "p10": 5.4,
        "p90": 6.4
      }
    }
  }
}
```

**Benefits:**
- Explicit path: `gradient_speeds.{category}.kmh.mean`
- Probabilistic distributions included
- Clear structure prevents loading errors
- Console logs verify successful loading

---

## Notes

- The v4 architecture separates concerns: athlete data (slow-changing) from performance model (frequently calibrated)
- Technical skill percentile gain (+15) automatically converts to 1.15x multiplier
- Calibration factors from race history apply automatically based on race type
- Use the migration tool (`tools/migrate_v3_to_v4.html`) to convert existing v3 profiles

---

## Success Criteria

✅ **Test PASSED** if:
1. All v4 files load without errors
2. Speeds in console match `performance_model.json` values (not defaults)
3. Tech skill = 1.15
4. Prediction for Arc 25 is within 4:18 - 4:28 range (±5 min of 4:23 actual)

❌ **Test FAILED** if:
1. Speeds don't load (still showing defaults)
2. JavaScript errors in console
3. Prediction error >15 minutes
4. Calibration factors not applying

---

*Last Updated: 2026-01-22*
*Digital Ultra Twin v4.0*
