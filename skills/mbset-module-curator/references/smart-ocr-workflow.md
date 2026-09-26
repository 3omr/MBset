# Smart OCR Workflow for MBset

Use this as a second OCR route for scanned PDFs, screenshots, and pages where the existing OCRmyPDF/Tesseract text is incomplete or garbled. It adapts the [Smart OCR skill](https://www.skills.sh/claude-office-skills/skills/smart-ocr) to MBset's source-by-source extraction and verification gates.

## Run PaddleOCR

PaddleOCR stays outside MBset's base requirements. This workspace has an isolated CPU environment at `.venv-smart-ocr/` with PaddlePaddle 3.3.0 and PaddleOCR 3.5.0. To recreate it on this workstation:

```bash
python3 -m venv .venv-smart-ocr
.venv-smart-ocr/bin/python -m pip install paddlepaddle==3.3.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
.venv-smart-ocr/bin/python -m pip install paddleocr==3.5.0
```

For another OS or a compatible GPU, install the matching inference engine from the [official installation guide](https://www.paddleocr.ai/latest/en/version3.x/installation.html), then install PaddleOCR 3.x in an isolated environment.

The helper uses PaddleOCR's English mobile detector and recognizer to fit this machine's available memory and disables MKL-DNN because its default oneDNN path raised a Paddle PIR runtime error during the first local inference. These CPU settings trade speed for reliable local inference.

Run the bundled extractor on one source at a time:

```bash
.venv-smart-ocr/bin/python .agents/skills/mbset-module-curator/scripts/ocr_paddle_pages.py "<source.pdf>" --output-dir /tmp/mbset-smart-ocr
```

It accepts PDF and common image files and uses English mobile detection/recognition models for MBset exam sources. For a screenshot set, pass each image path as an input. For very small print, render the affected page at 300 DPI with `pdftoppm` and pass the resulting image instead of the PDF. The script uses the PaddleOCR 3.x `PaddleOCR.predict()` interface and writes, for every page/image:

- a text draft with each line's confidence and bounding box;
- a JSON record with line text, confidence, and coordinates;
- a source manifest with page counts and low-confidence line counts.

The original source is never modified. PaddleOCR may download its model files the first time it runs.

## Read and reconcile the output

1. Render and inspect at least the first two pages, then inspect every page flagged with low-confidence lines. Use the source image/PDF as the authority.
2. Treat the configured confidence cutoff (default `0.85`) only as a review flag. It is not a probability of correctness: high-confidence medical terms, option letters, superscripts, and answer markings still need source checks.
3. Use bounding boxes to reconstruct reading order. For multi-column pages, extract each column separately and concatenate in page/column order; never accept a global top-to-bottom transcript that interleaves columns.
4. Keep OCR output as working evidence only. Continue the normal file-specific Markdown extraction, figure handling, noise removal, three-counter completeness audit, and answer-source verification. OCR confidence never changes `Answer Source`, proves an answer key, or permits filling a missing stem/option.
5. If PaddleOCR and the existing text layer disagree, resolve against the rendered original. Log unresolved questions as `EXCLUDED — unreadable scan` in the catalog.

## References

- [Smart OCR skill page](https://www.skills.sh/claude-office-skills/skills/smart-ocr)
- [PaddleOCR 3.x OCR pipeline and result format](https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/OCR.html)
- [PaddleOCR installation guide](https://www.paddleocr.ai/latest/en/version3.x/installation.html)

The Smart OCR skill page includes examples for earlier PaddleOCR APIs. The bundled helper follows the current 3.x API documented above.
