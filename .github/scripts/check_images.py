"""Verify every <img src> in the built site/ resolves to an existing file.

A missing file means the browser would render the alt text instead of the image.
Run this after `mkdocs build` so site/ exists.
"""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class ImgCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            d = dict(attrs)
            src = d.get("src", "")
            alt = d.get("alt", "")
            if src:
                self.images.append((src, alt))


site = Path("site")
broken = []
for html in sorted(site.rglob("*.html")):
    if html.name == "404.html":
        continue
    c = ImgCollector()
    c.feed(html.read_text(encoding="utf-8", errors="ignore"))
    for src, alt in c.images:
        p = urlparse(src)
        if p.scheme in ("http", "https", "data", "mailto"):
            continue
        if src.startswith("/"):  # root-relative: deployment-specific, skip
            continue
        resolved = (html.parent / src).resolve()
        if not resolved.exists():
            rel_html = html.relative_to(site)
            broken.append((str(rel_html), src, alt))

if broken:
    print(f"ERROR: {len(broken)} broken image(s) — browser would show alt text:")
    for page, src, alt in broken:
        print(f"  [{page}] {src!r}  alt={alt!r}")
    sys.exit(1)
print(f"All images OK ({len(list(site.rglob('*.html')))} pages checked)")
