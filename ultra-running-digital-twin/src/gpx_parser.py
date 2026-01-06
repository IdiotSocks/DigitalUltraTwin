#!/usr/bin/env python3
"""
GPX file parser for elevation profile extraction
"""

import gpxpy
import numpy as np
from typing import List, Dict


def parse_gpx_file(gpx_file_path: str, simplify_interval_km: float = 1.0) -> Dict:
    """
    Parse GPX file and extract elevation profile.
    
    Args:
        gpx_file_path: Path to GPX file
        simplify_interval_km: Sampling interval in kilometers
        
    Returns:
        Dictionary with profile data and metadata
    """
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    
    points = []
    cumulative_distance = 0.0
    
    # Extract all points
    for track in gpx.tracks:
        for segment in track.segments:
            prev_point = None
            for point in segment.points:
                if prev_point:
                    distance_delta = prev_point.distance_2d(point)
                    cumulative_distance += distance_delta / 1000  # Convert to km
                
                points.append({
                    'distance_km': cumulative_distance,
                    'elevation_m': point.elevation if point.elevation else 0,
                    'latitude': point.latitude,
                    'longitude': point.longitude
                })
                
                prev_point = point
    
    # Simplify by sampling at regular intervals
    profile = []
    distance_intervals = np.arange(0, cumulative_distance + simplify_interval_km, simplify_interval_km)
    
    for target_distance in distance_intervals:
        # Find closest point
        closest_idx = min(range(len(points)), 
                         key=lambda i: abs(points[i]['distance_km'] - target_distance))
        
        profile.append({
            'distance_km': points[closest_idx]['distance_km'],
            'elevation_m': points[closest_idx]['elevation_m'],
            'gradient_pct': 0.0  # Will be calculated
        })
    
    # Calculate gradients
    for i in range(1, len(profile)):
        distance_delta = profile[i]['distance_km'] - profile[i-1]['distance_km']
        elevation_delta = profile[i]['elevation_m'] - profile[i-1]['elevation_m']
        
        if distance_delta > 0:
            profile[i]['gradient_pct'] = (elevation_delta / (distance_delta * 1000)) * 100
    
    # Calculate elevation gain
    total_gain = sum(
        max(0, profile[i]['elevation_m'] - profile[i-1]['elevation_m'])
        for i in range(1, len(profile))
    )
    
    return {
        'profile': profile,
        'metadata': {
            'total_distance_km': cumulative_distance,
            'total_elevation_gain_m': total_gain,
            'num_points': len(points),
            'num_simplified_points': len(profile),
            'simplify_interval_km': simplify_interval_km
        }
    }


def smooth_elevation_profile(profile: List[Dict], window_size: int = 3) -> List[Dict]:
    """
    Apply moving average smoothing to elevation data.
    
    Args:
        profile: Elevation profile
        window_size: Window size for smoothing
        
    Returns:
        Smoothed profile
    """
    elevations = [p['elevation_m'] for p in profile]
    smoothed = np.convolve(elevations, np.ones(window_size)/window_size, mode='same')
    
    smoothed_profile = []
    for i, p in enumerate(profile):
        smoothed_profile.append({
            'distance_km': p['distance_km'],
            'elevation_m': smoothed[i],
            'gradient_pct': p.get('gradient_pct', 0.0)
        })
    
    # Recalculate gradients after smoothing
    for i in range(1, len(smoothed_profile)):
        distance_delta = smoothed_profile[i]['distance_km'] - smoothed_profile[i-1]['distance_km']
        elevation_delta = smoothed_profile[i]['elevation_m'] - smoothed_profile[i-1]['elevation_m']
        
        if distance_delta > 0:
            smoothed_profile[i]['gradient_pct'] = (elevation_delta / (distance_delta * 1000)) * 100
    
    return smoothed_profile


if __name__ == "__main__":
    print("GPX parser module loaded successfully")
