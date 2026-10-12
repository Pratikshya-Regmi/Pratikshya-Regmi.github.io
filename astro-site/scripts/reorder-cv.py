"""Reorder existing CV regions without changing their text or links."""
from pathlib import Path
from collections import Counter
import sys,re,shutil
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.tools/python'))
import pymupdf as fitz
original=fitz.open(ROOT/'assets/CV_PR.pdf')
assert len(original)==5
output=fitz.open()
output.new_page(width=612,height=792)
output.insert_pdf(original,from_page=1,to_page=3)
output.new_page(width=612,height=792)
def place(source_page, clip, dest_page, destination):
    # Remove text outside each retained region, so clipped content cannot remain
    # hidden/searchable or appear multiple times in extracted CV text.
    segment=fitz.open()
    segment.insert_pdf(original,from_page=source_page,to_page=source_page)
    page=segment[0]
    links=[l for l in page.get_links() if l.get('uri') and clip.contains(l['from'])]
    for rect in [fitz.Rect(0,0,612,clip.y0),fitz.Rect(0,clip.y1,612,792)]:
        page.add_redact_annot(rect,fill=(1,1,1))
    page.apply_redactions()
    dest_page.show_pdf_page(destination,segment,0,clip=clip,keep_proportion=False)
    sx=destination.width/clip.width;sy=destination.height/clip.height
    for link in links:
        r=link['from']
        target=fitz.Rect(destination.x0+(r.x0-clip.x0)*sx,destination.y0+(r.y0-clip.y0)*sy,destination.x0+(r.x1-clip.x0)*sx,destination.y0+(r.y1-clip.y0)*sy)
        dest_page.insert_link({'kind':fitz.LINK_URI,'from':target,'uri':link['uri']})
    segment.close()
p=output[0]
# Keep the header, education and section heading; ongoing role precedes internship.
assert original[0].search_for('Intern, Oak Ridge')[0].y0 < 450, 'CV already reordered or layout changed'
place(0,fitz.Rect(0,0,612,429),p,fitz.Rect(0,0,612,429))
place(0,fitz.Rect(0,494,612,730),p,fitz.Rect(0,430,612,666))
place(0,fitz.Rect(0,430,612,488),p,fitz.Rect(0,674,612,732))
place(0,fitz.Rect(0,733,612,792),p,fitz.Rect(0,733,612,792))
# Five service rows: ongoing appointments first, then latest end date.
p=output[4]
lines=[line for block in original[4].get_text('dict')['blocks'] if 'lines' in block for line in block['lines']]
rows=[]
for line in lines:
 text=''.join(s['text'] for s in line['spans'])
 if 70 < line['bbox'][1] < 144 and len(text.strip()) > 2:
  rows.append(line['bbox'])
ys=sorted(set(round(r[1],2) for r in rows))
assert len(ys)==5,ys
bounds=[70]+[(ys[i]+12.3+ys[i+1])/2 for i in range(4)]+[144]
place(4,fitz.Rect(0,0,612,70),p,fitz.Rect(0,0,612,70))
for target,source in enumerate([1,3,0,2,4]):
 clip=fitz.Rect(0,bounds[source],612,bounds[source+1])
 # Translate each baseline into the original target row without scaling typography.
 dest=fitz.Rect(0,clip.y0+ys[target]-ys[source],612,clip.y1+ys[target]-ys[source])
 place(4,clip,p,dest)
place(4,fitz.Rect(0,144,612,792),p,fitz.Rect(0,144,612,792))
target=ROOT/'astro-site/test-results/CV_PR-chronological.pdf'
output.set_metadata({})
output.save(target,garbage=4,deflate=True,clean=True)
output.close()
with fitz.open(target) as checked:
 words=lambda doc: Counter(re.findall(r'\w+',' '.join(p.get_text() for p in doc)))
 assert words(original)==words(checked),'CV text changed'
 links=lambda doc:Counter(l['uri'] for p in doc for l in p.get_links() if l.get('uri'))
 assert links(original)==links(checked),'CV links changed'
 for i in [0,4]:checked[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(ROOT/f'astro-site/test-results/cv-chronology-{i+1}.png')
original.close()
for path in ['assets/CV_PR.pdf','astro-site/public/assets/CV_PR.pdf']:
 shutil.copyfile(target,ROOT/path)
print('CV reordered; every word and URI link preserved.')

