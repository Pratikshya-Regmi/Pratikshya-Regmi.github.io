import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
const browser=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
try {
 await page.goto('http://localhost:4321/');
 await page.locator('[data-journey-load]').click();
 await page.waitForFunction(()=>document.querySelector('[data-journey]').dataset.tourRunning==='true',{},{timeout:40000});
 assert.equal(await page.locator('[data-journey]').getAttribute('data-tour-phase'),'earth');
 await page.locator('[data-play]').click();
 await page.waitForTimeout(1200);
 assert.equal(await page.locator('[data-journey]').getAttribute('data-tour-phase'),'earth');
 await page.locator('[data-journey-canvas]').screenshot({path:'test-results/journey-earth.png'});
 await page.evaluate(()=>{
   const shell=document.querySelector('[data-journey]');window.tourPhases=['earth'];
   new MutationObserver(()=>{const phase=shell.dataset.tourPhase;if(phase!==window.tourPhases.at(-1))window.tourPhases.push(phase)}).observe(shell,{attributes:true,attributeFilter:['data-tour-phase']});
 });
 await page.locator('[data-play]').click();
 // The complete user-paced sequence is intentionally tested in real time.
 await page.waitForFunction(()=>document.querySelector('[data-journey]').dataset.tourPhase==='nepal-to-usa',{},{timeout:60000});
 await page.waitForTimeout(4200);
 await page.locator('[data-play]').click();
 assert((await page.locator('[data-tour-heading]').innerText()).includes('13,900 km'));
 await page.locator('[data-journey-canvas]').screenshot({path:'test-results/journey-nepal-texas-globe.png'});
 await page.locator('[data-play]').click();
 await page.waitForFunction(()=>document.querySelector('[data-journey]').dataset.tourPhase==='ncsu',{},{timeout:45000});
 await page.waitForFunction(()=>document.querySelector('[data-journey]').dataset.tourRunning==='false');
 const phases=await page.evaluate(()=>window.tourPhases);
 assert.deepEqual(phases,['earth','nepal','home','beni','capitol','kathmandu','depart-nepal','nepal-to-usa','usa','tamucc','ncsu']);
 await page.locator('[data-restart]').click();
 assert.equal(await page.locator('[data-journey]').getAttribute('data-tour-phase'),'earth');
 await page.locator('[data-place-picker]').selectOption('1');
 await page.waitForTimeout(4200);
 assert.equal(await page.locator('[data-journey]').getAttribute('data-tour-phase'),'beni');
 assert.equal(await page.locator('[data-journey]').getAttribute('data-tour-running'),'false');
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.waitForFunction(()=>document.querySelector('[data-play]').disabled);
 await page.locator('[data-distance-view]').click();
 assert.equal(await page.locator('[data-journey]').getAttribute('data-tour-phase'),'nepal-to-usa');
 await page.setViewportSize({width:375,height:812});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('[data-journey-canvas]').screenshot({path:'test-results/journey-globe-mobile.png'});
 assert.deepEqual(errors,[]);
 const result={phases,pauseResume:true,restart:true,manualCancellation:true,reducedMotion:true,mobileOverflow:false,errors};
 await writeFile('test-results/globe-tour-report.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
} finally {await browser.close();}
