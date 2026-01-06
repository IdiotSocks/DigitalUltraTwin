# Contributing to Ultra-Running Digital Twin

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)
- Relevant code snippets or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- Clear description of the proposed feature
- Use case and motivation
- Potential implementation approach (if applicable)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Add tests** if applicable
5. **Update documentation** as needed
6. **Commit with clear messages**: `git commit -m "Add feature: description"`
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write clear docstrings for functions and classes
- Keep functions focused and modular
- Add comments for complex logic

Example:
```python
def calculate_speed(
    gradient_pct: float,
    fitness_level: float = 1.0
) -> float:
    """
    Calculate adjusted speed based on gradient and fitness.
    
    Args:
        gradient_pct: Terrain gradient in percentage (-50 to 50)
        fitness_level: Athlete fitness multiplier (default: 1.0)
        
    Returns:
        Adjusted speed in km/h
    """
    # Implementation
    pass
```

### Testing

- Add unit tests for new functionality
- Ensure existing tests pass: `pytest`
- Aim for >80% code coverage
- Test edge cases and error handling

### Documentation

- Update README.md if adding major features
- Add/update docstrings for all public functions
- Update relevant documentation in `docs/`
- Add usage examples if appropriate

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ultra-running-digital-twin.git
cd ultra-running-digital-twin

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
flake8 src/
```

## Areas for Contribution

### High Priority
- [ ] Additional race validations (more athletes, more races)
- [ ] Real-time race tracking and adjustment
- [ ] Weather API integration
- [ ] Training load API integration (Strava/TrainingPeaks)

### Medium Priority
- [ ] Web interface for predictions
- [ ] Improved visualizations
- [ ] Multi-athlete calibration
- [ ] Mobile app (GPS tracking)

### Nice to Have
- [ ] Machine learning auto-calibration
- [ ] Race database (community contributed)
- [ ] Social features (compare with friends)
- [ ] Integration with race registration platforms

## Pull Request Process

1. **Update documentation** - README, docstrings, usage guides
2. **Add tests** - Unit tests for new functionality
3. **Pass CI checks** - Linting, tests, coverage
4. **Request review** - Tag maintainers for review
5. **Address feedback** - Make requested changes
6. **Merge** - Maintainer will merge when ready

## Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience, education
- Nationality, personal appearance, race
- Religion, sexual identity and orientation

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct reasonably considered inappropriate

### Enforcement

Violations can be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- Project README for major features

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in GitHub Discussions
- Reach out to maintainers directly

Thank you for contributing! 🏃‍♂️⛰️
