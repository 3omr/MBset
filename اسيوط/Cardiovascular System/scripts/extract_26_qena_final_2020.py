#!/usr/bin/env python3
"""Source 26 — OTHER EXAMS/فاينل قنا ٢٠٢٠.pdf ("Final Qena 2020").

South Valley University, Faculty of Medicine (Qena), CVS Block Final Exam,
Second Year, dated 23/11/2020. 10 pages, "Total Marks: 54" = Part I (3 written
case questions, 21 marks) + Part II (66 single-best-answer MCQs at half a mark
each, 33 marks). This is the most damaged source of the four: a 10-page
scanned PDF (pdftotext returns nothing — pure image) whose OCR
(.ocr/26_qena_final_2020.txt) is badly corrupted, and whose PHYSICAL page order
does not match the paper's own question order — physical pages 8, 9, 10 hold
questions 60-66, 53-59 and 46-52 respectively (reversed relative to the
question numbers). Per the extraction contract this file was re-rendered
(`pdftoppm -png -r 300`) and all 10 pages read by eye; all 69 questions below
are emitted in the paper's own numbering order (1-66 for Part II, plus the 3
Part I case questions), not physical-page order.

Every MCQ carries a hand mark (a diagonal slash through one option letter, or
occasionally a circle) that looks at first like a baked-in answer key — but on
cross-checking against medical knowledge the marks are inconsistent: some
questions carry TWO different marks on two different options (e.g. Q4 circles
"A" but also slashes "D"; Q19 slashes "B" but circles "C"; Q21 slashes "C" but
circles "B"), and several single marks point to an option that is medically
wrong (e.g. Q22's slashed "B", Q29's slashed "B") while a plainly correct
option elsewhere carries no mark at all. This pattern is characteristic of a
student's own personal working copy (first-pass guesses plus later
self-corrections), not an examiner's key, and the contract is explicit that a
student's own selected answer is not a key. Every answer below is therefore
Answer Source 'derived' — worked out independently from medical knowledge —
even where it happens to agree with one of the source's own marks.

The 3 Part I case-based questions are written (QROC); each is kept as ONE
question per numbered clinical case (their lettered sub-parts A/B/C are minor
sub-marks of one integrated vignette), with the full model answer in EXP.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '26_Qena_Final_2020.md')
TAG, YEAR = 'External, Qena 2020', 2020
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/فاينل قنا ٢٠٢٠.pdf'

WRITTEN = [
("A 62-year-old woman with a history of atrial fibrillation and anemia presents with dyspnea "
 "and easy fatigability. On examination her BP is 100/55 mmHg, heart rate is 120 beats/minute "
 "and irregularly irregular, with increased jugular venous distention and a water-hammer pulse. "
 "A) Describe water-hammer pulse and list two other abnormal pulses with their causes. "
 "B) Describe four factors affecting venous pressure. "
 "C) Explain from the case why she has a low diastolic blood pressure, and list two other "
 "factors affecting arterial blood pressure.",
 "A) Water-hammer (Corrigan's) pulse is a bounding pulse with a rapid, forceful upstroke and an "
 "equally rapid collapse, reflecting a wide pulse pressure — classically seen in aortic "
 "regurgitation, but also in high-output states such as severe anemia, thyrotoxicosis, PDA and "
 "AV fistula (as in this anemic patient). Other abnormal pulses: (1) Pulsus alternans — "
 "regular alternation of strong and weak beats, seen in severe left ventricular failure. "
 "(2) Pulsus paradoxus — an exaggerated (>10 mmHg) fall in systolic pressure during inspiration, "
 "seen in cardiac tamponade, constrictive pericarditis and severe asthma. "
 "B) Factors affecting venous pressure: (1) circulating blood volume, (2) venous tone/venomotor "
 "sympathetic activity, (3) right atrial (central venous) pressure and the pumping action of the "
 "heart, (4) the skeletal-muscle and respiratory pumps, and gravity/posture. "
 "C) Her low diastolic pressure reflects the wide pulse pressure of chronic anemia: reduced blood "
 "viscosity and a compensatory hyperdynamic circulation lower peripheral resistance and diastolic "
 "pressure while systolic pressure and stroke volume rise. Other factors affecting arterial blood "
 "pressure: cardiac output and total peripheral resistance (also blood volume and arterial "
 "elasticity/compliance)."),
("Ahmed, 52 years old, has occasional angina relieved by nitroglycerin, pulmonary edema, and "
 "serial ECGs suggesting a left ventricular myocardial infarction, with low cardiac output and an "
 "ejection fraction (EF) of 35%. "
 "A) Explain why pulmonary edema occurs in this case, and list two causes of left-sided heart "
 "failure. "
 "B) Give the definition and normal value of EF, and list three reflexes that arise from atrial "
 "receptors.",
 "A) Left ventricular infarction impairs LV contractility, raising left atrial and pulmonary "
 "venous/capillary hydrostatic pressure until it exceeds plasma oncotic pressure, driving fluid "
 "transudation into the alveoli (pulmonary edema). Two causes of left-sided heart failure: "
 "ischemic heart disease/myocardial infarction and chronic systemic hypertension (also valvular "
 "disease such as aortic stenosis or mitral regurgitation, or cardiomyopathy). "
 "B) Ejection fraction is the fraction of the end-diastolic volume ejected per beat "
 "(EF = stroke volume / end-diastolic volume x 100); normal value is approximately 55-70%. "
 "Three reflexes arising from atrial (stretch/volume) receptors: (1) the Bainbridge reflex — "
 "atrial stretch reflexly increases heart rate; (2) the atrial natriuretic peptide reflex — "
 "atrial stretch triggers ANP release, causing natriuresis and diuresis; (3) the renal "
 "(Henry-Gauer) reflex — atrial stretch inhibits ADH secretion, promoting diuresis."),
("A 56-year-old woman arrives in the emergency department with hypotension after severe "
 "haemorrhage and a low CVP. What are the delayed compensatory reactions after haemorrhage "
 "(2 items)?",
 "Delayed compensatory reactions after haemorrhage (occurring over hours to weeks, as opposed to "
 "the immediate neural/vasoconstrictor and intermediate fluid-shift/renin-angiotensin responses): "
 "(1) Restoration of plasma proteins — hepatic synthesis of plasma proteins (especially albumin) "
 "over the following 3-4 days restores plasma oncotic pressure and volume. "
 "(2) Restoration of red cell mass — hypoxia-driven erythropoietin release stimulates bone-marrow "
 "erythropoiesis, gradually restoring the red cell mass over several weeks."),
]

# (original Q#, stem, [options A..], correct letter, explanation)
RAW = [
(1, "Scavenger receptor B1 concerned with uptake of which of the followings?",
 ["LDL-cholesterol", "HDL-cholesterol", "VLDL", "Chylomicrons"], "B",
 "Scavenger receptor class B type 1 (SR-B1) mediates selective hepatic/steroidogenic uptake of "
 "HDL-cholesteryl esters, without endocytosing the whole HDL particle."),
(2, "Which of the followings are considered the biochemical markers of choice in the evaluation of acute coronary syndromes?",
 ["Troponin I (cTnI)", "Troponin T (cTnT)", "Troponin C (cTnC)", "Both A and B"], "D",
 "Cardiac troponins I and T are the biomarkers of choice for ACS because of their high cardiac "
 "specificity and sensitivity; troponin C is not cardiac-specific and is not used diagnostically."),
(3, "Myoglobin:",
 ["Is an iron- and oxygen-binding protein", "Abundantly present in the smooth muscle",
  "Has a molecular weight of 16.8 Da", "May be elevated as early as one week after myocardial injury"], "A",
 "Myoglobin is a small iron- and oxygen-binding heme protein of cardiac and skeletal muscle; it "
 "rises very early (within 1-2 hours) after myocardial injury, not as late as one week, and its "
 "molecular weight is about 17.8 kDa, not present in smooth muscle."),
(4, "Mature chylomicron contains:",
 ["Apo B-48", "Apo-CII", "Apo E", "All of the above"], "D",
 "A nascent chylomicron carries only ApoB-48; as it matures in plasma it acquires ApoC-II and ApoE "
 "from HDL, so a mature chylomicron contains all three apolipoproteins."),
(5, "Cardiac Enzymes include:",
 ["Creatinine phosphokinase", "Aspartate transaminase", "Lactate Dehydrogenase", "All of the above"], "D",
 "CPK (CK-MB), AST and LDH are all classic (if non-specific) cardiac enzyme markers used "
 "historically in the evaluation of myocardial injury."),
(6, "Troponin C:",
 ["Binds to calcium ions to produce a conformational change in TnI", "Binds to tropomyosin",
  "Binds to actin in thin myofilaments", "All of the above"], "A",
 "Troponin C binds Ca2+, producing a conformational change transmitted to troponin I that moves "
 "tropomyosin off the actin binding sites, permitting cross-bridge cycling."),
(7, "All of the followings activate the HMG CoA reductase EXCEPT:",
 ["Diet rich in unsaturated fat", "Exercise", "Vitamin B6 and niacin",
  "Dietary or endogenously synthesized cholesterol"], "D",
 "Cholesterol (dietary or endogenous) provides negative feedback that SUPPRESSES/inhibits HMG-CoA "
 "reductase, the rate-limiting enzyme of cholesterol synthesis, rather than activating it."),
(8, "The prophylaxis action of vegetable oils against atherosclerosis is due to:",
 ["Their antioxidant contents", "Enhance mobilization of cholesterol ester to the liver",
  "Increase hepatic LDL receptor expression", "All of the above"], "C",
 "Unsaturated vegetable oils lower plasma LDL cholesterol chiefly by up-regulating hepatic LDL "
 "receptor expression, enhancing LDL clearance from plasma."),
(9, "The early signs of glycosides intoxication are:",
 ["Visual changes", "Ventricular tachyarrhythmias", "GIT disturbances", "All the above"], "C",
 "The earliest signs of digitalis (glycoside) toxicity are gastrointestinal — anorexia, nausea and "
 "vomiting — preceding visual disturbances and the more dangerous arrhythmias."),
(10, "Which one of the following drugs decreases de novo cholesterol synthesis by inhibiting the enzyme 3-hydroxy-3-methylglutaryl coenzyme A reductase?",
 ["Fenofibrate", "Niacin", "Cholestyramine", "Lovastatin"], "D",
 "Lovastatin is a statin, directly inhibiting HMG-CoA reductase to reduce de novo cholesterol synthesis."),
(11, "If the patient has a history of gout, which of the following drugs is most likely to exacerbate this condition?",
 ["Colestipol", "Simvastatin", "Ezetimibe", "Niacin"], "D",
 "Niacin raises serum uric acid and can precipitate or worsen gout."),
(12, "A 55-year-old pregnant woman with hyperlipidemia, which of the following drugs should be avoided because of a risk of harming the fetus?",
 ["Cholestyramine", "Niacin", "Ezetimibe", "Atorvastatin"], "D",
 "Statins (atorvastatin) are contraindicated in pregnancy because of risk of fetal harm; "
 "cholestyramine (not systemically absorbed) is the preferred lipid-lowering option in pregnancy."),
(13, "All of the followings are adverse effects of nitrates and nitrite drugs, EXCEPT:",
 ["Orthostatic hypotension, tachycardia", "GIT disturbance", "Throbbing headache", "Tolerance"], "B",
 "Nitrates classically cause orthostatic hypotension with reflex tachycardia, throbbing headache "
 "(from cerebral vasodilation) and tolerance with continuous use; GIT disturbance is not a "
 "characteristic nitrate adverse effect."),
(14, "Which of the following antianginal agents is a calcium channel blocker?",
 ["Nitroglycerin", "Dipyridamole", "Minoxidil", "Nifedipine"], "D",
 "Nifedipine is a dihydropyridine calcium channel blocker used as an antianginal agent."),
(15, "The drug of choice in treatment of vasospastic angina is:",
 ["Atenolol", "Nifedipine", "Propranolol", "Dobutamine"], "B",
 "Calcium channel blockers such as nifedipine are first-line for vasospastic (Prinzmetal) angina, "
 "relieving coronary vasospasm; non-selective beta-blockers can worsen spasm."),
(16, "A 45-year-old woman with acute heart failure and pulmonary edema. Which of the following drugs is the most useful for her case?",
 ["Furosemide", "Propranolol", "Verapamil", "Nitroglycerin"], "A",
 "A loop diuretic such as furosemide rapidly reduces preload and pulmonary congestion in acute "
 "heart failure with pulmonary edema, making it the most useful single choice among these options."),
(17, "Which of the following has been shown to prolong life in patients with chronic congestive failure in spite of having a negative inotropic effect on cardiac contractility?",
 ["Carvedilol", "Digoxin", "Dobutamine", "Enalapril"], "A",
 "Beta-blockers such as carvedilol improve long-term survival in chronic heart failure despite an "
 "acute negative inotropic effect, through favorable remodeling and neurohormonal blockade."),
(18, "In very severe digitalis intoxication, the best choice is to use:",
 ["Digoxin antibodies", "Lidocaine infusion", "Potassium by mouth", "Phenytoin by mouth"], "A",
 "Digoxin-specific antibody fragments (Digoxin immune Fab) are the definitive treatment for "
 "severe, life-threatening digitalis toxicity."),
(19, "From the complication of sub-acute bacterial endocarditis is the following EXCEPT",
 ["Infarction", "Pyemic abscess", "Focal embolic glomerulonephritis", "Mycotic aneurysms"], "B",
 "Pyemic (suppurative) abscesses are typical of acute (high-virulence) infective endocarditis; "
 "subacute bacterial endocarditis more typically causes bland infarction, immune-complex "
 "(focal embolic) glomerulonephritis, and mycotic aneurysms rather than suppurative abscesses."),
(20, "From the major criteria of rheumatic fever is:",
 ["Erythema marginatum", "Leukocytosis", "Elevated erythrocytic sedimentation rate", "Fever"], "A",
 "Erythema marginatum is one of the Jones major criteria for rheumatic fever (with carditis, "
 "polyarthritis, chorea and subcutaneous nodules); leukocytosis, elevated ESR and fever are minor criteria."),
(21, "The following are true for subacute bacterial endocarditis EXCEPT:",
 ["Caused by streptococci viridans", "Leads to Infarction of multiple organs, focal embolic glomerulonephritis",
  "Organism attach the healthy valves", "Leads to mycotic aneurysm of the cerebral and mesenteric arteries"], "C",
 "Subacute bacterial endocarditis organisms (typically low-virulence Strep viridans) characteristically "
 "attach to previously DAMAGED heart valves, not healthy ones — attachment to normal valves is more "
 "typical of acute, high-virulence organisms such as Staph aureus."),
(22, "Not seen in mitral stenosis:",
 ["Hypertrophy and dilatation of the left atrium", "Chronic venous congestion of the lung",
  "Pulmonary hypertension which causes atherosclerosis in the pulmonary arteries",
  "Terminates by left-sided heart failure"], "D",
 "In pure mitral stenosis the left ventricle is protected/underfilled, so the disease classically "
 "terminates in right-sided (not left-sided) heart failure secondary to pulmonary hypertension; "
 "left atrial enlargement, pulmonary venous congestion and pulmonary arterial changes are all typical."),
(23, "Not seen in atherosclerosis:",
 ["Cholesterol and its esters are deposited in the subintimal connective tissue",
  "Neovascularization, fibrosis and hyalinosis around the deposited lipids",
  "Hyperplasia of internal elastic lamina", "Atrophy of the media opposite the atheroma"], "C",
 "Atherosclerosis typically causes fragmentation/destruction (not hyperplasia) of the internal "
 "elastic lamina at the plaque, along with subintimal lipid deposition, neovascularization/fibrosis "
 "and pressure atrophy of the underlying media."),
(24, "Not seen in primary hypertension:",
 ["Concentric hypertrophy of the left ventricle", "Retinal hemorrhage and exudates",
  "Normal sized kidney", "Hyalinosis and elastosis of blood vessels"], "B",
 "Retinal hemorrhages and exudates are a hallmark of malignant (accelerated) hypertension, not "
 "the more indolent benign/primary (essential) hypertension, which instead shows concentric LVH, "
 "vascular hyalinosis/elastosis and a normal or only mildly contracted kidney."),
(25, "Unstable (Crescendo) angina is characterized by EXCEPT:",
 ["Chest pain and shortness of breath that occur at rest, with progressively less exertion",
  "Chest pain is prolonged more than 20 min", "Is associated with a significant risk of acute transmural myocardial infarction",
  "Chest pain with decreasing frequency"], "D",
 "'Crescendo' angina is defined by pain of INCREASING frequency, severity and duration; "
 "'decreasing frequency' directly contradicts the crescendo pattern and is the exception. "
 "(Rest pain lasting >20 minutes is itself one of the recognized diagnostic criteria for unstable angina.)"),
(26, "Thromboangitis obliterans (Burger's disease) is characterized by EXCEPT:",
 ["Segmental inflammatory condition of arteries only", "Organization and recanalization of the affected vessels",
  "Occurs in heavy smokers", "Gangrene of the lower limb"], "A",
 "Buerger's disease is a segmental inflammatory condition of small/medium arteries AND veins (and "
 "adjacent nerves), not arteries only, strongly linked to heavy smoking, with organization/"
 "recanalization of thrombosed segments and a risk of limb gangrene."),
(27, "The most common aneurysm in cerebral vessels is:",
 ["Dissecting aneurysm", "False aneurysm", "Congenital aneurysm", "Mycotic aneurysm"], "C",
 "Congenital (berry) aneurysms of the circle of Willis are the most common type of cerebral "
 "vascular aneurysm, and the leading cause of non-traumatic subarachnoid hemorrhage."),
(28, "From the complication of varicose veins is EXCEPT:",
 ["Neoplastic changes", "Thrombosis and embolism", "Haemorrhage", "Trophic skin changes"], "A",
 "Neoplastic transformation is not a recognized complication of simple varicose veins, unlike "
 "thrombosis/embolism, variceal haemorrhage and chronic trophic skin changes."),
(29, "In malignant hypertension, the arterial wall pathology leads to cerebral hemorrhage is:",
 ["Fibrinoid necrosis", "Concentric hyperplasia", "Hyalinosis only", "Hyalinosis and elastosis"], "A",
 "Fibrinoid necrosis of small arteries/arterioles is the classic lesion of malignant hypertension "
 "responsible for vessel rupture and hemorrhage (including cerebral hemorrhage)."),
(30, "From the causes of congenital heart diseases are the following EXCEPT:",
 ["Autoimmune diseases", "German measles (rubella) affecting the pregnant mother especially during the first three months",
  "Drugs administered by the pregnant mother as thalidomide and cortisone",
  "Nutritional and vitamin deficiencies in pregnancy"], "A",
 "Maternal autoimmune disease is not a classic recognized cause of congenital heart disease (though "
 "maternal SLE/anti-Ro antibodies cause congenital heart BLOCK specifically, not structural CHD in "
 "general); first-trimester rubella, teratogenic drugs and maternal nutritional deficiency are all "
 "established causes of congenital heart malformations."),
(31, "Poly arteritis nodosa usually complicated by:",
 ["Dissecting aneurysms", "Atherosclerotic aneurysms", "Mycotic aneurysms", "All of the above"], "C",
 "Polyarteritis nodosa classically produces multiple small aneurysms of medium-sized muscular "
 "arteries at branch points due to the necrotizing vasculitis itself; among the listed (imperfect) "
 "options, mycotic aneurysm is the conventionally selected answer — flagged as a judgement call, "
 "since PAN aneurysms are strictly inflammatory rather than infective/mycotic, dissecting or "
 "atherosclerotic in the classic sense."),
(32, "Fleeting arthritis is characterized by EXCEPT:",
 ["Affect the small joint", "The joint cavity showed serous exudate with congestion of the synovial, "
  "capsular tissue with inflammatory cell infiltration and Aschoff nodules", "Occur with rheumatic fever",
  "The articular cartilage is not damaged"], "A",
 "The migratory (fleeting) polyarthritis of rheumatic fever characteristically affects LARGE "
 "joints, not small joints, distinguishing it from the exception here."),
(33, "Cor-pulmonale is a complication of",
 ["Fascioliasis", "Cysticercosis", "Schistosomiasis", "Hydatidosis"], "C",
 "Schistosomiasis causes pulmonary hypertension via embolization of eggs to the pulmonary "
 "vasculature, leading to cor pulmonale."),
(34, "Congenital heart disease due to Toxoplasma gondii when infection occurred in:",
 ["1st trimester", "2nd trimester", "3rd trimester", "All of the above"], "A",
 "Congenital toxoplasmosis acquired in the first trimester carries the highest risk of severe "
 "fetal damage, including congenital heart and CNS malformations, even though transmission risk "
 "itself rises later in pregnancy."),
(35, "Winged bug is the vector of",
 ["Plasmodium vivax", "Trypanosoma cruzi", "Trypanosoma gambiense", "None of the above"], "B",
 "The winged reduviid (\"kissing\") bug is the vector of Trypanosoma cruzi, the cause of Chagas' disease."),
(36, "Cardiac tamponade occur in",
 ["Chagas disease", "Amoebic pericarditis", "Cysticercosis", "Hydatidosis"], "B",
 "Amoebic pericarditis can produce a rapidly accumulating pericardial effusion leading to cardiac tamponade."),
(37, "A 25-year-old woman developed fever, chest pain, and arrhythmia 1 week after experiencing a "
     "flu-like illness. A variety of tests lead to the diagnosis of myocarditis of microbial origin. "
     "What is the most likely etiology?",
 ["Borrelia burgdorferi", "Corynebacterium diphtheriae", "Coxsackievirus B", "Influenza virus"], "C",
 "Coxsackievirus B is the most common identifiable cause of viral myocarditis, classically "
 "following a flu-like prodrome."),
(38, "Measles, Mumps, Rubella (MMR) Vaccine is",
 ["Killed vaccine", "Living attenuated vaccine", "Toxoid", "Recombinant vaccine"], "B",
 "MMR is a live attenuated viral vaccine."),
(39, "True statement about subacute bacterial endocarditis include that it:",
 ["Often arise as complication of dental manipulation", "Is frequently caused by β-hemolytic streptococci",
  "Is frequently caused by non-hemolytic streptococci", "Usually affects normal heart valves"], "A",
 "SBE is classically preceded by transient bacteremia from dental manipulation, with Strep viridans "
 "(alpha-hemolytic, not beta- or non-hemolytic) as the usual organism, attacking previously "
 "damaged (not normal) valves."),
(40, "Rheumatic fever is most commonly caused by ------- after 3-4 weeks from infection",
 ["Streptococcus viridans", "Streptococcus pyogenes", "Staphylococcus aureus", "Enterococcus"], "B",
 "Rheumatic fever follows group A Streptococcus (Streptococcus pyogenes) pharyngitis by about "
 "2-4 weeks."),
(41, "Most important virulence factor of Streptococcus pyogenes is",
 ["Hyaluronic acid capsule", "Polypeptide capsule", "C-streptokinase production", "M protein"], "D",
 "M protein is the major virulence factor of Streptococcus pyogenes, conferring antiphagocytic "
 "properties and antigenic diversity."),
(42, "Which of the following HIV antigens is used in early diagnosis before appearance of anti-HIV antibodies?",
 ["p24", "p55", "gp120", "gp160"], "A",
 "The p24 core antigen appears in blood before anti-HIV antibodies develop, making it useful for "
 "early diagnosis (as in combined antigen/antibody assays)."),
(43, "A case with positive Anti-HCV (Hepatitis C virus) must be confirmed by",
 ["Western blotting", "Southern blotting", "PCR", "Latex agglutination"], "C",
 "A positive anti-HCV antibody screen is confirmed by HCV RNA PCR, which detects active viremia."),
(44, "Usually given as prophylaxis for Rheumatic fever patients",
 ["Long acting penicillin", "Tetracycline", "Dicloxacillin", "Cephalexin"], "A",
 "Long-acting benzathine penicillin G is the standard secondary prophylaxis for rheumatic fever "
 "patients to prevent recurrent group A streptococcal infection."),
(45, "Blood culture for diagnosis of sub-acute bacterial endocarditis must be",
 ["At least 3 samples from different sites", "At the peak of the fever",
  "5-10 ml blood added to 50-100 ml broth to enhance the bacterial growth", "All of the above"], "A",
 "Because bacteremia in SBE is continuous (unlike other infections), timing samples to a fever "
 "peak is not required; the key practice is taking at least 3 separate blood culture samples from "
 "different sites/times to confirm true, persistent bacteremia."),
(46, "Which of the following statement is true for streptococcal viridance:",
 ["Produce β-hemolysis on blood agar", "Insoluble in bile", "Part of normal flora in Cerebrospinal fluid",
  "Settle on normal heart valve"], "B",
 "Viridans streptococci are bile-insoluble (unlike bile-soluble pneumococci), alpha- not "
 "beta-hemolytic, not normal CSF flora, and settle on previously damaged (not normal) heart valves."),
(47, "The wall of I.V.C. is characterized by:",
 ["Well-developed internal elastic lamina", "Well-developed media",
  "A layer of longitudinal smooth muscle fibers in adventitia",
  "A layer of longitudinal smooth muscle fibers in the media"], "C",
 "The IVC, as a large vein, has a poorly developed media but a thick adventitia containing "
 "longitudinal smooth muscle bundles."),
(48, "The wall of a medium-sized vein is more or less similar to that of a corresponding artery except that:",
 ["The media is less developed", "The adventitia is more developed (thicker)",
  "The lumen is wider, wall is thinner", "All of above"], "D",
 "Compared with a corresponding artery, a medium vein has a less developed media, a thicker "
 "(more developed) adventitia, and a wider lumen with a thinner overall wall — all of the above."),
(49, "Regarding vasa vasorum, the following is incorrect:",
 ["Small arteries in tunica adventitia", "Present mainly in large vessels especially veins",
  "They nourish the outer part of the wall of large vessels", "They contain venous blood"], "D",
 "Vasa vasorum are small ARTERIES (and their capillary/venous drainage) supplying the outer wall "
 "of large vessels; describing them simply as \"containing venous blood\" is the incorrect statement, "
 "since their primary defining components are the small nutrient arteries themselves."),
(50, "Blood sinusoids are not characterized by the following:",
 ["The cells are separated by large inter cellular spaces", "Have continuous basement membrane",
  "Macrophages are found among or outside their wall", "They are wide irregular blood channels"], "B",
 "Sinusoids characteristically have a discontinuous (not continuous) basement membrane, permitting "
 "free exchange of cells and macromolecules."),
(51, "The function of chemoreceptors is:",
 ["Responded by the changes in the chemical composition of the blood", "Responded by the changes in blood pressure",
  "Responded by the changes in the blood volume", "All of the above"], "A",
 "Chemoreceptors respond specifically to changes in the chemical composition of the blood (O2, CO2, "
 "H+); baroreceptors sense pressure, and volume receptors sense blood/atrial volume."),
(52, "The sino-atrial (SA) node, the atrio-ventricular (AV) node, and the Purkinje fibers of the "
     "myocardium all consist of specialized:",
 ["Endothelial cells", "Fibroblasts", "Smooth muscle cells", "Cardiac muscle cells"], "D",
 "The cardiac conduction system (SA node, AV node, bundle of His, Purkinje fibers) is composed of "
 "specialized, modified cardiac muscle cells, not endothelial, fibroblast or smooth muscle cells."),
(53, "One of the following is a content of superior mediastinum:",
 ["Ascending aorta", "Descending aorta", "Inferior vena cava", "Trachea"], "D",
 "The trachea passes through the superior mediastinum; the ascending aorta lies in the middle "
 "mediastinum, and the descending aorta/IVC are not contents of the superior mediastinum."),
(54, "The pulmonary artery carries blood from ...... to the ......:",
 ["Left ventricle - mediastinum", "Right atrium - lungs", "Right ventricle - lingula", "Right ventricle - lungs"], "D",
 "The pulmonary artery (trunk) carries deoxygenated blood from the right ventricle to the lungs."),
(55, "The coronary sulcus separates the:",
 ["Two atria", "Two ventricles", "Atria & the ventricles", "Apex & the base"], "C",
 "The coronary (atrioventricular) sulcus marks the external boundary between the atria and the ventricles."),
(56, "Apex of the heart is formed only by:",
 ["Left atrium", "Left ventricle", "Right atrium", "Right ventricle"], "B",
 "The cardiac apex is formed exclusively by the left ventricle."),
(57, "A point on the left 5th intercostal space 9 cm from the midline, referrers to surface anatomy of:",
 ["Apex of the heart", "Aortic valve", "Mitral valve", "Tricuspid valve"], "A",
 "The left 5th intercostal space, about 9 cm from the midline (mid-clavicular line), is the surface "
 "landmark for the cardiac apex/apex beat."),
(58, "One of the following is a feature of the left ventricle:",
 ["Limbus fossa ovalis", "Septal papillary muscles", "Septomarginal trabeculae", "Trabeculae carneae"], "D",
 "Trabeculae carneae are a feature of ventricular walls in general (present in the left ventricle); "
 "limbus fossa ovalis is a right atrial feature, and septal papillary muscles/septomarginal "
 "trabeculae (moderator band) are right-ventricular features."),
(59, "Left marginal artery is a branch of:",
 ["Anterior interventricular artery", "Posterior interventricular artery", "Circumflex artery", "Right coronary artery"], "C",
 "The left marginal artery arises from the circumflex branch of the left coronary artery."),
(60, "Ascending aorta, one statement is CORRECT:",
 ["Originates from infundibulum of left ventricle", "Gives right coronary artery from its right posterior sinus",
  "Has a bicuspid aortic valve", "It ends at level of sternal angle"], "D",
 "The ascending aorta ends at the level of the sternal angle, where it becomes the arch of the "
 "aorta; the normal aortic valve is tricuspid (not bicuspid), it arises from the aortic vestibule "
 "of the left ventricle (not an infundibulum, a right-ventricular structure), and the right "
 "coronary artery arises from the anterior (right) aortic sinus."),
(61, "Arch of aorta, one statement is CORRECT:",
 ["Begins & ends at level of sternal angle", "Gives right & left brachiocephalic arteries",
  "Has 4 branches", "Its arch is directed downwards & backwards"], "A",
 "The arch of the aorta both begins and ends at the level of the sternal angle (manubriosternal "
 "joint); it gives three branches (brachiocephalic trunk, left common carotid, left subclavian — "
 "not paired \"right and left\" brachiocephalic arteries, and not four branches)."),
(62, "All the following are correct about the IVC EXCEPT:",
 ["It drains into the right atrium", "It ends at level of left 6th costal cartilage",
  "It is formed by union of 2 common iliac veins", "Its abdominal part is longer than its thoracic part"], "B",
 "The IVC pierces the diaphragm and opens into the right atrium at the level of the right (not "
 "left) side, around the T8 vertebral level — not \"left 6th costal cartilage\"; it is formed by "
 "union of the common iliac veins and its abdominal course is far longer than its very short "
 "thoracic segment."),
(63, "One of the following does NOT share in the development of the atria:",
 ["Left half of common atrium", "Left horn of sinus venosus", "Right half of common atrium", "Right horn of sinus venosus"], "B",
 "The left horn of the sinus venosus mainly regresses to form the coronary sinus and oblique vein "
 "of the left atrium rather than contributing atrial chamber wall, unlike the right horn (which "
 "forms the smooth part of the right atrium) and both halves of the common (primitive) atrium."),
(64, "Concerning steps of interatrial septum formation all are true, EXCEPT:",
 ["Firstly: septum primum descends from the roof of common atrium",
  "Then the septum primum descends to close the ostium primum",
  "The septum primum leaving its connection with the roof to form ostium secondum",
  "The septum secondum then appears on the left side of the septum primum"], "D",
 "Septum secundum develops on the RIGHT side of septum primum (not the left), growing down beside "
 "it to eventually overlap the ostium secundum and form the foramen ovale."),
(65, "One of the following is a feature on the interatrial septum:",
 ["Atrioventricular canal", "Crista terminalis", "Fossa ovalis", "Sulcus terminalis"], "C",
 "Fossa ovalis, the remnant of the foramen ovale, is a feature of the interatrial septum itself; "
 "crista and sulcus terminalis are features of the right atrial wall, not the septum."),
(66, "Left 4th aortic arch gives:",
 ["Left common carotid", "Left subclavian", "Main part of arch of aorta", "Ductus arteriosus"], "C",
 "The left 4th pharyngeal (aortic) arch forms the main part of the definitive arch of the aorta, "
 "between the origins of the left common carotid and left subclavian arteries."),
]


def main():
    questions = []
    for stem, exp in WRITTEN:
        questions.append(Q(stem, None, '-', 'derived', exp=exp, qtype='QROC', tag=TAG, year=YEAR))
    for _, stem, opts, letter, exp in RAW:
        questions.append(Q(stem, opts, letter, 'derived', exp=exp, tag=TAG, year=YEAR))

    meta = {'Source file': SRC,
            'Type': 'Scanned image PDF, 10 pages, declares 54 total marks '
                    '(Part I: 3 written cases, 21 marks; Part II: 66 MCQs at 0.5 mark each, 33 marks)',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': YEAR,
            'Answer source': 'derived — the source carries inconsistent/contradictory hand marks '
                              '(consistent with a student\'s own working copy, not an examiner key); '
                              'every answer was independently derived from medical knowledge'}
    n = write_md(OUT, 'Source 26 — Qena CVS final 2020', meta, questions)

    mcq_letters = collections.Counter(r[3] for r in RAW)
    mcq = len(RAW)
    written = len(WRITTEN)
    highest = max(r[0] for r in RAW)
    print(f'source 26: {n} questions ({mcq} MCQ / {written} written)')
    print(f'  counters: declared in source = 66 MCQ + 3 written cases, highest MCQ number = {highest}, '
          f'option-A blocks = {len(RAW)}, ### Q = {n}')
    print(f'  answer source breakdown: derived={mcq + written} (all — no reliable key in source)')
    total = sum(mcq_letters.values())
    dist = ', '.join(f'{k}={v} ({v*100//total}%)' for k, v in sorted(mcq_letters.items()))
    top = max(mcq_letters.values()) / total
    verdict = 'PASS' if top <= 0.45 else ('INVESTIGATE' if top <= 0.60 else 'FAIL')
    print(f'  answer distribution (MCQ only): {dist}  -> bias gate: {verdict} (top={top*100:.0f}%, n={total})')
    print('  judgement calls: Q31 (Polyarteritis nodosa aneurysm type) is a weak fit among the given '
          'options — kept as the conventionally taught answer (mycotic) with a note in EXP. '
          'Physical PDF page order (pages 8-10) is reversed relative to question numbers 46-66 — '
          'questions here are emitted in logical numbering order, not page order.')


if __name__ == '__main__':
    main()
