"""One-time, reviewable import from the preserved Jekyll sources."""
from pathlib import Path
import re, json, html, yaml
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'astro-site'
CONTENT = SITE / 'src/content'

def read(name):
    return (ROOT / name).read_text(encoding='utf-8')

def strip_front(text):
    return re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.S)

def put(collection, slug, title, body='', **fields):
    data = dict(title=title, summary=fields.pop('summary', title), source=fields.pop('source', 'Existing CV and website'), order=fields.pop('order', 0), **fields)
    path = CONTENT / collection / (slug + '.md')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\n' + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + '---\n\n' + body.strip() + '\n', encoding='utf-8')

def clean_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    for tag in soup.find_all(True):
        tag.attrs.pop('style', None)
        tag.attrs.pop('target', None)
    for im in soup.find_all('img'):
        im.decompose()
    return str(soup)

for filename, kind, collection in [('conferences.md','Conference','presentations'),('symposiums.md','Symposium','presentations'),('workshops.md','Workshop','workshops')]:
    soup = BeautifulSoup(strip_front(read(filename)), 'html.parser')
    for i, heading in enumerate(soup.find_all('h3')):
        card = heading.parent
        title = heading.get_text(' ', strip=True)
        image = card.find('img')
        paragraphs = card.find_all('p')
        summary = paragraphs[-1].get_text(' ', strip=True) if paragraphs else title
        meta = paragraphs[0].get_text(' ', strip=True) if paragraphs else ''
        year = re.search(r'20\d\d', title + ' ' + meta)
        fields = dict(kind=kind, order=i + (10 if kind=='Symposium' else 0), date=year[0] if year else '', source=filename, summary=summary, pending=['Poster / slides — upload pending'] if collection=='presentations' else [])
        if image: fields.update(image=image['src'], alt=title + ' — event photograph')
        heading.decompose()
        put(collection, f'{kind.lower()}-{i+1}',title,clean_html(str(card)), **fields)

pub = strip_front(read('Publications.md'))
for i, block in enumerate(re.split(r'\n(?=- )', pub.strip())):
    title = re.search(r'\*([^*]+)\*',block)
    titles = re.findall(r'(?<!\*)\*([^*]+)\*(?!\*)',block)
    title = titles[0] if titles else f'Publication {i+1}'
    put('publications',f'publication-{i+1}',title,block.removeprefix('- '),order=i,source='Publications.md',summary='Publication, thesis, or conference contribution', kind='Research output')

for file,title in [('volunteer.md','Outreach & STEM engagement'),('hackathon.md','Hackathons'),('geogiggles.md','GeoGiggles')]:
    body=strip_front(read(file))
    body=body.replace('[Hacking climate and soil data for North Carolina’s crops](<ARTICLE_URL>)','**Hackathon article — link to be added.**')
    body=re.sub(r' style="[^"]*"','',body)
    body=body.replace('alt="PSI Hackathon 2024 Team Photo"','alt="PSI Hackathon team photograph"')
    if file=='geogiggles.md': body=body.replace('## 💡 Got a Geo-Joke?','</div>\n\n## Got a Geo-Joke?')
    put('engagement',file[:-3],title,body,source=file,summary={'volunteer.md':'Science thrives when it is inclusive, hands-on, and inspiring.','hackathon.md':'Applying geospatial and AI methods in interdisciplinary teams.','geogiggles.md':'Coordinates meet comedy. A lighter side of geospatial science.'}[file])

about=strip_front(read('aboutme.md')).replace('I’m a Ph.D. student at','I’m a fourth-year Ph.D. candidate (started fall 2023) at').replace("master's in Geospatial Engineering", "master's in Geospatial Systems Engineering")
put('pages','about','About',about,source='aboutme.md; user confirmation 2026-09-16',summary='Fieldwork, open science, and a curiosity about changing landscapes.')

for i, item in enumerate(yaml.safe_load(read('_data/linkedin_post.yml'))):
    fields=dict(order=i,source='_data/linkedin_post.yml',summary=item['snippet'],date='2025')
    if (ROOT / item['image'].lstrip('/')).exists(): fields.update(image=item['image'],alt=item['title']+' — photograph')
    else: fields['pending']=['Photograph — upload pending']
    if 'your-post-link' not in item['link']: fields['links']=[dict(label='Read the original update',url=item['link'])]
    else: fields['pending']=['Original update — link to be added']
    put('highlights',f'highlight-{i+1}',item['title'],**fields)

education=[
('ncsu','Ph.D. in Geospatial Analytics','Fall 2023 – present','North Carolina State University · Raleigh, North Carolina','Fourth-year Ph.D. candidate, Center for Geospatial Analytics. Research on reproducible fusion of LiDAR, UAS, and satellite imagery for monitoring post-disaster geomorphic change. Advisor: Dr. Helena Mitasova.'),
('tamucc','M.S. in Geospatial Systems Engineering','2023','Texas A&M University-Corpus Christi','Thesis: Application of UAS Photogrammetry and Geospatial AI Techniques for Palm Tree Detection and Mapping. Advisor: Dr. Michael J. Starek.'),
('kathmandu','B.E. in Geomatics Engineering','2018','Kathmandu University · Dhulikhel, Nepal','Thesis: Analyzing the Effect of Image Overlap, Number of GCPs & its Distribution Pattern on Overall Accuracy of UAV Photogrammetry. Advisor: Dr. Uma Shankar Panday.')]
for i,(slug,title,date,location,body) in enumerate(education): put('education',slug,title,body,order=i,date=date,location=location,summary=location,source='CV; NCSU status confirmed by user 2026-09-16')

