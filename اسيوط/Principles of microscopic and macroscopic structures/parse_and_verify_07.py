import re

with open('scratch_07_ocr.txt', encoding='utf-8') as f:
    raw = f.read()

# Let's clean noise headers/footers
raw = re.sub(r'=== PAGE \d+ ===', '', raw)
raw = re.sub(r'Scanned with CamScanner', '', raw)
raw = re.sub(r'\d+\s+Page', '', raw)

# Let's write out each question cleanly
# We will define a structured parser for the 109 questions
