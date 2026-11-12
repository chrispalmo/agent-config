// A quote belongs to one preview pane. Text offsets disambiguate repeated words;
// surrounding text lets it survive small edits that move it within that pane.
function textIndex(pane) {
  const walker = document.createTreeWalker(pane, NodeFilter.SHOW_TEXT);
  const nodes = [];
  let text = '';
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    nodes.push({node, start:text.length});
    text += node.data;
  }
  return {nodes, text};
}

function locate(pane, note) {
  const {text, nodes} = textIndex(pane);
  const {quote, anchor} = note;
  let start = text.indexOf(quote);
  if (start < 0) return null;
  if (anchor?.repeated || text.indexOf(quote, start + 1) >= 0) {
    const matches = [];
    while (start >= 0) {
      const end = start + quote.length;
      if (anchor && text.slice(0,start).endsWith(anchor.before) && text.slice(end).startsWith(anchor.after)) {
        matches.push(start);
      }
      start = text.indexOf(quote, start + 1);
    }
    if (matches.length === 1) start = matches[0];
    else if (matches.includes(anchor?.start)) start = anchor.start;
    else return null;
  }
  const end = start + quote.length;
  const first = nodes.find(n => start < n.start + n.node.length);
  const last = nodes.find(n => end <= n.start + n.node.length);
  if (!first || !last) return null;
  const range = new Range();
  range.setStart(first.node, start-first.start);
  range.setEnd(last.node, end-last.start);
  return range;
}

export function noteTone(note) {
  if (Number.isInteger(note.tone) && note.tone >= 0 && note.tone < 4) return note.tone;
  let value = 0;
  for (const ch of note.id) value = (value * 31 + ch.charCodeAt(0)) >>> 0;
  return value % 4;
}

const inset = (value, min, max) => Math.max(min, Math.min(max, value));
const stroke = paths => '<svg viewBox="0 0 24 24" aria-hidden="true">'+paths+'</svg>';
const icons = {
  comment:stroke('<path d="M4 4h16v12H10l-5 4v-4H4Z"/>'),
  save:stroke('<path d="m5 12 4 4L19 6"/>'),
  cancel:stroke('<path d="m6 6 12 12M18 6 6 18"/>'),
  minimize:stroke('<path d="M5 12h14"/>'),
  edit:stroke('<path d="m5 15 10-10 4 4L9 19l-5 1Z"/>')
};

