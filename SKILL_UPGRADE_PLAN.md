# خطة تطوير سكيل `mbset-module-curator` — استخراج أسرع وأدق

**التاريخ:** 2026-09-26
**الهدف:** نقلل وقت استخراج الموديول من أيام لساعات، ونرفع الدقة، من غير ما نكسر الـ prime directive (كل سؤال موجود، وإجابته هي اللي في المصدر، والاتنين متثبتين بالقياس).

---

## 0. التشخيص (ليه الشغل بطيء دلوقتي)

| المشكلة | الدليل من المشروع | الأثر |
| :--- | :--- | :--- |
| الموديل بيكتب كل سؤال بإيده (output tokens) | `scripts/extract_endocrinology_*.py` فيها الأسئلة كـ Python literals، و174 سكريبت مؤقت في `scratch/` | أبطأ وأغلى جزء في الشغل كله، وفيه خطر تلخيص أو إعادة صياغة |
| إعادة صياغة بدل نقل حرفي | مثال: `"A 72-year-old man with hypoglycemia most likely took which medication?"` | الأسئلة مش verbatim، فالدقة بتقل |
| القاعدة "Never run a generic regex script" | `SKILL.md` Stage 1 §1 | كل ملف بيبدأ من الصفر |
| نص المصادر scanned | 179 من 367 PDF مالهمش text layer | الـ OCR والقراءة بالعين بيحصلوا جوه الـ session |
| مفيش dedupe للمصادر | 8 ملفات مكررة بنفس الـ sha256 جوه `Raw_PDF_Questions` | نفس الملف بيتستخرج مرتين |
| أرقام ملفات مكررة في الـ markdown | Endocrinology: `01_…` مرتين و`32_…` مرتين | الـ catalog بيلخبط والـ reconciliation بيفشل |
| مفيش حالة محفوظة لكل ملف | — | لما الـ context يتقفل أو الـ session تقع، الشغل بيتعاد |
| SKILL.md طويل (246 سطر + 7 references) | — | كل agent بيستهلك tokens كتير عشان يقراه قبل ما يشتغل |
| مفيش git | المشروع مش git repo | مفيش rollback لو تعديل على السكيل بوّظ حاجة |

**المبدأ الجديد:**
> **Parse first, review second.** السكريبتات هي اللي تنقل النص من المصدر. الموديل يكتب **profile** صغير، ويراجع **التقرير**، ويصلّح **الأسئلة المعلّمة بس**. الموديل ممنوع يكتب نص سؤال من ذاكرته.

---

## 1. البنية الجديدة (نظرة عامة)

أداة واحدة `mbset.py` بـ subcommands، وكل خطوة بتكتب state في `<Module>/.mbset/state.json`:

```
mbset.py inventory  <Module>          # Stage 0: expand archives, hash, dedupe, triage, catalog skeleton
mbset.py ocr        <Module>          # Stage 0.5: OCR متوازي لكل الـ scanned (background)
mbset.py profile    <Module> <file>   # يقترح profile أولي للملف من الـ triage
mbset.py parse      <Module> [file]   # Stage 1: profile + text → markdown + flags
mbset.py answers    <Module> [file]   # Stage 2: key grids / marked (bold/highlight) / DocReader online
mbset.py figures    <Module> [file]   # Stage 1 §7: crop الصور للأسئلة المعتمدة على figure
mbset.py check      <Module> [file]   # Stage 2+3: كل الـ gates → تقرير بالمشاكل بس
mbset.py packets    <Module> --n 4    # يقسم الملفات على agents متوازيين
mbset.py build      <Module>          # Stage 4: Excel + validate + audit
mbset.py status     <Module>          # حالة كل ملف في كل stage
```

كل السكريبتات بتفضل في `.agents/skills/mbset-module-curator/scripts/`، والـ mirror `skills/` بيتعمله sync بسكريبت.

---

## 2. المراحل

### المرحلة A — الأساس والأمان (قبل أي كود جديد)

