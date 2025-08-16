
import streamlit as st

def render_risks_view(circular_cells, risky_map, traces):
    st.subheader("Circular References")
    if circular_cells:
        for addr in circular_cells:
            with st.expander(addr):
                st.code("\n".join(traces.get(addr, [])), language="text")
    else:
        st.success("No circular references detected.")

    st.subheader("Risky Patterns")
    if not risky_map:
        st.success("No risky formulas flagged.")
        return
    for kw, cells in risky_map.items():
        with st.expander(f"{kw} ({len(cells)})"):
            for addr in cells:
                st.write(addr)
