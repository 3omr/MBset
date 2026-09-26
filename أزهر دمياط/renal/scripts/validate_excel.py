import openpyxl, re, sys

REQUIRED_COLUMNS = [
    'id', 'Cas', 'Text', 'Image', 'explanationImage',
    'A', 'B', 'C', 'D', 'E', 'F',
    'A_EXP', 'B_EXP', 'C_EXP', 'D_EXP', 'E_EXP', 'F_EXP',
    'Correct', 'Hint', 'EXP', 'Note', 'Type',
    'categoryId', 'categoryName', 'subcategoryId', 'subcategoryName',
    'tagSuggere', 'Year', 'Tag', 'ImageMasks', 'ExplanationImageMasks'
]

def validate(xlsx_path):
    print(f"--- Running Automated Validation on {xlsx_path} ---")
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    
    rows = list(ws.iter_rows(values_only=True))
    header = list(rows[0])
    
    errors = []
    
    # 1. Column Count & Names
    if len(header) != 31:
        errors.append(f"Column count mismatch: Expected 31, got {len(header)}")
    if header != REQUIRED_COLUMNS:
        errors.append(f"Header schema mismatch!\nExpected: {REQUIRED_COLUMNS}\nGot:      {header}")
        
    # Indices
    id_idx = header.index('id')
    text_idx = header.index('Text')
    a_idx = header.index('A')
    b_idx = header.index('B')
    c_idx = header.index('C')
    d_idx = header.index('D')
    e_idx = header.index('E')
    f_idx = header.index('F')
    corr_idx = header.index('Correct')
    exp_idx = header.index('EXP')
    type_idx = header.index('Type')
    subcat_id_idx = header.index('subcategoryId')
    subcat_name_idx = header.index('subcategoryName')
    cat_id_idx = header.index('categoryId')
    cat_name_idx = header.index('categoryName')
    tag_idx = header.index('Tag')
    year_idx = header.index('Year')
    
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    
    qcs_count = 0
    qroc_count = 0
    
    for row_num, r in enumerate(rows[1:], start=2):
        # Check id must be None
        if r[id_idx] is not None:
            errors.append(f"Row {row_num}: 'id' must be None, got '{r[id_idx]}'")
            
        # Check subcategoryId & subcategoryName must be None
        if r[subcat_id_idx] is not None:
            errors.append(f"Row {row_num}: 'subcategoryId' must be None, got '{r[subcat_id_idx]}'")
        if r[subcat_name_idx] is not None:
            errors.append(f"Row {row_num}: 'subcategoryName' must be None, got '{r[subcat_name_idx]}'")
            
        # Check categoryId & categoryName
        if r[cat_id_idx] != 'DamiettaFa_RENAL':
            errors.append(f"Row {row_num}: categoryId must be 'DamiettaFa_RENAL', got '{r[cat_id_idx]}'")
        if r[cat_name_idx] != 'Renal':
            errors.append(f"Row {row_num}: categoryName must be 'Renal', got '{r[cat_name_idx]}'")
            
        # Check Text stem
        stem = str(r[text_idx] or '')
        if len(stem.strip()) < 5:
            errors.append(f"Row {row_num}: 'Text' too short or empty: '{stem}'")
        if arabic_pattern.search(stem):
            errors.append(f"Row {row_num}: 'Text' contains Arabic characters!")
            
        # Check Type & Correct
        qtype = r[type_idx]
        corr = str(r[corr_idx] or '')
        
        # Check Arabic in all text cells
        for c_i, cell_val in enumerate(r):
            if cell_val is not None and isinstance(cell_val, str):
                if arabic_pattern.search(cell_val):
                    errors.append(f"Row {row_num}, Col {header[c_i]}: Contains Arabic: '{cell_val[:50]}'")
                if '\u200b' in cell_val or '\ufeff' in cell_val:
                    errors.append(f"Row {row_num}, Col {header[c_i]}: Contains invisible unicode!")
                    
        if qtype == 'QCS':
            qcs_count += 1
            if corr not in ['A', 'B', 'C', 'D', 'E', 'F']:
                errors.append(f"Row {row_num}: QCS Correct must be A-F, got '{corr}'")
            # Check options A and B must be non-empty
            if not r[a_idx] or not r[b_idx]:
                errors.append(f"Row {row_num}: QCS options A and B must not be empty!")
            # Check that Correct letter points to an existing option
            opt_map = {'A': r[a_idx], 'B': r[b_idx], 'C': r[c_idx], 'D': r[d_idx], 'E': r[e_idx], 'F': r[f_idx]}
            if not opt_map.get(corr):
                errors.append(f"Row {row_num}: Option mismatch! Correct is '{corr}', but option {corr} is empty!")
        elif qtype == 'QROC':
            qroc_count += 1
            if corr != '-':
                errors.append(f"Row {row_num}: QROC Correct must be '-', got '{corr}'")
            # Options A-F must be None
            for c_col, c_name in [(a_idx, 'A'), (b_idx, 'B'), (c_idx, 'C'), (d_idx, 'D'), (e_idx, 'E'), (f_idx, 'F')]:
                if r[c_col] is not None:
                    errors.append(f"Row {row_num}: QROC option {c_name} must be None, got '{r[c_col]}'")
            # EXP must not be empty
            if not r[exp_idx] or len(str(r[exp_idx]).strip()) == 0:
                errors.append(f"Row {row_num}: QROC model answer in 'EXP' cannot be empty!")
        else:
            errors.append(f"Row {row_num}: Invalid Type '{qtype}', must be 'QCS' or 'QROC'")
            
    total_qs = len(rows) - 1
    print(f"Total Rows Validated: {total_qs}")
    print(f"  - QCS (MCQ) Questions:     {qcs_count}")
    print(f"  - QROC (Written) Questions: {qroc_count}")
    
    if errors:
        print(f"\n[FAIL] Found {len(errors)} validation errors:")
        for e in errors[:20]:
            print(f"  ERROR: {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] 0 SCHEMA ERRORS, 0 OPTION MISMATCHES, 0 ARABIC CHARACTERS!")
        print("Master Question Bank is 100% compliant with the MBset standard specification!")

if __name__ == '__main__':
    validate('renal/Renal_Questions.xlsx')
