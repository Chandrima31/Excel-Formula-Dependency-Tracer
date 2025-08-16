
import re
import openpyxl.utils as xlutils

A1_REF = r"\$?[A-Z]{1,3}\$?\d+"
RANGE = rf"{A1_REF}:(?:{A1_REF})"
SHEET = r"(?:'[^']+'|[A-Za-z0-9_\. ]+)"
CELL_OR_RANGE = rf"(?:({SHEET})!)?({RANGE}|{A1_REF})"

def normalize_formula(formula: str) -> str:
    if not formula:
        return ""
    return formula.lstrip('=')

def extract_refs(formula: str):
    f = normalize_formula(formula)
    refs = []
    for m in re.finditer(CELL_OR_RANGE, f):
        sheet, ref = m.groups()
        if sheet:
            sheet = sheet.strip("'")
        refs.append((sheet, ref))
    return refs

def expand_range(a1range: str):
    if ':' not in a1range:
        return [a1range]
    min_col, min_row, max_col, max_row = xlutils.range_boundaries(a1range)
    out = []
    for col in range(min_col, max_col+1):
        for row in range(min_row, max_row+1):
            out.append(f"{xlutils.get_column_letter(col)}{row}")
    return out
