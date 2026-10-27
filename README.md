# Industrial Monitoring & Fault Diagnosis AI Agent 🏭

An AI-powered industrial predictive maintenance and fault diagnosis agent built using **CrewAI**, **Groq**, and **Streamlit**.

The system collects and validates industrial machinery telemetry (temperature, vibration, and pressure), performs automated rules-based verification, and engages an autonomous CrewAI maintenance specialist agent powered by Groq LLM to synthesize diagnoses, identify potential root causes, and recommend actionable inspection checklists.

---

## 🌟 Features

- **Interactive Streamlit Web Dashboard**: Real-time visual gauges/bars for temperature, vibration, and pressure readings.
- **Rule-Based Sensor Telemetry Engine**: Instant detection of high temperatures, abnormal vibration velocities, or out-of-range pressures (`sensor_tools.py`).
- **Autonomous CrewAI Agent**: Delivers expert diagnostic reports without hallucinative claims, separating facts from hypotheses (`crew_setup.py`).
- **High Performance**: Powered by Groq inference for near-instant responses.
- **CLI & GUI Modes**: Run in your terminal or launch the web dashboard.

---

## 📸 User Interface

The application features a clean, responsive web interface matching industrial monitoring standards:
- **Telemetry Visual Cards**: Visual ranges with dynamic indicators.
- **Overall Operational Status Alert**: Instant Critical, Warning, or Normal banners.
- **Side-by-side Inspection Views**: Raw Sensor Analysis JSON output and the CrewAI Diagnostic Report.

---

## 🚀 How to Setup Locally on Another Windows PC

Follow these exact steps to set up and run this project seamlessly on any other Windows computer (Windows 10 / Windows 11).

### Prerequisites

1. **Python 3.10 – 3.12** installed on Windows.
   - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ **Important during installation**: Check the box **"Add python.exe to PATH"**.
   - Verify in PowerShell or Command Prompt:
     ```powershell
     python --version
     ```
2. **Git for Windows** installed:
   - Download from [git-scm.com](https://git-scm.com/download/win).
3. A **Groq API Key**:
   - Get a free key at [console.groq.com/keys](https://console.groq.com/keys).

---

### Step-by-Step Windows Installation

Open **PowerShell** or **Command Prompt (CMD)** and run:

#### 1. Clone the Repository
```powershell
git clone https://github.com/Naveen-gale/industrial_fault.git
cd industrial_fault
```

#### 2. Create and Activate a Virtual Environment

- **In PowerShell:**
  ```powershell
  python -m venv .venv
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\.venv\Scripts\Activate.ps1
  ```

- **OR in Command Prompt (CMD):**
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```

*(Once activated, you will see `(.venv)` at the beginning of your terminal line)*

#### 3. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure Environment Variables (.env)
Create your `.env` file from the provided example template:

- **In PowerShell:**
  ```powershell
  Copy-Item .env.example .env
  ```
- **OR in CMD:**
  ```cmd
  copy .env.example .env
  ```

Open the `.env` file in Notepad (or any text editor) and put your actual Groq API key:
```powershell
notepad .env
```

Save the file with this content:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

---

## 💻 Running the Application

### Option A: Launch the Streamlit Web UI (Recommended)
Make sure your virtual environment is active (`(.venv)`), then run:
```powershell
streamlit run app.py
```
Your default browser will automatically open to:
👉 **`http://localhost:8501`**

### Option B: Run the Command-Line Interface (CLI)
To run diagnosis interactively directly in your Windows terminal:
```powershell
python main.py
```

### Option C: Run Unit Tests
To verify all sensor evaluation rules:
```powershell
python test_sensor_tools.py
```

---

## 🛠️ Windows Troubleshooting & Error Prevention

- **PowerShell Script Execution Error (`running scripts is disabled on this system`)**:
  Run this one-time command in PowerShell:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
  Then re-run `.\.venv\Scripts\Activate.ps1`.

- **Access Denied / PermissionError during CrewAI execution**:
  Ensure you run the commands from a directory where your Windows user profile has normal read/write permissions (e.g. `C:\Users\<YourUsername>\Desktop` or Documents).

- **Groq API Rate or Cache errors**:
  The project includes built-in compatibility hooks for Groq with CrewAI (`mark_cache_breakpoint`) to prevent request payload errors.

---

## 📁 Project Structure

```text
industrial-fault-agent/
│
├── app.py                 # Streamlit Web UI Dashboard
├── main.py                # Command-line interface runner
├── crew_setup.py          # CrewAI agent, task, and Groq LLM setup
├── sensor_tools.py        # Sensor threshold logic & CrewAI tool definition
├── test_sensor_tools.py   # Unit tests for sensor analysis
├── requirements.txt       # Project dependencies (crewai, python-dotenv, streamlit, mcp>=1.31.0)
├── .env.example           # Example environment configuration file
├── .gitignore             # Git ignore file protecting .env and virtual environments
└── README.md              # Windows setup guide & documentation
```
