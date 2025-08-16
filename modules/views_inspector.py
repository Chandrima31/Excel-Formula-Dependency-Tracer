
import streamlit as st

def render_cell_inspector(traces: dict):
    st.write("Search or browse individual cell traces.")
    q = st.text_input("Filter (sheet or cell, e.g., P&L!B8, or substring in address):", "")
    matched = {k:v for k,v in traces.items() if q.lower() in k.lower()} if q else traces
    st.caption(f"Showing {len(matched)} cells")
    for addr, lines in matched.items():
        with st.expander(addr, expanded=False):
            st.code("\n".join(lines), language="text")
