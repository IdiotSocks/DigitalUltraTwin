#!/usr/bin/env python3
"""
Digital Twin v3.2 - Chianti 74K Race Simulator
Enhanced with course profile v1.1 specifications
"""

import json
import numpy as np
import pandas as pd
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class TerrainSegment:
    """Represents a segment of the race course"""
    distance_km: float
    elevation_m: float
    gradient_pct: float = 0.0

@dataclass
class EnvironmentalConditions:
    """Environmental factors affecting performance"""
    temperature_celsius: float = 15.0
    altitude_m: float = 500.0
    humidity_pct: float = 50.0
    wind_speed_kmh: float = 0.0
    precipitation: str = "dry"  # dry, light_rain, wet

@dataclass
class NutritionStrategy:
    """Fueling and hydration strategy"""
    calories_per_hour: float = 250.0
    fluid_ml_per_hour: float = 500.0
    electrolytes_mg_per_hour: float = 500.0

class DigitalTwinV32:
    """
    Enhanced Digital Twin v3.2 with course profile integration
    """
    
    def __init__(self, athlete_profile_path: str, course_profile_path: str):
        """Load athlete and course profiles"""
        with open(athlete_profile_path, 'r') as f:
            self.athlete_profile = json.load(f)
        
        with open(course_profile_path, 'r') as f:
            self.course_profile = json.load(f)
        
        # Extract key parameters
        self.speed_by_gradient = self.athlete_profile['performance_by_gradient']
        self.respiratory_profile = self.athlete_profile['respiratory_profile']
        
        # Course-specific parameters
        self.terrain = self.course_profile['terrain_profile']
        self.fatigue_model = self.course_profile['simulation_defaults']['fatigue_model']
        self.field_effects = self.course_profile['simulation_defaults']['field_effects']
        self.altitude_penalty = self.course_profile['environment_profile']['altitude_penalty']
        
        # Initialize state
        self.fitness_level = 1.0
        
    def get_base_speed(self, gradient_pct: float) -> float:
        """Get baseline speed for a given gradient"""
        if gradient_pct < -15:
            return self.speed_by_gradient['steep_downhill']['base_speed_kmh']
        elif gradient_pct < -5:
            return self.speed_by_gradient['moderate_downhill']['base_speed_kmh']
        elif gradient_pct < 5:
            return self.speed_by_gradient['flat']['base_speed_kmh']
        elif gradient_pct < 15:
            return self.speed_by_gradient['moderate_uphill']['base_speed_kmh']
        else:
            return self.speed_by_gradient['steep_uphill']['base_speed_kmh']
    
    def calculate_technical_impact(self, precipitation: str = 'dry') -> float:
        """
        Calculate technical terrain impact using course profile
        """
        multipliers = self.terrain['technicality']
        
        if precipitation == 'dry':
            return multipliers['dry_multiplier']
        elif precipitation == 'light_rain':
            return multipliers['light_rain_multiplier']
        else:  # wet
            return multipliers['wet_multiplier']
    
    def calculate_temperature_impact(self, temperature: float) -> float:
        """Calculate performance impact from temperature"""
        if temperature > 15:
            # Heat penalty: 2% slower per degree above 15°C
            return 0.98 ** (temperature - 15)
        elif temperature < 10:
            # Cold penalty: 1% slower per degree below 10°C
            return 0.99 ** (10 - temperature)
        return 1.0
    
    def calculate_altitude_impact(self, altitude_m: float, distance_km: float) -> float:
        """
        Calculate altitude impact using course profile
        Chianti-specific: minimal penalty since course is 150-700m
        """
        if not self.altitude_penalty['apply']:
            return 1.0
        
        # Only apply penalty if above threshold
        if altitude_m < self.altitude_penalty['starts_m']:
            return 1.0
        
        # Penalty per 1000m above threshold
        excess_altitude = altitude_m - self.altitude_penalty['starts_m']
        multiplier = self.altitude_penalty['multiplier_per_1000m']
        return multiplier ** (excess_altitude / 1000)
    
    def calculate_fatigue_impact(self, distance_km: float) -> float:
        """
        Calculate cumulative fatigue using course-specific model
        Softer fatigue for runnable sub-80k profile
        """
        inflection = self.fatigue_model['fatigue_inflection_km']
        base_rate = self.fatigue_model['fatigue_per_km_base']
        slope_mult = self.fatigue_model['fatigue_slope_multiplier']
        
        if distance_km < inflection:
            # Before inflection: minimal fatigue
            fatigue_factor = base_rate ** distance_km
        else:
            # After inflection: accelerated fatigue
            base_fatigue = base_rate ** inflection
            excess_km = distance_km - inflection
            accelerated_fatigue = (base_rate * slope_mult) ** excess_km
            fatigue_factor = base_fatigue * accelerated_fatigue
        
        return max(0.7, fatigue_factor)
    
    def calculate_field_loss(self, distance_km: float, gradient_pct: float) -> float:
        """
        Calculate field loss multiplier for Chianti's runnable profile
        Accounts for athlete's strength on runnable terrain with short climbs
        """
        base_multiplier = 1.0
        
        # Runnable trail advantage
        if abs(gradient_pct) < 10:  # Runnable sections
            base_multiplier *= self.field_effects['field_loss_multiplier_runnable_trail']
        
        # Short climb advantage (6-16% grades typical)
        if 6 <= gradient_pct <= 16:
            base_multiplier *= self.field_effects['field_loss_multiplier_short_climbs']
        
        return base_multiplier
    
    def calculate_nutrition_impact(self, hours_running: float, cal_per_hour: float) -> float:
        """Calculate nutrition impact"""
        if hours_running < 2:
            return 1.0
        
        required_calories = 250 * hours_running
        actual_calories = cal_per_hour * hours_running
        nutrition_ratio = min(1.0, actual_calories / required_calories)
        
        return 0.85 + (0.15 * nutrition_ratio)
    
    def calculate_respiratory_impact(
        self,
        distance_km: float,
        gradient_pct: float,
        hr_estimated: int,
        temperature: float,
        time_in_zone3_minutes: float,
        fitness_level: float
    ) -> Tuple[float, bool]:
        """
        Calculate respiratory impact with Arc 2025 validation
        """
        impact = self.respiratory_profile['baseline_impact']['optimal_conditions']
        is_incident = False
        
        # Fitness bonus
        fitness_bonus = min(0.05, (fitness_level - 1.0) * 0.05)
        impact += fitness_bonus
        
        # Early race vulnerability (3-25km)
        vulnerable_zone = self.respiratory_profile['vulnerable_zones']['early_race_km']
        if vulnerable_zone['start_km'] <= distance_km <= vulnerable_zone['end_km']:
            if fitness_level >= 1.15:
                impact *= 0.97
            else:
                impact *= 0.94
                if temperature < 10 and distance_km >= 10:
                    is_incident = True
        
        # High HR penalty
        if hr_estimated > 150:
            hr_penalty = 1 - ((hr_estimated - 150) * 0.0008)
            impact *= max(0.88, hr_penalty)
        
        # Temperature impact
        temp_thresholds = self.respiratory_profile['temperature_thresholds']
        if temperature <= temp_thresholds['extreme_danger_c']:
            impact *= 0.85
            is_incident = True if 5 <= distance_km <= 25 else is_incident
        elif temperature <= temp_thresholds['high_risk_c']:
            temp_penalty = 0.98 ** (8 - temperature)
            impact *= temp_penalty
            if 10 <= distance_km <= 25:
                incident_prob = 0.7 if fitness_level < 1.15 else 0.3
                is_incident = random.random() < incident_prob
        elif temperature <= temp_thresholds['moderate_risk_c']:
            temp_penalty = 0.98 ** (10 - temperature)
            impact *= temp_penalty
        
        # Sustained hard effort
        if time_in_zone3_minutes > 45:
            effort_minutes = time_in_zone3_minutes - 45
            if fitness_level >= 1.2:
                sustained_penalty = 0.998 ** effort_minutes
            else:
                sustained_penalty = 0.995 ** effort_minutes
            impact *= max(0.88, sustained_penalty)
        
        # Recovery on descents
        if gradient_pct < -5 and hr_estimated < 130:
            recovery = min(1.0, impact + 0.05)
            impact = recovery
        
        return max(0.85, min(1.0, impact)), is_incident
    
    def estimate_heart_rate(
        self,
        gradient_pct: float,
        speed_kmh: float,
        fatigue: float,
        fitness_level: float = 1.0
    ) -> int:
        """Estimate HR based on gradient, speed, and fatigue"""
        base_hr = 122
        
        # Fitness HR reduction
        fitness_hr_reduction = (fitness_level - 1.0) * 8
        base_hr -= fitness_hr_reduction
        
        # Gradient impact
        if gradient_pct > 5:
            hr_addition = (gradient_pct - 5) * 2
        elif gradient_pct < -5:
            hr_addition = abs(gradient_pct + 5) * 1
        else:
            hr_addition = 0
        
        # Speed impact
        speed_factor = (speed_kmh / 5.32) * 10
        
        # Fatigue impact
        fatigue_hr = fatigue * 10
        
        estimated_hr = int(base_hr + hr_addition + speed_factor + fatigue_hr)
        return min(163, max(85, estimated_hr))
    
    def simulate_race(
        self,
        elevation_profile: List[Dict],
        scenario: Dict,
        pacing_strategy: str = 'even',
        start_time_hour: int = 6
    ) -> Dict:
        """
        Simulate complete race with course profile integration
        """
        # Set up
        env = scenario['environment']
        nutrition = scenario['nutrition']
        fitness = scenario['fitness_level']
        
        # Pacing multipliers
        pacing_multipliers = {
            'conservative': {'early': 0.92, 'mid': 0.98, 'late': 1.05},
            'moderate': {'early': 0.95, 'mid': 1.00, 'late': 1.03},
            'aggressive': {'early': 1.03, 'mid': 0.98, 'late': 0.95},
            'even': {'early': 1.00, 'mid': 1.00, 'late': 1.00},
            'negative_split': {'early': 0.90, 'mid': 0.95, 'late': 1.08},
            'race_mode': {'early': 1.05, 'mid': 1.05, 'late': 1.05},
        }
        
        pacing = pacing_multipliers.get(pacing_strategy, pacing_multipliers['even'])
        
        # Initialize tracking
        results = []
        cumulative_time_hours = 0.0
        time_in_zone3_minutes = 0.0
        respiratory_incidents = []
        total_distance = elevation_profile[-1]['distance_km']
        aid_station_time_hours = 0.0
        
        # Technical multiplier (from course profile)
        tech_multiplier = self.calculate_technical_impact(env.precipitation)
        
        # Simulate segment-by-segment
        for i in range(1, len(elevation_profile)):
            segment = elevation_profile[i]
            prev_segment = elevation_profile[i-1]
            distance_segment_km = segment['distance_km'] - prev_segment['distance_km']
            
            # Determine race phase
            progress = segment['distance_km'] / total_distance
            if progress < 0.33:
                phase = 'early'
            elif progress < 0.66:
                phase = 'mid'
            else:
                phase = 'late'
            
            # Time-based temperature
            elapsed_hours = cumulative_time_hours
            current_hour = start_time_hour + int(elapsed_hours)
            
            if current_hour < 9:
                temp_adjustment = -4
            elif current_hour < 12:
                temp_adjustment = -1
            elif current_hour < 15:
                temp_adjustment = 0
            else:
                temp_adjustment = -2
            
            current_temp = env.temperature_celsius + temp_adjustment
            
            # Get base speed and apply pacing
            base_speed = self.get_base_speed(segment['gradient_pct'])
            base_speed *= pacing[phase]
            
            # Calculate adjusted speed
            adjusted_speed = base_speed
            
            # Apply fitness
            adjusted_speed *= fitness
            
            # Apply technical terrain (course-specific)
            adjusted_speed *= tech_multiplier
            
            # Apply field loss (runnable trail advantage)
            adjusted_speed *= self.calculate_field_loss(segment['distance_km'], segment['gradient_pct'])
            
            # Apply environmental factors
            adjusted_speed *= self.calculate_temperature_impact(current_temp)
            adjusted_speed *= self.calculate_altitude_impact(env.altitude_m, segment['distance_km'])
            
            # Apply course-specific fatigue model
            adjusted_speed *= self.calculate_fatigue_impact(prev_segment['distance_km'])
            
            # Apply nutrition
            adjusted_speed *= self.calculate_nutrition_impact(cumulative_time_hours, nutrition.calories_per_hour)
            
            # Estimate heart rate
            fatigue_factor = 1 - self.calculate_fatigue_impact(prev_segment['distance_km'])
            hr_estimate = self.estimate_heart_rate(
                segment['gradient_pct'],
                adjusted_speed,
                fatigue_factor,
                fitness
            )
            
            # Track Zone 3+ time
            if hr_estimate > 150:
                estimated_segment_time_minutes = (distance_segment_km / adjusted_speed) * 60
                time_in_zone3_minutes += estimated_segment_time_minutes
            
            # Calculate respiratory impact
            respiratory_multiplier, is_incident = self.calculate_respiratory_impact(
                distance_km=segment['distance_km'],
                gradient_pct=segment['gradient_pct'],
                hr_estimated=hr_estimate,
                temperature=current_temp,
                time_in_zone3_minutes=time_in_zone3_minutes,
                fitness_level=fitness
            )
            
            # Track incidents
            if is_incident:
                respiratory_incidents.append({
                    'distance_km': segment['distance_km'],
                    'impact': respiratory_multiplier,
                    'hr_estimate': hr_estimate,
                    'temperature': current_temp,
                    'gradient': segment['gradient_pct']
                })
            
            # Apply respiratory impact
            final_speed = adjusted_speed * respiratory_multiplier
            
            # Calculate time
            segment_time_hours = distance_segment_km / final_speed
            cumulative_time_hours += segment_time_hours
            
            # Hiking determination
            is_hiking = final_speed < 4.5
            
            results.append({
                'distance_km': segment['distance_km'],
                'elevation_m': segment['elevation_m'],
                'gradient_pct': segment['gradient_pct'],
                'temperature_c': current_temp,
                'base_speed_kmh': base_speed,
                'adjusted_speed_kmh': adjusted_speed,
                'respiratory_multiplier': respiratory_multiplier,
                'final_speed_kmh': final_speed,
                'hr_estimate': hr_estimate,
                'segment_time_hours': segment_time_hours,
                'cumulative_time_hours': cumulative_time_hours,
                'is_hiking': is_hiking,
                'phase': phase
            })
        
        # Add aid station time (6-10 stops, median 120s)
        num_aid_stations = random.randint(6, 10)
        avg_stop_seconds = random.gauss(120, 30)  # Mean 120s, std 30s
        aid_station_time_hours = (num_aid_stations * avg_stop_seconds) / 3600
        
        # Calculate summary
        total_time_hours = cumulative_time_hours + aid_station_time_hours
        avg_speed = total_distance / total_time_hours
        hiking_time = sum(r['segment_time_hours'] for r in results if r['is_hiking'])
        
        return {
            'segments': results,
            'summary': {
                'total_distance_km': total_distance,
                'total_time_hours': total_time_hours,
                'moving_time_hours': cumulative_time_hours,
                'aid_station_time_hours': aid_station_time_hours,
                'total_time_formatted': self._format_time(total_time_hours),
                'average_speed_kmh': avg_speed,
                'hiking_percentage': (hiking_time / cumulative_time_hours) * 100,
                'respiratory_incidents': len(respiratory_incidents),
                'worst_respiratory_impact': min([r['impact'] for r in respiratory_incidents]) if respiratory_incidents else 1.0,
                'pacing_strategy': pacing_strategy,
                'fitness_level': fitness,
                'technical_multiplier': tech_multiplier
            },
            'respiratory_incidents': respiratory_incidents,
            'conditions': scenario
        }
    
    def _format_time(self, hours: float) -> str:
        """Format hours as HH:MM:SS"""
        total_seconds = int(hours * 3600)
        hours_int = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours_int:02d}:{minutes:02d}:{seconds:02d}"


