import fitz, pytesseract, re
from PIL import Image
import io

doc = fitz.open('01- Principles of microscopic and macroscopic structures/Anatomy Qs Bank(4).pdf')

# Let's inspect page by page
for pno in range(len(doc)):
    page = doc[pno]
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    txt = pytesseract.image_to_string(img)
    # count questions on this page
    q_matches = re.findall(r'(?:^|\n)\s*(\d{1,3})\s*[\.\-\)]\s*([A-Z][^\n]+)', txt)
    print(f'Page {pno+1}: {len(q_matches)} Qs found: {[q[0] for q in q_matches]}')
