
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

CARD_STYLE = """
<style>
.kpi-card {background: #0f172a; color: #e2e8f0; border-radius: 16px; padding: 14px 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);}
.kpi-label {font-size: 12px; color: #93c5fd; text-transform: uppercase; letter-spacing: .08em;}
.kpi-value {font-size: 22px; font-weight: 700; margin-top: 2px;}
</style>
"""

def kpi_card(label, value):
    return f"""
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
</div>
"""

def render_overview(stats: dict, hop_hist_df: pd.DataFrame, deep_df: pd.DataFrame):
    st.markdown(CARD_STYLE, unsafe_allow_html=True)
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi_card("Sheets", stats.get("Sheets",0)), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Formula cells", stats.get("Formula cells",0)), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Max hop depth", stats.get("Max hop depth",0)), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Circular cells", stats.get("Circular cells",0)), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("Risky funcs", stats.get("Risky funcs flagged",0)), unsafe_allow_html=True)
    with c6: st.markdown(kpi_card("Edges", stats.get("Edges",0)), unsafe_allow_html=True)

    st.subheader("Hop Depth Distribution")
    if not hop_hist_df.empty:
        fig = px.bar(hop_hist_df, x="Max Depth", y="# Cells", height=360)
        fig.update_layout(margin=dict(l=10,r=10,t=30,b=10))
        fig.update_traces(hovertemplate="Depth %{x}<br>Cells %{y}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hop data available.")

    st.subheader("Deepest Traces (Top 20 by length)")
    st.caption("Longer trace = more precedents to evaluate. These are prime candidates for review.")
    st.dataframe(deep_df, use_container_width=True, hide_index=True)
