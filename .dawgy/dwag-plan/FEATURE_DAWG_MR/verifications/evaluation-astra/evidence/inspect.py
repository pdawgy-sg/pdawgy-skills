from pathlib import Path
import hashlib,json,os,subprocess
root=Path('/tmp/dawg-mr-astra-eval')
def fingerprint(p):
 return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file()}
for name in ('project','ambiguous'):
 (root/f'evidence/{name}-before.json').write_text(json.dumps(fingerprint(root/name),indent=2)+'\n')
records=[]
def git(p,*args):
 r=subprocess.run(['git',*args],cwd=root/p,text=True,capture_output=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
 record={'project':p,'argv':['git',*args],'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}; records.append(record)
 print(json.dumps(record,indent=2));assert r.returncode==0
 return r.stdout.strip()
p='project';git(p,'rev-parse','--show-toplevel');git(p,'status','--porcelain=v1');git(p,'show','HEAD:AGENTS.md')
base=git(p,'rev-parse','main^{commit}');head=git(p,'rev-parse','HEAD^{commit}');comparison=git(p,'merge-base',base,head)
git(p,'log','--oneline',comparison+'..'+head);git(p,'diff','--stat',comparison,head);git(p,'diff',comparison,head)
for name in ['.gitlab/merge_request_templates/Default.md','REQUEST.md','average.py','summary.py','check_empty.py','check_legacy.py','check_nonempty.py','verification/records.json']:
 git(p,'show',head+':'+name)
git(p,'diff','--stat',head,head)
p='ambiguous';git(p,'status','--porcelain=v1');git(p,'branch','-avv');git(p,'remote','-v');git(p,'ls-tree','-r','--name-only','HEAD');git(p,'log','--all','--oneline','--decorate')
(root/'evidence/runtime-commands.json').write_text(json.dumps(records,indent=2)+'\n')
for name in ('project','ambiguous'):
 after=fingerprint(root/name)
 before=json.loads((root/f'evidence/{name}-before.json').read_text())
 assert after==before,name
 (root/f'evidence/{name}-after.json').write_text(json.dumps(after,indent=2)+'\n')
print('Both complete fixture file fingerprints, including .git, unchanged.')
