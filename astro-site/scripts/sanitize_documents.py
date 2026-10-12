"""Create public PDF copies with real text redaction, not visual overlays.
Requires PyMuPDF. Tracked source documents must already be public-safe.
Do not store private originals in this repository.
"""
from pathlib import Path
import sys,re
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'.tools/python'))
import pymupdf
out=ROOT/'astro-site/public/assets'
out.mkdir(parents=True,exist_ok=True)
for source in (ROOT/'assets').glob('*.pdf'):
    doc=pymupdf.open(source)
    removed=[]
    for page in doc:
        text=page.get_text()
        targets=[]
        for line in text.splitlines():
            if re.search(r'\b(?:Apt\s|Cell:)',line,re.I) or re.search(r'\b\d{1,6}\s+(?:[A-Za-z]+\s+){0,5}(?:Rd|Road|Street|St|Ave|Avenue|Blvd|Lane|Ln|Drive|Dr)\b',line,re.I): targets.append(line.strip())
            else: targets.extend(re.findall(r'(?:\+1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}',line))
        for target in targets:
            for rect in page.search_for(target):
                page.add_redact_annot(rect,fill=(1,1,1));removed.append(target)
        page.apply_redactions()
        for link in page.get_links():
            if link.get('uri','').startswith('tel:'): page.delete_link(link)
    doc.set_metadata({})
    doc.del_xml_metadata()
    for name in doc.embfile_names(): doc.embfile_del(name)
    dest=out/source.name
    doc.save(dest,garbage=4,deflate=True,clean=True)
    doc.close()
    with pymupdf.open(dest) as checked:
        text='\n'.join(p.get_text() for p in checked)
        assert all(value not in text for value in removed)
        assert not re.search(r'\bCell:|\bApt\s|\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}',text,re.I)
        assert 'pregmi3@ncsu.edu' in text
    print(source.name,': redacted',len(removed),'items; public text verified')
