"""Convert extracted CHM HTML topics (Innovasys/DX template) into compact Markdown bundles.
Usage: python3 -I chm2md.py <extracted_chm_dir> <out_dir> <hhc_file>
One output file per class/object (Lib~Class incl. members/methods/properties/events),
one file per enum library group, one file per conceptual topic.
"""
import sys, os, re, collections
from bs4 import BeautifulSoup, NavigableString, Tag

src, dst, hhc = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(dst, exist_ok=True)

def cell_text(td):
    return re.sub(r'\s+', ' ', td.get_text(' ', strip=True)).replace('|', '\\|')

def conv(node, out):
    for ch in node.children:
        if isinstance(ch, NavigableString):
            t = str(ch)
            if t.strip():
                out.append(re.sub(r'[ \t\r\n\xa0]+', ' ', t))
            continue
        if not isinstance(ch, Tag):
            continue
        cls = ' '.join(ch.get('class', []))
        if ch.name in ('script', 'style'):
            continue
        if 'i-section-heading' in cls.split():
            out.append('\n\n### ' + ch.get_text(' ', strip=True) + '\n')
            continue
        if 'i-popup-content' in cls or 'i-footer' in cls:
            continue
        if ch.name == 'table' and 'syntaxtable' in cls:
            # language tabs: a short row with the language name precedes the code row
            lang = ''
            for tr in ch.find_all('tr'):
                for td in tr.find_all(['td', 'th']):
                    raw_t = td.get_text().replace('\xa0', ' ').replace('\r', '')
                    st = raw_t.strip()
                    if not st:
                        continue
                    if td.find('pre') is None and '\n' not in st and len(st) < 30:
                        lang = st
                        continue
                    out.append(f'\n*{lang}:*\n```\n{st}\n```\n' if lang else f'\n```\n{st}\n```\n')
                    lang = ''
            continue
        if ch.name == 'table' and ch.find('pre') is not None:
            th = ch.find('th')
            title = th.get_text(' ', strip=True) if th else ''
            if title:
                out.append(f'\n*{title}:*')
            for pre in ch.find_all('pre'):
                code = pre.get_text().replace('\xa0', ' ').replace('\r', '')
                out.append(f'\n```\n{code.rstrip()}\n```\n')
            continue
        if ch.name == 'table':
            rows = []
            for tr in ch.find_all('tr'):
                if tr.find_parent('table') is not ch:
                    continue
                cells = [cell_text(td) for td in tr.find_all(['td', 'th'], recursive=False)]
                if any(cells):
                    rows.append('| ' + ' | '.join(cells) + ' |')
            if rows:
                out.append('\n' + rows[0] + '\n|' + '---|' * rows[0].count(' | ') + '---|\n' + '\n'.join(rows[1:]) + '\n')
            continue
        if ch.name == 'pre':
            code = ch.get_text().replace('\xa0', ' ').replace('\r', '')
            out.append(f'\n```\n{code.rstrip()}\n```\n')
            continue
        if ch.name in ('h1', 'h2', 'h3', 'h4'):
            out.append('\n\n#### ' + ch.get_text(' ', strip=True) + '\n')
            continue
        if ch.name == 'br':
            out.append('\n'); continue
        if ch.name in ('p', 'div', 'li', 'dt', 'dd', 'tr'):
            out.append('\n')
            if ch.name == 'li':
                out.append('- ')
            conv(ch, out)
            out.append('\n')
            continue
        conv(ch, out)

def topic(path):
    raw = open(path, 'rb').read()
    raw = re.sub(rb'<!--.*?-->', b'', raw, flags=re.S)
    s = BeautifulSoup(raw, 'html.parser')
    title = s.title.get_text(strip=True) if s.title else os.path.basename(path)
    proj = s.find(class_='i-project-title')
    crumbs = s.find(class_='i-breadcrumbs-container')
    body = s.find(class_='i-body-content') or s.body or s
    out = []
    conv(body, out)
    txt = ''.join(out)
    # drop See Also section (navigation only)
    txt = re.sub(r'\n### See Also\n.*', '', txt, flags=re.S)
    txt = re.sub(r'[ \t]+\n', '\n', txt)
    txt = re.sub(r'\n{3,}', '\n\n', txt).strip()
    head = f'## {title}\n\n*Quelle: `{os.path.basename(path)}`'
    if proj: head += ' · ' + proj.get_text(' ', strip=True)
    if crumbs:
        c = crumbs.get_text(' ', strip=True)
        if c: head += ' · ' + re.sub(r'\s+', ' ', c)
    head += '*\n\n'
    return head + txt + '\n'

# order according to TOC
t = open(hhc, 'rb').read().decode('cp1252', 'replace')
order = []
for m in re.finditer(r'<param name="Local" value="([^"]*)">', t, re.I):
    f = m.group(1).replace('%20', ' ').split('#')[0]
    if f not in order:
        order.append(f)
allhtml = sorted(f for f in os.listdir(src) if f.lower().endswith(('.html', '.htm')))
for f in allhtml:
    if f not in order:
        order.append(f)

groups = collections.OrderedDict()
for f in order:
    p = os.path.join(src, f)
    if not os.path.isfile(p):
        continue
    stem = f.rsplit('.', 1)[0]
    if '~' in stem:
        parts = stem.split('~')
        lib, cls = parts[0], parts[1]
        cls = re.sub(r'_(members|methods|properties|events|EV)$', '', cls)
        key = f'{lib}~{cls}'
    elif re.search(r'_(P|references)$', stem):
        key = re.sub(r'_(P|references)$', '', stem) + '~_Library'
    else:
        key = '_Konzept~' + stem
    groups.setdefault(key, []).append(p)

def safe(n):
    return re.sub(r'[^A-Za-z0-9_.~-]+', '_', n)

index = []
for key, files in groups.items():
    lib, cls = key.split('~', 1)
    txt = '\n\n---\n\n'.join(topic(p) for p in files)
    d = os.path.join(dst, safe(lib))
    os.makedirs(d, exist_ok=True)
    fn = safe(cls) + '.md'
    open(os.path.join(d, fn), 'w', encoding='utf-8').write(f'# {lib} – {cls}\n\n' + txt)
    index.append((lib, cls, f'{safe(lib)}/{fn}', len(files)))
with open(os.path.join(dst, 'INDEX.md'), 'w', encoding='utf-8') as fh:
    fh.write('| Bibliothek | Thema/Klasse | Datei | Anzahl CHM-Themen |\n|---|---|---|---|\n')
    for r in index:
        fh.write(f'| {r[0]} | {r[1]} | `{r[2]}` | {r[3]} |\n')
print(len(index), 'bundles')
