#!/usr/bin/env python3
"""Generate compare.html with embedded university data and comparison logic"""

import json

# Read data
with open('assets/unis_data.json', 'r', encoding='utf-8') as f:
    unis = json.load(f)
with open('assets/i18n_data.json', 'r', encoding='utf-8') as f:
    i18n = json.load(f)

# Read base HTML
base_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>University Comparison - China University Directory</title>
<meta name="description" content="Compare Chinese universities side by side - rankings, tuition fees, admission requirements, and program strengths.">
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#0a1628;--gold:#c9a96e;--gold-l:#e8d5b0;--cream:#faf7f0;--white:#fff;--text:#1a1a2e;--text-l:#5a6070;--border:rgba(0,0,0,.08);--r:16px;--green:#1e8449;--blue:#2471a3}
html{scroll-behavior:smooth}
body{font-family:Inter,-apple-system,sans-serif;color:var(--text);background:var(--cream);line-height:1.7;overflow-x:hidden}
html[dir=rtl] body{font-family:'Noto Naskh Arabic',Inter,sans-serif}

/* Nav */
nav{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(10,22,40,.95);backdrop-filter:blur(20px);height:72px}
.ni{max-width:1280px;margin:0 auto;padding:0 32px;height:100%;display:flex;align-items:center;justify-content:space-between}
.nl{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--gold);text-decoration:none;display:flex;align-items:center;gap:10px;cursor:pointer}
.nlicon{width:34px;height:34px;background:linear-gradient(135deg,var(--gold),#a6844a);border-radius:8px;display:flex;align-items:center;justify-content:center;color:var(--navy);font-size:15px;font-weight:900}
.nr{display:flex;align-items:center;gap:10px}
.lb{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);padding:6px 10px;border-radius:6px;font-size:11px;cursor:pointer;color:rgba(255,255,255,.6);font-family:inherit;font-weight:500;text-transform:uppercase;transition:.2s;outline:none;white-space:nowrap}
.lb:hover,.lb.on{border-color:var(--gold);color:var(--gold);background:rgba(201,169,110,.1)}
.back-link{color:rgba(255,255,255,.7);text-decoration:none;font-size:13px;padding:8px 14px;border-radius:8px;transition:.2s;white-space:nowrap}
.back-link:hover{background:rgba(255,255,255,.08);color:var(--gold)}

/* Main */
main{padding-top:72px;max-width:1280px;margin:0 auto;min-height:100vh}
.cmp-header{text-align:center;padding:60px 32px 40px}
.cmp-badge{display:inline-block;border:1px solid var(--gold);color:var(--gold);font-size:11px;font-weight:600;letter-spacing:3px;padding:8px 20px;margin-bottom:20px;text-transform:uppercase}
.cmp-title{font-family:'Playfair Display',serif;font-size:clamp(28px,4vw,42px);font-weight:900;color:var(--navy);margin-bottom:10px}
.cmp-sub{font-size:16px;color:var(--text-l);max-width:550px;margin:0 auto}

/* Search area */
.search-area{max-width:900px;margin:0 auto 40px;padding:0 32px;position:relative}
.search-box{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.search-input-wrap{flex:1;min-width:280px;position:relative}
.search-input{width:100%;padding:14px 20px;border:2px solid var(--border);border-radius:12px;font-size:15px;font-family:inherit;background:var(--white);color:var(--text);transition:.2s;outline:none}
.search-input:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(201,169,110,.15)}
.search-dropdown{position:absolute;top:100%;left:0;right:0;margin-top:6px;background:var(--white);border-radius:12px;box-shadow:0 12px 48px rgba(0,0,0,.15);max-height:320px;overflow-y:auto;z-index:100;display:none}
.search-dropdown.show{display:block}
.dropdown-item{padding:14px 20px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);transition:.15s;font-size:14px}
.dropdown-item:hover{background:#fdfaf3}
.dropdown-item.disabled{opacity:.4;pointer-events:none}
.di-name{font-weight:600;font-family:'Playfair Display',serif}
.di-info{font-size:12px;color:var(--text-l);margin-top:2px}
.di-add{color:var(--gold);font-size:20px;font-weight:700;flex-shrink:0;margin-left:12px}
.badge-tier{font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;color:var(--white);white-space:nowrap;display:inline-block;margin-left:4px}
.badge-tier.c9{background:linear-gradient(135deg,#b8860b,#daa520)}
.badge-tier.a985{background:linear-gradient(135deg,#2471a3,#4a90d9)}
.badge-tier.a211{background:linear-gradient(135deg,#1e8449,#27ae60)}

.btn-cmp{padding:14px 28px;border:none;border-radius:12px;font-size:14px;font-weight:600;font-family:inherit;cursor:pointer;transition:.2s;white-space:nowrap}
.btn-add{background:var(--navy);color:var(--gold)}
.btn-add:hover{background:#1a2a48}
.btn-clear{background:transparent;border:1.5px solid var(--border);color:var(--text-l)}
.btn-clear:hover{border-color:#d44;color:#d44}

/* Selected universities */
.selected-area{max-width:1280px;margin:0 auto;padding:0 32px 48px;display:none}
.selected-area.show{display:block}
.selected-label{font-size:12px;font-weight:600;letter-spacing:2px;color:var(--text-l);text-transform:uppercase;margin-bottom:16px;text-align:center}

.slots{display:flex;gap:16px;overflow-x:auto;padding:8px 0 24px;-webkit-overflow-scrolling:touch}
.slot{flex:1;min-width:220px;background:var(--white);border-radius:var(--r);padding:24px;position:relative;border:2px solid var(--border);text-align:center;min-height:140px;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:.25s}
.slot.filled{border-color:rgba(201,169,110,.3);text-align:left;align-items:stretch;justify-content:flex-start;background:linear-gradient(180deg,#fdfaf3,#fff)}
.slot.filled:hover{border-color:var(--gold);box-shadow:0 8px 36px rgba(0,0,0,.1);transform:translateY(-2px)}
.slot-empty-icon{font-size:36px;color:rgba(0,0,0,.08);margin-bottom:10px}
.slot-empty-text{font-size:13px;color:var(--text-l)}
.slot-num{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--navy);color:var(--gold);width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.slot-remove{position:absolute;top:10px;right:10px;width:24px;height:24px;border-radius:50%;border:none;background:rgba(0,0,0,.06);color:var(--text-l);font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;line-height:1;transition:.2s}
.slot-remove:hover{background:#fee;color:#d44}
.slot-name{font-family:'Playfair Display',serif;font-size:17px;font-weight:700;color:var(--navy);margin-bottom:2px}
.slot-name-zh{font-size:12px;color:var(--text-l);margin-bottom:10px}
.slot-city{font-size:12px;color:var(--text-l)}
.slot-rank{font-size:13px;font-weight:600;color:var(--gold);margin-top:6px}

/* Comparison Table */
.cmp-table-wrap{max-width:1280px;margin:0 auto;padding:0 32px 80px;display:none}
.cmp-table-wrap.show{display:block}
.cmp-table-scroll{overflow-x:auto}
.cmp-table{width:100%;border-collapse:collapse;background:var(--white);border-radius:var(--r);overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.08);min-width:600px}
.cmp-table th,.cmp-table td{padding:16px 20px;text-align:center;border-bottom:1px solid var(--border);font-size:14px;vertical-align:middle}
.cmp-table thead th{background:var(--navy);color:var(--gold);font-family:'Playfair Display',serif;font-size:15px;font-weight:700;position:sticky;top:72px;z-index:10}
.cmp-table thead th:first-child{text-align:left;background:var(--navy);width:160px;color:rgba(255,255,255,.5);font-size:11px;letter-spacing:1px}
.cmp-table tbody th{text-align:left;font-weight:600;color:var(--text);background:#fafaf7;font-size:13px;white-space:nowrap;width:160px}
.cmp-table tbody td{font-size:13px;color:var(--text);line-height:1.5}
.cmp-table tbody tr:hover td{background:#fdfaf3}
.cmp-table tbody tr.row-section th{background:var(--navy);color:var(--gold);font-size:11px;letter-spacing:2px;text-transform:uppercase;padding:10px 20px}
.cmp-table tbody tr.row-section td{background:var(--navy)}
.cmp-highlight{color:var(--gold);font-weight:700}
.prog-tags-wrap{display:flex;flex-wrap:wrap;gap:4px;justify-content:center}
.prog-tag{font-size:10px;font-weight:600;padding:3px 10px;border-radius:4px;background:rgba(201,169,110,.12);color:#8b6914;white-space:nowrap}
.med-info{font-size:12px;color:var(--text-l);line-height:1.6}
.med-highlight{color:var(--gold);font-weight:700;font-size:13px}
.med-strength{font-size:11px;color:var(--text-l)}
td a{color:var(--blue);font-size:12px;word-break:break-all}

/* Empty state */
.empty-state{text-align:center;padding:80px 32px}
.empty-icon{font-size:64px;margin-bottom:20px}
.empty-title{font-family:'Playfair Display',serif;font-size:24px;font-weight:700;color:var(--navy);margin-bottom:8px}
.empty-sub{font-size:15px;color:var(--text-l);max-width:450px;margin:0 auto}

@media(max-width:768px){
  .ni{padding:0 16px;gap:8px}
  .nl{font-size:16px}
  .back-link{font-size:12px;padding:6px 10px}
  .lb{padding:4px 8px;font-size:10px}
  .cmp-header{padding:40px 20px 30px}
  .cmp-title{font-size:28px}
  .search-area{padding:0 20px}
  .search-box{flex-direction:column}
  .search-input-wrap{min-width:auto}
  .slots{flex-direction:column;overflow-x:visible}
  .slot{min-width:auto;min-height:100px}
  .cmp-table-wrap{padding:0 8px 80px}
  .cmp-table-wrap.show{overflow-x:auto}
  .cmp-table{font-size:11px}
  .cmp-table th,.cmp-table td{padding:10px 10px;font-size:11px}
  .cmp-table thead th:first-child{width:90px}
  .cmp-table tbody th{width:90px;font-size:11px}
}
</style>
</head>
<body>
<nav>
  <div class="ni">
    <a class="nl" href="index.html"><span class="nlicon">大</span><span data-i18n="site">China University Directory</span></a>
    <div class="nr">
      <a href="index.html" class="back-link">← <span data-i18n="back_home">Home</span></a>
      <button class="lb" onclick="switchLang('zh')">zh</button>
      <button class="lb on" onclick="switchLang('en')">en</button>
      <button class="lb" onclick="switchLang('es')">es</button>
      <button class="lb" onclick="switchLang('ar')">ar</button>
      <button class="lb" onclick="switchLang('ru')">ru</button>
    </div>
  </div>
</nav>

<main>
  <div class="cmp-header">
    <div class="cmp-badge" data-i18n="cmp_badge">Side-by-Side Analysis</div>
    <h1 class="cmp-title" data-i18n="cmp_title">Compare Universities</h1>
    <p class="cmp-sub" data-i18n="cmp_sub">Select 2-4 universities to compare rankings, tuition fees, admission requirements, and program strengths side by side.</p>
  </div>

  <div class="search-area">
    <div class="search-box">
      <div class="search-input-wrap">
        <input type="text" class="search-input" data-i18n-placeholder="search_ph" placeholder="Search universities by name or city..." oninput="searchUnis(this.value)" onfocus="searchUnis(this.value)">
        <div class="search-dropdown" id="search-dropdown"></div>
      </div>
      <button class="btn-cmp btn-clear" onclick="clearAll()" data-i18n="clear_all">Clear All</button>
    </div>
    <div style="margin-top:12px;font-size:11px;color:var(--text-l);text-align:center" data-i18n="cmp_hint">Type to search, click to add. Compare up to 4 universities.</div>
  </div>

  <div class="selected-area" id="selected-area">
    <div class="selected-label"><span data-i18n="selected_label">Selected Universities</span> · <span id="selected-count">0</span>/4</div>
    <div class="slots" id="slots">
      <div class="slot" id="slot-0"><div class="slot-num">1</div><div class="slot-empty-icon">🏛️</div><div class="slot-empty-text" data-i18n="add_uni">Add a university</div></div>
      <div class="slot" id="slot-1"><div class="slot-num">2</div><div class="slot-empty-icon">🏛️</div><div class="slot-empty-text" data-i18n="add_uni">Add a university</div></div>
    </div>
  </div>

  <div class="cmp-table-wrap" id="cmp-table-wrap">
    <div class="cmp-table-scroll">
      <table class="cmp-table" id="cmp-table"></table>
    </div>
  </div>
</main>

<div style="text-align:center;padding:24px 32px 40px;font-size:11px;color:var(--text-l)" data-i18n="disc">For reference only. Verify all information with official university websites.</div>
'''

# Build JS block
js_lines = []

js_lines.append('<script>')
js_lines.append('const UNIS=%s;' % json.dumps(unis, ensure_ascii=False))
js_lines.append('const I18N=%s;' % json.dumps(i18n, ensure_ascii=False))
js_lines.append('const LANGS=["zh","en","es","ar","ru"];')
js_lines.append('let currentLang="en";')
js_lines.append('let selectedUnis=[];')
js_lines.append('const MAX_SELECT=4;')

js_lines.append('function t(key){return (I18N[currentLang]&&I18N[currentLang][key])||key;}')

# Language switch
js_lines.append('''function switchLang(lang){
  currentLang=lang;
  localStorage.setItem("chinauni_lang",lang);
  document.querySelectorAll(".lb").forEach(function(b){b.classList.toggle("on",b.textContent.trim()===lang.toUpperCase())});
  document.querySelectorAll("[data-i18n]").forEach(function(el){
    var k=el.dataset.i18n;var v=I18N[lang]&&I18N[lang][k];
    if(v)el.textContent=v;
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(function(el){
    var k=el.dataset.i18nPlaceholder;var v=I18N[lang]&&I18N[lang][k];
    if(v)el.placeholder=v;
  });
  document.documentElement.lang=lang;
  document.documentElement.dir=(lang==="ar")?"rtl":"ltr";
  updateSlots();
  if(selectedUnis.length>=2)renderTable();
}''')

# Search
js_lines.append('''function searchUnis(query){
  var dd=document.getElementById("search-dropdown");
  if(!query||query.length<1){dd.classList.remove("show");return}
  query=query.toLowerCase();
  var results=UNIS.filter(function(u){
    return u.name_en.toLowerCase().indexOf(query)>=0||u.name_zh.indexOf(query)>=0||u.city.toLowerCase().indexOf(query)>=0
  }).slice(0,12);
  if(results.length===0){
    dd.innerHTML='<div style="padding:20px;text-align:center;color:var(--text-l);font-size:13px">'+t("no_results")+'</div>';
    dd.classList.add("show");return;
  }
  var html="";
  results.forEach(function(u){
    var selected=selectedUnis.some(function(s){return s.name_en===u.name_en});
    var cls=selected?"disabled":"";
    var badge=u.tier==="C9"?"c9":u.tier==="985"?"a985":"a211";
    html+='<div class="dropdown-item '+cls+'" onclick="addUni(\\''+esc(u.name_en)+'\\')">'
      +'<div><div class="di-name">'+u.name_en+' <span class="badge-tier '+badge+'">'+u.tier+'</span></div>'
      +'<div class="di-info">'+u.city+' · QS #'+u.qs_rank+'</div></div>'
      +'<div class="di-add">'+(selected?"✓":"+")+'</div></div>';
  });
  dd.innerHTML=html;dd.classList.add("show");
}''')

js_lines.append("""function esc(s){return s.replace(/'/g,"\\\\'")}""")

# Add/remove
js_lines.append('''function addUni(name){
  if(selectedUnis.length>=MAX_SELECT)return;
  var uni=UNIS.find(function(u){return u.name_en===name});
  if(!uni||selectedUnis.some(function(s){return s.name_en===name}))return;
  selectedUnis.push(uni);updateSlots();
  if(selectedUnis.length>=2)renderTable();
  document.getElementById("search-dropdown").classList.remove("show");
  document.querySelector(".search-input").value="";
}''')

js_lines.append('''function removeUni(idx){
  selectedUnis.splice(idx,1);updateSlots();
  if(selectedUnis.length>=2)renderTable();
  else document.getElementById("cmp-table-wrap").classList.remove("show");
}''')

js_lines.append('''function clearAll(){
  selectedUnis=[];updateSlots();
  document.getElementById("cmp-table-wrap").classList.remove("show");
}''')

# Slots update
js_lines.append('''function updateSlots(){
  var area=document.getElementById("selected-area");
  document.getElementById("selected-count").textContent=selectedUnis.length;
  if(selectedUnis.length===0){area.classList.remove("show");return}
  area.classList.add("show");
  var html="";
  for(var i=0;i<MAX_SELECT;i++){
    if(i<selectedUnis.length){
      var u=selectedUnis[i];
      var badge=u.tier==="C9"?"c9":u.tier==="985"?"a985":"a211";
      var zhName=currentLang==="zh"?u.name_zh:u.name_en;
      html+='<div class="slot filled">'
        +'<div class="slot-num">'+(i+1)+'</div>'
        +'<button class="slot-remove" onclick="removeUni('+i+')">\u00d7</button>'
        +'<div class="slot-name"><span class="badge-tier '+badge+'" style="margin-right:6px">'+u.tier+'</span>'+u.name_en+'</div>'
        +'<div class="slot-name-zh">'+u.name_zh+'</div>'
        +'<div class="slot-city">'+u.city+'</div>'
        +'<div class="slot-rank">QS Rank: #'+u.qs_rank+'</div>'
        +'</div>';
    }else{
      html+='<div class="slot">'
        +'<div class="slot-num">'+(i+1)+'</div>'
        +'<div class="slot-empty-icon">🏛️</div>'
        +'<div class="slot-empty-text">'+t("add_uni")+'</div>'
        +'</div>';
    }
  }
  document.getElementById("slots").innerHTML=html;
}''')

# Table rendering
js_lines.append('''function renderTable(){
  document.getElementById("cmp-table-wrap").classList.add("show");
  var unis=selectedUnis,n=unis.length;
  
  var h='<thead><tr><th>'+t("cmp_dimension")+'</th>';
  for(var i=0;i<n;i++){
    var badge=unis[i].tier==="C9"?"c9":unis[i].tier==="985"?"a985":"a211";
    h+='<th>'+unis[i].name_en+' <span class="badge-tier '+badge+'" style="font-size:9px">'+unis[i].tier+'</span></th>';
  }
  h+='</tr></thead><tbody>';
  
  h+=rowSection(t("sec_basic"),n);
  h+=row(t("cmp_name"),unis.map(function(u){return u.name_en}),n);
  h+=row(t("cmp_name_zh"),unis.map(function(u){return u.name_zh}),n);
  h+=row(t("city_label"),unis.map(function(u){return u.city}),n);
  h+=row(t("qs_rank"),unis.map(function(u){return "#"+u.qs_rank}),n,true);
  h+=row(t("cmp_tier"),unis.map(function(u){return u.tier}),n);
  
  h+=rowSection(t("sec_costs"),n);
  h+=row(t("cmp_tuition_ug"),unis.map(function(u){return u.tuition_undergraduate||"-"}),n);
  h+=row(t("cmp_tuition_pg"),unis.map(function(u){return u.tuition_master||"-"}),n);
  
  h+=rowSection(t("sec_req"),n);
  h+=row(t("cmp_hsk"),unis.map(function(u){return u.hsk_required||"-"}),n);
  h+=row(t("cmp_ielts"),unis.map(function(u){return u.ielts_required||"-"}),n);
  
  h+=rowSection(t("sec_progs"),n);
  h+=rowPrograms(unis,n);
  
  if(unis.some(function(u){return u.medical_school})){
    h+=rowSection(t("sec_medical"),n);
    h+=rowMedical(unis,n);
  }
  
  h+=rowSection(t("sec_contact"),n);
  h+=row(t("cmp_email"),unis.map(function(u){return u.intl_office_email||"-"}),n);
  h+=rowWebsite(unis,n);
  
  h+='</tbody>';
  document.getElementById("cmp-table").innerHTML=h;
}

function rowSection(label,n){
  return '<tr class="row-section"><th colspan="'+(n+1)+'">'+label+'</th></tr>';
}

function row(label,values,n,lowerBetter){
  var h='<tr><th>'+label+'</th>';
  if(lowerBetter){
    var nums=values.map(function(v){var p=parseFloat(String(v).replace("#",""));return isNaN(p)?Infinity:p});
    var bestIdx=nums.indexOf(Math.min.apply(null,nums));
    for(var i=0;i<n;i++){
      var cls=(n>1&&i===bestIdx&&nums[i]<Infinity)?"cmp-highlight":"";
      h+='<td class="'+cls+'">'+values[i]+'</td>';
    }
  }else{
    for(var i=0;i<n;i++)h+='<td>'+values[i]+'</td>';
  }
  h+='</tr>';return h;
}

function rowPrograms(unis,n){
  var h='<tr><th>'+t("top_programs")+'</th>';
  for(var i=0;i<n;i++){
    var progs=unis[i].top_programs?unis[i].top_programs.slice(0,6):[];
    var tags=progs.map(function(p){return '<span class="prog-tag">'+p+'</span>'}).join("");
    h+='<td><div class="prog-tags-wrap">'+tags+'</div></td>';
  }
  h+='</tr>';return h;
}

function rowMedical(unis,n){
  var h='<tr><th>'+t("cmp_med_school")+'</th>';
  for(var i=0;i<n;i++){
    var u=unis[i];
    if(u.medical_school){
      var hl=u.medical_school.highlights?u.medical_school.highlights.slice(0,2).join(", "):"";
      h+='<td><div class="med-info"><span class="med-highlight">'+(u.medical_school.name_en||"")+'</span>'
        +'<div class="med-strength">'+(u.medical_school.strength||"")+'</div>'
        +(hl?('<div class="med-strength">'+hl+'</div>'):"")
        +'</div></td>';
    }else{h+='<td style="color:var(--text-l);font-size:11px">-</td>'}
  }
  h+='</tr>';return h;
}

function rowWebsite(unis,n){
  var h='<tr><th>'+t("cmp_website")+'</th>';
  for(var i=0;i<n;i++){
    var url=unis[i].website_intl||"#";
    h+='<td><a href="'+url+'" target="_blank" rel="noopener">'+url+'</a></td>';
  }
  h+='</tr>';return h;
}''')

# Init
js_lines.append('''(function(){
  var urlLang=(new URLSearchParams(location.search)).get("lang");
  var savedLang=localStorage.getItem("chinauni_lang");
  var bl=navigator.language.split("-")[0];
  var initLang=urlLang||savedLang||bl||"en";
  if(LANGS.indexOf(initLang)<0)initLang="en";
  if(urlLang)localStorage.setItem("chinauni_lang",initLang);
  switchLang(initLang);
  document.addEventListener("click",function(e){
    var dd=document.getElementById("search-dropdown");
    var input=document.querySelector(".search-input");
    if(dd&&!dd.contains(e.target)&&e.target!==input)dd.classList.remove("show");
  });
})();''')

js_lines.append('</script>')

# Combine
full_html = base_html + '\n'.join(js_lines) + '\n</body>\n</html>'

# Write
with open('compare.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'compare.html generated successfully')
print(f'Universities: {len(unis)}')
print(f'File size: {len(full_html):,} bytes ({len(full_html)/1024:.1f} KB)')
