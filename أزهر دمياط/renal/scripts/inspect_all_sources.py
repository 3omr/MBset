import glob, os, re

files = sorted(glob.glob('renal/markdown_output/*.md'))

for idx, fpath in enumerate(files, 1):
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
        text = ''.join(lines)
        
    print(f"\n[{idx:02d}] {fname} ({len(lines)} lines)")
    
    # Check sections
    sections = re.findall(r'(?m)^#+\s*(.+)', text)
    print("  Headers:", sections[:6])