export function mountAnnotations({area, drawer, notes, context, save, saveText=()=>'', renderSave=()=>{}}) {
  const layer = document.createElement('div');
  layer.className = 'dr-annotation-layer';
  const add = document.createElement('button');
  add.className = 'dr-add-comment';
  add.textContent = 'Add comment';
  add.hidden = true;
  const card = document.createElement('section');
  card.className = 'dr-annotation-card';
  card.setAttribute('role','dialog');
  card.setAttribute('aria-label','Inline comment');
  card.hidden = true;
  layer.append(add,card);
  document.body.append(layer);

  const fallback = document.createElement('div');
  fallback.className='dr-highlight-layer';
  layer.prepend(fallback);
  const nativeHighlights=!!(window.CSS?.highlights && window.Highlight);
  const pins = new Map();
  // Uncommitted text stays available if the user briefly visits another quote.
  const edits = new Map();
  function editKey(note) {
    return notes().some(saved=>saved.id===note.id) ? note.id : JSON.stringify([
      note.packageId,note.variationId,note.stateId,note.theme,note.side,note.anchor,note.quote
    ]);
  }
  let anchors = [];
  let selection = null, opened = null, frame = 0, hoverTimer = 0;

  function action(name, label, run) {
    const button = document.createElement('button');
    button.type = 'button';
    button.setAttribute('aria-label',label);
    button.title = label;
    button.innerHTML = icons[name];
    button.onclick = run;
    return button;
  }

  function matches(note) {
    const scope = context();
    return note.packageId === scope.packageId && note.variationId === scope.variationId &&
      (!note.stateId || note.stateId === scope.stateId);
  }

  function paneFor(note) {
    if (!area || !matches(note)) return null;
    if (!note.side && !note.theme) return area;
    const panes = [...area.querySelectorAll('[data-reference]')];
    return panes.find(el => el.dataset.theme === note.theme &&
      el.dataset.reference === (note.side === 'current' ? 'current' : 'proposal'));
  }

  function selectedQuote() {
    const selected = window.getSelection();
    if (!selected?.rangeCount || selected.isCollapsed) return null;
    const range = selected.getRangeAt(0);
    if (!area?.contains(range.commonAncestorContainer) || drawer.contains(range.commonAncestorContainer) || layer.contains(range.commonAncestorContainer)) return null;
    const element = range.startContainer.nodeType === 1 ? range.startContainer : range.startContainer.parentElement;
    const column = element.closest('[data-reference]');
    const pane = column || area;
    if (!pane.contains(range.endContainer)) return null;
    const before = new Range();
    before.selectNodeContents(pane);
    before.setEnd(range.startContainer, range.startOffset);
    const start = before.toString().length;
    const quote = range.toString();
    if (!quote.trim()) return null;
    const text = pane.textContent;
    return {...context(), quote,
      side:column ? (column.dataset.reference === 'current' ? 'current' : 'proposed') : null,
      theme:column?.dataset.theme || null,
      anchor:{start, repeated:text.indexOf(quote)!==text.lastIndexOf(quote), before:text.slice(Math.max(0,start-32),start), after:text.slice(start+quote.length,start+quote.length+32)}
    };
  }

  function visibleBounds(pane) {
    const viewport=window.visualViewport;
    let left=viewport?.offsetLeft || 0, top=viewport?.offsetTop || 0;
    let right=left+(viewport?.width || innerWidth), bottom=top+(viewport?.height || innerHeight);
    for (let el=pane; el; el=el.parentElement) {
      const box=el.getBoundingClientRect(), style=getComputedStyle(el);
      if (el===area || /(auto|scroll|hidden|clip)/.test(style.overflowX)) {
        left=Math.max(left,box.left); right=Math.min(right,box.right);
      }
      if (el===area || /(auto|scroll|hidden|clip)/.test(style.overflowY)) {
        top=Math.max(top,box.top); bottom=Math.min(bottom,box.bottom);
      }
    }
    return {left,top,right,bottom};
  }

  function anchorBox(range, bounds) {
    return [...range.getClientRects()].filter(r => r.width && r.bottom>bounds.top &&
      r.top<bounds.bottom && r.right>bounds.left && r.left<bounds.right).at(-1);
  }

  function place(el, box, bounds) {
    el.style.left = inset(box.left, bounds.left+3, bounds.right-el.offsetWidth-3)+'px';
    const below=box.bottom+5;
    el.style.top = inset(below+el.offsetHeight<=bounds.bottom ? below : box.top-el.offsetHeight-5,
      bounds.top+2,bounds.bottom-el.offsetHeight-2)+'px';
  }

  function closeCard(focusPin=false) {
    clearTimeout(hoverTimer);
    const pin=opened && pins.get(opened.note.id);
    opened=null;card.hidden=true;card.replaceChildren();paintHighlights();
    if (focusPin) (pin || area)?.focus({preventScroll:true});
  }

  function display(note, mode) {
    closeCard();
    opened={note,mode};
    const header=document.createElement('div');
    header.className='dr-card-heading';
    const quote=document.createElement('q');
    quote.textContent=note.quote;
    header.append(quote);
    card.dataset.tone=noteTone(note);
    card.hidden=false;card.append(header);paintHighlights();
    if (mode==='edit') {
      const input=document.createElement('textarea');
      input.setAttribute('aria-label','Inline comment text');
      const key=editKey(note);
      input.placeholder='Write a comment…';input.rows=2;input.value=edits.get(key) ?? note.text ?? '';
      const controls=document.createElement('div');
      controls.className='dr-card-actions';
      const commit=()=>{
        const text=input.value.trim();
        if (!text) return;
        edits.delete(key);save({...note,text,status:'open'});
        closeCard();render();pins.get(note.id)?.focus({preventScroll:true});
      };
      const tick=action('save','Save comment',commit);
      tick.disabled=!input.value.trim();
      input.oninput=()=>{edits.set(key,input.value);tick.disabled=!input.value.trim();};
      input.onkeydown=e=>{if ((e.ctrlKey||e.metaKey) && e.key==='Enter') {e.preventDefault();commit();}};
      controls.append(action('cancel','Discard edit',()=>{edits.delete(key);closeCard(true);}),tick);
      card.append(input,controls);layout();input.focus({preventScroll:true});
    } else {
      header.append(action('edit','Edit comment',()=>display(note,'edit')),
        action('minimize','Minimize comment',()=>closeCard(true)));
      const body=document.createElement('p');body.textContent=note.text;card.append(body);
      const status=document.createElement('div');status.className='dr-save-state';status.dataset.inlineSave='';status.setAttribute('role','status');
      renderSave(note,status);card.append(status);
      layout();
    }
  }

  function hoverOut() {
    clearTimeout(hoverTimer);
    if (opened?.mode==='hover') hoverTimer=setTimeout(()=>closeCard(),180);
  }
  card.onpointerenter=()=>clearTimeout(hoverTimer);
  card.onpointerleave=hoverOut;
  card.onkeydown=e=>{if(e.key==='Escape'){
    e.preventDefault();
    if(opened?.mode==='edit') edits.delete(editKey(opened.note));
    closeCard(true);
  }};
  function pinFor(note) {
    let pin=pins.get(note.id);
    if (!pin) {
      pin=document.createElement('button');pin.type='button';pin.className='dr-annotation-pin';
      pin.innerHTML=icons.comment;layer.append(pin);pins.set(note.id,pin);
    }
    pin.dataset.tone=noteTone(note);
    pin.setAttribute('aria-label','Comment on “'+note.quote+'”: '+note.text);
    pin.title=saveText(note);
    pin.onclick=()=>display(note,'read');
    pin.onpointerenter=e=>{
      if (e.pointerType==='mouse' && (!opened || opened.mode==='hover')) display(note,'hover');
    };
    pin.onpointerleave=hoverOut;
    return pin;
  }

  function paintHighlights() {
    const ranges=anchors.slice();
    if(opened?.mode==='edit' && !pins.has(opened.note.id)){
      const pane=paneFor(opened.note), range=pane && locate(pane,opened.note);
      if(range) ranges.push({note:opened.note,pane,range});
    }
    if(nativeHighlights){
      for(let tone=0;tone<4;tone++) {
        const matching=ranges.filter(a=>noteTone(a.note)===tone).map(a=>a.range);
        CSS.highlights.set('dr-quote-'+tone,new Highlight(...matching));
      }
    }else{
      fallback.replaceChildren();
      for(const {note,pane,range} of ranges){
        const bounds=visibleBounds(pane);
        for(const box of range.getClientRects()){
          const left=Math.max(bounds.left,box.left),top=Math.max(bounds.top,box.top);
          const width=Math.min(bounds.right,box.right)-left,height=Math.min(bounds.bottom,box.bottom)-top;
          if(width<=0 || height<=0) continue;
          const mark=document.createElement('i');
          mark.dataset.tone=noteTone(note);
          Object.assign(mark.style,{left:left+'px',top:top+'px',width:width+'px',height:height+'px'});
          fallback.append(mark);
        }
      }
    }
  }

  function render() {
    anchors=[];
    for (const note of notes()) {
      if (!note.quote || !note.text.trim()) continue;
      const pane=paneFor(note),range=pane && locate(pane,note);
      if (!range) continue;
      anchors.push({note,pane,range,pin:pinFor(note)});
    }
    const visible=new Set(anchors.map(a=>a.note.id));
    for(const [id,pin] of pins) if(!visible.has(id)){pin.remove();pins.delete(id);}
    paintHighlights();
    layout();
  }

  function layout() {
    frame=0;
    if (!nativeHighlights) paintHighlights();
    const occupied=[];
    for (const {pane,range,pin} of anchors) {
      const bounds=visibleBounds(pane),box=anchorBox(range,bounds);
      pin.hidden=!box;
      if(!box) continue;
      let x=inset(box.right-9,bounds.left,bounds.right-21);
      let y=inset(box.top-20,bounds.top,bounds.bottom-21);
      for (const other of occupied) if(Math.abs(other.x-x)<20 && Math.abs(other.y-y)<20) {
        if (other.x+40<=bounds.right) x=other.x+20;
        else y=inset(other.y+20,bounds.top,bounds.bottom-20);
      }
      pin.style.left=x+'px';pin.style.top=y+'px';occupied.push({x,y});
    }
    for (const [el,note] of [[add,selection],[card,opened?.note]]) {
      const pane=note && paneFor(note);
      const range=pane && locate(pane,note);
      const bounds=pane && visibleBounds(pane);
      const box=range && anchorBox(range,bounds);
      el.hidden=!box;
      if(box) place(el,box,bounds);
    }
  }
  function schedule(){if (!frame) frame=requestAnimationFrame(layout);}
  document.addEventListener('selectionchange',()=>{
    selection=selectedQuote();schedule();
  });
  add.onpointerdown=e=>e.preventDefault();
  add.onclick=()=>{
    if (!selection) return;
    const usage=[0,0,0,0];
    for(const note of notes()) if(note.quote && matches(note))usage[noteTone(note)]++;
    const tone=usage.indexOf(Math.min(...usage));
    const note={...selection,id:crypto.randomUUID(),tone};
    window.getSelection()?.removeAllRanges();selection=null;add.hidden=true;
    display(note,'edit');
  };
  if(area)new ResizeObserver(schedule).observe(area);
  document.addEventListener('scroll',schedule,true);
  window.addEventListener('resize',schedule);
  window.visualViewport?.addEventListener('resize',schedule);
  return {
    render,
    drafts(){return [...edits].map(([key,text])=>({key,text}));},
    clearDrafts(){edits.clear();closeCard();},
    refreshStatus(){
      for(const note of notes()){const pin=pins.get(note.id);if(pin)pin.title=saveText(note);}
      const line=card.querySelector('[data-inline-save]');
      if(line && opened){const note=notes().find(n=>n.id===opened.note.id);if(note)renderSave(note,line);}
    },
    setTheme(theme){layer.dataset.theme=theme;add.dataset.theme=theme;},
    reveal(note) {
      const target=anchors.find(a=>a.note.id===note.id);
      if (!target) return false;
      target.range.startContainer.parentElement?.scrollIntoView({block:'nearest',inline:'nearest'});
      display(note,'read');return true;
    },
    close:closeCard
  };
}
