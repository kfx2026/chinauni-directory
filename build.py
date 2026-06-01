#!/usr/bin/env python3
"""中国大学目录站 — 面向国际留学生，5语言静态站"""

import json, os, shutil

# ── 数据 ──
DESKTOP = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(os.path.dirname(DESKTOP), "大学目录数据_211_universities.json"), "r", encoding="utf-8") as f:
    UNIS = json.load(f)
with open(os.path.join(os.path.dirname(DESKTOP), "大学目录数据_programs_index.json"), "r", encoding="utf-8") as f:
    PROGS = json.load(f)

LANGS = ["zh", "en", "es", "ar", "ru"]
CAT_ICON = {"Medicine": "💉", "Engineering": "⚙️", "Business": "📊", "Sciences": "🔬", "Agriculture": "🌾", "Humanities": "📖", "Arts": "🎨"}
CAT_COLOR = {"Medicine": "#c0392b", "Engineering": "#2471a3", "Business": "#b8860b", "Sciences": "#7d3c98", "Agriculture": "#1e8449", "Humanities": "#0e6655", "Arts": "#c2185b"}

# ── i18n ──
T = {}
def t(k, l):
    d = T.get(k, {})
    return d.get(l, d.get("en", k))

T["site"] = {"zh": "中国大学目录", "en": "China University Directory", "es": "Directorio Universitario de China", "ar": "دليل الجامعات الصينية", "ru": "Каталог университетов Китая"}
T["tagline"] = {"zh": "探索中国顶尖学府，开启你的学术之旅", "en": "Discover China's Elite Universities — Begin Your Academic Journey", "es": "Descubre las mejores universidades de China", "ar": "اكتشف نخبة الجامعات الصينية", "ru": "Откройте элитные университеты Китая"}
T["home"] = {"zh": "首页", "en": "Home", "es": "Inicio", "ar": "الرئيسية", "ru": "Главная"}
T["cities"] = {"zh": "城市", "en": "Cities", "es": "Ciudades", "ar": "المدن", "ru": "Города"}
T["tiers"] = {"zh": "学术层次", "en": "Academic Tiers", "es": "Niveles", "ar": "المستويات", "ru": "Уровни"}
T["programs"] = {"zh": "专业", "en": "Programs", "es": "Programas", "ar": "البرامج", "ru": "Программы"}
T["about"] = {"zh": "关于", "en": "About", "es": "Acerca", "ar": "حول", "ru": "О нас"}
T["search"] = {"zh": "搜索大学或专业...", "en": "Search universities or programs...", "es": "Buscar universidad o programa...", "ar": "ابحث عن جامعة أو برنامج...", "ru": "Поиск университета или программы..."}
T["uni_count"] = {"zh": "收录大学", "en": "Universities", "es": "Universidades", "ar": "جامعة", "ru": "Университетов"}
T["prog_count"] = {"zh": "专业方向", "en": "Programs", "es": "Programas", "ar": "برنامج", "ru": "Программ"}
T["city_count"] = {"zh": "覆盖城市", "en": "Cities", "es": "Ciudades", "ar": "مدينة", "ru": "Городов"}
T["intro_title"] = {"zh": "为什么选择中国大学", "en": "Why Study in China", "es": "Por qué estudiar en China", "ar": "لماذا الدراسة في الصين", "ru": "Почему Китай"}
T["intro_text"] = {"zh": "中国拥有3,117所高等教育机构，其中116所入选211工程重点大学。38万国际学生来自191个国家，享受世界一流的工程、医学、商科教育，学费仅为欧美国家的1/3。", "en": "China hosts 3,117 higher education institutions, with 116 designated as national key universities. 380,000 international students from 191 countries benefit from world-class education in engineering, medicine, and business — at one-third the cost of Western universities.", "es": "China cuenta con 3.117 instituciones de educación superior. 380.000 estudiantes internacionales de 191 países disfrutan de educación de clase mundial.", "ar": "تضم الصين 3117 مؤسسة للتعليم العالي. 380000 طالب دولي من 191 دولة يستفيدون من تعليم عالمي المستوى.", "ru": "В Китае 3117 высших учебных заведений. 380000 иностранных студентов из 191 страны получают образование мирового уровня."}
T["by_region"] = {"zh": "按城市浏览", "en": "Browse by City", "es": "Por Ciudad", "ar": "حسب المدينة", "ru": "По городам"}
T["by_tier"] = {"zh": "按学术层次浏览", "en": "Browse by Academic Tier", "es": "Por Nivel", "ar": "حسب المستوى", "ru": "По уровню"}
T["by_prog"] = {"zh": "按专业浏览", "en": "Browse by Program", "es": "Por Programa", "ar": "حسب البرنامج", "ru": "По программе"}
T["tier_c9"] = {"zh": "C9联盟 · 中国常春藤", "en": "C9 League · China's Ivy League", "es": "Liga C9", "ar": "رابطة C9", "ru": "Лига C9"}
T["tier_985"] = {"zh": "985工程 · 世界一流大学", "en": "Project 985 · World-Class", "es": "Proyecto 985", "ar": "مشروع 985", "ru": "Проект 985"}
T["tier_211"] = {"zh": "211工程 · 国家重点大学", "en": "Project 211 · National Key", "es": "Proyecto 211", "ar": "مشروع 211", "ru": "Проект 211"}
T["tuition"] = {"zh": "学费", "en": "Tuition", "es": "Matrícula", "ar": "الرسوم", "ru": "Обучение"}
T["website"] = {"zh": "官方网站", "en": "Official Website", "es": "Sitio Web", "ar": "الموقع الرسمي", "ru": "Официальный сайт"}
T["dist_prog"] = {"zh": "优势领域", "en": "Distinguished Programs", "es": "Programas Destacados", "ar": "برامج متميزة", "ru": "Ведущие направления"}
T["stem"] = {"zh": "理工类", "en": "STEM", "es": "Ciencia e Ingeniería", "ar": "العلوم والهندسة", "ru": "Наука и инженерия"}
T["humanities"] = {"zh": "文科类", "en": "Humanities", "es": "Humanidades", "ar": "العلوم الإنسانية", "ru": "Гуманитарные науки"}
T["top"] = {"zh": "顶尖", "en": "Top Choice", "es": "Excelencia", "ar": "ممتاز", "ru": "Лучший выбор"}
T["strong"] = {"zh": "强势", "en": "Strong", "es": "Fuerte", "ar": "قوي", "ru": "Сильный"}
T["avail"] = {"zh": "可选", "en": "Available", "es": "Disponible", "ar": "متاح", "ru": "Доступен"}
T["disc"] = {"zh": "本目录仅供参考，不提供申请服务。请通过大学官网核实信息。", "en": "Information directory only. No application services. Verify with official sources.", "es": "Directorio informativo. Verifique fuentes oficiales.", "ar": "دليل معلوماتي فقط. تحقق من المصادر الرسمية.", "ru": "Информационный справочник. Проверяйте официальные источники."}
T["view"] = {"zh": "查看详情", "en": "View Details", "es": "Ver Detalles", "ar": "عرض التفاصيل", "ru": "Подробнее"}
T["back"] = {"zh": "返回", "en": "Back", "es": "Volver", "ar": "رجوع", "ru": "Назад"}
T["back_home"] = {"zh": "← 返回首页", "en": "← Back to Home", "es": "← Volver al Inicio", "ar": "← العودة للرئيسية", "ru": "← На главную"}
T["back_progs"] = {"zh": "← 返回专业列表", "en": "← Back to Programs", "es": "← Volver a Programas", "ar": "← العودة للبرامج", "ru": "← К программам"}
T["tuition_ug"] = {"zh": "学费（本科）", "en": "Tuition (UG)", "es": "Matrícula (Grado)", "ar": "الرسوم (بكالوريوس)", "ru": "Обучение (Бакалавр)"}
T["tuition_master"] = {"zh": "学费（硕士）", "en": "Tuition (Master)", "es": "Matrícula (Máster)", "ar": "الرسوم (ماجستير)", "ru": "Обучение (Магистр)"}
T["hsk"] = {"zh": "HSK等级", "en": "HSK", "es": "Nivel HSK", "ar": "مستوى HSK", "ru": "Уровень HSK"}
T["ielts"] = {"zh": "雅思要求", "en": "IELTS", "es": "Requisito IELTS", "ar": "متطلبات IELTS", "ru": "Требование IELTS"}
T["email_label"] = {"zh": "联系邮箱", "en": "Email", "es": "Correo", "ar": "البريد", "ru": "Эл. почта"}
T["phone_label"] = {"zh": "联系电话", "en": "Phone", "es": "Teléfono", "ar": "الهاتف", "ru": "Телефон"}
T["qs_rank"] = {"zh": "QS排名", "en": "QS Rank", "es": "Ranking QS", "ar": "تصنيف QS", "ru": "Рейтинг QS"}

