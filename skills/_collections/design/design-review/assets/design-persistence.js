// Review content travels between devices. Display choices belong to this browser.
export const viewKeys=['currentChangeId','activeOptions','appearance','reference','scene','scenes','showCurrent','previewThemes','expanded','placement','position','size','drawerHeight','drawerCollapsed','tab','sides'];
export function reviewContent(value){
  if(!value)return value;
  const content=structuredClone(value);
  for(const key of [...viewKeys,'version','view','uiDrafts'])delete content[key];
  return content;
}
export const contentKey=value=>JSON.stringify(reviewContent(value));
export function deviceView(value){return Object.fromEntries(viewKeys.filter(key=>value?.[key]!==undefined).map(key=>[key,structuredClone(value[key])]));}
export function recoveryDiff(draft,latest){
  const rows=[];
  for(const note of draft?.comments || []){
    const other=latest?.comments?.find(n=>n.id===note.id);
    if(!other || JSON.stringify(other)!==JSON.stringify(note))rows.push({label:note.label || 'Comment',text:note.text});
  }
  const packages=Array.isArray(draft?.changes)?draft.changes.map(p=>[p.id,{...p,options:Object.fromEntries(p.options.map(o=>[o.id,o]))}]):Object.entries(draft?.changes || {});
  for(const [id,pkg] of packages)for(const [optionId,option] of Object.entries(pkg.options || {})){
    const other=Array.isArray(latest?.changes)?latest.changes.find(p=>p.id===id)?.options.find(o=>o.id===optionId):latest?.changes?.[id]?.options?.[optionId];
    const label=draft.catalog?.find(p=>p.id===id)?.options.find(o=>o.id===optionId)?.title || option.title || optionId;
    for(const [key,value] of Object.entries(option.tweaks || {}))if(JSON.stringify(value)!==JSON.stringify(other?.tweaks?.[key]))rows.push({label:label+' · '+key,text:'This device: '+JSON.stringify(value)+' · Latest: '+JSON.stringify(other?.tweaks?.[key] ?? null)});
    if(option.decision!==other?.decision)rows.push({label:label+' · Decision',text:'This device: '+option.decision+' · Latest: '+(other?.decision || 'undecided')});
  }
  for(const [,text] of draft?.uiDrafts?.comments || [])if(text.trim())rows.push({label:'Unsubmitted comment',text});
  for(const edit of draft?.uiDrafts?.inline || [])if(edit.text.trim())rows.push({label:'Unsubmitted inline comment',text:edit.text});
  for(const field of draft?.uiDrafts?.parameters || [])rows.push({label:'Unsubmitted parameter · '+field.key,text:field.value});
  return rows;
}
