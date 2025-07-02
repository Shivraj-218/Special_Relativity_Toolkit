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
    st.latex(f"s^2 = {s_squared:.4e} \, \text{{m}}^2")

    if np.isclose(s_squared, 0.0, atol=1e-8):
        st.success("This is a **light-like (null)** interval.")
    elif s_squared > 0:
        st.info("This is a **time-like** interval.")
    else:
        st.warning("This is a **space-like** interval.")
