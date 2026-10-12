from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
site=Path(__file__).resolve().parents[1]
urls=set()
for p in (site/'dist').rglob('*.html'):
    soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    for link in soup.find_all('a',href=True):
        if link['href'].startswith('https://') and 'pratikshya-regmi.github.io' not in link['href']:urls.add(link['href'])
legacy=['','aboutme','conferences','symposiums','workshops','Publications','hackathon','volunteer','geogiggles','resume','blogs','projects']
urls.update('https://pratikshya-regmi.github.io/'+p for p in legacy)
def check(url):
    try:
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 portfolio-link-audit'}),timeout=20) as r:
            data=r.read(150000) if 'text/html' in r.headers.get('Content-Type','') else b''
            soup=BeautifulSoup(data,'html.parser')
            return dict(url=url,status=r.status,final=r.url,title=soup.title.get_text(' ',strip=True) if soup.title else '',headings=[h.get_text(' ',strip=True) for h in soup.find_all(['h1','h2','h3'])][:16])
    except HTTPError as e:return dict(url=url,status=e.code,note='May require login or block automated requests' if e.code in [401,403,429,999] else 'Review destination')
    except Exception as e:return dict(url=url,status='unverified',note=type(e).__name__)
with ThreadPoolExecutor(max_workers=6) as pool: result=list(pool.map(check,sorted(urls)))
target=site/'test-results';target.mkdir(exist_ok=True)
(target/'external-links.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
for item in result:print(json.dumps(item,ensure_ascii=True))
