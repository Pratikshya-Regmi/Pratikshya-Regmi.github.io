from pathlib import Path
import json
from PIL import Image,ImageOps
site=Path(__file__).resolve().parents[1]
manifest_path=site/'src/data/images.json'
manifest=json.loads(manifest_path.read_text())
for name in ['AGU.jpeg','agu1.jpg','iale.jpeg','tamuccsympo.jpg']:
    with Image.open(site.parent/'assets/img'/name) as source:
        image=ImageOps.exif_transpose(source).convert('RGB')
        variants=[]
        for width in [480,800,1200]:
            thumb=ImageOps.fit(image,(width,round(width*.625)))
            filename=Path(name).stem+f'-cover-{width}.webp'
            thumb.save(site/'public/media'/filename,'WEBP',quality=72)
            variants.append(dict(src='/media/'+filename,width=thumb.width,height=thumb.height))
        manifest['/assets/img/'+name]['covers']=variants
manifest_path.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
