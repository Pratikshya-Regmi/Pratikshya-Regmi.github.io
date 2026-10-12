"""Read-only guard for the exact public documents shipped to Pages."""
from pathlib import Path
import sys,re
site=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(site.parent/'.tools/python'))
import pymupdf
for path in (site/'public/assets').glob('*.pdf'):
    with pymupdf.open(path) as doc:
        text='\n'.join(page.get_text() for page in doc)
        assert not re.search(r'\bCell:|\bApt\s|\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}',text,re.I),f'Private contact information in {path.name}'
        assert not re.search(r'\b\d{1,6}\s+(?:[A-Za-z]+\s+){0,5}(?:Rd|Road|Street|St|Ave|Avenue|Blvd|Lane|Ln|Drive|Dr)\b',text,re.I),f'Possible street address in {path.name}'
        assert not doc.embfile_count(),f'Unexpected embedded files in {path.name}'
        assert all(not link.get('uri','').startswith('tel:') for page in doc for link in page.get_links())
        assert 'pregmi3@ncsu.edu' in text
    print(path.name+': privacy check passed')
