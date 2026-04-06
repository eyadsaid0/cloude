import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

st.set_page_config(page_title="Resistivity Lab Simulator", layout="wide")

=========================
STYLE
=========================

st.markdown("""

<style> body { background-color: #0e1117; } .block-container { padding-top: 2rem; } .metric-box { background-color: #1c1f26; padding: 15px; border-radius: 10px; text-align: center; } </style>

""", unsafe_allow_html=True)

=========================
FUNCTIONS
=========================

def compute_resistivity_two_probe(V, I, L, A, Rc, Rw):
R_measured = V / I if I != 0 else 0
R_sample = R_measured - (2 * Rc + Rw)
rho = R_sample * (A / L) if L != 0 else 0
return R_measured, R_sample, rho

def compute_resistivity_four_probe(V, I, s, t, mode="Bulk"):
if I == 0:
return 0
if mode == "Bulk":
rho = 2 * math.pi * s * (V / I)
else:
rho = (math.pi / math.log(2)) * t * (V / I)
return rho

def plot_interactive_graph(df):
if len(df) < 2:
return None, None

I = df["Current"]
V = df["Voltage"]

slope, intercept = np.polyfit(I, V, 1)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=I, y=V,
    mode='markers',
    name='Measurements'
))

fig.add_trace(go.Scatter(
    x=I,
    y=slope * I + intercept,
    mode='lines',
    name=f'Fit (R = {slope:.3f} Ω)'
))

fig.update_layout(
    template="plotly_dark",
    title="V-I Characteristics",
    xaxis_title="Current (A)",
    yaxis_title="Voltage (V)"
)

return fig, slope

def draw_probe_diagram(method):
if method == "Two-Probe":
st.markdown("### Two-Probe Configuration")
st.markdown("""
Current and voltage are measured using the same probes.
Contact resistance affects measurement.
""")
else:
st.markdown("### Four-Probe Configuration")
st.markdown("""
Outer probes inject current, inner probes measure voltage.
Eliminates contact resistance.
""")

=========================
SIDEBAR
=========================

st.sidebar.title("Control Panel")

method = st.sidebar.selectbox("Measurement Method", ["Two-Probe", "Four-Probe"])

st.sidebar.markdown("### Electrical Inputs")
I_input = st.sidebar.number_input("Current (A)", value=0.01)
V_input = st.sidebar.number_input("Voltage (V)", value=1.0)

st.sidebar.markdown("### Sample Parameters")
L = st.sidebar.number_input("Length (m)", value=1.0)
A = st.sidebar.number_input("Area (m²)", value=1e-6)
t = st.sidebar.number_input("Thickness (m)", value=1e-6)
s = st.sidebar.number_input("Probe Spacing (m)", value=0.01)

st.sidebar.markdown("### Resistances")
Rc = st.sidebar.number_input("Contact Resistance (Ω)", value=0.1)
Rw = st.sidebar.number_input("Wire Resistance (Ω)", value=0.05)

mode = None
if method == "Four-Probe":
mode = st.sidebar.radio("Mode", ["Bulk", "Thin Film"])

show_ideal = st.sidebar.checkbox("Show Ideal vs Real Measurement")

=========================
DATA INPUT
=========================

st.title("Resistivity Measurement Simulator")

st.markdown("### Experimental Data Input")

data = st.data_editor(
pd.DataFrame({
"Current": [0.01, 0.02, 0.03],
"Voltage": [1.0, 2.1, 3.05]
}),
num_rows="dynamic"
)

=========================
GRAPH
=========================

col1, col2 = st.columns([2, 1])

with col1:
fig, slope = plot_interactive_graph(data)
if fig:
st.plotly_chart(fig, use_container_width=True)

with col2:
draw_probe_diagram(method)

=========================
CALCULATIONS
=========================

st.markdown("## Results")

col1, col2, col3 = st.columns(3)

if method == "Two-Probe":
Rm, Rs, rho = compute_resistivity_two_probe(V_input, I_input, L, A, Rc, Rw)

with col1:
    st.metric("Measured Resistance (Ω)", f"{Rm:.4f}")
with col2:
    st.metric("Sample Resistance (Ω)", f"{Rs:.4f}")
with col3:
    st.metric("Resistivity (ρ)", f"{rho:.4e}")

else:
rho = compute_resistivity_four_probe(V_input, I_input, s, t, mode)

with col1:
    st.metric("Slope (Resistance)", f"{slope:.4f}" if slope else "N/A")
with col2:
    st.metric("Resistivity (ρ)", f"{rho:.4e}")
with col3:
    st.metric("Method", mode)
=========================
FORMULAS
=========================

st.markdown("## Governing Equations")

if method == "Two-Probe":
st.latex(r"R = \frac{V}{I}")
st.latex(r"R_{sample} = R - (2R_c + R_w)")
st.latex(r"\rho = R_{sample} \cdot \frac{A}{L}")
else:
if mode == "Bulk":
st.latex(r"\rho = 2\pi s \cdot \frac{V}{I}")
else:
st.latex(r"\rho = \frac{\pi}{\ln(2)} \cdot t \cdot \frac{V}{I}")

=========================
IDEAL VS REAL
=========================

if show_ideal and method == "Two-Probe":
ideal_R = V_input / I_input if I_input != 0 else 0
real_R = ideal_R - (2 * Rc + Rw)

st.markdown("## Ideal vs Real Comparison")
st.write(f"Ideal Resistance: {ideal_R:.4f} Ω")
st.write(f"Real Resistance: {real_R:.4f} Ω")
=========================
EXPLANATION BOX
=========================

st.markdown("## Why Four-Probe is More Accurate")

st.info("""
The four-probe method eliminates the effect of contact and wire resistance by separating current injection and voltage measurement.

This ensures that the measured voltage drop is only due to the sample itself, making it significantly more accurate—especially for low-resistance materials.
""")