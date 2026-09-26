# -*- coding: utf-8 -*-
import os

mcqs = [
    # --- I. Gametogenesis: 1. Spermatogenesis (10 Qs) ---
    {
        "stem": "Regarding spermatogenesis, all are true EXCEPT:",
        "options": [
            "A) It starts at puberty.",
            "B) The whole process takes about 70 - 80 days.",
            "C) Spermatogonia divide by meiosis.",
            "D) One spermatogonium gives rise to four spermatids.",
            "E) It is continuous through life."
        ],
        "correct": "C",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "The normal chromosomal number of human spermatid is:",
        "options": [
            "A) 23 autosomes + two different sex chromosomes.",
            "B) 22 autosomes + X and Y chromosomes.",
            "C) 23 autosomes + two identical sex chromosomes.",
            "D) 22 autosomes + X or Y chromosome.",
            "E) 23 autosomes + X or Y chromosome."
        ],
        "correct": "D",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "Concerning spermatogenesis, all are true EXCEPT:",
        "options": [
            "A) Secondary spermatocyte contains 23 chromosomes including X and Y.",
            "B) Secondary spermatocyte gives two spermatids by meiosis II.",
            "C) Primary spermatocyte contains 46 chromosomes.",
            "D) It starts at puberty tell old age."
        ],
        "correct": "A",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "Which type of the following germ cells contains haploid number of chromosomes:",
        "options": [
            "A) Spermatogonia.",
            "B) Primary spermatocytes.",
            "C) Primary oocytes.",
            "D) Secondary oocytes.",
            "E) Oogonia."
        ],
        "correct": "D",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "One cell contains 23 chromosomes:",
        "options": [
            "A) Primary oocyte.",
            "B) 2nd polar body.",
            "C) Primary spermatocytes.",
            "D) Oogonia."
        ],
        "correct": "B",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "Regarding spermiogenesis, all are true EXCEPT:",
        "options": [
            "A) It is the morphological transformation of spermatid into sperm.",
            "B) The nucleus forms the future head of the sperm.",
            "C) The flagellum (tail) develops from one centriole.",
            "D) Golgi apparatus forms acrosomal cap."
        ],
        "correct": "C",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "Spermiogenesis means transformation of:",
        "options": [
            "A) 1ry spermatocyte into 2ry spermatocyte.",
            "B) 2ry spermatocyte into spermatid.",
            "C) Spermatid into sperm.",
            "D) Spermatogonium into 1ry spermatocyte."
        ],
        "correct": "C",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "The following are correct regarding sperm EXCEPT:",
        "options": [
            "A) It consists of head, body and tail.",
            "B) Its nucleus contains 23 chromosomes.",
            "C) Its head is covered by the acrosome cap.",
            "D) The acrosome cap contains lytic (hydrolytic) enzymes.",
            "E) The tail is immotile."
        ],
        "correct": "E",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "The following are true about sperm EXCEPT:",
        "options": [
            "A) Smaller in size than ovum.",
            "B) Has no power of motility.",
            "C) Has acrosomal cap.",
            "D) Formed of head, neck, and tail."
        ],
        "correct": "B",
        "topic": "Spermatogenesis"
    },
    {
        "stem": "Concerning the seminal fluid, all the following are correct EXCEPT:",
        "options": [
            "A) Its volume is 2 - 3 cc.",
            "B) Its count is about 200 - 300 thousands of sperms per ml.",
            "C) It contains secretions from the epididymis, prostate, and seminal vesicle.",
            "D) Normally, it is deposited during sexual intercourse in the posterior fornix of the vagina.",
            "E) Normally, 60 - 70% of its sperms are motile."
        ],
        "correct": "B",
        "topic": "Spermatogenesis"
    },

    # --- 2. Oogenesis (12 Qs) ---
    {
        "stem": "Concerning the 1st meiotic division of the primary oocyte, all are correct EXCEPT:",
        "options": [
            "A) It results in one secondary oocyte and one polar body.",
            "B) It is completed after fertilization.",
            "C) It results in two cells with haploid number of chromosomes.",
            "D) It is always followed by the second meiotic division."
        ],
        "correct": "B",
        "topic": "Oogenesis"
    },
    {
        "stem": "The following are correct regarding gametogenesis EXCEPT:",
        "options": [
            "A) Spermatogenesis starts after puberty till an old age.",
            "B) Oogenesis begins after puberty till menopause.",
            "C) The male gamete determines the sex of embryo.",
            "D) The mature ovum contains haploid number of chromosomes.",
            "E) Spermiogenesis means the transformation of spermatids into sperms."
        ],
        "correct": "B",
        "topic": "Oogenesis"
    },
    {
        "stem": "Concerning oogenesis, all are true EXCEPT:",
        "options": [
            "A) It may take up to 40 years to be completed.",
            "B) Primary oocytes are arrested in diplotene stage of meiosis II.",
            "C) Meiosis inhibitory factor is secreted by primary oocytes.",
            "D) Zona granulosa is secreted by granulosa cells and the oocyte.",
            "E) About 5-15 primordial follicles begin maturation each ovarian cycle."
        ],
        "correct": "C",
        "topic": "Oogenesis"
    },
    {
        "stem": "Which stage of human development there is maximum number of oogonia?",
        "options": [
            "A) At birth.",
            "B) Five months intrauterine fetal life.",
            "C) At puberty.",
            "D) During early adulthood."
        ],
        "correct": "B",
        "topic": "Oogenesis"
    },
    {
        "stem": "The secondary oocyte completes the second maturation division:",
        "options": [
            "A) Before maturation.",
            "B) During maturation.",
            "C) At fertilization.",
            "D) Before birth.",
            "E) Before puberty."
        ],
        "correct": "C",
        "topic": "Oogenesis"
    },
    {
        "stem": "Concerning the human oocyte, all the following are correct EXCEPT:",
        "options": [
            "A) At ovulation, it is larger than the human sperm.",
            "B) It commences its first meiotic division at the age of puberty.",
            "C) It contains haploid number of chromosomes.",
            "D) It is developed from the germ cells."
        ],
        "correct": "B",
        "topic": "Oogenesis"
    },
    {
        "stem": "The ootids are:",
        "options": [
            "A) Female germ cells.",
            "B) Have 23 chromosomes.",
            "C) All ootids contain X chromosome.",
            "D) All the above."
        ],
        "correct": "D",
        "topic": "Oogenesis"
    },
    {
        "stem": "Concerning oogenesis, all are true EXCEPT:",
        "options": [
            "A) Oogonia divide by mitosis during fetal life.",
            "B) The 1ry oocyte is surrounded by zona pellucida.",
            "C) The 1ry oocyte divides by mitosis to give 2ry oocytes just before birth.",
            "D) The 2ry oocyte contains haploid number of chromosomes.",
            "E) The 2ry oocytes are ready for fertilization at the time of their formation."
        ],
        "correct": "C",
        "topic": "Oogenesis"
    },
    {
        "stem": "Just after ovulation, the mature ovum is surrounded by the following layers EXCEPT:",
        "options": [
            "A) Corona radiate.",
            "B) Zona pellucida.",
            "C) Primordial germ cells.",
            "D) Vitelline membrane.",
            "E) Previtelline space."
        ],
        "correct": "C",
        "topic": "Oogenesis"
    },
    {
        "stem": "The following are correct regarding the ovum EXCEPT:",
        "options": [
            "A) It is larger than the sperm.",
            "B) Its nucleus contains 22 chromosomes + one X chromosome.",
            "C) It goes to the uterus by the peristaltic movements of the uterine tube.",
            "D) Normally two ova are formed in the ovary every 28 days.",
            "E) The sperm is attracted to it by chemotaxis."
        ],
        "correct": "D",
        "topic": "Oogenesis"
    },
    {
        "stem": "One statement is NOT correct about oogenesis:",
        "options": [
            "A) Zona pellucida is secreted by the nucleus of the ovum.",
            "B) Meiosis inhibitory factor is secreted by the follicular cells.",
            "C) Primary oocytes are arrested in diplotene stage of meiosis I.",
            "D) About 5-15 primordial follicles begin maturation each ovarian cycle."
        ],
        "correct": "A",
        "topic": "Oogenesis"
    },
    {
        "stem": "The first meiotic division is completed just prior to ovulation, forming a secondary oocyte. The second division begins immediately but does not finished unless:",
        "options": [
            "A) hCG levels are high.",
            "B) Fertilization takes place.",
            "C) The epiblast is no longer present.",
            "D) The sperm are uncapacitated.",
            "E) A developmental anomaly is present."
        ],
        "correct": "B",
        "topic": "Oogenesis"
    },

    # --- II. Ovarian Cycle (12 Qs) ---
    {
        "stem": "Concerning the corpus luteum, all the following are correct EXCEPT:",
        "options": [
            "A) Present in the 2nd half of the cycle.",
            "B) Starts to degenerate few days before menstruation if fertilization does not occur.",
            "C) Secretes oestrogen.",
            "D) Under control of luteinizing hormone.",
            "E) Transforms into a corpus albicans when it degenerates."
        ],
        "correct": "C",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "Concerning the ovarian cycle, all the following are correct EXCEPT:",
        "options": [
            "A) The luteal phase is under the influence of luteinizing hormone.",
            "B) The hormone of the proliferative phase is progesterone.",
            "C) Corpus luteum secretes progesterone.",
            "D) The duration of the luteal phase is about 14 days."
        ],
        "correct": "B",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "Concerning the ovarian cycle, all the following are correct EXCEPT:",
        "options": [
            "A) Starts at the age of puberty.",
            "B) Its follicular phase corresponds to the proliferative phase of the endometrium.",
            "C) It is under the influence of both LH and FSH.",
            "D) The corpus luteum secretes progesterone till the end of pregnancy."
        ],
        "correct": "D",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "Phases of the ovarian cycle are the following EXCEPT:",
        "options": [
            "A) Proliferative phase.",
            "B) Follicular phase.",
            "C) Ovulation.",
            "D) Luteal phase."
        ],
        "correct": "A",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "Factors causing ovulation are the following EXCEPT:",
        "options": [
            "A) Sharp rise in LH.",
            "B) Local weakness of the ovarian surface.",
            "C) Sharp rise in progesterone level.",
            "D) Increased intrafollicular pressure."
        ],
        "correct": "A",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "Luteal phase of the ovarian cycle is under the effect of:",
        "options": [
            "A) FSH.",
            "B) LH.",
            "C) Estrogen.",
            "D) Progesterone."
        ],
        "correct": "B",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "One statement is NOT a factor causing transport of the oocyte towards the uterus:",
        "options": [
            "A) Movement of the fimbria.",
            "B) Cilliary action of the uterine tube.",
            "C) Peristaltic movements of the uterine tube.",
            "D) Cilliary action of the endometrium."
        ],
        "correct": "D",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "Just after ovulation, the mature ovum is surrounded by the following layers EXCEPT:",
        "options": [
            "A) Corona radiate.",
            "B) Zona pellucida.",
            "C) Primordial germ cells.",
            "D) Vitelline membrane.",
            "E) Previtelline space."
        ],
        "correct": "C",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "The primary oocytes are arrested in the first meiotic division till puberty due to the presence of:",
        "options": [
            "A) Early pregnancy factor.",
            "B) Human chorionic gonadotrophin.",
            "C) Meiosis inhibitory factor.",
            "D) Follicle stimulating hormone."
        ],
        "correct": "C",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "The corona radiate is:",
        "options": [
            "A) Germinal vesicle.",
            "B) Germinal spot.",
            "C) Cumulus oophorous.",
            "D) Granulosa cells surrounding the ovum."
        ],
        "correct": "D",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "Movement of the ovum in the uterine tube is due to:",
        "options": [
            "A) Tubal contractions.",
            "B) Cilia of the tube.",
            "C) Flagellum.",
            "D) None of the above.",
            "E) A + B + C.",
            "F) A + B."
        ],
        "correct": "F",
        "topic": "Ovarian Cycle"
    },
    {
        "stem": "The follicular antrum of the Graafian follicle contains:",
        "options": [
            "A) Estrogen.",
            "B) Progesterone.",
            "C) LH.",
            "D) FSH."
        ],
        "correct": "A",
        "topic": "Ovarian Cycle"
    },

    # --- III. Menstrual Cycle (7 Qs) ---
    {
        "stem": "Concerning the endometrium, all are true EXCEPT:",
        "options": [
            "A) It is supplied by spiral arterioles.",
            "B) It becomes decidua during pregnancy.",
            "C) The basal layer is its functional layer.",
            "D) It becomes secretory in the second half of pregnancy."
        ],
        "correct": "C",
        "topic": "Menstrual Cycle"
    },
    {
        "stem": "Concerning the menstrual cycle, all the following are correct EXCEPT:",
        "options": [
            "A) The proliferative phase is under the influence of oestrogen.",
            "B) The main changes occur in the basal layer of the endometrium.",
            "C) Usually, the luteal phase has constant duration.",
            "D) Menstruation occurs as a result of withdrawal of the ovarian hormones."
        ],
        "correct": "B",
        "topic": "Menstrual Cycle"
    },
    {
        "stem": "Concerning the menstrual phase of the uterine cycle, all are true EXCEPT:",
        "options": [
            "A) Bleeds about 500 cc.",
            "B) Its duration is about 3 - 5 days.",
            "C) It is preceded by the luteal phase.",
            "D) It doesn't involve the basal layer of the endometrium.",
            "E) It is followed by the proliferative phase."
        ],
        "correct": "A",
        "topic": "Menstrual Cycle"
    },
    {
        "stem": "The stage of the menstrual cycle that is under influence of progesterone is:",
        "options": [
            "A) Luteal phase.",
            "B) Proliferative.",
            "C) Menstrual.",
            "D) All of the stages."
        ],
        "correct": "A",
        "topic": "Menstrual Cycle"
    },
    {
        "stem": "Proliferative (proliferative) phase of the menstrual cycle is under the effect of:",
        "options": [
            "A) Estogen hormone of the growing ovarian follicle.",
            "B) Progesterone hormone of the corpus luteum.",
            "C) LH of the anterior pituitary.",
            "D) FSH of the anterior pituitary."
        ],
        "correct": "A",
        "topic": "Menstrual Cycle"
    },
    {
        "stem": "The uterine glands become more tortuous and full of secretion (screw-like) in:",
        "options": [
            "A) Menstrual phase.",
            "B) Proliferative phase.",
            "C) Ischemic phase.",
            "D) Secretory phase."
        ],
        "correct": "D",
        "topic": "Menstrual Cycle"
    },
    {
        "stem": "The ischemic phase of the menstrual cycle occurs due to:",
        "options": [
            "A) Decreased level of estrogen.",
            "B) Increased level of estrogen.",
            "C) Increased level of progesterone.",
            "D) Decreased level of progesterone."
        ],
        "correct": "D",
        "topic": "Menstrual Cycle"
    },

    # --- IV. Fertilization (21 Qs) ---
    {
        "stem": "The union of the human sex cells is believed to occur in:",
        "options": [
            "A) Middle third of the fallopian tube.",
            "B) Medial third of the fallopian tube.",
            "C) Lateral third of the fallopian tube.",
            "D) Uterus.",
            "E) Vagina."
        ],
        "correct": "C",
        "topic": "Fertilization"
    },
    {
        "stem": "The normal site of fertilization is:",
        "options": [
            "A) Isthmus of uterine tube.",
            "B) Fimbria of uterine tube.",
            "C) Ampulla of uterine tube.",
            "D) Intramural part of uterine tube.",
            "E) At the ovary."
        ],
        "correct": "C",
        "topic": "Fertilization"
    },
    {
        "stem": "Capacitation of sperm is:",
        "options": [
            "A) Release of acrosome enzymes.",
            "B) Penetration of zona pellucida.",
            "C) Removal of glycoprotein coat.",
            "D) Passage of sperm into corona radiate.",
            "E) Fusion of the sperm and ovum."
        ],
        "correct": "C",
        "topic": "Fertilization"
    },
    {
        "stem": "Capacitation of sperm means:",
        "options": [
            "A) Release of proteolytic enzymes from sperm acrosome.",
            "B) Dispersal of the corona radiata cells.",
            "C) Removal of the glycoprotein and seminal protein from the sperm.",
            "D) Fusion of the sperm and ovum.",
            "E) Movement of the sperm in the female genital tract."
        ],
        "correct": "C",
        "topic": "Fertilization"
    },
    {
        "stem": "Concerning fertilization, all are true EXCEPT:",
        "options": [
            "A) Occurs in the lateral third of the fallopian tube.",
            "B) Restores the diploid number of the chromosomes.",
            "C) Results in determination of the fetal sex.",
            "D) Results in determination of the characters."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },
    {
        "stem": "All are true concerning fertilization EXCEPT:",
        "options": [
            "A) The oocyte completes the second meiotic division just before or during it.",
            "B) The sperm has to penetrate the corona radiata and zona pellucida.",
            "C) After the sperm penetrates the ovum, the tail degenerates.",
            "D) After entry of one sperm into the ovum, the zona pellucida prevents penetration of other sperms.",
            "E) It normally occurs in the ovaries."
        ],
        "correct": "E",
        "topic": "Fertilization"
    },
    {
        "stem": "Results of fertilization are the following EXCEPT:",
        "options": [
            "A) Restoration of the diploid number of chromosomes (46).",
            "B) Restoration of the embryo's chromosomal sex.",
            "C) Lyses of the zona pellucida.",
            "D) Initiation of cleavage."
        ],
        "correct": "C",
        "topic": "Fertilization"
    },
    {
        "stem": "Results of fertilization are the following EXCEPT:",
        "options": [
            "A) The number of chromosomes returns to the diploid number (46).",
            "B) Formation of blastocyst.",
            "C) Determination of the chromosomal sex of the embryo.",
            "D) Start of cleavage."
        ],
        "correct": "B",
        "topic": "Fertilization"
    },
    {
        "stem": "Results of fertilization are the following EXCEPT:",
        "options": [
            "A) Initiation of cleavage.",
            "B) Restoration of diploid number of chromosomes.",
            "C) Determination of chromosome sex of the embryo.",
            "D) Formation of chorionic villi."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },
    {
        "stem": "Concerning fertilization, the following is true EXCEPT:",
        "options": [
            "A) Penetration of zona is done by acrosome reaction.",
            "B) Capacitation means removal of glycoprotein coat.",
            "C) It leads to chromosomal sex determination of the embryo.",
            "D) Zona reaction allows the entry of more than one sperm into the ovum."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },
    {
        "stem": "Concerning fertilization, the following is TRUE:",
        "options": [
            "A) Results in determination of fetal sex.",
            "B) Stimulates cleavage.",
            "C) The sperm has to penetrate the zona pellucida.",
            "D) All the above."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },
    {
        "stem": "All the following are correct regarding fertilization EXCEPT:",
        "options": [
            "A) The usual site is the ampulla of the uterine tube.",
            "B) Sperms can live in the female genital tract for up to 48 hours.",
            "C) Sperms reach to the ovum by their motility.",
            "D) The secondary oocyte finishes its 2nd meiotic division after sperm entry.",
            "E) Ova reach the uterine tube by cilliary action of the corona radiate."
        ],
        "correct": "E",
        "topic": "Fertilization"
    },
    {
        "stem": "In fertilization:",
        "options": [
            "A) It leads to restoration of the haploid number of chromosome.",
            "B) It stimulates implantation.",
            "C) It occurs in the isthmus of uterine tube.",
            "D) It determines the sex of the embryo."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },
    {
        "stem": "The following are correct regarding fertilization EXCEPT:",
        "options": [
            "A) It is meeting of the sperm and ovum.",
            "B) It occurs in the ismthus of the uterine tube.",
            "C) It results in a zygote with 46 chromosomes.",
            "D) It determines the chromosomal sex of the embryo.",
            "E) It stimulates cleavage."
        ],
        "correct": "B",
        "topic": "Fertilization"
    },
    {
        "stem": "One statement is NOT correct regarding fertilization:",
        "options": [
            "A) It takes about 24 hours.",
            "B) It occurs on the surface of the ovary.",
            "C) The sperm must undergo capacitation and acrosome reaction to be able to penetrate the ovum.",
            "D) Leads to restoration of the diploid number of chromosomes."
        ],
        "correct": "B",
        "topic": "Fertilization"
    },
    {
        "stem": "As regards fertilization:",
        "options": [
            "A) It stimulates cleavage.",
            "B) It takes about 24 hours.",
            "C) Determines the sex of the embryo.",
            "D) The sperm has to penetrate the zona pellucid.",
            "E) All of the above."
        ],
        "correct": "E",
        "topic": "Fertilization"
    },
    {
        "stem": "The following are true regarding fertilization EXCEPT:",
        "options": [
            "A) It means formation of the zygote.",
            "B) It takes 6 hours.",
            "C) The sperms reach the ovum by the movement of their tails.",
            "D) It takes place in the ampulla of the Fallopian tube."
        ],
        "correct": "B",
        "topic": "Fertilization"
    },
    {
        "stem": "Human chorionic gonadotrophin hormone (hCG) is secreted by:",
        "options": [
            "A) Hypoplast.",
            "B) Theca interna cells.",
            "C) Inner cell mass.",
            "D) Trophoblast."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },
    {
        "stem": "The hormone used to detect pregnancy is:",
        "options": [
            "A) Estrogen.",
            "B) Progesterone.",
            "C) Human chorionic gonadotrophin.",
            "D) Prolactin."
        ],
        "correct": "C",
        "topic": "Fertilization"
    },
    {
        "stem": "The following are correct regarding IVF (Invitro fertilization) EXCEPT:",
        "options": [
            "A) The ova are collected from the Graffian follicles of the ovary.",
            "B) The ova are placed with the husband's sperms in a petri dish.",
            "C) Two-3 fertilized ova are placed back in the uterus of the wife.",
            "D) It is used if the sperm count is very low (severe oligospermia).",
            "E) It is used if there is uterine tube obstruction."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },
    {
        "stem": "Regarding in vitro fertilization (IVF) one statement is FALSE:",
        "options": [
            "A) It is used in cases of tubal obstruction.",
            "B) Egg retrival means withdrawal of many mature ovarian follicles.",
            "C) Embryo transfer means putting 2-3 embryos in the wife's uterus.",
            "D) Fertilization is done by injection one husband's sperm into the ovum."
        ],
        "correct": "D",
        "topic": "Fertilization"
    },

    # --- V. Cleavage (10 Qs) ---
    {
        "stem": "The cells formed by cleavage are:",
        "options": [
            "A) Granulosa cells.",
            "B) Theca interna cells.",
            "C) Mesoderm.",
            "D) Blastomeres."
        ],
        "correct": "D",
        "topic": "Cleavage"
    },
    {
        "stem": "Morula is:",
        "options": [
            "A) 16 blastomere embryo.",
            "B) 32 blastomere embryo.",
            "C) 8 blastomere embryo.",
            "D) 64 blastomere embryo."
        ],
        "correct": "A",
        "topic": "Cleavage"
    },
    {
        "stem": "The following are true regarding cleavage EXCEPT:",
        "options": [
            "A) It means repeated mitosis of the embryo.",
            "B) Its stages are formation of the morula and blastocyst.",
            "C) It occurs in the uterine tube medial to the ampulla.",
            "D) The morula is the embryo with 4-8 blastomeres.",
            "E) The cells formed are called blastomeres."
        ],
        "correct": "D",
        "topic": "Cleavage"
    },
    {
        "stem": "The following is true regarding cleavage EXCEPT:",
        "options": [
            "A) The morula enters the uterus about the 6th day after fertilization.",
            "B) The blastocyst is formed of inner cell mass and trophoblasts.",
            "C) Trophoblasts form the fetal part of the placenta.",
            "D) The inner cell mass is called the emberyoblasts.",
            "E) The inner cell mass forms the embryo proper."
        ],
        "correct": "A",
        "topic": "Cleavage"
    },
    {
        "stem": "The following is true regarding cleavage EXCEPT:",
        "options": [
            "A) Its stages are morula and blastocyst formation.",
            "B) Zona pellucida persists to allow for implantation.",
            "C) The blastomers are pluripotent cells.",
            "D) The two cell stage embryo occurs 30 hours after implantation."
        ],
        "correct": "B",
        "topic": "Cleavage"
    },
    {
        "stem": "One structure is Not present in the blastocyst:",
        "options": [
            "A) Inner cell mass.",
            "B) Trophoblasts.",
            "C) Blastocele.",
            "D) Decidua."
        ],
        "correct": "D",
        "topic": "Cleavage"
    },
    {
        "stem": "Which structure bounds the cells after fertilization as they compact to form the morula?",
        "options": [
            "A) Zona pellucida.",
            "B) Corona radiate.",
            "C) Pronucleus.",
            "D) Inner cell mass.",
            "E) Outer cell mass."
        ],
        "correct": "A",
        "topic": "Cleavage"
    },
    {
        "stem": "All the following are correct regarding blastocyst EXCEPT:",
        "options": [
            "A) It has a blastocyst cavity.",
            "B) It is surrounded by the zona pellucida and corona radiate.",
            "C) It has an outer cell mass or trophoblasts.",
            "D) It has an inner cell mass from which the embryo is formed."
        ],
        "correct": "B",
        "topic": "Cleavage"
    },
    {
        "stem": "Which of the following events is involved in cleavage of the zygote during week 1 of development?",
        "options": [
            "A) A series of meiotic divisions forming blastomeres.",
            "B) Production of highly differentiated blastomeres.",
            "C) An increased cytoplasmic content of blastomeres.",
            "D) An increase in size of blastomeres.",
            "E) A decrease in size of blastomeres."
        ],
        "correct": "E",
        "topic": "Cleavage"
    },
    {
        "stem": "The following are correct regarding the blastocyst EXCEPT:",
        "options": [
            "A) It has an embryonic pole formed of the inner cell mass.",
            "B) It has a cavity called blastocele.",
            "C) Its peripheral cells are called trophoblasts.",
            "D) The trophoblasts will form the embryo proper.",
            "E) It is surrounded by the zona pellucida."
        ],
        "correct": "D",
        "topic": "Cleavage"
    },

    # --- VI. Decidua and Implantation (13 Qs) ---
    {
        "stem": "Decidua is:",
        "options": [
            "A) Inner cell mass.",
            "B) Trophoblasts.",
            "C) Endometrium after implantation of blastocyst.",
            "D) Penetration of endometrium by blastocyst."
        ],
        "correct": "C",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "The part of the decidua which shares in the formation of the placenta is:",
        "options": [
            "A) Decidua parietalis.",
            "B) Decidua basalis.",
            "C) Decidua capsularis.",
            "D) Decidua marginalis.",
            "E) None of the above."
        ],
        "correct": "B",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "The following are true regarding implantation EXCEPT:",
        "options": [
            "A) It means penetration of the blastocyst into the compact layer of the endometrium.",
            "B) The endometrium after implantation is called chorion.",
            "C) It occurs between 6th to 11th day after fertilization.",
            "D) It occurs in the fundus of the uterus."
        ],
        "correct": "B",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "The normal site of implantation is:",
        "options": [
            "A) Ampulla of the fallopian tube.",
            "B) Upper part of the posterior wall of the uterus.",
            "C) Lateral part of the uterus.",
            "D) Ovary."
        ],
        "correct": "B",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "Concerning implantation, all are true EXCEPT:",
        "options": [
            "A) It is completed in the 12th day after fertilization.",
            "B) Placenta previa is its most common abnormal type.",
            "C) Tubal implantation is its most common extra-uterine type.",
            "D) It occurs only after the appearance of the syncytiotrophoblast.",
            "E) Implantation in lower part of uterus is called ectopic pregnancy."
        ],
        "correct": "E",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "Concerning implantation, the following is CORRECT:",
        "options": [
            "A) Placenta previa centralis leads to postpartum hemorrhage.",
            "B) The chorion is the endometrium after implantation.",
            "C) Blastocyst is superficially implanted at the end of the second week.",
            "D) Ectopic tubal pregnancy leads to tubal rupture and early abortion."
        ],
        "correct": "D",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "Regarding early human development, all are true EXCEPT:",
        "options": [
            "A) Fertilization occurs in the ampullary part of the fallopian tube.",
            "B) Implantation occurs two to three days after fertilization.",
            "C) Implantation occurs in the stage of blastocyst.",
            "D) The yolk sac develops within the blastocyst."
        ],
        "correct": "B",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "Ectopic implantation (pregnancy) may occur in the following sites EXCEPT:",
        "options": [
            "A) Cervix.",
            "B) Abdominal peritoneum.",
            "C) Ovaries.",
            "D) Fundus of the uterus."
        ],
        "correct": "D",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "Ectopic pregnancy means:",
        "options": [
            "A) Implantation of blastocyst in a place other than fundus of uterus.",
            "B) Implantation of blastocyst in the fundus of uterus.",
            "C) Meeting of sperm and ovum.",
            "D) Formation of bilaminar germ disc."
        ],
        "correct": "A",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "The following are correct regarding implantation EXCEPT:",
        "options": [
            "A) It means attachment of the blastocyst to the myometrium.",
            "B) The blastocyst attaches to the endometrium by its embryonic pole.",
            "C) Penetration of the blastocyst into the endometrium is caused by proteolytic enzymes of the trophoblasts.",
            "D) It is completed by the 11th day after fertilization.",
            "E) Cannot occur unless zona pellucida disappears."
        ],
        "correct": "A",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "The following are correct regarding implantation EXCEPT:",
        "options": [
            "A) The normal site is the upper part of the posterior wall of the uterus.",
            "B) Implantation into the lower part of the uterus may lead to placenta previa.",
            "C) It starts 6 days after fertilization.",
            "D) Ectopic pregnancy is due to implantation outside the uterus.",
            "E) The most common site of abnormal implantation is in the ovary."
        ],
        "correct": "E",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "Tubal pregnancy leads to the following EXCEPT:",
        "options": [
            "A) Antepartum hemorrhage.",
            "B) Tubal rupture.",
            "C) Internal hemorrhage.",
            "D) Early abortion."
        ],
        "correct": "A",
        "topic": "Decidua and Implantation"
    },
    {
        "stem": "About implantation (one statement is correct):",
        "options": [
            "A) Blastocyst is superficially implanted at the end of 2nd week.",
            "B) The chorion is the endometrium after implantation.",
            "C) Placenta previa centralis leads to postpartum haemorrhage.",
            "D) Ectopic tubal pregnancy leads to tubal rupture and early abortion."
        ],
        "correct": "D",
        "topic": "Decidua and Implantation"
    },

    # --- VII. Second Week Development (6 Qs) ---
    {
        "stem": "The bilaminar germ disc is formed of:",
        "options": [
            "A) Hypoblast.",
            "B) Epiblast.",
            "C) A & B.",
            "D) None of the above."
        ],
        "correct": "C",
        "topic": "Second Week Development"
    },
    {
        "stem": "Regarding second week of pregnancy, one statement is NOT correct:",
        "options": [
            "A) Formed of ectoderm and mesoderm.",
            "B) Formation of amniotic cavity and yolk sac.",
            "C) Differentiation of trophoblasts into cyto- and syncytiotrophoblasts.",
            "D) Formation of extraembryonic coelom."
        ],
        "correct": "A",
        "topic": "Second Week Development"
    },
    {
        "stem": "All the following are correct regarding bilaminar disc EXCEPT:",
        "options": [
            "A) It has a blastocyst cavity.",
            "B) It is surrounded by the zona pellucida and corona radiate.",
            "C) It implants in the endometrium.",
            "D) It has an outer cell mass or trophoblasts.",
            "E) It has an inner cell mass from which the embryo is formed."
        ],
        "correct": "B",
        "topic": "Second Week Development"
    },
    {
        "stem": "The following are correct regarding the bilaminar germ disc EXCEPT:",
        "options": [
            "A) It consists of endoderm and mesoderm.",
            "B) It is derived from the inner cell mass.",
            "C) It forms the embryo proper.",
            "D) It has the amniotic sac to the ectodermal site.",
            "E) It has the yolk sac to the endodermal site."
        ],
        "correct": "A",
        "topic": "Second Week Development"
    },
    {
        "stem": "The bilaminar germ disc is formed of:",
        "options": [
            "A) Inner cell mass and trophoplasts.",
            "B) Decidua basallis and chorion.",
            "C) Epiblasts and hypoblasts.",
            "D) Epiblasts and chorion.",
            "E) Hypoblasts and decidua."
        ],
        "correct": "C",
        "topic": "Second Week Development"
    },
    {
        "stem": "The following are correct regarding the second week of pregnancy EXCEPT:",
        "options": [
            "A) Cleavage has just started.",
            "B) The inner cell mass is formed of epi- and hypoblasts.",
            "C) The trophoblasts are differentiated into cyto- and syncytiotrophoblasts.",
            "D) The primary mesoderm is differentiated into somatopleuric and splanchnopleuric mesoderm."
        ],
        "correct": "A",
        "topic": "Second Week Development"
    },

    # --- VIII. Chorion and Chorionic Villi (10 Qs) ---
    {
        "stem": "Chorion is:",
        "options": [
            "A) Cytotrophoblasts.",
            "B) Syncytiotrophoblasts.",
            "C) Cyto-, syncytiotrophoblasts and extraembryonic mesoderm.",
            "D) All of the above and yolk sac."
        ],
        "correct": "C",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "The extraembryonic mesoderm is formed from:",
        "options": [
            "A) Cells forming the roof of the amniotic cavity.",
            "B) Cytotrophoblasts.",
            "C) Inner cell mass.",
            "D) Epiblast.",
            "E) Cells of yolk sac."
        ],
        "correct": "E",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "The rule of the trophoblast of the blastocyst include the following EXCEPT:",
        "options": [
            "A) Enclosure of the blastocyst cavity.",
            "B) Production of hormones.",
            "C) Formation of the embryo proper.",
            "D) Invasion of endometrial epithelium."
        ],
        "correct": "C",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "Concerning the chorionic villi, all are false EXCEPT:",
        "options": [
            "A) The 2ry villi contain only trophoblast.",
            "B) The 3ry villi contain blood capillaries.",
            "C) The nourishing villi fix the zygote.",
            "D) The whole surface of the blastocyst contains villi till the end of pregnancy.",
            "E) The chorion leave will form the fetal component of the placenta."
        ],
        "correct": "B",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "Which statement concerning the chorionic villi is correct?",
        "options": [
            "A) Primary villi consist of syncytiotrophoblast only.",
            "B) Most anchoring villi are side branches from the stem villus.",
            "C) The main stem villus is called the absorbing villus.",
            "D) Secondary villi do not contain mesoderm.",
            "E) Tertiary villi consist of 2 layers of trophoblast, mesoderm and blood vessels."
        ],
        "correct": "E",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "The following are correct as regard the chorionic villi EXCEPT:",
        "options": [
            "A) The primary villi contain trophoblasts only.",
            "B) The tertiary villi contain blood capillaries.",
            "C) The whole surface of the blastocyst possesses villi till the end of pregnancy.",
            "D) The anchoring villi fixes the embryo.",
            "E) The chorion frondosum forms the fetal part of placenta."
        ],
        "correct": "C",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "Tertiary villi are formed of all the following EXCEPT:",
        "options": [
            "A) Decidua.",
            "B) Trophoblasts.",
            "C) Extraembryonic mesoderm.",
            "D) Blood vessels."
        ],
        "correct": "A",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "Secondary chorionic villi are:",
        "options": [
            "A) Cyto- and syncytotrophoblasts.",
            "B) Cyto-, syncytioblasts and extraembryonic (primary) mesoderm.",
            "C) Trophoblasts and blood vessels.",
            "D) None of the above."
        ],
        "correct": "B",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "The villi that fix the embryo are named:",
        "options": [
            "A) Nourishing villi.",
            "B) Chorion leavae.",
            "C) Chorion frundosum.",
            "D) Anchoring villi."
        ],
        "correct": "D",
        "topic": "Chorion and Chorionic Villi"
    },
    {
        "stem": "During week 2 of development, the embryoblast receives its nutrients via:",
        "options": [
            "A) Diffusion.",
            "B) Osmosis.",
            "C) Reverse osmosis.",
            "D) Fetal capillaries.",
            "E) Yolk sac nourishment."
        ],
        "correct": "A",
        "topic": "Chorion and Chorionic Villi"
    },

    # --- IX. Third week development (Gastrulation) (16 Qs) ---
    {
        "stem": "The process by which the bilaminar embryonic disc is converted into a trilaminar embryonic disc is called:",
        "options": [
            "A) Cleavage.",
            "B) Gastrulation.",
            "C) Folding of the embryo.",
            "D) Implantation.",
            "E) Fertilization."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "All are true regarding the human trilaminar embryonic disc EXCEPT:",
        "options": [
            "A) It is formed during the early part of the third week.",
            "B) It is composed of three primary germ layers.",
            "C) It is initially flat and wide at the cranial end.",
            "D) It is characterized by the primitive streak cranially.",
            "E) It has two spots devoid of mesoderm."
        ],
        "correct": "D",
        "topic": "Third Week Development"
    },
    {
        "stem": "Concerning the intraembryonic mesoderm, all are true EXCEPT:",
        "options": [
            "A) Paraxial mesoderm gives the somites.",
            "B) Intermediate mesoderm gives the suprarenal medulla.",
            "C) Gives the vertebral column.",
            "D) Gives the ribs."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "Concerning intraembryonic mesoderm, all are true EXCEPT:",
        "options": [
            "A) Intermediate mesoderm gives the urogenital organs.",
            "B) It appears next to the extraembryonic mesoderm.",
            "C) Paraxial mesoderm lies next to the notochord.",
            "D) Mesoderm at caudal part of the embryonic plate forms the septum transversum.",
            "E) Lateral plate mesoderm divides into somatic and splanchnic layers."
        ],
        "correct": "D",
        "topic": "Third Week Development"
    },
    {
        "stem": "Concerning the embryonic plate, all are true EXCEPT:",
        "options": [
            "A) The primitive streak develops from ectoderm.",
            "B) The prochordal plate develops near its caudal end.",
            "C) No mesoderm develops in the region of the prochordal plate.",
            "D) The secondary mesoderm develops from the primitive streak."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "The intraembryonic mesoderm differentiates into:",
        "options": [
            "A) Somatopleure.",
            "B) Body stalk.",
            "C) Lateral plate.",
            "D) Splanchnopleure.",
            "E) Yolk sac."
        ],
        "correct": "C",
        "topic": "Third Week Development"
    },
    {
        "stem": "Concerning notochord, all the following are true EXCEPT:",
        "options": [
            "A) Forms the embryonic basis of the axial skeleton.",
            "B) Initially, it is formed cranially and develops caudally as the embryo grows.",
            "C) It acts as an organizer for the CNS.",
            "D) Lies in the midline between the roof of the yolk sac and the embryonic ectoderm."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "The following statements are true as regard the primitive streak EXCEPT:",
        "options": [
            "A) It extends to the cranial end of the embryo.",
            "B) It gives rise to cells which migrate cranially to form the notochord.",
            "C) It gives rise to cells which migrate laterally to form the intraembryonic mesoderm.",
            "D) Its terminal part shows the primitive node."
        ],
        "correct": "A",
        "topic": "Third Week Development"
    },
    {
        "stem": "Concerning the primitive streak, all are true EXCEPT:",
        "options": [
            "A) Derived from ectodermal cells.",
            "B) Starts development at the cranial part of the embryonic plate.",
            "C) Lays down the mesodermal germ layer.",
            "D) Forms the notochord."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "The point of contact between endoderm and ectoderm at the caudal end of the embryonic disc is called:",
        "options": [
            "A) Oral membrane.",
            "B) Cloacal membrane.",
            "C) Notochord.",
            "D) Neural groove.",
            "E) Intraembryonic coelom."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "The cloacal membrane is formed of:",
        "options": [
            "A) Endoderm and mesoderm.",
            "B) Ectoderm and endoderm.",
            "C) Endoderm and mesoderm.",
            "D) Endoderm only.",
            "E) Ectoderm only."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "Functions of notochord are all of the following EXCEPT:",
        "options": [
            "A) Formation of nucleus pulposus.",
            "B) Induction of ectoderm to form neural tube.",
            "C) Formation of primordium of axial skeleton.",
            "D) Formation of somites."
        ],
        "correct": "D",
        "topic": "Third Week Development"
    },
    {
        "stem": "The following are correct regarding the human trilaminar embryonic disc:",
        "options": [
            "A) It is formed during the third week.",
            "B) It is composed of three primary germ layers.",
            "C) It is initially flat and wide at the cranial end.",
            "D) It is characterized by the primitive streak caudally.",
            "E) It has one spot devoid of mesoderm."
        ],
        "correct": "E",
        "topic": "Third Week Development"
    },
    {
        "stem": "The following are correct regarding the notochord EXCEPT:",
        "options": [
            "A) It forms the embryonic basis of the axial skeleton.",
            "B) It develops in the second week of pregnancy.",
            "C) It affects the overlying ectoderm to differentiate into neural tissue.",
            "D) It lies in the midline between the roof of the yolk sac and the embryonic ectoderm.",
            "E) It is initially formed caudally and develops cranially as the embryo grows."
        ],
        "correct": "B",
        "topic": "Third Week Development"
    },
    {
        "stem": "The following are correct regarding the notochord EXCEPT:",
        "options": [
            "A) It forms the embryonic basis of the axial skeleton.",
            "B) It is initially formed caudally and develops cranially as the embryo grows.",
            "C) It affects the overlying ectoderm to differentiate into neural tissue.",
            "D) It lies in the midline between the roof of the yolk sac and the embryonic ectoderm.",
            "E) It extends the whole length of the embryo."
        ],
        "correct": "E",
        "topic": "Third Week Development"
    },
    {
        "stem": "The notochord has all of the following functions EXCEPT:",
        "options": [
            "A) Development of immune system.",
            "B) CNS development.",
            "C) Vertebral column development.",
            "D) Forms anatomic midline.",
            "E) Forms nucleus pulposis."
        ],
        "correct": "A",
        "topic": "Third Week Development"
    },

    # --- X. Derivatives of the Three Germ Layers (11 Qs) ---
    {
        "stem": "Which of the following structures develops from endoderm?",
        "options": [
            "A) Suprarenal gland.",
            "B) Muscle.",
            "C) Gonads.",
            "D) Hair.",
            "E) Mucosa of the respiratory tract."
        ],
        "correct": "E",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "All the following are derivatives of the surface ectoderm EXCEPT:",
        "options": [
            "A) The lens of the eye.",
            "B) The iris of the eye.",
            "C) The epidermis.",
            "D) The anterior lobe of the pituitary gland."
        ],
        "correct": "B",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "Derivatives of endoderm include the following EXCEPT:",
        "options": [
            "A) Thyroid gland.",
            "B) Epithelium of the pharynx.",
            "C) Epithelium of the trachea.",
            "D) Glands of the gastrointestinal tract.",
            "E) Nails."
        ],
        "correct": "E",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "Ectoderm derivatives include the following EXCEPT:",
        "options": [
            "A) The brain.",
            "B) The hair.",
            "C) The salivary glands.",
            "D) The heart.",
            "E) The pituitary gland."
        ],
        "correct": "D",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "The following structures develop from mesoderm EXCEPT:",
        "options": [
            "A) Spleen.",
            "B) Heart.",
            "C) Liver glandular tissue.",
            "D) Serous membranes.",
            "E) Diaphragm."
        ],
        "correct": "C",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "Which structure is derived from the same embryonic primordium as the dorsal root ganglia?",
        "options": [
            "A) Gonads.",
            "B) Adrenal medulla.",
            "C) Liver.",
            "D) Kidney.",
            "E) Pineal gland."
        ],
        "correct": "B",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "The following are derivatives of the neural crest EXCEPT:",
        "options": [
            "A) Sensory ganglia.",
            "B) Cortex of the adrenal gland.",
            "C) Bones of the pharyngeal arches.",
            "D) Meninges of the brain and spinal cord."
        ],
        "correct": "B",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "The paraxial mesoderm gives rise to:",
        "options": [
            "A) Muscles of the upper limb.",
            "B) Muscles of the neck region.",
            "C) Vertebrae.",
            "D) Urinary system."
        ],
        "correct": "C",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "Concerning the paraxial mesoderm, all the following are true EXCEPT:",
        "options": [
            "A) It is continues medially with the intermediate mesoderm.",
            "B) It is separated from the lateral plate mesoderm by the intermediate cell mass.",
            "C) It gives rise to the vertebral column.",
            "D) It gives rise to mesodermal somites which form the axial musculature."
        ],
        "correct": "A",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "The following structures are ectodermal in origin EXCEPT:",
        "options": [
            "A) Hair.",
            "B) CNS.",
            "C) Nails.",
            "D) Dermis.",
            "E) Epidermis."
        ],
        "correct": "D",
        "topic": "Derivatives of Germ Layers"
    },
    {
        "stem": "Which structure is derived from the same embryonic primordium as the kidney?",
        "options": [
            "A) Liver.",
            "B) Adrenal medulla.",
            "C) Gonads.",
            "D) Epidermis.",
            "E) Pineal gland."
        ],
        "correct": "C",
        "topic": "Derivatives of Germ Layers"
    },

    # --- XI. Folding (6 Qs) ---
    {
        "stem": "Concerning folding, all are true EXCEPT:",
        "options": [
            "A) Occurs at the 5th week of IUL.",
            "B) It occurs in an antero-posterior and side to side direction.",
            "C) Transforms the embryonic plate into an embryo.",
            "D) Reacts mostly on the yolk sac.",
            "E) Results in the formation of the umbilical cord."
        ],
        "correct": "A",
        "topic": "Folding"
    },
    {
        "stem": "Concerning folding, all are true EXCEPT:",
        "options": [
            "A) Folding occurs also in the caudal end of the embryonic plate.",
            "B) The part of the yolk sac inside the head fold is called the foregut.",
            "C) The pericardial cavity becomes posterior to the cardiogenic plate after folding.",
            "D) The head fold contains the stomodium."
        ],
        "correct": "C",
        "topic": "Folding"
    },
    {
        "stem": "Regarding folding, all are true EXCEPT:",
        "options": [
            "A) The two lateral folds meet the cranio-caudal folds at the umbilical cord.",
            "B) The lateral folds enclose the midgut.",
            "C) The lateral folding is completed in the second half of pregnancy.",
            "D) The intraembryonic coelom becomes well defined."
        ],
        "correct": "C",
        "topic": "Folding"
    },
    {
        "stem": "All the following are results of head folding EXCEPT:",
        "options": [
            "A) The brain becomes cephalic in position.",
            "B) The septum transversum lies caudal to the heart.",
            "C) The allantois lies ventral to the hindgut.",
            "D) Formation of the foregut."
        ],
        "correct": "C",
        "topic": "Folding"
    },
    {
        "stem": "In folding of embryo:",
        "options": [
            "A) It occurs in the 5th week of intrauterine life.",
            "B) It occurs in the head, tail and laterally.",
            "C) As result of folding, part of the amniontic cavity forms the gut.",
            "D) One of its result, the body stalk will shift ventral to the embryo."
        ],
        "correct": "D",
        "topic": "Folding"
    },
    {
        "stem": "The following is true regarding the results of folding of the embryo EXCEPT:",
        "options": [
            "A) It results in cylindrical embryo.",
            "B) It results in rapid growth of the placenta.",
            "C) It leads to incorporation of the yolk sac into the embryo.",
            "D) The brain forms the most cephalic part of the embryo.",
            "E) The cloaca and allantois become ventral in position."
        ],
        "correct": "B",
        "topic": "Folding"
    },

    # --- XII. Fetal Membranes: 1. Amnion (6 Qs) ---
    {
        "stem": "The amnion:",
        "options": [
            "A) Contains the amniotic fluid.",
            "B) Contains about 2 litters at the end of pregnancy.",
            "C) Its floor is formed of endoderm.",
            "D) It shares in the development of gastrointestinal tract."
        ],
        "correct": "A",
        "topic": "Amnion"
    },
    {
        "stem": "All the following statements regarding the amniotic fluid are true EXCEPT:",
        "options": [
            "A) It allows for free growth and movement of the fetus.",
            "B) It has constant temperature around the fetus.",
            "C) It stimulate suckling reflex.",
            "D) It transmits maternal antibodies to the fetus.",
            "E) It permits normal development to the lung."
        ],
        "correct": "D",
        "topic": "Amnion"
    },
    {
        "stem": "Concerning the amnion, all are true EXCEPT:",
        "options": [
            "A) Its volume is about one liter at birth.",
            "B) Its cavity appears on the 7th day after fertilization.",
            "C) Its membrane covers the placenta.",
            "D) Great decrease of its fluid is called oligohydramnios."
        ],
        "correct": "B",
        "topic": "Amnion"
    },
    {
        "stem": "The floor of the amniotic cavity is formed of:",
        "options": [
            "A) Hypoblast.",
            "B) Epiblast.",
            "C) Extraembryonic mesoderm.",
            "D) Trophoblasts."
        ],
        "correct": "B",
        "topic": "Amnion"
    },
    {
        "stem": "Concerning the amnion, all are true EXCEPT:",
        "options": [
            "A) It wraps the umbilical cord.",
            "B) The amniotic fluid is 1.5 - 2 liters at full term.",
            "C) Polyhydramnios may be associated with oesophageal atresia.",
            "D) Oligohydramnios may hinder the development of the fetus."
        ],
        "correct": "B",
        "topic": "Amnion"
    },
    {
        "stem": "Cells forming the roof of the amniotic cavity is named:",
        "options": [
            "A) Hypoblasts.",
            "B) Epiblasts.",
            "C) Amnioblasts.",
            "D) Somatopleuric mesoderm."
        ],
        "correct": "C",
        "topic": "Amnion"
    },

    # --- 2. Yolk Sac (7 Qs) ---
    {
        "stem": "Regarding the yolk sac, all are true EXCEPT:",
        "options": [
            "A) Its wall is derived from endoderm.",
            "B) Its intraembryonic part forms the gut tube.",
            "C) Its cranial part gives the allantois.",
            "D) It is linked to the development of the genital system."
        ],
        "correct": "C",
        "topic": "Yolk Sac"
    },
    {
        "stem": "Which of the following statements is not correct for the yolk sac?",
        "options": [
            "A) Acts as a nutritional store.",
            "B) Appears at the beginning of the 2nd week of I.U.L.",
            "C) Shows great changes as a result of folding.",
            "D) Sends a diverticulum into the body stalk.",
            "E) Its covering mesoderm is a site for angioblast (blood cells) formation."
        ],
        "correct": "B",
        "topic": "Yolk Sac"
    },
    {
        "stem": "Concerning Meckle's diverticulum, all are true EXCEPT:",
        "options": [
            "A) It occurs in 2% of people.",
            "B) It is two inches long.",
            "C) It is two feet from the ileocaecal junction.",
            "D) Usually, it is found in the mesenteric border of the intestine.",
            "E) May contain accessory gastric or pancreatic tissues."
        ],
        "correct": "D",
        "topic": "Yolk Sac"
    },
    {
        "stem": "The following are congenital anomalies of the yolk sac EXCEPT:",
        "options": [
            "A) Vitellointestinal duct fistula.",
            "B) Meckle's diverticulum.",
            "C) Persistant fibrous band.",
            "D) Urachal sinus."
        ],
        "correct": "D",
        "topic": "Yolk Sac"
    },
    {
        "stem": "Regarding the yolk sac all are false EXCEPT:",
        "options": [
            "A) Its wall is derived from ectoderm.",
            "B) Its cranial part gives the allantois.",
            "C) Its intraembryonic part forms the gut tube.",
            "D) It is linked to the development of genital system.",
            "E) Its extraembryonic part will form anal canal."
        ],
        "correct": "C",
        "topic": "Yolk Sac"
    },
    {
        "stem": "Abnormalities of the yolk sac include all the following EXCEPT:",
        "options": [
            "A) Congenital umbilical fecal fistula.",
            "B) Meckel's diverticulum.",
            "C) Congenital umbilical sinus.",
            "D) Urachal fistula.",
            "E) Fibrous band connecting the midgut with the external embryonic yolk sac."
        ],
        "correct": "D",
        "topic": "Yolk Sac"
    },
    {
        "stem": "As regard the yolk sac which of the following is correct:",
        "options": [
            "A) It is situated dorsal to the embryo.",
            "B) It is lined with ectoderm.",
            "C) It is filled with amniotic fluid.",
            "D) It is connected to the midgut by the yolk stalk."
        ],
        "correct": "D",
        "topic": "Yolk Sac"
    },

    # --- 3. Allantois (5 Qs) ---
    {
        "stem": "The following are fetal membranes EXCEPT:",
        "options": [
            "A) Chorion.",
            "B) Yolk sac.",
            "C) Decidua.",
            "D) Amnion.",
            "E) Allantois."
        ],
        "correct": "C",
        "topic": "Allantois"
    },
    {
        "stem": "Persistent allantois gives one of the following:",
        "options": [
            "A) Urachal fistula.",
            "B) Omphalocele.",
            "C) Utrovesical fistula.",
            "D) Meckle's diverticulum.",
            "E) Ectopia vesica."
        ],
        "correct": "A",
        "topic": "Allantois"
    },
    {
        "stem": "The median umbilical fold overlies remnants of:",
        "options": [
            "A) Urachus.",
            "B) Yolk sac.",
            "C) Umbilical cord.",
            "D) Amniotic membrane.",
            "E) Umbilical blood vessels."
        ],
        "correct": "A",
        "topic": "Allantois"
    },
    {
        "stem": "The abnormality which is due to partial persistence of the allantois is:",
        "options": [
            "A) Congenital umbilical hernia.",
            "B) Meckle's diverticulum.",
            "C) Urachal sinus.",
            "D) Urethral fistula."
        ],
        "correct": "C",
        "topic": "Allantois"
    },
    {
        "stem": "The allantois:",
        "options": [
            "A) Arises from the cranial part of the yolk sac.",
            "B) It opens in the cloaca.",
            "C) It is the lateral umbilical ligament in the adult.",
            "D) None of the above."
        ],
        "correct": "B",
        "topic": "Allantois"
    },

    # --- 4. Umbilical Cord (7 Qs) ---
    {
        "stem": "Concerning the umbilical cord, all are false EXCEPT:",
        "options": [
            "A) Attached to the maternal surface of the placenta.",
            "B) Wrapped by the amniotic membrane.",
            "C) Contains one artery and two veins.",
            "D) Contains yolk stalk till the end of pregnancy.",
            "E) Has a length of 25 cm.",
            "F) It contains a pair of umbilical arteries and a pair of umbilical veins at birth."
        ],
        "correct": "B",
        "topic": "Umbilical Cord"
    },
    {
        "stem": "As regards the primitive umbilical cord, all the following are correct EXCEPT:",
        "options": [
            "A) The yolk stalk contains vitelline vessels.",
            "B) It is not covered with amniotic ectoderm.",
            "C) It contains Wharton's jelly.",
            "D) It extends from the primitive umbilical ring to the chorion frondosum."
        ],
        "correct": "B",
        "topic": "Umbilical Cord"
    },
    {
        "stem": "Which of the following statements is NOT correct for the umbilical cord?",
        "options": [
            "A) Contains the allantoic diverticulum.",
            "B) Contains mesoderm of the body stalk.",
            "C) Has a covering sheath of amnion.",
            "D) Contains 2 veins and one artery.",
            "E) Contains the vitelline duct in early stages.",
            "F) Attaches the fetus to the allantois."
        ],
        "correct": "D",
        "topic": "Umbilical Cord"
    },
    {
        "stem": "Which of the following statements is correct for the umbilical vein?",
        "options": [
            "A) Carries non oxygenated (venous) blood.",
            "B) Carries blood from the foetus to the placenta.",
            "C) It is paired in the umbilical cord.",
            "D) After birth, its oblitration forms the ligamentum teres of the liver."
        ],
        "correct": "D",
        "topic": "Umbilical Cord"
    },
    {
        "stem": "After birth, the following are normal changes in the umbilical cord EXCEPT:",
        "options": [
            "A) The yolk sac disappears.",
            "B) The median umbilical ligament is due to obliterated urachus.",
            "C) The medial umbilical ligament is due to obliterated umbilical artery.",
            "D) The lateral umbilical ligament presents the obliterated umbilical vein."
        ],
        "correct": "D",
        "topic": "Umbilical Cord"
    },
    {
        "stem": "As regards the primitive umbilical cord all the following are correct EXCEPT:",
        "options": [
            "A) It contains body stalk containing allantois and umbilical vessels.",
            "B) It contains the yolk sac containing vitelline vessels.",
            "C) It is covered with amniotic ectoderm.",
            "D) It contains Wharton's jelly.",
            "E) It extends from the primitive umbilical ring to the chorion frondosum."
        ],
        "correct": "B",
        "topic": "Umbilical Cord"
    },
    {
        "stem": "The following are true regarding the umbilical cord EXCEPT:",
        "options": [
            "A) It is attached near the center of the placenta.",
            "B) It is wrapped by the amniotic membrane.",
            "C) It has a length of 25 cm.",
            "D) At early formation, it contains the yolk stalk."
        ],
        "correct": "C",
        "topic": "Umbilical Cord"
    },

    # --- 5. Placenta (14 Qs) ---
    {
        "stem": "The normal site of placenta is:",
        "options": [
            "A) Upper segment of the uterus.",
            "B) Cervix of the uterus.",
            "C) Lower segment of the uterus.",
            "D) Vagina.",
            "E) Middle segment of the uterus."
        ],
        "correct": "A",
        "topic": "Placenta"
    },
    {
        "stem": "The fetal part of the placenta is formed from:",
        "options": [
            "A) Chorion leave.",
            "B) Chorion frondosum.",
            "C) Decidua basalis.",
            "D) Decidua parietalis.",
            "E) Decidua marginalis."
        ],
        "correct": "B",
        "topic": "Placenta"
    },
    {
        "stem": "Concerning the placenta, all are false EXCEPT:",
        "options": [
            "A) Derived from a fetal part called chorion leave.",
            "B) Derived from a maternal part called decidua capsularis.",
            "C) The umbilical cord is attached to the fetal surface.",
            "D) Its maternal surface covered by amniotic membrane.",
            "E) It has one type of circulation."
        ],
        "correct": "C",
        "topic": "Placenta"
    },
    {
        "stem": "Concerning the placenta, all are true EXCEPT:",
        "options": [
            "A) Its fetal part is the chorion frondosum.",
            "B) Its fetal surface is covered by amnion.",
            "C) It can produce antibodies.",
            "D) It can produce gonadotrophic hormones."
        ],
        "correct": "C",
        "topic": "Placenta"
    },
    {
        "stem": "Regarding the placenta, all are true EXCEPT:",
        "options": [
            "A) It develops from decidua basalis and chorion frondosum.",
            "B) It is covered by amnion on its fetal surface.",
            "C) It is divided into 15 - 20 lobes on its fetal surface.",
            "D) The umbilical cord is attached to its fetal surface.",
            "E) It produces progesterone."
        ],
        "correct": "C",
        "topic": "Placenta"
    },
    {
        "stem": "Concerning the placenta at full term, all are true EXCEPT:",
        "options": [
            "A) 20 cm in diameter.",
            "B) About half kg. in weight.",
            "C) 3 cm thick at its center.",
            "D) Not covered by amnion."
        ],
        "correct": "D",
        "topic": "Placenta"
    },
    {
        "stem": "Concerning abnormal placentation, all the following are true EXCEPT:",
        "options": [
            "A) When the umbilical cord is marginal, it is called batelledor.",
            "B) Twins always share single placenta.",
            "C) Placenta previa is caused by implantation in the lower uterine segment.",
            "D) Abnormal forms of placentae may cause antepartum haemorrhage."
        ],
        "correct": "B",
        "topic": "Placenta"
    },
    {
        "stem": "The placental barrier during pregnancy include all the following EXCEPT:",
        "options": [
            "A) Syncytiotrophoblast.",
            "B) Cytotrophoblast.",
            "C) Primary mesoderm.",
            "D) Fetal blood vessels.",
            "E) Amniotic membrane covering."
        ],
        "correct": "E",
        "topic": "Placenta"
    },
    {
        "stem": "At late pregnancy, the placental barrier is formed of all the following EXCEPT:",
        "options": [
            "A) Endothelium of fetal blood vessels.",
            "B) Fibrinoid material.",
            "C) Cytotrophoblast.",
            "D) Syncytiotrophoblast.",
            "E) Mesoderm of the villus."
        ],
        "correct": "C",
        "topic": "Placenta"
    },
    {
        "stem": "At early pregnancy the placental barrier is formed by all the following EXCEPT:",
        "options": [
            "A) Endotheluim of fetal blood vessels.",
            "B) Primary mesoderm.",
            "C) Fibrinoid material.",
            "D) Cytotrophoblast.",
            "E) Syncytiotrophoblast."
        ],
        "correct": "C",
        "topic": "Placenta"
    },
    {
        "stem": "The cause of placenta previa is:",
        "options": [
            "A) Implantation at lower uterine segment.",
            "B) Cervical implantation.",
            "C) Tubal implantation.",
            "D) Implantation at the fundus of the uterus.",
            "E) It leads to post-partum haemorrhage."
        ],
        "correct": "A",
        "topic": "Placenta"
    },
    {
        "stem": "Complications of placenta previa are:",
        "options": [
            "A) Abortion.",
            "B) Antepartum haemorrhage.",
            "C) Postpartum haemorrhage.",
            "D) A & B."
        ],
        "correct": "D",
        "topic": "Placenta"
    },
    {
        "stem": "Placental abnormalities leading to postpartum hemorrhage are:",
        "options": [
            "A) Placenta accrete, placenta percreta.",
            "B) Accessory placenta.",
            "C) Placenta previa.",
            "D) B + C.",
            "E) A + B."
        ],
        "correct": "E",
        "topic": "Placenta"
    },
    {
        "stem": "As regard the placenta:",
        "options": [
            "A) Its fetal origin is the chorion leva.",
            "B) Its maternal origin is deciduas parietalis.",
            "C) It secrets hormones.",
            "D) Its intervellous space contains fetal blood.",
            "E) It doesn't lead to malposition of the fetus."
        ],
        "correct": "C",
        "topic": "Placenta"
    },

    # --- XIII. Multiple Pregnancy (2 Qs) ---
    {
        "stem": "All are true concerning multiple pregnancy EXCEPT:",
        "options": [
            "A) Dizygotic twins arise from two separate ova produced simultaneously and fertilized by the two sperms.",
            "B) The differences between monozygotic twins are genetic in origin.",
            "C) Monozygotic twins may share a common chorionic sac.",
            "D) Twins of different sexes arise from different zygotes.",
            "E) Conjoined twins are produced by incomplete splitting of the inner cell mass."
        ],
        "correct": "B",
        "topic": "Multiple Pregnancy"
    },
    {
        "stem": "All are true concerning multiple pregnancy EXCEPT:",
        "options": [
            "A) Dizygotic twins may be of different sex.",
            "B) Monozygotic twins have different finger prints.",
            "C) Monozygotic twins have one placenta.",
            "D) Dizygotic twins are produced by two ova and two sperms."
        ],
        "correct": "B",
        "topic": "Multiple Pregnancy"
    },

    # --- XIV. Teratogenicity (7 Qs) ---
    {
        "stem": "Concerning teratogenicity, all are true EXCEPT:",
        "options": [
            "A) A teratogen is any agent that can produce malformation in the developing embryo.",
            "B) The most sensitive stage in human development is the fetal period.",
            "C) Congenital malformation can be due to exposure of the ovum to a teratogen.",
            "D) Exposure to a teratogen before implantation could interrupt pregnancy.",
            "E) Certain teratogens cause specific anomalies."
        ],
        "correct": "B",
        "topic": "Teratogenicity"
    },
    {
        "stem": "Congenital malformations are probably caused by the following EXCEPT:",
        "options": [
            "A) Chromosomal aberrations.",
            "B) Genetic abnormality.",
            "C) Young maternal age.",
            "D) Irradiation."
        ],
        "correct": "C",
        "topic": "Teratogenicity"
    },
    {
        "stem": "The following are true regarding congenital anomalies EXCEPT:",
        "options": [
            "A) It is always single.",
            "B) It means structural abnormalities of the fetus present at birth.",
            "C) Its incidence is about 3% live births.",
            "D) It is due to genetic, environmental, or multifactorial causes.",
            "E) It may be minor or major."
        ],
        "correct": "A",
        "topic": "Teratogenicity"
    },
    {
        "stem": "Non-invasive methods of prenatal diagnosis are the following EXCEPT:",
        "options": [
            "A) Amniocentesis.",
            "B) Maternal alfa fetoprotein (AFP) estimation.",
            "C) Maternal triple test.",
            "D) Ultrasound."
        ],
        "correct": "A",
        "topic": "Teratogenicity"
    },
    {
        "stem": "One of the following is a non-invasive method of prenatal diagnosis:",
        "options": [
            "A) Amniocentesis.",
            "B) Chorionic villus sampling (CVS).",
            "C) Fetal blood sampling.",
            "D) Ultrasonography."
        ],
        "correct": "D",
        "topic": "Teratogenicity"
    },
    {
        "stem": "The following are true regarding congenital anomalies EXCEPT:",
        "options": [
            "A) It is always single.",
            "B) It means structural abnormalities of the fetus present at birth.",
            "C) Its incidence is about 3% live births.",
            "D) It is due to genetic, environmental, or multifactorial causes.",
            "E) It may be minor or major."
        ],
        "correct": "A",
        "topic": "Teratogenicity"
    },
    {
        "stem": "Programmed cell death means:",
        "options": [
            "A) Cancer.",
            "B) Mitosis.",
            "C) Meiosis.",
            "D) Apoptosis."
        ],
        "correct": "D",
        "topic": "Teratogenicity"
    }
]

print(f"Total MCQs loaded: {len(mcqs)}")

# Let's generate the markdown content
header = """# embryology Qs bank.pdf

- **Source File**: `embryology Qs bank.pdf`
- **File Type**: Scanned PDF Booklet (Dr. Ayman Ahmed Khanfour)
- **Total Pages / Slides**: 37
- **Assiut Tag**: Department, QBank, Embryology
- **Discipline**: Embryology
- **Total Questions**: 182

---

"""

body = []
for idx, q in enumerate(mcqs, 1):
    q_str = f"### Question {idx}\n\n"
    q_str += f"{q['stem']}\n\n"
    for opt in q['options']:
        q_str += f"- **{opt[:2]}** {opt[3:].strip()}\n"
    q_str += f"\n**Correct Answer**: {q['correct']}\n\n---\n"
    body.append(q_str)

full_content = header + "\n".join(body)

output_path = "Markdown_Questions/56_embryology_Qs_bank.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Successfully wrote {len(mcqs)} questions to {output_path}")
