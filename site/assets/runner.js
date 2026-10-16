(() => {
  const panel=document.querySelector('#python-runner');if(!panel)return;
  const C=window.Course,data=JSON.parse(document.querySelector('#runner-data').textContent),get=id=>document.getElementById(id);
  const editor=get('python-editor'),input=get('python-input'),output=get('python-output'),status=get('runner-status'),saveStatus=get('save-status'),run=get('run-python'),stop=get('stop-python'),reset=get('reset-python'),check=get('check-python'),results=get('check-results'),original=get('source-code').textContent;
  const storageKey=`cosc-practice:${C.base.pathname}:${data.path}`;
  let busy=false,execution=null,cancelled=false,filesPromise,saveTimer;
  panel.hidden=false;editor.value=original;input.value=data.cases[0]?.stdin||'';
  try{const saved=JSON.parse(localStorage.getItem(storageKey));if(saved&&typeof saved.code==='string'){editor.value=saved.code;input.value=typeof saved.stdin==='string'?saved.stdin:'';saveStatus.textContent=saved.original!==original?'Restored your copy. The course example has changed; Reset code loads the updated original.':'Restored your saved copy from this browser.';}}catch{saveStatus.textContent='Browser saving is unavailable. Download your code to keep it.';}
  C.enhanceEditor(editor);
  function save(){clearTimeout(saveTimer);try{localStorage.setItem(storageKey,JSON.stringify({code:editor.value,stdin:input.value,original}));saveStatus.textContent='Saved on this browser. Download a copy to use another device.';}catch{saveStatus.textContent='Could not save in this browser. Download your code to keep it.';}}
  for(const control of[editor,input])control.addEventListener('input',()=>{clearTimeout(saveTimer);saveTimer=setTimeout(save,300);});window.addEventListener('pagehide',save);
  function setBusy(value){busy=value;for(const button of[run,reset,check,get('trace-python'),get('lesson-test')])if(button)button.disabled=value;stop.disabled=!value;panel.setAttribute('aria-busy',String(value));}
  function files(){if(!filesPromise)filesPromise=C.loadFiles(data.files).catch(error=>{filesPromise=null;throw error;});return filesPromise;}
  function execute(code,stdin,overrides={},extra={}){execution=C.run({code,stdin,overrides,path:data.path,files:files(),...extra,onOutput:text=>output.textContent=text,onState:state=>status.textContent=state==='loading'?'Loading Python and lesson files… The first run may take a little longer.':'Running…'});return execution;}
  function showError(result){output.textContent+='\n'+result.error;if(result.error.includes('EOFError'))output.textContent+='\nAdd the missing answers to Program input, one per line, then run again.';C.showError(get('runner-error'),result.error,result.detail,editor);}
  async function start(kind='run'){
    if(busy)return;save();cancelled=false;setBusy(true);output.textContent='';results?.replaceChildren();get('runner-trace').hidden=true;C.showError(get('runner-error'),'');
    const code=editor.value;
    try{
      if(kind==='checks'){
        let passed=0;for(const[index,sample]of data.cases.entries()){if(cancelled)break;output.textContent='';const result=await execute(code,sample.stdin||'',sample.overrides||{},{assertions:sample.assertions||[]});const comparison=C.compare(result.text,sample),ok=!result.error&&comparison.ok&&(result.checks||[]).every(check=>check.ok);if(ok)passed++;const row=C.el('li',{class:ok?'check-pass':'check-fail',text:`Case ${index+1}${sample.label?': '+sample.label:''} — ${ok?'Passed':result.error?'Could not complete':comparison.reason}`});const details=C.el('details',{},C.el('summary',{text:'Expected and actual output'}),C.el('h4',{text:'Expected'}),C.el('pre',{text:String(comparison.expected)}),C.el('h4',{text:'Actual'}),C.el('pre',{text:(result.text+(result.error?'\n'+result.error:''))||'(no output)'}));for(const value of result.checks||[])details.append(C.el('p',{text:`${value.expression}: expected ${value.expected}; actual ${value.actual}`}));row.append(details);results.append(row);if(result.error)showError(result);}
        status.textContent=cancelled?'Checks stopped.':`${passed} of ${data.cases.length} sample checks passed. Review the requirements too; these checks are not a grade.`;
      }else{
        const result=await execute(code,input.value,{}, {trace:kind==='trace'});if(result.error)showError(result);status.textContent=result.error?(cancelled?'Stopped.':'Run finished with an error. See Output.'):'Run complete.';if(kind==='trace')C.traceView(get('runner-trace'),result,code);
        if(kind==='test'){const comparison=C.compare(result.text,{mode:get('lesson-mode').value,expected:get('lesson-expected').value,tolerance:Number(get('lesson-tolerance').value)}),host=get('lesson-test-result');host.replaceChildren(C.el('p',{class:comparison.ok&&!result.error?'check-pass':'check-fail',text:result.error?'The program could not complete.':comparison.reason}),C.el('div',{class:'custom-test-output'},C.el('section',{},C.el('h4',{text:'Expected'}),C.el('pre',{text:String(comparison.expected)})),C.el('section',{},C.el('h4',{text:'Actual'}),C.el('pre',{text:result.text||'(no output)'}))));}
      }
    }finally{setBusy(false);execution=null;}
  }
  run.onclick=()=>start();get('trace-python').onclick=()=>start('trace');check?.addEventListener('click',()=>start('checks'));get('lesson-test').onclick=()=>start('test');stop.onclick=()=>{cancelled=true;execution?.cancel();};
  reset.onclick=()=>{if(!confirm('Replace your saved edits with the original course code? Download your code first if you want to keep it.'))return;editor.value=original;editor.courseRender();input.value=data.cases[0]?.stdin||'';output.textContent='';results?.replaceChildren();status.textContent='Original code restored.';save();editor.focus();editor.setSelectionRange(0,0);editor.scrollTop=0;};
  get('download-python').onclick=()=>{save();C.download(data.path.split('/').pop(),editor.value,'text/x-python;charset=utf-8');};
  editor.addEventListener('keydown',event=>{if((event.ctrlKey||event.metaKey)&&event.key==='Enter'){event.preventDefault();start();}});
})();
