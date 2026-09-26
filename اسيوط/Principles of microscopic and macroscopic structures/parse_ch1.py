import json, re

with open('scratch_56_booklet_pages.json') as f:
    pages = json.load(f)

# P3, P4_L, P4_R, P5_L have Chapter 1
text_ch1 = pages.get('P3', '') + '\n' + pages.get('P4_L', '') + '\n' + pages.get('P4_R', '') + '\n' + pages.get('P5_L', '')

print("CH1 length:", len(text_ch1))
print("CH1 text snippet:")
print(text_ch1[:1000])
