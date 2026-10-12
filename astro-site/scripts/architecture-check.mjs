import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage();
const navigation=JSON.parse(await readFile('src/data/navigation.json','utf8'));
const redirects=JSON.parse(await readFile('src/data/redirects.json','utf8'));
const base=process.env.PREVIEW_URL || 'http://localhost:4321';
const results=[];
try{
 await page.goto(base+'/');
 assert.deepEqual(await page.locator('.desktop-nav > a').allTextContents(),navigation.primary.map(x=>x[0]));
 results.push('Exactly seven primary navigation items');
 for(const [old,target] of Object.entries(redirects))for(const suffix of (process.env.PREVIEW_URL ? ['/', '.html',''] : ['/', '.html'])){
  await page.goto(base+'/'+old+suffix);
  await page.waitForURL(base+target);
 }
 await page.goto(base+'/conferences/#conference-3');await page.waitForURL(base+'/presentations/#conference-3');
 results.push('Legacy route forms and bookmarked presentation fragment redirect correctly');
 await page.setViewportSize({width:375,height:812});await page.goto(base+'/');
 await page.locator('.mobile-nav > summary').click();await page.locator('.mobile-research summary').click();
 assert.equal(await page.locator('.mobile-research details a:visible').count(),7);
 await page.locator('.mobile-research a[href="/projects/#hackathons"]').click();await page.waitForURL(base+'/projects/#hackathons');
 results.push('Mobile secondary menu opens and reaches hackathons');
 await page.locator('[data-filter="LiDAR"]').click();assert.equal(await page.locator('.project-row:visible').count(),3);
 await page.locator('[data-filter="All"]').click();assert.equal(await page.locator('.project-row:visible').count(),5);
 results.push('Project filters show correct subset and restore all projects');
 await page.goto(base+'/cv/');assert.equal(await page.locator('a[download][href="/assets/CV_PR.pdf"]').count(),1);
 await page.goto(base+'/education/');await page.locator('[data-campus="tamucc"]').click();assert.equal(new URL(page.url()).hash,'#tamucc');assert.ok(await page.locator('#tamucc').isVisible());
 results.push('CV download and education timeline work');
 const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();await staticPage.goto(base+'/projects/');assert.equal(await staticPage.locator('.project-row:visible').count(),5);await nojs.close();
 results.push('All projects remain available without JavaScript');
 console.log(JSON.stringify(results,null,2));await writeFile('test-results/architecture-report.json',JSON.stringify(results,null,2));
}finally{await browser.close();}
