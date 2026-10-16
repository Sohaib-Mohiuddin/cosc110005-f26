const runtimeURL = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs';
const validPath = path => typeof path === 'string' && path.length <= 240 && !/[\x00-\x1f\x7f\\:*?"<>|]/.test(path) && !path.split('/').some(part => !part || part === '.' || part === '..' || part.startsWith('.'));
self.onmessage = async ({data}) => {
  let pending = '', size = 0, started = false;
  const flush = () => { if (pending) self.postMessage({type: 'output', text: pending}); pending = ''; };
  try {
    const {loadPyodide} = await import(runtimeURL);
    const py = await loadPyodide();
    const decoder = new TextDecoder();
    const write = bytes => {
      size += bytes.length;
      if(size > 65536){const message='Output limit reached (64 KB). Reduce printing and try again.';flush();self.postMessage({type:'error',text:message});throw new Error(message);}
      pending += decoder.decode(bytes,{stream:true});if(pending.length>=2048||pending.includes('\n'))flush();return bytes.length;
    };
    py.setStdout({write});py.setStderr({write});
    const input=String(data.stdin||'').replace(/\r\n?/g,'\n'),lines=input===''?[]:input.split('\n');if(input.endsWith('\n'))lines.pop();py.setStdin({stdin:()=>lines.shift()});
    const initial=new Map();
    for(const file of data.files||[]){if(!validPath(file.path))throw new Error('Unsupported project path.');const path='/course/'+file.path;py.FS.mkdirTree(path.substring(0,path.lastIndexOf('/')));const bytes=new Uint8Array(file.bytes);py.FS.writeFile(path,bytes);initial.set(path,bytes);}
    if(!validPath(data.path))throw new Error('Unsupported entry-point path.');
    const selectedPath='/course/'+data.path;py.FS.mkdirTree(selectedPath.substring(0,selectedPath.lastIndexOf('/')));const selectedBytes=new TextEncoder().encode(data.code);py.FS.writeFile(selectedPath,selectedBytes);initial.set(selectedPath,selectedBytes);
    py.globals.set('_runner_payload',JSON.stringify({code:data.code,path:data.path,overrides:data.overrides||{},trace:!!data.trace,syntaxOnly:!!data.syntaxOnly,assertions:data.assertions||[],directories:[...new Set((data.files||[]).map(file=>'/course/'+file.path.substring(0,file.path.lastIndexOf('/')+1)))]}));
    const driver=await fetch(new URL('runtime.py',import.meta.url));if(!driver.ok)throw new Error('The Python driver could not load.');
    started=true;self.postMessage({type:'running'});
    const result=JSON.parse(await py.runPythonAsync(await driver.text()));
    flush();
    const files=[];let total=0,visited=0;
    const collect=(directory,depth=0)=>{if(depth>12)return;for(const name of py.FS.readdir(directory)){if(name==='.'||name==='..'||++visited>300)continue;const path=directory+'/'+name,stat=py.FS.lstat(path);if(py.FS.isLink(stat.mode))continue;if(py.FS.isDir(stat.mode))collect(path,depth+1);else if(files.length<50&&stat.size<=2000000&&total+stat.size<=4000000){const bytes=py.FS.readFile(path),before=initial.get(path);if(!before||before.length!==bytes.length||bytes.some((byte,index)=>byte!==before[index])){files.push({path:path.slice('/course/'.length),bytes});total+=bytes.length;}}}};
    if(!data.syntaxOnly)collect('/course');
    result.files=files;
    if(result.error)self.postMessage({type:'error',text:result.errorText,result});else self.postMessage({type:'done',result});
  }catch(error){flush();self.postMessage({type:'error',text:(started?'':'Python could not load. Check your connection and retry, or download the lesson for desktop Python.\n')+String(error.message||error)});}
};