roles=[
('ncsu','Graduate Research and Teaching Assistant','2023 – present','North Carolina State University','Built spatiotemporal Earth observation workflows for post-disaster mapping using multi-temporal LiDAR, SfM point clouds, and imagery. Quantified terrain change and modeled drainage and flow paths using GRASS GIS and Python. Developing reusable research code and an LLM-assisted geospatial workflow.'),
('itre','Summer Research Assistant','June – August 2024','Institute for Transportation Research and Education, NCSU','Worked on parachute integration and deployment in Mavic drones for operations-over-people waivers, and visibility analysis for safe UAS operation.'),
('tamucc','Graduate Research Assistant','2021 – 2023','MANTIS Lab, Conrad Blucher Institute, TAMUCC','Conducted UAS flights, processed imagery, developed 2D/3D web maps and dashboards in ArcGIS Online, and maintained the historical UAS imagery site.'),
('nea','Geomatics Engineer','January – July 2021','NEA Engineering Company Limited · Kathmandu, Nepal','Performed GIS mapping and satellite-based analysis for transmission-line routing, considering cost, distance, and community benefit.')]
for i,(slug,title,date,location,body) in enumerate(roles): put('experience',slug,title,body,order=i,date=date,location=location,summary=location)

awards=[('2025','N.C. PSI Hackathon — 1st Place, Advanced Track','N.C. Plant Sciences Initiative'),('2025','Women in GIS Award','Women in GIS'),('2023','University Graduate Fellowship','North Carolina State University'),('2023, 2022, 2021','C.J. Davidson Scholarship','Texas A&M University-Corpus Christi'),('2022','Conrad Blucher Institute Scholarship','Conrad Blucher Institute'),('2022, 2021','Geospatial Surveying Engineering Scholarship','Texas A&M University-Corpus Christi'),('2022','ASPRS Student Conference Presentation Grant','American Society for Photogrammetry and Remote Sensing'),('2019','Best Paper Presented','UASG, IIT Roorkee, India')]
for i,(date,title,org) in enumerate(awards): put('honors',f'award-{i+1}',title,order=i,date=date,summary=org)

certs=[('2025','AUVSI Trusted Operator','AUVSI'),('2024','FAA Part 107 Certified sUAS Remote Pilot','FAA'),('2022','Spatial Data Science: The New Frontier in Analytics','Esri'),('2022','ArcGIS Notebooks Basics','Esri'),('2022','Data Science Workflows Using ArcGIS Notebooks','Esri'),('2022','Introduction to ArcGIS API for Python','Esri'),('2022','Introduction to Regression Analysis Using ArcGIS Pro','Esri'),('2021','Mapping Clusters: Hot Spot & Outlier Analysis','Esri'),('2021','Crime Analysis: Tactical and Strategic','Esri'),('2021','Optimal Facility Location Using ArcGIS Pro','Esri'),('2021','Introduction to the Crime Analysis Solution','Esri'),('2021','Space-Time Analysis: Time-Series Clustering','Esri'),('2021','Capstone: Retrieving, Processing & Visualizing Data with Python','University of Michigan'),('2020','Machine Learning','Stanford University'),('2020','Neural Networks and Deep Learning','DeepLearning.AI'),('2020','Python Data Structures','University of Michigan'),('2020','Python for Everybody: Getting Started','University of Michigan')]
for i,(date,title,org) in enumerate(certs): put('certifications',f'certificate-{i+1}',title,order=i,date=date,summary=org)

put('engagement','service','Professional service','''- AGU H3S Subcommittee — member (2025–2026)
- Nepali Student Association, NCSU — President (2026–present)
- Nepali Student Association, NCSU — Vice President (2025–2026)
- Geospatial Graduate Student Organization — External Affairs Officer (2024–2025)
- American Geophysical Union — member (2024–present)
- ASPRS — member (2023–2024)

## Open-source contribution

Contributed security technique documentation and references to [SAFE-MCP](https://github.com/SAFE-MCP/safe-mcp), collaborating through GitHub pull requests.''',summary='Leadership, professional community, and open-source contribution.')
put('presentations','webinar','Simulating Wildfire Ash Transport Following a Precipitation Event by Coupling Dorado and Overland Flow',date='2024',kind='Webinar',location='Virtual · CSDMS Fall Webinar Series',order=20,summary='A presentation connecting particle transport and overland flow modeling.',pending=['Recording / slides — upload pending'])

