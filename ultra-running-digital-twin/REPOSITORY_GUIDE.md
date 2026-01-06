# Repository Structure Guide

This document explains the organization of the Ultra-Running Digital Twin repository.

## Directory Structure

```
ultra-running-digital-twin/
│
├── README.md                    # Main project documentation
├── QUICKSTART.md               # Quick start guide
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── setup.py                    # Package installation
├── .gitignore                  # Git ignore patterns
│
├── src/                        # Source code
│   ├── __init__.py            # Package initialization
│   ├── digital_twin_v32_simulator.py  # Core simulator (main model)
│   ├── monte_carlo_runner.py  # Monte Carlo simulation engine
│   └── gpx_parser.py          # GPX file parsing utilities
│
├── data/                       # Data files
│   ├── profiles/              # Athlete profiles
│   │   └── simbarashe_enhanced_profile_v3_3.json
│   ├── courses/               # Course profiles  
│   │   └── chianti_74k_course_profile_v1_3_FINAL.json
│   └── elevation/             # Elevation data
│       └── chianti_elevation_profile.json
│
├── docs/                       # Documentation
│   ├── DIGITAL_TWIN_TECHNICAL_HANDOVER.md  # Complete technical specs
│   ├── MODEL_V3_UPDATE_GUIDE.md           # Version history
│   ├── USAGE_GUIDE.md                     # Detailed usage
│   └── SNOWDONIA_FINDINGS_AND_IMPLICATIONS.md
│
├── examples/                   # Usage examples
│   ├── basic_prediction.py    # Simple single prediction
│   ├── monte_carlo_analysis.py # 200-simulation study
│   └── sensitivity_analysis.py # Parameter testing
│
├── notebooks/                  # Jupyter notebooks (optional)
│
└── tests/                      # Unit tests (future)
```

## Key Files

### Core Simulation

**`src/digital_twin_v32_simulator.py`** (1,100 lines)
- Main DigitalTwinV32 class
- Gradient-based speed calculations
- Environmental adjustments (temperature, altitude)
- Respiratory/asthma modeling
- Fatigue accumulation
- Technical terrain handling
- Pacing strategy execution

Key classes:
- `DigitalTwinV32`: Main simulator
- `TerrainSegment`: Elevation point
- `EnvironmentalConditions`: Weather/altitude
- `NutritionStrategy`: Fueling parameters

### Monte Carlo Engine

**`src/monte_carlo_runner.py`** (300 lines)
- `run_monte_carlo_simulations()`: Main function
- `create_default_weather_scenarios()`: Weather generation
- `analyze_results()`: Statistical analysis

### Utilities

**`src/gpx_parser.py`** (150 lines)
- `parse_gpx_file()`: Import GPX elevation
- `smooth_elevation_profile()`: Noise reduction

## Data Files

### Athlete Profile
**`data/profiles/simbarashe_enhanced_profile_v3_3.json`** (3,178 lines)

Contains:
- Baseline performance data (UTMB 2025)
- Speed by gradient calibration
- Respiratory/asthma parameters
- Fitness progression targets
- Race history validation
- Terrain advantages

### Course Profile
**`data/courses/chianti_74k_course_profile_v1_3_FINAL.json`** (80 lines)

Contains:
- Course metadata (distance, elevation)
- Technical terrain multipliers
- Fatigue model parameters
- Field effect multipliers
- Aid station timing
- Validation targets

### Elevation Profile
**`data/elevation/chianti_elevation_profile.json`** (73 points)

Contains:
- Distance (km) for each point
- Elevation (m) for each point  
- Calculated gradients (%)
- Course metadata

## Documentation

### Technical Documentation

**`docs/DIGITAL_TWIN_TECHNICAL_HANDOVER.md`** (Comprehensive)
- Complete model specifications
- Validation results (UTMB, Snowdonia, Arc)
- All equations and multipliers
- Usage instructions
- Code repository
- Known limitations

**`docs/MODEL_V3_UPDATE_GUIDE.md`**
- Version history (v1.0 → v3.3)
- Migration guides
- Calibration changes
- New features

**`docs/USAGE_GUIDE.md`**
- Detailed usage instructions
- Parameter explanations
- Race strategy recommendations
- Training implications
- Comparison tables

### Research Documentation

