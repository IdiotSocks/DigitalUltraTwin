# Loading New GPX Files for Race Analysis

## Quick Start

### 1. Get Your GPX File

Download the race GPX file from:
- Race website
- Strava route
- Garmin Connect
- Any GPX source

### 2. Run the GPX Loader

From your terminal (in the `examples` directory):

```bash
python3 load_gpx.py /path/to/your/race.gpx race_name
```

**Example:**
```bash
# If you downloaded UTMB 2026 GPX file to Downloads folder
python3 load_gpx.py ~/Downloads/utmb_2026.gpx utmb_2026
```

### 3. Follow the Prompts

The script will:
1. Parse the GPX file
2. Show distance and elevation gain
3. Ask if you want to smooth elevation data (recommended for noisy GPS data)
4. Save the elevation profile
5. Ask if you want to run a prediction

### 4. Use the Profile

Once saved, you can use the elevation profile in any prediction script!

## Detailed Usage

### Basic Command

```bash
python3 load_gpx.py <gpx_file_path> [output_name]
```

**Parameters:**
- `gpx_file_path` (required): Path to your GPX file
- `output_name` (optional): Name for the saved profile (default: uses GPX filename)

### Examples

**Load and analyze UTMB GPX:**
```bash
python3 load_gpx.py ~/Downloads/utmb.gpx utmb_2026
```

**Load Western States GPX:**
```bash
python3 load_gpx.py ~/Documents/races/western_states.gpx ws100
```

**Load with relative path:**
```bash
python3 load_gpx.py ../data/gpx/hardmoors55.gpx hardmoors_55
```

## What Happens

### Step 1: Parsing
The script reads your GPX file and extracts:
- All GPS points (latitude, longitude, elevation)
- Calculates cumulative distance
- Simplifies to 1km intervals for efficiency

### Step 2: Profile Creation
Creates an elevation profile with:
- Distance markers (every 1km)
- Elevation at each marker
- Gradient percentages between markers
- Total elevation gain

### Step 3: Saving
Saves to: `data/elevation/{race_name}_elevation_profile.json`

Format:
```json
{
  "race": "UTMB 2026",
  "total_distance_km": 171.5,
  "total_elevation_gain_m": 10000,
  "profile": [
    {
      "distance_km": 0.0,
      "elevation_m": 1035,
      "gradient_pct": 0
    },
    {
      "distance_km": 1.0,
      "elevation_m": 1120,
      "gradient_pct": 8.5
    }
    // ... more points
  ]
}
```

### Step 4: Race Prediction (Optional)
If you choose to run a prediction:
- Uses your existing athlete profile
- Asks for fitness level (or CTL)
- Runs simulation with default conditions
- Shows predicted finish time

## Using the Profile Later

Once saved, you can use the profile in predictions:

### Option 1: Modify Existing Scripts

Edit `basic_prediction.py` or `interactive_ctl_prediction.py`:

```python
# Change this line:
with open('../data/elevation/chianti_elevation_profile.json', 'r') as f:

# To:
with open('../data/elevation/utmb_2026_elevation_profile.json', 'r') as f:
```

### Option 2: Create Custom Script

```python
import json
import sys
sys.path.append('..')

from src.digital_twin_v32_simulator import DigitalTwinV32, EnvironmentalConditions, NutritionStrategy

# Load your new profile
with open('../data/elevation/utmb_2026_elevation_profile.json', 'r') as f:
    profile_data = json.load(f)
    elevation_profile = profile_data['profile']

# Initialize simulator
simulator = DigitalTwinV32(
    athlete_profile_path='../data/profiles/simbarashe_enhanced_profile_v3_3.json',
    course_profile_path='../data/courses/chianti_74k_course_profile_v1_3_FINAL.json'
)

# Run prediction
scenario = {
    'environment': EnvironmentalConditions(temperature_celsius=15),
    'nutrition': NutritionStrategy(calories_per_hour=270),
    'fitness_level': 1.15
}

result = simulator.simulate_race(elevation_profile, scenario, 'race_mode')
print(f"Predicted finish: {result['summary']['total_time_formatted']}")
```

## Tips

### Smoothing Elevation Data
- **Use smoothing** if GPS data is noisy (lots of spikes)
- **Don't smooth** if you want exact elevation changes
- Smoothing uses a 3-point moving average

### Accuracy
- Better GPS data = better predictions
- Official race GPX files are usually most accurate
- Strava routes can have GPS noise

### File Organization

Store GPX files in:
```
data/
  gpx/                    # Original GPX files (optional)
    utmb_2026.gpx
    western_states.gpx
  elevation/              # Generated profiles (auto-created)
    utmb_2026_elevation_profile.json
    western_states_elevation_profile.json
```

## Troubleshooting

### Error: "No module named 'gpxpy'"
Install dependencies:
```bash
pip3 install gpxpy
```

Or install all requirements:
```bash
cd ..
pip3 install -r requirements.txt
```

### Error: "File not found"
Make sure your path is correct:
```bash
# Use absolute path
python3 load_gpx.py /Users/yourname/Downloads/race.gpx

# Or relative path from examples directory
python3 load_gpx.py ~/Downloads/race.gpx
```

### Profile Looks Wrong
- Check the GPX file in a viewer (like Strava)
- Try smoothing the elevation data
- Verify distance and elevation gain match race specs

## Example Workflow

Complete workflow for analyzing a new race:

```bash
# 1. Download GPX from race website
# Save to ~/Downloads/my_race.gpx

# 2. Navigate to examples directory
cd ultra-running-digital-twin/examples

# 3. Load and analyze
python3 load_gpx.py ~/Downloads/my_race.gpx my_race

# Output:
# ✓ Parsed successfully
# 📊 Distance: 100.0 km
# 📈 Elevation gain: 5000 m
#
# Smooth elevation data? (y/n): y
# ✓ Applied smoothing
# ✓ Saved to data/elevation/my_race_elevation_profile.json
#
# Run race prediction? (y/n): y
# Enter fitness level (e.g., 1.0) or CTL: 120
#
# 📊 FINISH TIME: 14:32:15
# ...

# 4. Use in predictions
python3 interactive_ctl_prediction.py
# (Then modify script to use your new profile)
```

## Advanced: Batch Processing

Process multiple GPX files:

```bash
for gpx in ~/Downloads/races/*.gpx; do
    python3 load_gpx.py "$gpx"
done
```

This loads all GPX files in the races folder!