def slug(s):
    return s.lower().replace(" ", "-").replace("'", "")

# ── CSS ──
CSS = """@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;0,900;1,500&family=Inter:wght@300;400;500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#0a1628;--gold:#c9a96e;--gold-l:#e8d5b0;--cream:#faf7f0;--white:#fff;--text:#1a1a2e;--text-l:#5a6070;--border:rgba(0,0,0,.08);--r:16px}
body{font-family:Inter,sans-serif;color:var(--text);background:var(--cream);line-height:1.7}
nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(10,22,40,.94);backdrop-filter:blur(20px);height:72px}
.ni{max-width:1280px;margin:0 auto;padding:0 32px;height:100%;display:flex;align-items:center;justify-content:space-between}
.nl{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--gold);text-decoration:none;display:flex;align-items:center;gap:10px}
.nlicon{width:34px;height:34px;background:linear-gradient(135deg,var(--gold),#a6844a);border-radius:8px;display:flex;align-items:center;justify-content:center;color:var(--navy);font-size:15px;font-weight:900}
.nli{display:flex;gap:6px}
.nli a{text-decoration:none;color:rgba(255,255,255,.75);font-size:14px;padding:10px 18px;border-radius:8px}
.nli a:hover,.nli a.ac{background:rgba(201,169,110,.15);color:var(--gold)}
.lb{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);padding:6px 10px;border-radius:6px;font-size:11px;cursor:pointer;color:rgba(255,255,255,.6);font-family:inherit;text-transform:uppercase}
.lb.on,.lb:hover{border-color:var(--gold);color:var(--gold)}
.hero{position:relative;min-height:90vh;display:flex;align-items:center;overflow:hidden;background:var(--navy)}
.hero-bg{position:absolute;inset:0;background:url(https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1920&q=80) center/cover;opacity:.35}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,22,40,.7),rgba(10,22,40,.5),rgba(10,22,40,.85))}
.hero-content{position:relative;z-index:2;max-width:800px;padding:120px 40px 80px}
.hero-badge{display:inline-block;border:1px solid var(--gold);color:var(--gold);font-size:11px;font-weight:600;letter-spacing:3px;padding:8px 20px;margin-bottom:28px;text-transform:uppercase}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(34px,5vw,54px);font-weight:900;color:var(--white);line-height:1.15;margin-bottom:20px}
.hero h1 span{color:var(--gold)}.hero p{font-size:17px;color:rgba(255,255,255,.7);font-weight:300;max-width:500px;margin-bottom:32px}
.search-box{display:flex;gap:12px;max-width:500px}
.search-box input{flex:1;padding:14px 20px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.1);color:white;border-radius:8px;font-size:15px;font-family:inherit;outline:none}
.search-box input::placeholder{color:rgba(255,255,255,.5)}.search-box input:focus{border-color:var(--gold)}
.search-box button{padding:14px 28px;background:var(--gold);color:var(--navy);border:none;border-radius:8px;font-weight:700;font-size:14px;cursor:pointer;font-family:inherit;transition:.2s}
.search-box button:hover{background:#d4b87a}
.hero-stats{display:flex;gap:60px;margin-top:40px}
.hs-num{font-family:'Playfair Display',serif;font-size:42px;font-weight:900;color:var(--gold)}.hs-label{font-size:13px;color:rgba(255,255,255,.55);text-transform:uppercase;letter-spacing:1.5px}
.section{padding:100px 32px;max-width:1200px;margin:0 auto}
.section-dark{background:var(--navy);max-width:100%;padding:100px 32px}
.section-dark .section-title{color:var(--white)}.section-dark .section-sub{color:rgba(255,255,255,.5)}
.section-header{text-align:center;margin-bottom:56px}
.section-label{font-size:11px;font-weight:600;letter-spacing:3px;color:var(--gold);text-transform:uppercase;margin-bottom:16px}
.section-title{font-family:'Playfair Display',serif;font-size:clamp(28px,3vw,36px);font-weight:700;margin-bottom:12px}
.section-sub{font-size:16px;color:var(--text-l)}
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px}
.card-grid-wide{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}
.card{background:var(--white);border-radius:var(--r);overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.06);transition:.35s;text-decoration:none;color:inherit;display:block}
.card:hover{transform:translateY(-6px);box-shadow:0 16px 48px rgba(0,0,0,.12)}
.card-img{height:180px;background-size:cover;background-position:center}
.card-body{padding:20px 24px 24px}
.card-title{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;margin-bottom:6px}
.card-sub{font-size:13px;color:var(--text-l)}
.tier-card{background:var(--white);border-radius:var(--r);padding:36px 32px;box-shadow:0 4px 24px rgba(0,0,0,.06);transition:.35s;text-decoration:none;color:inherit;display:block;position:relative;overflow:hidden}
.tier-card::before{content:"";position:absolute;top:0;left:0;right:0;height:4px}
.tier-card.c9::before{background:#b8860b}.tier-card.a985::before{background:#2471a3}.tier-card.a211::before{background:#1e8449}
.tier-card:hover{transform:translateY(-6px);box-shadow:0 16px 48px rgba(0,0,0,.12)}
.tier-icon{font-size:36px;margin-bottom:16px}
.tier-card h3{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;margin-bottom:8px}
.tier-card p{font-size:14px;color:var(--text-l)}
.prog-card{background:var(--white);border-radius:var(--r);padding:24px 20px;box-shadow:0 2px 16px rgba(0,0,0,.05);transition:.3s;text-decoration:none;color:inherit;border-top:3px solid transparent}
.prog-card:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(0,0,0,.1)}
.prog-icon{font-size:24px;margin-bottom:12px}.prog-card h3{font-size:15px;font-weight:600;margin-bottom:4px}.prog-card .prog-sub{font-size:11px;color:var(--text-l)}
.prog-list-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.uni-hero{background:var(--navy);padding:120px 32px 64px;text-align:center;color:var(--white)}
.uni-hero h1{font-family:'Playfair Display',serif;font-size:clamp(26px,4vw,40px);font-weight:900;margin-bottom:8px}
.uni-loc{font-size:15px;color:rgba(255,255,255,.55);margin-bottom:16px}
.tier-badge{display:inline-block;border:1px solid var(--gold);color:var(--gold);padding:6px 16px;font-size:11px;letter-spacing:2px;text-transform:uppercase}
.info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.info-item{background:var(--white);border-radius:var(--r);padding:20px;box-shadow:0 2px 12px rgba(0,0,0,.04);border-left:3px solid var(--gold)}
.info-item h4{font-size:10px;color:var(--gold);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px}
.info-item p{font-size:14px;font-weight:600}
.back-link{display:inline-flex;align-items:center;gap:6px;color:var(--gold);text-decoration:none;font-size:14px;margin-bottom:20px;font-weight:500}
.tier-section{margin-bottom:36px}
.tier-section h3{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid var(--gold-l)}
.ul-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.ul-item{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:14px 18px;text-decoration:none;color:var(--text);transition:.2s;display:block}
.ul-item:hover{border-color:var(--gold);box-shadow:0 4px 16px rgba(0,0,0,.08)}
.ul-name{font-weight:600;font-size:14px}.ul-meta{font-size:11px;color:var(--text-l);margin-top:2px}
.prog-hero{padding:120px 32px 64px;text-align:center;color:var(--white)}
.prog-hero h1{font-family:'Playfair Display',serif;font-size:clamp(26px,4vw,40px);font-weight:900;margin-bottom:8px}
.prog-sub{font-size:15px;opacity:.8}.prog-meta{font-size:13px;opacity:.6;margin-top:6px}
.intro-section{max-width:900px;margin:0 auto;padding:80px 32px;text-align:center}
.intro-section h2{font-family:'Playfair Display',serif;font-size:30px;font-weight:700;margin-bottom:20px}
.intro-section p{font-size:16px;color:var(--text-l);line-height:1.9}
footer{background:var(--navy);color:rgba(255,255,255,.6);padding:56px 32px 36px;text-align:center}
footer .f-brand{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--gold);margin-bottom:10px}
footer p{font-size:13px;max-width:600px;margin:0 auto;line-height:1.8}
footer .f-links{margin-top:20px;display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
footer .f-links a{color:rgba(255,255,255,.5);text-decoration:none;font-size:13px}
footer .f-links a:hover{color:var(--gold)}footer .f-copy{margin-top:28px;font-size:11px;color:rgba(255,255,255,.3)}
.container{max-width:1100px;margin:0 auto;padding:0 20px}
@media(max-width:768px){.nli{display:none}.hero h1{font-size:30px}.hero-stats{gap:28px;flex-wrap:wrap}.section{padding:60px 20px}.card-grid{grid-template-columns:1fr}.tier-card{grid-template-columns:1fr}}
"""

