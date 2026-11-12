import {mountAnnotations, noteTone} from './design-annotations.js';
import {reviewContent,contentKey,deviceView,recoveryDiff} from './design-persistence.js';
import {createState,currentRecords,decide,approvalCurrent,exportReview,normalizeDesigns,syncOptionComment,needsTweaks} from './design-state.js';
export function icon(name) {
  const shapes={check:'<path d="m5 12 4 4 10-10"/>',eye:'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',comment:'<path d="M4 4h16v12H9l-5 4Z"/>',home:'<path d="m3 10 9-7 9 7M5 9v12h14V9M9 21v-8h6v8"/>',reopen:'<path d="M4 9a8 8 0 1 1 0 7M4 4v5h5"/>',history:'<path d="M4 9a8 8 0 1 1 0 7M4 4v5h5M12 7v5l3 2"/>',export:'<path d="M12 3v12m-4-4 4 4 4-4M5 16v5h14v-5"/>',dismiss:'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="m8 8 8 8m0-8-8 8"/>',previous:'<path d="m14 6-6 6 6 6"/>',next:'<path d="m10 6 6 6-6 6"/>',close:'<path d="m7 7 10 10M17 7 7 17"/>',tweaks:'<path d="M4 7h16M4 17h16M9 4v6m6 4v6"/>',detach:'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 15h16m-4-8h1v1"/>',dock:'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 15h16m-8-8v5m-2-2 2 2 2-2"/>',more:'<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',moon:'<path d="M20 14a8 8 0 0 1-10-10 8 8 0 1 0 10 10Z"/>',drag:'<path d="M8 6h.01M16 6h.01M8 12h.01M16 12h.01M8 18h.01M16 18h.01"/>'};
  return '<svg viewBox="0 0 24 24" aria-hidden="true">'+shapes[name]+'</svg>';
}
export function mountDesignFooter(root, {
  changes:packages, design, reviewId=location.pathname, reviewVersion=1,
  revisions=[], historyExamples=[], commentUpdates={}, initialReview, mode='review', persistence=null,
  headerHost=document.querySelector('[data-review-header]'),
  reviewArea=document.getElementById('preview'), onAppearance=()=>{}, onChange
}) {
  const changes = normalizeDesigns(packages, design);
  const pageControls=document.createElement('div');
  pageControls.className='dr-page-controls';
  pageControls.innerHTML=`
    <div class="theme-choices" role="group" aria-label="Design comparison" data-choice="sides">
      <button type="button" data-side="current">Current</button><button type="button" data-side="proposed">Proposed</button><button type="button" data-side="both">Both</button>
      <button type="button" class="dr-choice-cycle" data-dr="cycle-sides"></button>
    </div>
    <div class="theme-choices" role="group" aria-label="Preview themes" data-choice="previewThemes">
      <button type="button" data-preview-theme="light">Light</button><button type="button" data-preview-theme="dark">Dark</button><button type="button" data-preview-theme="both">Both</button>
      <button type="button" class="dr-choice-cycle" data-dr="cycle-themes"></button>
    </div>
    <button type="button" class="dr-icon" data-dr="theme"></button>`;
  if (headerHost) {headerHost.classList.add('dr-review-header');headerHost.append(pageControls);}
  else (reviewArea || root).before(pageControls);
  let dialogRoot=null,recoveryRoot=null;
  const $ = id => root.querySelector('[data-dr="'+id+'"]') || (dialogRoot?.dataset.dr===id ? dialogRoot : dialogRoot?.querySelector('[data-dr="'+id+'"]')) || recoveryRoot?.querySelector('[data-dr="'+id+'"]') || pageControls.querySelector('[data-dr="'+id+'"]');
  const test = new URLSearchParams(persistence?.search ?? location.search).get('test') === '1';
  const legacyExample = reviewId === 'shared-design-controls-example';
  const storageKey = (legacyExample ? 'design-review-example-v4' : 'design-review:'+reviewId) + (test ? '-test' : '');
  let saved=null, canSave=true, loadedRaw=null, storageError='';
  try {
    if(persistence) {
      saved=structuredClone(persistence.data);
      if(saved?.reviewId && saved.reviewId!==reviewId) throw new Error('This saved review belongs to a different example.');
      if(saved?.schemaVersion===4){
        if(saved.reviewVersion!==reviewVersion)throw new Error('This export belongs to another review version. Open its matching example to continue.');
        initialReview=saved;saved=null;
      }
    } else {
    const raw = loadedRaw = localStorage.getItem(storageKey);
    const suffix=test?'-test':'';
    const previous=legacyExample && !raw ? localStorage.getItem('design-review-example-v3'+suffix) ||
      localStorage.getItem('design-review-example-v1'+suffix) : null;
    saved=JSON.parse(raw || previous || 'null');
    }
    if(saved?.reviewVersion > reviewVersion) throw new Error('A newer revision is saved. Export edits from this older view before closing.');
  } catch(error) {
    if(persistence)throw error;
    canSave=false;
    storageError=persistence || saved?.reviewVersion > reviewVersion ? error.message : 'Storage unavailable. Export before closing.';
    if(saved?.reviewVersion > reviewVersion) saved=null;
  }
  const prior = revisions.filter(r => r.reviewId===reviewId && r.reviewVersion<reviewVersion)
    .sort((a,b)=>b.reviewVersion-a.reviewVersion)[0];
  const stateOptions={reviewId,reviewVersion,commentUpdates,previousReview:prior,initialReview};
  let state=createState(changes,persistence?reviewContent(saved):saved,stateOptions);
  if(persistence?.view)state=createState(changes,{...state,...persistence.view},stateOptions);
  let tab=state.tab || 'comments';
  const commentDrafts=new Map();
  let composerKey=null;
  let activeComment=null, general=false, gesture=null, saveTimer=null;
  const acknowledgedComments=new Map((persistence?.data?.comments || saved?.comments || initialReview?.comments || []).map(note=>[note.id,JSON.stringify(note)]));
  const pendingSaves=new Set(),saveStates=new Map();
  let sharedStatus=persistence?'Saved in Artifact Box':'';
  const mobile=matchMedia('(max-width:650px)'),system=matchMedia('(prefers-color-scheme:dark)');
  const headerLayout=headerHost?.parentElement?.matches('[data-review-layout]') &&
    reviewArea?.parentElement===headerHost.parentElement ? headerHost.parentElement : null;
  let headerOffset=0,headerHeight=0,previousScroll=0,scrollHeaderMobile=false;
  const headerScrollTop=()=>clamp(reviewArea.scrollTop,0,Math.max(0,reviewArea.scrollHeight-reviewArea.clientHeight));
  function paintHeaderOffset(){headerHost.style.setProperty('--dr-header-offset',headerOffset+'px');}
  function syncScrollHeader(){
    if(!headerLayout)return;
    const height=headerHost.getBoundingClientRect().height,wasHidden=headerHeight>0 && headerOffset===headerHeight;
    if(height!==headerHeight || mobile.matches!==scrollHeaderMobile){
      headerOffset=mobile.matches && scrollHeaderMobile ? (wasHidden?height:Math.min(headerOffset,height)) : 0;
      headerHeight=height;scrollHeaderMobile=mobile.matches;
      headerLayout.style.setProperty('--dr-header-height',height+'px');
      previousScroll=headerScrollTop();paintHeaderOffset();
    }
  }
  if(headerLayout){
    headerLayout.classList.add('dr-scroll-header-layout');reviewArea.setAttribute('data-review-scroll','');
    reviewArea.addEventListener('scroll',()=>{
      const position=headerScrollTop(),delta=position-previousScroll;previousScroll=position;
      if(!mobile.matches)return;
      headerOffset=position===0?0:clamp(headerOffset+delta,0,headerHeight);
      if(headerHost.contains(document.activeElement) && document.activeElement.matches(':focus-visible'))headerOffset=0;
      paintHeaderOffset();
    },{passive:true});
    headerHost.addEventListener('focusin',event=>{
      if(event.target.matches(':focus-visible')){headerOffset=0;paintHeaderOffset();}
    });
  }
  const headerChoices=[
    {key:'previewThemes',control:'cycle-themes',values:['light','dark','both'],symbol:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor"/></svg>'},
    {key:'sides',control:'cycle-sides',values:['current','proposed','both'],symbol:icon('eye')}
  ];
  function syncHeaderChoices(){
    for(const {key,control,values,symbol} of headerChoices){
      const button=$(control),value=state[key],next=values[(values.indexOf(value)+1)%values.length];
      const label=value[0].toUpperCase()+value.slice(1),nextLabel=next[0].toUpperCase()+next.slice(1);
      button.innerHTML=symbol+'<span>'+label+'</span>';
      button.setAttribute('aria-label',button.parentElement.getAttribute('aria-label')+': '+label+'. Switch to '+nextLabel);
      button.dataset.tooltip=button.getAttribute('aria-label');
    }
  }
  function fitPageHeader(){
    const host=headerHost || pageControls,focused=document.activeElement;
    // Measure the full controls and title on one line before choosing a compact form.
    // Use actual available space, including fonts and other host header content.
    host.classList.add('dr-header-measuring');
    for(const {control} of headerChoices)$(control).parentElement.classList.remove('dr-choice-compact');
    const compact=host.scrollWidth>host.clientWidth+1;
    for(const {control} of headerChoices)$(control).parentElement.classList.toggle('dr-choice-compact',compact);
    host.classList.remove('dr-header-measuring');
    if(pageControls.contains(focused) && !focused.getClientRects().length){
      const group=focused.closest('.theme-choices');
      (group?.classList.contains('dr-choice-compact')?group.querySelector('.dr-choice-cycle'):group?.querySelector('[aria-pressed=true]'))?.focus({preventScroll:true});
    }
    syncScrollHeader();
  }
  root.className='dr-footer';
  root.innerHTML=`
    <div class="dr-height-handle" data-dr="height-handle" role="separator" aria-label="Resize drawer height" aria-orientation="horizontal" tabindex="0"></div>
    <div class="dr-footer-inner">
      <div class="dr-navigation" data-dr="header">
        <button type="button" class="dr-icon dr-grip" data-dr="grip" aria-label="Move design controls" data-tooltip="Drag the header; arrow keys move the panel">${icon('drag')}</button>
        <div class="dr-view-tabs" role="tablist" aria-label="Design tool view">
          <button class="dr-icon" role="tab" data-tab="comments" aria-label="Comments" aria-controls="dr-comments">${icon('comment')}</button>
          <button class="dr-icon" role="tab" data-tab="parameters" aria-label="Design Controls" aria-controls="dr-parameters">${icon('tweaks')}</button>
        </div>
        <span class="dr-tool-title" data-dr="tab-title">Comments</span>
        <div class="dr-utilities" data-dr="utilities">
          <button type="button" class="dr-icon" data-dr="collapse" aria-label="Collapse drawer" aria-expanded="true"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
          <button type="button" class="dr-icon dr-placement" data-dr="detach" aria-label="Detach controls">${icon('detach')}</button>
          <button type="button" class="dr-icon" data-dr="history" aria-label="Review history" data-tooltip="Review history">${icon('history')}</button>
          <button type="button" class="dr-icon" data-dr="export-draft" aria-label="Export review" data-tooltip="Export review">${icon('export')}</button>
        </div>
        <div class="dr-menu-wrap" data-dr="overflow" hidden><button type="button" class="dr-icon" data-dr="more" aria-label="More actions" data-tooltip="More actions" aria-expanded="false">${icon('more')}</button><div class="dr-menu" data-dr="menu" role="group" aria-label="Overflow actions" hidden></div></div>
      </div>
      <div class="dr-selectors" data-dr="scope" aria-label="Review context">
          <div class="dr-selector"><label for="dr-package">Package</label><select id="dr-package" data-dr="package"></select></div>
          <div class="dr-selector"><label for="dr-variation">Variation</label><select id="dr-variation" data-dr="option"></select></div>
          <div class="dr-selector dr-state-selector"><label for="dr-state">State</label><select id="dr-state" data-dr="scene"></select></div>
      </div>
      <div class="dr-feedback" id="dr-comments" role="tabpanel" aria-label="Comments" data-dr="comments" hidden>
          <div class="dr-compose">
            <textarea data-dr="comment" placeholder="Write a comment…"></textarea>
            <div class="dr-compose-actions">
              <label class="dr-entire-review"><input type="checkbox" data-dr="entire-review"> Apply to entire review</label>
              <div class="dr-action-buttons">
                <div class="dr-actions" role="group" aria-label="Variation decision">
                  <button data-dr="approve">Approve</button><button data-dr="reject">Reject</button>
                  <button class="dr-icon dr-clear" data-dr="clear" aria-label="Clear decision">${icon('close')}</button>
                </div>
                <button class="dr-icon" data-dr="discard-comment" aria-label="Discard comment edit">${icon('close')}</button>
                <button class="dr-icon" data-dr="commit-comment" aria-label="Save drawer comment">${icon('check')}</button>
              </div>
            </div>
          </div>
          <div class="dr-save-state" data-dr="save-problem" role="status" aria-live="polite" hidden></div>
          <div class="dr-status" role="status"><span data-dr="decision"></span></div>
          <small data-dr="list-label"></small>
          <div class="dr-comments-list" data-dr="list" aria-label="All comments"></div>
      </div>
      <p class="dr-error" data-dr="notice" role="alert" hidden></p>
      <section class="dr-parameters" id="dr-parameters" data-dr="parameters" aria-label="Design Controls" hidden>
        <div class="dr-tweaks" data-dr="tweaks"></div>
        <div class="dr-parameter-status"><span class="dr-save-state" data-dr="parameters-save" role="status" aria-live="polite"></span><button type="button" data-dr="reset" data-tooltip="Restore this variation’s default parameters; keep comments and decisions">Reset parameters</button></div>
      </section>
    </div>
    <div class="dr-resize dr-nw" data-corner="nw" role="button" aria-roledescription="resize handle" aria-label="Resize controls from top left" data-tooltip="Drag this corner or use arrow keys to resize" tabindex="0"></div>
    <div class="dr-resize dr-ne" data-corner="ne" role="button" aria-roledescription="resize handle" aria-label="Resize controls from top right" data-tooltip="Drag this corner or use arrow keys to resize" tabindex="0"></div>
    <div class="dr-resize dr-sw" data-corner="sw" role="button" aria-roledescription="resize handle" aria-label="Resize controls from bottom left" data-tooltip="Drag this corner or use arrow keys to resize" tabindex="0"></div>
    <div class="dr-resize dr-se" data-corner="se" role="button" aria-roledescription="resize handle" aria-label="Resize controls from bottom right" data-tooltip="Drag this corner or use arrow keys to resize" tabindex="0"></div>
    <dialog class="dr-receipt" data-dr="receipt" aria-labelledby="dr-history-title">
      <div class="dr-dialog-header"><h2 id="dr-history-title" data-dr="receipt-title" tabindex="-1">Revision history</h2><button type="button" class="dr-icon" data-dr="close" aria-label="Close history">${icon('close')}</button></div>
      <div class="dr-dialog-body"><select data-dr="submission" aria-label="Review revision"></select>
      <button type="button" class="dr-recovery" data-dr="device-drafts" hidden>This device’s unsaved drafts</button>
      <p data-dr="receipt-note"></p><div data-dr="summary"></div></div>
    </dialog>`;
  // A dialog belongs to the viewport, independently of drawer sizing/clipping.
  dialogRoot=$('receipt');document.body.append(dialogRoot);
  if(persistence?.check){
    recoveryRoot=document.createElement('dialog');recoveryRoot.className='dr-receipt';recoveryRoot.setAttribute('aria-labelledby','dr-sync-title');
    recoveryRoot.innerHTML=`<div class="dr-dialog-header"><h2 id="dr-sync-title" data-dr="sync-title" tabindex="-1">Newer saved changes</h2><button class="dr-icon" type="button" data-dr="sync-close" aria-label="Close recovery">${icon('close')}</button></div>
      <div class="dr-dialog-body"><p data-dr="sync-message"></p><select data-dr="sync-draft" aria-label="This device’s recovery draft" hidden></select><div data-dr="sync-diff" hidden></div>
      <div class="dr-dialog-actions"><button type="button" data-dr="sync-continue">Continue latest saved review</button><button type="button" data-dr="sync-review">Review my unsaved changes</button><button type="button" data-dr="sync-back" hidden>Back</button><button type="button" data-dr="sync-export" hidden>Export this device’s draft</button></div></div>`;
    document.body.append(recoveryRoot);
  }
  $('header').insertBefore($('scope'),$('utilities'));
  // Native title delays are browser-controlled; these hints appear immediately.
  const tooltip=document.createElement('div');tooltip.className='dr-tooltip';tooltip.id='dr-tooltip';tooltip.setAttribute('role','tooltip');tooltip.hidden=true;document.body.append(tooltip);
  let tooltipTarget=null;
  function hideTooltip(){if(tooltipTarget)tooltipTarget.removeAttribute('aria-describedby');tooltipTarget=null;tooltip.hidden=true;}
  function showTooltip(target){
    if(!target||target.disabled)return;
    const text=target.dataset.tooltip||(target.classList.contains('dr-icon')?target.getAttribute('aria-label'):'');if(!text)return;
    hideTooltip();tooltipTarget=target;tooltip.textContent=text;tooltip.hidden=false;target.setAttribute('aria-describedby',tooltip.id);
    const box=target.getBoundingClientRect(),tip=tooltip.getBoundingClientRect();
    tooltip.style.left=Math.max(8,Math.min(innerWidth-tip.width-8,box.left+(box.width-tip.width)/2))+'px';
    tooltip.style.top=(box.top>=tip.height+12?box.top-tip.height-6:Math.min(innerHeight-tip.height-8,box.bottom+6))+'px';
  }
  for (const surface of [root,pageControls]) {
    surface.addEventListener('pointerover',e=>{if(e.pointerType==='touch')return;const target=e.target.closest('[data-tooltip],.dr-icon');if(target!==tooltipTarget){hideTooltip();showTooltip(target);}});
    surface.addEventListener('pointerout',e=>{if(tooltipTarget&&!tooltipTarget.contains(e.relatedTarget))hideTooltip();});
    surface.addEventListener('focusin',e=>showTooltip(e.target.closest('[data-tooltip],.dr-icon')));
    surface.addEventListener('focusout',hideTooltip);surface.addEventListener('pointerdown',hideTooltip);
    surface.addEventListener('keydown',e=>{if(e.key==='Escape')hideTooltip();});
  }
  window.addEventListener('resize',hideTooltip);document.addEventListener('scroll',hideTooltip,true);
  function notice(message='') {$('notice').textContent=message;$('notice').hidden=!message;}
  const saveKey=kind=>state.currentChangeId+':'+state.activeOptions[state.currentChangeId]+':'+kind;
  function renderSaveLine(line,text,recovery=false){
      line.textContent=text;
      if(recovery && persistence?.showRecovery){
        const link=document.createElement('button');link.type='button';link.className='dr-recovery';
        link.textContent='Recovery';link.setAttribute('aria-label','Open save and recovery details');
        link.title=storageError;
        link.addEventListener('click',()=>persistence.paused?showSyncDialog():persistence.showRecovery().catch(error=>notice(error.message)));
        line.append(' · ',link);
      }
  }
  function commentSaveText(note){
    if(acknowledgedComments.get(note.id)===JSON.stringify(note))return persistence?'Saved in Artifact Box':'Saved locally';
    return canSave?'Saving…':sharedStatus==='Save conflict'?'Save conflict':'Not saved';
  }
  function renderCommentSave(note,line){
    const text=commentSaveText(note);
    renderSaveLine(line,text,text==='Save conflict'||text==='Not saved');
  }
  function saveStatus(){
    const failure=persistence?.paused?'Newer changes available':sharedStatus==='Save conflict'?'Save conflict':'Not saved';
    renderSaveLine($('parameters-save'),!canSave ? failure : $('tweaks').querySelector('[aria-invalid=true]') ?
      'Invalid value · not saved' : pendingSaves.has(saveKey('parameters'))?'Saving…':sharedStatus || saveStates.get(saveKey('parameters')) || 'Saved locally',!canSave);
    $('save-problem').hidden=canSave || state.comments.some(note=>acknowledgedComments.get(note.id)!==JSON.stringify(note));
    if(!canSave)renderSaveLine($('save-problem'),failure,true);
    for(const line of $('list').querySelectorAll('[data-note-save]')){
      const note=state.comments.find(n=>n.id===line.dataset.noteSave);if(note)renderCommentSave(note,line);
    }
    annotations.refreshStatus();
  }
  function acknowledgeComments(notes){
    for(const note of notes)if(JSON.stringify(state.comments.find(n=>n.id===note.id))===JSON.stringify(note))acknowledgedComments.set(note.id,JSON.stringify(note));
    saveStatus();
  }
  function persist() {
    clearTimeout(saveTimer);saveTimer=null;
    if(persistence){
      persistence.saveView?.(deviceView(state))?.catch(error=>notice(error.message));
      if(!canSave){saveStatus();if(persistence.paused)void preserveDraft().catch(error=>notice(error.message));else if(!persistence.showRecovery)notice(storageError);return;}
      pendingSaves.clear();
      // The adapter snapshots synchronously, then acknowledges the shared save.
      const comments=structuredClone(state.comments);
      persistence.save(reviewContent(state)).then(saved=>acknowledgeComments(saved?.data?.comments || comments)).catch(async error=>{
        canSave=false;storageError=error.status===409 ?
          'Newer saved changes are available. Your changes remain on this device.' :
          'Shared save failed. Export your edits before reloading. '+error.message;
        saveStatus();status();if(!persistence.showRecovery)notice(storageError);
        if(error.status===409 && persistence.check){try{await persistence.check();}catch(cause){notice(cause.message);}}
      });
      return;
    }
    if(canSave)try{
      if(localStorage.getItem(storageKey)!==loadedRaw){
        canSave=false;
        storageError='Another tab changed this review. Export this draft before reloading.';
      }else{
        const raw=JSON.stringify(state);
        localStorage.setItem(storageKey,raw);
        loadedRaw=raw;
        for(const note of state.comments)acknowledgedComments.set(note.id,JSON.stringify(note));
      }
    }catch{canSave=false;storageError='Save failed. Draft is in memory; export before closing.';}
    for(const key of pendingSaves)saveStates.set(key,canSave?'Saved locally':'Save failed');pendingSaves.clear();saveStatus();if(!canSave)notice(storageError);
  }
  function scheduleSave(kind){const key=saveKey(kind);pendingSaves.add(key);saveStates.set(key,'Saving…');saveStatus();clearTimeout(saveTimer);saveTimer=setTimeout(persist,350);}
  window.addEventListener('pagehide',persist);
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden'&&pendingSaves.size)persist();});
  function theme() {
    const dark=state.appearance==='dark'||(!state.appearance&&system.matches);
    root.dataset.theme=dark?'dark':'light';
    dialogRoot.dataset.theme=root.dataset.theme;
    if(recoveryRoot)recoveryRoot.dataset.theme=root.dataset.theme;
    pageControls.dataset.theme=root.dataset.theme;tooltip.dataset.theme=root.dataset.theme;annotations.setTheme(root.dataset.theme);
    onAppearance(root.dataset.theme);
    $('theme').innerHTML=icon(dark?'moon':'sun');
    $('theme').setAttribute('aria-label',dark?'Switch interface to light theme':'Switch interface to dark theme');$('theme').dataset.tooltip=$('theme').getAttribute('aria-label');
  }
  const clamp=(n,min,max)=>Math.max(min,Math.min(Math.max(min,max),n));
  const minimumHeight=width=>width<622?240:150;
  const maximumDrawerHeight=()=>Math.max(160,innerHeight-(headerHost?.offsetHeight || 40)-80);
  function placement() {
    const floating=state.placement[mode]&&!mobile.matches;
    root.classList.toggle('dr-floating',floating);document.body.classList.toggle('dr-has-floating',floating);
    root.classList.toggle('dr-collapsed',!!state.drawerCollapsed);
    $('collapse').setAttribute('aria-label',state.drawerCollapsed?'Expand drawer':'Collapse drawer');
    $('collapse').setAttribute('aria-expanded',String(!state.drawerCollapsed));
    $('collapse').querySelector('path').setAttribute('d',state.drawerCollapsed?'m6 15 6-6 6 6':'m6 9 6 6 6-6');
    $('detach').innerHTML=icon(floating?'dock':'detach');$('detach').setAttribute('aria-label',floating?'Dock controls':'Detach controls');$('detach').dataset.tooltip=$('detach').getAttribute('aria-label');
    root.style.width=floating&&state.size?clamp(state.size.width,360,innerWidth-16)+'px':'';
    const width=floating&&state.size?clamp(state.size.width,360,innerWidth-16):Math.min(760,innerWidth-32);
    root.style.minHeight=floating&&!state.drawerCollapsed?minimumHeight(width)+'px':'';
    root.style.height=state.drawerCollapsed?'auto':floating?(state.size?clamp(state.size.height,minimumHeight(width),innerHeight-16)+'px':'min(300px,60dvh)'):
      clamp(state.drawerHeight || (mobile.matches?320:Math.min(280,132+48*state.comments.length)),minimumHeight(innerWidth),maximumDrawerHeight())+'px';
    $('height-handle').setAttribute('aria-valuemin','48');
    $('height-handle').setAttribute('aria-valuemax',String(Math.round(maximumDrawerHeight())));
    $('height-handle').setAttribute('aria-valuenow',String(Math.round(root.offsetHeight)));
    if(floating&&state.position) {
      root.style.left=clamp(state.position.x,8,innerWidth-root.offsetWidth-8)+'px';
      root.style.top=clamp(state.position.y,8,innerHeight-root.offsetHeight-8)+'px';root.style.right='auto';root.style.bottom='auto';
    }else{root.style.removeProperty('left');root.style.removeProperty('top');root.style.removeProperty('right');root.style.removeProperty('bottom');}
  }
  function status() {
    const {change,option,entry,draft}=currentRecords(state,changes),fresh=approvalCurrent(draft);
    let text=entry.decision==='rejected'?'Package dismissed':draft.decision==='rejected'?'Option dismissed':draft.decision==='approved'?!fresh?'Changed since approval · review needed':entry.selectedOptionId!==option.id?'Previously approved · another option chosen':needsTweaks(state,change.id,option.id)?'Chosen · required tweaks':'Chosen':'';
    if(text && persistence && sharedStatus!=='Saved in Artifact Box')text+=' · '+(canSave?'saving…':'not saved');
    if(general)text='Entire review · selected variation in each package';
    $('decision').textContent=text;$('decision').parentElement.hidden=!text;
    const targets=general?changes.map(c=>({entry:state.changes[c.id],id:state.activeOptions[c.id]})):[{entry,id:option.id}];
    $('approve').setAttribute('aria-pressed',String(targets.every(t=>approvalCurrent(t.entry.options[t.id])&&t.entry.selectedOptionId===t.id)));
    $('reject').setAttribute('aria-pressed',String(targets.every(t=>t.entry.options[t.id].decision==='rejected')));
    $('approve').disabled=!!$('tweaks').querySelector('[aria-invalid=true]');$('reject').disabled=false;
    $('clear').disabled=targets.every(t=>t.entry.options[t.id].decision==='undecided');
  }
  const colorHex=(control,value)=>control.presets?.find(([id])=>id===value)?.[2]||(/^#[0-9a-f]{6}$/i.test(value)?value:'#000000');
  function syncControl(control,value,source){
    const field=[...$('tweaks').children].find(el=>el.dataset.control===control.key);if(!field)return;
    field.querySelector('output').textContent=control.type==='number'?(control.unit||''):String(value)+(control.unit||'');
    if(control.type==='color'){
      const hex=colorHex(control,value);
      field.querySelectorAll('[data-color-input]').forEach(input=>{if(input!==source)input.value=hex;input.removeAttribute('aria-invalid');});
      field.querySelectorAll('[data-choice]').forEach(button=>button.setAttribute('aria-pressed',String(control.presets[Number(button.dataset.choice)][2].toLowerCase()===hex.toLowerCase())));
    }
    if(control.type==='segmented')field.querySelectorAll('[data-choice]').forEach(button=>button.setAttribute('aria-pressed',String(control.choices[Number(button.dataset.choice)][0]===value)));
  }
  function renderTweaks() {
    const {option,draft}=currentRecords(state,changes);$('tweaks').replaceChildren();
    for(const control of option.controls||[]) {
      const field=document.createElement('div');field.className='dr-tweak';field.dataset.control=control.key;field.setAttribute('role','group');field.setAttribute('aria-label',control.label);
      const name=document.createElement('span');name.textContent=control.label;
      const value=document.createElement('output');value.textContent=String(draft.tweaks[control.key])+(control.unit||'');field.append(name,value);
      const error=document.createElement('small');error.className='dr-field-error';error.hidden=true;error.setAttribute('role','alert');
      if(control.type==='color'||control.type==='segmented'){
        value.hidden=true;field.classList.add('dr-'+control.type);
        const choices=document.createElement('div');choices.className=control.type==='color'?'dr-swatches':'dr-segments';
        (control.presets||control.choices).forEach(([id,title,color],i)=>{const button=document.createElement('button');button.type='button';button.dataset.choice=i;button.setAttribute('aria-label',control.label+': '+title);button.dataset.tooltip=title+(color?' '+color:'');
          if(color){button.style.setProperty('--swatch',color);button.className='dr-swatch';}else button.textContent=title;
          choices.append(button);});field.append(choices);
        if(control.type==='color'){
          const custom=document.createElement('div');custom.className='dr-custom-color';
          const picker=document.createElement('input');picker.type='color';picker.dataset.tweak=control.key;picker.dataset.colorInput='picker';picker.setAttribute('aria-label','Custom '+control.label.toLowerCase()+' color');picker.dataset.tooltip='Choose any color';
          const hex=document.createElement('input');hex.type='text';hex.dataset.tweak=control.key;hex.dataset.colorInput='hex';hex.setAttribute('aria-label',control.label+' hex');hex.placeholder='#RRGGBB';hex.maxLength=7;hex.spellcheck=false;
          custom.append(picker,hex);field.append(custom);
        }
      }else{
        const input=document.createElement(control.type==='select'?'select':'input');input.dataset.tweak=control.key;
        if(control.type==='select'){for(const [id,text] of control.choices){const item=document.createElement('option');item.value=id;item.textContent=text;input.append(item);}input.value=draft.tweaks[control.key];value.hidden=true;}
        else if(control.type==='checkbox'){input.type='checkbox';input.checked=Boolean(draft.tweaks[control.key]);value.hidden=true;}
        else if(control.type==='text'){input.type='text';input.value=draft.tweaks[control.key];input.required=!!control.required;if(control.maxLength)input.maxLength=control.maxLength;value.hidden=true;}
        else{input.type=control.type==='number'?'number':'range';input.min=control.min;input.max=control.max;input.step=control.step||1;input.value=draft.tweaks[control.key];if(control.type==='number')value.textContent=control.unit||'';}
        input.setAttribute('aria-label',control.label);field.append(input);
      }
      field.append(error);$('tweaks').append(field);syncControl(control,draft.tweaks[control.key]);
    }
    $('reset').disabled=JSON.stringify(draft.tweaks)===JSON.stringify(option.defaults);
  }
  function refresh({inputs=true,preview=true,save=true}={}) {
    const {change,option,draft,entry}=currentRecords(state,changes);
    $('package').replaceChildren(...changes.map((c,i)=>{const o=document.createElement('option');o.value=c.id;o.textContent=(i+1)+'/'+changes.length+' '+c.title;return o;}));$('package').value=change.id;
    $('scene').replaceChildren(...change.scenes.map(([value,label])=>{const o=document.createElement('option');o.value=value;o.textContent=label;return o;}));$('scene').value=state.scene;
    for(const button of pageControls.querySelectorAll('[data-side]')) button.setAttribute('aria-pressed',String(button.dataset.side===state.sides));
    for(const button of pageControls.querySelectorAll('[data-preview-theme]')) button.setAttribute('aria-pressed',String(button.dataset.previewTheme===state.previewThemes));
    syncHeaderChoices();
    $('option').replaceChildren(...change.options.map((o,i)=>{const item=document.createElement('option');item.value=o.id;const d=state.changes[change.id].options[o.id];item.textContent=(i+1)+'. '+o.title+(d.decision==='rejected'?' · Dismissed':state.changes[change.id].selectedOptionId===o.id?' · Chosen':'');return item;}));$('option').value=option.id;
    if(inputs) renderTweaks();
    renderPanels();
    status();theme();if(save)persist();else saveStatus();placement();if(preview){onChange({state,change,option,draft,entry,mode});annotations.render();}fitPageHeader();
  }
  function changeTo(id) {
    const change=changes.find(c=>c.id===id);
    if(!change) return;
    resetEditor();persist();state.currentChangeId=id;
    const remembered=state.scenes[id];
    state.scene=change.scenes.some(([key])=>key===remembered) ? remembered : change.scenes[0][0];
    state.version++;notice();refresh();reviewArea?.scrollTo(0,0);
  }
  function optionTo(id){resetEditor();persist();state.activeOptions[state.currentChangeId]=id;state.version++;notice();refresh();}
  $('package').onchange=e=>changeTo(e.target.value);
  $('option').onchange=e=>optionTo(e.target.value);
  function sceneTo(value){resetEditor();state.scene=value;state.scenes[state.currentChangeId]=value;refresh({inputs:false});}
  $('scene').onchange=e=>sceneTo(e.target.value);
  for(const button of pageControls.querySelectorAll('[data-side]')) button.onclick=()=>{
    state.sides=button.dataset.side;
    refresh({inputs:false});
  };
  for(const button of pageControls.querySelectorAll('[data-preview-theme]')) button.onclick=()=>{
    state.previewThemes=button.dataset.previewTheme;
    refresh({inputs:false});
  };
  for(const {key,control,values} of headerChoices)$(control).onclick=()=>{
    hideTooltip();state[key]=values[(values.indexOf(state[key])+1)%values.length];refresh({inputs:false});
  };
  const tabs = [...root.querySelectorAll('[data-tab]')];
  for(const button of tabs) button.onclick=()=>openTab(button.dataset.tab);
  root.querySelector('[role=tablist]').onkeydown=e=>{
    const items=tabs.filter(t=>!t.hidden),index=items.indexOf(e.target);
    if(index<0 || !['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
    e.preventDefault();
    const next=e.key==='Home'?0:e.key==='End'?items.length-1:(index+(e.key==='ArrowLeft'?-1:1)+items.length)%items.length;
    items[next].click();items[next].focus();
  };
  function openTab(name){
    tab=name;state.drawerCollapsed=false;placement();
    renderPanels();
    persist();
  }
  function renderPanels(){
    const {change,option}=currentRecords(state,changes);
    tabs[1].hidden=!option.controls.length;
    if(!tabs.some(t=>!t.hidden && t.dataset.tab===tab)) tab='comments';
    state.tab=tab;
    $('tab-title').textContent=tab==='parameters'?'Design Controls':'Comments';
    for(const button of tabs){
      const selected=button.dataset.tab===tab;
      button.tabIndex=selected?0:-1;
      button.setAttribute('aria-selected',String(selected));
      $(button.dataset.tab).hidden=!selected;
    }
    const counts=[changes.length,change.options.length,change.scenes.length];
    [...$('scope').children].forEach((row,i)=>row.hidden=counts[i]<=1);
    $('scope').hidden=counts.every(count=>count<=1);
    root.dataset.tab=tab;
    if(tab==='comments') renderComments();
  }
  $('detach').onclick=()=>{state.placement[mode]=!root.classList.contains('dr-floating');refresh({preview:false});};
  $('collapse').onclick=()=>{state.drawerCollapsed=!state.drawerCollapsed;placement();persist();};
  $('theme').onclick=()=>{hideTooltip();state.appearance=root.dataset.theme==='dark'?'light':'dark';refresh({inputs:false,preview:false});};
  function scopeLabel(){
    const {change,option}=currentRecords(state,changes);
    const scene=change.scenes.find(([id])=>id===state.scene);
    return [change.title, option.title!==change.title && option.title, scene?.[1]].filter(Boolean).join(' · ') || 'Design';
  }
  function resetScope(){general=false;$('entire-review').checked=false;}
  function resetEditor(){activeComment=null;resetScope();annotations.close();}
  function draftKey(){
    return JSON.stringify(activeComment ? ['edit',activeComment] :
      ['scope',state.currentChangeId,state.activeOptions[state.currentChangeId],state.scene]);
  }
  function syncComposer(){
    const text=$('comment').value;
    $('commit-comment').disabled=!text.trim();
    $('discard-comment').disabled=!text && !activeComment;
    saveStatus();
  }
  function renderComments(){
    const note=state.comments.find(c=>c.id===activeComment);
    const key=draftKey();
    if(composerKey!==key){
      $('comment').value=commentDrafts.get(key) ?? note?.text ?? '';
      composerKey=key;
    }
    syncComposer();
    $('entire-review').checked=general;
    $('comment').setAttribute('aria-label','Comment on '+(general?'entire review':scopeLabel()));
    renderList();
  }
  function renderList(){
    $('list').replaceChildren();
    const notes=state.comments.filter(c=>c.text.trim()).slice().reverse();
    $('list-label').textContent=notes.length ? 'All comments ('+notes.length+')' : '';
    for(const note of notes){
      const row=document.createElement('article');row.className='dr-note';
      row.setAttribute('aria-current', String(note.id===activeComment));
      const button=document.createElement('button');button.type='button';button.className='dr-note-open';
      const label=document.createElement('small');label.textContent=note.label+' · '+note.status;
      const body=document.createElement('span');body.textContent=note.text;
      button.append(label,body);
      if(note.quote) {row.dataset.tone=noteTone(note);const quote=document.createElement('q');quote.textContent=note.quote;button.append(quote);}
      if(note.reply) {const reply=document.createElement('small');reply.textContent='Reply: '+note.reply;button.append(reply);}
      button.onclick=()=>visitComment(note);
      const saved=document.createElement('div');saved.className='dr-save-state';saved.dataset.noteSave=note.id;saved.setAttribute('role','status');
      renderCommentSave(note,saved);row.append(button,saved);$('list').append(row);
    }
  }
  function visitComment(note){
    if(!note.packageId){
      resetEditor();general=true;activeComment=note.id;openTab('comments');status();$('comment').focus();return;
    }
    const change=changes.find(c=>c.id===note.packageId);
    if(!change || !change.options.some(o=>o.id===note.variationId) ||
       (note.stateId && !change.scenes.some(([id])=>id===note.stateId))){
      notice('This comment belongs to an earlier design. Open revision history to see its context.');
      return;
    }
    persist();
    state.currentChangeId=change.id;
    state.activeOptions[change.id]=note.variationId;
    state.scene=note.stateId || state.scenes[change.id] || change.scenes[0][0];
    state.scenes[change.id]=state.scene;
    if(note.theme && state.previewThemes!=='both') state.previewThemes=note.theme;
    if(note.side && state.sides!=='both') state.sides=note.side;
    activeComment=note.quote?null:note.id;
    general=false;tab='comments';state.drawerCollapsed=false;notice();refresh();
    if(note.quote){
      if(!annotations.reveal(note)) notice('The quoted text is no longer identifiable in this preview.');
      return;
    }
    if(note.side && reviewArea){
      const column=[...reviewArea.querySelectorAll('[data-reference]')].find(el=>
        el.dataset.reference===(note.side==='current'?'current':'proposal') && el.dataset.theme===note.theme);
      column?.scrollIntoView({block:'nearest',inline:'nearest'});
    }
    $('comment').focus({preventScroll:true});
  }

  $('entire-review').onchange=e=>{
    general=e.target.checked;
    $('comment').setAttribute('aria-label','Comment on '+(general?'entire review':scopeLabel()));
    status();
  };
  function scopedFields(){
    const {change,option}=currentRecords(state,changes);
    return {packageId:change.id,variationId:option.id,stateId:state.scene,label:scopeLabel(),reviewVersion};
  }
  function storeComment(note,text,{save=true}={}){
    const fresh=!state.comments.includes(note);
    note.text=text;
    note.status='open';
    if(fresh)state.comments.push(note);
    syncOptionComment(state,note);
    state.version++;status();renderList();
    if(save)persist();
    if(fresh)$('list').scrollTop=0;
  }
  $('comment').oninput=()=>{
    commentDrafts.set(draftKey(),$('comment').value);
    syncComposer();
  };
  function clearComposer(){
    commentDrafts.delete(draftKey());
    activeComment=null;resetScope();composerKey=draftKey();$('comment').value='';
    renderComments();
    status();
    $('comment').focus();
  }
  $('discard-comment').onclick=clearComposer;
  function commitComposer(save=true){
    const text=$('comment').value.trim();
    if(!text)return;
    const scope=general ? {packageId:null,variationId:null,stateId:null,label:'Entire review',reviewVersion} : scopedFields();
    const existing=state.comments.find(c=>c.id===activeComment);
    const note=existing || {...scope,id:crypto.randomUUID()};
    if(existing){const oldScope={...existing};Object.assign(note,scope);syncOptionComment(state,oldScope);}
    storeComment(note,text,{save});
    clearComposer();
  }
  $('commit-comment').onclick=()=>commitComposer();
  $('comment').onkeydown=e=>{
    if(e.key==='Escape'){e.preventDefault();clearComposer();}
    if((e.ctrlKey || e.metaKey) && e.key==='Enter'){e.preventDefault();$('commit-comment').click();}
  };
  const annotations=mountAnnotations({
    area:reviewArea,drawer:root,notes:()=>state.comments,context:scopedFields,
    saveText:commentSaveText,renderSave:renderCommentSave,
    save:edit=>{
      const existing=state.comments.find(c=>c.id===edit.id);
      storeComment(existing || edit,edit.text);
    }
  });
  let newest=null,comparisonCopies=[];
  function draftSnapshot(){
    return {...reviewContent(state),uiDrafts:{comments:[...commentDrafts],inline:annotations.drafts(),parameters:[...$('tweaks').querySelectorAll('[aria-invalid=true]')].map(input=>({key:input.dataset.tweak,value:input.value}))}};
  }
  function hasUnsubmitted(){return [...commentDrafts.values()].some(text=>text.trim()) || annotations.drafts().some(edit=>edit.text.trim()) || !!$('tweaks').querySelector('[aria-invalid=true]');}
  function hasUnsaved(latest){return hasUnsubmitted() || contentKey(state)!==contentKey(persistence.data) && contentKey(state)!==contentKey(latest);}
  async function preserveDraft(){await persistence.captureRecovery(draftSnapshot());}
  function pendingCopies(latest){return persistence.recoveries.filter(record=>!persistence.isAcknowledged(record) && (contentKey(record.data)!==contentKey(latest) || recoveryDiff(record.data,latest).length));}
  function renderComparison(){
    const copy=comparisonCopies[Number($('sync-draft').value)||0];
    const rows=copy?recoveryDiff(copy.data,newest?.data ?? persistence.data):[];
    $('sync-diff').replaceChildren();
    if(!rows.length){const p=document.createElement('p');p.textContent='No review-content differences are visible. This copy may contain older view settings or review metadata. The export retains the complete draft.';$('sync-diff').append(p);}
    for(const row of rows){const section=document.createElement('section'),heading=document.createElement('h3'),body=document.createElement('p');heading.textContent=row.label;body.textContent=row.text;section.append(heading,body);$('sync-diff').append(section);}
    $('sync-export').disabled=!copy;
  }
  function showSyncDialog(review=false){
    if(!recoveryRoot)return;
    if(dialogRoot.open)dialogRoot.close();
    comparisonCopies=[...persistence.recoveries].sort((a,b)=>String(b.updatedAt).localeCompare(String(a.updatedAt)));
    $('sync-title').textContent=review?'This device’s unsaved changes':newest?'Newer saved changes':'Unsaved changes on this device';
    $('sync-message').textContent=review?'Review these differences before choosing what to keep. Exporting preserves this device’s draft for follow-up.':'The latest saved review is available. This device’s unsaved copies will remain available in History.';
    $('sync-draft').replaceChildren(...comparisonCopies.map((record,i)=>new Option((record.updatedAt?new Date(record.updatedAt).toLocaleString():'This device')+(record.recoveryOnly?' · Includes unsubmitted edits':''),String(i))));
    $('sync-draft').hidden=!review || comparisonCopies.length<2;
    $('sync-diff').hidden=!review;$('sync-review').hidden=review;$('sync-back').hidden=!review;$('sync-export').hidden=!review;
    if(review)renderComparison();
    if(!recoveryRoot.open)recoveryRoot.showModal();$('sync-title').focus();
  }
  async function continueLatest(){
    const button=$('sync-continue');if(button?.disabled)return;
    if(button)button.disabled=true;
    const focused=document.activeElement;
    root.inert=true;pageControls.inert=true;if(reviewArea)reviewArea.inert=true;
    try{
      if(hasUnsaved(newest?.data ?? persistence.data))await preserveDraft();
      const data=await persistence.continueLatest();
      if(data?.reviewVersion>reviewVersion || data?.reviewId && data.reviewId!==reviewId){canSave=false;storageError='Open the matching current review version before continuing. This device’s drafts remain preserved.';saveStatus();throw new Error(storageError);}
      const view=deviceView(state);
      state=createState(changes,data,stateOptions);state=createState(changes,{...state,...view},stateOptions);tab=state.tab || 'comments';
      commentDrafts.clear();annotations.clearDrafts();composerKey=null;activeComment=null;resetScope();
      pendingSaves.clear();saveStates.clear();acknowledgedComments.clear();
      for(const note of data?.comments || [])acknowledgedComments.set(note.id,JSON.stringify(note));
      canSave=true;sharedStatus='Saved in Artifact Box';storageError='';notice();
      if(recoveryRoot?.open)recoveryRoot.close();
      refresh({save:false});
    }catch(error){if(recoveryRoot?.open)$('sync-message').textContent=error.message;else notice(error.message);throw error;}
    finally{if(button)button.disabled=false;root.inert=false;pageControls.inert=false;if(reviewArea)reviewArea.inert=false;if(focused?.isConnected && (root.contains(focused)||pageControls.contains(focused)))focused.focus({preventScroll:true});}
  }
  async function receiveLatest(head){
    newest=head;clearTimeout(saveTimer);saveTimer=null;
    if(hasUnsaved(head.data)){
      canSave=false;sharedStatus='Newer changes available';storageError='Your unsaved changes are preserved on this device.';
      let captureError;try{await preserveDraft();}catch(error){captureError=error;}
      saveStatus();showSyncDialog();if(captureError)$('sync-message').textContent='Recovery storage is unavailable. Export this device’s draft before leaving. '+captureError.message;
    }else if(pendingCopies(head.data).length){showSyncDialog();}
    else await continueLatest();
  }
  if(recoveryRoot){
    $('sync-close').onclick=()=>recoveryRoot.close();
    $('sync-review').onclick=()=>showSyncDialog(true);$('sync-back').onclick=()=>showSyncDialog();
    $('sync-draft').onchange=renderComparison;
    $('sync-continue').onclick=()=>{void continueLatest().catch(()=>{});};
    $('device-drafts').onclick=()=>showSyncDialog(true);
    $('sync-export').onclick=()=>{
      const copy=comparisonCopies[Number($('sync-draft').value)||0];if(!copy)return;
      const payload={...copy.data,recovery:{kind:'This device’s unconfirmed draft',updatedAt:copy.updatedAt,version:copy.version}};
      const json=JSON.stringify(payload,null,2)+'\n';
      let fallback=$('sync-diff').querySelector('[data-recovery-json]');
      if(!fallback){fallback=document.createElement('details');fallback.dataset.recoveryJson='';const title=document.createElement('summary');title.textContent='Copy draft JSON';const text=document.createElement('textarea');text.readOnly=true;text.rows=6;text.setAttribute('aria-label','Draft JSON');fallback.append(title,text);$('sync-diff').append(fallback);}
      fallback.open=true;fallback.querySelector('textarea').value=json;
      const url=URL.createObjectURL(new Blob([json],{type:'application/json'}));
      const link=document.createElement('a');link.href=url;link.download=reviewId+'-unsaved-device-draft.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    };
  }
  function setTweak(control,value,source){
    const {draft}=currentRecords(state,changes);draft.tweaks[control.key]=value;state.version++;
    const field=[...$('tweaks').children].find(el=>el.dataset.control===control.key);field.querySelector('.dr-field-error').hidden=true;
    syncControl(control,value,source);refresh({inputs:false,save:false});$('reset').disabled=JSON.stringify(draft.tweaks)===JSON.stringify(currentRecords(state,changes).option.defaults);scheduleSave('parameters');
  }
  $('tweaks').oninput=e=>{
    const key=e.target.dataset.tweak;if(!key)return;const control=currentRecords(state,changes).option.controls.find(c=>c.key===key),input=e.target;
    let value=input.value,message='';
    if(control.type==='color'){
      if(!/^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(value))message='Use #RGB or #RRGGBB.';
      else value=(value.length===4?'#'+[...value.slice(1)].map(c=>c+c).join(''):value).toLowerCase();
    }else if(control.type==='checkbox')value=input.checked;
    else if(control.type==='range'||control.type==='number'){value=Number(value);if(input.value===''||!Number.isFinite(value)||!input.checkValidity())message='Enter '+control.min+'–'+control.max+(control.unit||'')+'.';}
    else if(control.type==='text'&&input.required&&!value.trim())message='Enter a label.';
    const error=input.closest('[data-control]').querySelector('.dr-field-error');input.setAttribute('aria-invalid',String(!!message));error.textContent=message;error.hidden=!message;
    if(message){saveStatus();status();return;}setTweak(control,value,input);
  };
  $('tweaks').onclick=e=>{const button=e.target.closest('[data-choice]');if(!button)return;const control=currentRecords(state,changes).option.controls.find(c=>c.key===button.closest('[data-control]').dataset.control);const choice=(control.presets||control.choices)[Number(button.dataset.choice)];setTweak(control,control.type==='color'?choice[2]:choice[0]);};
  $('reset').onclick=()=>{const {option,draft}=currentRecords(state,changes);draft.tweaks=structuredClone(option.defaults);state.version++;refresh({save:false});scheduleSave('parameters');};
  for(const [button,decision] of [['approve','approved'],['reject','rejected'],['clear','undecided']])$(button).onclick=()=>{
    const targets=general?changes.map(c=>[c.id,state.activeOptions[c.id]]):[[state.currentChangeId,state.activeOptions[state.currentChangeId]]];
    if(button!=='clear' && $('comment').value.trim())commitComposer(false);
    for(const [changeId,optionId] of targets)decide(state,changeId,optionId,decision);
    resetScope();notice();refresh({inputs:false,preview:false});
  };
  $('more').onclick=()=>{const open=$('menu').hidden;$('menu').classList.toggle('dr-menu-below',$('more').getBoundingClientRect().top<60);$('menu').hidden=!open;$('more').setAttribute('aria-expanded',String(open));};
  function closeMenu(){$('menu').hidden=true;$('more').setAttribute('aria-expanded','false');}
  root.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('menu').hidden){closeMenu();$('more').focus();}});
  function historyEntries(){
    return [
      ...historyExamples.map((data,i)=>({label:'Example revision '+(data.reviewVersion || i+1),data,example:true})),
      ...state.submissions.map((data,i)=>({label:data.reviewVersion?'Local revision '+data.reviewVersion:data.legacyDraft?'Previous working draft':'Previous snapshot '+(i+1),data})),
      ...revisions.map(data=>({label:'Revision '+data.reviewVersion,data})),
      {label:'Current revision '+reviewVersion,data:exportReview(state,changes)}
    ];
  }
  let entries=[];
  function showRevision(index){
    const {data,example}=entries[index];
    $('receipt-note').textContent=example?'Fictional example history':'Read-only review record';
    $('summary').replaceChildren();
    const add=(tag,text)=>{const el=document.createElement(tag);el.textContent=text;$('summary').append(el);};
    for(const change of data.changes || []){
      add('h3',change.title || 'Design');
      for(const option of change.options){
        const details=document.createElement('details'),summary=document.createElement('summary'),values=document.createElement('pre');
        summary.textContent=[option.title,option.decision].filter(Boolean).join(' · ');
        values.textContent=JSON.stringify(option.tweaks,null,2);
        details.append(summary,values);$('summary').append(details);
        if(!data.comments?.length && option.comment) add('p',option.comment);
      }
    }
    for(const note of data.comments || []){
      add('h4',note.label+' · '+note.status);
      if(note.quote)add('q',note.quote);
      add('p',note.text);if(note.reply)add('p',note.reply);
    }
  }
  $('history').onclick=()=>{
    $('device-drafts').hidden=!persistence?.recoveries?.length;
    entries=historyEntries();
    $('submission').replaceChildren(...entries.map((entry,i)=>new Option(entry.label,String(i))));
    const index=entries.length-1;
    $('submission').selectedIndex=index;
    showRevision(index);closeMenu();hideTooltip();$('receipt').showModal();$('receipt-title').focus();
  };
  $('submission').onchange=e=>showRevision(Number(e.target.value));
  $('close').onclick=()=>$('receipt').close();
  $('export-draft').onclick=()=>{
    if($('tweaks').querySelector('[aria-invalid=true]')){
      openTab('parameters');notice('Correct invalid parameter values before exporting.');return;
    }
    persist();closeMenu();
    const payload=exportReview(state,changes);
    payload.exportedAt=new Date().toISOString();
    const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)+'\n'],{type:'application/json'}));
    const link=document.createElement('a');link.href=url;
    link.download=reviewId+'-v'+reviewVersion+'.json';link.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  };
  function moveTo(x,y){state.position={x:clamp(x,8,innerWidth-root.offsetWidth-8),y:clamp(y,8,innerHeight-root.offsetHeight-8)};placement();}
  function resizeTo(corner,dx,dy,box) {
    const west=corner.includes('w'),north=corner.includes('n');
    const width=clamp(box.width+(west?-dx:dx),360,west?box.right-8:innerWidth-box.left-8);
    const height=clamp(box.height+(north?-dy:dy),minimumHeight(width),north?box.bottom-8:innerHeight-box.top-8);
    state.size={width,height};state.position={x:west?box.right-width:box.left,y:north?box.bottom-height:box.top};placement();
  }
  function resizeDrawer(height){
    state.drawerCollapsed=height<100;
    if(!state.drawerCollapsed)state.drawerHeight=clamp(height,minimumHeight(innerWidth),maximumDrawerHeight());
    placement();
  }
  root.addEventListener('pointerdown',e=>{
    if(e.button!==0)return;
    if(e.target===$('height-handle')&&!root.classList.contains('dr-floating')){
      e.preventDefault();gesture={dock:true,y:e.clientY,height:root.offsetHeight};root.setPointerCapture(e.pointerId);return;
    }
    if(!root.classList.contains('dr-floating'))return;
    const corner=e.target.closest('[data-corner]')?.dataset.corner;
    const box=root.getBoundingClientRect();
    const inHeader=e.clientY>=box.top && e.clientY<=$('header').getBoundingClientRect().bottom;
    if(!corner && (!inHeader || e.target.closest('select,textarea,input,a,button:not([data-dr="grip"])')))return;
    e.preventDefault();
    gesture={corner,x:e.clientX,y:e.clientY,box};root.setPointerCapture(e.pointerId);
  });
  root.addEventListener('pointermove',e=>{if(!gesture)return;if(gesture.dock){resizeDrawer(gesture.height+gesture.y-e.clientY);return;}const {corner,x,y,box}=gesture,dx=e.clientX-x,dy=e.clientY-y;if(corner)resizeTo(corner,dx,dy,box);else moveTo(box.x+dx,box.y+dy);});
  root.addEventListener('pointerup',()=>{if(gesture){gesture=null;persist();}});
  root.addEventListener('pointercancel',()=>{gesture=null;persist();});
  root.addEventListener('keydown',e=>{
    if(e.target===$('height-handle')){
      const height={ArrowUp:root.offsetHeight+24,ArrowDown:root.offsetHeight-24,Home:48,End:maximumDrawerHeight()}[e.key];
      if(height!==undefined){e.preventDefault();resizeDrawer(height);persist();}return;
    }
    const corner=e.target.dataset.corner,isGrip=e.target===$('grip');
    if((!corner&&!isGrip)||!root.classList.contains('dr-floating'))return;
    const delta={ArrowLeft:[-16,0],ArrowRight:[16,0],ArrowUp:[0,-16],ArrowDown:[0,16]}[e.key];if(!delta)return;e.preventDefault();
    const box=root.getBoundingClientRect();if(corner)resizeTo(corner,...delta,box);else moveTo(box.x+delta[0],box.y+delta[1]);persist();
  });
  mobile.addEventListener('change',()=>refresh({preview:false}));system.addEventListener('change',()=>{if(!state.appearance)refresh({inputs:false});});window.addEventListener('resize',placement);
  const utilityButtons=['collapse','detach','history','export-draft'].map(id=>$(id));
  if(persistence){
    persistence.onStatus(message=>{sharedStatus=message;saveStatus();status();});
    persistence.beforeLeave(()=>{persist();return persistence.flush();});
    if(persistence.check){
      persistence.onUpdate(receiveLatest);
      let lastCheck=0;
      const check=()=>{if(document.visibilityState!=='hidden' && !recoveryRoot.open && !dialogRoot.open){lastCheck=Date.now();void persistence.check().catch(error=>notice('Could not check newer changes. '+error.message));}};
      window.addEventListener('focus',check);document.addEventListener('visibilitychange',check);
      window.addEventListener('pageshow',check);
      // Embedded browsers do not always forward a window-focus transition.
      // The first interaction is a fallback, without polling in the background.
      document.addEventListener('pointerdown',()=>{if(Date.now()-lastCheck>1000)check();},true);
      document.addEventListener('focusin',()=>{if(Date.now()-lastCheck>1000)check();},true);
      queueMicrotask(async()=>{
        try{
          await persistence.check();
          if(pendingCopies(persistence.data).length && !recoveryRoot.open)showSyncDialog();
        }catch(error){notice(error.message);}
      });
    }
  }
  function fitToolbar(){
    const header=$('header');closeMenu();$('utilities').append(...utilityButtons);$('overflow').hidden=true;
    root.classList.toggle('dr-compact',root.clientWidth-parseFloat(getComputedStyle(root).paddingLeft)-parseFloat(getComputedStyle(root).paddingRight)<=600);
    while(header.scrollWidth>header.clientWidth+1){const visible=[...$('utilities').children].filter(b=>b.offsetWidth);if(!visible.length)break;$('menu').prepend(visible.at(-1));$('overflow').hidden=false;}
  }
  new ResizeObserver(fitToolbar).observe(root);
  const headerObserver=new ResizeObserver(fitPageHeader);
  headerObserver.observe(headerHost || pageControls);
  if(headerHost)for(const child of headerHost.children)headerObserver.observe(child);
  document.fonts?.ready.then(fitPageHeader);
  refresh();fitToolbar();
  function updateView(values) {
    const {change}=currentRecords(state,changes);
    const scene=change.scenes.some(([id])=>id===values.scene) ? values.scene : state.scene;
    if(scene!==state.scene) resetEditor();
    Object.assign(state,values,{scene});
    state.scenes[change.id]=scene;
    refresh({inputs:false});
  }
  return {getContext:()=>currentRecords(state,changes),changeTo,updateView,render:()=>refresh({inputs:false})};
}
