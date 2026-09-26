import fitz, re

doc = fitz.open('01- Principles of microscopic and macroscopic structures/embryology Qs bank(3).pdf')

chapters = [
    ("Male and female genital system & Gametogenesis", 4, 18),
    ("Ovarian and menstrual cycle", 19, 22),
    ("Fertilization", 23, 32),
    ("Implantation", 33, 38),
    ("Decidua", 39, 41),
    ("Embryonic disc", 42, 43),
    ("Extra-embryonic mesoderm", 44, 45),
    ("Derivatives of the three germ layers", 46, 51),
    ("Notochord and Gastrulation", 52, 57),
    ("Neurulation and folding", 58, 60),
    ("Fetal membranes", 61, 66),
    ("Placenta and umbilical cord & twins", 67, 76)
]

for name, start, end in chapters:
    # Get answer table on page end
    key_txt = doc[end-1].get_text()
    pos = key_txt.lower().find('answers of')
    if pos == -1:
        print('KEY NOT FOUND:', name)
        continue
    sub = key_txt[pos:]
    sub = re.split(r'[\u0600-\u06FF]', sub)[0]
    tokens = sub.strip().split()
    
    # parse grid of numbers and letters
    ans_map = {}
    i = 0
    while i < len(tokens):
        current_nums = []
        while i < len(tokens) and tokens[i].isdigit():
            current_nums.append(int(tokens[i]))
            i += 1
        current_letters = []
        while i < len(tokens) and not tokens[i].isdigit():
            current_letters.append(tokens[i].upper())
            i += 1
        for n, l in zip(current_nums, current_letters):
            ans_map[n] = l
            
    # Get questions text from start to end
    ch_txt = ''
    for p in range(start-1, end):
        ch_txt += doc[p].get_text() + '\n'
    # cut at answer table
    p_key = ch_txt.lower().find('answers of')
    if p_key != -1:
        ch_txt = ch_txt[:p_key]
        
    # clean header
    ch_txt = re.sub(r'[\u0600-\u06FF]+', '', ch_txt)
    ch_txt = re.sub(r'https\s*\?[^\n]+', '', ch_txt)
    ch_txt = re.sub(r'www[^\n]+', '', ch_txt)
    
    # split questions
    q_splits = re.split(r'(?:^|\n)\s*(\d+)[\.\-\)]\s*', ch_txt)
    print(f'{name:40}: {len(q_splits)//2} Qs extracted | {len(ans_map)} answers in key')
