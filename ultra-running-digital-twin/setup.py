from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ultra-running-digital-twin",
    version="3.3.0",
    author="Simbarashe",
    author_email="your.email@example.com",
    description="Monte Carlo simulation-based digital twin for ultra-running race performance prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ultra-running-digital-twin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Athletes",
        "Intended Audience :: Coaches",
        "Topic :: Sports/Exercise :: Performance Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "scipy>=1.7.0",
        "gpxpy>=1.5.0",
        "requests>=2.26.0",
        "python-dateutil>=2.8.0",
        "pytz>=2021.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.6b0",
            "flake8>=3.9.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "digital-twin=src.cli:main",
        ],
    },
)
