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
    // Requested height and header behavior, including actual pointer gestures and
    // container-only resize: a wide viewport must not mask a squeezed header.
    for(const width of [390,1200])for(const theme of ['light','dark']) {
      const context=await browser.newContext({viewport:{width,height:800},hasTouch:width===390,colorScheme:theme});
      try {
        const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
        await page.goto(`${base}/runtime/review-example.html?test=1`);
        await page.locator('.dr-footer').waitFor();await settle(page);
        const drawer=page.locator('.dr-footer'),handle=page.locator('[data-dr=height-handle]');
        const collapsed=()=>drawer.evaluate(e=>e.classList.contains('dr-collapsed'));
        for(const height of [175,120,99,76]) {
          const box=await handle.boundingBox(),start=await drawer.evaluate(e=>e.offsetHeight);
          await page.mouse.move(box.x+box.width/2,box.y+4);await page.mouse.down();
          await page.mouse.move(box.x+box.width/2,box.y+4+start-height,{steps:5});await page.mouse.up();await settle(page);
          near(await drawer.evaluate(e=>e.offsetHeight),height,'continuous drawer height');
          assert.equal(await collapsed(),false,'drag never collapses');
          assert.equal(await page.locator('[data-dr=collapse]').getAttribute('aria-expanded'),'true');
        }
        await page.reload();await page.locator('.dr-footer').waitFor();await settle(page);
        near(await drawer.evaluate(e=>e.offsetHeight),76,'short height persists');
        await page.locator('[data-dr=collapse]').click();assert.equal(await collapsed(),true);
        await page.locator('[data-dr=collapse]').click();assert.equal(await collapsed(),false);
        near(await drawer.evaluate(e=>e.offsetHeight),76,'explicit collapse restores requested height');
        await handle.focus();await page.keyboard.press('Home');await settle(page);
        near(await drawer.evaluate(e=>e.offsetHeight),Number(await handle.getAttribute('aria-valuemin')),'minimum leaves toolbar reachable');
        assert.equal(await collapsed(),false,'Home resizes without collapsing');
        await page.keyboard.press('ArrowUp');await settle(page);
        assert.equal(await collapsed(),false);
        // The short expanded body remains scrollable to its actual actions.
        const panel=page.locator('.dr-footer-inner');
        assert(await panel.evaluate(e=>e.scrollHeight>e.clientHeight),'short panel scrolls');
        await page.locator('[data-dr=comment]').focus();await page.keyboard.type('Unsubmitted height check');
        await page.locator('[data-dr=commit-comment]').focus();await settle(page);
        const button=await page.locator('[data-dr=commit-comment]').boundingBox(),bounds=await drawer.boundingBox();
        assert(button.y>=bounds.y && button.y+button.height<=bounds.y+bounds.height,'keyboard reaches short-panel actions');
        await handle.focus();await page.keyboard.press('End');await settle(page);
        // Force both forms within this viewport. Every compact state has identical geometry.
        await page.locator('header').evaluate(e=>e.style.width='300px');await settle(page);
        for(const control of ['cycle-sides','cycle-themes']) {
          const button=page.locator(`[data-dr=${control}]`);assert(await button.isVisible());
          const initial=await button.boundingBox(),symbol=await button.locator('svg').innerHTML();
          const labels=new Set();
          for(let i=0;i<3;i++) {
            labels.add(await button.locator('.dr-choice-current').innerText());
            near((await button.boundingBox()).width,initial.width,'fixed compact width');
            assert.equal(await button.locator('svg').innerHTML(),symbol,'symbol identifies function, not state');
            await button.focus();await page.keyboard.press(i===1?'Space':'Enter');await settle(page);
          }
          assert.deepEqual([...labels].sort(),(control==='cycle-sides'?['Both','Current','New']:['Both','Dark','Light']).sort());
          assert.match(await button.getAttribute('aria-label'),/Switch to/);
        }
        if(evidence)await page.screenshot({path:path.join(evidence,`controls-${width}-${theme}.png`)});
        if(width===1200) {
          const header=page.locator('header');await header.evaluate(e=>e.style.width='1100px');await settle(page);
          assert.equal(await page.locator('[data-dr=cycle-sides]').isVisible(),false);
          assert.equal(await page.locator('[data-side=proposed]').innerText(),'New');
          // Step through the transition, checking that expanded selectors never wrap.
          let sawFull=false,sawCompact=false;
          for(let available=800;available>=320;available-=4) {
            await header.evaluate((e,w)=>e.style.width=w+'px',available);await settle(page);
            const compact=await page.locator('[data-dr=cycle-sides]').isVisible();
            assert.equal(await page.locator('[data-dr=cycle-themes]').isVisible(),compact,'selectors switch together');
            if(compact)sawCompact=true;else {
              sawFull=true;
              const rects=await header.evaluate(e=>[...e.children].map(c=>c.getBoundingClientRect().toJSON()));
              assert(rects[0].y<rects[1].bottom && rects[1].y<rects[0].bottom,'full controls remain on title row');
            }
          }
          assert(sawFull&&sawCompact,'container width crosses actual fit threshold');
          await page.locator('[data-dr=cycle-sides]').focus();
          await header.evaluate(e=>e.style.width='1100px');await settle(page);
          assert(await page.locator('[data-side][aria-pressed=true]').evaluate(e=>e===document.activeElement),'focus follows expanded selector');
          await header.evaluate(e=>e.style.width='320px');await settle(page);
          assert(await page.locator('[data-dr=cycle-sides]').evaluate(e=>e===document.activeElement),'focus follows compact selector');
          await header.evaluate(e=>{e.style.width='650px';e.querySelector('h1').textContent='A substantially longer review title';e.style.fontSize='24px';});await settle(page);
          assert(await page.locator('[data-dr=cycle-sides]').isVisible(),'title and enlarged text affect fit');
        }
        results.push({kind:'continuous-height-and-compact-controls',width,theme});
      } finally {await context.close();}
    }
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
