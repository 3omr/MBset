import re

path = 'Markdown_Questions/73_زقازيق_Mcq.md'
c = open(path, encoding='utf-8').read()

# Fix Q31
q31_old = rf'### Question 31\n\nThe general name for an alternate pathway of blood flow in or around an organ, around 2 joint, or past an obstruction is called:\n\n\n\*\*Correct Answer\*\*: E'
q31_new = """### Question 31

The general name for an alternate pathway of blood flow in or around an organ, around a joint, or past an obstruction is called:

- **A)** an arteriovenous anastomosis
- **B)** a periarticular network
- **C)** a perivascular plexus
- **D)** a venous plexus
- **E)** collateral circulation

**Correct Answer**: E"""

c = re.sub(q31_old, q31_new, c)

# Fix Q51
q51_old = rf'### Question 51\n\nWhat is the anatomical term for wide, sheet-like tendons\n\n- \*\*A\)\*\* Endomysium\.\n- \*\*B\)\*\* Tendons\. c, Epimysium\.\n- \*\*C\)\*\* Aponeuroses\.\n\n\*\*Correct Answer\*\*: D'
q51_new = """### Question 51

What is the anatomical term for wide, sheet-like tendons:

- **A)** Endomysium
- **B)** Tendons
- **C)** Epimysium
- **D)** Aponeuroses

**Correct Answer**: D"""

c = re.sub(q51_old, q51_new, c)

# Fix Q63
q63_old = rf'### Question 63\n\nWhich of the following can best be used to distinguish cardiac muscle from smooth muscle\n\n\n\*\*Correct Answer\*\*: A'
q63_new = """### Question 63

Which of the following can best be used to distinguish cardiac muscle from smooth muscle:

- **A)** Cardiac muscle is involuntary
- **B)** Cardiac muscle, unlike smooth muscle, has peripheral nuclei
- **C)** Cardiac muscle has a single nucleus, smooth muscle has peripheral nuclei
- **D)** It is striated

**Correct Answer**: D"""

c = re.sub(q63_old, q63_new, c)

# Fix Q89
q89_old = rf'### Question 89\n\nThe only moveable joint in the head is the >\n\n\n\*\*Correct Answer\*\*: B'
q89_new = """### Question 89

The only moveable joint in the head is the:

- **A)** Sagittal suture
- **B)** Lambdoid suture
- **C)** Gomphosis
- **D)** Temporomandibular joint
- **E)** None of the above

**Correct Answer**: D"""

c = re.sub(q89_old, q89_new, c)

open(path, 'w', encoding='utf-8').write(c)
print('Updated Q31, Q51, Q63, Q89 in 73_زقازيق_Mcq.md!')
