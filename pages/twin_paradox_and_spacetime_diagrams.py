import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set up
st.set_page_config(page_title="Twin Paradox Simulator", layout="centered")
st.title("👯‍♂️ Twin Paradox Simulator")

st.latex(r"""
\text{Earth twin:} \quad \tau_A = T \\
\text{Traveling twin:} \quad \tau_B = T \sqrt{1 - v^2}
""")

# ---------------- INPUT SECTION ----------------
st.subheader("🔧 Input Parameters")

# Speed input
v = st.number_input("Traveler's speed v (as fraction of c)", min_value=0.0, max_value=0.99, value=0.8, step=0.01)

# Time input
col1, col2 = st.columns([2, 1])
with col1:
    T_raw = st.number_input("Total coordinate time on Earth (T)", min_value=0.1, value=10.0, step=0.1)
with col2:
    unit = st.selectbox("Time unit", ["seconds", "minutes", "hours", "days", "years"])

# Convert input time to seconds (for internal consistency)
unit_factors = {
    "seconds": 1,
    "minutes": 60,
    "hours": 3600,
    "days": 86400,
    "years": 365.25 * 24 * 3600,
}
T_seconds = T_raw * unit_factors[unit]

# ---------------- CALCULATION ----------------
gamma = 1 / np.sqrt(1 - v**2)
tau_A = T_seconds
tau_B = T_seconds / gamma
delta_tau = tau_A - tau_B

# Format outputs to selected unit
T_display = T_raw
tau_B_display = tau_B / unit_factors[unit]
delta_display = delta_tau / unit_factors[unit]

# Worldline data
t = np.linspace(0, T_display, 300)
x_out = v * t[t <= T_display/2]
x_back = v * (T_display - t[t > T_display/2])
x_travel = np.concatenate((x_out, x_back))
t_travel = np.concatenate((t[t <= T_display/2], t[t > T_display/2]))

# ---------------- LAYOUT ----------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌌 Spacetime Diagram")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot([0, 0], [0, T_display], label="Earth twin", color="blue")
    ax.plot(x_travel, t_travel, label="Traveling twin", color="red")
    ax.set_xlabel("x")
    ax.set_ylabel(f"t ({unit})")
    ax.set_xlim(-T_display * v * 1.1, T_display * v * 1.1)
    ax.set_ylim(0, T_display)
    ax.set_title("Worldlines")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with col4:
    st.subheader("📊 Results")
    st.latex(rf"\gamma = \frac{{1}}{{\sqrt{{1 - v^2}}}} = {gamma:.4f}")
    st.latex(rf"\tau_A = {T_display:.4f}~\text{{{unit}}}")
    st.latex(rf"\tau_B = {tau_B_display:.4f}~\text{{{unit}}}")
    st.latex(rf"\Delta \tau = {delta_display:.4f}~\text{{{unit}}}")
    if delta_display > 0:
        st.success("✅ Earth twin is older. Time dilation confirmed.")
    else:
        st.error("⚠️ Error: Travel twin shouldn't age more. Check inputs.")

