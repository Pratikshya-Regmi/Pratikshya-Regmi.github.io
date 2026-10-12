import {readdir,readFile,writeFile,copyFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('dist');
const names=(await readdir(root,{withFileTypes:true})).filter(x=>x.isDirectory()&&!x.name.startsWith('_')).map(x=>x.name);
const redirects=JSON.parse(await readFile('src/data/redirects.json','utf8'));
const routes=['/'];
for(const name of names){
 try{await readFile(path.join(root,name,'index.html'));}catch{continue;}
 if(!redirects[name]) routes.push(`/${name}/`);
 if(name==='404'){await copyFile(path.join(root,name,'index.html'),path.join(root,'404.html'));continue;}
 const target=redirects[name] ?? `/${name}/`;
 await writeFile(path.join(root,`${name}.html`),`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Continue to ${name}</title><link rel="canonical" href="https://pratikshya-regmi.github.io${target.split('#')[0]}"><meta http-equiv="refresh" content="0;url=${target}"></head><body><a href="${target}">Continue to ${name}</a><script>if(location.hash)location.replace(${JSON.stringify(target.split("#")[0])}+location.hash);</script></body></html>`);
}
const projects=(await readdir(path.join(root,'projects'),{withFileTypes:true})).filter(x=>x.isDirectory());
routes.push(...projects.map(x=>`/projects/${x.name}/`));
await writeFile(path.join(root,'sitemap.xml'),`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${routes.filter(x=>x!='/404/').map(x=>`<url><loc>https://pratikshya-regmi.github.io${x}</loc></url>`).join('')}</urlset>`);
await writeFile(path.join(root,'feed.xml'),'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Pratikshya Regmi</title><link>https://pratikshya-regmi.github.io/</link><description>Geospatial research portfolio. No blog posts have been published.</description></channel></rss>');
await writeFile(path.join(root,'tags.html'),'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Research topics</title><meta http-equiv="refresh" content="0;url=/projects/"></head><body><a href="/projects/">Explore research topics</a></body></html>');
await writeFile(path.join(root,'.nojekyll'),'');
