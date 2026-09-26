import re, json, urllib.request

def test_fetch():
    url = 'https://doc-reader-guide.com/mcq-quizzes/2763'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    chunks = re.findall(r'self\.__next_f\.push\(\[1,\"(.*?)\"\]\)', html)
    full_text = ''.join(chunks).encode('utf-8').decode('unicode_escape')
    q_idx = full_text.find('\"questions\":[')
    start = q_idx + len('\"questions\":')
    bracket_depth = 0
    end = start
    for i in range(start, len(full_text)):
        if full_text[i] == '[':
            bracket_depth += 1
        elif full_text[i] == ']':
            bracket_depth -= 1
            if bracket_depth == 0:
                end = i + 1
                break
    qs = json.loads(full_text[start:end])
    print('Fetched Formative 2026 questions:', len(qs))

test_fetch()
