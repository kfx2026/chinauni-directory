# -*- coding: utf-8 -*-
"""chinauni-directory index.html 生成器 - 完整版
4 页导航：首页 / 地区 / 学术层次 / 专业
5 语言完整 i18n，所有动态内容语言感知，城市配图"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DESKTOP = "D:/Users/Administrator/Desktop/大学目录站"
SRC = os.path.dirname(DESKTOP)

with open(os.path.join(SRC, "大学目录数据_211_universities.json"), "r", encoding="utf-8") as f:
    UNIS = json.load(f)
with open(os.path.join(SRC, "大学目录数据_programs_index.json"), "r", encoding="utf-8") as f:
    PROGS = json.load(f)

def slug(s): return s.lower().replace(" ", "-").replace("'", "")

# ---- 城市统计 ----
cts = {}
for u in UNIS: cts[u["city"]] = cts.get(u["city"], 0) + 1
tc = sorted(cts.items(), key=lambda x: -x[1])[:12]

# ---- 分层 ----
c9_unis = [u for u in UNIS if u.get("tier") == "C9"]
a9_unis = [u for u in UNIS if u.get("tier") == "985"]
d1_unis = [u for u in UNIS if u.get("tier") == "211"]

# ---- 城市图片 (多源: Unsplash优先, Picsum兜底) ----
# 已验证可用的 Unsplash URL
_UNSPLASH_OK = {
    "Beijing":  "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    "Shanghai": "https://images.unsplash.com/photo-1474181487882-5abf3f0ba6c2?w=800&q=80",
    "Guangzhou":"https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=800&q=80",
    "Wuhan":    "https://images.unsplash.com/photo-1545893835-abaa50cbe628?w=800&q=80",
    "Xi'an":    "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800&q=80",
    "Nanjing":  "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800&q=80",
    "Hangzhou": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",
    "Chengdu":  "https://images.unsplash.com/photo-1624628639856-100bf817fd35?w=800&q=80",
    "Tianjin":  "https://images.unsplash.com/photo-1598703012620-f966ce22ef40?w=800&q=80",
    "Harbin":   "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&q=80",
    "Changsha": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800&q=80",
    "Shenyang": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
}

# 所有40个城市: Unsplash优先, 没有则用Picsum(保证每城不同图)
CITY_IMG = {}
for c in sorted(set(u["city"] for u in UNIS)):
    if c in _UNSPLASH_OK:
        CITY_IMG[c] = _UNSPLASH_OK[c]
    else:
        CITY_IMG[c] = "https://picsum.photos/seed/" + slug(c) + "/800/500"

FIMG = CITY_IMG.get("Beijing", "https://picsum.photos/seed/china/800/500")

# ---- 专业分类 ----
STEM_CATS = ["Medicine", "Engineering", "Sciences", "Agriculture"]
HUM_CATS  = ["Business", "Humanities", "Arts"]
CAT_ICON = {
    "Medicine":"💉","Engineering":"⚙️","Business":"📊",
    "Sciences":"🔬","Agriculture":"🌾","Humanities":"📖","Arts":"🎨"
}
CAT_COLOR = {
    "Medicine":"#c0392b","Engineering":"#2471a3","Business":"#b8860b",
    "Sciences":"#7d3c98","Agriculture":"#1e8449","Humanities":"#0e6655","Arts":"#c2185b"
}

# ---- i18n 字典 ----
LANGS = ["zh","en","es","ar","ru"]

i18n = {
    "zh": {
        "site": "中国大学目录",
        "tagline": "探索中国顶尖学府，开启你的学术之旅",
        "hero_badge": "学术卓越",
        "home": "首页", "cities": "地区", "tiers": "学术层次", "programs": "专业",
        "uni_count": "所大学", "prog_count": "个专业方向", "city_count": "座城市",
        "intro_title": "为什么选择中国大学",
        "intro_text": "中国拥有3117所高等教育机构，其中116所入选211工程重点大学。38万国际学生来自191个国家，享受世界一流的工程、医学、商科教育，学费仅为欧美国家的1/3。",
        "by_region": "按城市浏览", "by_tier": "按学术层次浏览", "by_prog": "按专业浏览",
        "tier_c9": "C9联盟 · 中国常春藤",
        "tier_c9_sub": "中国首个顶尖大学联盟，代表最高学术水平",
        "tier_a985": "985工程 · 世界一流大学",
        "tier_a985_sub": "国家重点建设的世界一流大学",
        "tier_a211": "211工程 · 国家重点大学",
        "tier_a211_sub": "21世纪重点建设的100所高水平大学",
        "stem_tab": "理工农医", "hum_tab": "人文社科艺术",
        "qs_rank": "QS排名", "city_label": "城市",
        "sec_label_location": "按地区", "sec_label_prestige": "学术层次", "sec_label_academics": "学科专业",
        "cities_sub": "探索中国各大城市的顶尖大学",
        "programs_sub": "59个专业方向，覆盖7大学科门类",
        "disc": "本目录仅供参考，不提供申请服务。请通过大学官网核实信息。",
        "search_placeholder": "搜索大学或专业...",
        "about": "关于本站",
    },
    "en": {
        "site": "China University Directory",
        "tagline": "Discover China's Elite Universities",
        "hero_badge": "Academic Excellence",
        "home": "Home", "cities": "Regions", "tiers": "Tiers", "programs": "Programs",
        "uni_count": "Universities", "prog_count": "Programs", "city_count": "Cities",
        "intro_title": "Why Study in China",
        "intro_text": "China hosts 3,117 higher education institutions, with 116 designated as national key universities. 380,000 international students from 191 countries benefit from world-class education at one-third the cost of Western universities.",
        "by_region": "Browse by City", "by_tier": "Browse by Tier", "by_prog": "Browse by Program",
        "tier_c9": "C9 League · China's Ivy League",
        "tier_c9_sub": "China's premier university alliance, representing the highest academic standard",
        "tier_a985": "Project 985 · World-Class Universities",
        "tier_a985_sub": "Nationally designated world-class universities",
        "tier_a211": "Project 211 · National Key Universities",
        "tier_a211_sub": "Top 100 universities designated for 21st century excellence",
        "stem_tab": "STEM & Medicine", "hum_tab": "Humanities & Arts",
        "qs_rank": "QS Rank", "city_label": "City",
        "sec_label_location": "Location", "sec_label_prestige": "Prestige", "sec_label_academics": "Academics",
        "cities_sub": "Explore universities across China's major cities",
        "programs_sub": "59 programs across 7 academic disciplines",
        "disc": "Information directory only. No application services. Verify details on official university websites.",
        "search_placeholder": "Search universities or programs...",
        "about": "About",
    },
    "es": {
        "site": "Directorio de Universidades de China",
        "tagline": "Descubre las mejores universidades de China",
        "hero_badge": "Excelencia Académica",
        "home": "Inicio", "cities": "Regiones", "tiers": "Niveles", "programs": "Programas",
        "uni_count": "Universidades", "prog_count": "Programas", "city_count": "Ciudades",
        "intro_title": "Por qué estudiar en China",
        "intro_text": "China cuenta con 3117 instituciones, 116 universidades nacionales clave. 380000 estudiantes internacionales de 191 países se benefician de educación de clase mundial.",
        "by_region": "Por Ciudad", "by_tier": "Por Nivel", "by_prog": "Por Programa",
        "tier_c9": "Liga C9 · Ivy League de China",
        "tier_c9_sub": "La alianza universitaria premier de China",
        "tier_a985": "Proyecto 985 · Clase Mundial",
        "tier_a985_sub": "Universidades de clase mundial designadas nacionalmente",
        "tier_a211": "Proyecto 211 · Clave Nacional",
        "tier_a211_sub": "100 mejores universidades para la excelencia del siglo XXI",
        "stem_tab": "STEM y Medicina", "hum_tab": "Humanidades y Artes",
        "qs_rank": "Clasificación QS", "city_label": "Ciudad",
        "sec_label_location": "Ubicación", "sec_label_prestige": "Prestigio", "sec_label_academics": "Académico",
        "cities_sub": "Explora universidades en las principales ciudades de China",
        "programs_sub": "59 programas en 7 disciplinas académicas",
        "disc": "Directorio informativo solamente.",
        "search_placeholder": "Buscar universidad o programa...",
        "about": "Acerca de",
    },
    "ar": {
        "site": "دليل الجامعات الصينية",
        "tagline": "اكتشف نخبة الجامعات الصينية",
        "hero_badge": "التميز الأكاديمي",
        "home": "الرئيسية", "cities": "المناطق", "tiers": "المستويات", "programs": "البرامج",
        "uni_count": "جامعة", "prog_count": "برنامج", "city_count": "مدينة",
        "intro_title": "لماذا الدراسة في الصين",
        "intro_text": "تضم الصين 3117 مؤسسة تعليم عالي، منها 116 جامعة وطنية رئيسية. 380000 طالب دولي من 191 دولة.",
        "by_region": "حسب المدينة", "by_tier": "حسب المستوى", "by_prog": "حسب البرنامج",
        "tier_c9": "رابطة C9 · رابطة اللبلاب الصينية",
        "tier_c9_sub": "تحالف الجامعات النخبوية الصينية",
        "tier_a985": "مشروع 985 · المستوى العالمي",
        "tier_a985_sub": "جامعات عالمية المستوى معينة وطنيا",
        "tier_a211": "مشروع 211 · المفتاح الوطني",
        "tier_a211_sub": "أفضل 100 جامعة للتميز في القرن الحادي والعشرين",
        "stem_tab": "العلوم والطب", "hum_tab": "العلوم الإنسانية والفنون",
        "qs_rank": "تصنيف QS", "city_label": "المدينة",
        "sec_label_location": "الموقع", "sec_label_prestige": "المكانة", "sec_label_academics": "الأكاديميات",
        "cities_sub": "استكشف الجامعات في المدن الرئيسية بالصين",
        "programs_sub": "59 برنامجا عبر 7 تخصصات أكاديمية",
        "disc": "دليل معلوماتي فقط. لا نقدم خدمات التقديم.",
        "search_placeholder": "بحث عن جامعة أو برنامج...",
        "about": "حول",
    },
    "ru": {
        "site": "Каталог университетов Китая",
        "tagline": "Откройте элитные университеты Китая",
        "hero_badge": "Академическое превосходство",
        "home": "Главная", "cities": "Регионы", "tiers": "Уровни", "programs": "Программы",
        "uni_count": "Университетов", "prog_count": "Программ", "city_count": "Городов",
        "intro_title": "Почему стоит учиться в Китае",
        "intro_text": "В Китае 3117 вузов, 116 имеют статус национальных ключевых университетов. 380000 иностранных студентов из 191 страны.",
        "by_region": "По городам", "by_tier": "По уровню", "by_prog": "По программам",
        "tier_c9": "Лига C9 · Лига плюща Китая",
        "tier_c9_sub": "Премьер-альянс университетов Китая",
        "tier_a985": "Проект 985 · Мировой класс",
        "tier_a985_sub": "Национальные университеты мирового класса",
        "tier_a211": "Проект 211 · Национальный ключ",
        "tier_a211_sub": "100 лучших университетов для совершенства XXI века",
        "stem_tab": "STEM и Медицина", "hum_tab": "Гуманитарные науки и искусства",
        "qs_rank": "Рейтинг QS", "city_label": "Город",
        "sec_label_location": "Расположение", "sec_label_prestige": "Престиж", "sec_label_academics": "Академия",
        "cities_sub": "Исследуйте университеты в крупных городах Китая",
        "programs_sub": "59 программ по 7 академическим дисциплинам",
        "disc": "Информационный справочник.",
        "search_placeholder": "Поиск университета или программы...",
        "about": "О нас",
    },
}

# 专业中文名注入 (prog_xxx)
prog_zh_map = {}
for p in PROGS:
    prog_zh_map["prog_" + p["id"]] = p.get("program_zh", "")
i18n["zh"].update(prog_zh_map)

# 城市中文名 + 英文名映射 (city_xxx)
all_cities = sorted(set(u["city"] for u in UNIS))
for c in all_cities:
    i18n["en"]["city_" + slug(c)] = c

# 城市中文名
_zh_names = {"Beijing":"北京","Shanghai":"上海","Guangzhou":"广州","Wuhan":"武汉","Xi'an":"西安","Nanjing":"南京","Hangzhou":"杭州","Chengdu":"成都","Tianjin":"天津","Changsha":"长沙","Harbin":"哈尔滨","Shenyang":"沈阳","Shenzhen":"深圳","Chongqing":"重庆","Suzhou":"苏州","Dalian":"大连","Qingdao":"青岛","Xiamen":"厦门","Kunming":"昆明","Hefei":"合肥","Jinan":"济南","Fuzhou":"福州","Zhengzhou":"郑州","Changchun":"长春","Lanzhou":"兰州","Nanning":"南宁","Guiyang":"贵阳","Taiyuan":"太原","Nanchang":"南昌","Urumqi":"乌鲁木齐","Hohhot":"呼和浩特","Lhasa":"拉萨","Yinchuan":"银川","Xining":"西宁","Haikou":"海口","Shijiazhuang":"石家庄","Ningbo":"宁波","Wuxi":"无锡","Foshan":"佛山","Dongguan":"东莞"}
for en_name, zh_name in _zh_names.items():
    i18n["zh"]["city_" + slug(en_name)] = zh_name
    i18n["es"]["city_" + slug(en_name)] = en_name
    i18n["ar"]["city_" + slug(en_name)] = en_name
    i18n["ru"]["city_" + slug(en_name)] = en_name

# 分类名翻译 (cat_xxx)
_cat_trans = {
    "zh": {"Medicine":"医学","Engineering":"工程","Business":"商科","Sciences":"理学","Agriculture":"农学","Humanities":"人文","Arts":"艺术"},
    "en": {"Medicine":"Medicine","Engineering":"Engineering","Business":"Business","Sciences":"Sciences","Agriculture":"Agriculture","Humanities":"Humanities","Arts":"Arts"},
    "es": {"Medicine":"Medicina","Engineering":"Ingeniería","Business":"Negocios","Sciences":"Ciencias","Agriculture":"Agricultura","Humanities":"Humanidades","Arts":"Artes"},
    "ar": {"Medicine":"الطب","Engineering":"الهندسة","Business":"الأعمال","Sciences":"العلوم","Agriculture":"الزراعة","Humanities":"العلوم الإنسانية","Arts":"الفنون"},
    "ru": {"Medicine":"Медицина","Engineering":"Инженерия","Business":"Бизнес","Sciences":"Науки","Agriculture":"Сельское хозяйство","Humanities":"Гуманитарные","Arts":"Искусство"},
}
for lang in LANGS:
    for cat_en, cat_tr in _cat_trans.get(lang, _cat_trans["en"]).items():
        i18n[lang]["cat_" + slug(cat_en)] = cat_tr

# ---- 生成城市卡片 HTML ----
city_cards_html = ""
for c, n in tc:
    img = CITY_IMG.get(c, FIMG)
    city_cards_html += '<a href="en/cities/' + slug(c) + '.html" class="card city-card"><div class="card-img" style="background-image:url(' + img + ')"></div><div class="card-body"><div class="card-title" data-i18n="city_' + slug(c) + '">' + c + '</div><div class="card-sub">' + str(n) + ' <span data-i18n="uni_count">Universities</span></div></div></a>'

# ---- 生成专业卡片 (按分类分组) ----
stem_progs_html = ""
hum_progs_html = ""
for cat in sorted(set(p["category"] for p in PROGS)):
    cat_progs = [p for p in PROGS if p["category"] == cat]
    if not cat_progs: continue
    icon = CAT_ICON.get(cat, "📖")
    color = CAT_COLOR.get(cat, "#ccc")
    cards_html = ""
    for p in cat_progs:
        pid = p["id"]
        pen = p["program_en"]
        pzh = p.get("program_zh", "")
        count = p.get("total_universities", len(p.get("universities", [])))
        cards_html += '<a href="en/programs/' + pid + '.html" class="prog-card" style="border-top-color:' + color + '"><div class="prog-icon">' + icon + '</div><div class="prog-name" data-i18n="prog_' + pid + '">' + pen + '</div><div class="prog-meta"><span class="prog-count">' + str(count) + ' unis</span></div></a>'
    section_html = '<div class="prog-cat-section"><div class="prog-cat-head"><span class="prog-cat-icon">' + icon + '</span><span class="prog-cat-label" data-i18n="cat_' + slug(cat) + '">' + cat + '</span><span class="prog-cat-n">' + str(len(cat_progs)) + ' programs</span></div><div class="prog-grid">' + cards_html + '</div></div>'
    if cat in STEM_CATS: stem_progs_html += section_html
    else: hum_progs_html += section_html

# ---- 嵌入 JSON ----
UNIS_JSON = json.dumps(UNIS, ensure_ascii=False)
PROGS_JSON = json.dumps(PROGS, ensure_ascii=False)
I18N_JSON = json.dumps(i18n, ensure_ascii=False)

# ==================== CSS ====================
CSS = r"""@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#0a1628;--gold:#c9a96e;--gold-l:#e8d5b0;--cream:#faf7f0;--white:#fff;--text:#1a1a2e;--text-l:#5a6070;--border:rgba(0,0,0,.08);--r:16px}
html{scroll-behavior:smooth}
body{font-family:Inter,-apple-system,sans-serif;color:var(--text);background:var(--cream);line-height:1.7;overflow-x:hidden}
html[dir=rtl] body{font-family:'Noto Naskh Arabic',Inter,sans-serif}

nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(10,22,40,.95);backdrop-filter:blur(20px);height:72px}
.ni{max-width:1280px;margin:0 auto;padding:0 32px;height:100%;display:flex;align-items:center;justify-content:space-between}
.nl{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--gold);text-decoration:none;display:flex;align-items:center;gap:10px;cursor:pointer}
.nlicon{width:34px;height:34px;background:linear-gradient(135deg,var(--gold),#a6844a);border-radius:8px;display:flex;align-items:center;justify-content:center;color:var(--navy);font-size:15px;font-weight:900}
.nt{display:flex;gap:4px}
.nt a{text-decoration:none;color:rgba(255,255,255,.7);font-size:14px;font-weight:500;padding:10px 18px;border-radius:8px;cursor:pointer;transition:.2s}
.nt a:hover,.nt a.active{background:rgba(201,169,110,.15);color:var(--gold)}
.nr{display:flex;align-items:center;gap:10px}
.lb{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);padding:6px 10px;border-radius:6px;font-size:11px;cursor:pointer;color:rgba(255,255,255,.6);font-family:inherit;font-weight:500;text-transform:uppercase;transition:.2s}
.lb:hover,.lb.on{border-color:var(--gold);color:var(--gold);background:rgba(201,169,110,.1)}

.page-section{display:none;min-height:calc(100vh - 72px)}
.page-section.active{display:block}

/* Hero */
.hero{position:relative;min-height:90vh;display:flex;align-items:center;overflow:hidden;background:var(--navy)}
.hero-bg{position:absolute;inset:0;background:url(https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1920&q=80) center/cover;opacity:.3}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,22,40,.75),rgba(10,22,40,.5),rgba(10,22,40,.9))}
.hero-content{position:relative;z-index:2;max-width:800px;padding:120px 40px 80px}
.hero-badge{display:inline-block;border:1px solid var(--gold);color:var(--gold);font-size:11px;font-weight:600;letter-spacing:3px;padding:8px 20px;margin-bottom:28px;text-transform:uppercase}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(34px,5vw,54px);font-weight:900;color:var(--white);line-height:1.15;margin-bottom:20px}
.hero p{font-size:17px;color:rgba(255,255,255,.7);font-weight:300;max-width:500px;margin-bottom:32px}
.hero-stats{display:flex;gap:60px;margin-top:40px}
.hs-num{font-family:'Playfair Display',serif;font-size:42px;font-weight:900;color:var(--gold)}
.hs-label{font-size:13px;color:rgba(255,255,255,.55);text-transform:uppercase;letter-spacing:1.5px}

