"""
Demo: Computing Travel Times for Delhi Landmarks
=================================================
Author: Kasturi Kandalam

This script demonstrates both methods for calculating travel times:
1. Many-to-many matrix using osrm_table_matrix
2. Pairwise OD pairs using OSRMTravelTimeCalculator

Run: python examples/demo_run.py
"""

import sys
import os
import pandas as pd

# Add parent directory to path to import osrm_tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from osrm_tools import osrm_table_matrix, OSRMTravelTimeCalculator

def demo_matrix_calculation():
    """
    Demo 1: Many-to-many travel time matrix
    ----------------------------------------
    Useful when you want all combinations of origins to destinations.
    """
    
    print("=" * 70)
    print("DEMO 1: Many-to-Many Travel Time Matrix")
    print("=" * 70)
    print()
    
    # Define origins and destinations
    # Format: (latitude, longitude)
    origins = [
        (28.68902, 77.20989),  # ISI Delhi
        (28.53074, 77.21043),  # ABCOFFEE
    ]
    
    destinations = [
        (28.55616, 77.10004),  # Delhi Airport
        (28.59330, 77.21957),  # Lodhi Gardens
    ]
    
    print("Origins:")
    print("  1. ISI Delhi (28.68902, 77.20989)")
    print("  2. ABCOFFEE Malviya Nagar (28.53074, 77.21043)")
    print()
    print("Destinations:")
    print("  1. Delhi Airport (28.55616, 77.10004)")
    print("  2. Lodhi Gardens (28.59330, 77.21957)")
    print()
    
    # Calculate travel times
    print("Calculating travel times using OSRM /table API...")
    dur_df, dist_df = osrm_table_matrix(origins, destinations, profile="driving")
    
    print("\nTravel Times (minutes):")
    print(dur_df.round(1))
    print("\nDistances (km):")
    print(dist_df.round(2))
    
    # Save results
    os.makedirs('results', exist_ok=True)
    dur_df.to_csv('results/demo_durations_min.csv')
    dist_df.to_csv('results/demo_distances_km.csv')
    
    print("\n✓ Results saved to results/")
    print()


def demo_pairwise_calculation():
    """
    Demo 2: Pairwise OD pairs from DataFrame
    -----------------------------------------
    Useful when you have specific origin-destination pairs in your data.
    """
    
    print("=" * 70)
    print("DEMO 2: Pairwise Origin-Destination Travel Times")
    print("=" * 70)
    print()
    
    # Create sample OD pairs
    pairs = pd.DataFrame([
        {
            "origin": "ISI Delhi",
            "o_lat": 28.68902,
            "o_lon": 77.20989,
            "dest": "Lodhi Gardens",
            "d_lat": 28.59330,
            "d_lon": 77.21957
        },
        {
            "origin": "ABCOFFEE",
            "o_lat": 28.53074,
            "o_lon": 77.21043,
            "dest": "Delhi Airport",
            "d_lat": 28.55616,
            "d_lon": 77.10004
        }
    ])
    
    print("Origin-Destination Pairs:")
    print(pairs[['origin', 'dest']])
    print()
    
    # Calculate travel times
    calc = OSRMTravelTimeCalculator(profile="driving")
    results = calc.calculate_travel_matrix(
        pairs,
        origin_lat_col="o_lat",
        origin_lon_col="o_lon",
        dest_lat_col="d_lat",
        dest_lon_col="d_lon",
        delay=1.0
    )
    
    print("\nResults:")
    print(results[['origin', 'dest', 'travel_time_minutes', 'distance_km']].round(2))
    
    # Save results
    os.makedirs('results', exist_ok=True)
    results.to_csv('results/demo_pairwise_results.csv', index=False)
    
    print("\n✓ Results saved to results/demo_pairwise_results.csv")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "OSRM Travel Time Tools Demo" + " " * 26 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Run both demos
    demo_matrix_calculation()
    print("\n" + "-" * 70 + "\n")
    demo_pairwise_calculation()
    
    print("=" * 70)
    print("Demo complete! Check the results/ folder for output files.")
    print("=" * 70)
