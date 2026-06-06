# app_ui.py
import streamlit as st
import algorithms  # Importing your unchanged logic engine cleanly

# Page Configurations optimized for mobile layouts
st.set_page_config(
    page_title="Mobile OS Scheduler Engine", page_icon="📱", layout="centered"
)

st.title("📱 Mobile OS Core Scheduler")
st.caption(
    "A decoupled execution matrix framework simulation for mobile application threads."
)

# -----------------------------
# Core State Initialization
# -----------------------------
if "process_pipeline" not in st.session_state:
    st.session_state.process_pipeline = [
        {"pid": "Camera Framework", "at": 0, "bt": 5},
        {"pid": "Network Thread", "at": 2, "bt": 3},
        {"pid": "UI Sync Engine", "at": 4, "bt": 1},
    ]

# -----------------------------
# Input Form Panel (Responsive Mobile Layout)
# -----------------------------
with st.form("process_form", clear_on_submit=True):
    st.write("**Deploy a New Application Thread**")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        new_pid = st.text_input("App Name (PID)", placeholder="e.g., WhatsApp")
    with col2:
        new_at = st.number_input("Arrival Clock", min_value=0, value=0, step=1)
    with col3:
        new_bt = st.number_input("Burst Cycles", min_value=1, value=2, step=1)

    submit_btn = st.form_submit_with_clicks = st.form_submit_button(
        "Deploy Thread", use_container_width=True
    )

    if submit_btn and new_pid:
        st.session_state.process_pipeline.append(
            {"pid": new_pid, "at": new_at, "bt": new_bt}
        )
        st.toast(f"Thread '{new_pid}' injected into pipeline!")

# Stop execution gracefully if the pipeline is emptied out
if not st.session_state.process_pipeline:
    st.info("No active application threads running in the pipeline.")
    st.stop()

# -----------------------------
# Logic Engine Calculations Matrix
# -----------------------------
# Run both models concurrently to populate the analytics dashboard cards
fcfs_res, fcfs_gantt = algorithms.first_come_first_served(
    [dict(p) for p in st.session_state.process_pipeline]
)
sjf_res, sjf_gantt = algorithms.shortest_job_first(
    [dict(p) for p in st.session_state.process_pipeline]
)

avg_wt_fcfs = sum(r["wt"] for r in fcfs_res) / len(fcfs_res)
avg_wt_sjf = sum(r["wt"] for r in sjf_res) / len(sjf_res)

# -----------------------------
# Cross-Framework Comparison Analytics Dashboard
# -----------------------------
st.write("### 📊 Cross-Engine Analytics Matrix")
metric_col1, metric_col2 = st.columns(2)
metric_col1.metric(
    label="FCFS Avg Latency", value=f"{avg_wt_fcfs:.2f}s", delta_color="inverse"
)
metric_col2.metric(
    label="SJF Avg Latency", value=f"{avg_wt_sjf:.2f}s", delta_color="inverse"
)

# Strategy Controller Selector Toggle Switch
selected_algo = st.radio(
    "Active Framework Engine Strategy:",
    ["FCFS", "SJF"],
    horizontal=True,
    label_visibility="collapsed",
)
active_results, active_gantt = (
    (fcfs_res, fcfs_gantt) if selected_algo == "FCFS" else (sjf_res, sjf_gantt)
)

# -----------------------------
# Live Horizontal Gantt Tracker View (Pure Markdown Flow)
# -----------------------------
st.write("### ⏱️ Live Threads Gantt Execution Tracker")
gantt_html = '<div style="display: flex; flex-direction: row; gap: 8px; overflow-x: auto; padding: 10px 0;">'

for seg in active_gantt:
    duration = seg["end"] - seg["start"]
    box_width = max(80, duration * 30)
    gantt_html += f"""
    <div style="
        min-width: {box_width}px; 
        background-color: #1e293b; 
        border: 1px solid #00adb5; 
        border-radius: 6px; 
        padding: 8px; 
        text-align: center;
        color: white;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
    ">
        <strong style="font-size: 13px; display:block; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{seg['pid']}</strong>
        <span style="font-size: 10px; color: #00adb5;">{seg['start']}s - {seg['end']}s</span>
    </div>
    """
gantt_html += "</div>"
st.markdown(gantt_html, unsafe_allow_html=True)

# -----------------------------
# Detailed Simulation Logs Grid
# -----------------------------
st.write("### 📝 Pipeline Metrics Output Log")
st.dataframe(active_results, use_container_width=True, hide_index=True)

# Quick Wipe Pipeline Mechanism UI Option
if st.button("Wipe Pipeline History", type="secondary"):
    st.session_state.process_pipeline = []
    st.rerun()
