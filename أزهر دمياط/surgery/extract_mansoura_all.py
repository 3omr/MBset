import os, sys, json, re, time
os.environ['OMP_THREAD_LIMIT'] = '1'

import cv2, numpy as np, fitz, pytesseract
from multiprocessing import Pool

pdf_path = 'surgery/اسئلة/McQ surgery mansoura .pdf'
cache_dir = 'scratch/mansoura_cache'
os.makedirs(cache_dir, exist_ok=True)

def process_single_page(p_idx):
    cache_file = os.path.join(cache_dir, f'page_{p_idx+1:03d}.json')
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    doc = fitz.open(pdf_path)
    pix = doc[p_idx].get_pixmap(dpi=200)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))[:, :, :3]
    h, w = img.shape[:2]
    
    # Gutter split at x=1170
    left_page = img[:, :1170]
    right_page = img[:, 1170:]
    
    page_results = []
    
    for side_name, p_img in [('left', left_page), ('right', right_page)]:
        ph, pw = p_img.shape[:2]
        gray = cv2.cvtColor(p_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY_INV)
        scale = 30
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (scale, 1))
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, scale))
        table_grid = cv2.add(cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_h), cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_v))
        contours, _ = cv2.findContours(table_grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        table_boxes = []
        table_answers = {}
        
        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            if bw > 120 and bh > 50:
                table_boxes.append((x, y, bw, bh))
                tbl = p_img[y:y+bh, x:x+bw]
                col_div = int(bw * 0.45)
                
                # Ans col
                ans_crop = tbl[15:bh-5, col_div:bw-5]
                if ans_crop.shape[0] > 10 and ans_crop.shape[1] > 10:
                    gray_a = cv2.cvtColor(ans_crop, cv2.COLOR_BGR2GRAY)
                    th_a = cv2.threshold(gray_a, 200, 255, cv2.THRESH_BINARY)[1]
                    row_m = np.mean(th_a, axis=1)
                    for ry, rm in enumerate(row_m):
                        if rm < 150:
                            th_a[max(0, ry-1):min(len(row_m), ry+2), :] = 255
                    th_a = cv2.copyMakeBorder(th_a, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
                    th_a = cv2.resize(th_a, (0,0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    txt_a = pytesseract.image_to_string(th_a, config='--psm 6 -c tessedit_char_whitelist=ABCDE\n').strip().split()
                else:
                    txt_a = []
                    
                # Q col
                q_crop = tbl[15:bh-5, 5:col_div]
                if q_crop.shape[0] > 10 and q_crop.shape[1] > 10:
                    gray_q = cv2.cvtColor(q_crop, cv2.COLOR_BGR2GRAY)
                    th_q = cv2.threshold(gray_q, 200, 255, cv2.THRESH_BINARY)[1]
                    row_m = np.mean(th_q, axis=1)
                    for ry, rm in enumerate(row_m):
                        if rm < 150:
                            th_q[max(0, ry-1):min(len(row_m), ry+2), :] = 255
                    th_q = cv2.copyMakeBorder(th_q, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
                    th_q = cv2.resize(th_q, (0,0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    txt_q = pytesseract.image_to_string(th_q, config='--psm 6 -c tessedit_char_whitelist=0123456789\n').strip().split()
                else:
                    txt_q = []
                    
                for q_num, ans_let in zip(txt_q, txt_a):
                    table_answers[q_num] = ans_let
                    
        # Mask out table
        masked_page = p_img.copy()
        for x, y, bw, bh in table_boxes:
            masked_page[max(0, y-10):min(ph, y+bh+10), max(0, x-10):min(pw, x+bw+10)] = 255
            
        txt = pytesseract.image_to_string(masked_page, config='--psm 6')
        page_results.append({
            'page': p_idx + 1,
            'side': side_name,
            'answers': table_answers,
            'ocr': txt
        })
        
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(page_results, f, ensure_ascii=False, indent=2)
        
    print(f"Processed Page {p_idx+1}/120: left {len(page_results[0]['answers'])} ans, right {len(page_results[1]['answers'])} ans", flush=True)
    return page_results

if __name__ == '__main__':
    pages = list(range(1, 121)) # pages 2 to 121 in 1-based index (0-indexed 1 to 120)
    print(f'Processing {len(pages)} pages using 4 worker processes...')
    t0 = time.time()
    with Pool(4) as pool:
        all_results = pool.map(process_single_page, pages)
    t1 = time.time()
    print(f'Finished all {len(pages)} pages in {t1-t0:.2f} seconds!')
