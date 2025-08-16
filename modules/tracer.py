
from collections import defaultdict
from modules.refs import extract_refs, expand_range

def trace_cell(wb, sheet_name, cell_ref, path=None, depth=0, max_depth=500, memo=None):
    if path is None:
        path = []
    if memo is None:
        memo = {}
    node = (sheet_name, cell_ref)
    if node in path:
        return {'lines':[f"{'  '*depth}{sheet_name}!{cell_ref} = [CIRCULAR]"], 'max_depth': depth, 'edges': []}
    if node in memo:
        return memo[node]
    if depth > max_depth:
        return {'lines':[f"{'  '*depth}{sheet_name}!{cell_ref} = [TOO DEEP]"], 'max_depth': depth, 'edges': []}

    sheet = wb[sheet_name]
    cell = sheet[cell_ref]
    if cell.data_type != 'f' or not cell.value:
        res = {'lines':[f"{'  '*depth}{sheet_name}!{cell_ref} = {cell.value}"], 'max_depth': depth, 'edges': []}
        memo[node] = res
        return res

    formula = cell.value
    lines = [f"{'  '*depth}{sheet_name}!{cell_ref} = {formula}"]
    edges = []
    max_d = depth
    for ref_sheet, raw_ref in extract_refs(formula):
        tgt_sheet = ref_sheet or sheet_name
        if tgt_sheet not in wb.sheetnames:
            continue
        for tgt_cell in expand_range(raw_ref):
            sub = trace_cell(wb, tgt_sheet, tgt_cell, path + [node], depth+1, max_depth, memo)
            lines.extend(sub['lines'])
            edges.append((f"{sheet_name}!{cell_ref}", f"{tgt_sheet}!{tgt_cell}"))
            max_d = max(max_d, sub['max_depth'])
    res = {'lines':lines, 'max_depth': max_d, 'edges': edges}
    memo[node] = res
    return res

def trace_workbook(wb):
    traces = {}
    hop_hist = defaultdict(int)
    edges = []
    risky = defaultdict(list)
    circular_cells = set()

    for sname in wb.sheetnames:
        sheet = wb[sname]
        for row in sheet.iter_rows():
            for c in row:
                if c.data_type == 'f':
                    t = trace_cell(wb, sname, c.coordinate)
                    traces[f"{sname}!{c.coordinate}"] = t['lines']
                    hop_hist[t['max_depth']] += 1
                    edges.extend(t['edges'])
                    f = (c.value or "").upper()
                    for kw in ("INDIRECT", "OFFSET", "NOW", "RAND", "RANDBETWEEN", "CELL"):
                        if kw in f:
                            risky[kw].append(f"{sname}!{c.coordinate}")
                    if any("CIRCULAR" in line for line in t['lines']):
                        circular_cells.add(f"{sname}!{c.coordinate}")

    return traces, hop_hist, edges, dict(risky), sorted(circular_cells)
