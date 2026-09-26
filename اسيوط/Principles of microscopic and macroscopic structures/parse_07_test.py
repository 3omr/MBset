import re

with open('scratch_07_ocr.txt', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== PAGE ')

# Let's inspect all questions across the 11 pages
# We will build clean questions list
