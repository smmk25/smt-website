#!/usr/bin/env python3
"""Builds preview-full.html: the whole site in ONE self-contained file.
Splash and mobile menu are already part of index-scroll.html; this only
inlines assets so the file renders without its folder."""
import base64, os, re
BASE = os.path.dirname(os.path.abspath(__file__))
def b64(p):
    return base64.b64encode(open(os.path.join(BASE, p), 'rb').read()).decode()

html = open(os.path.join(BASE, 'index-scroll.html'), encoding='utf-8').read()

for sub in ('services', 'about', 'clients'):
    d = os.path.join(BASE, 'assets', sub)
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        rel = 'assets/%s/%s' % (sub, f)
        ext = f.rsplit('.', 1)[-1].lower()
        mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else 'image/' + ext
        if rel in html:
            html = html.replace(rel, 'data:%s;base64,%s' % (mime, b64(rel)))

fav = 'assets/favicon/favicon.svg'
if fav in html and os.path.exists(os.path.join(BASE, fav)):
    html = html.replace(fav, 'data:image/svg+xml;base64,' + b64(fav))
for pat in (r'\s*<link rel="icon" href="assets/favicon/favicon\.ico"[^>]*>',
            r'\s*<link rel="icon" type="image/png"[^>]*>',
            r'\s*<link rel="apple-touch-icon"[^>]*>',
            r'\s*<link rel="manifest"[^>]*>'):
    html = re.sub(pat, '', html)

for rel in ('assets/logo.svg', 'assets/logo-white.svg'):
    if rel in html:
        html = html.replace(rel, 'data:image/svg+xml;base64,' + b64(rel))

for stem in ('Montserrat-VariableFont_wght', 'Montserrat-Italic-VariableFont_wght'):
    woff2_rel = 'fonts/%s.woff2' % stem
    ttf_rel = 'fonts/%s.ttf' % stem
    data = b64(woff2_rel)
    # inline the woff2 and close the src list here...
    html = html.replace(
        "url('%s') format('woff2-variations')," % woff2_rel,
        "url(data:font/woff2;base64,%s) format('woff2-variations');" % data)
    # ...then drop the now-redundant ttf fallback line rather than leaving a dangling comma
    html = html.replace(
        "\n         url('%s') format('truetype-variations');" % ttf_rel, '')

open(os.path.join(BASE, 'preview-full.html'), 'w', encoding='utf-8').write(html)
print('written preview-full.html (%d KB)' % (len(html) // 1024))
print('unresolved:', re.findall(r'src="(assets/[^"]+)"', html) or 'none')
