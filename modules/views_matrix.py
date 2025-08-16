
import streamlit as st
import pandas as pd
import plotly.express as px

def render_matrix_view(matrix_df: pd.DataFrame):
    st.write("Cross-sheet dependency counts (From ➜ To).")
    if matrix_df is None or matrix_df.empty:
        st.info("No cross-sheet edges found.")
        return
    idx = sorted(set(matrix_df.index).union(set(matrix_df.columns)))
    matrix_df = matrix_df.reindex(index=idx, columns=idx, fill_value=0)
    fig = px.imshow(
        matrix_df,
        text_auto=True,
        aspect="auto",
        height=520,
        labels=dict(color="Refs"),
    )
    fig.update_layout(margin=dict(l=10,r=10,t=30,b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Tip: Heavier rows/cols indicate sheets that either reference many others (producers) or are referenced by many (consumers).")
