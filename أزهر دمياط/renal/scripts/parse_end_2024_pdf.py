import fitz, re

doc = fitz.open('renal/Raw_PDF_Questions/Renal/End 2024.pdf')
full_text = ""
for i, page in enumerate(doc):
    t = page.get_text()
    # Normalize page breaks
    full_text += f"\n--- PAGE {i+1} ---\n" + t

# Clean known header noise
full_text = re.sub(r'(?i)free\s*phalasstine[^\n]*', '', full_text)
full_text = re.sub(r'(?i)dire+cted\s*by[^\n]*', '', full_text)
full_text = re.sub(r'[\u1d400-\u1d7ff]+', '', full_text) # unicode math/stylized font
full_text = full_text.replace('\xa0', ' ').replace('\u200b', '')

print("Total length of text:", len(full_text))

# Let's inspect the question blocks
# Normalize roman numeral II) to 11)
full_text = re.sub(r'(?m)^\s*II\)\s*', '11) ', full_text)
# Normalize 33 ) to 33)
full_text = re.sub(r'(?m)^\s*33\s*\)\s*', '33) ', full_text)

# Find all questions starting with number)
q_pattern = re.compile(r'(?m)^(?:\s*---\s*PAGE\s*\d+\s*---\s*)*^\s*(\d{1,2})\)\s*(.*?)(?=^\s*(?:\d{1,2}\)|---\s*PAGE|$))', re.DOTALL | re.MULTILINE)

# Let's test matches
matches = list(re.finditer(r'(?m)^\s*(\d{1,2})\)\s*(.+)', full_text))
print("Found question starts:", len(matches))
