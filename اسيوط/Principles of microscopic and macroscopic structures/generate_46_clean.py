import re

c = open('Markdown_Questions/46_anatomy_bank.md', encoding='utf-8').read()

# Let's clean noise
c = re.sub(r'[\u0600-\u06FF]+', '', c)
c = re.sub(r'CamScanner[^\n]*', '', c)
c = re.sub(r'Chapter 6:\s*Anatomy', '', c)
c = re.sub(r'\*\s+\*\s+\*', '', c)
c = re.sub(r'-\s*\*\*([A-F])\)\*?\s*', r'- **\1)** ', c)
c = re.sub(r'\*\s*\*', '', c)

# Let's verify all questions in 46
# We will inspect each question and set authentic medical answers
# Let's load the answer key from page 10 for matching questions 31-40
# And solve MCQs 1-30 and 41-52 medically
