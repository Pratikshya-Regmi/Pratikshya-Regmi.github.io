import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {distanceKm,distanceLabel,greatCircle,arcPoint} from '../src/utils/journey-geometry.ts';
assert(Math.abs(distanceKm([0,0],[90,0])-10007.557)<0.01);
assert.equal(distanceKm([85,28],[85,28]),0);
assert.deepEqual(arcPoint([0,0],[90,0],0.5),[45,0]);
assert.throws(()=>arcPoint([0,0],[180,0],0.5),/antipodal/);
const wrap=greatCircle([179,0],[-179,0]);
assert.equal(wrap.length,2);assert(Math.abs(distanceKm([179,0],[-179,0])-222.39)<0.01);
const places=JSON.parse(await readFile('src/data/locations.json','utf8'));
const coord=id=>{const p=places.find(p=>p.id===id);return [p.lng,p.lat]};
const from=coord('kathmandu'),to=coord('tamucc'),route=greatCircle(from,to);
assert.deepEqual(route[0][0],from);assert.deepEqual(route.at(-1).at(-1),to);
let length=0;
for(const segment of route)for(let i=1;i<segment.length;i++){
 assert(Math.abs(segment[i][0]-segment[i-1][0])<=180,'Dateline split failed');
 length+=distanceKm(segment[i-1],segment[i]);
}
assert(Math.abs(length-distanceKm(from,to))<0.1,'Arc length should match surface distance');
assert(distanceKm(from,to)>13000&&distanceKm(from,to)<15000);
console.log(`Geometry passed: known distances, short dateline crossing, antipodal ambiguity, valid route segments. Nepal–Texas: ${distanceLabel(from,to)}.`);
