import json, re

with open('scratch_56_booklet_pages.json') as f:
    pages = json.load(f)

# The chapters and question counts
# 1. Spermatogenesis: 10
# 2. Oogenesis: 12
# 3. Ovarian Cycle: 12
# 4. Menstrual Cycle: 7
# 5. Fertilization: 21
# 6. Cleavage: 10
# 7. Decidua and Implantation: 13
# 8. Second Week Development: 6
# 9. Chorion and Chorionic Villi: 10
# 10. Third Week Development: 16
# 11. Derivatives of the Three Germ Layers: 11
# 12. Folding: 6
# 13. Fetal Membranes - Amnion: 6
# 14. Fetal Membranes - Yolk Sac: 7
# 15. Fetal Membranes - Allantois: 5
# 16. Fetal Membranes - Umbilical Cord: 7
# 17. Placenta: 14
# 18. Multiple Pregnancy: 2
# 19. Teratogenicity: 7

# Keys
keys = {
    'Spermatogenesis': ['C', 'D', 'A', 'D', 'B', 'C', 'C', 'E', 'B', 'B'],
    'Oogenesis': ['B', 'B', 'C', 'B', 'C', 'B', 'D', 'C', 'C', 'D', 'A', 'B'],
    'Ovarian Cycle': ['C', 'B', 'D', 'A', 'A', 'B', 'D', 'C', 'C', 'D', 'F', 'A'],
    'Menstrual Cycle': ['C', 'B', 'A', 'A', 'A', 'D', 'D'],
    'Fertilization': ['C', 'C', 'C', 'C', 'D', 'E', 'C', 'B', 'D', 'D', 'D', 'E', 'D', 'B', 'B', 'E', 'B', 'D', 'C', 'D', 'D'],
    'Cleavage': ['D', 'A', 'D', 'A', 'B', 'D', 'A', 'B', 'E', 'D'],
    'Decidua and Implantation': ['C', 'B', 'B', 'B', 'E', 'D', 'B', 'D', 'A', 'A', 'E', 'A', 'D'],
    'Second Week Development': ['C', 'A', 'B', 'A', 'C', 'A'],
    'Chorion and Chorionic Villi': ['C', 'E', 'C', 'B', 'E', 'C', 'A', 'B', 'D', 'A'],
    'Third Week Development': ['B', 'D', 'B', 'D', 'B', 'C', 'B', 'A', 'B', 'B', 'B', 'D', 'E', 'B', 'E', 'A'],
    'Derivatives of Germ Layers': ['E', 'B', 'E', 'D', 'C', 'B', 'B', 'C', 'A', 'D', 'C'],
    'Folding': ['A', 'C', 'C', 'C', 'D', 'B'],
    'Amnion': ['A', 'D', 'B', 'B', 'B', 'C'],
    'Yolk Sac': ['C', 'B', 'D', 'D', 'C', 'D', 'D'],
    'Allantois': ['C', 'A', 'A', 'C', 'B'],
    'Umbilical Cord': ['B', 'B', 'D', 'D', 'D', 'B', 'C'],
    'Placenta': ['A', 'B', 'C', 'C', 'C', 'D', 'B', 'E', 'C', 'C', 'A', 'D', 'E', 'C'],
    'Multiple Pregnancy': ['B', 'B'],
    'Teratogenicity': ['B', 'C', 'A', 'A', 'D', 'A', 'D']
}

total = sum(len(v) for v in keys.values())
print(f"Total MCQs across all 19 topics: {total}")
