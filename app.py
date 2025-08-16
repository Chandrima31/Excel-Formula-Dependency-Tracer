
import streamlit as st
import pandas as pd

from modules.loader import load_workbook_cached, bytes_to_tempfile
from modules.tracer import trace_workbook
from modules.summaries import build_overview_stats, build_hop_hist_df, cross_sheet_matrix, top_deep_cells
from modules.views_overview import render_overview
from modules.views_inspector import render_cell_inspector
from modules.views_matrix import render_matrix_view
from modules.views_risks import render_risks_view
from modules.views_kpi import render_kpi_tracer

st.set_page_config(page_title="Excel Formula Dependency Tracer", page_icon="🔎", layout="wide")
st.title("🔍🔗 Excel Formula Dependency Tracer")
st.caption("Professional-grade formula lineage, hop-depth analytics, and cross-sheet mapping for Excel models.")
st.markdown("---")

uploaded = st.file_uploader("Upload Excel workbook (.xlsx)", type=["xlsx"])

if not uploaded:
    st.info("Please upload an Excel file to begin.")
    st.stop()

tmp_path = bytes_to_tempfile(uploaded)

with st.spinner("Loading workbook..."):
    wb = load_workbook_cached(tmp_path)

with st.spinner("Tracing formulae & building graph..."):
    traces, hop_hist, edges, risky_map, circular_cells = trace_workbook(wb)

overview_stats = build_overview_stats(wb, traces, hop_hist, edges, risky_map, circular_cells)
hop_hist_df = build_hop_hist_df(hop_hist)
matrix = cross_sheet_matrix(edges)
deep_df = top_deep_cells(traces, hop_hist)

# Sidebar summary & help
with st.sidebar:
    st.header('Quick Summary')
    st.write(f"**Sheets**: {overview_stats['Sheets']}  |  **Formulas**: {overview_stats['Formula cells']}")
    st.write(f"**Max Depth**: {overview_stats['Max hop depth']}  |  **Circular**: {overview_stats['Circular cells']}")
    st.write(f"**Risky Funcs**: {overview_stats['Risky funcs flagged']}")
    st.markdown('---')
    st.subheader('How it works')
    st.caption('This app parses formulae, expands ranges, and builds dependency graphs across sheets. '
               'Hop depth indicates the longest chain from a formula to its precedents.')

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Cell Inspector", "Cross-Sheet Matrix", "Circular & Risky", "KPI Tracer"]
)

with tab1:
    render_overview(overview_stats, hop_hist_df, deep_df)

with tab2:
    render_cell_inspector(traces)

with tab3:
    render_matrix_view(matrix)

with tab4:
    render_risks_view(circular_cells, risky_map, traces)

with tab5:
    render_kpi_tracer(traces, edges)
