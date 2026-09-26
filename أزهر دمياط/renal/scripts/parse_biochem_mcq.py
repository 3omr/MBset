import re

with open("renal/markdown_output/Biochemistry Doctor's questions(MCQ).md") as f:
    text = f.read()

# Let's inspect the sections in this file
pages = text.split('## Page ')
print(f'Total pages in Biochem MCQ: {len(pages)-1}')
