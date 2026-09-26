import re

with open('scratch_07_ocr.txt', encoding='utf-8') as f:
    text = f.read()

# Remove page markers
pages = text.split('=== PAGE ')

# We can parse page by page
# Page 1: Q1 to Q8
# Page 2: Q9 to Q20 (+ Q21 stem)
# Page 3: Q21 options to Q30 (+ Q31 stem)
# Page 4: Q31 options to Q40 (+ Q41 stem)
# Page 5: Q41 options to Q50
# Page 6: Q51 to Q61
# Page 7: Q62 to Q70 (+ Q71 stem)
# Page 8: Q71 options to Q81
# Page 9: Q82 to Q91
# Page 10: Q92 to Q102
# Page 11: Q103 to Q109

print('Total pages in OCR:', len(pages) - 1)
