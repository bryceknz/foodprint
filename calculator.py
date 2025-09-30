import csv
import os
from typing import Dict


def calculate_impact(food: str, weight_grams: float) -> Dict[str, float]:
    """
    Calculate the environmental impact of a food item based on its weight.

    Args:
        food (str): The name of the food item to look up
        weight_grams (float): The weight of the food in grams

    Returns:
        Dict[str, float]: Dictionary containing:
            - co2: CO2 emissions in kg
            - water: Water usage in liters
            - land: Land usage in square meters

    Raises:
        ValueError: If the food item is not found in the database
        FileNotFoundError: If the food_impact.csv file cannot be found
    """
    # Get the path to the CSV file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "data", "food_impact.csv")

    # Check if file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Food impact data file not found at {csv_path}")

    # Read the CSV file and look for the food item
    with open(csv_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row["food"].lower() == food.lower():
                # Convert weight from grams to kg for calculations
                weight_kg = weight_grams / 1000.0

                # Calculate scaled impact metrics
                co2 = float(row["co2_per_kg"]) * weight_kg
                water = float(row["water_l_per_kg"]) * weight_kg
                land = float(row["land_m2_per_kg"]) * weight_kg

                return {
                    "co2": round(co2, 3),
                    "water": round(water, 1),
                    "land": round(land, 3),
                }

    # If food not found, raise an error
    raise ValueError(f"Food item '{food}' not found in the database")
