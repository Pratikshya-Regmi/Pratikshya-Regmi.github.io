import {readdir,readFile,stat} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('dist');
async function walk(dir){return (await Promise.all((await readdir(dir,{withFileTypes:true})).map(e=>e.isDirectory()?walk(path.join(dir,e.name)):path.join(dir,e.name)))).flat();}
const files=await walk(root);const failures=[];let checked=0;
for(const file of files){
 if(/\.(las|laz|e57)$/i.test(file)) failures.push(`Raw data in output: ${file}`);
 if(!file.endsWith('.html'))continue;
 const text=await readFile(file,'utf8');
 if(/\bCell:|\bApt\s|\b\d{3}[\s()-]+\d{3}[\s-]+\d{4}\b|ARTICLE_URL|your-post-link/.test(text))failures.push(`Private or placeholder link text: ${file}`);
 for(const match of text.matchAll(/(?:href|src)="([^"#]+)"/g)){
  const value=match[1].replaceAll('&amp;','&');if(!value.startsWith('/'))continue;
  const target=path.join(root,decodeURIComponent(value.split(/[?#]/)[0]));
  try{const info=await stat(target);if(info.isDirectory())await stat(path.join(target,'index.html'));checked++;}catch{failures.push(`Missing ${value} in ${path.relative(root,file)}`);}
 }
}
for(const forbidden of ['AGENTS.md','_config.yml','README.md','src','node_modules']){try{await stat(path.join(root,forbidden));failures.push(`Source exposed: ${forbidden}`);}catch{}}
if(failures.length){console.error(failures.join('\n'));process.exit(1);}
console.log(`Validated ${files.length} output files and ${checked} internal references; source/private text checks passed.`);
