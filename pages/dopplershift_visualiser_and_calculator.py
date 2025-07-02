import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Setup ---
st.set_page_config(page_title="Cosmic Doppler Shift Explorer", layout="centered")
st.title("🌌 Cosmic Doppler Shift Explorer")
st.markdown("""
This simulator demonstrates how light from a moving source shifts in wavelength or frequency due to the **relativistic Doppler effect**.
Useful for analyzing galaxies, quasars, stellar jets, and high-speed objects.
""")

# --- Constants ---
c = 3e8  # speed of light in m/s

# --- Inputs ---
st.sidebar.header("🔧 Input Parameters")
v_frac = st.sidebar.slider("Source Speed (as fraction of c)", -0.99, 0.99, 0.3, 0.01)
mode = st.sidebar.radio("Input Type", ["Wavelength (nm)", "Frequency (THz)"])
if mode == "Wavelength (nm)":
    λ_emit = st.sidebar.number_input("Emitted Wavelength (nm)", value=500.0)
    λ_emit_m = λ_emit * 1e-9
    f_emit = c / λ_emit_m
else:
    f_emit = st.sidebar.number_input("Emitted Frequency (THz)", value=600.0)
    f_emit *= 1e12
    λ_emit_m = c / f_emit
    λ_emit = λ_emit_m * 1e9

# --- Doppler Shift Calculations ---
beta = v_frac
factor = np.sqrt((1 - beta) / (1 + beta))

f_obs = f_emit * factor
λ_obs_m = c / f_obs
λ_obs = λ_obs_m * 1e9
z = (λ_obs - λ_emit) / λ_emit

# --- Results ---
st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Observed λ (nm)", f"{λ_obs:.2f}")
with col2:
    st.metric("Observed f (THz)", f"{f_obs/1e12:.2f}")
with col3:
    st.metric("Redshift (z)", f"{z:.4f}")
    st.success("🔵 Blueshift" if v_frac < 0 else "🔴 Redshift")

# --- Spectrum Plot ---
st.subheader("🌈 Shifted Spectrum Visualization")

wavelengths = np.linspace(380, 750, 1000)
spectrum = np.exp(-0.5 * ((wavelengths - λ_obs)/10)**2)  # Gaussian at observed wavelength

fig, ax = plt.subplots(figsize=(8, 1.5))
for i in range(len(wavelengths) - 1):
    color = plt.cm.hsv((wavelengths[i]-380)/370)
    ax.axvspan(wavelengths[i], wavelengths[i+1], color=color, alpha=spectrum[i])

ax.axvline(λ_obs, color='white', linestyle='--', label=f"λ_obs = {λ_obs:.1f} nm")
ax.set_xlim(380, 750)
ax.set_yticks([])
ax.set_xlabel("Wavelength (nm)")
ax.set_title("Simulated Spectrum Shift")
ax.legend()
st.pyplot(fig)

# --- Info Box ---
st.markdown("### 📚 Explanation")
st.latex(r"""
\textbf{Relativistic Doppler effect} \text{ modifies the observed frequency and wavelength:} \\
\lambda_{\text{obs}} = \lambda_{\text{emit}} \cdot \sqrt{\frac{1 + v/c}{1 - v/c}} \\
z = \frac{\lambda_{\text{obs}} - \lambda_{\text{emit}}}{\lambda_{\text{emit}}}
""")

st.markdown(r"""
- \( z > 0 \): **Redshift** (receding source)  
- \( z < 0 \): **Blueshift** (approaching source)  

This phenomenon is fundamental in astrophysics and cosmology — it helps us:
- Measure galaxy velocities  
- Estimate distances (via Hubble's law)  
- Analyze binary stars, jets, and quasars  
- Explore the universe’s expansion history
""")
st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
