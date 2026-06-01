"""
Fix language persistence on university directory individual pages.
1. Read ?lang= param → persist to localStorage
2. Fix language buttons to redirect to root SPA with lang param
3. Add lang= parameter to all internal links
"""
import os, re, glob

BASE = r"D:\Users\Administrator\Desktop\大学目录站\zh"
LANG_BTN_SCRIPT = """
<script>
(function(){
  // Read URL lang param and persist
  var urlLang=(new URLSearchParams(location.search)).get('lang');
  if(urlLang)localStorage.setItem('chinauni_lang',urlLang);
  // Fix language buttons to redirect to root SPA
  var up='../'.repeat('DEPTH_PLACEHOLDER');
  var btns=document.querySelectorAll('.lb');
  btns.forEach(function(b){
    var lang=b.textContent.trim().toLowerCase();
    var langs=['zh','en','es','ar','ru'];
    if(langs.indexOf(lang)>=0){
      b.onclick=function(){localStorage.setItem('chinauni_lang',lang);location.href=up+'index.html?lang='+lang}
    }
  });
  // Add lang to nav links
  var saved=localStorage.getItem('chinauni_lang')||'zh';
  var links=document.querySelectorAll('nav a[href]');
  links.forEach(function(a){
    var href=a.getAttribute('href');
    if(href&&href.indexOf('index.html?lang=')===-1&&href.indexOf('.html')>=0){
      a.href=href+(href.indexOf('?')>=0?'&':'?')+'lang='+saved
    }
  });
})();
</script>
"""

def fix_file(filepath, depth):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject script before </body>
    script = LANG_BTN_SCRIPT.replace('DEPTH_PLACEHOLDER', str(depth))
    
    # Remove existing onclick language handlers to avoid conflicts
    # Pattern: onclick="location.href='../../XX/index.html'"
    content = re.sub(r'onclick="location\.href=\'[^\']*index\.html\'"', 'onclick="void(0)"', content)
    
    if '<script>' not in content and '</body>' in content:
        content = content.replace('</body>', script + '</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix city pages (depth=2 from root, up=../../)
city_files = glob.glob(os.path.join(BASE, 'cities', '*.html'))
print(f"City pages: {len(city_files)}")
for f in city_files:
    try:
        if fix_file(f, 2):
            print(f"  FIXED: cities/{os.path.basename(f)}")
    except Exception as e:
        print(f"  ERROR: {f}: {e}")

# Fix university pages (depth=2)
uni_files = glob.glob(os.path.join(BASE, 'uni', '*.html'))
print(f"Uni pages: {len(uni_files)}")
for f in uni_files:
    try:
        if fix_file(f, 2):
            print(f"  FIXED: uni/{os.path.basename(f)}")
    except Exception as e:
        print(f"  ERROR: {f}: {e}")

# Fix cities.html (depth=1)
cities_list = os.path.join(BASE, 'cities.html')
if os.path.exists(cities_list):
    try:
        if fix_file(cities_list, 1):
            print("  FIXED: cities.html")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nDone!")