| # | المهمة | التفاصيل |
| :--- | :--- | :--- |
| A1 | `git init` للمشروع | نتتبع السكيل والسكريبتات والـ markdown بس، ونعمل `.gitignore` للـ PDFs والصور والـ OCR والـ `.venv*` و`scratch/`. كده أي تعديل على السكيل يترجع فيه |
| A2 | Golden test set | ناخد 6 إلى 8 ملفات من Endocrinology متراجعة يدوي، ونغطي كل الأنواع: digital single، multi-column، scanned، marked، key grid، DocReader، docx، written. الـ markdown الحالي بتاعهم يبقى الـ expected output في `tests/fixtures/` |
| A3 | `sync_skill.sh` | ينسخ `.agents/skills/mbset-module-curator` → `skills/mbset-module-curator`، ويفشل لو حد عدّل في الـ mirror بإيده |
| A4 | تنظيف `scratch/` | ننقل السكريبتات اللي ليها قيمة لـ `scripts/legacy/` والباقي يتأرشف. ومن هنا ورايح أي شغل مؤقت يروح `<Module>/.mbset/work/` |

**معيار القبول:** `git status` نضيف، والـ fixtures موجودة، والـ sync شغال.

---

### المرحلة B — Stage 0 أوتوماتيك: `inventory` + `triage`

| # | المهمة | التفاصيل |
| :--- | :--- | :--- |
| B1 | فك الـ archives | zip/7z/rar → `Raw_PDF_Questions/`، ويتسجل إن الملف الفلاني جاي من الأرشيف الفلاني |
| B2 | Hash + dedupe | sha256 لكل مصدر. المكرر يتعلّم `EXCLUDED — duplicate of <file>` تلقائي |
| B3 | Near-duplicate | ملفين بأسماء مختلفة وأول 3 صفحات نصهم متطابق فوق 95% (`rapidfuzz`) → يتعلّموا للمراجعة، مش استبعاد تلقائي |
| B4 | Triage classifier | لكل ملف: عدد الصفحات، وهل فيه text layer، وعدد الأعمدة (من `extract_pdf_columns --probe`)، والـ signatures: Moodle (`Select one:`, `Flag question`) وDocReader (`doc-reader-guide.com`) وphone screenshot وslides وdocx/pptx. كمان هل فيه bold/highlight على الاختيارات، وهل فيه answer grid في آخر صفحتين |
| B5 | Index ثابت | كل مصدر ياخد `NN` فريد ومش بيتغير، وده بيمنع تكرار `01_` و`32_` |
| B6 | Tag/Year مقترح | من اسم الملف والفولدر، طبقاً لـ `tagging-and-naming.md` (Damietta / Assiut)، مع normalize لأسماء الدكاترة. الناتج **مقترح** والموديل يأكده |
| B7 | Catalog skeleton | `00_CATALOG_OF_ALL_FILES.md` + `.mbset/inventory.json` بيتولّدوا أوتوماتيك |

**معيار القبول:** على Endocrinology، الـ inventory يطلع نفس عدد المصادر اللي في الـ catalog الحالي، والـ 8 مكررات يتكشفوا.

---

### المرحلة C — Stage 0.5: OCR جماعي في الخلفية

| # | المهمة | التفاصيل |
| :--- | :--- | :--- |
| C1 | دمج `scripts/ocr_module_sources.py` في `mbset.py ocr` | OCRmyPDF/Tesseract، و`--workers 4 --ocr-jobs 2` على 8 cores، وبيشتغل على الملفات الـ scanned بس (من الـ triage) |
| C2 | Cache | لو الـ OCR اتعمل قبل كده (بنفس الـ hash) مايتعادش |
| C3 | Confidence لكل صفحة | من Tesseract (`hocr`/`tsv`) أو PaddleOCR للصفحات الصعبة. الصفحات اللي confidence بتاعها واطي تتعلّم في الـ state |
| C4 | الموديل مايستناش | الـ OCR يبدأ أول ما الـ inventory يخلص، والـ agent يشتغل على الملفات الـ digital في نفس الوقت |
| C5 | Vision fallback | الصفحات المعلّمة بس هي اللي الموديل يبص على صورتها (render بـ 200 DPI). ده بدل ما يبص على كل الصفحات |

**ملاحظة:** الـ GPU (Quadro M2000M) ضعيف، فـ PaddleOCR على الـ CPU للصفحات الصعبة بس، وTesseract المتوازي هو الأساس.

---

### المرحلة D — Stage 1: الـ Parser العام + Profiles (أكبر مكسب)

#### D1. شكل الـ profile
ملف لكل مصدر في `<Module>/.mbset/profiles/<NN>.yaml`، وبيطلع مقترح من الـ triage والموديل يصلّحه:

