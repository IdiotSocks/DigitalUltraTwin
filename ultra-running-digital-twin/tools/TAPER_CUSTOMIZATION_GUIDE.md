# CTL Taper Customization Guide

## Overview
The updated CTL tracker now supports **customizable taper settings**, allowing you to model different taper strategies for your race.

## New Features

### 1. Taper Toggle
- **Enable/Disable taper** with a checkbox
- When disabled, you race at peak CTL (no taper)
- When enabled, you get full taper controls

### 2. Taper Duration
Choose from:
- **0.5 weeks** - Ultra-short taper
- **1 week** - Light taper (your preference)
- **1.5 weeks** - Medium taper
- **2 weeks** - Standard taper (default)
- **3 weeks** - Long taper

### 3. Taper Intensity
Choose how much you reduce training:
- **80%** - Light reduction (maintain most volume)
- **70%** - Moderate reduction
- **60%** - Standard reduction (default)
- **50%** - Heavy reduction
- **40%** - Very heavy reduction (aggressive taper)

## How Taper Works

### The Math
During taper, your CTL drops based on:
```
CTL Loss per Week = Weekly Gain × (1 - Taper Intensity)
```

**Example:** Your case (1 week @ 60% intensity)
- Training plan: Moderate (3.5 CTL/week gain)
- Taper intensity: 60% (reducing to 60% of normal volume)
- CTL loss: 3.5 × (1 - 0.6) = **1.4 CTL per week**

So with 1 week taper, you'd lose 1.4 CTL from your peak.

### Comparison

**Your Upcoming Race Setup:**
```
Current CTL: 106
Weeks to race: 8
Training plan: Moderate (+3.5 CTL/week)
Taper: 1 week @ 60% intensity

Build phase: 7 weeks → Peak CTL = 106 + (7 × 3.5) = 130.5
Taper phase: 1 week → Loss = 1.4 CTL
Race day CTL: 130.5 - 1.4 = 129.1
Race day fitness: 1.076
```

**vs. Standard 2-week Taper:**
```
Build phase: 6 weeks → Peak CTL = 106 + (6 × 3.5) = 127
Taper phase: 2 weeks → Loss = 2.8 CTL
Race day CTL: 127 - 2.8 = 124.2
Race day fitness: 1.035
```

**Result:** Your light 1-week taper gives you **4.9 higher CTL** on race day!

## Usage Examples

### Example 1: Your Upcoming Race (Light 1-Week Taper)

**Settings:**
- ✅ Enable Taper
- Taper Weeks: **1 week**
- Taper Intensity: **60%** (reducing to 60% of normal)

**What this means:**
- You maintain 60% of your training volume in the final week
- CTL drops slightly but you stay sharp
- Good for shorter races or when you need to maintain fitness

---

### Example 2: Standard 2-Week Taper (Default)

**Settings:**
- ✅ Enable Taper
- Taper Weeks: **2 weeks**
- Taper Intensity: **60%**

**What this means:**
- Classic taper approach
- More recovery time
- Better for longer ultra races (100km+)

---

### Example 3: No Taper (Peak Race)

**Settings:**
- ❌ Disable Taper

**What this means:**
- Race at peak CTL
- No fitness loss
- Useful for modeling "what if I raced today at peak?"

---

### Example 4: Aggressive 3-Week Taper

**Settings:**
- ✅ Enable Taper
- Taper Weeks: **3 weeks**
- Taper Intensity: **40%** (very heavy reduction)

**What this means:**
- Long recovery period
- Significant CTL drop
- Good for very long races (100 miles+) or if you're overtrained

---

## Quick Reference: Taper Strategies by Race Distance

| Race Distance | Recommended Taper | Intensity | Notes |
|--------------|-------------------|-----------|-------|
| **50km** | 0.5-1 week | 70-80% | Stay sharp, minimal recovery |
| **50 miles** | 1-1.5 weeks | 60-70% | Light taper, maintain fitness |
| **100km** | 1.5-2 weeks | 60% | Standard approach |
| **100 miles** | 2-3 weeks | 50-60% | Longer recovery needed |
| **200km+** | 2-3 weeks | 40-50% | Maximum recovery |

## How to Update Your HTML

### Replace the CTL Card Section

1. **Find** your existing CTL Fitness Tracker card (the one you added earlier)
2. **Replace** it with the code from `html_ctl_with_taper.html`
3. **Test** by toggling taper on/off and changing values

### What Changed

**Old version:**
- Fixed 2-week taper
- Fixed -2 CTL/week loss
- No customization

**New version:**
- ✅ Toggle taper on/off
- ✅ Choose taper duration (0.5-3 weeks)
- ✅ Choose taper intensity (40-80%)
- ✅ See build weeks separately
- ✅ Live description of taper effect

## Testing Your Settings

After updating, try these scenarios:

### Test 1: Your Light Taper
```
Current CTL: 106
Race Date: 1 week from now
Training Plan: Moderate
✅ Enable Taper
Taper Weeks: 1
Taper Intensity: 60%

Expected Result:
- Build Weeks: 0
- Peak CTL: 106
- Race Day CTL: ~104.6
- Description: "Reducing to 60% load (-1.4 CTL/week)"
```

### Test 2: No Taper
```
Current CTL: 106
Race Date: 8 weeks from now
Training Plan: Moderate
❌ Disable Taper

Expected Result:
- Build Weeks: 8.0
- Peak CTL: 134
- Race Day CTL: 134 (same as peak)
- Description: "No taper - racing at peak CTL"
```

### Test 3: Standard Taper
```
Current CTL: 106
Race Date: 8 weeks from now
Training Plan: Moderate
✅ Enable Taper
Taper Weeks: 2
Taper Intensity: 60%

Expected Result:
- Build Weeks: 6.0
- Peak CTL: 127
- Race Day CTL: 124.2
- Description: "Reducing to 60% load (-1.4 CTL/week)"
```

## Troubleshooting

**Q: Taper settings not showing?**
- Make sure you checked "Enable Taper"
- Check that `toggleTaperSettings()` function is defined

**Q: CTL going up during taper?**
- This shouldn't happen - check your taper intensity
- Taper should always reduce or maintain CTL, never increase

**Q: Want different taper percentages?**
- Edit the `<select id="taperIntensity">` options
- Add custom values like `<option value="0.65">65%</option>`

## Advanced: Custom Taper Curves

The current system uses a linear taper (same reduction each week). If you want a non-linear taper (e.g., bigger drop in week 1, smaller in week 2), you'd need to modify the `updateCTLProjection()` function.

Example for progressive taper:
```javascript
// Week 1: 80% volume (-0.7 CTL)
// Week 2: 60% volume (-1.4 CTL)
// Total: -2.1 CTL over 2 weeks
```

## Real-World Example: Your March Race

**Scenario:**
- Today: January 10 (CTL 106)
- Race: March 8 (8 weeks away)
- Plan: Build for 7 weeks, taper 1 week

**Settings in HTML:**
```
Current CTL: 106
Race Date: 2026-03-08
Training Plan: Moderate (3.5 CTL/week)
✅ Enable Taper: Yes
Taper Weeks: 1
Taper Intensity: 60%
```

**Results:**
```
Weeks to Race: 8.4
Build Weeks: 7.4
Peak CTL: 132 (before taper)
Race Day CTL: 130.6 (after 1-week light taper)
Race Day Fitness: 1.088

Your predicted improvement: ~8.8% faster than current fitness
```

This matches your real training plan - light taper to stay sharp!