**`docs/SNOWDONIA_FINDINGS_AND_IMPLICATIONS.md`**
- Technical terrain analysis
- Multi-race validation
- Athlete strength identification
- Weather impact studies

## Examples

### Basic Usage
**`examples/basic_prediction.py`** (150 lines)
- Load profiles
- Configure scenario
- Run single prediction
- Display results

### Statistical Analysis
**`examples/monte_carlo_analysis.py`** (120 lines)
- Run 200 simulations
- Analyze distributions
- Calculate success rates
- Save results to CSV

### Sensitivity Testing
**`examples/sensitivity_analysis.py`** (150 lines)
- Test fitness impact
- Test temperature impact
- Test pacing strategies
- Compare results

## Usage Patterns

### Quick Prediction
```bash
cd examples
python basic_prediction.py
```

### Custom Analysis
```bash
# Edit basic_prediction.py
python basic_prediction.py > my_results.txt
```

### Monte Carlo Study
```bash
python monte_carlo_analysis.py
# Creates: monte_carlo_results.csv
```

### Parameter Testing
```bash
python sensitivity_analysis.py
```

## Adding Your Own Data

### 1. Add Custom Athlete Profile

Create `data/profiles/my_profile.json`:
```json
{
  "metadata": {...},
  "performance_by_gradient": {
    "steep_downhill": {"base_speed_kmh": 6.5, ...},
    ...
  },
  "respiratory_profile": {...}
}
```

### 2. Add Custom Course Profile

Create `data/courses/my_race.json`:
```json
{
  "course_metadata": {...},
  "terrain_profile": {
    "technicality": {"dry_multiplier": 0.96, ...}
  },
  ...
}
```

### 3. Import GPX Elevation

```python
from src.gpx_parser import parse_gpx_file

profile_data = parse_gpx_file('my_race.gpx')
# Save to data/elevation/my_race.json
```

## File Sizes

| File | Lines | Size | Purpose |
|------|-------|------|---------|
| digital_twin_v32_simulator.py | 1,100 | ~45 KB | Core model |
| monte_carlo_runner.py | 300 | ~12 KB | Simulations |
| simbarashe_profile_v3_3.json | 3,178 | ~120 KB | Athlete data |
| chianti_course_v1_3.json | 80 | ~4 KB | Course data |
| TECHNICAL_HANDOVER.md | 2,500 | ~100 KB | Documentation |

## Dependencies

From `requirements.txt`:
- numpy>=1.21.0 (numerical operations)
- pandas>=1.3.0 (data analysis)
- matplotlib>=3.4.0 (plotting)
- seaborn>=0.11.0 (visualization)
- scipy>=1.7.0 (statistics)
- gpxpy>=1.5.0 (GPX parsing)
- requests>=2.26.0 (API calls)

## Version History

- **v3.3 (Jan 2026):** Calibrated for 10:30 Chianti target
- **v3.2 (Jan 2026):** Course profile integration
- **v3.1 (Dec 2025):** Arc 2025 validation
- **v3.0 (Dec 2025):** Multi-race validation
- **v2.0 (Dec 2025):** Enhanced respiratory model
- **v1.0 (Aug 2025):** UTMB baseline

## Git Workflow

```bash
# Initial setup
git clone https://github.com/yourusername/ultra-running-digital-twin.git
cd ultra-running-digital-twin

# Create feature branch
git checkout -b feature/my-feature

# Make changes, commit
git add .
git commit -m "Add feature: description"

# Push and create PR
git push origin feature/my-feature
```

## Testing (Future)

```
tests/
├── test_simulator.py       # Unit tests for simulator
├── test_monte_carlo.py     # Monte Carlo tests
├── test_gpx_parser.py      # GPX parsing tests
└── test_integration.py     # End-to-end tests
```

Run with: `pytest tests/`

## Continuous Integration (Future)

`.github/workflows/ci.yml`:
- Run tests on push
- Check code style (flake8)
- Calculate coverage
- Build documentation

## Distribution

Package for PyPI:
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

Install from PyPI:
```bash
pip install ultra-running-digital-twin
```

## Support

- 📖 Documentation: `docs/`
- 💡 Examples: `examples/`
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📧 Email: See README.md

---

**Last Updated:** January 3, 2026  
**Version:** 3.3.0