```yaml
source: "Raw_PDF_Questions/end 2024.pdf"
text: ocr            # native | columns | ocr | docx | pptx | moodle | images
columns: auto        # 1 | 2 | auto
pages: "1-12"
skip_patterns: ["^DocReader Guide", "^Page \\d+ of \\d+"]
question_start: '^\s*(\d{1,3})\s*[.)-]\s+'
option_pattern: '^\s*\(?([a-eA-E])[.)]\s+'   # أو inline: "a. … b. … c. …"
options_inline: false
sections_restart: true        # الترقيم بيرجع 1 مع كل chapter
declared_total: 90            # لو المصدر كاتب العدد
answers:
  mode: grid                  # grid | inline | marked | online | none
  grid_pages: "12"
  grid_pattern: '(\d+)\s*[-.:]?\s*([A-E])'
written:
  start_marker: "Written questions"
  model_answer: after_question
```

#### D2. `parse_questions.py`
- بيقرا النص حسب `text`: native أو columns (`extract_pdf_columns.py`) أو OCR text أو `python-docx`/`python-pptx`.
- بيقسّم الأسئلة بالـ `question_start` ويتابع الـ section restarts.
- بيفصل الاختيارات، سواء كل اختيار في سطر أو inline، وبيعمل repack من A.
- بيطبق `clean_markdown_noise.py` (نفس القواعد) وتصليح الـ notation: `Ca²⁺`, `β1`, `µm`, `→`.
- **بينقل النص حرفي من المصدر**، ومفيش أي إعادة صياغة.
- بيكتب `<NN>_<Source>.md` بالفورمات الحالي بالظبط، عشان `build_module_template.py` يفضل شغال من غير تغيير.
- وبيكتب `.mbset/flags/<NN>.json` بالأسئلة المشكوك فيها:
  - اختيارات أقل من 2 أو فيها فجوة (A, B, D)
  - سطر فيه رقمين أسئلة مختلفين (chimera)
  - سؤال طويل بشكل غير طبيعي (غالباً سؤالين اندمجوا)
  - فجوة في الترقيم (سؤال 14 ناقص)
  - stem فيه كلمات figure ومفيش صورة
  - Arabic أو noise باقي بعد التنظيف
  - سطور من صفحة confidence الـ OCR بتاعها واطي

#### D3. Recipes جاهزة (profiles templates)
profile جاهز لكل نوع معروف في `references/profiles/`:
`digital_single`, `digital_two_column`, `scanned_marked`, `moodle_review`, `phone_screenshots`, `docreader`, `docx_bold`, `pptx_answer_line`, `department_book_sections`, `written_only`.
الموديل يختار الـ template ويغيّر 2 أو 3 سطور بس.

#### D4. Escape hatch
لو ملف غريب جداً والـ parser مش قادر عليه (مثلاً handwritten)، الموديل مسموحله يكتب الـ markdown يدوي. بس يتعلّم في الـ state `method: manual`، والـ `check` بيطلب spot-check مضاعف (20%).

**معيار القبول:** على الـ golden set، الـ parser يطلع نفس عدد الأسئلة، ونص الـ stems يتطابق مع الـ expected بنسبة ≥ 98% (`rapidfuzz`) من غير تدخل يدوي، في 6 من 8 ملفات على الأقل.

---

### المرحلة E — Stage 2: الإجابات أوتوماتيك

| # | المهمة | التفاصيل |
| :--- | :--- | :--- |
| E1 | Key grid parser | يقرا جداول الإجابات (`1-A 2-C …` أو جدول) من الصفحات المحددة ويربطها برقم السؤال، مع مراعاة الـ section restarts. `Answer Source: key` |
| E2 | Inline key | `Answer: C` / `Ans: c` / `(C)` في آخر السؤال. `key` |
| E3 | Marked detection (digital) | PyMuPDF `get_text("dict")`: الاختيار اللي font بتاعه bold، أو لونه مختلف، أو عليه highlight annotation، أو جوه rectangle ملون (`page.get_drawings()`). `marked` |
| E4 | Marked detection (scanned) | نقيس كثافة الألوان حوالين كل اختيار من الـ bbox بتاع الـ OCR: highlight أصفر أو أخضر، أو علامة ✓، أو دايرة. `marked`، مع confidence. والـ confidence الواطي يتعلّم |
| E5 | docx/pptx | `run.bold` و`run.font.highlight_color` و`run.font.color`. `marked` |
| E6 | DocReader online | fetcher يجيب الإجابات من `doc-reader-guide.com/mcq-quizzes/<id>` ويعمل cache في `.mbset/online/`. `online`. الـ cache الموجود في `scratch/all_docreader_subjects.json` يتنقل ويتستخدم |
| E7 | Derived | الموديل بيجاوب **بس** على الأسئلة اللي مالهاش مصدر، وبيعمل كده في batch واحد لكل ملف، وتتعلّم `derived`. والعدد يتحط في تقرير للمستخدم |
| E8 | تعارض بين المصادر | لو نفس الـ stem (normalized) موجود في مصدرين بإجابتين مختلفتين، الاتنين يتعلّموا للمراجعة. **مفيش نسخ** إجابة من ملف لملف، ده مجرد تنبيه |

