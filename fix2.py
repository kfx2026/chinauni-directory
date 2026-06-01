"""Fix university sub-pages - take 2"""
import os, glob

BASE = r'D:\腾讯龙虾后台文件\Claw\uni-temp\zh'
LANGS = ['zh','en','es','ar','ru']

def fix_file(filepath, levels):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    modified = False
    
    # Replace each language button onclick
    for l in LANGS:
        old_onclick = "onclick=\"location.href='" + ('../' * levels) + ('../' if levels > 0 else '') + l + "/index.html'\""
        new_onclick = "onclick=\"var up='" + ('../' * levels) + "';localStorage.setItem('chinauni_lang','" + l + "');location.href=up+'index.html?lang=" + l + "'\""
        if old_onclick in c:
            c = c.replace(old_onclick, new_onclick)
            modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

fixed = 0
for dirname in ['cities', 'uni']:
    for f in glob.glob(os.path.join(BASE, dirname, '*.html')):
        try:
            if fix_file(f, 1):
                fixed += 1
        except Exception as e:
            print(f'ERR {dirname}/{os.path.basename(f)}: {e}')

for name in ['cities.html', 'tiers.html', 'index.html']:
    f = os.path.join(BASE, name)
    if os.path.exists(f):
        try:
            if fix_file(f, 0):
                fixed += 1
        except Exception as e:
            print(f'ERR {name}: {e}')

print(f'Fixed: {fixed} files')
