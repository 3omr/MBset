import re

with open('Markdown_Questions/56_embryology_Qs_bank.md') as f:
    text = f.read()

# Find all questions in 56_embryology_Qs_bank.md
raw_qs = re.findall(r'### Question (\d+)\n(.*?)(?=\n### Question|\Z)', text, re.DOTALL)
print(f"Total raw questions in 56: {len(raw_qs)}")

# Let's inspect the first 20 questions
for qnum, body in raw_qs[:20]:
    lines = [l.strip() for l in body.split('\n') if l.strip()]
    stem = lines[0] if lines else ""
    opts = [l for l in lines if l.startswith('- **')]
    print(f"Q{qnum}: {len(opts)} opts | {stem[:70]}")
