import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {mkdir,writeFile} from 'node:fs/promises';
await mkdir('test-results',{recursive:true});
await mkdir('../docs/previews',{recursive:true});
const browser=await chromium.launch({headless:true});
const report={layouts:[],accessibility:[],errors:[],interaction:[]};
const paths=['/projects/helene-forest-recovery/','/work-research/','/community/','/cv/','/','/aboutme/','/education/','/experience/','/projects/','/projects/helene/','/presentations/','/conferences/','/symposiums/','/workshops/','/honors/','/Publications/','/hackathon/','/volunteer/','/geogiggles/','/certifications/','/resume/','/contact/','/engagement/','/service/','/media/','/blogs/'];
const context=await browser.newContext();
const page=await context.newPage();
page.on('pageerror',e=>report.errors.push(e.message));
for(const width of [320,375,768,1024,1440]){
 await page.setViewportSize({width,height:1000});
 for(const route of paths){
  const response=await page.goto('http://localhost:4321'+route,{waitUntil:'networkidle'});
  await page.evaluate(async()=>{await Promise.all([...document.images].map(async image=>{image.loading='eager';try{await image.decode();}catch{}}));});
  const metrics=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,brokenImages:[...document.images].filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.src),h1:document.querySelectorAll('h1').length}));
  report.layouts.push({width,route,status:response.status(),...metrics});
 }
 if(width===375||width===1440){await page.goto('http://localhost:4321/');await page.evaluate(async()=>{await Promise.all([...document.images].map(async image=>{image.loading='eager';try{await image.decode();}catch{}}));});await page.screenshot({path:`test-results/home-${width}.png`,fullPage:true});await page.screenshot({path:`../docs/previews/homepage-${width===1440?'desktop':'mobile'}.png`});}
}
await page.setViewportSize({width:1440,height:1000});
for(const route of ['/work-research/','/community/','/cv/','/','/aboutme/','/education/','/projects/','/projects/helene/','/Publications/','/hackathon/','/geogiggles/']){
 await page.goto('http://localhost:4321'+route,{waitUntil:'networkidle'});
 const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']).analyze();
 report.accessibility.push({route,violations:result.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>n.target)}))});
}
await page.setViewportSize({width:375,height:812});await page.goto('http://localhost:4321/');
await page.locator('.mobile-nav > summary').click();await page.locator('.mobile-nav a[href="/education/"]').click();
report.interaction.push({mobileMenu:page.url().endsWith('/education/')});
await page.goto('http://localhost:4321/');await page.keyboard.press('Tab');report.interaction.push({skipLink:await page.locator('.skip-link').evaluate(x=>x===document.activeElement)});await page.keyboard.press('Enter');report.interaction.push({skipTarget:await page.locator('#main').evaluate(x=>x===document.activeElement)});
await page.emulateMedia({reducedMotion:'reduce'});report.interaction.push({reducedMotion:await page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches)});
const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:375,height:812}});const staticPage=await nojs.newPage();await staticPage.goto('http://localhost:4321/');report.interaction.push({noJsContent:await staticPage.locator('h1').isVisible(),staticLidarPlaceholder:await staticPage.getByText('LiDAR visualization — data upload pending',{exact:true}).isVisible()});
await browser.close();
await writeFile('test-results/browser-report.json',JSON.stringify(report,null,2));
const failed=report.layouts.filter(x=>x.overflow||x.brokenImages.length||x.h1!==1||x.status!==200);
const a11y=report.accessibility.filter(x=>x.violations.length);
console.log(JSON.stringify({layouts:report.layouts.length,layoutFailures:failed,accessibility:a11y,errors:report.errors,interactions:report.interaction},null,2));
if(failed.length||a11y.length||report.errors.length||report.interaction.some(x=>Object.values(x).some(v=>v===false)))process.exitCode=1;
