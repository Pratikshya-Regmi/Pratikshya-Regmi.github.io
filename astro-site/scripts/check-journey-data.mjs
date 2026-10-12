import assert from 'node:assert/strict';
import {readFile,readdir,stat} from 'node:fs/promises';
const locations=JSON.parse(await readFile('src/data/locations.json','utf8'));
const journey=JSON.parse(await readFile('src/data/journey.json','utf8'));
assert.equal(new Set(locations.map(p=>p.id)).size,locations.length,'Place IDs must be unique');
assert.equal(new Set(journey.chapters.map(p=>p.locationId)).size,journey.chapters.length,'Chapter locations must be unique');
const home=locations.find(p=>p.id==='home');
assert(home,'A public home-region record is required');
for(const key of ['lat','lng'])assert.equal(Math.round(home[key]*100)/100,home[key],'Keep home coordinates generalized to two decimal degrees');
assert(home.areaRadiusKm>=1,'Show home as an area, not an exact house');
for(const chapter of journey.chapters){
 const location=locations.find(p=>p.id===chapter.locationId);
 assert(location,`Missing place ${chapter.locationId}`);
 assert(Number.isFinite(location.lat)&&Math.abs(location.lat)<=90);
 assert(Number.isFinite(location.lng)&&Math.abs(location.lng)<=180);
 if(chapter.record)await stat(`src/content/${chapter.record.collection}/${chapter.record.id}.md`);
 for(const photo of chapter.photos){
  assert(photo.src.startsWith('/assets/journey/'),'Use local journey photographs');
  assert(photo.alt.trim()&&photo.width>0&&photo.height>0,'Photo alt text and dimensions are required');
  await stat(`public${photo.src}`);
 }
}
async function checkPublic(dir){
 for(const file of await readdir(dir,{withFileTypes:true})){
  if(file.isDirectory())await checkPublic(`${dir}/${file.name}`);
  else assert(!/\.(kml|kmz)$/i.test(file.name),'Do not publish the original location export');
 }
}
await checkPublic('public');
console.log('Journey references, coordinates, home-region precision and public assets verified.');