CITY_IMG = {
    "Beijing": "https://images.unsplash.com/photo-1523730205978-59fd1b2965e3?w=800&q=80",
    "Shanghai": "https://images.unsplash.com/photo-1548625361-1d6c4ca5e26f?w=800&q=80",
    "Guangzhou": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&q=80",
    "Chengdu": "https://images.unsplash.com/photo-1562774053-701939374585?w=800&q=80",
    "Wuhan": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800&q=80",
    "Xi'an": "https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800&q=80",
    "Nanjing": "https://images.unsplash.com/photo-1562774053-701939374585?w=800&q=80",
    "Hangzhou": "https://images.unsplash.com/photo-1547981609-4b6bfe67ca0b?w=800&q=80",
}
FALLBACK_IMG = "https://images.unsplash.com/photo-1562774053-701939374585?w=800&q=80"

# ── HTML组件 ──
def nav(lang, depth=0):
    up = "../" * depth
    # Language buttons redirect to root SPA with ?lang= param for language persistence
    lb = "".join(['<button class="lb ' + ('on' if x == lang else '') + '" onclick="var u=\'' + up + '\';localStorage.setItem(\'chinauni_lang\',\'' + x + '\');location.href=u+\'index.html?lang=' + x + '\'">' + x + '</button>' for x in LANGS])
    return '<nav><div class="ni"><a href="' + up + 'index.html" class="nl"><span class="nlicon">大</span>' + t("site", lang) + '</a><div class="nli"><a href="' + up + 'index.html" class="ac">' + t("home", lang) + '</a><a href="' + up + 'cities.html">' + t("cities", lang) + '</a><a href="' + up + 'tiers.html">' + t("tiers", lang) + '</a><a href="' + up + 'programs.html">' + t("programs", lang) + '</a></div><div>' + lb + '</div></div></nav>'