/* Sections */
.section{padding:100px 32px;max-width:1200px;margin:0 auto}
.section-header{text-align:center;margin-bottom:56px}
.section-label{font-size:11px;font-weight:600;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:16px}
.section-title{font-family:'Playfair Display',serif;font-size:clamp(28px,3vw,36px);font-weight:700;margin-bottom:12px}
.section-sub{font-size:16px;color:var(--text-l)}
.intro-section{max-width:900px;margin:0 auto;padding:80px 32px;text-align:center}
.intro-section h2{font-family:'Playfair Display',serif;font-size:30px;font-weight:700;margin-bottom:20px}
.intro-section p{font-size:16px;color:var(--text-l);line-height:1.9}

.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px}
.card{background:var(--white);border-radius:var(--r);overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.06);transition:.35s;text-decoration:none;color:inherit;display:block}
.card:hover{transform:translateY(-6px);box-shadow:0 16px 48px rgba(0,0,0,.12)}
.card-img{height:180px;background-size:cover;background-position:center}
.card-body{padding:20px 24px 24px}
.card-title{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;margin-bottom:6px}
.card-sub{font-size:13px;color:var(--text-l)}

/* Home quick-nav cards */
.home-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.home-card{background:var(--white);border-radius:var(--r);padding:36px 28px;box-shadow:0 4px 24px rgba(0,0,0,.06);transition:.35s;text-decoration:none;color:inherit;cursor:pointer;position:relative;overflow:hidden}
.home-card::before{content:"";position:absolute;top:0;left:0;right:0;height:4px}
.home-card:nth-child(1)::before{background:linear-gradient(90deg,#2471a3,#4a90d9)}
.home-card:nth-child(2)::before{background:linear-gradient(90deg,#b8860b,#daa520)}
.home-card:nth-child(3)::before{background:linear-gradient(90deg,#1e8449,#27ae60)}
.home-card:hover{transform:translateY(-6px);box-shadow:0 16px 48px rgba(0,0,0,.12)}
.hc-icon{font-size:36px;margin-bottom:16px}
.home-card h3{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;margin-bottom:8px}
.home-card p{font-size:14px;color:var(--text-l)}

/* Tiers */
.tier-sections{max-width:1200px;margin:0 auto}
.tier-block{margin-bottom:32px;background:var(--white);border-radius:var(--r);box-shadow:0 4px 24px rgba(0,0,0,.06);overflow:hidden}
.tier-head{cursor:pointer;display:flex;align-items:center;gap:20px;padding:28px 36px;transition:.2s;user-select:none;position:relative}
.tier-head::after{content:"";position:absolute;top:0;left:0;right:0;height:4px}
.tier-block.c9 .tier-head::after{background:linear-gradient(90deg,#b8860b,#daa520,#f0d060)}
.tier-block.a985 .tier-head::after{background:linear-gradient(90deg,#2471a3,#4a90d9,#6db3f2)}
.tier-block.a211 .tier-head::after{background:linear-gradient(90deg,#1e8449,#27ae60,#52d681)}
.tier-head:hover{background:#fdfaf3}
.tier-head-icon{font-size:40px;flex-shrink:0}
.tier-head-info{flex:1}
.tier-head-info h3{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;margin-bottom:4px}
.tier-head-info .tier-sub{font-size:13px;color:var(--text-l)}
.tier-head-arrow{font-size:18px;color:var(--text-l);transition:.3s;flex-shrink:0}
.tier-block.open .tier-head-arrow{transform:rotate(180deg)}
.tier-body{display:none;padding:0 36px 36px}
.tier-block.open .tier-body{display:block}

/* Uni Cards */
.uni-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}
.uni-card{background:#fafafa;border:1px solid var(--border);border-radius:12px;padding:24px;transition:.25s;text-decoration:none;color:inherit;display:block}
.uni-card:hover{background:var(--white);border-color:rgba(201,169,110,.3);box-shadow:0 4px 20px rgba(0,0,0,.06);transform:translateY(-2px)}
.uni-card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;gap:12px}
.uni-name-en{font-family:'Playfair Display',serif;font-size:17px;font-weight:700;color:var(--navy);line-height:1.3}
.uni-name-zh{font-size:12px;color:var(--text-l);margin-top:2px}
.uni-badge{flex-shrink:0;font-size:11px;font-weight:700;padding:4px 12px;border-radius:6px;color:var(--white);white-space:nowrap}
.uni-badge.c9{background:linear-gradient(135deg,#b8860b,#daa520)}
.uni-badge.a985{background:linear-gradient(135deg,#2471a3,#4a90d9)}
.uni-badge.a211{background:linear-gradient(135deg,#1e8449,#27ae60)}
.uni-meta{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:10px}
.uni-meta-item{display:flex;align-items:center;gap:5px;font-size:12px;color:var(--text-l)}
.uni-meta-item svg{width:14px;height:14px;flex-shrink:0}
.uni-progs{display:flex;flex-wrap:wrap;gap:6px}
.uni-tag{font-size:10px;font-weight:600;padding:3px 10px;border-radius:4px;background:rgba(201,169,110,.12);color:#8b6914;white-space:nowrap}

/* Programs */
.prog-page-header{text-align:center;padding:40px 32px 0;max-width:1200px;margin:0 auto}
.prog-filter{display:flex;justify-content:center;gap:12px;margin:0 auto 40px;padding:0 32px;max-width:1200px}
.prog-filter button{padding:10px 28px;border:1.5px solid var(--border);background:var(--white);border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit;color:var(--text-l);transition:.2s}
.prog-filter button:hover,.prog-filter button.on{background:var(--navy);color:var(--gold);border-color:var(--navy)}
.prog-content{display:none}
.prog-content.on{display:block}
.prog-cat-section{margin-bottom:48px;padding:0 32px;max-width:1200px;margin-left:auto;margin-right:auto}
.prog-cat-head{display:flex;align-items:center;gap:12px;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid var(--border)}
.prog-cat-icon{font-size:22px}
.prog-cat-label{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--navy)}
.prog-cat-n{font-size:12px;color:var(--text-l);margin-left:auto}
.prog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.prog-card{background:var(--white);border-radius:12px;padding:20px 18px;box-shadow:0 2px 16px rgba(0,0,0,.04);transition:.3s;text-decoration:none;color:inherit;border-top:3px solid transparent;display:block}
.prog-card:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(0,0,0,.1)}
.prog-icon{font-size:20px;margin-bottom:10px}
.prog-name{font-size:14px;font-weight:600;margin-bottom:6px;color:var(--text);line-height:1.4}
.prog-meta{display:flex;align-items:center;gap:10px}
.prog-count{font-size:11px;color:var(--gold);font-weight:600}

.page-top{padding-top:72px}

footer{background:var(--navy);color:rgba(255,255,255,.6);padding:56px 32px 36px;text-align:center}
footer .f-brand{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--gold);margin-bottom:10px}
footer p{font-size:13px;max-width:600px;margin:0 auto;line-height:1.8}
footer .f-links{margin-top:20px;display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
footer .f-links a{color:rgba(255,255,255,.5);text-decoration:none;font-size:13px;cursor:pointer}
footer .f-links a:hover{color:var(--gold)}
footer .f-copy{margin-top:28px;font-size:11px;color:rgba(255,255,255,.3)}

.menu-btn{display:none;background:none;border:none;color:var(--gold);font-size:24px;cursor:pointer}
@media(max-width:768px){
  .nt{display:none;position:absolute;top:72px;left:0;right:0;background:rgba(10,22,40,.98);flex-direction:column;padding:20px}
  .nt.open{display:flex}
  .menu-btn{display:block}
  .hero h1{font-size:30px}
  .hero-stats{gap:28px;flex-wrap:wrap}
  .section{padding:60px 20px}
  .card-grid,.home-cards{grid-template-columns:1fr}
  .uni-grid{grid-template-columns:1fr}
  .prog-grid{grid-template-columns:1fr}
  .prog-filter{flex-wrap:wrap}
  .tier-head{padding:20px 24px}
  .tier-body{padding:0 24px 24px}
  .tier-head-icon{font-size:32px}
}
"""

# ==================== JS ====================
JS = r"""let currentLang='en',currentPage='home';
const LANGS=['zh','en','es','ar','ru'];
const PROGS=""" + PROGS_JSON + r""";
const UNIS=""" + UNIS_JSON + r""";
const I18N=""" + I18N_JSON + r""";

function $(s){return document.querySelector(s)}
function $$(s){return document.querySelectorAll(s)}
function t(key){return (I18N[currentLang]&&I18N[currentLang][key])||key}

/* --- Language Switch --- */
function switchLang(lang){
  currentLang=lang;
  // lang buttons
  $$('.lb').forEach(function(b){b.classList.toggle('on',b.textContent.trim()===lang.toUpperCase())});
  // static data-i18n elements
  $$('[data-i18n]').forEach(function(el){
    var k=el.dataset.i18n;var v=I18N[lang]&&I18N[lang][k];
    if(v)el.textContent=v
  });
  // link prefixes
  $$('a[href^="en/"]').forEach(function(a){
    a.href=a.href.replace(/^(en|zh|es|ar|ru)\//,lang+'/')
  });
  // RTL
  document.documentElement.lang=lang;
  document.documentElement.dir=(lang==='ar')?'rtl':'ltr';
  // dynamic content
  renderAllUniCards();
  updateProgramNames()
}

/* --- Page Switch --- */
function switchPage(page){
  currentPage=page;
  $$('.page-section').forEach(function(s){s.classList.remove('active')});
  var target=$('#page-'+page);
  if(target)target.classList.add('active');
  $$('.nt a').forEach(function(a){a.classList.remove('active')});
  var link=$('#nav-'+page);
  if(link)link.classList.add('active');
  window.scrollTo(0,0);
  if(page==='tiers')renderAllUniCards()
}

/* --- Tier Toggle --- */
function toggleTier(tier){
  var block=$('#tier-'+tier);
  if(!block)return;
  var wasOpen=block.classList.contains('open');
  // close all first
  $$('.tier-block').forEach(function(b){b.classList.remove('open')});
  if(wasOpen)return; // just closed it
  // open & render
  block.classList.add('open');
  renderUniGrid(tier)
}

/* --- Render University Cards (language-aware) --- */
function renderUniGrid(tier){
  var grid=$('#uni-grid-'+tier);
  if(!grid)return;
  grid.innerHTML=''; // always rebuild (fixes stale language links)
  var filtered=UNIS.filter(function(u){return u.tier===tier});
  var groups={};
  filtered.forEach(function(u){
    if(!groups[u.city])groups[u.city]=[];
    groups[u.city].push(u)
  });
  var cities=Object.keys(groups).sort(function(a,b){return groups[b].length-groups[a].length});
  var html='';
  cities.forEach(function(city){
    var cityUnis=groups[city];
    cityUnis.forEach(function(u){
      var badgeCls=u.tier==='C9'?'c9':u.tier==='985'?'a985':'a211';
      var progs=u.top_programs?u.top_programs.slice(0,4):[];
      var progTags=progs.map(function(p){return '<span class="uni-tag">'+p+'</span>'}).join('');
      var qsRank=u.qs_rank||'—';
      var cityName=u.city;
      // try i18n city name
      var cityKey='city_'+slugfn(u.city);
      if(I18N[currentLang]&&I18N[currentLang][cityKey])cityName=I18N[currentLang][cityKey];
      html+='<a href="'+currentLang+'/universities/'+slugfn(u.name_en)+'.html" class="uni-card">';
      html+='<div class="uni-card-top"><div><div class="uni-name-en">'+u.name_en+'</div><div class="uni-name-zh">'+u.name_zh+'</div></div><span class="uni-badge '+badgeCls+'">'+u.tier+'</span></div>';
      html+='<div class="uni-meta"><span class="uni-meta-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>QS '+qsRank+'</span><span class="uni-meta-item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'+cityName+'</span></div>';
      html+='<div class="uni-progs">'+progTags+'</div>';
      html+='</a>'
    })
  });
  grid.innerHTML=html
}

function renderAllUniCards(){
  var tiers=['C9','985','211'];
  tiers.forEach(function(t){
    var grid=$('#uni-grid-'+t);
    if(grid){grid.innerHTML='';renderUniGrid(t)}
  })
}

/* --- Update program names on language switch --- */
function updateProgramNames(){
  $$('.prog-name[data-i18n]').forEach(function(el){
    var k=el.dataset.i18n;var v=I18N[currentLang]&&I18N[currentLang][k];
    if(v)el.textContent=v
  })
}

/* --- Program tab switch --- */
function switchProg(type){
  $$('.prog-content').forEach(function(c){c.classList.remove('on')});
  var ct=$('#prog-'+type);
  if(ct)ct.classList.add('on');
  $$('.prog-filter button').forEach(function(b){b.classList.remove('on')});
  var btn=$('#prog-btn-'+type);
  if(btn)btn.classList.add('on')
}

function slugfn(s){return s.toLowerCase().replace(/ /g,'-').replace(/'/g,'')}

/* --- Init --- */
(function(){
  var bl=navigator.language.split('-')[0];
  if(LANGS.indexOf(bl)>=0)switchLang(bl);
  switchPage('home');
  // pre-render C9 grid (it's open by default)
  renderUniGrid('C9');
})();
"""

# ==================== HTML ====================
LB = "".join(['<button class="lb' + (' on' if x == 'en' else '') + '" onclick="switchLang(\'' + x + '\')">' + x + '</button>' for x in LANGS])

html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>China University Directory</title><style>' + CSS + '</style></head><body>'

# ---- Nav ----
html += '<nav><div class="ni"><div class="nl" onclick="switchPage(\'home\')"><span class="nlicon">大</span><span data-i18n="site">China University Directory</span></div><div class="nt"><a id="nav-home" class="active" onclick="switchPage(\'home\')" data-i18n="home">Home</a><a id="nav-cities" onclick="switchPage(\'cities\')" data-i18n="cities">Regions</a><a id="nav-tiers" onclick="switchPage(\'tiers\')" data-i18n="tiers">Tiers</a><a id="nav-programs" onclick="switchPage(\'programs\')" data-i18n="programs">Programs</a></div><button class="menu-btn" onclick="var nt=this.parentNode.querySelector(\'.nt\');nt.classList.toggle(\'open\')">☰</button><div class="nr">' + LB + '</div></div></nav>'

# === Page 1: Home ===
html += '<div id="page-home" class="page-section active">'
html += '<div class="hero"><div class="hero-bg"></div><div class="hero-overlay"></div><div class="hero-content"><div class="hero-badge" data-i18n="hero_badge">Academic Excellence</div><h1 data-i18n="site">China University Directory</h1><p data-i18n="tagline">Discover China\'s Elite Universities</p><div class="hero-stats"><div><div class="hs-num">116</div><div class="hs-label" data-i18n="uni_count">Universities</div></div><div><div class="hs-num">' + str(len(PROGS)) + '</div><div class="hs-label" data-i18n="prog_count">Programs</div></div><div><div class="hs-num">40</div><div class="hs-label" data-i18n="city_count">Cities</div></div></div></div></div>'
html += '<div class="intro-section"><h2 data-i18n="intro_title">Why Study in China</h2><p data-i18n="intro_text">China hosts 3,117 higher education institutions...</p></div>'
html += '<div class="section"><div class="home-cards">'
html += '<div class="home-card" onclick="switchPage(\'cities\')"><div class="hc-icon">🏙️</div><h3 data-i18n="by_region">Browse by City</h3><p>40 <span data-i18n="city_count">Cities</span></p></div>'
html += '<div class="home-card" onclick="switchPage(\'tiers\')"><div class="hc-icon">🏆</div><h3 data-i18n="by_tier">Browse by Tier</h3><p>C9 · 985 · 211</p></div>'
html += '<div class="home-card" onclick="switchPage(\'programs\')"><div class="hc-icon">📚</div><h3 data-i18n="by_prog">Browse by Program</h3><p>' + str(len(PROGS)) + ' <span data-i18n="prog_count">Programs</span></p></div>'
html += '</div></div></div>'

# === Page 2: Cities ===
html += '<div id="page-cities" class="page-section"><div class="page-top"></div>'
html += '<div class="section"><div class="section-header"><div class="section-label" data-i18n="sec_label_location">Location</div><div class="section-title" data-i18n="by_region">Browse by City</div><div class="section-sub" data-i18n="cities_sub">Explore universities across China\'s major cities</div></div><div class="card-grid">' + city_cards_html + '</div></div></div>'

# === Page 3: Tiers ===
html += '<div id="page-tiers" class="page-section"><div class="page-top"></div>'
html += '<div class="section"><div class="section-header"><div class="section-label" data-i18n="sec_label_prestige">Prestige</div><div class="section-title" data-i18n="by_tier">Browse by Academic Tier</div></div>'
html += '<div class="tier-sections">'

for tier_key, tier_icon, tier_list in [("C9","🥇",c9_unis), ("985","🥈",a9_unis), ("211","🥉",d1_unis)]:
    tier_cls = {"C9":"c9","985":"a985","211":"a211"}[tier_key]
    i18n_prefix = {"C9":"c9","985":"a985","211":"a211"}[tier_key]
    html += '<div id="tier-' + tier_key + '" class="tier-block ' + tier_cls + (' open' if tier_key == 'C9' else '') + '">'
    html += '<div class="tier-head" onclick="toggleTier(\'' + tier_key + '\')"><div class="tier-head-icon">' + tier_icon + '</div><div class="tier-head-info"><h3 data-i18n="tier_' + i18n_prefix + '">' + tier_key + '</h3><div class="tier-sub"><span data-i18n="tier_' + i18n_prefix + '_sub">Description</span> · ' + str(len(tier_list)) + ' <span data-i18n="uni_count">Universities</span></div></div><div class="tier-head-arrow">▼</div></div>'
    html += '<div class="tier-body"><div id="uni-grid-' + tier_key + '" class="uni-grid"></div></div></div>'

html += '</div></div></div>'

# === Page 4: Programs ===
html += '<div id="page-programs" class="page-section"><div class="page-top"></div>'
html += '<div class="prog-page-header"><div class="section-label" data-i18n="sec_label_academics">Academics</div><div class="section-title" data-i18n="by_prog">Browse by Program</div><div class="section-sub" data-i18n="programs_sub">59 programs across 7 disciplines</div></div>'
html += '<div class="prog-filter"><button id="prog-btn-stem" class="on" onclick="switchProg(\'stem\')" data-i18n="stem_tab">STEM & Medicine</button><button id="prog-btn-hum" onclick="switchProg(\'hum\')" data-i18n="hum_tab">Humanities & Arts</button></div>'
html += '<div id="prog-stem" class="prog-content on">' + stem_progs_html + '</div>'
html += '<div id="prog-hum" class="prog-content">' + hum_progs_html + '</div>'
html += '</div>'

# ---- Footer ----
html += '<footer><div class="f-brand" data-i18n="site">China University Directory</div><p data-i18n="disc">Information directory only.</p><div class="f-links"><a data-i18n="about" href="en/about.html">About</a><a onclick="switchPage(\'home\')" style="cursor:pointer" data-i18n="home">Home</a></div><div class="f-copy">&copy; 2026 China University Directory</div></footer>'

html += '<script>' + JS + '</script></body></html>'

out = os.path.join(DESKTOP, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 完整版 index.html 已生成: " + out)
print("   大小: " + str(os.path.getsize(out)) + " 字节")
print("   修复: 全部 data-i18n + 动态渲染语言感知 + 城市配图")
