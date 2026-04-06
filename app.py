import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import io
import base64

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Resistivity Lab · Probe Methods",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap');

:root {
    --bg-deep:    #0a0e1a;
    --bg-card:    #111827;
    --bg-surface: #1c2333;
    --border:     #2a3347;
    --accent:     #38bdf8;
    --accent2:    #818cf8;
    --accent3:    #34d399;
    --warn:       #fb923c;
    --text-hi:    #f1f5f9;
    --text-lo:    #94a3b8;
    --mono:       'IBM Plex Mono', monospace;
    --sans:       'Inter', sans-serif;
    --display:    'Playfair Display', serif;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-hi) !important;
    font-family: var(--sans);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * { color: var(--text-hi) !important; }

h1, h2, h3, h4 { font-family: var(--sans); font-weight: 600; color: var(--text-hi); }

.lab-title {
    font-family: var(--display);
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin: 0;
}
.lab-subtitle {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--text-lo);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 6px;
}

.metric-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.metric-card.green  { border-left-color: var(--accent3); }
.metric-card.purple { border-left-color: var(--accent2); }
.metric-card.orange { border-left-color: var(--warn); }

.metric-label {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--text-lo);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.metric-value {
    font-family: var(--mono);
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--text-hi);
}
.metric-unit {
    font-size: 0.85rem;
    color: var(--text-lo);
    margin-left: 4px;
}

