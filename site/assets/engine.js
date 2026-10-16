(() => {
  const C=window.Course;
  C.run = options => {
    let cancel;
    const promise=new Promise(resolve=>{
      let worker,finished=false,timer,text='';
      const finish=(error='',extras={})=>{if(finished)return;finished=true;clearTimeout(timer);worker?.terminate();resolve({...extras,text,error,detail:extras.error});};
      cancel=()=>finish('Stopped. Edit your code and run again.');
      options.onState?.('loading');timer=setTimeout(()=>finish('Python could not load within 60 seconds. Check your connection and retry, or download the lesson.'),60000);
      Promise.resolve(options.files||[]).then(files=>{
        if(finished)return;worker=new Worker(new URL('assets/python-worker.mjs',C.base),{type:'module'});
        worker.onerror=event=>{event.preventDefault();finish('Python could not start. Check your connection and retry, or use desktop Python.');};
        worker.onmessage=({data})=>{
          if(finished)return;
          if(data.type==='running'){clearTimeout(timer);timer=setTimeout(()=>finish('Stopped after 10 seconds. Check loop conditions and stop values, then try again.'),10000);options.onState?.('running');}
          else if(data.type==='output'){if(text.length+data.text.length>65536)return finish('Output limit reached (64 KB). Reduce printing and try again.');text+=data.text;options.onOutput?.(text);}
          else if(data.type==='done')finish('',data.result||{});
          else if(data.type==='error')finish(data.text,data.result||{});
        };
        worker.postMessage({...options,files,onState:undefined,onOutput:undefined});
      }).catch(error=>finish(error.message));
    });
    promise.cancel=()=>cancel?.();return promise;
  };
  C.loadFiles=async files=>Promise.all(files.map(async file=>{const response=await fetch(file.url,{signal:AbortSignal.timeout(30000)});if(!response.ok)throw new Error('Could not load '+file.path+'. Download the lesson ZIP or retry.');return {path:file.path,bytes:await response.arrayBuffer()};}));
  C.traceView=(host,result,source)=>{
    host.courseCleanup?.();host.replaceChildren();host.hidden=false;const frames=result.trace||[];
    if(!frames.length){host.append(C.el('p',{text:'No trace steps were captured. Run Trace with a short Python program.'}));return;}
    let index=0,interval;
    const title=C.el('p',{role:'status'}),code=C.el('pre',{class:'trace-code',tabindex:'0'}),table=C.el('table'),body=C.el('tbody');
    table.append(C.el('thead',{},C.el('tr',{},C.el('th',{text:'Variable'}),C.el('th',{text:'Value before this line'}))),body);
    const previous=C.el('button',{class:'button small',type:'button',text:'Previous step'}),next=C.el('button',{class:'button small',type:'button',text:'Next step'}),play=C.el('button',{class:'button small',type:'button',text:'Play trace'}),range=C.el('input',{type:'range',min:'0',max:String(frames.length-1),value:'0','aria-label':'Trace step'});
    const draw=()=>{const step=frames[index];title.textContent=`Step ${index+1} of ${frames.length} · ${step.event==='return'?'Return from':'Before'} line ${step.line} · ${step.function === '<module>' ? 'program' : step.function} · ${step.path.replace(/^projects\/[^/]+\//, '')}${result.traceLimited?' · Trace limit reached':''}`;range.value=index;previous.disabled=index===0;next.disabled=index===frames.length-1;code.replaceChildren();const lines=(step.path===result.path?source:result.sources?.[step.path]||'').split('\n');lines.forEach((line,n)=>code.append(C.el('span',{class:n+1===step.line?'trace-current':'',text:`${n+1}  ${line}`})));body.replaceChildren();for(const [name,value]of Object.entries(step.variables)){const changed=index>0&&frames[index-1].variables[name]!==value;body.append(C.el('tr',{class:changed?'variable-changed':''},C.el('td',{text:name}),C.el('td',{text:value})));}if(!body.children.length)body.append(C.el('tr',{},C.el('td',{colspan:'2',text:'No values assigned in this frame yet.'})));};
    const pause=()=>{clearInterval(interval);play.textContent='Play trace';interval=null;};host.courseCleanup=pause;previous.onclick=()=>{pause();index=Math.max(0,index-1);draw();};next.onclick=()=>{pause();index=Math.min(frames.length-1,index+1);draw();};range.oninput=()=>{pause();index=Number(range.value);draw();};play.onclick=()=>{if(interval)return pause();if(index===frames.length-1)index=0;play.textContent='Pause trace';interval=setInterval(()=>{if(index>=frames.length-1)return pause();index++;draw();},700);};
    host.append(C.el('h3',{text:'Trace replay'}),C.el('p',{text:'Replay a captured run. Values are shown before each highlighted line; return steps show final local values. Traces stop at 300 steps.'}),C.el('div',{class:'runner-actions'},previous,play,next),range,title,code,C.el('div',{class:'table-scroll'},table));draw();
  };
})();
