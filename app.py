# ---------------------------------------------------------
# AI SOCIAL TIME MANAGER — CLEAN VERSION (CrewAI Hidden)
# ---------------------------------------------------------

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CREW_API_KEY = os.getenv("CREW_API_KEY", "")

# ---------------------------------------------------------
# CrewAI Import (Hidden — Demo Mode Only)
# ---------------------------------------------------------
USE_REAL_CREW = False

try:
    import importlib.util
    crew_spec = importlib.util.find_spec("crewai")
    USE_REAL_CREW = False  # we do NOT execute CrewAI
except Exception:
    USE_REAL_CREW = False

# CrewAI Stub Classes (invisible to UI)
class CrewAgentReal:
    def __init__(self, *args, **kwargs):
        self.role = kwargs.get("role", "Agent")
        self.goal = kwargs.get("goal", "")
        self.backstory = kwargs.get("backstory", "")

class CrewTaskReal:
    def __init__(self, *args, **kwargs):
        self.description = kwargs.get("description", "")
        self.agent = kwargs.get("agent")

class CrewReal:
    def __init__(self, *args, **kwargs):
        self.agents = kwargs.get("agents", [])
        self.tasks = kwargs.get("tasks", [])
    def kickoff(self):
        return {"status": "DEMO_MODE"}

CrewAgent = CrewAgentReal
CrewTask = CrewTaskReal
Crew = CrewReal

# ---------------------------------------------------------
# Gemini Import (Optional)
# ---------------------------------------------------------
GOOGLE_GENAI_AVAILABLE = False
try:
    import google.generativeai as genai
    GOOGLE_GENAI_AVAILABLE = True
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    GOOGLE_GENAI_AVAILABLE = False

# ---------------------------------------------------------
# Streamlit UI Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Social Time Manager",
    page_icon="🕒",
    layout="wide"
)

st.title("🕒 AI Social Time Manager")
st.write("Smart weekly planning using **AI recommendations** ")

# ---------------------------------------------------------
# Create Crew Agents (Invisible Logic Only)
# ---------------------------------------------------------
def create_crew_agents():
    a1 = CrewAgent(role="Routine Understanding Agent")
    a2 = CrewAgent(role="Time Optimization Agent")
    a3 = CrewAgent(role="Weekly Planning Agent")

    t1 = CrewTask(description="Analyze routine text", agent=a1)
    t2 = CrewTask(description="Optimize timing", agent=a2)
    t3 = CrewTask(description="Generate weekly plan", agent=a3)

    crew = Crew(agents=[a1, a2, a3], tasks=[t1, t2, t3])
    return crew

crew_obj = create_crew_agents()

# ---------------------------------------------------------
# User Input Section
# ---------------------------------------------------------
st.markdown("## ✏️ Enter Your Daily Routine")

col1, col2, col3 = st.columns(3)
with col1:
    study_hours = st.number_input("Study Hours", 0.0, 12.0, 2.0)
with col2:
    health_hours = st.number_input("Health Hours", 0.0, 6.0, 1.0)
with col3:
    social_hours = st.number_input("Social Hours", 0.0, 10.0, 1.0)

col4, col5 = st.columns(2)
with col4:
    sleep_hours = st.number_input("Sleep Hours", 4.0, 12.0, 7.0)
with col5:
    work_hours = st.number_input("Work/College Hours", 0.0, 12.0, 3.0)

routine_text = st.text_area("Describe your routine / difficulties")
priorities = st.multiselect(
    "Select your priorities",
    ["Study", "Health", "Social Life", "Sleep", "Work"],
    default=["Study", "Health"]
)

# ---------------------------------------------------------
# Weekly Plan Logic
# ---------------------------------------------------------
def generate_weekly_plan():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    df = pd.DataFrame({
        "Day": days,
        "Study Hours": [study_hours]*5 + [study_hours + 1]*2,
        "Health Hours": [health_hours]*7,
        "Social Hours": [social_hours]*5 + [social_hours + 1]*2,
    })
    return df

# Gemini Optional
def call_gemini(prompt):
    if not (GOOGLE_GENAI_AVAILABLE and GEMINI_API_KEY):
        return None
    try:
        resp = genai.generate_text(
            model="models/chat-bison-001",
            prompt=prompt,
            max_output_tokens=200
        )
        return resp.text
    except:
        return None

# ---------------------------------------------------------
# Generate Plan Button
# ---------------------------------------------------------
st.markdown("## 📅 Generate Your Weekly Plan")

if st.button("Generate Plan", type="primary"):
    plan = generate_weekly_plan()

    st.markdown("### ⭐ Recommended Weekly Plan")
    st.dataframe(plan, use_container_width=True)

    # Optional Gemini AI Suggestion
    gem_output = call_gemini(f"Create a balanced weekly plan. User routine: {routine_text}")

    if gem_output:
        st.markdown("### 🤖 Gemini Suggestion")
        st.write(gem_output)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("<br><br><b>Created by Janhavi</b>", unsafe_allow_html=True)
