"""Build the static academic homepage. Uses only the Python standard library."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
e = escape
ARROW = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M7 17 17 7M7 7h10v10"/></svg>'
PAPER = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M14 3H5v18h14V8zM14 3v5h5M8 12h8M8 16h6"/></svg>'


def link(url, label, icon=''):
    return f'<a href="{e(url, quote=True)}" target="_blank" rel="noopener noreferrer">{icon}{e(label)}</a>'


def bio_paragraph(paragraph):
    if isinstance(paragraph, str):
        return f'<p>{e(paragraph)}</p>'
    parts = [link(part['url'], part['text']) if part.get('url') else e(part['text']) for part in paragraph]
    return '<p>' + ''.join(parts) + '</p>'


def bibtex(p):
    authors = ' and '.join(f"{a.rsplit(' ', 1)[1]}, {a.rsplit(' ', 1)[0]}" for a in p['authors'])
    venue_key = 'booktitle' if p['type'] == 'inproceedings' else 'journal'
    fields = {'title': '{' + p['title'] + '}', 'author': authors, venue_key: p['venue_full'], 'year': str(p['year'])}
    if p.get('doi'):
        fields['doi'] = p['doi']
    if p.get('arxiv'):
        fields['eprint'] = p['arxiv']
        fields['archivePrefix'] = 'arXiv'
    fields['url'] = p['links'][0]['url']
    first = p['authors'][0].rsplit(' ', 1)[-1].lower()
    return '@' + p['type'] + '{' + f"{first}{p['year']}{p['id'].replace('-', '')},\n" + ',\n'.join(f'  {key} = {{{value}}}' for key, value in fields.items()) + '\n}'


def publication(p):
    poster = f"assets/site/media/{p['media']}.webp"
    alt = e(f"{p['title'].split(':')[0]} research preview")
    media = f'<img class="still" src="{poster}" alt="{alt}" loading="lazy" width="640" height="400">'
    if p['video']:
        media += f'<video data-src="assets/site/media/{p["media"]}.mp4" poster="{poster}" muted loop playsinline preload="none" aria-label="{alt}"></video>'
    authors = ', '.join(f'<strong>{e(a)}</strong>' if a == data['name'] else e(a) for a in p['authors'])
    links = ''.join(link(l['url'], l['label'], PAPER if l['label'] == 'Paper' else ARROW) for l in p['links'])
    return f'''<article class="publication" id="{p['id']}" aria-labelledby="title-{p['id']}">
      <figure class="preview">{media}<span class="media-label">{e(p['id'].upper())}</span></figure>
      <div class="paper-content">
        <span class="venue">{e(p['venue'])}</span>
        <h3 id="title-{p['id']}">{link(p['links'][0]['url'], p['title'])}</h3>
        <p class="authors">{authors}</p>
        <p class="paper-desc">{e(p['description'])}</p>
        <div class="paper-links">{links}</div>
      </div>
    </article>'''


def news(n):
    paper = f'<a href="#{e(n["paper_id"], quote=True)}">{e(n["paper"])}</a>'
    venue = '<strong>' + link(n['url'], n['venue']) + '</strong>'
    return f'<li class="news-item"><time datetime="{e(n["date"], quote=True)}">[{e(n["label"])}]</time><span>1 paper on {e(n["topic"])} ({paper}) is accepted to {venue}.</span></li>'


socials = data['socials'][:]
if data.get('scholar'):
    socials.insert(0, {'label': 'Google Scholar', 'url': data['scholar']})
if data.get('email'):
    socials.insert(0, {'label': 'Email', 'url': 'mailto:' + data['email']})
if data.get('cv'):
    socials.append({'label': 'CV', 'url': data['cv']})
social_html = ''.join(link(s['url'], s['label']) for s in socials)
bio = ''.join(bio_paragraph(p) for p in data['bio'])
pubs = '\n'.join(publication(p) for p in data['publications'])
news_items = ''.join(news(n) for n in data['news'])
description = f"{data['name']} — research in robot learning, embodied intelligence, autonomous exploration, and multi-agent systems."
if data.get('position'):
    description = f"{data['name']} — {data['position']}. Research in robot learning, embodied intelligence, and multi-agent systems."
schema = {'@context': 'https://schema.org', '@type': 'Person', 'name': data['name'], 'url': data['url'], 'image': data['url'] + '/assets/site/media/portrait.webp', 'sameAs': [s['url'] for s in data['socials']], 'knowsAbout': ['Robot learning', 'Reinforcement learning', 'Multi-agent systems', 'Legged locomotion']}
if data.get('scholar'):
    schema['sameAs'].append(data['scholar'])
if data.get('affiliations'):
    schema['affiliation'] = [{'@type': 'CollegeOrUniversity', 'name': name} for name in data['affiliations']]
html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(data['name'])} | Robot Learning &amp; Embodied Intelligence</title>
  <meta name="description" content="{e(description, quote=True)}">
  <meta name="author" content="{e(data['name'], quote=True)}">
  <meta name="theme-color" content="#205e91">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(data['name'], quote=True)} | Robot Learning &amp; Embodied Intelligence">
  <meta property="og:description" content="{e(description, quote=True)}">
  <meta property="og:url" content="{data['url']}/">
  <meta property="og:image" content="{data['url']}/assets/site/media/portrait.webp">
  <meta name="twitter:card" content="summary">
  <link rel="canonical" href="{data['url']}/">
  <link rel="icon" type="image/svg+xml" href="assets/site/favicon.svg">
  <link rel="preload" href="assets/site/media/portrait.webp" as="image">
  <script src="assets/site/theme.js"></script>
  <link rel="stylesheet" href="assets/site/style.css">
  <script type="application/ld+json">{json.dumps(schema).replace('<', chr(92) + 'u003c')}</script>
  <script src="assets/site/main.js" defer></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <nav class="wrap nav" aria-label="Main navigation">
      <div class="nav-links">
        <a href="#about">About</a><a class="nav-news" href="#news">News</a><a href="#publications">Publications</a>
        <button class="icon-button" id="theme-toggle" type="button" aria-label="Switch to dark theme">
          <svg class="moon" aria-hidden="true" viewBox="0 0 24 24"><path d="M20.5 13A8.7 8.7 0 0 1 11 3.5 8.8 8.8 0 1 0 20.5 13Z"/></svg>
          <svg class="sun" aria-hidden="true" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></svg>
        </button>
      </div>
    </nav>
  </header>
  <main id="main" class="wrap">
    <section class="hero" id="about" aria-labelledby="name">
      <div class="hero-copy">
        <div class="hero-heading">
          <p class="eyebrow">Learning to act in the physical world</p>
          <h1 id="name">{e(data['name'])}</h1>
          <p class="subtitle">{e(data['position'] or data['tagline'])}</p>
        </div>
        <div class="bio">{bio}</div>
      </div>
      <figure class="profile">
        <img class="portrait" src="assets/site/media/portrait.webp" alt="Portrait of {e(data['name'], quote=True)}" width="600" height="873" fetchpriority="high">
        <figcaption class="socials" aria-label="Academic profiles and contact">{social_html}</figcaption>
      </figure>
    </section>
    <div class="interests"><strong>Research interests</strong><div class="interest-items"><span>Reinforcement learning</span><span>Embodied intelligence</span><span>Multi-agent systems</span></div></div>
    <section class="section" id="news" aria-labelledby="news-heading">
      <div class="section-top"><h2 id="news-heading">News</h2></div>
      <ul class="news-list">{news_items}</ul>
    </section>
    <section class="section pub-section" id="publications" aria-labelledby="pub-heading">
      <div class="section-top"><div class="section-label"><h2 id="pub-heading">Selected publications</h2><span class="count">{len(data['publications'])} works</span></div>
        <button class="motion-toggle" id="motion-toggle" type="button" aria-pressed="true" hidden>Ⅱ Pause previews</button>
      </div>
      <div class="publications">{pubs}</div>
    </section>
    <footer class="footer">
      <span>© {data['updated'][:4]} {e(data['name'])} <span aria-hidden="true">·</span> Last updated {data['updated'][:7].replace('-', '.')}</span>
      <div class="footer-right"><a href="https://github.com/shuhaoliao/shuhaoliao.github.io" target="_blank" rel="noopener noreferrer">Website source ↗</a><a href="#about">Back to top ↑</a></div>
    </footer>
  </main>
</body>
</html>
'''
(ROOT / 'index.html').write_text(html, encoding='utf-8')
(ROOT / 'publications.bib').write_text('\n\n'.join(bibtex(p) for p in data['publications']) + '\n', encoding='utf-8')
for path, anchor in [('publications', 'publications'), ('about', 'about'), ('news', 'news')]:
    folder = ROOT / path
    folder.mkdir(exist_ok=True)
    folder.joinpath('index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url=../#{anchor}"><link rel="canonical" href="{data["url"]}/#{anchor}"><title>{e(path.title())} | {e(data["name"])}</title><p><a href="../#{anchor}">Continue to {e(path)}</a></p></html>', encoding='utf-8')
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {data["url"]}/sitemap.xml\n', encoding='utf-8')
(ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{data["url"]}/</loc><lastmod>{data["updated"]}</lastmod></url></urlset>\n', encoding='utf-8')
print(f'Built index.html, bibliography, redirects, and sitemap ({len(data["publications"])} publications).')
