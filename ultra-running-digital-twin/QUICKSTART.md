# Quick Start Guide

Get up and running with the Ultra-Running Digital Twin in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ultra-running-digital-twin.git
cd ultra-running-digital-twin

# Install dependencies
pip install -r requirements.txt

# Optional: Install in development mode
pip install -e .
```

## Your First Prediction

### Step 1: Run the basic example

```bash
cd examples
python basic_prediction.py
```

This will predict race time for Chianti 74K with default parameters.

### Step 2: Customize the prediction

Edit `basic_prediction.py` to change:

```python
# Change fitness level (1.0 = baseline, 1.2 = 20% fitter)
'fitness_level': 1.20

# Change temperature (°C)
temperature_celsius=12

# Change pacing strategy
pacing_strategy='aggressive'  # Options: conservative, moderate, even, aggressive, race_mode
```

### Step 3: Run Monte Carlo simulations

```bash
python monte_carlo_analysis.py
```

This runs 200 simulations with varying conditions and analyzes results.

## Using with Your Own Data

### Option 1: Use existing profile with different fitness

```python
from src.digital_twin_v32_simulator import DigitalTwinV32

simulator = DigitalTwinV32(
    'data/profiles/simbarashe_enhanced_profile_v3_3.json',
    'data/courses/chianti_74k_course_profile_v1_3_FINAL.json'
)

# Just change the fitness level
scenario['fitness_level'] = 1.10  # Your estimated fitness
```

### Option 2: Import GPX file

```python
from src.gpx_parser import parse_gpx_file

# Parse your race GPX
profile_data = parse_gpx_file('path/to/your/race.gpx', simplify_interval_km=1.0)
elevation_profile = profile_data['profile']

# Use in simulation
result = simulator.simulate_race(elevation_profile, scenario, 'even')
```

### Option 3: Create custom athlete profile

1. Copy `data/profiles/simbarashe_enhanced_profile_v3_3.json`
2. Edit the speed_by_gradient values based on your data
3. Adjust respiratory_profile if needed
4. Save as `my_profile.json`
5. Use in simulator

## Understanding Results

### Key Outputs

```python
result = simulator.simulate_race(...)

# Finish time
result['summary']['total_time_formatted']  # "10:30:45"
result['summary']['total_time_hours']      # 10.51

# Performance metrics
result['summary']['average_speed_kmh']     # 7.05
result['summary']['hiking_percentage']     # 15.3

# Respiratory impact
result['summary']['respiratory_incidents'] # 5
```

### Interpreting Predictions

**Finish Time:**
- ±3% = Very accurate (good conditions match)
- ±5% = Typical accuracy
- ±10% = Uncertain conditions or untested course

**Respiratory Incidents:**
- 0-5 = Minimal impact
- 5-15 = Moderate impact (+5-10 minutes)
- 15+ = Significant impact (+15-30 minutes)

## Common Use Cases

### 1. "What pace should I target?"

```python
# Run with your expected fitness
scenario['fitness_level'] = 1.15
result = simulator.simulate_race(...)

# Check segment speeds
for seg in result['segments'][::5]:  # Every 5km
    print(f"{seg['distance_km']:.0f}km: {seg['final_speed_kmh']:.2f} km/h")
```

### 2. "How much faster if I improve fitness?"

```python
# Test multiple fitness levels
for fitness in [1.10, 1.15, 1.20]:
    scenario['fitness_level'] = fitness
    result = simulator.simulate_race(...)
    print(f"Fitness {fitness}: {result['summary']['total_time_formatted']}")
```

### 3. "What if it's cold?"

```python
# Compare temperatures
for temp in [8, 12, 16]:
    scenario['environment'].temperature_celsius = temp
    result = simulator.simulate_race(...)
    print(f"{temp}°C: {result['summary']['total_time_formatted']}")
```

### 4. "Best pacing strategy?"

```python
# Compare all strategies
for pacing in ['conservative', 'even', 'aggressive', 'race_mode']:
    result = simulator.simulate_race(..., pacing_strategy=pacing)
    print(f"{pacing}: {result['summary']['total_time_formatted']}")
```

## Fitness Level Guide

Estimate your fitness level:

| Fitness | Description | How to estimate |
|---------|-------------|-----------------|
| **1.00** | Baseline | Your recent ultra performance |
| **1.05** | +5% | 5 weeks of focused training |
| **1.10** | +10% | 8-10 weeks of progressive build |
| **1.15** | +15% | 12-15 weeks of quality training |
| **1.20** | +20% | Peak fitness, 20+ weeks prep |
| **1.25+** | Elite | Exceptional fitness |

**Quick estimate from recent race:**
```
Recent race: 50km in 6 hours at fitness X
Baseline prediction: 50km in 7 hours
Fitness level = 7 / 6 = 1.17
```

## Next Steps

- 📖 Read [USAGE_GUIDE.md](docs/USAGE_GUIDE.md) for detailed explanations
- 🔬 Check [TECHNICAL_HANDOVER.md](docs/DIGITAL_TWIN_TECHNICAL_HANDOVER.md) for model details
- 📊 Explore examples in `examples/` directory
- 🧪 Run sensitivity analysis: `python examples/sensitivity_analysis.py`
- 💬 Ask questions in GitHub Discussions

## Troubleshooting

**Problem: "Module not found"**
```bash
# Make sure you're in the project directory
cd ultra-running-digital-twin

# Install dependencies
pip install -r requirements.txt
```

**Problem: "JSON file not found"**
```bash
# Check you're running from examples/ directory
cd examples
python basic_prediction.py
```

**Problem: "Prediction seems way off"**
- Check your fitness level estimate (most common issue)
- Verify temperature is reasonable for race date
- Ensure course profile matches actual race

## Getting Help

- 🐛 **Bugs:** Open an issue on GitHub
- ❓ **Questions:** Start a GitHub Discussion
- 📧 **Direct contact:** See README.md

---

Happy racing! 🏃‍♂️⛰️
