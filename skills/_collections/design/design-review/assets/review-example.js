import {createState,decide,exportReview,syncOptionComment} from './design-state.js';
import {mountDesignFooter} from './design-footer.js';
import {openArtifactPersistence} from './artifact-persistence.js';
async function startExample(){
const bridge=window.artifacts;
if(bridge)await bridge.ready;
const range=(key,label,min,max,unit='px',step=1)=>({key,label,type:'range',min,max,unit,step});
const check=(key,label)=>({key,label,type:'checkbox'});
const palette=[['lime','Lime','#c1ff3d'],['pink','Rose','#ff8bc0'],['yellow','Amber','#ffd84a'],['blue','Blue','#2563eb'],['violet','Violet','#7c3aed'],['ink','Ink','#242424']];
const accentControl={key:'accent',label:'Accent',type:'color',presets:palette};
const shared=[accentControl,range('fontSize','Text size',13,24),{key:'fontWeight',label:'Text weight',type:'select',choices:[['400','Regular'],['500','Medium'],['600','Semibold']]},range('titleSize','Title size',20,48),range('pagePadding','Page padding',8,48)];
const accentHex=value=>palette.find(([id])=>id===value)?.[2]||(/^#[0-9a-f]{6}$/i.test(value)?value:'#c1ff3d');
const accentText=hex=>{const linear=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return linear[0]*.2126+linear[1]*.7152+linear[2]*.0722>.179?'#000000':'#ffffff';};
const base={fontWeight:'400',fontSize:16,titleSize:30,pagePadding:24,accent:'#c1ff3d',buttonHeight:42,buttonRadius:5,navPadding:18,navGap:8,labelSize:14,iconStroke:1.75,navSurface:false,activeFill:false};
const taskDefaults={...base,heading:'Today',spacing:18,radius:0,rowGap:0,checkboxSize:20,metadata:true,dividers:true,count:true,buttonRadius:5};
const taskControls=[...shared,{key:'heading',label:'Heading',type:'text',maxLength:80},range('spacing','Row padding',8,30),range('rowGap','Row gap',0,20),range('radius','Row corners',0,20),range('checkboxSize','Checkbox size',16,28),check('metadata','Task details'),check('dividers','Row dividers'),check('count','Task count'),range('buttonRadius','Button corners',0,20)];
const goalDefaults={...base,actionLabel:'Continue',spacing:14,radius:6,buttonHeight:44,fullButton:false,goalDescriptions:true,progress:true,intro:true};
const goalControls=[...shared,{key:'actionLabel',label:'Action label',type:'text',required:true,maxLength:60},range('spacing','Choice gap',6,24),range('radius','Choice corners',0,20),{key:'buttonHeight',label:'Button height',type:'number',min:28,max:96,unit:'px'},range('buttonRadius','Button corners',0,20),{key:'fullButton',label:'Button width',type:'segmented',choices:[[false,'Fit'],[true,'Full']]},check('goalDescriptions','Choice descriptions'),check('progress','Setup progress'),check('intro','Intro text')];
const iconDefaults={...base,iconSize:22,labels:true,navPadding:18};
const iconControls=[...shared,range('iconSize','Icon size',18,36),range('iconStroke','Stroke width',1,3,'px',.25),check('labels','Navigation labels'),range('labelSize','Label size',11,18),range('navGap','Icon / label gap',2,16),range('navPadding','Navigation padding',8,28),check('navSurface','Navigation surface'),check('activeFill','Active item fill')];
const changes=[
 {id:'tasks',title:'Task layout',description:'Compare how the task list guides attention. Find the next task and distinguish completed work.',baseline:{kind:'list',tweaks:taskDefaults},scenes:[['default','Today · tasks'],['complete','All complete'],['empty','Empty']],options:[
  {id:'list',revision:5,title:'Simple list',kind:'list',tradeoff:'Dense and easy to scan; the next task has the same weight as the others.',defaults:taskDefaults,controls:taskControls},
  {id:'grouped',revision:5,title:'Separated tasks',kind:'grouped',tradeoff:'Clear task boundaries require more vertical space.',defaults:{...taskDefaults,spacing:16,radius:6,rowGap:12},controls:taskControls},
  {id:'focus',revision:5,title:'Next task first',kind:'focus',tradeoff:'A stronger starting point pushes later tasks lower on the screen.',defaults:{...taskDefaults,radius:6,rowGap:8},controls:taskControls}
 ]},
 {id:'onboarding',title:'Onboarding',description:'Compare ways to choose a daily goal. Keep the explanation and next action clear.',baseline:{kind:'guided',tweaks:{...goalDefaults,radius:4,goalDescriptions:false}},scenes:[['default','Choose goal'],['ready','Goal selected'],['done','Goal set']],options:[
  {id:'guided',revision:3,title:'Guided choice',kind:'guided',tradeoff:'A vertical choice is clear and deliberate, with more scrolling on small screens.',defaults:goalDefaults,controls:goalControls},
  {id:'overview',revision:3,title:'Compact choice',kind:'overview',tradeoff:'A shorter choice group leaves more context visible.',defaults:{...goalDefaults,spacing:10,radius:4,goalDescriptions:false},controls:goalControls}
 ]},
 {id:'icons',title:'Navigation icons',description:'Compare icon weight and label visibility in the actual navigation context.',baseline:{kind:'outline',tweaks:{...iconDefaults,iconSize:20}},scenes:[['default','Today · tasks'],['empty','Empty']],options:[
  {id:'outline',revision:3,title:'Outline icons',kind:'outline',tradeoff:'Quiet visual weight; labels help distinguish destinations.',defaults:iconDefaults,controls:iconControls},
  {id:'filled',revision:3,title:'Filled icons',kind:'filled',tradeoff:'Stronger silhouettes make the navigation more prominent.',defaults:{...iconDefaults,activeFill:true},controls:iconControls}
 ]}
];
const params=new URLSearchParams(bridge?.navigation.search ?? location.search),mode=params.get('mode')==='live'?'live':'review';
const $=id=>document.getElementById(id),demo={checked:[false,false,true],goal:0};
$('title').textContent=mode==='live'?'Design controls':'Design review';document.title=$('title').textContent;
$('mode-link').textContent=mode==='live'?'Open structured review':'Try the floating placement demo';
$('mode-link').href='?'+new URLSearchParams({...(params.get('single')==='1'?{single:'1'}:{}),...(params.get('test')==='1'?{test:'1'}:{}),...(mode==='review'?{mode:'live'}:{})});
let active=null;
const navIcon=(kind,name,size)=>{
 const paths={today:'<rect x="5" y="4" width="14" height="16" rx="2"/><path d="m8 12 3 3 5-6"/>',upcoming:'<rect x="4" y="6" width="16" height="14" rx="2"/><path d="M8 3v6m8-6v6M4 11h16"/>',settings:'<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2"/>'};
 return '<svg style="width:'+size+'px;height:'+size+'px;'+(kind==='filled'?'fill:currentColor;fill-opacity:.25;':'')+'" viewBox="0 0 24 24" aria-hidden="true">'+paths[name]+'</svg>';
};
function makePreview(theme,reference,context){
 const {state,change,option,draft}=context,design=reference==='current'?change.baseline:option;
 const t={...base,...taskDefaults,...(reference==='current'?change.baseline.tweaks:draft.tweaks)};
 const col=document.createElement('section'),key=theme+'-'+reference;
 col.className='preview-column';col.setAttribute('aria-label',theme+' '+reference+' preview');col.dataset.theme=theme;col.dataset.reference=reference;
 col.innerHTML='<div class="theme-label">'+(reference==='current'?'Current':'New')+' ('+(theme==='light'?'Light':'Dark')+')'+'</div><div class="screen '+theme+'"><div class="appbar"><strong>Tasks</strong><span>Workspace</span></div><div class="app-content"></div><div class="appnav"></div></div>';
 const screen=col.querySelector('.screen'),content=col.querySelector('.app-content'),nav=col.querySelector('.appnav');
 for(const [name,value] of Object.entries({font:t.fontSize+'px',title:t.titleSize+'px',padding:t.pagePadding+'px','button-height':t.buttonHeight+'px','button-radius':t.buttonRadius+'px','nav-padding':t.navPadding+'px','nav-gap':t.navGap+'px','label-size':t.labelSize+'px','icon-stroke':t.iconStroke,'weight':t.fontWeight,'accent':accentHex(t.accent),'on-accent':accentText(accentHex(t.accent))}))screen.style.setProperty('--app-'+name,value);
 if(t.navSurface)nav.classList.add('nav-surface');if(t.activeFill)nav.classList.add('active-fill');
 if(change.id==='onboarding'){
  const selected=state.scene==='ready'?(demo.goal||20):demo.goal;
  content.innerHTML=state.scene==='done'?'<span class="step">Setup complete</span><h3>Daily goal set</h3><p class="date">'+(selected||20)+' minutes each day</p><button type="button" class="app-action" data-demo="back">Change goal</button>':(t.progress?'<span class="step">Step 1 of 2</span><div class="setup-progress"><i></i></div>':'')+'<h3>Set a daily goal</h3>'+(t.intro?'<p class="date">Choose the time you want to spend each day.</p>':'')+'<div class="goal-options '+(design.kind==='overview'?'inline':'')+'" style="gap:'+t.spacing+'px">'+[10,20,30].map((n,i)=>'<button type="button" data-goal="'+n+'" aria-pressed="'+(selected===n)+'" style="border-radius:'+t.radius+'px">'+n+' minutes'+(t.goalDescriptions?'<small>'+['A quick start','Build a habit','Go further'][i]+'</small>':'')+'</button>').join('')+'</div><button type="button" class="app-action '+(t.fullButton?'full-width':'')+'" data-demo="continue" '+(!selected?'disabled':'')+'>Continue</button><p class="quiet">You can change this later.</p>';
  nav.innerHTML='<span>Account</span><span><strong>Daily goal</strong></span><span>Finish</span>';
 }else{
  const selected=state.scene==='complete'?[true,true,true]:demo.checked;
  content.innerHTML='<h3>Today</h3><p class="date">Wednesday, 4 November</p>';
  if(state.scene==='empty')content.innerHTML+='<div class="empty"><strong>No tasks for today</strong><p>New tasks will appear here.</p></div>';
  else{
   if(t.count){const count=document.createElement('span');count.className='count';count.textContent='3 tasks · '+selected.filter(Boolean).length+' complete';content.append(count);}
   [['Review onboarding','Product · 10:00'],['Book studio','Personal · 14:00'],['Send invoice','Admin · Complete']].forEach(([name,meta],i)=>{
    const row=document.createElement('div');row.className='task'+(selected[i]?' done':'');
    row.style.padding=t.spacing+'px '+(design.kind==='grouped'?'14px':'0');row.style.marginBottom=t.rowGap+'px';row.style.borderRadius=t.radius+'px';
    row.style.borderTop=t.dividers?'1px solid var(--s-line)':'none';
    if(design.kind==='grouped'||(design.kind==='focus'&&i===0)){row.style.background='var(--s-surface)';row.style.border=t.dividers?'1px solid var(--s-line)':'none';}
    row.innerHTML='<input style="width:'+t.checkboxSize+'px;height:'+t.checkboxSize+'px" type="checkbox" id="'+key+'-task-'+i+'" data-task="'+i+'" '+(selected[i]?'checked':'')+'><label for="'+key+'-task-'+i+'"><span>'+name+'</span>'+(t.metadata?'<small>'+meta+'</small>':'')+'</label>';content.append(row);
   });
  }
  content.innerHTML+='<button type="button" class="app-action" disabled aria-label="Add task, shown for context">Add task</button>';
  nav.innerHTML=['Today','Upcoming','Settings'].map((name,i)=>'<span>'+(change.id==='icons'?navIcon(design.kind,['today','upcoming','settings'][i],t.iconSize):'')+((change.id!=='icons'||t.labels)?(i===0?'<strong>'+name+'</strong>':name):'<span class="dr-sr">'+name+'</span>')+'</span>').join('');
 }
 if(change.id==='tasks')content.querySelector('h3').textContent=t.heading??'Today';
 const actionLabel=content.querySelector('[data-demo=continue]');if(actionLabel)actionLabel.textContent=t.actionLabel||'Continue';
 return col;
}
function render(context){
 active=context;const {state,change,option,entry}=context,index=changes.indexOf(change);
 $('description').textContent=change.description;$('tradeoff').textContent=option.tradeoff;
 const sides=state.sides==='both'?['current','proposal']:state.sides==='current'?['current']:['proposal'];
 $('pair').classList.toggle('compare',sides.length===2);$('pair').replaceChildren();
 const themes=state.previewThemes==='both'?['light','dark']:[state.previewThemes];
 $('pair').classList.toggle('one-theme',themes.length===1);
 for(const theme of themes){
  const group=document.createElement('section');group.className='theme-group';group.setAttribute('aria-label',(theme==='light'?'Light':'Dark')+' designs');
  const heading=document.createElement('h2');heading.textContent=[option.title,change.scenes.find(([id])=>id===state.scene)?.[1]].filter(Boolean).join(' · ')+' ('+(theme==='light'?'Light':'Dark')+')';heading.className='group-title';group.append(heading);
  const designs=document.createElement('div');designs.className='comparison-pair';
  for(const reference of sides)designs.append(makePreview(theme,reference,context));
  group.append(designs);$('pair').append(group);
 }
}
// These two fictional revisions never enter the working review.
const exampleState=createState(changes,null);
const exampleComment={
  id:'example-spacing',packageId:'tasks',variationId:'list',stateId:'default',
  label:'Task layout · Simple list · Today',quote:'Review onboarding',theme:'light',side:'proposed',
  text:'Increase row spacing to 20px.',status:'open',reviewVersion:1
};
exampleState.comments.push(exampleComment);
syncOptionComment(exampleState,exampleComment);
decide(exampleState,'tasks','list','approved');
const historyExamples=[exportReview(exampleState,changes)];
exampleState.reviewVersion=2;
exampleState.changes.tasks.options.list.tweaks.spacing=20;
exampleComment.status='resolved';
exampleComment.reply='Set row spacing to 20px.';
syncOptionComment(exampleState,exampleComment);
decide(exampleState,'tasks','list','approved');
historyExamples.push(exportReview(exampleState,changes));

const single=params.get('single')==='1';
const singleDesign={...changes[0].options[0], id:'tasks', title:'Task layout',
  description:'Review a single task list.', baseline:changes[0].baseline};
const persistence=bridge ? await openArtifactPersistence(bridge,(single?'single-review':'review')+(params.get('test')==='1'?'-test':'')) : null;
const controls=mountDesignFooter($('design-controls'),{
  ...(single ? {design:singleDesign,reviewId:'single-design-example'} : {changes,historyExamples,reviewId:'shared-design-controls-example'}),
  reviewVersion:3,mode,persistence,onAppearance:theme=>document.documentElement.dataset.theme=theme,onChange:render
});
$('pair').onchange=e=>{
 if(!e.target.matches('[data-task]'))return;const i=Number(e.target.dataset.task),id=e.target.id;
 if(active.state.scene==='complete')demo.checked=[true,true,true];demo.checked[i]=e.target.checked;controls.updateView({scene:demo.checked.every(Boolean)?'complete':'default'});document.getElementById(id)?.focus();
};
$('pair').onclick=e=>{
 const goal=e.target.closest('[data-goal]');if(goal){demo.goal=Number(goal.dataset.goal);controls.updateView({scene:'ready'});return;}
 const action=e.target.closest('[data-demo]')?.dataset.demo;if(!action)return;controls.updateView({scene:action==='continue'?'done':'ready'});
};

}
startExample().catch(error=>{
 const message=document.createElement('p');message.setAttribute('role','alert');message.textContent='Could not open the saved review. '+error.message;
 const reload=document.createElement('button');reload.textContent='Reload example';reload.onclick=()=>window.artifacts?window.artifacts.navigation.reload():location.reload();
 document.getElementById('preview').replaceChildren(message,reload);
});
