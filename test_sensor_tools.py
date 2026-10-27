
import unittest

from sensor_tools import analyze_sensor_data


class TestSensorAnalysis(unittest.TestCase):

    def test_normal_readings(self):
        result = analyze_sensor_data(50, 2, 3)
        self.assertTrue(result["status"].startswith("NORMAL"))
        self.assertEqual(result["faults"], [])

    def test_high_temperature(self):
        result = analyze_sensor_data(95, 2, 3)
        self.assertIn("High temperature", result["faults"])

    def test_high_vibration(self):
        result = analyze_sensor_data(50, 12, 3)
        self.assertIn("Excessive vibration", result["faults"])

    def test_pressure_outside_range(self):
        result = analyze_sensor_data(50, 2, 6)
        self.assertIn(
            "Pressure outside demo range",
            result["faults"],
        )

    def test_multiple_faults(self):
        result = analyze_sensor_data(95, 12, 6)
        self.assertEqual(len(result["faults"]), 3)
        self.assertTrue(result["status"].startswith("CRITICAL"))

    def test_warning(self):
        result = analyze_sensor_data(80, 2, 3)
        self.assertIn(
            "Elevated temperature",
            result["warnings"],
        )
        self.assertTrue(result["status"].startswith("WARNING"))

    def test_negative_reading_rejected(self):
        with self.assertRaises(ValueError):
            analyze_sensor_data(-5, 2, 3)

    def test_nan_reading_rejected(self):
        with self.assertRaises(ValueError):
            analyze_sensor_data(float("nan"), 2, 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
