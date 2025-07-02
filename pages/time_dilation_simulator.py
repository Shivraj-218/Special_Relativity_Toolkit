import streamlit as st
import time
from mpmath import mp
import numpy as np
import plotly.graph_objs as go
from math import pi, cos, sin

# High precision math
mp.dps = 100

# Page setup
st.set_page_config(page_title="Time Dilation Snapshot Simulator", layout="wide")
st.title("⏳ Time Dilation Simulator — Final Snapshot with Live Digital Clocks")

st.markdown("""
Simulate relativistic time dilation:
- 🕒 **Digital clocks update live**
- 🕰️ **Analog clocks + time plot** shown **after pause/stop**
""")
st.latex(r"\gamma(v) = \frac{1}{\sqrt{1 - (v/c)^2}}")

# Input fields
v_input = st.text_input("Enter speed as a fraction of c (0 < v < 1):", "0.99")
sim_time = st.number_input("Duration of simulation (seconds):", min_value=1, value=30)

# Control buttons
start = st.button("▶️ Start")
pause = st.button("⏸️ Pause")
stop = st.button("⏹️ Stop")

# UI placeholders
col1, col2 = st.columns(2)
clock_col1 = col1.empty()
clock_col2 = col2.empty()
plot_area = st.empty()
digital_clocks = st.empty()
status_text = st.empty()

# Format digital time
def format_time(t):
    ms = int((t - int(t)) * 1000)
    return time.strftime("%H:%M:%S", time.gmtime(t)) + f".{ms:03d}"

# Draw analog clock
def draw_analog_clock(seconds_elapsed, title):
    sec_angle = 2 * pi * ((seconds_elapsed % 60) / 60)
    min_angle = 2 * pi * (((seconds_elapsed / 60) % 60) / 60)

    fig = go.Figure()
    fig.add_shape(type="circle", x0=-1, y0=-1, x1=1, y1=1, line=dict(color="white", width=3))

    # Second hand
    fig.add_trace(go.Scatter(
        x=[0, 0.9 * sin(sec_angle)],
        y=[0, 0.9 * cos(sec_angle)],
        mode="lines", line=dict(color="red", width=2), showlegend=False
    ))

    # Minute hand
    fig.add_trace(go.Scatter(
        x=[0, 0.7 * sin(min_angle)],
        y=[0, 0.7 * cos(min_angle)],
        mode="lines", line=dict(color="white", width=4), showlegend=False
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        width=300, height=300,
        plot_bgcolor="black", paper_bgcolor="black",
        margin=dict(l=10, r=10, t=40, b=10)
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

# Shared logic for snapshot rendering
def render_snapshot(earth_times, ship_times):
    final_earth = earth_times[-1]
    final_ship = ship_times[-1]

    # Digital clocks
    digital_clocks.markdown(f"""
    **🟢 Earth Clock:** `{format_time(final_earth)}`  
    **🛸 Ship Clock:** `{format_time(final_ship)}`  
    """)

    # Analog clocks
    clock_col1.plotly_chart(draw_analog_clock(final_earth, "🟢 Earth Clock (Final)"), use_container_width=True)
    clock_col2.plotly_chart(draw_analog_clock(final_ship, "🛸 Ship Clock (Final)"), use_container_width=True)

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=earth_times, y=earth_times, name="Earth Time", line=dict(color="green", width=2)))
    fig.add_trace(go.Scatter(x=earth_times, y=ship_times, name="Ship Time", line=dict(color="orange", width=2)))
    fig.update_layout(
        title="⏱️ Time Passage Comparison",
        xaxis_title="Earth Time (s)",
        yaxis_title="Elapsed Time (s)",
        width=900,
        height=400,
        template="plotly_dark"
    )
    plot_area.plotly_chart(fig, use_container_width=True)

# Start simulation
if start or pause or stop:
    try:
        v = mp.mpf(v_input.strip())
        if v < 0 or v >= 1:
            raise ValueError("Velocity must be in range (0, 1).")

        gamma = 1 / mp.sqrt(1 - v**2)
        gamma_float = float(gamma)
        status_text.success(f"Lorentz Factor γ = {mp.nstr(gamma, 20)}")

        # Time capture
        start_time = time.time()
        earth_times = []
        ship_times = []
        stop_triggered = False

        while True:
            now = time.time()
            elapsed_earth = now - start_time
            elapsed_ship = elapsed_earth / gamma_float

            earth_times.append(elapsed_earth)
            ship_times.append(elapsed_ship)

            # Live update of digital clocks
            digital_clocks.markdown(f"""
            **🟢 Earth Clock:** `{format_time(elapsed_earth)}`  
            **🛸 Ship Clock:** `{format_time(elapsed_ship)}`  
            """)

            if pause or stop or elapsed_earth >= sim_time:
                stop_triggered = True
                break

            time.sleep(0.066)  # ~15 FPS

        if stop_triggered:
            render_snapshot(earth_times, ship_times)
            if stop:
                status_text.info("⏹️ Simulation stopped.")
            else:
                status_text.info("⏸️ Simulation paused.")

    except Exception as e:
        status_text.error(f"Error: {e}")
