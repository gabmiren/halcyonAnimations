const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const f=process.argv[2];const dir=process.argv[3];fs.mkdirSync(dir,{recursive:true});const ts=process.argv.slice(4).map(Number);
const br=await chromium.launch();const p=await br.newPage({viewport:{width:1080,height:1920}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+path.resolve(f));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
for(const t of ts){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`${dir}/${t.toFixed(2).padStart(6,'0')}.jpg`,type:'jpeg',quality:85});}
console.log('errors',errs);await br.close();})();