projects=[
('helene','Reading a landscape after Hurricane Helene','Multi-sensor terrain analysis in Chimney Rock, western North Carolina.','/assets/img/AGU.jpeg',['LiDAR','Landscape change','GRASS GIS'],True,'''## Research question
How did Hurricane Helene alter terrain, drainage, and infrastructure in western North Carolina?
## Data & methods
The existing AGU 2025 presentation describes multi-temporal LiDAR (2017 and November 2024) and immediate post-storm SfM point clouds (October 2024). The analysis mapped elevation change, debris accumulation, drainage modification, and infrastructure disruption.
## My contribution
Presented the study at AGU 2025. Related research workflows use DEMs of Difference, GRASS GIS terrain/hydrology tools, and Python for reproducible analysis.
## Research context
The work supports hazard interpretation and recovery planning. Quantitative result figures will be added with the supplied materials.
## Related work
[AGU 2025 presentation](/conferences/) · [Graduate Research Symposium](/symposiums/)
'''),
('uas-visibility','Seeing terrain. Planning safer flights.','LiDAR-based visibility analysis for safe UAS operation.','/assets/img/agu1.jpg',['LiDAR','UAS','GIS'],True,'''## Research question
How can terrain visibility analysis inform safe and efficient UAS flight planning in complex landscapes?
## Data & methods
LiDAR-based terrain modeling and visibility analysis, presented at AGU 2024 and the CNR Symposium in 2025.
## My contribution
Developed and presented visibility-analysis research; related summer research at NCSU's Institute for Transportation Research and Education addressed safe drone operations.
## Research output
[Visibility Analysis for Safe UAS Operation Using Lidar Datasets](https://ui.adsabs.harvard.edu/abs/2024AGUFMB21F.1358R/abstract).
Study-area details, result figures, and the survey visualization will be added with the source materials.
'''),
('geospatial-ai','A conversation with geospatial data','Connecting natural-language questions to open-source GIS workflows.','/assets/img/iale.jpeg',['AI','GRASS GIS','Python'],False,'''## Research question
How can large language models help people ask geospatial questions and obtain maps and explanations?
## Methods & contribution
Prototyping LLM-assisted workflows connected to GRASS GIS through structured tool/function calling and documentation retrieval. Presented a digital visualization showcase at IALE North America 2025.
## Research output
“Accessing the Potential of Large Language Models (LLMs) for Geospatial Analysis.” Evaluation results, a demonstration, and graphical abstract will be added when available.
[Presentation details](/conferences/)
'''),
('palm-mapping','Mapping palms from the air','UAS photogrammetry and geospatial AI for palm-tree detection.','/assets/img/tamuccsympo.jpg',['Remote sensing','UAS','AI'],False,'''## Research question
How can UAS imagery and geospatial AI support palm-tree detection and mapping?
## Data & methods
UAS photogrammetry and deep learning for detection and mapping, developed during the M.S. in Geospatial Systems Engineering at Texas A&M University-Corpus Christi.
## My contribution
Master's thesis research, advised by Dr. Michael J. Starek; presented at the TAMUCC Research and Innovation Symposium in 2023.
## Research output
[Read the master's thesis](https://www.proquest.com/docview/2864701741?pq-origsite=gscholar&fromopenview=true&sourcetype=Dissertations%20&%20Theses).
Study-area figures and quantitative evaluation visuals will be added with the research materials.
''')]
for i,(slug,title,summary,image,tags,lidar,body) in enumerate(projects): put('projects',slug,title,body,order=i,summary=summary,image=image,alt=title+' — associated presentation photograph',tags=tags,lidar=lidar,pending=['Research figures / poster — upload pending'])

# Preserve compatible image URLs while stripping metadata and resizing for the web.
manifest={}
out=SITE/'public/assets/img'; out.mkdir(parents=True,exist_ok=True)
optimized=SITE/'public/media'; optimized.mkdir(parents=True,exist_ok=True)
for source in (ROOT/'assets/img').iterdir():
    if not source.is_file(): continue
    with Image.open(source) as original:
        image=ImageOps.exif_transpose(original).convert('RGB')
        image.thumbnail((1600,1600))
        dest=out/source.name
        image.save(dest,quality=85)
        variants=[]
        for width in [480,960,1440]:
            resized=image.copy(); resized.thumbnail((width,width))
            name=source.stem.replace(' ','-')+f'-{width}.webp'
            resized.save(optimized/name,'WEBP',quality=80)
            variants.append(dict(src='/media/'+name,width=resized.width,height=resized.height))
        manifest['/assets/img/'+source.name]=dict(width=image.width,height=image.height,variants=variants)
(SITE/'src/data/images.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

# Retain a reviewable inventory of original external links without publishing it.
links=set()
for source in ROOT.glob('*.md'):
    if source.name=='AGENTS.md': continue
    links.update(re.findall(r'https?://[^\s<>"\)]+',source.read_text(encoding='utf-8')))
(ROOT/'docs/existing-external-links.txt').write_text('\n'.join(sorted(links)),encoding='utf-8')
print('Imported content and optimized',len(manifest),'images')
