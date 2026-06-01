"""Fix language persistence on zh/ sub-pages"""
import os, re, glob

BASE = r'D:/腾讯龙虾后台文件/Claw/uni-temp'
ZH = os.path.join(BASE, 'zh')
LANGS = ['zh','en','es','ar','ru']

def fix_file(filepath, up_levels):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Fix language buttons onclick
    for l in LANGS:
        old = 'onclick="location.href=\'' + ('../' * up_levels) + ('../' if up_levels > 0 else '') + l + '/index.html\'"'
        new = 'onclick="var up=\'' + ('../' * up_levels) + '\';localStorage.setItem(\'chinauni_lang\',\'' + l + '\');location.href=up+\'index.html?lang=' + l + '\'"'
        content = content.replace(old, new)
    
    # 2. Inject localStorage persistence script
    script = '''
<script>
(function(){
  var urlLang=(new URLSearchParams(location.search)).get("lang");
  if(urlLang&&["zh","en","es","ar","ru"].indexOf(urlLang)>=0){
    localStorage.setItem("chinauni_lang",urlLang);
  }
  var saved=localStorage.getItem("chinauni_lang");
  if(saved&&saved!=="zh"){
    var links=document.querySelectorAll("a[href]");
    links.forEach(function(a){
      var h=a.getAttribute("href");
      if(h&&h.startsWith("../")&&h.indexOf(".html")>=0&&h.indexOf("?lang=")<0&&h.indexOf("index.html")<0){
        a.href=h+"?lang="+saved;
      }
    });
  }
})();
</script>
'''
    if '</body>' in content:
        content = content.replace('</body>', script + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

fixed = 0
for f in glob.glob(os.path.join(ZH, 'cities', '*.html')):
    try:
        fix_file(f, 2)
        fixed += 1
    except Exception as e:
        print(f'ERR cities/{os.path.basename(f)}: {e}')

for f in glob.glob(os.path.join(ZH, 'uni', '*.html')):
    try:
        fix_file(f, 2)
        fixed += 1
    except Exception as e:
        print(f'ERR uni/{os.path.basename(f)}: {e}')

for name in ['cities.html', 'tiers.html']:
    f = os.path.join(ZH, name)
    if os.path.exists(f):
        try:
            fix_file(f, 1)
            fixed += 1
        except Exception as e:
            print(f'ERR {name}: {e}')

print(f'Fixed: {fixed} files')
