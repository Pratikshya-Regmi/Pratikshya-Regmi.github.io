import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
const browser=await chromium.launch();
try {
const page=await browser.newPage();
await page.goto('http://localhost:4321/');
assert.equal(await page.locator('[data-chapter] img').count(),10);
for(const width of [375,1440]){
await page.setViewportSize({width,height:1000});
for(let i=0;i<7;i++){
await page.locator(`[data-stop="${i}"]`).click();
const chapter=page.locator(`[data-chapter="${i}"]`);
const details=chapter.locator('details');
if(await details.count()) await details.evaluate(el=>el.open=true);
for(const img of await chapter.locator('img').all()){
await img.scrollIntoViewIfNeeded();
await img.evaluate(el=>el.decode());
assert(await img.evaluate(el=>el.naturalWidth>0));
}
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
}
}
console.log('All 10 journey photos load; seven chapters and expandable photos pass at 375 and 1440px.');
}finally{await browser.close();}

