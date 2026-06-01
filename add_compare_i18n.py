#!/usr/bin/env python3
"""Add compare-related I18N translations to index.html"""

import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'const I18N=(\{.+?\});', content)
if not m:
    print('I18N not found in index.html')
    exit(1)

i18n = json.loads(m.group(1))

# All compare-related keys
new_keys = {
    'compare': {'en':'Compare','zh':'对比','es':'Comparar','ar':'مقارنة','ru':'Сравнить'},
    'cmp_badge': {'en':'Side-by-Side Analysis','zh':'并排分析','es':'Análisis Comparativo','ar':'تحليل مقارن','ru':'Сравнительный анализ'},
    'cmp_title': {'en':'Compare Universities','zh':'大学对比','es':'Comparar Universidades','ar':'مقارنة الجامعات','ru':'Сравнение университетов'},
    'cmp_sub': {'en':'Select 2-4 universities to compare rankings, tuition fees, admission requirements, and program strengths side by side.',
                'zh':'选择2-4所大学，并排对比排名、学费、录取要求和专业优势。',
                'es':'Seleccione 2-4 universidades para comparar rankings, matrículas, requisitos de admisión y fortalezas de programas.',
                'ar':'اختر 2-4 جامعات لمقارنة التصنيفات والرسوم الدراسية ومتطلبات القبول ونقاط قوة البرامج.',
                'ru':'Выберите 2-4 университета для сравнения рейтингов, стоимости обучения, требований и сильных сторон программ.'},
    'cmp_dimension': {'en':'Dimension','zh':'对比维度','es':'Dimensión','ar':'البعد','ru':'Параметр'},
    'no_results': {'en':'No universities found','zh':'未找到匹配的大学','es':'No se encontraron universidades','ar':'لم يتم العثور على جامعات','ru':'Университеты не найдены'},
    'clear_all': {'en':'Clear All','zh':'清空','es':'Limpiar Todo','ar':'مسح الكل','ru':'Очистить всё'},
    'add_uni': {'en':'Add a university','zh':'添加大学','es':'Añadir universidad','ar':'أضف جامعة','ru':'Добавить университет'},
    'selected_label': {'en':'Selected for Comparison','zh':'已选对比大学','es':'Seleccionadas','ar':'مختارة للمقارنة','ru':'Выбрано для сравнения'},
    'cmp_hint': {'en':'Type to search, click to add. Compare up to 4 universities.',
                 'zh':'输入搜索，点击添加。最多对比4所大学。',
                 'es':'Escriba para buscar, haga clic para añadir. Máximo 4 universidades.',
                 'ar':'اكتب للبحث، انقر للإضافة. قارن حتى 4 جامعات.',
                 'ru':'Введите для поиска, нажмите чтобы добавить. До 4 университетов.'},
    'search_ph': {'en':'Search universities by name or city...','zh':'搜索大学名称或城市...',
                  'es':'Buscar universidades por nombre o ciudad...','ar':'ابحث عن الجامعات بالاسم أو المدينة...',
                  'ru':'Поиск университетов по названию или городу...'},
    'sec_basic': {'en':'Basic Information','zh':'基本信息','es':'Información Básica','ar':'معلومات أساسية','ru':'Основная информация'},
    'sec_costs': {'en':'Tuition & Costs','zh':'学费与费用','es':'Matrícula y Costos','ar':'الرسوم والتكاليف','ru':'Стоимость обучения'},
    'sec_req': {'en':'Admission Requirements','zh':'录取要求','es':'Requisitos de Admisión','ar':'متطلبات القبول','ru':'Требования к поступлению'},
    'sec_progs': {'en':'Program Strengths','zh':'专业优势','es':'Fortalezas de Programas','ar':'نقاط قوة البرامج','ru':'Сильные стороны программ'},
    'sec_medical': {'en':'Medical School','zh':'医学院','es':'Facultad de Medicina','ar':'كلية الطب','ru':'Медицинская школа'},
    'sec_contact': {'en':'Contact','zh':'联系方式','es':'Contacto','ar':'اتصال','ru':'Контакты'},
    'cmp_name': {'en':'University Name','zh':'大学名称','es':'Nombre','ar':'اسم الجامعة','ru':'Название'},
    'cmp_name_zh': {'en':'Chinese Name','zh':'中文名','es':'Nombre Chino','ar':'الاسم الصيني','ru':'Китайское название'},
    'cmp_tier': {'en':'Tier','zh':'层次','es':'Nivel','ar':'المستوى','ru':'Уровень'},
    'cmp_tuition_ug': {'en':'Tuition (Undergraduate)','zh':'本科学费','es':'Matrícula (Grado)','ar':'الرسوم (بكالوريوس)','ru':'Обучение (Бакалавр)'},
    'cmp_tuition_pg': {'en':'Tuition (Postgraduate)','zh':'研究生学费','es':'Matrícula (Posgrado)','ar':'الرسوم (دراسات عليا)','ru':'Обучение (Магистр)'},
    'cmp_hsk': {'en':'HSK Required','zh':'HSK要求','es':'HSK Requerido','ar':'HSK مطلوب','ru':'Требуемый HSK'},
    'cmp_ielts': {'en':'IELTS Required','zh':'IELTS要求','es':'IELTS Requerido','ar':'IELTS مطلوب','ru':'Требуемый IELTS'},
    'cmp_email': {'en':'Admissions Email','zh':'招生邮箱','es':'Email de Admisiones','ar':'بريد القبول','ru':'Email приёмной комиссии'},
    'cmp_website': {'en':'Website','zh':'官网','es':'Sitio Web','ar':'الموقع','ru':'Сайт'},
    'cmp_med_school': {'en':'Medical School','zh':'医学院','es':'Facultad de Medicina','ar':'كلية الطب','ru':'Медицинская школа'},
    'top_programs': {'en':'Top Programs','zh':'优势专业','es':'Programas Destacados','ar':'أفضل البرامج','ru':'Лучшие программы'},
    'back_home': {'en':'Home','zh':'首页','es':'Inicio','ar':'الرئيسية','ru':'Главная'},
}

for lang in ['zh','en','es','ar','ru']:
    for key, trans in new_keys.items():
        if key not in i18n[lang]:
            i18n[lang][key] = trans[lang]

new_i18n = json.dumps(i18n, ensure_ascii=False, separators=(',', ':'))
content = re.sub(r'const I18N=\{.+?\};', 'const I18N=' + new_i18n + ';', content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('I18N updated with 28 new keys per language')
for lang in i18n:
    print(f'  {lang}: {len(i18n[lang])} keys')
