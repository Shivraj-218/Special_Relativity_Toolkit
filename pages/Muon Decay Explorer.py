import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpmath import mp

# Set decimal precision (e.g., 100 digits for extreme accuracy)
mp.dps = 100

# Streamlit Setup
st.set_page_config(page_title="Muon Lifetime Simulator", layout="centered")
st.title("☄️ Muon Lifetime Simulator: A Proof of Time Dilation")

st.markdown("""
Muons are created ~10–15 km above Earth's surface by cosmic rays. Their rest-frame lifetime is only 2.2 μs,
yet they are observed in abundance at ground level. This simulator shows how **time dilation** allows them to survive.
""")

# ---------- Constants (defined as mpmath objects for high precision calculations) ----------
c_mp = mp.mpf(3e8)  # speed of light in m/s
tau_0_mp = mp.mpf(2.2e-6)  # muon lifetime in seconds (rest frame)

# ---------- Centered Inputs ----------
st.markdown("### 🔧 Simulation Controls")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    h_km = st.slider("Atmospheric Depth (km)", 5, 20, 10)

with col2:
    # Changed to text_input to allow higher precision velocity input
    v_frac_str = st.text_input("Muon Speed (v/c) (e.g., 0.9999999):", "0.99999")

with col3:
    N0 = st.number_input("Initial Muon Count", min_value=1000, value=10000, step=1000)

# ---------- Input Validation and Calculations with mpmath ----------
try:
    # Convert v_frac string to mpmath float
    v_frac_mp = mp.mpf(v_frac_str.strip())

    # Validate velocity range
    if v_frac_mp <= 0 or v_frac_mp >= 1:
        raise ValueError("Velocity (v/c) must be strictly between 0 and 1.")

    # Convert other inputs to mpmath for consistent high-precision calculations
    h_mp = mp.mpf(h_km * 1000)  # Convert km to meters as mpmath float
    N0_mp = mp.mpf(N0)

    # Calculate v in m/s using mpmath
    v_mp = v_frac_mp * c_mp

    # Calculate Lorentz Factor (gamma) using mpmath
    gamma_mp = 1 / mp.sqrt(1 - (v_mp/c_mp)**2)

    # Calculate time taken in Earth's frame (t_Earth) using mpmath
    t_Earth_mp = h_mp / v_mp

    # Calculate Dilated Lifetime (tau_dilated) using mpmath
    tau_dilated_mp = gamma_mp * tau_0_mp

    # Calculate survival counts using mp.exp for high precision in exponential decay
    N_survive_mp = N0_mp * mp.exp(-t_Earth_mp / tau_dilated_mp)
    N_decay_classical_mp = N0_mp * mp.exp(-t_Earth_mp / tau_0_mp)

    # Convert final results back to standard floats for display and numpy/matplotlib compatibility
    gamma = float(gamma_mp)
    t_Earth = float(t_Earth_mp)
    tau_dilated = float(tau_dilated_mp)
    N_survive = float(N_survive_mp)
    N_decay_classical = float(N_decay_classical_mp)

except Exception as e:
    st.error(f"Invalid input or calculation error: {e}. Please ensure velocity is a valid number between 0 and 1.")
    st.stop() # Stop execution if input is invalid

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

# Ensure plot data is generated using standard floats compatible with numpy/matplotlib
altitudes = np.linspace(0, float(h_mp), 500)
times = altitudes / float(v_mp) # Convert v_mp to float for numpy array division

# The original tau_0 constant is used for the classical plot, which is already a float
muons_SR = N0 * np.exp(-times / tau_dilated)
muons_classical = N0 * np.exp(-times / float(tau_0_mp)) # Use the float version of tau_0_mp for this calculation

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
st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
