
import streamlit as st
import plotly.graph_objects as go
import networkx as nx

from .summaries import subgraph_for_endpoints

def _sheet_of(addr: str) -> str:
    return addr.split('!')[0] if '!' in addr else ''

def _build_network_fig(sub_edges):
    if not sub_edges:
        return None
    G = nx.DiGraph()
    G.add_edges_from(sub_edges)

    # Stable node ordering
    nodes = list(G.nodes())

    # Layout
    pos = nx.spring_layout(G, k=0.6, seed=42)

    # Node positions and labels
    x_nodes = [pos[n][0] for n in nodes]
    y_nodes = [pos[n][1] for n in nodes]
    labels = [(n.split('!')[1] if '!' in n else n) for n in nodes]
    hover = [n for n in nodes]

    # Color nodes by sheet
    sheets = [_sheet_of(n) for n in nodes]
    sheet_to_idx = {s:i for i,s in enumerate(sorted(set(sheets)))}
    colors = [sheet_to_idx[s] for s in sheets]  # numeric category; Plotly will color by colorscale

    node_trace = go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        text=labels,
        textposition="top center",
        hovertext=hover,
        hoverinfo="text",
        marker=dict(
            size=14,
            color=colors,
            colorscale="Blues",
            line=dict(width=1)
        )
    )

    # Edge segments
    x_edges = []
    y_edges = []
    for a,b in G.edges():
        x_edges += [pos[a][0], pos[b][0], None]
        y_edges += [pos[a][1], pos[b][1], None]

    edge_trace = go.Scatter(
        x=x_edges, y=y_edges, mode='lines', hoverinfo='none', line=dict(width=1)
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=560
    )
    return fig

def render_kpi_tracer(traces: dict, edges):
    st.write("Pick endpoints (cells) to display side-by-side traces and a lineage graph.")
    choices = sorted(list(traces.keys()))
    selected = st.multiselect("Choose output cells:", choices[:50], max_selections=10)
    if not selected:
        st.info("Select one or more cells above.")
        return

    # Graph section
    st.subheader("Dependency Graph")
    sub_edges = subgraph_for_endpoints(edges, selected, max_nodes=800)
    if sub_edges:
        fig = _build_network_fig(sub_edges)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No edges found for the selected endpoints.")

    # Text traces side-by-side
    st.subheader("Text Traces")
    cols = st.columns(min(3, len(selected)))
    for i, addr in enumerate(selected):
        with cols[i % len(cols)]:
            st.markdown(f"**{addr}**")
            st.code("\n".join(traces[addr]), language="text")
