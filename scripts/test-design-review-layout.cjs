#!/usr/bin/env node
/* Browser regression for the public mount contract. No fictional example CSS.
 * Supply an existing Playwright installation via PLAYWRIGHT_MODULE if needed.
 * node scripts/test-design-review-layout.cjs [assets-directory] [evidence-directory]
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assets = path.resolve(process.argv[2] || path.join(__dirname,'../skills/_collections/design/design-review/assets'));
const evidence = process.argv[3] && path.resolve(process.argv[3]);
const near = (actual, expected, message) => assert(Math.abs(actual-expected)<=1, `${message}: ${actual} vs ${expected}`);
async function settle(page) { await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))); }
async function metrics(page) {
  return page.evaluate(()=>{
    const rect=id=>{const e=document.getElementById(id),r=e.getBoundingClientRect(),s=getComputedStyle(e);
      return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,display:s.display,
        overflow:s.overflow,clientHeight:e.clientHeight,scrollHeight:e.scrollHeight,scrollTop:e.scrollTop};};
    return {width:innerWidth,height:innerHeight,pageWidth:document.documentElement.scrollWidth,
      pageHeight:document.documentElement.scrollHeight,pageScroll:scrollY,
      layout:rect('layout'),header:rect('header'),preview:rect('preview'),drawer:rect('drawer'),
      first:rect('first'),last:rect('last'),offset:parseFloat(document.getElementById('header').style.getPropertyValue('--dr-header-offset')) || 0};
  });
}
function bounded(m, mobile) {
  near(m.pageWidth,m.width,'page width'); near(m.pageHeight,m.height,'page height');
  near(m.layout.width,m.width,'layout width'); near(m.drawer.width,m.width,'drawer width');
  near(m.drawer.bottom,m.height,'drawer bottom');
  assert(m.preview.height>=79,`usable preview height: ${JSON.stringify(m)}`);
  assert(m.drawer.y>=m.layout.y && m.drawer.height>40,'reachable drawer');
  near(m.preview.bottom,m.drawer.y,'preview ends at drawer');
  if(mobile)near(m.preview.y,m.layout.y,'mobile overlay consumes no grid row');
}
(async()=>{
  if(evidence)fs.mkdirSync(evidence,{recursive:true});
  const results=[],errors=[];
  const server=http.createServer((req,res)=>{
    const pathname=new URL(req.url,'http://localhost').pathname;
    const name=pathname.startsWith('/runtime/')?pathname.slice(9):null;
    const file=name && /^[a-z-]+\.(css|js|html)$/.test(name)?path.join(assets,name):path.join(__dirname,'fixtures/design-review-layout.html');
    res.setHeader('Content-Type',file.endsWith('.css')?'text/css':file.endsWith('.js')?'text/javascript':'text/html');
    try{res.end(fs.readFileSync(file));}catch{res.statusCode=404;res.end();}
  });
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  let browser;
  try {
    browser=await chromium.launch({channel:process.env.PLAYWRIGHT_CHANNEL || 'chrome',headless:true,chromiumSandbox:true});
    const base=`http://127.0.0.1:${server.address().port}`;
    for(const kind of ['standalone','nested','legacy'])for(const [width,height] of [[320,569],[390,638],[430,740],[1200,800]])for(const theme of ['light','dark']) {
      const mobile=width<=650,context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile,colorScheme:theme});
      try {
        const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
        await page.goto(`${base}/?kind=${kind}`);await page.waitForFunction(()=>window.controls);await settle(page);
        const before=await metrics(page);bounded(before,mobile);
        assert(before.first.y>=before.header.bottom,'first preview control clears the visible header');
        if(evidence && width===390 && theme==='light')await page.screenshot({path:path.join(evidence,`${kind}-390-initial.png`)});
        await page.locator('#preview').evaluate(e=>e.scrollTop=20);await settle(page);
        let m=await metrics(page);
        near(m.pageScroll,0,'page stays still');near(m.first.y,before.first.y-20,'preview moves once');
        near(m.offset,mobile?20:0,'partial header hide');
        await page.locator('#preview').evaluate(e=>e.scrollTop=200);await settle(page);m=await metrics(page);
        near(m.offset,mobile?m.header.height:0,'full header hide');
        await page.locator('#preview').evaluate(e=>e.scrollTop-=10);await settle(page);m=await metrics(page);
        near(m.offset,mobile?m.header.height-10:0,'immediate direction reversal');
        await page.locator('#preview').evaluate(e=>e.scrollTop=e.scrollHeight);await settle(page);m=await metrics(page);
        assert(m.last.bottom<=m.preview.bottom+1 && m.last.y>=m.preview.y,'preview end reachable');
        await page.keyboard.press('Tab');await page.locator('[data-dr=theme]').focus();await settle(page);
        near((await metrics(page)).offset,0,'keyboard reveals header');
        await page.locator('#preview').evaluate(e=>e.scrollTop=0);await settle(page);
        await page.locator('[data-dr=collapse]').click();await settle(page);
        const collapsed=await metrics(page);assert(collapsed.drawer.height<before.drawer.height,'drawer collapses');bounded(collapsed,mobile);
        await page.locator('[data-dr=collapse]').click();await settle(page);bounded(await metrics(page),mobile);
        // Header reflow and a navigation resize must not require a window resize.
        await page.evaluate(()=>{
          document.querySelector('h1').textContent='A longer title for an enlarged review';
          document.documentElement.style.fontSize='20px';
          if(document.body.classList.contains('nested'))document.querySelector('nav').style.minHeight='104px';
        });await settle(page);await settle(page);
        bounded(await metrics(page),mobile);
        const handle=page.locator('[data-dr=height-handle]');await handle.focus();await page.keyboard.press('End');await settle(page);
        bounded(await metrics(page),mobile);
        await page.locator('[data-dr=theme]').click();await settle(page);
        assert.equal(await page.locator('#drawer').getAttribute('data-theme'),theme==='light'?'dark':'light');
        bounded(await metrics(page),mobile);
        if(!mobile){
          await page.locator('[data-dr=detach]').click();await settle(page);
          assert(await page.locator('#drawer').evaluate(e=>e.classList.contains('dr-floating')));
          await page.locator('[data-dr=detach]').click();await settle(page);bounded(await metrics(page),false);
        }
        await page.keyboard.press('Escape');await page.mouse.move(0,0);
        if(evidence && width===390 && theme==='light')await page.screenshot({path:path.join(evidence,`${kind}-390.png`)});
        results.push({kind,width,height,theme,initial:before,expanded:await metrics(page)});
      } finally {await context.close();}
    }
    for(const width of [390,1200]) {
      const context=await browser.newContext({viewport:{width,height:638}});
      try {
        const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
        await page.goto(`${base}/?kind=live`);await page.waitForFunction(()=>window.controls);await settle(page);
        const m=await metrics(page);
        assert.equal(m.layout.display,'block');assert(m.layout.height>1500,'live app retains document flow');
        assert.equal(await page.locator('.dr-scroll-header-layout').count(),0);
        assert.equal(await page.locator('[data-review-scroll]').count(),0);
        assert.equal(await page.locator('#drawer').evaluate(e=>e.classList.contains('dr-floating')),width>650);
        await page.evaluate(()=>scrollTo(0,100));await settle(page);assert((await metrics(page)).pageScroll>0,'live document scrolls');
        results.push({kind:'live',width,metrics:m});
      } finally {await context.close();}
    }
    const responsive=await browser.newContext({viewport:{width:390,height:638},hasTouch:true});
    try {
      const page=await responsive.newPage();page.on('pageerror',e=>errors.push(e.message));
      await page.goto(base);await page.waitForFunction(()=>window.controls);await settle(page);
      await page.locator('#preview').evaluate(e=>e.scrollTop=200);await settle(page);
      assert((await metrics(page)).offset>0);
      await page.setViewportSize({width:1200,height:800});await settle(page);bounded(await metrics(page),false);
      near((await metrics(page)).offset,0,'desktop resize reveals header');
      await page.setViewportSize({width:390,height:638});await settle(page);bounded(await metrics(page),true);
      near((await metrics(page)).offset,0,'mobile resize resets offset');
      results.push({kind:'responsive',metrics:await metrics(page)});
    } finally {await responsive.close();}
    if(fs.existsSync(path.join(assets,'review-example.html')))for(const width of [390,1200])for(const mode of ['review','live']) {
      const context=await browser.newContext({viewport:{width,height:638},hasTouch:width===390});
      try {
        const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
        await page.goto(`${base}/runtime/review-example.html?test=1&mode=${mode}`);
        await page.locator('.dr-footer').waitFor();await settle(page);
        const m=await page.evaluate(()=>{
          const drawer=document.querySelector('.dr-footer').getBoundingClientRect(),preview=document.getElementById('preview');
          return {width:innerWidth,height:innerHeight,pageWidth:document.documentElement.scrollWidth,pageHeight:document.documentElement.scrollHeight,
            drawer:{top:drawer.top,bottom:drawer.bottom,width:drawer.width},previewHeight:preview.clientHeight,scrollHeight:preview.scrollHeight};
        });
        near(m.pageWidth,width,'example width');near(m.pageHeight,638,'example height');
        assert(m.drawer.top>=0 && m.drawer.bottom<=639,'example drawer reachable');
        assert(m.scrollHeight>m.previewHeight,'example preview scrolls');
        if(evidence && width===1200 && mode==='review')await page.screenshot({path:path.join(evidence,'example-desktop.png')});
        results.push({kind:'example',width,mode,metrics:m});
      } finally {await context.close();}
    }
    assert.deepEqual(errors,[],'browser errors');
    const report={browser:browser.version(),sandbox:true,cases:results.length,results,errors};
    if(evidence)fs.writeFileSync(path.join(evidence,'layout-results.json'),JSON.stringify(report,null,2)+'\n');
    console.log(`PASS: ${results.length} layout cases; scrolling, header, placement, themes and navigation resize; no browser errors.`);
  } finally {if(browser)await browser.close();await new Promise(r=>server.close(r));}
})().catch(error=>{console.error(error);process.exitCode=1;});
