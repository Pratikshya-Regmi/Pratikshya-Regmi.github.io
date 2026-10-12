"""One-time addition to the existing public CV; preserves text and URI links.
Requires PyMuPDF (same as the existing PDF privacy tools).
Writes a review copy first; does not touch the employment resume.
"""
from pathlib import Path
from collections import Counter
import re, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.tools/python'))
import pymupdf as fitz
source=ROOT/'assets/CV_PR.pdf'
original=fitz.open(source)
before='\n'.join(p.get_text() for p in original)
if 'Oak Ridge National Laboratory' in before:
    raise SystemExit('ORNL already present; no duplicate entry added.')
assert len(original)==5, 'Review layout before changing a different CV edition.'
assert original[0].search_for('POSITIONS AND AFFILIATIONS')
output=fitz.open()
output.new_page(width=612,height=792)
output.insert_pdf(original,from_page=1)
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
place(0,fitz.Rect(0,65,612,163),p,fitz.Rect(0,33,612,131))
place(0,fitz.Rect(0,169,612,442),p,fitz.Rect(18.36,137,593.64,393.62))
place(0,fitz.Rect(0,448,612,469),p,fitz.Rect(0,407,612,428))
place(0,fitz.Rect(0,480,612,715.4),p,fitz.Rect(0,494,612,729.4))
p.insert_text((92,442),'-',fontname='tiro',fontsize=11)
p.insert_text((110,442),'Intern, Oak Ridge National Laboratory',fontname='tibo',fontsize=11)
p.insert_text((128,456),'May 2026 - August 2026',fontname='tiro',fontsize=11)
p.insert_text((128,470),'Project: Assessing Forest Resistance, Delayed Canopy Loss, and',fontname='tiro',fontsize=11)
p.insert_text((128,484),'Early Recovery Following Hurricane Helene',fontname='tiro',fontsize=11)
p.insert_text((534,742),'1',fontname='tiro',fontsize=7.92)
# Keep the existing summer-assistant heading with its details on page two.
place(0,fitz.Rect(0,715.5,612,731),output[1],fitz.Rect(0,48,612,63.5))
output.set_metadata({})
output.del_xml_metadata()
target=ROOT/'astro-site/test-results/CV_PR-ornl-review.pdf'
output.save(target,garbage=4,deflate=True,clean=True)
output.close()
with fitz.open(target) as checked:
    after='\n'.join(p.get_text() for p in checked)
    missing=Counter(re.findall(r'\w+',before))-Counter(re.findall(r'\w+',after))
    assert not missing, f'Original CV words missing: {missing}'
    old_links=Counter(l['uri'] for p in original for l in p.get_links() if l.get('uri'))
    new_links=Counter(l['uri'] for p in checked for l in p.get_links() if l.get('uri'))
    assert not old_links-new_links, 'Existing URI links lost'
    assert after.count('Oak Ridge National Laboratory')==1
    for i in [0,1]:checked[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(ROOT/f'astro-site/test-results/cv-ornl-page-{i+1}.png')
    print(f'Review CV: {len(checked)} pages; all existing words and {sum(old_links.values())} URI links retained.')
original.close()