def head(lang, title, depth=0):
    return '<!DOCTYPE html><html lang="' + lang + '"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>' + title + '</title><style>' + CSS + '</style></head><body>' + nav(lang, depth)

def foot(lang, depth=0):
    up = "../" * depth
    return '<footer><div class="f-brand">' + t("site", lang) + '</div><p>' + t("disc", lang) + '</p><div class="f-links"><a href="' + up + 'about.html">' + t("about", lang) + '</a></div><div class="f-copy">&copy; 2026</div></footer></body></html>'

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ── 建站 ──
def build():
    OUT = os.path.join(DESKTOP)
    
    # 城市统计
    cts = {}
    c9 = []; a9 = []; d1 = []
    for u in UNIS:
        cts[u["city"]] = cts.get(u["city"], 0) + 1
        tier = u.get("tier", "")
        if tier == "C9": c9.append(u)
        elif tier == "985": a9.append(u)
        elif tier == "211": d1.append(u)
    
    for lang in LANGS:
        d = os.path.join(OUT, lang)
        for sd in ["", "cities", "tiers", "uni", "programs"]:
            os.makedirs(os.path.join(d, sd), exist_ok=True)
        
        up0 = ""; up1 = "../"  # depth 0 and depth 1 prefixes
        
        # ══════ 首页 (depth 0) ══════
        tc = sorted(cts.items(), key=lambda x: -x[1])[:12]
        cc = "".join(['<a href="cities/' + slug(c) + '.html" class="card"><div class="card-img" style="background-image:url(' + CITY_IMG.get(c, FALLBACK_IMG) + ')"></div><div class="card-body"><div class="card-title">' + c + '</div><div class="card-sub">' + str(n) + ' ' + t("uni_count", lang) + '</div></div></a>' for c, n in tc])
        
        tier_cards = ""
        for cl, label, icon, n in [("c9", "tier_c9", "🥇", len(c9)), ("a985", "tier_985", "🥈", len(a9)), ("a211", "tier_211", "🥉", len(d1))]:
            tier_cards += '<a href="tiers/' + cl + '.html" class="tier-card ' + cl + '"><div class="tier-icon">' + icon + '</div><h3>' + t(label, lang) + '</h3><p>' + str(n) + ' ' + t("uni_count", lang) + '</p></a>'
        
        pp = []
        seen = set()
        for p in PROGS:
            if p["category"] not in seen and len(pp) < 8:
                pp.append(p); seen.add(p["category"])
        pc = "".join(['<a href="programs/' + p["id"] + '.html" class="prog-card" style="border-top-color:' + CAT_COLOR.get(p["category"], "#ccc") + '"><div class="prog-icon">' + CAT_ICON.get(p["category"], "📖") + '</div><h3>' + p["program_en"] + '</h3><div class="prog-sub">' + p.get("program_zh", "") + '</div></a>' for p in pp])
        
        index_html = head(lang, t("site", lang), 0)
        index_html += '<div class="hero"><div class="hero-bg"></div><div class="hero-overlay"></div><div class="hero-content"><div class="hero-badge">Academic Excellence</div><h1>' + t("site", lang) + '</h1><p>' + t("tagline", lang) + '</p><div class="search-box"><input type="text" placeholder="' + t("search", lang) + '" oninput="var q=this.value.toLowerCase();document.querySelectorAll(\'.card,.prog-card,.tier-card\').forEach(function(e){e.style.display=e.textContent.toLowerCase().includes(q)?\'\':\'none\'})"><button onclick="this.previousElementSibling.focus()">🔍</button></div><div class="hero-stats"><div><div class="hs-num">' + str(len(UNIS)) + '</div><div class="hs-label">' + t("uni_count", lang) + '</div></div><div><div class="hs-num">' + str(len(PROGS)) + '</div><div class="hs-label">' + t("prog_count", lang) + '</div></div><div><div class="hs-num">' + str(len(cts)) + '</div><div class="hs-label">' + t("city_count", lang) + '</div></div></div></div></div>'
        # Why China intro
        index_html += '<div class="intro-section"><h2>' + t("intro_title", lang) + '</h2><p>' + t("intro_text", lang) + '</p></div>'
        # Cities section
        index_html += '<div class="section"><div class="section-header"><div class="section-label">Location</div><div class="section-title">' + t("by_region", lang) + '</div></div><div class="card-grid">' + cc + '</div></div>'
        # Tiers
        index_html += '<div class="section-dark"><div style="max-width:1200px;margin:0 auto"><div class="section-header"><div class="section-label">Prestige</div><div class="section-title">' + t("by_tier", lang) + '</div></div><div class="card-grid-wide">' + tier_cards + '</div></div></div>'
        # Programs
        index_html += '<div class="section"><div class="section-header"><div class="section-label">Academics</div><div class="section-title">' + t("by_prog", lang) + '</div></div><div class="prog-list-grid">' + pc + '</div></div>'
        index_html += foot(lang, 0)
        w(os.path.join(d, "index.html"), index_html)
        
        # ══════ 城市列表 (depth 0) ══════
        sc = sorted(cts.items(), key=lambda x: -x[1])
        cl_cards = "".join(['<a href="cities/' + slug(c) + '.html" class="card"><div class="card-img" style="background-image:url(' + CITY_IMG.get(c, FALLBACK_IMG) + ')"></div><div class="card-body"><div class="card-title">' + c + '</div><div class="card-sub">' + str(n) + ' ' + t("uni_count", lang) + '</div></div></a>' for c, n in sc])
        cities_html = head(lang, t("cities", lang), 0) + '<div style="padding-top:100px" class="container"><h1 style="font-family:Playfair Display,serif;font-size:34px;font-weight:900;margin-bottom:8px">' + t("cities", lang) + '</h1><p style="color:var(--text-l);margin-bottom:36px">' + str(len(sc)) + ' ' + t("city_count", lang) + '</p><div class="card-grid">' + cl_cards + '</div></div>' + foot(lang, 0)
        w(os.path.join(d, "cities.html"), cities_html)
        
        # ══════ 城市详情 (depth 1) ══════
        for city in cts:
            cl = sorted([u for u in UNIS if u["city"] == city], key=lambda u: ({"C9": 0, "985": 1, "211": 2}.get(u.get("tier", ""), 3)))
            ul = "".join(['<a href="../uni/' + slug(u["name_en"]) + '.html" class="ul-item"><div class="ul-name">' + u["name_en"] + '</div><div class="ul-meta">' + u.get("tier", "") + ' · ' + u.get("city", "") + '</div></a>' for u in cl])
            ch = head(lang, city, 1) + '<div style="padding-top:100px" class="container"><a href="../index.html" class="back-link">' + t("back_home", lang) + '</a><h1 style="font-family:Playfair Display,serif;font-size:34px;font-weight:900;margin-bottom:8px">' + city + '</h1><p style="color:var(--text-l);margin-bottom:32px">' + str(len(cl)) + ' ' + t("uni_count", lang) + '</p><div class="ul-grid">' + ul + '</div></div>' + foot(lang, 1)
            w(os.path.join(d, "cities", slug(city) + ".html"), ch)
        
        # ══════ 层次详情 (depth 1) ══════
        for cls, tier_name in [("c9", "C9"), ("a985", "985"), ("a211", "211")]:
            tl = [u for u in UNIS if u.get("tier") == tier_name]
            ul = "".join(['<a href="../uni/' + slug(u["name_en"]) + '.html" class="ul-item"><div class="ul-name">' + u["name_en"] + '</div><div class="ul-meta">' + u.get("city", "") + '</div></a>' for u in tl])
            key = "tier_c9" if cls == "c9" else ("tier_985" if cls == "a985" else "tier_211")
            th = head(lang, t(key, lang), 1) + '<div style="padding-top:100px" class="container"><a href="../index.html" class="back-link">' + t("back_home", lang) + '</a><h1 style="font-family:Playfair Display,serif;font-size:34px;font-weight:900;margin-bottom:8px">' + t(key, lang) + '</h1><p style="color:var(--text-l);margin-bottom:32px">' + str(len(tl)) + ' ' + t("uni_count", lang) + '</p><div class="ul-grid">' + ul + '</div></div>' + foot(lang, 1)
            w(os.path.join(d, "tiers", cls + ".html"), th)
        
        # ══════ 层次总览 (depth 0) ══════
        tall = ""
        for cls, tier_name, icon in [("c9", "C9", "🥇"), ("a985", "985", "🥈"), ("a211", "211", "🥉")]:
            tl = [u for u in UNIS if u.get("tier") == tier_name]
            key = "tier_c9" if cls == "c9" else ("tier_985" if cls == "a985" else "tier_211")
            ul = "".join(['<a href="uni/' + slug(u["name_en"]) + '.html" class="ul-item"><div class="ul-name">' + u["name_en"] + '</div><div class="ul-meta">' + u.get("city", "") + '</div></a>' for u in tl])
            tall += '<div style="margin-bottom:48px"><h2 style="font-family:Playfair Display,serif;font-size:26px;font-weight:700;margin-bottom:8px">' + icon + ' ' + t(key, lang) + '</h2><p style="color:var(--text-l);margin-bottom:18px">' + str(len(tl)) + ' ' + t("uni_count", lang) + '</p><div class="ul-grid">' + ul + '</div></div>'
        tiers_all_html = head(lang, t("tiers", lang), 0) + '<div style="padding-top:100px" class="container">' + tall + '</div>' + foot(lang, 0)
        w(os.path.join(d, "tiers.html"), tiers_all_html)
        
        # ══════ 大学详情 (depth 1) ══════
        for u in UNIS:
            # Use language-specific name and description
            name = u.get("name_" + lang, u.get("name_en", ""))
            name_en = u.get("name_en", ""); name_zh = u.get("name_zh", "")
            tier = u.get("tier", "211")
            qs = " · " + t("qs_rank", lang) + ": " + str(u["qs_rank"]) if u.get("qs_rank") else ""
            desc = u.get("description_" + lang, u.get("description_en", ""))
            web = u.get("website_intl", "#")
            city = u.get("city_" + lang, u.get("city", ""))
            rows = ""
            for lbl_key, key in [("tuition_ug", "tuition_undergraduate"), ("tuition_master", "tuition_master"), ("hsk", "hsk_required"), ("ielts", "ielts_required"), ("email_label", "intl_office_email"), ("phone_label", "intl_office_phone")]:
                val = str(u.get(key, "-"))
                rows += '<div class="info-item"><h4>' + t(lbl_key, lang) + '</h4><p>' + val + '</p></div>'
            top = u.get("top_programs", [])
            tp = '<div style="margin-top:28px"><h3 style="font-family:Playfair Display,serif;font-size:20px;margin-bottom:14px">' + t("dist_prog", lang) + '</h3><div>' + "".join(['<span style="display:inline-block;background:var(--gold-l);color:#a6844a;padding:6px 14px;border-radius:16px;font-size:12px;margin:3px">' + x + '</span>' for x in top]) + '</div></div>' if top else ""
            uh = head(lang, name, 1) + '<div class="uni-hero"><h1>' + name + '</h1><div class="uni-loc">' + city + qs + '</div><div class="tier-badge">' + tier + '</div></div><div class="container" style="margin-top:-36px">'
            if desc: uh += '<p style="font-size:15px;color:var(--text);line-height:1.8;margin-bottom:28px;max-width:800px">' + desc + '</p>'
            uh += '<div class="info-grid">' + rows + '</div><div style="margin-top:20px"><strong>' + t("website", lang) + ':</strong> <a href="' + web + '" target="_blank" rel="noopener" style="color:var(--gold)">' + web + '</a></div>' + tp + '</div>' + foot(lang, 1)
            w(os.path.join(d, "uni", slug(name_en) + ".html"), uh)
        
        # ══════ 专业列表 (depth 0) — 分STEM/Humanities ══════
        stem_cats = ("Medicine", "Engineering", "Sciences", "Agriculture")
        hum_cats = ("Business", "Humanities", "Arts")
        stem_p = [p for p in PROGS if p["category"] in stem_cats]
        hum_p = [p for p in PROGS if p["category"] in hum_cats]
        def pcard(p):
            return '<a href="programs/' + p["id"] + '.html" class="prog-card" style="border-top-color:' + CAT_COLOR.get(p["category"], "#ccc") + '"><div class="prog-icon">' + CAT_ICON.get(p["category"], "📖") + '</div><h3>' + p["program_en"] + '</h3><div class="prog-sub">' + p.get("program_zh", "") + '</div></a>'
        stem_cards = "".join([pcard(p) for p in stem_p])
        hum_cards = "".join([pcard(p) for p in hum_p])
        pl = head(lang, t("programs", lang), 0) + '<div style="padding-top:100px" class="container"><h1 style="font-family:Playfair Display,serif;font-size:34px;font-weight:900;margin-bottom:8px">' + t("programs", lang) + '</h1><p style="color:var(--text-l);margin-bottom:36px">' + str(len(PROGS)) + ' ' + t("prog_count", lang) + '</p>'
        pl += '<div style="margin-bottom:40px"><h2 style="font-family:Playfair Display,serif;font-size:22px;font-weight:700;margin-bottom:18px;color:var(--text)">🔬 ' + t("stem", lang) + ' (' + str(len(stem_p)) + ')</h2><div class="prog-list-grid">' + stem_cards + '</div></div>'
        pl += '<div><h2 style="font-family:Playfair Display,serif;font-size:22px;font-weight:700;margin-bottom:18px;color:var(--text)">📖 ' + t("humanities", lang) + ' (' + str(len(hum_p)) + ')</h2><div class="prog-list-grid">' + hum_cards + '</div></div></div>' + foot(lang, 0)
        w(os.path.join(d, "programs.html"), pl)
        
        # ══════ 专业详情 (depth 1) ══════
        for p in PROGS:
            name = p["program_en"]; zh = p.get("program_zh", ""); cat = p["category"]
            dur = p.get("duration", ""); lt = p.get("teaching_language", ""); desc = p.get("description", "")
            unis_in_prog = p.get("universities", [])
            # 标记强弱
            for u in unis_in_prog:
                if "strength_tier" not in u:
                    u["strength_tier"] = "available"
            tiers_html = ""
            for label, key in [(t("top", lang), "top_choice"), (t("strong", lang), "strong"), (t("avail", lang), "available")]:
                items = [u for u in unis_in_prog if u.get("strength_tier") == key]
                if items:
                    tags = "".join(['<a href="../uni/' + slug(u["name_en"]) + '.html" class="ul-item"><div class="ul-name">' + u["name_en"] + '</div><div class="ul-meta">' + u.get("city", "") + ' · ' + u.get("tier", "") + '</div></a>' for u in items])
                    tiers_html += '<div class="tier-section"><h3>' + label + ' (' + str(len(items)) + ')</h3><div class="ul-grid">' + tags + '</div></div>'
            ph = head(lang, name, 1) + '<div class="prog-hero" style="background:linear-gradient(135deg,' + CAT_COLOR.get(cat, "#333") + ',var(--navy))"><h1>' + CAT_ICON.get(cat, "📖") + ' ' + name + '</h1><div class="prog-sub">' + zh + '</div><div class="prog-meta">' + dur + ' · ' + lt + '</div></div><div class="container"><a href="../programs.html" class="back-link">' + t("back_progs", lang) + '</a>'
            if desc: ph += '<p style="color:var(--text-l);font-size:15px;line-height:1.8;margin-bottom:20px">' + desc + '</p>'
            ph += tiers_html + '</div>' + foot(lang, 1)
            w(os.path.join(d, "programs", p["id"] + ".html"), ph)
        
        # ══════ About (depth 0) ══════
        about_html = head(lang, t("about", lang), 0) + '<div style="padding-top:100px" class="container"><h1 style="font-family:Playfair Display,serif;font-size:34px;font-weight:900">' + t("about", lang) + '</h1><p style="margin-top:20px;line-height:1.8;max-width:700px">A comprehensive directory of 116 Chinese universities across 40 cities, featuring 56 academic programs. Designed for international students exploring higher education in China. We do not provide application services or consulting.</p></div>' + foot(lang, 0)
        w(os.path.join(d, "about.html"), about_html)
        
        print("  ✅ " + lang.upper())
    
    # 入口页
    w(os.path.join(OUT, "index.html"), '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta http-equiv="refresh" content="0;url=en/index.html"></head><body><a href="en/index.html">Enter</a></body></html>')
    
    tf = sum(1 for _ in os.walk(OUT) for __ in _[2])
    print("\n✅ 全站生成完成！" + str(tf) + " 文件 → " + OUT)
    print("双击 " + os.path.join(OUT, "index.html") + " 开始浏览")

if __name__ == "__main__":
    build()
