"""Fix language persistence on zh/ sub-pages"""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.join(BASE, 'zh')
LANGS = ['zh','en','es','ar','ru']

def fix_file(filepath, up_levels):
    up = '../' * up_levels
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix language buttons: redirect to root SPA index.html?lang=XX
    for l in LANGS:
        # Replace onclick="location.href='PATH'" in language buttons
        old_pat = f'onclick="location.href=&#x27;' + ('../' * up_levels) + ('../' if up_levels > 0 else '') + l + '/index.html&#x27;"'
        new_val = f'onclick="var up=&#x27;' + up + '&#x27;;localStorage.setItem(&#x27;chinauni_lang&#x27;,&#x27;' + l + '&#x27;);location.href=up+&#x27;index.html?lang=' + l + '&#x27;"'
        content = content.replace(old_pat, new_val)
    
    # Inject localStorage persistence script before </body>
    script = """
<script>
(function(){
  var urlLang=(new URLSearchParams(location.search)).get('lang');
  if(urlLang&&['zh','en','es','ar','ru'].indexOf(urlLang)>=0){
    localStorage.setItem('chinauni_lang',urlLang);
  }
  var saved=localStorage.getItem('chinauni_lang');
  if(saved&&saved!=='zh'){
    // update nav links to include ?lang=
    var links=document.querySelectorAll('a[href]');
    links.forEach(function(a){
      var h=a.getAttribute('href');
      if(h&&h.startsWith('../')&&h.indexOf('.html')>=0&&h.indexOf('?lang=')<0&&h.indexOf('index.html')<0){
        a.href=h+'?lang='+saved;
      }
    });
  }
})();
</script>
"""
    if '</body>' in content:
        content = content.replace('</body>', script + '\n</body>')
    elif '</html>' in content:
        content = content.replace('</html>', script + '\n</html>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# Fix city pages
for f in glob.glob(os.path.join(ZH, 'cities', '*.html')):
    try:
        fix_file(f, 2)
        print(f"  OK: cities/{os.path.basename(f)}")
    except Exception as e:
        print(f"  ERR: {f}: {e}")

# Fix uni pages
for f in glob.glob(os.path.join(ZH, 'uni', '*.html')):
    try:
        fix_file(f, 2)
        print(f"  OK: uni/{os.path.basename(f)}")
    except Exception as e:
        print(f"  ERR: {f}: {e}")

# Fix cities.html & tiers.html in zh/
for name in ['cities.html', 'tiers.html']:
    f = os.path.join(ZH, name)
    if os.path.exists(f):
        try:
            fix_file(f, 1)
            print(f"  OK: {name}")
        except Exception as e:
            print(f"  ERR: {f}: {e}")

print("Done!")
