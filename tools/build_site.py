from pathlib import Path
import json, re, html, shutil
from datetime import datetime, date

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
CONTENT = ROOT / "content" / "articles"

MONTHS = ["", "januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]
SHORT_MONTHS = ["", "jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]


def esc(value):
    return html.escape(str(value or ""), quote=True)


def asset_path(value):
    value = str(value or "").strip()
    if value.startswith("/"):
        value = value[1:]
    return value


def normalize_body_assets(value):
    value = str(value or "")
    value = value.replace('src="/assets/', 'src="assets/')
    value = value.replace("src='/assets/", "src='assets/")
    value = value.replace('href="/assets/', 'href="assets/')
    value = value.replace("href='/assets/", "href='assets/")
    return value


def parse_date(value):
    if isinstance(value, datetime): return value
    if isinstance(value, date): return datetime(value.year, value.month, value.day)
    text = str(value or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"):
        try: return datetime.strptime(text, fmt)
        except ValueError: pass
    return datetime.min


def full_date(dt):
    return f"{dt.day} {MONTHS[dt.month]} {dt.year}" if dt != datetime.min else ""


def short_date(dt):
    return f"{dt.day} {SHORT_MONTHS[dt.month]}" if dt != datetime.min else ""


def month_year(dt):
    return f"{MONTHS[dt.month]} {dt.year}" if dt != datetime.min else ""


def clean_text(value):
    text = re.sub(r"<[^>]+>", " ", str(value or ""))
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def reading_minutes(body):
    words = re.findall(r"\b[\wÅÄÖåäöÉéÜü-]+\b", clean_text(body))
    return max(1, round(len(words) / 220))


def article_slug(path):
    stem = path.stem
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
    stem = re.sub(r"[^a-zA-Z0-9åäöÅÄÖ_-]+", "-", stem).strip("-").lower()
    trans = str.maketrans({"å":"a","ä":"a","ö":"o","Å":"a","Ä":"a","Ö":"o"})
    return stem.translate(trans)


def load_articles():
    result = []
    for path in sorted(CONTENT.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"VARNING: kunde inte läsa {path.name}: {exc}")
            continue
        if data.get("published") is not True:
            continue
        required = ["title", "publish_date", "type", "topic", "author", "excerpt", "hero_image", "hero_alt", "body"]
        missing = [key for key in required if not data.get(key)]
        if missing:
            print(f"VARNING: {path.name} hoppas över, saknar: {', '.join(missing)}")
            continue
        data["_date"] = parse_date(data.get("publish_date"))
        data["_slug"] = article_slug(path)
        data["_url"] = f"artikel-{data['_slug']}.html"
        data["_minutes"] = reading_minutes(data.get("body"))
        data["tags"] = data.get("tags") or []
        result.append(data)
    result.sort(key=lambda a: (a["_date"], a.get("title", "")), reverse=True)
    return result


def head(title, description="Marknadssamfundet – För fri marknad och ett fritt samhälle."):
    title_text = "Marknadssamfundet" if not title else f"{esc(title)} – Marknadssamfundet"
    return f'''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(description)}"><title>{title_text}</title><link rel="icon" type="image/png" href="assets/favicon.png"><link rel="stylesheet" href="styles.css"></head><body>'''


def header(active="", latest=None):
    def nav(label, href, key):
        cls = ' class="active"' if active == key else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    top = f'''<header class="masthead"><div class="wrap identity"><a href="index.html" aria-label="Marknadssamfundet, startsida"><img src="assets/mark-icon.png" alt=""></a><div class="identity-copy"><div class="identity-name">Marknadssamfundet</div><div class="identity-tagline">För fri marknad och ett fritt samhälle</div></div></div><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">Meny</button><nav id="main-nav" class="main-nav wrap" aria-label="Huvudmeny">{nav('Hem','index.html','home')}{nav('Rapporter & artiklar','arkiv.html','archive')}{nav('Om oss','om.html','about')}{nav('Butik','butik.html','shop')}</nav></header>'''
    if latest:
        top += f'<div class="newsline"><div class="wrap"><strong>Senaste</strong><a href="{esc(latest["_url"])}">{esc(latest["title"])}</a></div></div>'
    return top


def footer():
    return '''<footer class="footer"><div class="wrap"><div class="footer-grid"><div><div class="footer-brand"><img src="assets/mark-icon.png" alt=""><strong>MARKNADSSAMFUNDET</strong></div><p>För fri marknad och ett fritt samhälle.</p></div><div><strong>Innehåll</strong><p><a href="arkiv.html">Rapporter & artiklar</a></p><p><a href="om.html">Om oss</a></p><p><a href="butik.html">Butik</a></p></div><div><strong>Kontakt</strong><p>Kontaktuppgifter publiceras här.</p></div></div><div class="legal"><small>© 2026 Marknadssamfundet.</small></div></div></footer><script src="script.js"></script></body></html>'''


def image_tag(a, cls="", use_cover=False):
    image = a.get("cover_image") if use_cover and a.get("cover_image") else a.get("hero_image")
    alt = a.get("cover_alt") if use_cover and a.get("cover_image") else a.get("hero_alt")
    return f'<img src="{esc(asset_path(image))}" alt="{esc(alt)}"{(" class="+esc(cls)+"\"") if cls else ""}>'


def empty_state():
    return '''<main class="page"><section class="wrap empty-state"><span class="kicker">Marknadssamfundet</span><h1>Inga publiceringar ännu</h1><p class="lead">Marknadssamfundets rapporter, analyser, opinionstexter och reportage kommer att publiceras här.</p></section></main>'''


def build_index(articles):
    latest = articles[0] if articles else None
    parts = [head(""), header("home", latest)]
    if not articles:
        parts += [empty_state(), footer()]
        return "".join(parts)

    lead = articles[0]
    side = articles[1:3]
    single_cls = " single-lead" if not side else ""
    parts.append(f'<main class="page"><section class="wrap front-grid{single_cls}">')
    parts.append(f'''<article class="lead-story"><a class="story-image story-image-hero" href="{esc(lead['_url'])}">{image_tag(lead)}</a><span class="kicker">{esc(lead['type'])}</span><h1>{esc(lead['title'])}</h1><p class="dek">{esc(lead['excerpt'])}</p><div class="meta">{full_date(lead['_date'])} · {esc(lead['author'])} · {lead['_minutes']} min</div><a class="story-link" href="{esc(lead['_url'])}">Läs mer →</a></article>''')
    if side:
        parts.append('<div class="side-stack">')
        for a in side:
            parts.append(f'''<article class="side-story"><a class="story-image" href="{esc(a['_url'])}">{image_tag(a)}</a><span class="kicker">{esc(a['type'])}</span><h2><a href="{esc(a['_url'])}">{esc(a['title'])}</a></h2><p>{esc(a['excerpt'])}</p><div class="meta">{full_date(a['_date'])} · {a['_minutes']} min</div></article>''')
        parts.append('</div>')
    parts.append('</section>')

    parts.append('<section class="wrap section"><div class="section-head"><h2>Senaste</h2><a href="arkiv.html">Hela arkivet →</a></div><div class="latest-grid"><div class="latest-list">')
    for a in articles[:4]:
        parts.append(f'''<article class="latest-item"><a class="latest-thumb" href="{esc(a['_url'])}">{image_tag(a)}</a><div><span class="tag">{esc(a['type'])}</span><h3><a href="{esc(a['_url'])}">{esc(a['title'])}</a></h3><p>{esc(a['excerpt'])}</p></div><div class="meta">{short_date(a['_date'])}</div></article>''')
    parts.append('''</div><aside class="editorial-box"><span class="section-kicker">Vår idé</span><h3>För fri marknad och ett fritt samhälle</h3><p>Marknadssamfundet är en marknadsliberal idéorganisation för analys, opinionsbildning och samhällsdebatt.</p><a class="story-link" href="om.html">Om Marknadssamfundet →</a></aside></div></section>''')

    reports = [a for a in articles if a.get("type") == "Rapport"][:3]
    if reports:
        parts.append('<section class="wrap section"><div class="section-head"><h2>Rapporter</h2><a href="arkiv.html?typ=rapport">Fler rapporter →</a></div><div class="report-grid">')
        for i,a in enumerate(reports,1):
            parts.append(f'''<article class="report-card"><a class="report-cover" href="{esc(a['_url'])}">{image_tag(a, use_cover=True)}</a><div class="number">{i:02d}</div><span class="tag">{esc(a['topic'])}</span><h3><a href="{esc(a['_url'])}">{esc(a['title'])}</a></h3><p>{esc(a['excerpt'])}</p><div class="meta">Rapport · {month_year(a['_date'])}</div></article>''')
        parts.append('</div></section>')

    editorial = [a for a in articles if a.get("type") in ("Analys","Opinion","Kommentar")][:3]
    if editorial:
        parts.append('<section class="wrap section"><div class="section-head"><h2>Analys & opinion</h2><a href="arkiv.html">Visa alla →</a></div><div class="opinion-grid">')
        for a in editorial:
            parts.append(f'''<article class="opinion-card"><a class="opinion-image" href="{esc(a['_url'])}">{image_tag(a)}</a><span class="tag">{esc(a['type'])}</span><h3><a href="{esc(a['_url'])}">{esc(a['title'])}</a></h3><p>{esc(a['excerpt'])}</p></article>''')
        parts.append('</div></section>')
    parts.append('</main>')

    topics = sorted({str(a.get("topic","")).strip() for a in articles if a.get("topic")})
    if topics:
        parts.append('<section class="topics"><div class="wrap"><span class="section-kicker">Ämnen</span><div class="topic-links">')
        for topic in topics:
            parts.append(f'<a href="arkiv.html?q={esc(topic)}">{esc(topic)}</a>')
        parts.append('</div></div></section>')
    parts.append(footer())
    return "".join(parts)


def build_archive(articles):
    latest = articles[0] if articles else None
    parts=[head("Rapporter & artiklar"), header("archive", latest), '<main class="page"><div class="wrap"><header class="archive-header"><span class="kicker">Arkiv</span><h1>Rapporter & artiklar</h1><p class="lead">Sök bland Marknadssamfundets rapporter, analyser, opinionstexter och reportage.</p></header>']
    if not articles:
        parts.append('<section class="archive-empty"><h2>Inga publiceringar ännu</h2><p>Arkivet fylls automatiskt när den första publiceringen går live.</p></section></div></main>')
        parts.append(footer())
        return "".join(parts)
    types=[]
    for a in articles:
        t=a.get('type')
        if t and t not in types: types.append(t)
    parts.append('<section class="search-box"><label for="search">Sök i arkivet</label><input id="search" type="search" placeholder="Sök t.ex. skatter, bostäder, EU eller företagande…" autocomplete="off"><div class="filters"><button class="filter active" data-filter="alla">Alla</button>')
    for t in types:
        parts.append(f'<button class="filter" data-filter="{esc(t.lower())}">{esc(t)}</button>')
    parts.append('</div></section><section class="archive-list">')
    for a in articles:
        search_text=' '.join([a.get('title',''),a.get('topic',''),a.get('author',''),a.get('excerpt',''),' '.join(a.get('tags') or [])])
        parts.append(f'''<article class="archive-item" data-type="{esc(a['type'].lower())}" data-search="{esc(search_text)}"><a class="archive-thumb" href="{esc(a['_url'])}">{image_tag(a)}</a><div><span class="tag">{esc(a['type'])}</span><h2><a href="{esc(a['_url'])}">{esc(a['title'])}</a></h2><p>{esc(a['excerpt'])}</p></div><div class="meta">{full_date(a['_date'])}</div></article>''')
    parts.append('</section><p id="no-results" class="no-results" hidden>Inga träffar. Prova ett annat sökord eller filter.</p></div></main>')
    parts.append(footer())
    return "".join(parts)


def build_article(a, articles):
    body = normalize_body_assets(a.get('body',''))
    # Give the first normal paragraph the v4 drop-cap treatment.
    body = re.sub(r'<p(\s[^>]*)?>', lambda m: '<p class="dropcap"'+(m.group(1) or '')+'>', body, count=1, flags=re.I)
    related = [x for x in articles if x['_url'] != a['_url'] and (x.get('topic') == a.get('topic') or x.get('type') == a.get('type'))][:2]
    if len(related) < 2:
        for x in articles:
            if x['_url'] != a['_url'] and x not in related:
                related.append(x)
                if len(related) == 2: break
    tags='<br>'.join(esc(t) for t in (a.get('tags') or []))
    pdf=''
    if a.get('pdf'):
        pdf=f'<p><a class="story-link" href="{esc(asset_path(a["pdf"]))}">Ladda ned PDF →</a></p>'
    rel_html=''
    for r in related:
        rel_html += f'<h3><a href="{esc(r["_url"])}">{esc(r["title"])}</a></h3><p>{esc(r["type"])} · {full_date(r["_date"])}</p>'
    return ''.join([
        head(a['title'], a.get('excerpt','')),
        header('archive', articles[0] if articles else None),
        f'''<main><header class="article-header wrap"><span class="kicker">{esc(a['type'])}</span><h1>{esc(a['title'])}</h1><p class="lead">{esc(a['excerpt'])}</p><div class="byline">{esc(a['author'])} · {full_date(a['_date'])} · {a['_minutes']} min läsning</div></header><figure class="article-hero wrap">{image_tag(a)} </figure><div class="wrap article-layout"><aside class="article-aside"><strong>Ämne</strong>{esc(a['topic'])}''',
        (f'<br><br><strong>Taggar</strong>{tags}' if tags else ''),
        pdf,
        f'''</aside><article class="article-body">{body}</article><aside class="related"><span class="tag">Relaterat</span>{rel_html}</aside></div></main>''',
        footer()
    ])


def build_redirect():
    return '''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=arkiv.html"><title>Marknadssamfundet</title></head><body><p><a href="arkiv.html">Fortsätt till Rapporter & artiklar</a></p></body></html>'''


def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    # Copy static branding, CSS, JS and fixed pages.
    shutil.copytree(ROOT/'assets', OUT/'assets')
    for name in ('styles.css','script.js','om.html','butik.html'):
        shutil.copy2(ROOT/name, OUT/name)
    articles=load_articles()
    (OUT/'index.html').write_text(build_index(articles), encoding='utf-8')
    (OUT/'arkiv.html').write_text(build_archive(articles), encoding='utf-8')
    (OUT/'artikel.html').write_text(build_redirect(), encoding='utf-8')
    for a in articles:
        (OUT/a['_url']).write_text(build_article(a, articles), encoding='utf-8')
    print(f"Byggde {len(articles)} publicerade texter till {OUT}")

if __name__ == '__main__':
    main()
