import streamlit as st
import json
import os
from dotenv import load_dotenv

# Workaround for CrewAI's cache_breakpoint issue with Groq
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

# Ensure environment variables are loaded
load_dotenv()

# Import core business logic
from sensor_tools import analyze_sensor_data
import crew_setup

# Streamlit Page Configuration
st.set_page_config(
    page_title="Industrial Monitoring & Fault Diagnosis",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling - Premium Dark Industrial Theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global App Theme & Typography */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #131c31 0%, #090d16 75%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1440px;
    }

    /* Sidebar Glassmorphic Dark Styling */
    [data-testid="stSidebar"] {
        background-color: #0b111e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    /* Input Fields & Number Inputs in Dark Mode */
    div[data-baseweb="input"] > div {
        background-color: #131c2e !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        transition: all 0.2s ease;
    }
    div[data-baseweb="input"] > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }
    input {
        color: #f8fafc !important;
    }

    /* Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1rem !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5) !important;
    }
    .stButton > button[kind="secondary"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: rgba(51, 65, 85, 0.9) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
    }

    /* Header Typography */
    .main-title {
        background: linear-gradient(90deg, #ffffff 0%, #93c5fd 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 1.75rem;
    }

    /* Section Headers */
    .section-title {
        color: #e2e8f0;
        font-size: 1.05rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 1rem;
        padding-bottom: 0.45rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Premium Dark Glass Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 14px;
        padding: 1.35rem 1.5rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.45);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 36px -5px rgba(0, 0, 0, 0.6), 0 0 20px rgba(56, 189, 248, 0.08);
        border-color: rgba(56, 189, 248, 0.3);
    }
    .metric-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.05rem;
        font-weight: 700;
        margin: 0.55rem 0 0.85rem 0;
        letter-spacing: -0.02em;
    }

    /* Range Indicator Bars */
    .bar-container {
        position: relative;
        height: 8px;
        border-radius: 999px;
        background: #1e293b;
        margin-top: 10px;
        margin-bottom: 14px;
        overflow: visible;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.6);
    }
    .bar-labels {
        display: flex;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #64748b;
        font-weight: 500;
    }
    .bar-pin {
        position: absolute;
        top: -5px;
        width: 4px;
        height: 18px;
        background-color: #ffffff;
        border-radius: 4px;
        transform: translateX(-50%);
        z-index: 2;
        box-shadow: 0 0 10px #ffffff, 0 0 4px rgba(0, 0, 0, 0.9);
    }

    /* Glowing Dark Status Banners */
    .status-banner-critical {
        background: linear-gradient(90deg, rgba(127, 29, 29, 0.45) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        display: flex;
        align-items: center;
        gap: 1.1rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.12);
    }
    .status-banner-warning {
        background: linear-gradient(90deg, rgba(120, 53, 15, 0.45) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        display: flex;
        align-items: center;
        gap: 1.1rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.12);
    }
    .status-banner-normal {
        background: linear-gradient(90deg, rgba(20, 83, 45, 0.45) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(34, 197, 94, 0.4);
        border-left: 4px solid #22c55e;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        display: flex;
        align-items: center;
        gap: 1.1rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.12);
    }

    /* Content Display Cards & Panels */
    .content-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.4rem;
        min-height: 380px;
        font-size: 0.94rem;
        color: #cbd5e1;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    /* Sidebar Note */
    .sidebar-note {
        background: rgba(6, 78, 59, 0.35);
        border: 1px solid rgba(52, 211, 153, 0.25);
        border-left: 3px solid #10b981;
        border-radius: 10px;
        padding: 0.95rem;
        font-size: 0.82rem;
        color: #a7f3d0;
        margin-top: 1.5rem;
        line-height: 1.5;
    }

    /* Expander & JSON container dark polish */
    [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
    }
    [data-testid="stJson"] {
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
    }
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.25rem 0 0.5rem 0;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.01em;">
                🏭 Industrial Monitoring
            </div>
            <div style="font-size: 0.95rem; font-weight: 600; color: #38bdf8; margin-bottom: 0.25rem;">
                & Fault Diagnosis
            </div>
            <div style="font-size: 0.76rem; color: #64748b; font-weight: 500;">
                ⚡ AI Agent powered by CrewAI + Groq
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    selected_page = st.radio(
        "Navigation",
        options=["🔍 Diagnosis", "ℹ️ About", "⚙️ How it works"],
        label_visibility="collapsed",
    )

    if selected_page == "🔍 Diagnosis":
        st.markdown(
            "<div style='margin-top: 1rem; margin-bottom: 0.5rem; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #94a3b8;'>🎛️ Machine Telemetry Input</div>",
            unsafe_allow_html=True,
        )
        machine_name = st.text_input("Machine name", value="Industrial Motor")
        temperature_c = st.number_input("Temperature (°C)", min_value=0.0, max_value=200.0, value=95.0, step=0.5)
        vibration_mm_s = st.number_input("Vibration (mm/s)", min_value=0.0, max_value=50.0, value=12.0, step=0.1)
        pressure_bar = st.number_input("Pressure (bar)", min_value=0.0, max_value=20.0, value=2.1, step=0.1)

        st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            run_clicked = st.button("▶ Run Diagnosis", type="primary", use_container_width=True)
        with col_btn2:
            clear_clicked = st.button("Clear", use_container_width=True)

        if clear_clicked:
            st.session_state["has_run"] = False
            st.session_state["agent_result"] = None
            st.rerun()

        st.markdown(
            """
            <div class="sidebar-note">
                💡 <b>Telemetry Notice</b><br>
                This is a learning demonstration using simulated sensor readings. 
                Thresholds are for demonstration only and not universal industrial limits.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------- MAIN CONTENT -----------------
st.markdown('<div class="main-title">Industrial Monitoring & Fault Diagnosis</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Analyze real-time sensor telemetry, detect anomalies, and generate AI-powered maintenance protocols.</div>', unsafe_allow_html=True)

if selected_page == "ℹ️ About":
    st.info(
        "### About Industrial Fault Diagnosis Agent\n"
        "This system leverages modern agentic AI (CrewAI) backed by high-speed inference (Groq) "
        "to assist plant operators and maintenance engineers in inspecting and diagnosing machinery.\n\n"
        "- **Sensor Validation**: Rules-based instant verification of operational thresholds.\n"
        "- **Autonomous Reasoning**: Diagnostic agent analyzes discrepancies and isolates potential mechanical issues.\n"
        "- **Safe Guidelines**: Recommends non-destructive physical inspections without risking safety."
    )
elif selected_page == "⚙️ How it works":
    st.info(
        "### Architecture & Flow\n"
        "1. **Input Collection**: Operators provide motor temperature, vibration velocity, and line pressure.\n"
        "2. **Tool Execution**: `sensor_tools.py` evaluates metrics against standard industrial demo thresholds.\n"
        "3. **CrewAI Agent Workflow**: The Maintenance Specialist Agent receives inputs and the tool outputs.\n"
        "4. **Synthesis**: Outputs probable causes (e.g. bearing wear, misalignment) and inspection checklist."
    )
else:
    # Diagnosis view
    if "has_run" not in st.session_state:
        st.session_state["has_run"] = False
        st.session_state["agent_result"] = None
        st.session_state["tool_output"] = None

    # Calculate status & ranges using Python function directly
    tool_res = analyze_sensor_data(
        temperature_c=temperature_c,
        vibration_mm_s=vibration_mm_s,
        pressure_bar=pressure_bar,
    )

    if run_clicked:
        st.session_state["has_run"] = True
        st.session_state["tool_output"] = tool_res
        
        with st.spinner("🤖 Running CrewAI agent diagnosis with Groq LLM..."):
            try:
                crew = crew_setup.build_crew()
                res = crew.kickoff(
                    inputs={
                        "machine_name": machine_name,
                        "temperature_c": temperature_c,
                        "vibration_mm_s": vibration_mm_s,
                        "pressure_bar": pressure_bar,
                    }
                )
                st.session_state["agent_result"] = str(res)
            except Exception as e:
                st.session_state["agent_result"] = f"Error during agent execution: {e}"

    # Calculate pin positions (percentage clamped 0-100)
    # Temp range 0 to 120
    temp_pct = min(max((temperature_c / 120.0) * 100, 0), 100)
    # Vib range 0 to 20
    vib_pct = min(max((vibration_mm_s / 20.0) * 100, 0), 100)
    # Pressure range 0 to 5.0
    pres_pct = min(max((pressure_bar / 5.0) * 100, 0), 100)

    # 1. Metric Cards with Progress Bars
    st.markdown('<div class="section-title">📊 Live Sensor Telemetry</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-card-header">
                    <span>Temperature</span>
                    <span style="font-size: 1.3rem;">🌡️</span>
                </div>
                <div class="metric-card-value" style="color: #f87171; text-shadow: 0 0 20px rgba(248, 113, 113, 0.25);">
                    {temperature_c:.1f} °C
                </div>
                <div class="bar-container" style="background: linear-gradient(to right, #10b981 0%, #10b981 62.5%, #f59e0b 62.5%, #f59e0b 75%, #ef4444 75%, #ef4444 100%);">
                    <div class="bar-pin" style="left: {temp_pct}%;"></div>
                </div>
                <div class="bar-labels">
                    <span>0°C</span>
                    <span>75°C</span>
                    <span>90°C</span>
                    <span>120°C</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-card-header">
                    <span>Vibration</span>
                    <span style="font-size: 1.3rem;">📈</span>
                </div>
                <div class="metric-card-value" style="color: #f87171; text-shadow: 0 0 20px rgba(248, 113, 113, 0.25);">
                    {vibration_mm_s:.1f} mm/s
                </div>
                <div class="bar-container" style="background: linear-gradient(to right, #10b981 0%, #10b981 25%, #f59e0b 25%, #f59e0b 50%, #ef4444 50%, #ef4444 100%);">
                    <div class="bar-pin" style="left: {vib_pct}%;"></div>
                </div>
                <div class="bar-labels">
                    <span>0</span>
                    <span>5</span>
                    <span>10</span>
                    <span>20 mm/s</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-card-header">
                    <span>Line Pressure</span>
                    <span style="font-size: 1.3rem;">⏲️</span>
                </div>
                <div class="metric-card-value" style="color: #4ade80; text-shadow: 0 0 20px rgba(74, 222, 128, 0.25);">
                    {pressure_bar:.1f} bar
                </div>
                <div class="bar-container" style="background: linear-gradient(to right, #ef4444 0%, #ef4444 20%, #f59e0b 20%, #f59e0b 30%, #10b981 30%, #10b981 90%, #ef4444 90%, #ef4444 100%);">
                    <div class="bar-pin" style="left: {pres_pct}%;"></div>
                </div>
                <div class="bar-labels">
                    <span>0</span>
                    <span>1.5</span>
                    <span>4.5</span>
                    <span>5.0 bar</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Overall Status Banner
    status_text = tool_res["status"]
    if "CRITICAL" in status_text:
        st.markdown(
            f"""
            <div class="status-banner-critical">
                <span style="font-size: 2.1rem; filter: drop-shadow(0 0 8px rgba(239,68,68,0.6));">🚨</span>
                <div>
                    <h3 style="margin: 0; color: #fca5a5; font-size: 1.15rem; font-weight: 700; letter-spacing: 0.02em;">OVERALL STATUS: {status_text}</h3>
                    <p style="margin: 0.2rem 0 0 0; color: #fecaca; font-size: 0.9rem; opacity: 0.9;">Critical anomalies detected in sensor readings. Immediate diagnostic review recommended below.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif "WARNING" in status_text:
        st.markdown(
            f"""
            <div class="status-banner-warning">
                <span style="font-size: 2.1rem; filter: drop-shadow(0 0 8px rgba(245,158,11,0.6));">⚠️</span>
                <div>
                    <h3 style="margin: 0; color: #fcd34d; font-size: 1.15rem; font-weight: 700; letter-spacing: 0.02em;">OVERALL STATUS: {status_text}</h3>
                    <p style="margin: 0.2rem 0 0 0; color: #fde68a; font-size: 0.9rem; opacity: 0.9;">Elevated readings detected. Close operational monitoring recommended.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="status-banner-normal">
                <span style="font-size: 2.1rem; filter: drop-shadow(0 0 8px rgba(34,197,94,0.6));">✅</span>
                <div>
                    <h3 style="margin: 0; color: #86efac; font-size: 1.15rem; font-weight: 700; letter-spacing: 0.02em;">OVERALL STATUS: {status_text}</h3>
                    <p style="margin: 0.2rem 0 0 0; color: #bbf7d0; font-size: 0.9rem; opacity: 0.9;">All sensor readings are operating within nominal demo thresholds.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Two columns: Sensor Analysis (Tool Output) and AI Diagnosis Report (CrewAI Agent)
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-title">🔧 Sensor Analysis (Tool Output)</div>', unsafe_allow_html=True)
        st.json(tool_res)

    with col_right:
        st.markdown('<div class="section-title">🤖 AI Diagnosis Report (CrewAI Agent)</div>', unsafe_allow_html=True)
        
        if st.session_state.get("agent_result"):
            st.markdown(
                f'<div class="content-box">{st.session_state["agent_result"]}</div>',
                unsafe_allow_html=True,
            )
        elif st.session_state.get("has_run"):
            st.info("Analysis running or completed.")
        else:
            # Display simulated initial state matching the design mock or guidance
            st.markdown(
                f"""
                <div class="content-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.08);">
                        <span style="color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">Target Asset</span>
                        <span style="color: #38bdf8; font-weight: 700; font-size: 1rem;">{machine_name}</span>
                    </div>
                    <div style="margin-bottom: 1.25rem;">
                        <div style="color: #94a3b8; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Current Telemetry Snapshot</div>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; background: rgba(9, 13, 22, 0.6); padding: 0.85rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                            <div>
                                <div style="color: #64748b; font-size: 0.75rem;">Temperature</div>
                                <div style="color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-weight: 600;">{temperature_c:.1f} °C</div>
                            </div>
                            <div>
                                <div style="color: #64748b; font-size: 0.75rem;">Vibration</div>
                                <div style="color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-weight: 600;">{vibration_mm_s:.1f} mm/s</div>
                            </div>
                            <div>
                                <div style="color: #64748b; font-size: 0.75rem;">Pressure</div>
                                <div style="color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-weight: 600;">{pressure_bar:.1f} bar</div>
                            </div>
                        </div>
                    </div>
                    <div style="background: rgba(37, 99, 235, 0.1); border: 1px dashed rgba(56, 189, 248, 0.35); border-radius: 8px; padding: 1.1rem; text-align: center;">
                        <div style="color: #e2e8f0; font-weight: 600; margin-bottom: 0.35rem;">⚡ Ready for AI Diagnostic Sweep</div>
                        <div style="color: #94a3b8; font-size: 0.86rem;">
                            Click <b style="color: #38bdf8;">▶ Run Diagnosis</b> in the sidebar to engage the CrewAI agent for automated root-cause analysis and actionable inspection procedures.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # 4. Raw Agent Result Accordion
    st.markdown("---")
    st.markdown('<div class="section-title">📄 Raw Agent Result</div>', unsafe_allow_html=True)
    with st.expander("Show full result (for debugging)"):
        if st.session_state.get("agent_result"):
            st.text(st.session_state["agent_result"])
        else:
            st.write("No agent execution performed yet. Click 'Run Diagnosis' to execute.")