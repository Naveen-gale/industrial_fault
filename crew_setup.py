
import os

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

from sensor_tools import analyze_sensor_readings_tool

load_dotenv()


def build_crew():
    """Create the industrial fault diagnosis crew."""

    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    
    )

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    # Connect CrewAI to Groq.
    llm = LLM(
    model=f"groq/{model_name}",
    api_key=api_key,
    temperature=0.1,
    max_tokens=1200,
)

    # Define the specialist agent.
    diagnosis_agent = Agent(
        role="Industrial Fault Diagnosis Specialist",
        goal=(
            "Analyze sensor evidence, identify potential faults, "
            "and recommend safe inspection steps."
        ),
        backstory=(
            "You are a cautious industrial maintenance analyst. "
            "You distinguish sensor evidence from possible causes. "
            "You never invent readings or claim a fault is confirmed "
            "without sufficient evidence."
        ),
        llm=llm,
        tools=[analyze_sensor_readings_tool],
        allow_delegation=False,
        verbose=True,
        max_iter=5,
    )

    # Define the work the agent must complete.
    diagnosis_task = Task(
        description="""
        Diagnose the following industrial machine.

        Machine name: {machine_name}
        Temperature in Celsius: {temperature_c}
        Vibration in mm/s: {vibration_mm_s}
        Pressure in bar: {pressure_bar}

        Instructions:
        1. Use the sensor analysis tool on these readings.
        2. Explain the measured values and reported status.
        3. Identify possible causes of any abnormal readings.
        4. Recommend safe inspection and verification steps.
        5. Explain what additional information is needed.
        6. Separate confirmed measurements from hypotheses.

        The tool thresholds are only for this demonstration.
        Do not present them as universal industrial limits.
        Never issue a machine shutdown command or bypass
        any safety procedure.
        """,
        expected_output="""
        A clear industrial diagnosis report with:
        - Machine name and sensor readings
        - Sensor analysis status
        - Evidence and possible fault causes
        - Recommended inspection steps
        - Uncertainties and safety limitations
        """,
        agent=diagnosis_agent,
    )

    # Organize and execute the work.
    crew = Crew(
        agents=[diagnosis_agent],
        tasks=[diagnosis_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew
