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

# --- Inputs (Moved to Main Page) ---
st.subheader("🔧 Input Parameters")
col_input1, col_input2 = st.columns(2)

with col_input1:
    v_frac = st.slider("Source Speed (as fraction of c)", -0.99, 0.99, 0.3, 0.01)

with col_input2:
    mode = st.radio("Input Type", ["Wavelength (nm)", "Frequency (THz)"])

# Conditionally render wavelength/frequency input below the radio button
if mode == "Wavelength (nm)":
    λ_emit = st.number_input("Emitted Wavelength (nm)", value=500.0)
    λ_emit_m = λ_emit * 1e-9
    f_emit = c / λ_emit_m
else:
    f_emit = st.number_input("Emitted Frequency (THz)", value=600.0)
    f_emit *= 1e12
    λ_emit_m = c / f_emit
    λ_emit = λ_emit_m * 1e9

# --- Doppler Shift Calculations ---
beta = v_frac
# The factor formula is correct for frequency shift (positive beta = recession)
# f_obs = f_emit * sqrt((1 - beta) / (1 + beta))
factor_freq = np.sqrt((1 - beta) / (1 + beta))
f_obs = f_emit * factor_freq

# lambda_obs = lambda_emit * sqrt((1 + beta) / (1 - beta))
# Note: The LaTeX in your original code shows lambda_obs = lambda_emit * sqrt((1 + v/c) / (1 - v/c))
# This is equivalent to lambda_obs = lambda_emit / factor_freq
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
    # Clarify the sign convention for v_frac
    if v_frac > 0:
        st.success("🔴 Redshift (Source Receding)")
    elif v_frac < 0:
        st.success("🔵 Blueshift (Source Approaching)")
    else:
        st.info("No Shift (Source Stationary)")

# --- Spectrum Plot ---
st.subheader("🌈 Shifted Spectrum Visualization")

wavelengths = np.linspace(380, 750, 1000)
spectrum = np.exp(-0.5 * ((wavelengths - λ_obs)/10)**2)  # Gaussian at observed wavelength

fig, ax = plt.subplots(figsize=(8, 1.5))
for i in range(len(wavelengths) - 1):
    # This creates a smooth color gradient across the visible spectrum
    color_normalized = (wavelengths[i] - 380) / (750 - 380)
    color = plt.cm.jet(color_normalized) # Jet or viridis might be better than hsv for spectrum representation
    ax.axvspan(wavelengths[i], wavelengths[i+1], color=color, alpha=spectrum[i])

# Plotting the peak of the observed wavelength
ax.axvline(λ_obs, color='white', linestyle='--', label=f"Observed $\\lambda = {λ_obs:.1f}$ nm")
ax.axvline(λ_emit, color='red', linestyle=':', label=f"Emitted $\\lambda = {λ_emit:.1f}$ nm") # Add emitted wavelength for comparison

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
f_{\text{obs}} = f_{\text{emit}} \sqrt{\frac{1 - v/c}{1 + v/c}} \\
\lambda_{\text{obs}} = \lambda_{\text{emit}} \sqrt{\frac{1 + v/c}{1 - v/c}} \\
z = \frac{\lambda_{\text{obs}} - \lambda_{\text{emit}}}{\lambda_{\text{emit}}} = \frac{f_{\text{emit}} - f_{\text{obs}}}{f_{\text{obs}}}
""")





st.markdown(r"""
                     
     $z > 0$: Redshift (receding source)
     $z < 0$: Blueshift (approaching source)

This phenomenon is fundamental in astrophysics and cosmology — it helps us:
- Measure galaxy velocities
- Estimate distances (via Hubble's law)
- Analyze binary stars, jets, and quasars
- Explore the universe’s expansion history
""")
# --- End Fixed Section ---

st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
