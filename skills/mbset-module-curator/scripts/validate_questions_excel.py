#!/usr/bin/env python3
"""
MBset 31-Column Question Bank Validator
Validates Excel question bank files against official MBset schema and platform constraints.
"""

import sys
import os
import re
import argparse
import openpyxl

EXPECTED_HEADERS = [
    'id', 'Cas', 'Text', 'Image', 'explanationImage',
    'A', 'B', 'C', 'D', 'E', 'F',
    'A_EXP', 'B_EXP', 'C_EXP', 'D_EXP', 'E_EXP', 'F_EXP',
    'Correct', 'Hint', 'EXP', 'Note', 'Type',
    'categoryId', 'categoryName', 'subcategoryId', 'subcategoryName',
    'tagSuggere', 'Year', 'Tag', 'ImageMasks', 'ExplanationImageMasks'
]

ARABIC_REGEX = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')

def validate_excel(filepath: str) -> bool:
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False
        
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb.active
    
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print(f"Error: Sheet is empty in {filepath}")
        return False
        
    actual_headers = [str(c).strip() if c is not None else '' for c in rows[0]]
    
    # 1. Header Validation
    header_errors = []
    if len(actual_headers) != 31:
        header_errors.append(f"Header length is {len(actual_headers)}, expected exactly 31 columns.")
    for idx, (exp, act) in enumerate(zip(EXPECTED_HEADERS, actual_headers)):
        if exp != act:
            header_errors.append(f"Col {idx}: expected '{exp}', found '{act}'")
            
    if header_errors:
        print("[-] Schema Header Errors:")
        for err in header_errors:
            print(f"    - {err}")
        return False
    else:
        print("[+] Header schema: 31/31 columns strictly match.")

    # 2. Row by row validation
    total_questions = len(rows) - 1
    errors = []
    mcq_count = 0
    written_count = 0
    
    for r_idx, row in enumerate(rows[1:], start=2):
        # Column 0: id must be None
        if row[0] is not None and str(row[0]).strip() != '':
            errors.append(f"Row {r_idx}: 'id' column must be empty (None), found '{row[0]}'")
            
        # Column 2: Text
        text = str(row[2]) if row[2] is not None else ''
        if not text or len(text.strip()) < 5:
            errors.append(f"Row {r_idx}: Question stem 'Text' is missing or too short: '{text}'")
        if ARABIC_REGEX.search(text):
            errors.append(f"Row {r_idx}: Arabic characters found in stem 'Text'")
            
        # Column 21: Type
        qtype = str(row[21]).strip() if row[21] is not None else ''
        if qtype not in ['QCS', 'QROC']:
            errors.append(f"Row {r_idx}: Invalid Type '{qtype}', must be 'QCS' or 'QROC'")
            
        # Column 17: Correct
        cor = str(row[17]).strip() if row[17] is not None else ''
        
        # Options A-F (cols 5 to 10)
        options = {}
        for col_i, let in enumerate(['A', 'B', 'C', 'D', 'E', 'F'], start=5):
            val = row[col_i]
            if val is not None and str(val).strip():
                options[let] = str(val).strip()
                if ARABIC_REGEX.search(str(val)):
                    errors.append(f"Row {r_idx}: Arabic characters in option {let}")
                    
        if qtype == 'QCS':
            mcq_count += 1
            if cor not in ['A', 'B', 'C', 'D', 'E', 'F']:
                errors.append(f"Row {r_idx}: MCQ Correct answer '{cor}' is not a valid uppercase letter (A-F)")
            elif cor not in options:
                errors.append(f"Row {r_idx}: MCQ Correct answer '{cor}' does not match any populated option ({list(options.keys())})")
            if len(options) < 2:
                errors.append(f"Row {r_idx}: MCQ has fewer than 2 options ({len(options)})")
            # Verify options start at A and are continuous
            expected_keys = [chr(ord('A') + i) for i in range(len(options))]
            actual_keys = sorted(options.keys())
            if actual_keys != expected_keys:
                errors.append(f"Row {r_idx}: Non-sequential options: found {actual_keys}, expected {expected_keys}")
                
        elif qtype == 'QROC':
            written_count += 1
            if cor != '-':
                errors.append(f"Row {r_idx}: Written question Correct answer must be '-', found '{cor}'")
            exp = row[19]
            if exp is None or not str(exp).strip():
                errors.append(f"Row {r_idx}: Written question must have model answer in 'EXP' column")
                
        # Columns 24 & 25: subcategoryId & subcategoryName should be None
        if row[24] is not None and str(row[24]).strip() != '':
            errors.append(f"Row {r_idx}: 'subcategoryId' should be empty, found '{row[24]}'")
        if row[25] is not None and str(row[25]).strip() != '':
            errors.append(f"Row {r_idx}: 'subcategoryName' should be empty, found '{row[25]}'")

    print(f"[+] Total questions: {total_questions} (MCQ: {mcq_count}, Written: {written_count})")
    
    if errors:
        print(f"[-] Validation FAILED with {len(errors)} error(s):")
        for err in errors[:30]:  # Cap display at 30
            print(f"    - {err}")
        if len(errors) > 30:
            print(f"    ... and {len(errors) - 30} more errors.")
        return False
    else:
        print("[+] All validation checks PASSED with 0 errors!")
        return True

def main():
    parser = argparse.ArgumentParser(description="Validate MBset 31-Column Question Bank Excel File")
    parser.add_argument("excel_path", help="Path to Excel question bank (.xlsx)")
    args = parser.parse_args()
    
    success = validate_excel(args.excel_path)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
