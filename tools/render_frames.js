const fs=require('fs');const {chromium}=require('playwright');
const [svgPath,outDir,pw,ph,fps,secs]=process.argv.slice(2);
(async()=>{const svg=fs.readFileSync(svgPath,'utf8');fs.mkdirSync(outDir,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+pw,height:+ph}});
await p.setContent('<body style="margin:0;overflow:hidden">'+svg.replace('<svg ','<svg style="width:100vw;height:100vh;display:block" ')+'</body>');
await p.waitForTimeout(300);
const n=+fps*+secs;
for(let i=0;i<n;i++){await p.evaluate(t=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=t}),i*1000/+fps);
await p.screenshot({path:`${outDir}/f${String(i).padStart(4,'0')}.png`});}
await b.close()})();
