import {reviewContent,contentKey} from './design-persistence.js';

// Optional host adapter. Review semantics and editable source stay in this project.
export async function openArtifactPersistence(bridge,name){
  await bridge.ready;
  if(!bridge.device || !bridge.drafts.refresh)throw new Error('This review needs the updated Artifact Box runtime. Reopen its current link.');
  const opened=await bridge.drafts.open(name,{schema:'design-review-v3-options-5-3-3',statusDisplay:'inline',recovery:'defer'});
  let head=opened.shared || opened;
  if(head.data && ![3,4].includes(head.data.schemaVersion))throw new Error('Unsupported saved review format. Export it from Artifact Box before continuing.');
  let captures=Promise.resolve(),queued=Promise.resolve(),failure=null,checking=null,paused=false;
  let latest=contentKey(head.data),listener=()=>{},updated=async()=>{},viewSerial=Promise.resolve();
  const recoveries=[...(opened.recoveryDrafts || [])];
  const [view,seen]=await Promise.all([bridge.device.get(name+'-view').catch(()=>null),bridge.device.get(name+'-recovery').catch(()=>[])]);
  const ignored=new Set(Array.isArray(seen)?seen:[]);
  const adapter={
    get data(){return reviewContent(head.data);},view,search:bridge.navigation.search,recoveries,
    get paused(){return paused;},
    isAcknowledged(record){return ignored.has(record.id+':'+record.stamp);},
    onStatus(fn){listener=fn;},onUpdate(fn){updated=fn;},
    beforeLeave(fn){bridge.navigation.beforeLeave(fn);},
    showRecovery:()=>bridge.drafts.showRecovery(name),
    saveView(value){
      const snapshot=structuredClone(value);
      viewSerial=viewSerial.catch(()=>{}).then(()=>bridge.device.set(name+'-view',snapshot));return viewSerial;
    },
    async captureRecovery(value){
      await captures.catch(()=>{});
      const snapshot=structuredClone(value);
      const index=recoveries.findIndex(r=>r.id==='current');
      const record={id:'current',data:snapshot,updatedAt:new Date().toISOString(),recoveryOnly:true,localConfirmed:false};
      if(index<0)recoveries.push(record);else recoveries[index]=record;
      await bridge.drafts.stage(name,snapshot,{sync:false});record.localConfirmed=true;
    },
    async continueLatest(){
      await queued.catch(()=>{});await captures.catch(()=>{});
      const fresh=await bridge.drafts.refresh(name);
      head=fresh;latest=contentKey(head.data);failure=null;paused=false;captures=Promise.resolve();queued=Promise.resolve();
      recoveries.splice(0,recoveries.length,...(fresh.recoveryDrafts || []));
      for(const record of recoveries)ignored.add(record.id+':'+record.stamp);
      await bridge.device.set(name+'-recovery',[...ignored].slice(-128));
      listener('Saved in Artifact Box');return adapter.data;
    },
    async check(){
      if(checking)return checking;
      checking=(async()=>{
        await queued.catch(()=>{});
        const fresh=await bridge.state.get(name);
        if(fresh.revision===head.revision && !failure)return;
        paused=true;await updated(fresh);
      })().finally(()=>{checking=null;});
      return checking;
    },
    save(value){
      const snapshot=reviewContent(value),raw=contentKey(snapshot);
      if(paused)return Promise.reject(Object.assign(new Error('Newer saved changes are available.'),{status:409}));
      if(failure)return Promise.reject(failure);
      if(raw===latest)return queued.then(result=>result || head);
      latest=raw;listener('Saving…');
      captures=captures.then(()=>bridge.drafts.stage(name,snapshot));
      queued=captures.then(async()=>{
        const saved=await bridge.drafts.flush(name);head=saved;
        if(contentKey(saved.data)===latest)listener('Saved in Artifact Box');
        return saved;
      }).catch(error=>{failure=error;paused=error.status===409;listener(error.status===409?'Newer changes available':'Not saved');throw error;});
      return queued;
    },
    async flush(){await viewSerial.catch(()=>{});return queued;}
  };
  return adapter;
}
