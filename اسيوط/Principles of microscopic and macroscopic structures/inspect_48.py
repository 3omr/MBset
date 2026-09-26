import fitz

doc = fitz.open('01- Principles of microscopic and macroscopic structures/anatomy department.pdf')

print('--- P4 Digestive ---')
print(doc[3].get_text())
print(doc[4].get_text())

print('--- P6-9 Lectures 38-41 ---')
for p in range(5, 9):
    print(f'=== Page {p+1} ===')
    print(doc[p].get_text())

print('--- P11-15 Sample Slides ---')
for p in range(10, 15):
    print(f'=== Page {p+1} ===')
    print(doc[p].get_text())