**معيار القبول:** على الـ golden set، الإجابات الأوتوماتيك تطابق الـ expected بنسبة ≥ 97% في الملفات الـ key/marked، والـ bias gate يعدّي.

---

### المرحلة F — الصور (Figure-dependent questions)

| # | المهمة | التفاصيل |
| :--- | :--- | :--- |
| F1 | Detect | regex الـ figure الموجود في الـ playbook §7 |
| F2 | Locate | PyMuPDF `page.search_for(stem[:60])` يلاقي الصفحة والـ bbox |
| F3 | Crop | أقرب embedded image أو drawing region للسؤال (فوقه أو تحته) → `Images/<NN>_<Qn>.png` بـ 200 DPI |
| F4 | Contact sheet | صورة واحدة فيها كل الـ crops بتاعة الملف، والموديل يبص عليها **مرة واحدة** بدل ما يفتح كل crop لوحده |
| F5 | فشل | لو مفيش صورة اتلقت: `EXCLUDED — figure unrecoverable` بعد تأكيد الموديل |

---

### المرحلة G — Gate واحد: `mbset.py check`

يجمع اللي موجود حالياً (`audit_question_bank.py`, `clean_markdown_noise.py` inspection) مع فحوصات جديدة، **ويطلّع المشاكل بس**:

- الـ **three counters**: أعلى رقم في المصدر، وعدد الـ option-A blocks، وعدد الـ `### Q`، ولازم يتفقوا مع الـ `declared_total`
- الـ **bias gate** (45% investigate / 60% fail)
- Arabic = 0، وnoise signatures = 0، وnotation سليمة
- الاختيارات sequential، و`Correct` موجود ضمن الاختيارات
- كل MCQ عليه `Answer Source`
- كل figure question ليه `Image` والملف موجود فعلاً
- **Spot-check sampler**: يختار `max(5, 10%)` أسئلة موزعة على الملف، ويعمل render للجزء بتاعها من المصدر جنب نص الـ markdown في صورة واحدة (side-by-side). الموديل يأكد بنظرة، والنتيجة تتسجل في الـ catalog: `spot-check 6/6 OK`
- الـ **reconciliation**: عدد المصادر = عدد الـ markdown + الـ EXCLUDED، ومفيش index مكرر
- الناتج: `.mbset/reports/check_<date>.md`، وexit code غير صفر لو فيه hard fail

**معيار القبول:** على Endocrinology الحالي، يكشف الـ index المكرر (`01`, `32`)، ويعدّي باقي الملفات السليمة.

---

### المرحلة H — التوازي (Parallel agents)

| # | المهمة | التفاصيل |
| :--- | :--- | :--- |
| H1 | `mbset.py packets <Module> --n 4` | يقسم الملفات لـ N حزم متوازنة بعدد الصفحات، ويكتب `.mbset/packets/packet_<k>.md`. كل حزمة فيها: قايمة الملفات، والأوامر اللي تتشغل، ومعيار الـ done |
| H2 | ملكية واضحة | كل agent بيكتب في `profiles/`، و`<NN>_*.md`، و`flags/` بتوع ملفاته **بس**. الـ catalog والـ Excel بيتولّدوا من الـ state بسكريبت، ومحدش بيعدّلهم بإيده |
| H3 | Lock بسيط | `.mbset/locks/<NN>.lock` عشان اتنين agents مايشتغلوش على نفس الملف |
| H4 | تعليمات لكل أداة | قسم في السكيل: إزاي تشغّل 4 sessions في Antigravity، أو Codex، أو Claude Code subagents، وكل واحدة تاخد packet |
| H5 | Merge | لما الحزم تخلص: `mbset.py check` على الموديول كله، وبعدها `build` |

---

### المرحلة I — Stage 4 (تحسينات صغيرة)