.info-box {
    background: linear-gradient(135deg, #0f2a3f 0%, #0f1f38 100%);
    border: 1px solid #1e4060;
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 20px 24px;
    margin: 20px 0;
}
.info-box h4 {
    color: var(--accent);
    font-family: var(--mono);
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.info-box p { color: #cbd5e1; line-height: 1.7; margin: 0; font-size: 0.93rem; }

.formula-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    margin: 10px 0;
    font-family: var(--mono);
    font-size: 0.9rem;
    color: var(--accent3);
}

.section-header {
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-lo);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin: 24px 0 16px 0;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 1px;
    font-weight: 600;
    text-transform: uppercase;
}
.badge-blue   { background: #0c2d48; color: var(--accent);  border: 1px solid #1a5c7a; }
.badge-green  { background: #0c3028; color: var(--accent3); border: 1px solid #1a6050; }

.stSlider > div > div > div { color: var(--accent) !important; }
.stNumberInput input, .stTextInput input {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-hi) !important;
    border-radius: 6px !important;
    font-family: var(--mono) !important;
}
.stSelectbox > div > div {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-hi) !important;
    border-radius: 6px !important;
}
div[data-testid="stDataFrame"] {
    background: var(--bg-surface) !important;
    border-radius: 10px;
    border: 1px solid var(--border);
}
.stButton > button {
    background: linear-gradient(135deg, #0369a1, #0284c7) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--mono) !important;
    letter-spacing: 1px !important;
    font-size: 0.8rem !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0284c7, #38bdf8) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(56,189,248,0.3) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-lo) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: none !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  COMPUTATION FUNCTIONS
# ─────────────────────────────────────────────

def compute_resistivity_two_probe(V, I, L, A, R_contact=0.0, R_wire=0.0):
    """Two-probe: includes contact + wire resistance in measurement."""
    if I == 0:
        return None, None, None
    R_measured = V / I
    R_sample = R_measured - (2 * R_contact + R_wire)
    if A == 0 or L == 0:
        return R_measured, R_sample, None
    rho = R_sample * (A / L)
    return R_measured, R_sample, rho


def compute_resistivity_four_probe(V, I, s, t=None, mode="bulk"):
    """Four-probe: eliminates contact resistance."""
    if I == 0:
        return None, None
    R_sheet = V / I
    if mode == "bulk":
        rho = 2 * np.pi * s * R_sheet
    else:  # thin film
        if t is None or t == 0:
            return R_sheet, None
        rho = (np.pi / np.log(2)) * t * R_sheet
    return R_sheet, rho


def linear_fit(currents, voltages):
    """Returns slope (resistance), intercept, R² from V vs I data."""
    if len(currents) < 2:
        return None, None, None
    coeffs = np.polyfit(currents, voltages, 1)
    slope, intercept = coeffs
    V_fit = np.polyval(coeffs, currents)
    ss_res = np.sum((np.array(voltages) - V_fit) ** 2)
    ss_tot = np.sum((np.array(voltages) - np.mean(voltages)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    return slope, intercept, r2


# ─────────────────────────────────────────────
#  PLOTLY GRAPH
# ─────────────────────────────────────────────

def plot_interactive_graph(df, method, show_ideal=False,
                            R_contact=0.0, R_wire=0.0):
    """Interactive V vs I Plotly graph with linear fit."""
    currents = df["Current (A)"].values
    voltages = df["Voltage (V)"].values

    slope, intercept, r2 = linear_fit(currents, voltages)
    I_range = np.linspace(min(currents) * 0.9, max(currents) * 1.1, 200)

    fig = go.Figure()

    # Scatter – measured data
    fig.add_trace(go.Scatter(
        x=currents, y=voltages,
        mode="markers",
        name="Measured Data",
        marker=dict(
            color="#38bdf8",
            size=10,
            symbol="circle",
            line=dict(width=1.5, color="#0ea5e9"),
            opacity=0.9,
        ),
        hovertemplate="I = %{x:.4e} A<br>V = %{y:.4e} V<extra></extra>",
    ))

    # Linear fit
    if slope is not None:
        V_fit = slope * I_range + intercept
        fig.add_trace(go.Scatter(
            x=I_range, y=V_fit,
            mode="lines",
            name=f"Linear Fit  (R = {slope:.4e} Ω)",
            line=dict(color="#818cf8", width=2.5, dash="solid"),
        ))

    # Ideal (no contact/wire resistance) for Two-Probe comparison
    if show_ideal and method == "Two-Probe" and slope is not None:
        R_parasitic = 2 * R_contact + R_wire
        R_ideal = slope - R_parasitic
        V_ideal = R_ideal * I_range
        fig.add_trace(go.Scatter(
            x=I_range, y=V_ideal,
            mode="lines",
            name=f"Ideal (no contact R)  R = {R_ideal:.4e} Ω",
            line=dict(color="#34d399", width=2, dash="dot"),
        ))

    annotation_text = (
        f"Slope (R) = {slope:.4e} Ω<br>"
        f"R² = {r2:.5f}"
    ) if slope is not None else "Need ≥2 data points"

    fig.add_annotation(
        x=0.03, y=0.97, xref="paper", yref="paper",
        text=annotation_text,
        showarrow=False,
        font=dict(family="IBM Plex Mono", size=12, color="#f1f5f9"),
        bgcolor="rgba(17,24,39,0.85)",
        bordercolor="#2a3347",
        borderwidth=1,
        borderpad=10,
        align="left",
    )

    fig.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#0a0e1a",
        font=dict(family="Inter", color="#94a3b8", size=12),
        title=dict(
            text=f"<b>V – I Characteristic</b>  ·  {method}",
            font=dict(family="Playfair Display", size=18, color="#f1f5f9"),
            x=0.03, y=0.97,
        ),
        xaxis=dict(
            title="Current I  (A)",
            title_font=dict(family="IBM Plex Mono", size=12, color="#94a3b8"),
            gridcolor="#1c2333",
            linecolor="#2a3347",
            tickfont=dict(family="IBM Plex Mono", color="#64748b"),
            showgrid=True, zeroline=True,
            zerolinecolor="#2a3347", zerolinewidth=1,
        ),
        yaxis=dict(
            title="Voltage V  (V)",
            title_font=dict(family="IBM Plex Mono", size=12, color="#94a3b8"),
            gridcolor="#1c2333",
            linecolor="#2a3347",
            tickfont=dict(family="IBM Plex Mono", color="#64748b"),
            showgrid=True, zeroline=True,
            zerolinecolor="#2a3347", zerolinewidth=1,
        ),
        legend=dict(
            bgcolor="rgba(17,24,39,0.9)",
            bordercolor="#2a3347",
            borderwidth=1,
            font=dict(family="IBM Plex Mono", size=11, color="#cbd5e1"),
        ),
        margin=dict(l=60, r=30, t=60, b=60),
        hovermode="closest",
        height=460,
    )
    return fig, slope, r2


# ─────────────────────────────────────────────
#  MATPLOTLIB PROBE DIAGRAMS
# ─────────────────────────────────────────────

def draw_probe_diagram(method="Two-Probe"):
    """Returns a matplotlib figure with the probe setup diagram."""
    fig, ax = plt.subplots(figsize=(9, 3.6))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # ── Sample bar ──
    sample = plt.Rectangle((0.5, 1.8), 9, 1.4, linewidth=1.5,
                             edgecolor="#2a3347", facecolor="#1c2a40",
                             zorder=2)
    ax.add_patch(sample)
    ax.text(5, 0.9, "Sample (Semiconductor / Conductor)", ha="center",
            fontsize=8, color="#64748b", fontfamily="monospace")

    def draw_probe(x, y_top, label, color, is_current=True):
        # Probe body
        ax.plot([x, x], [y_top, 3.2], color=color, lw=2.5, zorder=4)
        # Probe tip (triangle)
        tri = plt.Polygon(
            [[x - 0.1, 3.2], [x + 0.1, 3.2], [x, 3.08]],
            closed=True, facecolor=color, edgecolor=color, zorder=5
        )
        ax.add_patch(tri)
        # Probe head box
        box = plt.Rectangle((x - 0.22, y_top - 0.25), 0.44, 0.5,
                              facecolor="#0c1c30", edgecolor=color,
                              linewidth=1.2, zorder=5)
        ax.add_patch(box)
        ax.text(x, y_top + 0.45, label, ha="center", fontsize=8,
                color=color, fontfamily="monospace", fontweight="bold", zorder=6)

    def draw_current_arrow(x_start, x_end, y=1.3, color="#38bdf8"):
        ax.annotate("", xy=(x_end, y), xytext=(x_start, y),
                    arrowprops=dict(arrowstyle="-|>",
                                    color=color, lw=1.8),
                    zorder=3)

    if method == "Two-Probe":
        # Two probes at x=2 and x=8 – both carry current AND voltage
        draw_probe(2.5, 4.5, "P₁\nI+V", "#38bdf8", is_current=True)
        draw_probe(7.5, 4.5, "P₂\nI+V", "#38bdf8", is_current=True)

        # Current lines (top)
        ax.annotate("", xy=(2.5, 4.5), xytext=(0.5, 4.5),
                    arrowprops=dict(arrowstyle="<|-",
                                    color="#38bdf8", lw=1.5))
        ax.annotate("", xy=(9.5, 4.5), xytext=(7.5, 4.5),
                    arrowprops=dict(arrowstyle="-|>",
                                    color="#38bdf8", lw=1.5))
        ax.text(0.3, 4.65, "I+", fontsize=8, color="#38bdf8", fontfamily="monospace")
        ax.text(9.3, 4.65, "I−", fontsize=8, color="#38bdf8", fontfamily="monospace")

        # Voltage bracket
        ax.annotate("", xy=(7.5, 4.0), xytext=(2.5, 4.0),
                    arrowprops=dict(arrowstyle="<->",
                                    color="#818cf8", lw=1.5, linestyle="dashed"))
        ax.text(5, 4.15, "V  (voltmeter)", ha="center",
                fontsize=8, color="#818cf8", fontfamily="monospace")

        # Equivalent circuit hint
        ax.text(5, 0.3, "⚠  Contact resistance Rc is IN SERIES → included in measurement",
                ha="center", fontsize=7.5, color="#fb923c",
                fontfamily="monospace", style="italic")

        # Current flow arrows inside sample
        for x in [3.5, 5.0, 6.5]:
            draw_current_arrow(x - 0.6, x + 0.6, y=2.5, color="#0ea5e9")

    else:  # Four-Probe
        xs = [1.5, 3.5, 6.5, 8.5]
        colors_p = ["#38bdf8", "#818cf8", "#818cf8", "#38bdf8"]
        labels = ["P₁\nI+", "P₂\nV+", "P₃\nV−", "P₄\nI−"]
        for x, lbl, col in zip(xs, labels, colors_p):
            draw_probe(x, 4.5, lbl, col)

        # Outer current leads
        ax.annotate("", xy=(1.5, 4.5), xytext=(0.3, 4.5),
                    arrowprops=dict(arrowstyle="<|-",
                                    color="#38bdf8", lw=1.5))
        ax.annotate("", xy=(9.5, 4.5), xytext=(8.5, 4.5),
                    arrowprops=dict(arrowstyle="-|>",
                                    color="#38bdf8", lw=1.5))
        ax.text(0.1, 4.65, "I+", fontsize=8, color="#38bdf8", fontfamily="monospace")
        ax.text(9.3, 4.65, "I−", fontsize=8, color="#38bdf8", fontfamily="monospace")

        # Inner voltage sense
        ax.annotate("", xy=(6.5, 4.05), xytext=(3.5, 4.05),
                    arrowprops=dict(arrowstyle="<->",
                                    color="#818cf8", lw=1.5, linestyle="dashed"))
        ax.text(5, 4.18, "V  (high-Z voltmeter — zero current)",
                ha="center", fontsize=8, color="#818cf8", fontfamily="monospace")

        # Current arrows inside sample
        for x in [2.5, 4.0, 5.0, 6.0, 7.5]:
            draw_current_arrow(x - 0.5, x + 0.5, y=2.5, color="#0ea5e9")

        ax.text(5, 0.3, "✓  Contact resistance at P₂ & P₃ eliminated — no current through voltmeter",
                ha="center", fontsize=7.5, color="#34d399",
                fontfamily="monospace", style="italic")

    # Spacing markers
    if method == "Four-Probe":
        for x1, x2 in [(1.5, 3.5), (3.5, 6.5), (6.5, 8.5)]:
            ax.annotate("", xy=(x2, 1.65), xytext=(x1, 1.65),
                        arrowprops=dict(arrowstyle="<->",
                                        color="#374151", lw=1.0))
        ax.text(5, 1.45, "← s →", ha="center",
                fontsize=7.5, color="#4b5563", fontfamily="monospace")

    ax.set_title(f"{method} Configuration",
                 color="#94a3b8", fontsize=11,
                 fontfamily="monospace", pad=6)

    plt.tight_layout(pad=0.5)
    return fig


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px 0;'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.65rem;
                    letter-spacing:3px;text-transform:uppercase;color:#475569;
                    margin-bottom:6px;'>Instrument Panel</div>
        <div style='font-size:1.15rem;font-weight:700;color:#38bdf8;'>
            ⚡ ResistivityLab
        </div>
    </div>
    <hr style='border:none;border-top:1px solid #1e293b;margin:8px 0 20px 0;'/>
    """, unsafe_allow_html=True)

    method = st.selectbox(
        "Measurement Method",
        ["Two-Probe", "Four-Probe"],
        help="Two-probe includes contact resistance; four-probe eliminates it."
    )

    st.markdown("<div class='section-header'>Electrical Inputs</div>",
                unsafe_allow_html=True)
    I_single = st.number_input("Current I (A)", value=1e-3,
                                format="%.6e", step=1e-4)
    V_single = st.number_input("Voltage V (V)", value=5e-3,
                                format="%.6e", step=1e-4)

    st.markdown("<div class='section-header'>Sample Geometry</div>",
                unsafe_allow_html=True)
    L = st.number_input("Length L (m)", value=0.01, format="%.5f")
    A = st.number_input("Cross-section A (m²)", value=1e-6, format="%.2e")
    t = st.number_input("Thickness t (m) — thin film", value=1e-4, format="%.2e")
    s = st.number_input("Probe Spacing s (m)", value=2e-3, format="%.4e")

    if method == "Four-Probe":
        fp_mode = st.radio("Sample Type", ["Bulk", "Thin Film"],
                            horizontal=True)
    else:
        fp_mode = "Bulk"

    st.markdown("<div class='section-header'>Parasitic Resistances</div>",
                unsafe_allow_html=True)
    R_contact = st.number_input("Contact Resistance Rc (Ω)", value=5.0,
                                  format="%.3f")
    R_wire = st.number_input("Wire Resistance Rw (Ω)", value=1.0,
                               format="%.3f")

    show_ideal = st.toggle("Show Ideal vs Real Curve", value=True)

    st.markdown("<hr style='border:none;border-top:1px solid #1e293b;margin:18px 0 10px 0;'/>",
                unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:"IBM Plex Mono",monospace;font-size:0.65rem;
                color:#334155;text-align:center;line-height:1.6;'>
        ResistivityLab v2.0<br>
        © 2024 Physics Instruments
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────

col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown(f"""
    <div style='padding: 8px 0 4px 0;'>
        <p class='lab-subtitle'>Electrical Characterization Laboratory</p>
        <p class='lab-title'>Resistivity Measurement</p>
        <p style='font-family:"IBM Plex Mono",monospace;font-size:0.85rem;
                   color:#475569;margin-top:6px;'>
            Two-Probe &amp; Four-Probe Methods · Interactive Simulation
        </p>
    </div>
    """, unsafe_allow_html=True)
with col_badge:
    badge_color = "badge-blue" if method == "Two-Probe" else "badge-green"
    st.markdown(f"""
    <div style='padding-top:28px;text-align:right;'>
        <span class='badge {badge_color}'>{method}</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid #1a2234;margin:8px 0 20px 0;'/>",
            unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  COMPUTE SINGLE-POINT
# ─────────────────────────────────────────────

if method == "Two-Probe":
    R_meas, R_samp, rho_val = compute_resistivity_two_probe(
        V_single, I_single, L, A, R_contact, R_wire
    )
    R_display   = R_samp
    rho_display = rho_val
else:
    mode_str = "thin_film" if fp_mode == "Thin Film" else "bulk"
    R_sheet, rho_val = compute_resistivity_four_probe(
        V_single, I_single, s, t if fp_mode == "Thin Film" else None, mode_str
    )
    R_meas     = V_single / I_single if I_single != 0 else None
    R_display  = R_sheet
    rho_display = rho_val


# ─────────────────────────────────────────────
#  TOP METRICS ROW
# ─────────────────────────────────────────────

mcol1, mcol2, mcol3, mcol4 = st.columns(4)

def metric_card(col, label, value, unit, cls=""):
    val_str = f"{value:.4e}" if value is not None else "—"
    col.markdown(f"""
    <div class='metric-card {cls}'>
        <div class='metric-label'>{label}</div>
        <div class='metric-value'>{val_str}
            <span class='metric-unit'>{unit}</span>
        </div>
    </div>""", unsafe_allow_html=True)

metric_card(mcol1, "Measured R",  R_meas,     "Ω",    "")
metric_card(mcol2, "Sample R",    R_display,  "Ω",    "purple")
metric_card(mcol3, "Resistivity ρ", rho_display, "Ω·m", "green")
if method == "Two-Probe":
    metric_card(mcol4, "Parasitic R", 2 * R_contact + R_wire, "Ω", "orange")
else:
    metric_card(mcol4, "Probe Spacing", s, "m", "orange")


# ─────────────────────────────────────────────
#  MAIN TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📊  V–I Graph & Dataset",
    "🔬  Probe Diagram",
    "📐  Formulas",
    "ℹ️   Theory",
])


# ══════════════════════════
#  TAB 1 – Graph & Dataset
# ══════════════════════════
with tab1:
    st.markdown("<div class='section-header'>Dataset — V / I Readings</div>",
                unsafe_allow_html=True)

    # Session state for dataset
    if "readings" not in st.session_state:
        default_I = [0.5e-3, 1.0e-3, 1.5e-3, 2.0e-3, 2.5e-3, 3.0e-3]
        default_V = [i * (V_single / I_single if I_single else 1) *
                     (1 + np.random.uniform(-0.02, 0.02))
                     for i in default_I]
        st.session_state.readings = pd.DataFrame({
            "Current (A)": default_I,
            "Voltage (V)": [round(v, 7) for v in default_V],
        })

    ga, gb = st.columns([2, 1])
    with ga:
        edited_df = st.data_editor(
            st.session_state.readings,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Current (A)": st.column_config.NumberColumn(format="%.4e"),
                "Voltage (V)": st.column_config.NumberColumn(format="%.4e"),
            },
            key="data_editor",
        )
        st.session_state.readings = edited_df

    with gb:
        st.markdown("""
        <div style='background:#111827;border:1px solid #1e293b;border-radius:8px;
                    padding:14px 16px;font-family:"IBM Plex Mono",monospace;
                    font-size:0.78rem;color:#64748b;line-height:1.8;'>
            <b style='color:#94a3b8;'>Tips</b><br>
            • Add rows with the ＋ button<br>
            • Edit cells inline<br>
            • Minimum 2 rows for fit<br>
            • Data auto-updates graph
        </div>
        """, unsafe_allow_html=True)

    df_clean = edited_df.dropna()
    if len(df_clean) >= 2:
        fig_plot, slope_fit, r2_fit = plot_interactive_graph(
            df_clean, method,
            show_ideal=show_ideal,
            R_contact=R_contact,
            R_wire=R_wire,
        )
        st.plotly_chart(fig_plot, use_container_width=True)

        # Derived resistivity from graph slope
        if slope_fit is not None:
            st.markdown("<div class='section-header'>Graph-Derived Results</div>",
                        unsafe_allow_html=True)
            gc1, gc2, gc3 = st.columns(3)
            with gc1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-label'>Slope (R from graph)</div>
                    <div class='metric-value'>{slope_fit:.4e}
                        <span class='metric-unit'>Ω</span>
                    </div>
                </div>""", unsafe_allow_html=True)
            with gc2:
                st.markdown(f"""
                <div class='metric-card green'>
                    <div class='metric-label'>R² Goodness of Fit</div>
                    <div class='metric-value'>{r2_fit:.5f}</div>
                </div>""", unsafe_allow_html=True)
            with gc3:
                if method == "Two-Probe":
                    R_s_graph = slope_fit - (2 * R_contact + R_wire)
                    rho_graph = R_s_graph * (A / L) if L and A else None
                else:
                    if fp_mode == "Thin Film" and t:
                        rho_graph = (np.pi / np.log(2)) * t * slope_fit
                    else:
                        rho_graph = 2 * np.pi * s * slope_fit
                st.markdown(f"""
                <div class='metric-card purple'>
                    <div class='metric-label'>ρ (from graph fit)</div>
                    <div class='metric-value'>{rho_graph:.4e if rho_graph else '—'}
                        <span class='metric-unit'>Ω·m</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("Add at least 2 data rows to generate the V–I graph.")


# ══════════════════════════
#  TAB 2 – Probe Diagram
# ══════════════════════════
with tab2:
    st.markdown("<div class='section-header'>Probe Configuration Diagram</div>",
                unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    for col_d, meth in zip([d1, d2], ["Two-Probe", "Four-Probe"]):
        with col_d:
            fig_diag = draw_probe_diagram(meth)
            b64 = fig_to_base64(fig_diag)
            active = "border: 1px solid #38bdf8;" if meth == method else "border: 1px solid #1e293b;"
            st.markdown(f"""
            <div style='{active} border-radius:10px; overflow:hidden; margin-bottom:8px;'>
                <img src='data:image/png;base64,{b64}'
                     style='width:100%;display:block;'/>
            </div>""", unsafe_allow_html=True)
            plt.close(fig_diag)

            tag = "badge-blue" if meth == "Two-Probe" else "badge-green"
            st.markdown(f"<div style='text-align:center;margin-top:4px;'>"
                        f"<span class='badge {tag}'>"
                        f"{'Active ✓' if meth == method else 'Inactive'}</span></div>",
                        unsafe_allow_html=True)

    st.markdown("""
    <div style='display:flex;gap:24px;margin-top:16px;flex-wrap:wrap;'>
        <div style='display:flex;align-items:center;gap:8px;font-family:"IBM Plex Mono",monospace;font-size:0.78rem;color:#64748b;'>
            <div style='width:28px;height:3px;background:#38bdf8;'></div> Current path
        </div>
        <div style='display:flex;align-items:center;gap:8px;font-family:"IBM Plex Mono",monospace;font-size:0.78rem;color:#64748b;'>
            <div style='width:28px;height:3px;background:#818cf8;border-top:2px dashed #818cf8;'></div> Voltage sense
        </div>
        <div style='display:flex;align-items:center;gap:8px;font-family:"IBM Plex Mono",monospace;font-size:0.78rem;color:#64748b;'>
            <div style='width:28px;height:3px;background:#0ea5e9;'></div> Internal current flow
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════
#  TAB 3 – Formulas (LaTeX)
# ══════════════════════════
with tab3:
    st.markdown("<div class='section-header'>Mathematical Framework</div>",
                unsafe_allow_html=True)

    if method == "Two-Probe":
        st.markdown("#### Two-Probe Method")
        st.latex(r"R_{\text{measured}} = \frac{V}{I}")
        st.latex(r"R_{\text{sample}} = R_{\text{measured}} - \left(2R_c + R_w\right)")
        st.latex(r"\rho = R_{\text{sample}} \cdot \frac{A}{L}")
        st.markdown("""
        <div class='formula-box'>
        Where:<br>
        &nbsp;&nbsp; Rc  = contact resistance per probe (Ω)<br>
        &nbsp;&nbsp; Rw  = total wire resistance (Ω)<br>
        &nbsp;&nbsp; A   = cross-sectional area (m²)<br>
        &nbsp;&nbsp; L   = sample length (m)
        </div>""", unsafe_allow_html=True)

        if R_display is not None and rho_display is not None:
            st.markdown("#### Numerical Substitution")
            st.latex(
                rf"R_{{\text{{sample}}}} = {R_meas:.4e} - ({2*R_contact:.3f} + {R_wire:.3f})"
                rf" = {R_display:.4e} \, \Omega"
            )
            st.latex(
                rf"\rho = {R_display:.4e} \times \frac{{{A:.2e}}}{{{L:.5f}}}"
                rf" = {rho_display:.4e} \, \Omega \cdot \text{{m}}"
            )

    else:
        st.markdown("#### Four-Probe Method")
        st.markdown("**Bulk sample (semi-infinite medium):**")
        st.latex(r"\rho = 2\pi s \cdot \frac{V}{I}")
        st.markdown("**Thin film (van der Pauw / collinear):**")
        st.latex(r"\rho = \frac{\pi}{\ln 2} \cdot t \cdot \frac{V}{I}")
        st.markdown("""
        <div class='formula-box'>
        Where:<br>
        &nbsp;&nbsp; s   = equal probe spacing (m)<br>
        &nbsp;&nbsp; t   = film thickness (m)<br>
        &nbsp;&nbsp; V/I = measured resistance (sheet resistance for thin film)
        </div>""", unsafe_allow_html=True)

        if rho_display is not None:
            st.markdown("#### Numerical Substitution")
            if fp_mode == "Thin Film":
                st.latex(
                    rf"\rho = \frac{{\pi}}{{\ln 2}} \cdot {t:.2e} \cdot "
                    rf"\frac{{{V_single:.4e}}}{{{I_single:.4e}}}"
                    rf" = {rho_display:.4e} \, \Omega \cdot \text{{m}}"
                )
            else:
                st.latex(
                    rf"\rho = 2\pi \cdot {s:.4e} \cdot "
                    rf"\frac{{{V_single:.4e}}}{{{I_single:.4e}}}"
                    rf" = {rho_display:.4e} \, \Omega \cdot \text{{m}}"
                )

    # Error analysis
    st.markdown("<div class='section-header'>Error Analysis</div>",
                unsafe_allow_html=True)
    st.latex(r"\frac{\Delta\rho}{\rho} = \sqrt{\left(\frac{\Delta V}{V}\right)^2 + \left(\frac{\Delta I}{I}\right)^2 + \left(\frac{\Delta L}{L}\right)^2 + \left(\frac{\Delta A}{A}\right)^2}")


# ══════════════════════════
#  TAB 4 – Theory
# ══════════════════════════
with tab4:
    st.markdown("<div class='section-header'>Why Four-Probe is More Accurate</div>",
                unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
        <h4>⚡ Fundamental Principle</h4>
        <p>
        In a <b>two-probe</b> setup, the same pair of electrodes injects current <em>and</em>
        senses voltage. Any resistance at the metal–semiconductor contact or in the lead wires
        is therefore in series with the sample and <em>adds directly to the measured value</em>.
        Contact resistances can range from a few ohms to several kilohms depending on surface
        condition, making the two-probe result unreliable for low-resistance samples.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box' style='border-left-color:#34d399;'>
        <h4 style='color:#34d399;'>✓ Four-Probe Advantage</h4>
        <p>
        The <b>four-probe</b> method uses <em>separate</em> current-injecting (outer) and
        voltage-sensing (inner) electrodes. Because the voltmeter has very high input impedance,
        negligible current flows through the inner probes — so the voltage drop across their
        contact resistances is essentially zero. The measured voltage reflects <em>only</em>
        the potential difference across the bulk of the sample, giving a true resistivity
        value independent of contact quality.
        </p>
    </div>
    """, unsafe_allow_html=True)

    ta, tb = st.columns(2)
    with ta:
        st.markdown("""
        <div style='background:#0f1a2e;border:1px solid #1e3a5f;border-radius:8px;padding:16px 18px;'>
            <div style='font-family:"IBM Plex Mono",monospace;font-size:0.72rem;
                        letter-spacing:2px;text-transform:uppercase;color:#38bdf8;
                        margin-bottom:10px;'>Two-Probe Limitations</div>
            <ul style='color:#94a3b8;font-size:0.88rem;line-height:1.9;margin:0;padding-left:16px;'>
                <li>Contact resistance included in reading</li>
                <li>Wire resistance adds systematic error</li>
                <li>Error ≫ signal for low-R samples</li>
                <li>Requires correction if contacts known</li>
                <li>Suitable for high-resistance samples only</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with tb:
        st.markdown("""
        <div style='background:#0a2218;border:1px solid #14532d;border-radius:8px;padding:16px 18px;'>
            <div style='font-family:"IBM Plex Mono",monospace;font-size:0.72rem;
                        letter-spacing:2px;text-transform:uppercase;color:#34d399;
                        margin-bottom:10px;'>Four-Probe Advantages</div>
            <ul style='color:#94a3b8;font-size:0.88rem;line-height:1.9;margin:0;padding-left:16px;'>
                <li>Contact resistance auto-cancelled</li>
                <li>High-Z voltmeter → negligible probe current</li>
                <li>Industry standard for semiconductors</li>
                <li>Valid for metals, thin films, wafers</li>
                <li>ASTM F84 / IEEE 1160 compliant</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Common Material Reference Values</div>",
                unsafe_allow_html=True)

    ref_data = {
        "Material": ["Silver", "Copper", "Aluminium", "Silicon (intrinsic)",
                     "Germanium", "GaAs", "ITO (thin film)", "Carbon (graphite)"],
        "ρ (Ω·m)": ["1.59 × 10⁻⁸", "1.72 × 10⁻⁸", "2.82 × 10⁻⁸",
                     "6.40 × 10²", "4.60 × 10⁻¹", "~1 × 10⁻⁶",
                     "~10⁻⁴", "~3 × 10⁻⁵"],
        "Class": ["Metal", "Metal", "Metal", "Semiconductor",
                  "Semiconductor", "Semiconductor", "TCO", "Semimetal"],
        "Typical Method": ["4-probe", "4-probe", "4-probe", "4-probe",
                            "4-probe", "Hall / 4-probe", "4-probe", "2-probe"],
    }
    st.dataframe(
        pd.DataFrame(ref_data),
        use_container_width=True,
        hide_index=True,
    )


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────

st.markdown("""
<div style='margin-top:40px;padding:20px;border-top:1px solid #1a2234;
            text-align:center;font-family:"IBM Plex Mono",monospace;
            font-size:0.68rem;color:#334155;letter-spacing:1px;'>
    ResistivityLab · Two-Probe &amp; Four-Probe Methods ·
    Built with Streamlit + Plotly · Physics Instruments Division
</div>
""", unsafe_allow_html=True)