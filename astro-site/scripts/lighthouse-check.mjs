import lighthouse from 'lighthouse';
import {chromium} from '@playwright/test';
import {writeFile,mkdir} from 'node:fs/promises';
const browser=await chromium.launch({headless:true,args:['--remote-debugging-port=9222']});
await mkdir('test-results',{recursive:true});
try{
 const summaries=[];
 for(const [name,route] of [['home','/'],['project','/projects/helene/']]){
  const result=await lighthouse('http://localhost:4321'+route,{port:9222,output:'json',logLevel:'error',onlyCategories:['performance','accessibility','best-practices','seo']});
  await writeFile(`test-results/lighthouse-${name}.json`,result.report);
  const summary={page:route,scores:Object.fromEntries(Object.entries(result.lhr.categories).map(([key,value])=>[key,Math.round(value.score*100)])),issues:Object.values(result.lhr.audits).filter(a=>a.score!==null&&a.score<1).map(a=>({id:a.id,title:a.title,score:a.score,displayValue:a.displayValue}))};
  summaries.push(summary);console.log(JSON.stringify(summary,null,2));
 }
 await writeFile('test-results/lighthouse-summary.json',JSON.stringify(summaries,null,2));
}finally{await browser.close();}
