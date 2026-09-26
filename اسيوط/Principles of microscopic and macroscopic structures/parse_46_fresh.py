import re

with open('scratch_46_ocr.txt', encoding='utf-8') as f:
    raw = f.read()

# Remove headers/footers
raw = re.sub(r'=== PAGE \d+ ===', '', raw)
raw = re.sub(r'CamScanner[^\n]*', '', raw)
raw = re.sub(r'Chapter 6:\s*Anatomy', '', raw)

# Questions 1 to 30 (Pages 2-4)
# Matchings 31 to 40 (Pages 5-7)
# Clinical MCQs 41 to 52 (Pages 8-9)

# Let's extract MCQs by finding \n(\d+)\.\s*([^\n]+)
# and options \n([a-e])\.\s*([^\n]+)
