
import pandas as pd

def build_overview_stats(wb, traces, hop_hist, edges, risky_map, circular_cells):
    total_sheets = len(wb.sheetnames)
    total_formulas = len(traces)
    max_depth = max(hop_hist.keys()) if hop_hist else 0
    risky_count = sum(len(v) for v in risky_map.values())
    stats = {
        "Sheets": total_sheets,
        "Formula cells": total_formulas,
        "Max hop depth": max_depth,
        "Circular cells": len(circular_cells),
        "Risky funcs flagged": risky_count,
        "Edges": len(edges)
    }
    return stats

def build_hop_hist_df(hop_hist):
    if not hop_hist:
        return pd.DataFrame(columns=["Max Depth","# Cells"])
    rows = sorted([(k,v) for k,v in hop_hist.items()], key=lambda x: x[0])
    return pd.DataFrame(rows, columns=["Max Depth","# Cells"])

def cross_sheet_matrix(edges):
    def sheet_of(addr): return addr.split('!')[0]
    if not edges:
        return pd.DataFrame()
    pairs = [(sheet_of(a), sheet_of(b)) for a,b in edges]
    df = pd.DataFrame(pairs, columns=["From","To"])
    pivot = df.pivot_table(index="From", columns="To", aggfunc=len, fill_value=0)
    return pivot

def top_deep_cells(traces, hop_hist):
    rows = [(cell, len(lines)) for cell, lines in traces.items()]
    df = pd.DataFrame(rows, columns=["Cell","Trace Lines"])
    return df.sort_values(by="Trace Lines", ascending=False).head(20)


def subgraph_for_endpoints(edges, endpoints, max_nodes=800):
    """Return edges limited to those reachable from selected endpoints (reverse DFS).
    edges: list of (from_cell, to_cell) pairs where from_cell depends on to_cell.
    We want all ancestors (precedents) of the endpoints.
    """
    if not edges or not endpoints:
        return []
    # Build reverse adjacency: for a given node X, who does X depend on? (parents)
    parents = {}
    for a,b in edges:
        parents.setdefault(a, set()).add(b)
    # DFS from each endpoint over parents
    keep_nodes = set()
    stack = list(endpoints)
    while stack and len(keep_nodes) < max_nodes:
        node = stack.pop()
        if node in keep_nodes:
            continue
        keep_nodes.add(node)
        for p in parents.get(node, []):
            if p not in keep_nodes:
                stack.append(p)
    # Filter edges to only those between kept nodes
    sub = [(a,b) for a,b in edges if a in keep_nodes and b in keep_nodes]
    return sub
