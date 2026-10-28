import sys,os,json,time,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent.parent
jobs=json.loads((root/'execution/jobs.json').read_text())
tag=sys.argv[1];job=jobs[tag];w=Path(job['workspace'])
env=os.environ.copy()
for k in list(env):
 if k!='CURSOR_API_KEY' and (k.endswith('API_KEY') or k in ['ANTHROPIC_AUTH_TOKEN','CLAUDE_CODE_OAUTH_TOKEN'] or k.startswith(('OPENAI_BASE_URL','ANTHROPIC_BASE_URL','CURSOR_API_ENDPOINT'))):env.pop(k)
if tag.startswith('fable'):
 env['CURSOR_CONFIG_DIR']=str(w/'cursor-config');env['CURSOR_DATA_DIR']=str(w/'cursor-data')
 argv=['agent','--print','--model','claude-fable-5-1-thinking-xhigh','--output-format','stream-json','--mode','ask','--sandbox','enabled','--auto-review','--workspace',str(w),'--trust',(w/'prompt.md').read_text()]
else:
 env.pop('CURSOR_API_KEY',None)
 argv=['codex','--no-daemon','--disable','apps','--disable','plugins','--disable','multi_agent','exec','--ignore-user-config','--model','gpt-6-astra','--sandbox','read-only','--skip-git-repo-check','-C',str(w),'-c','model_reasoning_effort="xhigh"','-c','project_doc_max_bytes=0','-c','memories.use_memories=false','-c','memories.generate_memories=false','-c','sqlite_home='+json.dumps(str(w/'codex-state')),'-c','web_search='+json.dumps('disabled' if tag.endswith('innate') else 'live'),'--json','-o',str(w/'final.md'),'-']
argv=['/usr/bin/sandbox-exec','-f',job['profile']]+argv
out=root/'results';out.mkdir(exist_ok=True)
receipt={'assignment':tag,'started_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'workspace':str(w),'requested_model':'claude-fable-5-1-thinking-xhigh' if tag.startswith('fable') else 'gpt-6-astra','requested_effort':'xhigh','isolation':job,'status':'running'}
(out/(tag+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
err=open(w/'process.stderr.txt','w')
p=subprocess.Popen(argv,cwd=w,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
if tag.startswith('astra'):p.stdin.write((w/'prompt.md').read_text())
p.stdin.close();messages=[];events=0
with open(out/(tag+'.events.jsonl'),'w') as f:
 for line in p.stdout:
  try:o=json.loads(line)
  except ValueError:continue
  if o.get('type') in ['thinking','reasoning']:continue
  item=o.get('item',{})
  if isinstance(item,dict) and item.get('type')=='reasoning':continue
  def scrub(x):
   if isinstance(x,dict):return {k:scrub(v) for k,v in x.items() if k not in ['thinking','reasoning','encrypted_content','signature']}
   if isinstance(x,list):return [scrub(v) for v in x if not(isinstance(v,dict) and v.get('type') in ['thinking','reasoning'])]
   return x
  o=scrub(o);f.write(json.dumps(o)+'\n');f.flush();events+=1
  if o.get('type')=='system' and o.get('subtype')=='init':
   receipt['runtime_model']=o.get('model');receipt['session_id']=o.get('session_id')
  if o.get('type')=='thread.started':receipt['session_id']=o.get('thread_id')
  if o.get('type')=='result':
   for k in ['usage','modelUsage','duration_ms','total_cost_usd','is_error']:
    if k in o:receipt[k]=o[k]
   if isinstance(o.get('result'),str):messages.append(o['result'])
  if o.get('type')=='assistant':
   for b in o.get('message',{}).get('content',[]):
    if b.get('type')=='text':messages.append(b.get('text',''))
   if isinstance(o.get('text'),str):messages.append(o['text'])
  if o.get('type')=='item.completed' and item.get('type')=='agent_message':messages.append(item.get('text',''))
  if o.get('type')=='turn.completed':receipt['usage']=o.get('usage')
  receipt['events']=events
  (out/(tag+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
code=p.wait();err.close()
(out/(tag+'.stderr.txt')).write_text((w/'process.stderr.txt').read_text())
receipt.update(exit_code=code,status='completed' if code==0 else 'failed',finished_at=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
if (w/'final.md').exists():report=(w/'final.md').read_text()
else:report='\n\n'.join(dict.fromkeys(messages))
(out/(tag+'.md')).write_text(report)
receipt['report_chars']=len(report)
(out/(tag+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
