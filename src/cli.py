#!/usr/bin/env python3
"""
Command line interface for the foodprint application.
"""

import argparse
import sys
from typing import Dict

from calculator import calculate_impact


def format_results(food: str, amount_grams: float, results: Dict[str, float]) -> str:
    """
    Format the calculation results into a human-readable string.

    Args:
        food (str): The name of the food item
        amount_grams (float): The amount in grams
        results (Dict[str, float]): The calculation results

    Returns:
        str: Formatted results string
    """
    return f"""For {amount_grams}g of {food}:
- CO2: {results["co2"]} kg
- Water: {results["water"]} L
- Land: {results["land"]} m²"""


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate the environmental impact of food items",
        prog="python -m foodprint.cli",
    )

    parser.add_argument(
        "food", type=str, help="Name of the food item (e.g., rice, beef, chicken)"
    )

    parser.add_argument("amount", type=float, help="Amount in grams (e.g., 100, 250.5)")

    args = parser.parse_args()

    # Validate amount is positive
    if args.amount <= 0:
        print("Error: Amount must be a positive number", file=sys.stderr)
        sys.exit(1)

    try:
        # Calculate the environmental impact
        results = calculate_impact(args.food, args.amount)

        # Print formatted results
        print(format_results(args.food, args.amount, results))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(
            "\nAvailable foods include: rice, beef, potatoes, chicken, pork, lamb, salmon, eggs, milk, cheese, bread, pasta, tomatoes, onions, carrots, apples, bananas, oranges, almonds, avocados",
            file=sys.stderr,
        )
        sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
