from pathlib import Path
import json,re,html
site=Path(__file__).resolve().parents[1]
images=json.loads((site/'src/data/images.json').read_text())
for path in (site/'src/content').rglob('*.md'):
    text=path.read_text(encoding='utf-8')
    def replace(match):
        tag=match[0]
        src=re.search(r'src="([^"]+)"',tag)
        if not src or src[1] not in images:return tag
        info=images[src[1]]; variant=info['variants'][1]
        alt=re.search(r'alt="([^"]*)"',tag)
        unique={}
        for x in info['variants']: unique.setdefault(x['width'],x)
        sources=', '.join(f"{x['src']} {x['width']}w" for x in unique.values())
        return f'<img src="{variant["src"]}" srcset="{sources}" sizes="(max-width: 700px) 90vw, 700px" width="{variant["width"]}" height="{variant["height"]}" alt="{alt[1] if alt else ""}" loading="lazy" decoding="async">'
    path.write_text(re.sub(r'<img\b[^>]*>',replace,text),encoding='utf-8')
