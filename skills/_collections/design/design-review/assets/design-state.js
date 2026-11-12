const copy = value => structuredClone(value);
export const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
export function optionSnapshot(option) {
  return {sourceRevision:option.sourceRevision,tweaks:copy(option.tweaks),comment:option.comment,
    ...(option.commentEvidence?.length ? {comments:copy(option.commentEvidence)} : {})
  };
}
export function approvalCurrent(option) {
  return option.decision === 'approved' && same(option.approval, optionSnapshot(option));
}
// Single designs use the same internal scope without inventing visible navigation.
export function normalizeDesigns(changes, design = {}) {
  return (changes?.length ? changes : [design]).map((change, i) => {
    const variants = change.options?.length ? change.options : [change];
    return {
      ...change, id: change.id || 'design-' + (i + 1),
      scenes: change.scenes?.length ? change.scenes : [['default', '']],
      options: variants.map((option, j) => ({
        ...option, id: option.id || 'option-' + (j + 1),
        defaults: option.defaults || {}, controls: option.controls || [],
        revision: option.revision || 1
      }))
    };
  });
}

export function createState(changes, saved, {reviewId='shared-design-controls-example', reviewVersion=1, commentUpdates={}, previousReview, initialReview} = {}) {
  // A supplied export can resume this same version in a fresh browser.
  if (!saved && initialReview?.reviewId===reviewId && initialReview.reviewVersion===reviewVersion) {
    const view = initialReview.view || {};
    saved = {
      schemaVersion:3, version:0, reviewVersion, ...copy(view),
      scene:view.scenes?.[view.currentChangeId], comments:copy(initialReview.comments || []),
      ...(initialReview.legacyReview ? {legacyReview:copy(initialReview.legacyReview)} : {}),
      changes:Object.fromEntries(initialReview.changes.map(c => [c.id, {
        decision:c.status==='rejected'?'rejected':'open', selectedOptionId:c.selectedOptionId,
        options:Object.fromEntries(c.options.map(o => [o.id,copy(o)]))
      }]))
    };
  }
  const state = saved?.schemaVersion === 3 ? copy(saved) : {
    schemaVersion:3,version:0,currentChangeId:changes[0].id,activeOptions:{},changes:{},appearance:null,
    reference:'proposal',scene:'default',scenes:{},showCurrent:false,previewThemes:'both',expanded:false,placement:{review:false,live:true},position:null,size:null,submissions:[]
  };
  state.submissions ||= [];
  state.version=Number.isFinite(state.version)?state.version:0;
  // Archive the version that was actually reviewed, including options later removed.
  const newRevision = state.reviewVersion && state.reviewVersion < reviewVersion;
  if (newRevision && state.catalog) {
    state.submissions.push({...exportReview(state, state.catalog), submittedAt:new Date().toISOString()});
    state.changes = {};
  } else if (saved?.schemaVersion === 3 && !state.reviewVersion) {
    const catalog = Object.entries(state.changes).map(([id, entry]) => {
      const definition = changes.find(c => c.id === id);
      return {id, title:definition?.title || id, options:Object.keys(entry.options).map(key => ({
        id:key, title:definition?.options.find(o=>o.id===key)?.title || key
      }))};
    });
    state.submissions.push({...exportReview(state, catalog), legacyDraft:true, submittedAt:new Date().toISOString()});
    for (const entry of Object.values(state.changes)) entry.decision='open';
  }
  if (!saved && previousReview) state.comments=copy(previousReview.comments || []);
  state.reviewId = reviewId;
  state.reviewVersion = reviewVersion;
  state.sides ||= state.showCurrent ? 'both' : 'proposed';
  state.catalog = changes.map(({id, title, options}) => ({
    id, title, options:options.map(({id, title})=>({id, title}))
  }));
  state.showCurrent ??= state.reference === 'current'; state.reference='proposal';
  state.previewThemes ||= 'both'; state.scenes ||= {[state.currentChangeId]:state.scene||'default'}; state.size ||= null;
  state.activeOptions ||= {}; state.changes ||= {}; state.submissions ||= []; state.placement ||= {review:false,live:true};
  if (!changes.some(c=>c.id===state.currentChangeId)) state.currentChangeId=changes[0].id;
  for (const change of changes) {
    const entry=state.changes[change.id] ||= {decision:'open',selectedOptionId:null,options:{}};
    entry.options ||= {};
    if (!change.options.some(o=>o.id===state.activeOptions[change.id])) state.activeOptions[change.id]=change.options[0].id;
    for (const option of change.options) {
      const stored=entry.options[option.id];
      entry.options[option.id]={tweaks:copy(option.defaults),comment:'',decision:'undecided',approval:null,approvalHistory:[],...stored,sourceRevision:option.revision};
      entry.options[option.id].tweaks={...option.defaults,...stored?.tweaks};
    }
  }
  if (saved && saved.schemaVersion !== 3) {
    state.legacyReview=copy(saved);
    if (['light','dark'].includes(saved.appearance)) state.appearance=saved.appearance;
    const task=state.changes.tasks;
    for (const id of ['list','grouped','focus']) {
      const previous=saved.drafts?.[id];
      if (previous && task?.options[id]) {
        task.options[id].comment=typeof previous.comment==='string'?previous.comment:'';
        task.options[id].previousRevision=copy(previous);
      }
    }
  }
  const change = changes.find(c => c.id === state.currentChangeId);
  state.scene = change.scenes.some(([id]) => id === state.scene) ? state.scene : change.scenes[0][0];
  if (!Array.isArray(state.comments)) {
    state.comments = [];
    for (const change of changes) for (const option of change.options) {
      const draft = state.changes[change.id].options[option.id];
      if (draft.comment.trim()) state.comments.push({
        id:crypto.randomUUID(), packageId:change.id, variationId:option.id, stateId:null,
        label:[change.title, option.title].filter(Boolean).join(' · '),
        text:draft.comment, quote:'', status:'open', reviewVersion
      });
    }
  }
  state.appliedCommentUpdates ||= {};
  for (const comment of state.comments) {
    const update = commentUpdates[comment.id];
    const stamp = update && JSON.stringify([reviewVersion,update]);
    const reviewedText = update?.expectedText ?? previousReview?.comments?.find(c=>c.id===comment.id)?.text
      ?? initialReview?.comments?.find(c=>c.id===comment.id)?.text;
    if (stamp && reviewedText===comment.text && state.appliedCommentUpdates[comment.id] !== stamp) {
      if (['open','resolved'].includes(update.status)) comment.status = update.status;
      if (typeof update.reply === 'string') comment.reply = update.reply;
      state.appliedCommentUpdates[comment.id] = stamp;
      syncOptionComment(state, comment, !!state.changes[comment.packageId]?.options[comment.variationId]?.commentEvidence);
    } else if (newRevision || (!saved && previousReview)) syncOptionComment(state, comment);
  }
  return state;
}
export function syncOptionComment(state, {packageId, variationId}, trackEvidence=true) {
  const targets=packageId?[[packageId,variationId]]:Object.entries(state.changes).flatMap(([id,entry])=>Object.keys(entry.options).map(optionId=>[id,optionId]));
  for(const [id,optionId] of targets){
    const draft = state.changes[id]?.options[optionId];
    if (!draft) continue;
    const notes = state.comments.filter(c => (!c.packageId || c.packageId===id && c.variationId===optionId) && c.text.trim());
    draft.comment = notes.map(c => c.text).join('\n');
    if (trackEvidence) draft.commentEvidence = notes.map(({status,reply,...authored}) => copy(authored));
  }
}

