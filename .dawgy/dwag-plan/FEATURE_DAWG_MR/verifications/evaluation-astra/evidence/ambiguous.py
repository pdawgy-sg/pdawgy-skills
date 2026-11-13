from pathlib import Path
import subprocess,json,os,hashlib
root=Path('/tmp/dawg-mr-astra-eval');p=root/'ambiguous-material';p.mkdir()
setup=[];runtime=[]
def run(args,records):
 r=subprocess.run(['git',*args],cwd=p,text=True,capture_output=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
 records.append({'argv':['git',*args],'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,r.stderr
 return r.stdout.strip()
for a in [('init','-b','release-a'),('config','user.name','Fixture Author'),('config','user.email','fixture@example.invalid')]:run(a,setup)
(p/'value.txt').write_text('one\n');run(['add','.'],setup);run(['commit','-m','chore: initial'],setup)
run(['switch','-c','release-b'],setup);(p/'value.txt').write_text('two\n');run(['add','.'],setup);run(['commit','-m','feat: second value'],setup)
run(['switch','-c','feature/value'],setup);(p/'label.txt').write_text('value label\n');run(['add','.'],setup);run(['commit','-m','feat: add label'],setup)
def fp():return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file()}
before=fp()
for a in [('status','--porcelain=v1'),('branch','-avv'),('remote','-v'),('ls-tree','-r','--name-only','HEAD'),('log','--all','--oneline','--decorate'),('diff','--stat','release-a','HEAD'),('diff','--stat','release-b','HEAD')]:
 run(a,runtime)
after=fp();assert before==after
for name,obj in [('ambiguous-material-setup',setup),('ambiguous-material-runtime',runtime),('ambiguous-material-before',before),('ambiguous-material-after',after)]:
 (root/f'evidence/{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(runtime,indent=2))
