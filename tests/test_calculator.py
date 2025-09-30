import pytest
import os
import sys

# Add the parent directory to the path so we can import the calculator module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import calculate_impact


class TestCalculateImpact:
    """Test cases for the calculate_impact function."""

    def test_calculate_impact_rice_100g(self):
        """Test calculating impact for 100g of rice."""
        result = calculate_impact("rice", 100.0)

        # Expected values for 100g (0.1kg) of rice:
        # CO2: 2.7 * 0.1 = 0.27 kg
        # Water: 2500 * 0.1 = 250.0 L
        # Land: 1.1 * 0.1 = 0.11 m²

        assert result["co2"] == pytest.approx(0.27, rel=1e-3)
        assert result["water"] == pytest.approx(250.0, rel=1e-3)
        assert result["land"] == pytest.approx(0.11, rel=1e-3)

    def test_calculate_impact_beef_250g(self):
        """Test calculating impact for 250g of beef."""
        result = calculate_impact("beef", 250.0)

        # Expected values for 250g (0.25kg) of beef:
        # CO2: 27.0 * 0.25 = 6.75 kg
        # Water: 15000 * 0.25 = 3750.0 L
        # Land: 27.0 * 0.25 = 6.75 m²

        assert result["co2"] == pytest.approx(6.75, rel=1e-3)
        assert result["water"] == pytest.approx(3750.0, rel=1e-3)
        assert result["land"] == pytest.approx(6.75, rel=1e-3)

    def test_calculate_impact_unknown_food(self):
        """Test that unknown food raises ValueError."""
        with pytest.raises(
            ValueError, match="Food item 'unknown_food' not found in the database"
        ):
            calculate_impact("unknown_food", 100.0)

    def test_calculate_impact_case_insensitive(self):
        """Test that food lookup is case-insensitive."""
        result_lower = calculate_impact("rice", 100.0)
        result_upper = calculate_impact("RICE", 100.0)
        result_mixed = calculate_impact("RiCe", 100.0)

        assert result_lower == result_upper == result_mixed

    def test_calculate_impact_zero_weight(self):
        """Test calculating impact for zero weight."""
        result = calculate_impact("rice", 0.0)

        assert result["co2"] == pytest.approx(0.0, rel=1e-3)
        assert result["water"] == pytest.approx(0.0, rel=1e-3)
        assert result["land"] == pytest.approx(0.0, rel=1e-3)

    def test_calculate_impact_chicken_500g(self):
        """Test calculating impact for 500g of chicken."""
        result = calculate_impact("chicken", 500.0)

        # Expected values for 500g (0.5kg) of chicken:
        # CO2: 6.9 * 0.5 = 3.45 kg
        # Water: 4325 * 0.5 = 2162.5 L
        # Land: 7.0 * 0.5 = 3.5 m²

        assert result["co2"] == pytest.approx(3.45, rel=1e-3)
        assert result["water"] == pytest.approx(2162.5, rel=1e-3)
        assert result["land"] == pytest.approx(3.5, rel=1e-3)

    def test_calculate_impact_return_type(self):
        """Test that the function returns the correct dictionary structure."""
        result = calculate_impact("potatoes", 200.0)

        assert isinstance(result, dict)
        assert set(result.keys()) == {"co2", "water", "land"}
        assert all(isinstance(value, float) for value in result.values())
