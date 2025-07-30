import streamlit as st
from PIL import Image
import numpy as np
from mpmath import mp

# High precision for near-c speeds
mp.dps = 100

# Streamlit config
st.set_page_config(page_title="Length Contraction Simulator", layout="centered")
st.title("🚀 Length Contraction Simulator")

st.markdown("### 📏 Visualizing Length Contraction in Special Relativity")

st.latex(r"""
L = L_0 \sqrt{1 - \frac{v^2}{c^2}} = \frac{L_0}{\gamma}
""")

st.markdown(r"""
- Contraction occurs **only along the direction of motion** (horizontal).
- **Height remains unchanged** — only the **length along motion** shortens.
- \(L_0\) is the proper length (measured at rest), and \(L\) is the contracted length in the moving frame.
""")

# Velocity input
v_input = st.text_input("Enter velocity as a fraction of c (0 < v < 1):", "0.9")

# Image options
st.subheader("Choose an Image")
preset = st.checkbox("Use preset spaceship image")
uploaded_file = st.file_uploader("Or upload your own image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if preset:
    try:
        # NOTE: If 'spaceship.png' is in an 'images' subfolder, use the relative path:
        image = Image.open("images/spaceship.png").convert("RGBA")
        st.success("Using preset spaceship image from 'images' folder.")
    except FileNotFoundError:
        st.error("Missing file: 'images/spaceship.png'. Please ensure it's in the 'images' folder.")
        st.stop()
elif uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    st.success("Using uploaded image.")
else:
    st.warning("Please select a preset or upload an image.")
    st.stop()

# Velocity validation
try:
    v = mp.mpf(v_input.strip())
    if v <= 0 or v >= 1:
        raise ValueError
except:
    st.error("Invalid velocity. Must be a number strictly between 0 and 1.")
    st.stop()

# Lorentz contraction calculations
gamma = 1/mp.sqrt(1 - v**2)
contracted_fraction = 1/gamma
contraction_percent = (1 - contracted_fraction)*100

# Resize image horizontally only
orig_w, orig_h = image.size
new_w = int(orig_w * float(contracted_fraction)) # Cast to float for Pillow's resize
contracted_image = image.resize((new_w, orig_h), Image.BICUBIC)

# Display results (vertical stack)
st.subheader("Results")

# Cap the original width for layout purposes to prevent overly large images
max_orig_width = 600
scale = min(max_orig_width / orig_w, 1.0) # Ensure image doesn't get scaled up if already small
disp_orig_w = int(orig_w * scale)
disp_new_w  = int(new_w  * scale)

# Original image
st.image(
    image,
    caption=f"Original (Rest Frame) – {orig_w}px",
    width=disp_orig_w
)

# Extra-large vertical gap (HTML hack for spacing)
st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)

st.markdown("**Contracted image is:**")

# Contracted image
st.image(
    contracted_image,
    width=disp_new_w
)

# Separator
st.markdown("---")

# Summary
st.markdown(f"""
### 📉 Contraction Summary
- **Lorentz Factor (γ)**: `{mp.nstr(gamma, 20)}`
- **Original Width**: `{orig_w}px`
- **Contracted Width**: `{new_w}px`
- **Contraction Fraction**: `{float(contracted_fraction):.5f}`
- **Contraction**: `{float(contraction_percent):.2f}%`
- **Direction**: Horizontal only (length parallel to motion)
""")

st.markdown("""
<hr style='margin-top: 50px; margin-bottom: 10px'>

<div style='text-align: center; font-size: 14px; color: gray;'>
&copy; 2025 Shivraj Deshmukh — All Rights Reserved<br>
Created with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
