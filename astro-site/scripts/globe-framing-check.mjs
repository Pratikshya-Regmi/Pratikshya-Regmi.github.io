import {chromium} from '@playwright/test';
const browser=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
 const page=await context.newPage();
 await page.goto('http://localhost:4321/');
 await page.locator('[data-journey-load]').click();
 await page.locator('[data-map-tools]').waitFor({state:'visible',timeout:40000});
 for(const width of [1440,375]){
  await page.setViewportSize({width,height:1000});
  for(const [control,name] of [['data-overview','earth'],['data-distance-view','distance']]){
   await page.locator(`[${control}]`).click();
   await page.waitForTimeout(3500);
   await page.locator('[data-journey-canvas]').screenshot({path:`test-results/globe-${name}-${width}.png`});
  }
 }
 console.log('Globe framing screenshots saved.');
} finally {await browser.close();}
