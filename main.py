# app_ui
import streamlit as st
import algorithms

st.set_page_config(
    page_title="Mobile OS Scheduler Engine", page_icon="📱", layout="centered"
)

st.title("📱 Mobile OS Core Scheduler")
st.caption("Fixed presentation engine with integrated Round Robin mechanics.")

if "process_pipeline" not in st.session_state:
    st.session_state.process_pipeline = [
        {"pid": "Camera UI Thread", "at": 0, "bt": 5},
        {"pid": "Network Sync", "at": 2, "bt": 3},
        {"pid": "Background Download", "at": 4, "bt": 1},
    ]

# -----------------------------
# App Thread Form Deployment
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

    submit_btn = st.form_submit_button("Deploy Thread", use_container_width=True)
    if submit_btn and new_pid:
        # Avoid duplicate PIDs breaking map lookups
        if any(p["pid"] == new_pid for p in st.session_state.process_pipeline):
            st.error("A process with this name already exists!")
        else:
            st.session_state.process_pipeline.append(
                {"pid": new_pid, "at": new_at, "bt": new_bt}
            )
            st.toast(f"Thread '{new_pid}' injected into pipeline!")

if not st.session_state.process_pipeline:
    st.info("No active application threads running in the pipeline.")
    st.stop()

# -----------------------------
# Configuration Strategy Bar
# -----------------------------
st.write("### ⚙️ Strategy Core Framework Target")
algo_col, quantum_col = st.columns([2, 1])

with algo_col:
    selected_algo = st.radio(
        "Framework Strategy",
        ["FCFS", "SJF", "Round Robin"],
        horizontal=True,
        label_visibility="collapsed",
    )

with quantum_col:
    # Enable quantum slider ONLY for Round Robin
    if selected_algo == "Round Robin":
        quantum = st.slider(
            "Time Quantum", min_value=1, max_value=10, value=2, step=1
        )
    else:
        quantum = 2
        st.write("")  # Visual spacer alignment

# -----------------------------
# Run Active Framework Computations
# -----------------------------
fcfs_res, fcfs_g = algorithms.first_come_first_served(
    [dict(p) for p in st.session_state.process_pipeline]
)
sjf_res, sjf_g = algorithms.shortest_job_first(
    [dict(p) for p in st.session_state.process_pipeline]
)
rr_res, rr_g = algorithms.round_robin(
    [dict(p) for p in st.session_state.process_pipeline], quantum
)

# Pick calculation set based on choice
if selected_algo == "FCFS":
    active_results, active_gantt = fcfs_res, fcfs_g
elif selected_algo == "SJF":
    active_results, active_gantt = sjf_res, sjf_g
else:
    active_results, active_gantt = rr_res, rr_g

# Calculate Averages safely
avg_wt_fcfs = sum(r["wt"] for r in fcfs_res) / len(fcfs_res)
avg_wt_sjf = sum(r["wt"] for r in sjf_res) / len(sjf_res)
avg_wt_rr = (
    sum(r["wt"] for r in rr_res) / len(rr_res) if rr_res else 0
)

# -----------------------------
# Cross-Framework Multi-Metric Analytics Grid
# -----------------------------
st.write("### 📊 Cross-Engine Latency Matrix")
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric(label="FCFS Latency", value=f"{avg_wt_fcfs:.2f}s")
m_col2.metric(label="SJF Latency", value=f"{avg_wt_sjf:.2f}s")
m_col3.metric(label="RR Latency", value=f"{avg_wt_rr:.2f}s")

# -----------------------------
# FIXED Live Gantt Visualizer
# -----------------------------
st.write("### ⏱️ Live Threads Gantt Execution Tracker")

# We wrap the elements directly into native HTML syntax blocks
gantt_html = (
    '<div style="display: flex; flex-direction: row; gap: 8px; '
    'overflow-x: auto; padding: 10px 0; width: 100%;">'
)

for seg in active_gantt:
    duration = seg["end"] - seg["start"]
    box_width = max(80, duration * 35)
    gantt_html += f"""
    <div style="
        min-width: {box_width}px; 
        background-color: #1e293b; 
        border: 1px solid #00adb5; 
        border-radius: 6px; 
        padding: 8px; 
        text-align: center;
        color: white;
    ">
        <strong style="font-size: 13px; display: block; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{seg['pid']}</strong>
        <span style="font-size: 10px; color: #00adb5;">{seg['start']}s - {seg['end']}s</span>
    </div>
    """
gantt_html += "</div>"

# CRITICAL FIX: Explicitly call st.html() to stop code from leaking as raw string text
st.html(gantt_html)

# -----------------------------
# Log Data Grid Engine
# -----------------------------
st.write("### 📝 Pipeline Metrics Output Log")
st.dataframe(active_results, use_container_width=True, hide_index=True)

if st.button("Wipe Pipeline History", type="secondary"):
    st.session_state.process_pipeline = []
    st.rerun()