def run_monte_carlo_v32(
    elevation_profile: List[Dict],
    athlete_profile_path: str,
    course_profile_path: str,
    weather_scenarios: List[Dict],
    num_simulations: int = 200
) -> pd.DataFrame:
    """
    Run Monte Carlo simulations with v3.2 enhancements
    """
    simulator = DigitalTwinV32(athlete_profile_path, course_profile_path)
    
    results = []
    
    print(f"Running {num_simulations} simulations with Digital Twin v3.2...")
    print("="*80)
    
    # Pacing strategies
    pacing_strategies = [
        'conservative', 'moderate', 'aggressive', 'even', 'negative_split', 'race_mode'
    ]
    
    for sim in range(num_simulations):
        # Select scenario
        weather_scenario = random.choice(weather_scenarios)
        
        # Randomize parameters
        scenario = {
            'environment': EnvironmentalConditions(
                temperature_celsius=weather_scenario['temp_c'],
                altitude_m=random.uniform(150, 700),  # Chianti range from course profile
                humidity_pct=random.uniform(50, 80),
                wind_speed_kmh=random.uniform(0, 20),
                precipitation=weather_scenario.get('precipitation', 'dry')
            ),
            'nutrition': NutritionStrategy(
                calories_per_hour=random.uniform(250, 290),
                fluid_ml_per_hour=random.uniform(500, 650),
                electrolytes_mg_per_hour=random.uniform(450, 600)
            ),
            'fitness_level': random.uniform(0.95, 1.15),  # Realistic range
            'pollen_level': random.choice(['low', 'low', 'low', 'medium'])
        }
        
        pacing = random.choice(pacing_strategies)
        
        # Run simulation
        result = simulator.simulate_race(elevation_profile, scenario, pacing)
        
        time_hours = result['summary']['total_time_hours']
        
        results.append({
            'Simulation': sim + 1,
            'Pacing Strategy': pacing,
            'Finish Time': result['summary']['total_time_formatted'],
            'Time (hours)': time_hours,
            'Moving Time (hours)': result['summary']['moving_time_hours'],
            'Aid Station Time (min)': result['summary']['aid_station_time_hours'] * 60,
            'Avg Speed (km/h)': result['summary']['average_speed_kmh'],
            'Temperature (°C)': scenario['environment'].temperature_celsius,
            'Precipitation': scenario['environment'].precipitation,
            'Fitness Level': scenario['fitness_level'],
            'Calories/hr': scenario['nutrition'].calories_per_hour,
            'Fluids (ml/hr)': scenario['nutrition'].fluid_ml_per_hour,
            'Pollen Level': scenario['pollen_level'],
            'Respiratory Incidents': result['summary']['respiratory_incidents'],
            'Worst Respiratory': result['summary']['worst_respiratory_impact'],
            'Hiking %': result['summary']['hiking_percentage'],
            'Technical Multiplier': result['summary']['technical_multiplier'],
            'Weather Scenario': weather_scenario['name']
        })
        
        if (sim + 1) % 50 == 0:
            print(f"Completed {sim + 1}/{num_simulations} simulations...")
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    print("Digital Twin v3.2 Simulator loaded successfully!")
