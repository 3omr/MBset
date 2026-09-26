# مراجعة تعارضات الإجابات المكررة

تاريخ المراجعة: 2026-09-17

نطاق المراجعة: `/tmp/neuroscience_questions_payload_before_cleanup.json` وملفات Markdown المرتبطة داخل `Markdown_Questions/`. لم يتم تعديل أي ملف مصدر أو Excel. أرقام الأسطر أدناه تشير إلى النسخة الحالية من ملفات Markdown.

الـpayload يعلن **16 سجل تعارض**. السجلان 4 و5 متطابقان تمامًا في بيانات التعارض، لأن السؤال نفسه موجود مرتين في `20_M3WAN_Mid_30.md` (Q2 وQ5)، ولذلك فهما **حالة جوهرية واحدة مكررة في التقرير الآلي**. أتعامل أدناه مع كل سجل معلن، وأوضح التكرار صراحة.

## القرارات

### 1) Basilar membrane of the organ of Corti

- **السؤال:** `Which of the following statements best describes the basilar membrane of the organ of Corti?`
- **المواضع:** [18_M3WAN_Final_32.md، Q67](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/18_M3WAN_Final_32.md:819) — `C`, مصدر `key`؛ [19_M3WAN_Mid_Final_31.md، Q52](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/19_M3WAN_Mid_Final_31.md:683) — `A`, مصدر `key`.
- **الأقوى:** العبارة الطبية المشتركة: **the apex responds better to low frequencies than the base**؛ فالقاعدة أصلب وأنسب للترددات العالية، والقمة ألين وأنسب للترددات المنخفضة. هذا تؤيده [مراجعة تشريح الأذن الداخلية](https://www.ncbi.nlm.nih.gov/books/NBK538335/).
- **قرار الدمج المقترح:** **يُدمج** كسؤال واحد، ويُحفظ نص الإجابة لا حرفها؛ وإذا استُخدم ترتيب Q52 فالإجابة `A`. السبب أن `C` في Q67 و`A` في Q52 نفس العبارة الطبية، وQ52 يملك مجموعة اختيارات أكمل.

### 2) Active cells during CNS inflammation

- **السؤال:** `Active cells during inflammation of CNS is ?`
- **المواضع:** [17_M3WAN_Final_30.md، Q109](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/17_M3WAN_Final_30.md:1434) — `E`, مصدر `key`؛ [19_M3WAN_Mid_Final_31.md، Q83](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/19_M3WAN_Mid_Final_31.md:1082) — `C`, مصدر `key`. الاختيارات في الموضعين متطابقة؛ `E` = Both a & c.
- **الأقوى:** **Both astrocytes and microglia**. كلاهما يشارك في الاستجابة الالتهابية العصبية؛ انظر [مراجعة التفاعل بين microglia وastrocytes في neuroinflammation](https://pmc.ncbi.nlm.nih.gov/articles/PMC10556371/).
- **قرار الدمج المقترح:** **يُدمج** مع اعتماد الإجابة النصية `Both a & c`، أي `E` مع ترتيب الاختيارات الحالي. السبب أن مفتاح Q109 يطابق الاستنتاج الطبي، بينما `C` في Q83 يسقط astrocytes رغم وجودها ضمن الاختيار المركب الصحيح.

### 3) Opening of ligand-gated Cl− channels — payload record 3

- **السؤال:** `Opening of ligand-gated Cl− channels causes ?`
- **المواضع:** [18_M3WAN_Final_32.md، Q73](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/18_M3WAN_Final_32.md:890) — `D`, مصدر `key`؛ [19_M3WAN_Mid_Final_31.md، Q94](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/19_M3WAN_Mid_Final_31.md:1226) — `A`, مصدر `key`.
- **الأقوى:** **inhibition of the postsynaptic neuron**؛ فتح قنوات الكلوريد المُفعّلة بالربيطة يسبب تثبيطًا/تثبيتًا غشائيًا مثبطًا في هذا السياق.
- **قرار الدمج المقترح:** **يُدمج**، مع إعادة مطابقة `Correct` حسب نص الاختيار بعد أي إعادة ترتيب؛ `D` و`A` هنا لا يمثلان اختلافًا طبيًا.

### 4) Opening of ligand-gated Cl− channels — payload record 4

- **السؤال:** نفس سؤال البند 3.
- **المواضع:** [18_M3WAN_Final_32.md، Q73](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/18_M3WAN_Final_32.md:890) — `D`, `key`؛ [20_M3WAN_Mid_30.md، Q2](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/20_M3WAN_Mid_30.md:26) — `A`, `key`.
- **الأقوى:** **inhibition of the postsynaptic neuron**.
- **قرار الدمج المقترح:** **يُدمج** مع البندين 3 و5؛ لا يوجد تعارض في المعنى، بل اختلاف ترتيب للاختيارات.

### 5) Opening of ligand-gated Cl− channels — payload record 5

- **السؤال:** نفس سؤال البند 3.
- **المواضع:** [18_M3WAN_Final_32.md، Q73](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/18_M3WAN_Final_32.md:890) — `D`, `key`؛ [20_M3WAN_Mid_30.md، Q5](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/20_M3WAN_Mid_30.md:65) — `A`, `key`.
- **الأقوى:** **inhibition of the postsynaptic neuron**.
- **قرار الدمج المقترح:** **لا تُعامل كحالة طبية مستقلة**؛ Q5 نسخة مكررة من Q2 داخل الملف نفسه. يُحتفظ بنسخة واحدة من Q2/Q5، ثم تُدمج مع البندين 3 و4.

### 6) Coactivation of dynamic γ- and α-motor neurons

- **السؤال:** `When dynamic γ-motor neurons are activated at the same time as α-motor neurons to muscle ?`
- **المواضع:** [18_M3WAN_Final_32.md، Q74](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/18_M3WAN_Final_32.md:903) — `B`, مصدر `key`؛ [20_M3WAN_Mid_30.md، Q9](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/20_M3WAN_Mid_30.md:117) — `D`, مصدر `key`.
- **الأقوى:** **the number of impulses in spindle Ia afferents is greater than with α discharge alone**؛ تنشيط γ يحافظ على شد المغزل أثناء انقباض العضلة بواسطة α.
- **قرار الدمج المقترح:** **يُدمج**، مع اعتماد نص الإجابة وإعادة تعيين الحرف بعد repacking؛ `B` و`D` نفس الاختيار المعاد ترتيبه.

### 7) Primary mechanism of local anesthetics

- **السؤال:** `The primary mechanism of action of local anesthetics is ?`
- **المواضع:** [06_Final_2022.md، Q54](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/06_Final_2022.md:644) — `C`, مصدر `derived`؛ [20_M3WAN_Mid_30.md، Q69](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/20_M3WAN_Mid_30.md:924) — `B`, مصدر `key`.
- **الأقوى:** **blockade of voltage-gated sodium channels**؛ هذا هو آلية التخدير الموضعي الأساسية، وتؤيده [مراجعة التخدير الموضعي في طب الأسنان](https://pmc.ncbi.nlm.nih.gov/articles/PMC9275172/). مصدر Q69 المطبوع (`key`) أقوى من اشتقاق Q54، والاثنان متفقان في المعنى.
- **قرار الدمج المقترح:** **يُدمج** مع اعتماد نسخة Q69 أو الإجابة النصية، أي `B` إذا بقي ترتيب Q69. لا يُستخدم حرف `C` من Q54 بعد repacking لأنه يشير إلى نفس العبارة في ترتيب مختلف.

### 8) Primary cutaneous hyperalgesia

- **السؤال:** `Primary cutaneous hyperalgesia:`
- **المواضع:** [22_Midterm_2020.md، Q8](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/22_Midterm_2020.md:105) — `C`, مصدر `derived`؛ [24_Qs_bank_1.md، Q14](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/24_Qs_bank_1.md:210) — `B`, مصدر `derived`.
- **الأقوى:** لا يوجد اختيار وحيد آمن. طبيًا، primary hyperalgesia في موضع الإصابة تتضمن زيادة الألم أمام المنبه فوق العتبة وانخفاض عتبة الألم؛ لذلك `B` (تعريف الظاهرة) و`C` (تغير عتبة مستقبلات الألم) ليسا متناقضين. انظر [مراجعة peripheral neuronal hyperexcitability](https://pmc.ncbi.nlm.nih.gov/articles/PMC7586453/).
- **قرار الدمج المقترح:** **غير محسوم — يحتاج spot-check** لمفتاح المحاضرة/المصدر الأصلي. لا تُدمج النسختان كسؤال MCQ ذي إجابة واحدة قبل التحقق؛ لا يجوز اختراع ترجيح بين `B` و`C`.

### 9) Visceral pain

- **السؤال:** `Visceral pain:`
- **المواضع:** [18_M3WAN_Final_32.md، Q58](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/18_M3WAN_Final_32.md:709) — `B`, مصدر `key`؛ [24_Qs_bank_1.md، Q17](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/24_Qs_bank_1.md:255) — `D`, مصدر `derived`. Q49 في الملف 24 سؤال مختلف عن referred visceral pain وليس طرفًا إضافيًا لهذا التعارض.
- **الأقوى:** **مصدرّيًا: `B`** لأن Q58 يحمل مفتاحًا مطبوعًا، بينما `D` في Q17 مشتق بلا مفتاح. كما أن spasm/viscerosomatic reflex معروف، في حين أن visceral pain قد يسبب أيضًا autonomic/depressor responses؛ لذلك لا ينبغي تقديم الاختيار المشتق كتصحيح لمفتاح مطبوع دون دليل من المصدر. للمقارنة الطبية: [Neuroscience Online عن visceral pain](https://nba.uth.tmc.edu/neuroscience/s2/chapter07.html) و[مراجعة visceral pain](https://pmc.ncbi.nlm.nih.gov/articles/PMC3272481/).
- **قرار الدمج المقترح:** **يُدمج مصدرّيًا مع الاحتفاظ بـ`B`**، وتُسجل ملاحظة أن صياغة السؤال واسعة وقد تكون ملتبسة طبيًا. لا يُستبدل مفتاح `key` بـ`D` المشتق إلا إذا أثبت spot-check للمصدر الأصلي أن السؤال كان يقصد autonomic depressor response تحديدًا.

### 10) Temporal summation — payload record 10

- **السؤال:** `Temporal summation:` / `Temporal summation ?`
- **المواضع:** [19_M3WAN_Mid_Final_31.md، Q95](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/19_M3WAN_Mid_Final_31.md:1239) — `B`, مصدر `key`؛ [25_Qs_bank_2.md، Q21](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/25_Qs_bank_2.md:299) — `A`, مصدر `derived`. Q15 وQ34 في الملف 25 صيغتا True/False موسعتان للمفهوم نفسه وإجابتهما `A`.
- **الأقوى:** **repeated/successive stimulation of a single presynaptic fiber/terminal within a short time**. هذا هو تعريف temporal summation، كما يشرح [NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK26910/).
- **قرار الدمج المقترح:** **يُدمج** كسؤال مفهوم واحد، مع اعتماد الإجابة النصية؛ `B` في Q95 و`A` في Q21 اختلاف ترتيب/صياغة، وQ15/Q34 داعمان لنفس الإجابة.

### 11) Amide local anesthetic

- **السؤال:** `Which one of the following local anesthetics is amide one?`
- **المواضع داخل الملف نفسه:** [27_Pharmacology_Qs_bank.md، Q45](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/27_Pharmacology_Qs_bank.md:585) — `A`, مصدر `marked`؛ Q70 — `C`, مصدر `marked`.
- **الأقوى:** **Lidocaine**؛ هو مخدر موضعي من نوع amide، بينما procaine/tetracaine/benzocaine من ester-type في هذه المجموعة. يؤيد ذلك [مرجع التخدير الموضعي في طب الأسنان](https://pmc.ncbi.nlm.nih.gov/articles/PMC9275172/).
- **قرار الدمج المقترح:** **يُدمج** Q45 وQ70، ويُحفظ الاختيار النصي `Lidocaine` لا الحرف؛ `A` و`C` صحيحان فقط بالنسبة لترتيبين مختلفين للاختيارات.

### 12) Local anesthetic used mainly for dental procedures

- **السؤال:** `The local anesthetics that used mainly for dental procedures is:`
- **المواضع داخل الملف نفسه:** [27_Pharmacology_Qs_bank.md، Q39](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/27_Pharmacology_Qs_bank.md:507) — `B`, مصدر `marked`؛ Q71 — `D`, مصدر `marked`.
- **الأقوى:** **Articaine**؛ كلا المفتاحين يشيران إلى articaine، مع اختلاف ترتيب الاختيارات. Articaine مستخدم على نطاق واسع في طب الأسنان؛ انظر [مراجعة articaine](https://pmc.ncbi.nlm.nih.gov/articles/PMC3417979/).
- **قرار الدمج المقترح:** **يُدمج** Q39 وQ71 مع اعتماد النص `Articaine` وإعادة توليد الحرف بعد توحيد الاختيارات.

### 13) Epinephrine added to local anesthetics

- **السؤال:** `Epinephrine added to local anesthetics to:`
- **المواضع داخل الملف نفسه:** [27_Pharmacology_Qs_bank.md، Q54](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/27_Pharmacology_Qs_bank.md:702) — `B`, مصدر `marked`؛ Q73 — `A`, مصدر `marked`؛ Q86 — `B`, مصدر `marked`.
- **الأقوى:** لا يوجد اختيار وحيد عند دمج الصيغ الحالية: **increase the concentration at the site of action** و**prolong the duration of action** نتيجتان صحيحتان لتقبض الأوعية وإبطاء الامتصاص الجهازي. يؤيد ذلك [DailyMed عن articaine/epinephrine](https://dailymed.nlm.nih.gov/dailymed/fdaDrugXsl.cfm?setid=4524cb96-40f7-471f-bfc6-1dcab47628ec) و[مراجعة التخدير الموضعي](https://pmc.ncbi.nlm.nih.gov/articles/PMC9275172/).
- **قرار الدمج المقترح:** **غير محسوم — يحتاج spot-check** للمصدر الأصلي لمعرفة المقصود التعليمي، أو إعادة صياغة السؤال/الاختيارات قبل الدمج. لا يُفرض `A` أو `B` على النسخ الثلاث؛ فكل منهما مدعوم طبيًا في صياغته الحالية.

### 14) Temporal summation — payload record 14

- **السؤال:** `Temporal Summation:`
- **المواضع:** [19_M3WAN_Mid_Final_31.md، Q95](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/19_M3WAN_Mid_Final_31.md:1239) — `B`, مصدر `key`؛ [28_Physiology_Qs_bank_MCQ.md، Q10](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/28_Physiology_Qs_bank_MCQ.md:139) — `D`, مصدر `marked`.
- **الأقوى:** **repeated stimulation of a single presynaptic fiber at a high rate**؛ هذا نفس تعريف البند 10.
- **قرار الدمج المقترح:** **يُدمج** مع البند 10؛ `B` و`D` اختلاف ترتيب، ولا يوجد خلاف طبي.

### 15) Spatial summation

- **السؤال:** `Spatial summation:`
- **المواضع:** [22_Midterm_2020.md، Q12](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/22_Midterm_2020.md:157) — `A`, مصدر `derived`؛ [28_Physiology_Qs_bank_MCQ.md، Q11](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/28_Physiology_Qs_bank_MCQ.md:153) — `C`, مصدر `marked`.
- **الأقوى:** **simultaneous inputs from several presynaptic neurons/afferents converging on the same postsynaptic neuron**؛ هذا هو spatial summation، مقابل temporal summation من ليف واحد عبر الزمن. يؤيده [NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK26910/).
- **قرار الدمج المقترح:** **يُدمج** مع اعتماد النص؛ `A` و`C` نفس الفكرة بصياغة وترتيب مختلفين. مصدر Q11 `marked` أقوى من اشتقاق Q12.

### 16) Intracranial headache

- **السؤال:** `Intracranial headache could result from painful stimuli applied on :-`
- **المواضع:** [24_Qs_bank_1.md، Q18](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/24_Qs_bank_1.md:270) — `A`, مصدر `derived`؛ [28_Physiology_Qs_bank_MCQ.md، Q18](</home/omar/MBset/اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions/28_Physiology_Qs_bank_MCQ.md:256) — `C`, مصدر `marked`.
- **الأقوى:** لا يوجد اختيار وحيد في الاختيارات الحالية: **parts of dura** و**large intracranial venous sinuses/veins** كلاهما من البنى الحساسة للألم، بينما brain tissue وarachnoid غير مناسبين عادةً. انظر [NCBI Clinical Methods عن Headache](https://www.ncbi.nlm.nih.gov/books/NBK377/).
- **قرار الدمج المقترح:** **غير محسوم — يحتاج spot-check وتصحيحًا لصياغة السؤال**؛ لا تُدمج النسختان كسؤال single-best-answer قبل إزالة تعدد الإجابات الصحيحة أو إثبات أن المصدر الأصلي يقصد أحد الخيارين تحديدًا.

### 17) Analgesia-system wording variant introduced by source #2

- **السؤال:** `Which of the following is not part of the analgesia system?`
- **المواضع:** source #2 composite, the Final 2022 MCQ copy; `14_Mid_Formatives.md`, Q20.
- **الملاحظة:** النسختان تستخدمان اختيارات مختلفة، لكن كل منهما يحتوي على بنية ليست جزءًا من descending analgesia system (`dorsal column-medial lemniscal system` في الأولى، و`lateral spinothalamic tract` في الثانية).
- **قرار الدمج:** تُعامل كنسخة صياغة/اختيارات مختلفة تحت مراجعة، ويُحتفظ بنسخة source #2 في الـnormalized master حسب ترتيب الدمج مع عدم تغيير مفتاح المصدر.

## الخلاصة العددية

- **حالات التعارض المحسومة:** **12 من 15 حالة جوهرية**.
- **حالات التعارض غير المحسومة وتحتاج spot-check:** **3 حالات جوهرية**: البنود 8 و13 و16. وتضاف حالة الصياغة المختلفة في البند 17 كتحذير مراجعة غير حاجب.
- **بحساب سجلات الـpayload حرفيًا:** **13 من 16 سجلًا حُسمت** و**3 من 16 سجلًا غير محسومة**؛ البند 5 سجل مكرر للبند 4 وليس حالة طبية إضافية.

بعد دمج النسخ ذات الاختيارات المعاد ترتيبها، يعرض الـpayload النهائي **12 سجل مراجعة غير حاجب** و**0 hard conflicts**؛ التفاصيل المصدرية أعلاه محفوظة للمراجعة اليدوية قبل أي تعديل لاحق للمفاتيح.
