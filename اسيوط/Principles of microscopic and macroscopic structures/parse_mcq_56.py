import re

with open('scratch_56_mcq_raw.txt') as f:
    text = f.read()

# Let's inspect sections
# Split by <<<PAGE_...>>>
pages = text.split('<<<PAGE_')
print(f"Total pages: {len(pages)-1}")

# We can parse questions by looking for numbers at start of lines or inside text
# E.g. ^\s*(\d+)[\.\)]\s*(.*)
