import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import math

# Page config for modern look
st.set_page_config(
    page_title="Resistivity Measurement Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for academic lab software feel
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #34495e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .stMetric > label {
        color: white !important;
        font-size: 0.9rem;
    }
    .stMetric > div > div {
        color: white !important;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def compute_two_probe(I, V, A, L, R_contact=0, R_wire=0):
    """Two-probe resistivity calculation"""
    if I == 0:
        return None, None, None
    
    R_measured = V / I
    R_sample = R_measured - 2 * R_contact - 2 * R_wire
    if R_sample < 0:
        R_sample = 0
    rho = R_sample * (A / L) if L > 0 else None
    return R_measured, R_sample, rho

def compute_four_probe(I, V, s, t=None, thin_film=False):
    """Four-probe resistivity calculation"""
    if I == 0:
        return None, None
    
    if thin_film and t is not None:
        rho = (math.pi / math.log(2)) * t * (V / I)
    else:
        rho = 2 * math.pi * s * (V / I)
    
    R = V / I
    return R, rho

def generate_sample_data(n_points=10, noise=0.05):
    """Generate realistic V-I data with noise"""
    I = np.linspace(0.1, 1.0, n_points)
    V_ideal = 50 * I  # 50 ohm resistance
    noise_factor = np.random.normal(1, noise, len(I))
    V_noisy = V_ideal * noise_factor
    return pd.DataFrame({'Current (mA)': I*1000, 'Voltage (mV)': V_noisy*1000})

def plot_vi_graph(data, method, R_true=None, show_fit=True):
    """Interactive V vs I plot with linear fit"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('V vs I Measurement', 'Resistance Analysis')
    )
    
    # Main V-I plot
    fig.add_trace(
        go.Scatter(x=data['Current (mA)'], y=data['Voltage (mV)'],
                  mode='markers+lines',
                  marker=dict(size=8, color='#3498db'),
                  line=dict(color='#3498db', width=2),
                  name='Measured Data',
                  showlegend=True),
        row=1, col=1
    )
    
    if show_fit and len(data) > 1:
        # Linear fit
        z = np.polyfit(data['Current (mA)'], data['Voltage (mV)'], 1)
        p = np.poly1d(z)
        fig.add_trace(
            go.Scatter(x=data['Current (mA)'], y=p(data['Current (mA)']),
                      mode='lines',
                      line=dict(color='red', width=3, dash='dash'),
                      name=f'Linear Fit (R = {z[0]:.2f} Ω)',
                      showlegend=True),
            row=1, col=1
        )
        
        # Residuals plot
        residuals = data['Voltage (mV)'] - p(data['Current (mA)'])
        fig.add_trace(
            go.Scatter(x=data['Current (mA)'], y=residuals,
                      mode='markers',
                      marker=dict(size=6, color='#e74c3c'),
                      name='Residuals',
                      showlegend=False),
            row=1, col=2
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=2)
    
    fig.update_layout(
        height=400,
        title_font_size=14,
        legend=dict(x=0.02, y=0.98),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    fig.update_xaxes(title_text="Current (mA)", row=1, col=1)
    fig.update_yaxes(title_text="Voltage (mV)", row=1, col=1)
    fig.update_xaxes(title_text="Current (mA)", row=1, col=2)
    fig.update_yaxes(title_text="Residuals (mV)", row=1, col=2)
    
    return fig

def draw_two_probe_diagram():
    """Two-probe diagram - fixed version"""
    fig = go.Figure()
    
    # Sample bar
    fig.add_shape(type="rect",
                  x0=0.1, y0=0.3, x1=0.9, y1=0.7,
                  line=dict(color="#2c3e50", width=3),
                  fillcolor="#34495e")
    
    # Probes
    fig.add_annotation(x=0.15, y=0.85, text="Probe 1<br>(I+, V+)", 
                      showarrow=True, arrowhead=2,
                      arrowcolor="#e74c3c", ax=0, ay=-40,
                      font=dict(size=10, color="#e74c3c"))
    
    fig.add_annotation(x=0.85, y=0.85, text="Probe 2<br>(I-, V-)", 
                      showarrow=True, arrowhead=2,
                      arrowcolor="#e74c3c", ax=0, ay=-40,
                      font=dict(size=10, color="#e74c3c"))
    
    # Current flow
    fig.add_annotation(x=0.2, y=0.2, text="I", showarrow=True,
                      arrowhead=2, arrowsize=1.5,
                      arrowcolor="#3498db", ax=40, ay=0)
    fig.add_annotation(x=0.8, y=0.2, text="I", showarrow=True,
                      arrowhead=2, arrowsize=1.5,
                      arrowcolor="#3498db", ax=-40, ay=0)
    
    fig.update_layout(
        width=400, height=300,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        annotations=[dict(text="Two-Probe Configuration", 
                         x=0.5, y=0.95, showarrow=False,
                         font=dict(size=14, color="#2c3e50"),
                         xref="paper", yref="paper")]
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

def draw_four_probe_diagram():
    """Four-probe diagram - fixed version"""
    fig = go.Figure()
    
    # Sample bar
    fig.add_shape(type="rect",
                  x0=0.1, y0=0.3, x1=0.9, y1=0.7,
                  line=dict(color="#2c3e50", width=3),
                  fillcolor="#34495e")
    
    # Current probes (outer)
    fig.add_annotation(x=0.2, y=0.85, text="I+", showarrow=True,
                      arrowhead=2, arrowcolor="#e74c3c", ax=0, ay=-40,
                      font=dict(size=12, color="#e74c3c"))
    fig.add_annotation(x=0.8, y=0.85, text="I-", showarrow=True,
                      arrowhead=2, arrowcolor="#e74c3c", ax=0, ay=-40,
                      font=dict(size=12, color="#e74c3c"))
    
    # Voltage probes (inner)
    fig.add_annotation(x=0.4, y=0.85, text="V+", showarrow=True,
                      arrowhead=2, arrowcolor="#f39c12", ax=0, ay=-40,
                      font=dict(size=12, color="#f39c12"))
    fig.add_annotation(x=0.6, y=0.85, text="V-", showarrow=True,
                      arrowhead=2, arrowcolor="#f39c12", ax=0, ay=-40,
                      font=dict(size=12, color="#f39c12"))
    
    # Current flow arrows
    for x in [0.25, 0.75]:
        fig.add_annotation(x=x, y=0.15, text="I", showarrow=True,
                          arrowhead=2, arrowsize=1.5,
                          arrowcolor="#3498db", ax=0, ay=30)
    
    fig.update_layout(
        width=400, height=300,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        annotations=[dict(text="Four-Probe Configuration", 
                         x=0.5, y=0.95, showarrow=False,
                         font=dict(size=14, color="#2c3e50"),
                         xref="paper", yref="paper")]
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

# Main App
st.markdown('<h1 class="main-header">🔬 Resistivity Measurement Lab</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Two-Probe vs Four-Probe Methods • Professional Analysis Tool</p>', unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("📊 Measurement Parameters")

method = st.sidebar.selectbox(
    "Measurement Method",
    ["Two-Probe", "Four-Probe"],
    index=1
)

# Common inputs
col1, col2 = st.sidebar.columns(2)
with col1:
    current = st.number_input("Current (mA)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
with col2:
    voltage = st.number_input("Voltage (mV)", min_value=0.0, max_value=5000.0, value=500.0, step=10.0)

# Method-specific inputs
if method == "Two-Probe":
    st.sidebar.subheader("Sample Geometry")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        length = st.number_input("Length (mm)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
    with col2:
        area = st.number_input("Area (mm²)", min_value=0.01, max_value=100.0, value=1.0, step=0.01)
    
    st.sidebar.subheader("Corrections")
    contact_res = st.number_input("Contact Resistance (Ω)", min_value=0.0, value=2.0, step=0.1)
    wire_res = st.number_input("Wire Resistance (Ω)", min_value=0.0, value=0.5, step=0.1)

elif method == "Four-Probe":
    st.sidebar.subheader("Probe Configuration")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        spacing = st.number_input("Probe Spacing s (mm)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    with col2:
        thickness = st.number_input("Thickness t (μm)", min_value=0.01, max_value=1000.0, value=10.0, step=0.1)
    
    thin_film_mode = st.sidebar.checkbox("Thin Film Mode", value=False)

# Data table option
use_table = st.sidebar.checkbox("📋 Use Multiple Data Points", value=False)
if use_table:
    st.sidebar.subheader("Dataset Controls")
    n_points = st.sidebar.slider("Number of points", 5, 20, 10)
    noise_level = st.sidebar.slider("Noise level (%)", 0.0, 10.0, 2.0)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📈 Interactive V-I Analysis")
    
    # Generate or use single point data
    if use_table:
        data = generate_sample_data(n_points, noise_level/100)
        current_avg = data['Current (mA)'].mean()
        voltage_avg = data['Voltage (mV)'].mean()
    else:
        data = pd.DataFrame({
            'Current (mA)': [current],
            'Voltage (mV)': [voltage]
        })
        current_avg, voltage_avg = current, voltage
    
    # Plot
    fig_vi = plot_vi_graph(data, method)
    st.plotly_chart(fig_vi, use_container_width=True)

with col2:
    st.header("🔍 Probe Configuration")
    
    if method == "Two-Probe":
        diagram = draw_two_probe_diagram()
        st.plotly_chart(diagram, use_container_width=True)
        st.markdown("**Formula:**")
        st.latex(r"R = \frac{V}{I}, \quad \rho = \left(R - 2R_c - 2R_w\right) \frac{A}{L}")
    else:
        diagram = draw_four_probe_diagram()
        st.plotly_chart(diagram, use_container_width=True)
        if thin_film_mode:
            st.markdown("**Thin Film:**")
            st.latex(r"\rho = \frac{\pi}{\ln 2} \cdot t \cdot \frac{V}{I}")
        else:
            st.markdown("**Bulk:**")
            st.latex(r"\rho = 2\pi s \frac{V}{I}")

# Results section
st.header("📊 Measurement Results")

# Calculations
if method == "Two-Probe":
    R_meas, R_sample, rho = compute_two_probe(
        current_avg/1000, voltage_avg/1000,
        area/1e6, length/1000,  # Convert to meters
        contact_res, wire_res
    )
    if R_sample is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Measured Resistance", f"{R_meas:.2f} Ω")
        with col2:
            st.metric("Sample Resistance", f"{R_sample:.2f} Ω")
        with col3:
            if rho:
                st.metric("Resistivity", f"{rho*1e6:.2f} μΩ·m")
        with col4:
            if len(data) > 1:
                z = np.polyfit(data['Current (mA)'], data['Voltage (mV)'], 1)
                st.metric("Graph Slope", f"{z[0]:.2f} Ω")
    
    st.info("⚠️ Two-probe includes contact & wire resistance errors")

else:  # Four-probe
    R, rho = compute_four_probe(
        current_avg/1000, voltage_avg/1000,
        spacing/1000, thickness/1e6 if thin_film_mode else None,
        thin_film=thin_film_mode
    )
    if rho is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Resistance", f"{R:.2f} Ω")
        with col2:
            st.metric("Resistivity", f"{rho*1e6:.2f} μΩ·m")
        with col3:
            if len(data) > 1:
                z = np.polyfit(data['Current (mA)'], data['Voltage (mV)'], 1)
                st.metric("Graph Slope", f"{z[0]:.2f} Ω")

# Data table display
if use_table and len(data) > 1:
    st.subheader("📋 Raw Data")
    st.dataframe(data, use_container_width=True)

# Explanation box
with st.container():
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Why Four-Probe is Superior</h3>
        <ul>
            <li><b>Eliminates contact resistance</b> - Voltage probes don't carry current</li>
            <li><b>No wire resistance error</b> - Pure sample measurement</li>
            <li><b>Higher accuracy</b> - Industry standard for precise ρ</li>
            <li><b>Works for thin films</b> - Special correction formulas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*Developed as professional laboratory instrumentation software | Units: SI standard*")