- `mbset.py build` يشغّل `build_module_template.py`، وبعده `validate_questions_excel.py`، وبعده `audit_question_bank.py --by-tag` ورا بعض، ويفشل عند أول gate يفشل.
- الـ Tag/Year/tagSuggere تتقري من `inventory.json` بدل ما تتكتب يدوي في `tag_map.json`.
- تقرير نهائي: الأعداد لكل مصدر مقابل الـ catalog، وعدد الـ derived لكل ملف.
- Migration أوتوماتيك للـ legacy layout (`Genetics`, `POD`) لما نلمسهم.

---

### المرحلة J — إعادة كتابة السكيل نفسها

| # | المهمة | التفاصيل |
| :--- | :--- | :--- |
| J1 | SKILL.md أقصر | حوالي 120 سطر: الـ prime directive، والـ workflow بالأوامر (`inventory → ocr → profile → parse → answers → figures → check → build`)، والقواعد اللي مش قابلة للنقاش. والتفاصيل تفضل في الـ references (progressive disclosure) |
| J2 | تغيير القاعدة | بدل "Never run a generic regex script across several files" تبقى: **"Every file gets its own triage and its own profile; one shared parser executes profiles. Never type question text from memory."** |
| J3 | `references/profiles.md` | شرح كل حقل في الـ profile، ومعاه الـ templates |
| J4 | `references/parallel-workflow.md` | شرح الـ packets والتوزيع على أكتر من agent |
| J5 | `references/model-routing.md` | إيه اللي يروح لموديل سريع (كتابة الـ profile، وتصليح الـ flags، والـ spot-check البصري) وإيه اللي يروح للموديل التقيل (الـ derived answers، والتعارضات، والملفات الـ manual) |
| J6 | تحديث `AGENTS.md` | Pipeline C يبقى بالأوامر الجديدة، ويتضاف قسم "Speed rules" |
| J7 | Sync | `sync_skill.sh`، وتأكد إن `skills/` متطابقة |

---

### المرحلة K — القياس (Benchmark)

1. نشغّل الـ pipeline الجديدة على **Endocrinology** من الصفر، في فولدر منفصل، والأصلي مايتلمسش.
2. نقارن بالـ markdown والـ Excel الحاليين:
   - عدد الأسئلة لكل مصدر
   - تطابق الـ stems (fuzzy ≥ 95%)
   - تطابق الإجابات
   - الفروقات: هل هي غلطة في النسخة القديمة (زي الأسئلة الملخصة) ولا في الجديدة
3. نقيس الوقت وعدد الـ tokens، قبل وبعد.
4. نجرب بعدها على موديول Assiut واحد، عشان نتأكد إن الـ tagging والـ profiles شغالين هناك كمان.

**النتيجة المتوقعة:** الجزء الميكانيكي (نقل النص) يبقى ثواني بدل ساعات، ووقت الموديل يروح في المراجعة والملفات الصعبة بس. التقدير الواقعي إن الوقت الكلي يقل من **5 لـ 10 مرات**، والدقة ترتفع لأن النص بيتنقل حرفي.

---

## 3. ترتيب التنفيذ

| الترتيب | المرحلة | ليه بالترتيب ده |
| :---: | :--- | :--- |
| 1 | A (git + golden set) | الأمان والقياس قبل أي تغيير |
| 2 | B (inventory/triage) | كل حاجة بعدها بتعتمد عليه |
| 3 | G (check) | عشان نقيس كل خطوة جاية |
| 4 | D (parser + profiles) | أكبر مكسب في السرعة |
| 5 | E (answers) | أكبر مكسب في الدقة |
| 6 | C (OCR جماعي) | موجود جزئياً، ومحتاج دمج بس |
| 7 | F (figures) | |
| 8 | H (parallel) | بعد ما الأدوات تبقى ثابتة |
| 9 | I + J (build + كتابة السكيل) | نكتب السكيل بعد ما نعرف الأدوات اشتغلت إزاي فعلاً |
| 10 | K (benchmark) | الحكم النهائي |

## 4. حاجات مش هتتغير

- فورمات الـ markdown (`### Q1:` …)، والـ 31-column schema، والـ tags. يعني الموديولات القديمة تفضل شغالة.
- الـ source files مابتتعدلش أبداً.
- `build_module_template.py` و`validate_questions_excel.py` و`audit_question_bank.py`: هنلفّهم بس، ومش هنعيد كتابتهم.
- الـ two-phase workflow بتاع الـ subcategories.
