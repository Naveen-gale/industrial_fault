

# Workaround for CrewAI's cache_breakpoint issue with Groq.
# This must run before importing crew_setup or creating the crew.

import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crew_setup import build_crew



def read_number(prompt: str) -> float:
    """Read a valid, non-negative sensor value."""
    while True:
        raw_value = input(prompt).strip()

        try:
            value = float(raw_value)

            if value < 0 or not __import__("math").isfinite(value):
                print("Enter a finite, non-negative number.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    print("=" * 55)
    print(" INDUSTRIAL MONITORING & FAULT DIAGNOSIS")
    print(" Learning demonstration - simulated sensor readings")
    print("=" * 55)

    machine_name = input(
        "Enter machine name [Industrial Motor]: "
    ).strip()

    if not machine_name:
        machine_name = "Industrial Motor"

    print("\nEnter the simulated sensor readings:")

    temperature_c = read_number("Temperature (Celsius): ")
    vibration_mm_s = read_number("Vibration (mm/s): ")
    pressure_bar = read_number("Pressure (bar): ")

    print("\nStarting the CrewAI diagnosis agent...")
    print("Please wait while the Groq model generates its report.")

    try:
        crew = build_crew()

        result = crew.kickoff(
            inputs={
                "machine_name": machine_name,
                "temperature_c": temperature_c,
                "vibration_mm_s": vibration_mm_s,
                "pressure_bar": pressure_bar,
            }
        )

        print("\n" + "=" * 55)
        print(" FINAL DIAGNOSIS REPORT")
        print("=" * 55)
        print(result)

    except Exception as exc:
        print("\nThe diagnosis could not be completed.")
        print(f"Error type: {type(exc).__name__}")
        print(f"Details: {exc}")
        print(
            "\nCheck your API key, model name, internet connection, "
            "and installed dependencies."
        )


if __name__ == "__main__":
    main()
