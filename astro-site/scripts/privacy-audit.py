"""Audit the complete working tree without printing personal values.

Read the pre-migration documents from Git into memory to identify the exact
historical values. Never write private originals or extracted text to disk.
--replace-tracked replaces only the two named tracked PDFs with reviewed copies.
"""
from pathlib import Path
import sys,subprocess,re,json,shutil,hashlib,os
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'.tools/python'))
import pymupdf
names=['CV_PR.pdf','Pratikshya_Resume_oct025.pdf']
phone_re=re.compile(r'(?:\+1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}')
address_re=re.compile(r'\b\d{1,6}\s+(?:[A-Za-z]+\s+){0,5}(?:Rd|Road|Street|St|Ave|Avenue|Blvd|Lane|Ln|Drive|Dr)\b',re.I)
phones=set();address_terms=set();history=[]
for name in names:
    data=subprocess.check_output(['git','show','3f90ac2:assets/'+name],cwd=root)
    with pymupdf.open(stream=data,filetype='pdf') as doc:text='\n'.join(p.get_text() for p in doc)
    matches=phone_re.findall(text)
    addresses=[line.strip() for line in text.splitlines() if address_re.search(line)]
    phones.update(re.sub(r'\D','',x)[-10:] for x in matches)
    for line in addresses:
        address_terms.add(line.casefold())
        match=address_re.search(line)
        if match:address_terms.add(match[0].casefold())
    history.append({'file':'assets/'+name,'sensitive_content_in_baseline_history':bool(matches or addresses)})
    del data,text
patterns=[re.compile(rb'[ ()+.-]*'.join(bytes([c]) for c in digits.encode())) for digits in phones]
terms=[term.encode() for term in address_terms]
def sensitive(data):
    low=data.lower()
    return any(term in low for term in terms) or any(pattern.search(data) for pattern in patterns)
if '--replace-tracked' in sys.argv:
    for name in names:
        safe=root/'astro-site/public/assets'/name
        with pymupdf.open(safe) as doc:
            assert not sensitive(('\n'.join(p.get_text() for p in doc)).encode()),'Public copy failed verification'
        shutil.copyfile(safe,root/'assets'/name)
findings=[];errors=[];files=0;pdfs=0;paths=[]
for directory,dirs,filenames in os.walk(root):
    if Path(directory)==root:dirs[:]=[d for d in dirs if d!='.git']
    for name in filenames:
        paths.append(Path(directory)/name)
def check_file(p):
    try:
        data=p.read_bytes()
        return p,sensitive(data),None
    except Exception as error:return p,False,type(error).__name__
print('Scanning',len(paths),'current working-tree files, including ignored files.',flush=True)
with ThreadPoolExecutor(max_workers=8) as pool:
    for p,hit,error in pool.map(check_file,paths):
        files+=1
        if error:errors.append({'file':str(p.relative_to(root)),'error':error})
        if p.suffix.lower()=='.pdf' and not error:
            pdfs+=1
            try:
                with pymupdf.open(p) as doc:
                    hit=hit or sensitive(('\n'.join(page.get_text() for page in doc)).encode())
                    hit=hit or sensitive(json.dumps(doc.metadata).encode())
            except Exception as error:errors.append({'file':str(p.relative_to(root)),'error':type(error).__name__})
        if hit:findings.append(str(p.relative_to(root)))
        if files%5000==0:print('Scanned',files,'files.',flush=True)
copies={}
for name in names:
    paths=[root/'assets'/name,root/'astro-site/public/assets'/name,root/'astro-site/dist/assets'/name]
    copies[name]={'identical_public_copies':len({hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})==1}
report={'scope':'All current working-tree files, including ignored tools, dependencies, build output, and caches. .git is history, checked separately in memory.','files_scanned':files,'pdfs_decoded':pdfs,'findings':findings,'scan_errors':errors,'documents':copies,'history':history,'private_backup_created':False}
out=root/'docs/privacy-audit.json';out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if findings or errors or not all(x['identical_public_copies'] for x in copies.values()):sys.exit(1)
