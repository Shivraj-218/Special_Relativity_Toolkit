import streamlit as st
import numpy as np

# --- Constants ---
c = 3e8  # Speed of light in m/s

# --- Page Setup ---
st.set_page_config(page_title="Spacetime Interval Checker", layout="centered")
st.title("🕳️ Spacetime Interval Checker")


st.markdown("""
This app determines whether the interval between two events in Minkowski spacetime is
**time-like**, **light-like**, or **space-like**.
""")

st.markdown("**Metric Signature Used**: \( (+, -, -, -) \)")

st.markdown("---")
st.subheader("Spacetime Interval:")
st.latex(r"s^2 = c^2 (\Delta t)^2 - (\Delta x)^2 - (\Delta y)^2 - (\Delta z)^2")
st.markdown("This quantity is **invariant** under Lorentz transformations.")


# --- Coordinate Inputs ---
st.header("📍 Enter Event Coordinates")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Event 1")
    t1 = st.number_input("t₁ (s)", value=0.0, key="t1")
    x1 = st.number_input("x₁ (m)", value=0.0, key="x1")
    y1 = st.number_input("y₁ (m)", value=0.0, key="y1")
    z1 = st.number_input("z₁ (m)", value=0.0, key="z1")

with col2:
    st.subheader("Event 2")
    t2 = st.number_input("t₂ (s)", value=0.0, key="t2")
    x2 = st.number_input("x₂ (m)", value=0.0, key="x2")
    y2 = st.number_input("y₂ (m)", value=0.0, key="y2")
    z2 = st.number_input("z₂ (m)", value=0.0, key="z2")

# --- Compute and Classify ---
if st.button("🔍 Check Spacetime Interval"):
    dt = t2 - t1
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    s_squared = (c * dt)**2 - dx**2 - dy**2 - dz**2

    st.markdown("### 🧮 Results")
    st.latex(r"s^2 = c^2 (\Delta t)^2 - (\Delta x)^2 - (\Delta y)^2 - (\Delta z)^2")

    # --- START OF CUSTOM FORMATTING FOR S_SQUARED ---
    if s_squared == 0:
        s_squared_display_latex = r"0 \, \text{m}^2"
    else:
        s_sign = "" if s_squared >= 0 else "-"
        abs_s_squared = abs(s_squared)

        if abs_s_squared >= 1 or abs_s_squared == 0: # For large numbers or exactly zero
            exponent = int(np.floor(np.log10(abs_s_squared))) if abs_s_squared > 0 else 0
            mantissa = abs_s_squared / (10**exponent) if abs_s_squared > 0 else 0.0
            s_squared_display_latex = rf"{s_sign}{mantissa:.4f} \times 10^{{{exponent}}} \, \text{{m}}^2"
        else: # For small numbers (0 < abs_s_squared < 1)
            # Find the exponent for numbers like 0.0001
            exponent = int(np.floor(np.log10(abs_s_squared)))
            mantissa = abs_s_squared / (10**exponent)
            s_squared_display_latex = rf"{s_sign}{mantissa:.4f} \times 10^{{{exponent}}} \, \text{{m}}^2"

    st.latex(rf"s^2 = {s_squared_display_latex}")
    # --- END OF CUSTOM FORMATTING FOR S_SQUARED ---


    # --- CORRECTED CLASSIFICATION DISPLAY ---
    if np.isclose(s_squared, 0.0, atol=1e-8):
        st.success("Interval Classification:") # Status message for the box color
        st.latex(r"\text{This is a } \textbf{light-like (null)} \text{ interval.}")
    elif s_squared > 0:
        st.info("Interval Classification:")
        st.latex(r"\text{This is a } \textbf{time-like} \text{ interval.}")
    else: # s_squared < 0
        st.warning("Interval Classification:")
        st.latex(r"\text{This is a } \textbf{space-like} \text{ interval.}")
    # --- END CORRECTED CLASSIFICATION DISPLAY ---

st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