export function needsTweaks(state,packageId,variationId) {
  return state.comments?.some(c=>(!c.packageId || c.packageId===packageId && c.variationId===variationId) && c.text.trim() && c.status!=='resolved');
}

export function currentRecords(state, changes) {
  const change=changes.find(c=>c.id===state.currentChangeId);
  const option=change.options.find(o=>o.id===state.activeOptions[change.id]);
  return {change,option,entry:state.changes[change.id],draft:state.changes[change.id].options[option.id]};
}
export function decide(state, changeId, optionId, decision) {
  const entry=state.changes[changeId], option=entry.options[optionId];
  if(decision==='approved') {
    if(state.comments?.some(c=>!c.packageId || c.packageId===changeId && c.variationId===optionId))syncOptionComment(state,{packageId:changeId,variationId:optionId});
    const snapshot=optionSnapshot(option);
    option.approval=copy(snapshot); option.approvalHistory.push({at:new Date().toISOString(),snapshot:copy(snapshot)});
    entry.selectedOptionId=optionId; entry.decision='open';
  } else if(entry.selectedOptionId===optionId) entry.selectedOptionId=null;
  option.decision=decision;
  state.version++;
}
export function exportReview(state, changes) {
  return {
    schemaVersion:4,reviewId:state.reviewId,reviewVersion:state.reviewVersion,
    comments:copy((state.comments || []).filter(note=>note.text.trim())),implementationRequested:false,
    semantics:{approve:'choose this option and exact settings',approvalComments:'required tweaks',reject:'dismiss only this option',commentOnly:'feedback without decision',entireReview:'apply decision to the active variation in each package'},
    changes:changes.map(change=>{
      const entry=state.changes[change.id],chosen=entry.options[entry.selectedOptionId];
      const status=entry.decision==='rejected'?'rejected':!chosen?'open':!approvalCurrent(chosen)?'needs_review':(state.comments ? needsTweaks(state,change.id,entry.selectedOptionId) : chosen.comment.trim())?'required_tweaks':'approved';
      return {id:change.id,title:change.title,status,selectedOptionId:entry.selectedOptionId,options:change.options.map(option=>({id:option.id,title:option.title,...copy(entry.options[option.id]),approvalCurrent:approvalCurrent(entry.options[option.id])}))};
    }),
    view:{currentChangeId:state.currentChangeId,activeOptions:copy(state.activeOptions),sides:state.sides,previewThemes:state.previewThemes,scenes:copy(state.scenes)},
    ...(state.legacyReview?{legacyReview:copy(state.legacyReview)}:{})
  };
}
