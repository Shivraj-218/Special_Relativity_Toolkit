import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# --- Setup ---
st.set_page_config(page_title="GPS Time Correction Simulator", layout="centered")
st.title("🛰️ GPS Time Correction Simulator")
st.markdown("""
This simulation shows how **Special Relativity (SR)** and **General Relativity (GR)** affect the onboard clocks of GPS satellites.
""")

# --- Constants ---
c = 3e8        # Speed of light (m/s)
g = 9.81       # Gravity (m/s²)
R_earth = 6.371e6  # Earth radius (m)

# --- Input Section ---
st.subheader("🔧 Satellite Parameters")
col1, col2 = st.columns(2)
with col1:
    alt_km = st.slider("Satellite Altitude (km)", 1000, 40000, 20200)
with col2:
    v_kms = st.slider("Satellite Speed (km/s)", 1.0, 8.0, 3.874)

alt = alt_km * 1e3  # m
v = v_kms * 1e3    # m/s

# --- Time Dilation Calculations ---
gamma = 1 / np.sqrt(1 - v**2 / c**2)
sr_drift = (1 - 1/gamma) * 86400       # seconds/day lost (SR)
gr_drift = (g * alt / c**2) * 86400    # seconds/day gained (GR)
net_drift_ns = (gr_drift - sr_drift) * 1e9  # ns/day

# --- Output Metrics ---
st.subheader("📊 Daily Time Drift Summary")

with st.container():
    st.metric("🔻 Special Relativity (Slower Clock)", f"-{sr_drift * 1e9:.2f} ns/day")
    st.latex(r"\Delta t_{SR} = t \left(1 - \frac{1}{\gamma} \right)")
st.divider()

with st.container():
    st.metric("🔺 General Relativity (Faster Clock)", f"+{gr_drift * 1e9:.2f} ns/day")
    st.latex(r"\Delta t_{GR} = t \cdot \frac{gh}{c^2}")
st.divider()

with st.container():
    st.metric("⚖️ Net Drift (GR - SR)", f"{net_drift_ns:.2f} ns/day")
    if net_drift_ns > 0:
        st.success("GPS clock ticks **faster** than Earth clock.")
    else:
        st.warning("GPS clock ticks **slower** than Earth clock.")

# --- Animation Settings ---
st.subheader("🎞️ Clock Drift Animation")
speed = st.slider("Animation Duration (seconds)", 1.0, 10.0, 4.0)

# Prepare data
days = np.linspace(0, 30, 300)
drift_over_days_ns = net_drift_ns * days

# --- Session State Initialization ---
if "running" not in st.session_state:
    st.session_state.running = False
if "frame_idx" not in st.session_state:
    st.session_state.frame_idx = 0

# --- Control Buttons ---
start, stop = st.columns(2)
with start:
    if st.button("▶️ Start Animation"):
        st.session_state.running = True
        st.session_state.frame_idx = 0
with stop:
    if st.button("⏹️ Stop Animation"):
        st.session_state.running = False

# --- Plot Area ---
plot_area = st.empty()

if st.session_state.running:
    # Animate from current frame
    for i in range(st.session_state.frame_idx, len(days)):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(days[:i+1], drift_over_days_ns[:i+1], color='darkgreen')
        ax.set_xlabel("Days")
        ax.set_ylabel("Cumulative Drift (ns)")
        ax.set_title("Net Time Difference: GPS vs Earth")
        ax.grid(True)
        plot_area.pyplot(fig)
        time.sleep(speed / len(days))
        st.session_state.frame_idx += 1
        if not st.session_state.running:
            break

    # If reached end, stop
    if st.session_state.frame_idx >= len(days):
        st.session_state.running = False
        st.success("✅ Animation complete. Press ▶️ to replay.")
else:
    # Static full plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(days, drift_over_days_ns, color='darkgreen')
    ax.set_xlabel("Days")
    ax.set_ylabel("Cumulative Drift (ns)")
    ax.set_title("Net Time Difference: GPS vs Earth")
    ax.grid(True)
    plot_area.pyplot(fig)

# --- Explanation ---
st.markdown("### 📚 Why This Matters")
st.info("""
Without relativistic corrections, GPS would accumulate errors of up to **10 km/day**.
Satellites are launched with clocks pre-adjusted to account for these effects, demonstrating Einstein’s relativity in action.
""")
