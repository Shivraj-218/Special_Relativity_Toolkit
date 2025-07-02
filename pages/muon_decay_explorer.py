import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit Setup
st.set_page_config(page_title="Muon Lifetime Simulator", layout="centered")
st.title("☄️ Muon Lifetime Simulator: A Proof of Time Dilation")

st.markdown("""
Muons are created ~10–15 km above Earth's surface by cosmic rays. Their rest-frame lifetime is only 2.2 μs, 
yet they are observed in abundance at ground level. This simulator shows how **time dilation** allows them to survive.
""")

# ---------- Constants ----------
c = 3e8  # speed of light in m/s
tau_0 = 2.2e-6  # muon lifetime in seconds (rest frame)

# ---------- Centered Inputs ----------
st.markdown("### 🔧 Simulation Controls")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    h_km = st.slider("Atmospheric Depth (km)", 5, 20, 10)

with col2:
    v_frac = st.slider("Muon Speed (v/c)", 0.90, 0.99999, 0.998, step=0.00001)

with col3:
    N0 = st.number_input("Initial Muon Count", min_value=1000, value=10000, step=1000)

# ---------- Calculations ----------
h = h_km * 1000  # m
v = v_frac * c
gamma = 1 / np.sqrt(1 - v**2 / c**2)
t_Earth = h / v
tau_dilated = gamma * tau_0

# With SR
N_survive = N0 * np.exp(-t_Earth / tau_dilated)

# Without SR
N_decay_classical = N0 * np.exp(-t_Earth / tau_0)

# ---------- Display Results ----------
st.subheader("📊 Summary of Results")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Lorentz Factor (γ)", f"{gamma:.4f}")
    st.latex(rf"\gamma = \frac{{1}}{{\sqrt{{1 - v^2/c^2}}}} = {gamma:.4f}")

with col2:
    st.metric("Time Taken (Earth Frame)", f"{t_Earth*1e6:.2f} μs")
    st.latex(rf"t = \frac{{h}}{{v}} = {t_Earth:.3e}~\text{{s}}")

with col3:
    st.metric("Dilated Lifetime", f"{tau_dilated*1e6:.2f} μs")
    st.latex(rf"\tau = \gamma \tau_0 = {tau_dilated:.3e}~\text{{s}}")

st.markdown("---")

# ---------- Plot: Muon Survival Comparison ----------
st.subheader("📈 Muon Survival: With and Without Relativity")

altitudes = np.linspace(0, h, 500)
times = altitudes / v
muons_SR = N0 * np.exp(-times / tau_dilated)
muons_classical = N0 * np.exp(-times / tau_0)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(altitudes / 1000, muons_SR, label="With Time Dilation (Relativity)", color='blue')
ax.plot(altitudes / 1000, muons_classical, label="Without Time Dilation (Classical)", color='red', linestyle='--')
ax.axvline(x=h_km, color='gray', linestyle=':', label=f"Surface @ {h_km} km")
ax.set_xlabel("Altitude (km)")
ax.set_ylabel("Surviving Muons")
ax.set_title("Muon Decay During Descent")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ---------- Final Survival Counts ----------
st.subheader("📊 Ground-Level Muon Count Comparison")
st.markdown(f"""
- **With Relativity:** ~{int(N_survive):,} muons reach the surface  
- **Without Relativity:** ~{int(N_decay_classical):,} muons reach the surface  
- **Time Dilation Gain:** ×{N_survive / N_decay_classical:.2f} more muons survive
""")
