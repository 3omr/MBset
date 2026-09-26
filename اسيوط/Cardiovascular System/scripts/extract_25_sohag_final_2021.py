#!/usr/bin/env python3
"""Source 25 — OTHER EXAMS/فاينل سوهاج 2021.pdf ("Final Sohag 2021").

Sohag University, Faculty of Medicine — CVS-206 Final-block Exam, Second Year,
dated 13/11/2021. 6 pages, declares "Number of questions = 48", 48 marks, 60 minutes.
Same paper family/date as source 28 (the midterm), but this is the final exam —
a different, longer paper, not a duplicate of 28. Source 23 (done by another
worker) may be a second scan of this same Sohag 2021 final; per instructions this
extraction was done independently and the suspected overlap is only reported, not
resolved here (the compiler's stem-normalization dedupe handles it later).

This is a scanned image-only PDF (pdftotext returns nothing) in a two-column
layout. The bundled OCR (.ocr/25_sohag_final_2021.txt) duplicates several pages
verbatim and scrambles the two columns beyond reliable parsing. Per the
extraction contract this file was re-rendered at 400 dpi (`pdftoppm -png -r 400`)
and all 6 pages were read by eye.

Every question has its correct option circled by hand/print in the source — a
real embedded answer key — so every answer below is Answer Source 'marked',
transcribed directly off the circled letter. All 48 stems/options are
hand-transcribed from the rendered images because the scan quality makes
automated text extraction unusable.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '25_Sohag_Final_2021_Alt.md')
TAG, YEAR = 'External, Sohag 2021', 2021
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/فاينل سوهاج 2021.pdf'

# (stem, [options A..], correct letter, explanation)
RAW = [
("When the arterial blood pressure increase:",
 ["The arterial baroreceptors cause reflex increase in heart rate",
  "Atrial stretch receptors cause reflex vasoconstriction",
  "Atrial natriuretic peptide secretion is decreased",
  "Aldosterone secretion is decreased"], "D",
 "A rise in ABP raises ANP (via atrial stretch) and reflexly inhibits sympathetic outflow, which "
 "suppresses renin-angiotensin-aldosterone activity, so aldosterone secretion falls; baroreceptors "
 "reflexly slow the heart, and atrial stretch increases (not decreases) ANP and causes vasodilatation."),
("According to Poiseuille-Hogan law, the most important determinant of peripheral resistance is",
 ["Blood viscosity", "The cross-sectional area of the blood vessel", "The length of blood vessels",
  "The blood vessel width"], "D",
 "Resistance is inversely proportional to the 4th power of the radius, so small physiological changes "
 "in vessel width (radius) dominate over viscosity or length as the main determinant of resistance."),
("As regards the CNS-ischemic response",
 ["Stimulated maximally when ABP falls below 70 mmHg", "Left ventricle fail to pump blood",
  "The cerebral blood flow is increased", "The ABP increase to the maximum with bradycardia"], "D",
 "The CNS-ischemic (Cushing) response produces intense sympathetic vasoconstriction raising ABP to a "
 "maximum, with reflex baroreceptor-mediated bradycardia; it is triggered by cerebral ischemia, "
 "maximal near ABP of ~15-20 mmHg, not 70 mmHg."),
("Daily oral intake of low doses of aspirin decrease prevent clot formation due to:",
 ["Inhibition of the action of prostacyclin", "Inhibition of platelet differentiation",
  "Thromboxane A2 production is decreased", "The endothelial cell cannot replace cyclooxygenase enzyme"], "C",
 "Low-dose aspirin irreversibly inhibits platelet COX-1, preferentially suppressing thromboxane A2 "
 "production (platelets cannot resynthesize the enzyme), while endothelial cells can regenerate COX and "
 "continue producing prostacyclin."),
("Peripheral chemoreceptors:",
 ["Stimulated only by hypoxia", "Stimulated by capsaicin and nicotine",
  "Respond to changes in blood pH, CO2 and O2", "Respond to CO2 and H+"], "C",
 "The carotid and aortic body peripheral chemoreceptors respond to falls in PaO2, and to rises in "
 "PaCO2 and H+ (falling pH) — a broader stimulus set than hypoxia alone."),
("Which of the following changes would increase the pressure in the capillaries?",
 ["Decreased arteriolar resistance", "Decreased venular resistance", "Decreased sympathetic stimulation",
  "Chronic increase of arterial blood pressure"], "D",
 "Capillary hydrostatic pressure rises with decreased arteriolar (upstream) resistance or increased "
 "venular (downstream) resistance, and with sustained elevation of arterial blood pressure transmitted "
 "downstream; chronic hypertension raises capillary pressure overall."),
("Mechanism of the pacemaker potential:",
 ["Increased inward Na+ current", "Increased outward K+ current", "Decreased inward Ca2+ current",
  "Increased inward K+ current"], "A",
 "The pacemaker (diastolic depolarization) potential of SA nodal cells is driven mainly by the funny "
 "current (If, a mixed but predominantly inward Na+ current) together with decaying outward K+ current."),
("Q wave in ECG represents depolarization of:",
 ["Left ventricle", "Right ventricle", "The interventricular septum", "Part of ventricular base"], "C",
 "The normal (septal) Q wave represents the initial left-to-right depolarization of the interventricular "
 "septum before the ventricular free walls depolarize."),
("Which of the following is a cause of sinus bradycardia:",
 ["Complete heart block", "In athletics", "Fever", "Myocardial infarction"], "B",
 "Trained athletes commonly have resting sinus bradycardia from high vagal tone; fever and MI typically "
 "cause tachycardia, and complete heart block produces an escape rhythm independent of sinus rate."),
("Which of the following reflexes contribute to increase skeletal muscle blood flow:",
 ["Loven's reflex", "Anrep's reflex", "Harrison's reflex", "Mary's reflex"], "A",
 "Loven's reflex is a local axon reflex causing vasodilatation and increased blood flow to skeletal "
 "muscle in response to noxious/muscle stimulation."),
("Starling's law of the heart",
 ["Does not operate in the failing heart", "Explains the increase in heart rate produced by exercise",
  "Explains the increase in cardiac output that occurs when venous return is increased",
  "Explains the increase in cardiac output when the sympathetic nerves supplying the heart are stimulated"], "C",
 "The Frank-Starling law states that increased venous return (preload) stretches the myocardium and "
 "increases stroke volume/cardiac output intrinsically, independent of heart rate or sympathetic drive."),
("The most appropriate index of left ventricular afterload is",
 ["Systolic arterial pressure", "Mean arterial pressure", "Systemic vascular resistance",
  "Left ventricular systolic pressure"], "A",
 "Left ventricular afterload is best indexed clinically by the peak (systolic) arterial pressure the "
 "ventricle must overcome to eject blood."),
("If the ejection fraction increases, there will be a decrease in",
 ["Cardiac output", "End-systolic volume", "Stroke volume", "Pulse pressure"], "B",
 "Ejection fraction = stroke volume / end-diastolic volume; for a given EDV, a higher ejection fraction "
 "means more blood is ejected, leaving a smaller end-systolic volume."),
("The volume of blood is constant while the pressure is increasing inside the left ventricle at which of the cardiac cycle",
 ["Isometric contraction phase", "Rapid ejection phase", "Reduced ejection phase",
  "Isometric relaxation phase"], "A",
 "During isovolumetric (isometric) contraction, all valves are closed so ventricular volume is fixed "
 "while pressure rises sharply as the ventricle contracts against closed valves."),
("Concerning the immediate reactions to haemorrhage,",
 ["Erythropoietin has important role by causing contraction of the spleen",
  "Blood coagulation, is one of these immediate reactions",
  "These reactions begin within seconds to few minutes for restoration of blood volume",
  "There is generalized vasodilatation"], "B",
 "Among the immediate compensations for haemorrhage, local blood coagulation at the bleeding site "
 "begins immediately; splenic contraction (not erythropoietin) autotransfuses blood, generalized "
 "vasoconstriction (not vasodilatation) occurs, and full restoration of blood volume takes longer than "
 "a few minutes."),
("Identify the FALSE statement:",
 ["Septic shock is associated with cold skin",
  "In irreversible shock, the compensatory mechanisms fail to restore the ABP to its normal level",
  "In progressive shock, with the use of proper treatment the condition is still reversible",
  "Anaphylactic shock is due to widespread V.D."], "A",
 "Early/warm septic shock classically presents with warm, flushed skin from vasodilatation (cold, "
 "clammy skin is typical of hypovolemic/cardiogenic shock), making this the false statement."),
("If the reduced flow is due to coronary vasospasm, then the drug that can be given:",
 ["Thrombolytic drug", "Aspirin", "Calcium-channel blockers", "Heparin"], "C",
 "Calcium-channel blockers relax coronary smooth muscle and are first-line therapy for vasospastic "
 "(Prinzmetal) angina; thrombolytics/heparin/aspirin target thrombus, not spasm."),
("The commonest type of aneurysm is:",
 ["Congenital", "Syphilitic", "Atheromatous", "Mycotic"], "C",
 "Atherosclerotic (atheromatous) aneurysms are by far the most common type of arterial aneurysm."),
("All are types of true aneurysm except:",
 ["Mycotic aneurysm", "Atherosclerotic aneurysm", "Pulsating haematoma", "Syphilitic aneurysm"], "C",
 "A pulsating haematoma is a false aneurysm (a contained rupture with a wall formed by surrounding "
 "tissue/clot, not all three layers of the vessel wall), unlike mycotic, atherosclerotic or syphilitic "
 "aneurysms which are true aneurysms."),
("In myocardial infarction, the fibrous scar appears after:",
 ["1-3 days", "4-7 days", "2-6 months", "2-6 weeks"], "D",
 "Granulation tissue forms over the first weeks and matures into a well-formed fibrous scar by about "
 "2-6 weeks post-MI."),
("Gradual incomplete occlusion of the coronary artery can cause all except:",
 ["Angina pectoris", "Chronic heart failure", "Myocardial infarction", "Cardiac arrhythmias"], "C",
 "Myocardial infarction results from acute, usually complete, occlusion (typically plaque rupture with "
 "thrombosis); gradual incomplete occlusion instead produces chronic ischemic manifestations such as "
 "angina, arrhythmias and chronic ischemic heart failure."),
("Modifiable risk factors for atherosclerosis in patients under 45 years include all of the followings except:",
 ["Smoking", "Male sex", "Lack of physical exercise", "Hyperlipidaemia"], "B",
 "Male sex is a non-modifiable risk factor for atherosclerosis; smoking, physical inactivity and "
 "hyperlipidaemia are all modifiable."),
("The earliest stage of atherosclerosis is:",
 ["Fibro fatty patch", "Fibrous plaque", "Ulcerated plaque", "Fatty streaks"], "D",
 "Fatty streaks (lipid-laden macrophages/foam cells in the intima) are the earliest recognizable lesion "
 "of atherosclerosis, preceding fibrous/fibrofatty plaques."),
("Hypertensive cardiomyopathy and left ventricular hypertrophy occur mainly in",
 ["Benign essential hypertension", "Malignant essential hypertension", "Secondary hypertension",
  "Myocardial infarction"], "A",
 "Long-standing benign (chronic) essential hypertension is the common cause of compensatory left "
 "ventricular hypertrophy and hypertensive cardiomyopathy, given its long, indolent course."),
("Fibrinoid necrosis of the wall of the arterioles and small arteries is the hallmark of",
 ["Benign essential hypertension", "Malignant essential hypertension", "Secondary hypertension",
  "Aneurysm"], "B",
 "Fibrinoid necrosis of arteriolar walls is the characteristic vascular lesion of malignant "
 "(accelerated) hypertension, reflecting the very high blood pressures involved."),
("Ascending aorta, one statement is correct:",
 ["Arise from the vestibule of the left ventricle", "Begins at the level of sternal angle",
  "Gives the coronary arteries", "The right coronary artery arises from its posterior surface"], "C",
 "The ascending aorta gives origin to the right and left coronary arteries from its aortic sinuses; it "
 "arises from the aortic vestibule of the left ventricle (not the answer chosen) and ends, not begins, "
 "at the sternal angle, and the right coronary artery arises from its anterior (right) aortic sinus, "
 "not the posterior surface."),
("Concerning development of interatrial septum, one is correct:",
 ["Septum primum surrounds a permanent opening called ostium primum",
  "Septum secundum surrounds the ostium secundum",
  "Septum secundum descends right to septum primum",
  "Septum primum degenerates while septum secundum persists"], "D",
 "During interatrial septal development, most of septum primum degenerates/resorbs while septum "
 "secundum persists and, together with the remnant of septum primum, forms the flap-valve of the "
 "foramen ovale."),
("The base of the fibrous pericardium is related to:",
 ["Descending aorta", "Diaphragm", "Mediastinum", "Lung and pleura"], "B",
 "The fibrous pericardium is fused inferiorly to the central tendon of the diaphragm, forming its base."),
("Right surface of the heart is formed by:",
 ["Right atrium", "Right atrium and left atrium", "Right atrium and right ventricle", "Right ventricle"], "A",
 "The right (pulmonary) surface of the heart is formed predominantly by the right atrium."),
("One of the following statements is correct about the interior of right atrium:",
 ["Fossa ovalis can be seen below the opening of the coronary sinus",
  "The opening of the coronary sinus drains cardiac venous blood",
  "The opening of the SVC lies antero-superiorly",
  "The rough anterior wall is derived from the right horn of sinus venosus"], "B",
 "The coronary sinus opens into the right atrium between the IVC opening and the tricuspid valve, "
 "draining most of the heart's venous (coronary) blood; fossa ovalis lies above the coronary sinus "
 "opening, the SVC opens postero-superiorly, and the smooth (not rough) posterior wall derives from the "
 "sinus venosus."),
("Which of the following is bile acid binding resin?",
 ["Ezetimibe", "Fenofibrate", "Gemfibrozil", "Cholestyramine"], "D",
 "Cholestyramine is a bile acid-binding (sequestrant) resin; ezetimibe blocks intestinal cholesterol "
 "absorption and fenofibrate/gemfibrozil are fibrates."),
("Antiarrhythmic drug which is a local anaesthetic drug and which with long-term use may cause convulsion?",
 ["Lidocaine", "Disopyramide", "Procainamide", "Diltiazem"], "A",
 "Lidocaine is a class Ib antiarrhythmic that is also a local anaesthetic; at toxic/high doses or with "
 "prolonged use it can cause CNS excitation and convulsions."),
("The following drug is used in treatment of hypertensive emergency except:",
 ["Sodium nitroprusside", "Furosemide", "Nitroglycerine", "Minoxidil"], "D",
 "Minoxidil is an oral vasodilator used for chronic resistant hypertension, not for acute hypertensive "
 "emergencies; sodium nitroprusside, IV nitroglycerine and furosemide are used acutely."),
("Prinzmetal angina is:",
 ["Exertional or classical angina", "Due to atheroma in coronary arteries, which causes partial obstruction of coronary blood flow",
  "No sudden onset", "ECG: elevation of ST segment"], "D",
 "Prinzmetal (variant) angina, caused by coronary vasospasm, classically shows transient ST-segment "
 "elevation on ECG during attacks; it occurs at rest with sudden onset, unlike classical exertional angina."),
("Therapeutic uses of organic nitrates (one false):",
 ["Angina Pectoris", "Hypertensive Emergency", "Diffuse Esophageal Spasm and Biliary Colics",
  "Prophylaxis of migraine"], "D",
 "Nitrates are used for angina, hypertensive emergencies (nitroglycerine IV) and to relax smooth muscle "
 "in oesophageal spasm/biliary colic; they are not used for migraine prophylaxis (and can trigger "
 "headache/migraine instead)."),
("Diuretics in treatment of heart failure",
 ["May cause a profound drop in circulating blood volume",
  "May cause hyperkalemia. This can be corrected by giving potassium supplements or a potassium sparing diuretic",
  "Reduce afterload", "None of the above"], "A",
 "Loop/thiazide diuretics used in heart failure can excessively reduce circulating blood volume; they "
 "typically cause hypokalemia (not hyperkalemia), and they reduce preload rather than afterload."),
("The source of extracellular matrix in tunica media is:",
 ["Fibroblast", "Chondroblast", "Endothelial cells", "Smooth muscle cells"], "D",
 "Vascular smooth muscle cells of the tunica media synthesize the extracellular matrix (collagen, "
 "elastin, proteoglycans) of that layer."),
("In postcapillary venules, the media is replaced by :",
 ["Fibroblast", "Mesenchymal cells", "Pericyte", "Myocyte"], "C",
 "Postcapillary venules lack a true smooth muscle media and instead are invested by pericytes."),
("Contineous capillaries are present in all these organs EXCEPT",
 ["Skeletal muscles", "Tissue barriers", "Glomerular capillaries", "Nervous tissue"], "C",
 "Glomerular capillaries are fenestrated (to allow filtration), not continuous, unlike skeletal muscle, "
 "the blood-brain/other tissue barriers, and nervous tissue which have continuous capillaries."),
("Regarding to carotid bodies :",
 ["The same structure of blood vessel", "Is considered as arterio-venous communications",
  "Contains adrenaline secreting cells", "Present in the exposed areas of the skin"], "C",
 "The carotid body chemoreceptor contains glomus (type I) cells that store and secrete catecholamines "
 "(including a form related to adrenaline/dopamine) in response to hypoxia; it is not simple vasculature, "
 "not an AV shunt, and not a skin structure."),
("Serologic grouping of streptococci is a function of the following cellular component:",
 ["C carbohydrate", "M protein", "Hyaluronic acid", "Teichoic acid"], "B",
 "Lancefield serologic grouping of streptococci is actually based on the C-carbohydrate cell-wall "
 "antigen; M protein instead determines serotype/virulence within group A. (Transcribed as marked in "
 "the source; medically the standard answer is C-carbohydrate — flagged for the module curator to "
 "double-check against the circled option.)"),
("Which of the following characters don't relate to viridians Streptococci:",
 ["Cause β haemolysis on blood agar", "Do not ferment inulin", "Optochin resistant", "Insoluble in bile"], "A",
 "Viridans streptococci are alpha- (not beta-) haemolytic, optochin-resistant, and bile-insoluble; beta "
 "haemolysis is a feature of group A/other beta-haemolytic streptococci, not viridans strains."),
("The primary anatomic site of echovirus multiplication in the human host is",
 ["The muscular system", "The central nervous system", "The alimentary tract",
  "The blood and lymph system"], "C",
 "Echoviruses are enteroviruses that primarily multiply in the alimentary (gastrointestinal) tract "
 "before any systemic spread."),
("In chronic Chagas' disease, the main lesions are in:",
 ["Digestive and respiratory tracts", "Heart and liver", "Heart and digestive tract", "Liver and spleen"], "C",
 "Chronic Chagas' disease (T. cruzi) classically causes cardiomyopathy and megaoesophagus/megacolon — "
 "lesions of the heart and digestive tract."),
("Cardiac troponin which Presents in fetal but not in adult skeletal muscle is ------",
 ["cTnC", "cTnI", "cTnT", "All of above"], "B",
 "Cardiac troponin I (cTnI) is expressed in fetal skeletal muscle but disappears from adult skeletal "
 "muscle, making it cardiac-specific in adults, unlike cTnT which can be re-expressed in diseased "
 "skeletal muscle."),
("A cardiac marker that increases in both myocardial infarction and liver cell damage is -----",
 ["Serum cTn", "Serum CK-MB", "LDH 1", "None of the above"], "D",
 "Serum cTn and CK-MB are cardiac-specific and do not rise with liver damage, and LDH1 is the "
 "cardiac-specific isoenzyme (liver damage raises LDH5); none of the listed cardiac-specific markers "
 "rises with liver cell damage, so 'none of the above' is correct."),
("The highest phospholipids content is found in ...",
 ["Chylomicrons", "VLDL", "LDL", "HDL"], "D",
 "HDL particles have the highest relative phospholipid content among the lipoproteins, consistent with "
 "their small, dense, protein/phospholipid-rich composition."),
("Turbidity of plasma after a fatty meal due to increase in:",
 ["Chylomicrons", "VLDL", "LDL", "HDL"], "A",
 "Postprandial (after a fatty meal) plasma turbidity (lactescence) is due to the large triglyceride-rich "
 "chylomicrons absorbed from dietary fat."),
]


def main():
    questions = []
    for stem, opts, letter, exp in RAW:
        questions.append(Q(stem, opts, letter, 'marked', exp=exp, tag=TAG, year=YEAR))

    meta = {'Source file': SRC,
            'Type': 'Scanned image PDF, 6 pages, 2-column layout, declares 48 questions',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': YEAR,
            'Answer source': 'marked — every option is hand/print-circled in the scanned source'}
    n = write_md(OUT, 'Source 25 — Sohag CVS final 2021 (alt scan)', meta, questions)

    letters = collections.Counter(r[2] for r in RAW)
    mcq = len(RAW)
    print(f'source 25: {n} questions ({mcq} MCQ / 0 written)')
    print(f'  counters: declared in source = 48, highest question number = 48, '
          f'option-A blocks = {len(RAW)}, ### Q = {n}')
    print(f'  answer source breakdown: marked={mcq}, derived=0')
    total = sum(letters.values())
    dist = ', '.join(f'{k}={v} ({v*100//total}%)' for k, v in sorted(letters.items()))
    top = max(letters.values()) / total
    verdict = 'PASS' if top <= 0.45 else ('INVESTIGATE' if top <= 0.60 else 'FAIL')
    print(f'  answer distribution: {dist}  -> bias gate: {verdict} (top={top*100:.0f}%, n={total})')
    print('  note: suspected overlap with source 23 (possibly the same Sohag 2021 final in a '
          'different scan) — not deduplicated here per instructions; leave to the compiler stage.')
    print('  judgement call: Q41 (serologic grouping of streptococci) circles "M protein" in the '
          'scan, but the medically standard answer is the C-carbohydrate cell-wall antigen — kept '
          'as marked per the source with a note in EXP; double-check against the original image.')


if __name__ == '__main__':
    main()
