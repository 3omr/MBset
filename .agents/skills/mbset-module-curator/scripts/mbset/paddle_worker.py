"""PaddleOCR worker — run with the Python that has PaddleOCR 3.x (e.g. `.venv-smart-ocr/bin/python`).

    python paddle_worker.py page1.png page2.png ...   →   JSON on stdout: [[{text, box, score}, ...], ...]

`ocr.py` calls it once per source (the model loads once) when a profile sets `ocr.tool: paddle`.
PaddleOCR reads phone photos, curved or unevenly lit scans and bold headings far better than
Tesseract; it gives line boxes but no word boxes.
"""

import json
import sys
import warnings


def main(paths: list[str]) -> int:
    warnings.filterwarnings("ignore")
    from paddleocr import PaddleOCR

    engine = PaddleOCR(text_detection_model_name="PP-OCRv5_mobile_det",
                       text_recognition_model_name="en_PP-OCRv5_mobile_rec",
                       use_doc_orientation_classify=False, use_doc_unwarping=False,
                       use_textline_orientation=False, device="cpu", enable_mkldnn=False)
    pages = []
    for path in paths:
        lines = []
        for res in engine.predict(path):
            for text, box, poly, score in zip(res["rec_texts"], res["rec_boxes"], res["rec_polys"], res["rec_scores"]):
                if not str(text).strip():
                    continue
                # a slightly tilted line has a tall axis-aligned box that overlaps its neighbours; keep the
                # box's x range but take y from the polygon: centre ± half the line's own height
                ys = [float(p[1]) for p in poly]
                h = ((poly[3][1] - poly[0][1]) + (poly[2][1] - poly[1][1])) / 2
                cy = sum(ys) / 4
                x0, _, x1, _ = (int(v) for v in box)
                lines.append({"text": str(text), "box": [x0, int(cy - h / 2), x1, int(cy + h / 2)],
                              "score": float(score)})
        pages.append(lines)
    sys.stdout.write("\n@@MBSET_JSON@@\n" + json.dumps(pages))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
