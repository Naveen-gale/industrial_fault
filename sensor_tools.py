
import json
import math

from crewai.tools import tool

# checks the measurements with normal Python logic.
def analyze_sensor_data(
    temperature_c: float,
    vibration_mm_s: float,
    pressure_bar: float,
) -> dict:
    """
    Analyze sensor readings using illustrative demo thresholds.
    These thresholds are not certified industrial safety limits.
    """

    values = [temperature_c, vibration_mm_s, pressure_bar]

    if not all(math.isfinite(value) for value in values):
        raise ValueError("Sensor readings must be finite numbers.")

    if any(value < 0 for value in values):
        raise ValueError("Sensor readings cannot be negative.")

    faults = []
    warnings = []

    if temperature_c >= 90:
        faults.append("High temperature")
    elif temperature_c >= 75:
        warnings.append("Elevated temperature")

    if vibration_mm_s >= 10:
        faults.append("Excessive vibration")
    elif vibration_mm_s >= 5:
        warnings.append("Elevated vibration")

    if pressure_bar < 1.0 or pressure_bar > 5.0:
        faults.append("Pressure outside demo range")
    elif pressure_bar < 1.5 or pressure_bar > 4.5:
        warnings.append("Pressure near demo range boundary")

    if faults:
        status = "CRITICAL - INSPECTION REQUIRED"
    elif warnings:
        status = "WARNING - MONITOR CLOSELY"
    else:
        status = "NORMAL - WITHIN DEMO THRESHOLDS"

    return {
        "status": status,
        "temperature_c": temperature_c,
        "vibration_mm_s": vibration_mm_s,
        "pressure_bar": pressure_bar,
        "faults": faults,
        "warnings": warnings,
        "thresholds_are_demo_only": True,
    }


@tool("Analyze industrial sensor readings")
def analyze_sensor_readings_tool(
    temperature_c: float,
    vibration_mm_s: float,
    pressure_bar: float,
) -> str:
    """
    Check industrial motor temperature, vibration, and pressure.
    Use this tool before making a diagnosis.
    Provide temperature in Celsius, vibration in mm/s,
    and pressure in bar. Returns a JSON sensor analysis.
    """
    try:
        result = analyze_sensor_data(
            temperature_c=temperature_c,
            vibration_mm_s=vibration_mm_s,
            pressure_bar=pressure_bar,
        )
        return json.dumps(result, indent=2)
    except (ValueError, TypeError) as exc:
        return json.dumps({"error": str(exc)})
