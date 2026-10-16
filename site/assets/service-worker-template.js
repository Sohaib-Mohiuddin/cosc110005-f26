const VERSION='__COURSE_VERSION__';
const SHELL=__COURSE_SHELL__;
const ROOT=new URL('./',self.location.href);
const CACHE='cosc-shell-'+ROOT.pathname+'-'+VERSION;
const PYTHON='cosc-python-314.0.7';
const isPython=url=>url.origin==='https://cdn.jsdelivr.net'&&url.pathname.startsWith('/pyodide/v314.0.7/full/');
self.addEventListener('install',event=>event.waitUntil((async()=>{const cache=await caches.open(CACHE);await Promise.all(SHELL.map(async path=>{const response=await fetch(new URL(path,ROOT),{cache:'reload'});if(!response.ok)throw new Error('Could not save course tools: '+path);await cache.put(new URL(path,ROOT),response);}));await self.skipWaiting();})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('cosc-shell-'+ROOT.pathname+'-')&&key!==CACHE)await caches.delete(key);await self.clients.claim();})()));
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;const url=new URL(event.request.url);
  if(isPython(url)){event.respondWith((async()=>{const cache=await caches.open(PYTHON),saved=await cache.match(event.request);if(saved)return saved;const response=await fetch(event.request);if(response.ok)await cache.put(event.request,response.clone());return response;})());return;}
  if(url.origin!==ROOT.origin||!url.pathname.startsWith(ROOT.pathname))return;
  event.respondWith((async()=>{const cache=await caches.open(CACHE),key=new URL(url);key.search='';if(key.pathname===ROOT.pathname)key.pathname+='index.html';const saved=await cache.match(key);try{const response=await fetch(event.request);if(response.ok&&(saved||SHELL.some(path=>new URL(path,ROOT).pathname===url.pathname)))await cache.put(key,response.clone());return response;}catch(error){if(saved)return saved;if(event.request.mode==='navigate')return Response.redirect(new URL('offline.html',ROOT).href,302);throw error;}})());
});
self.addEventListener('message',event=>{const reply=value=>event.ports[0]?.postMessage(value);event.waitUntil((async()=>{try{
  if(event.data.type==='SAVE_PACK'){
    const manifest=await (await fetch(new URL('offline-manifest.json',ROOT))).json();const pack=manifest.packs.find(pack=>pack.id===event.data.id);if(!pack)throw new Error('This lesson pack is not in the released course.');if(manifest.version!==VERSION)throw new Error('The course has updated. Reload this page before saving the new pack.');const cache=await caches.open(CACHE);let count=0;
    for(const path of pack.urls){const url=new URL(path,ROOT);if(url.origin!==ROOT.origin||!url.pathname.startsWith(ROOT.pathname))throw new Error('Unsupported pack URL.');const response=await fetch(url);if(!response.ok)throw new Error('Could not save '+path+'. Reconnect and retry.');await cache.put(url,response);count++;}await cache.put(new URL('__pack__/'+pack.id,ROOT),new Response(JSON.stringify({id:pack.id,version:VERSION}),{headers:{'Content-Type':'application/json'}}));reply({ok:true,count,version:VERSION});
  }else if(event.data.type==='STATUS'){
    const python=await caches.open(PYTHON),urls=(await python.keys()).map(request=>request.url);const course=await caches.open(CACHE),packs=(await course.keys()).filter(request=>new URL(request.url).pathname.startsWith(ROOT.pathname+'__pack__/')).map(request=>new URL(request.url).pathname.split('/').pop());reply({version:VERSION,packs,pythonReady:['pyodide.mjs','pyodide.asm.mjs','pyodide.asm.wasm','python_stdlib.zip'].every(name=>urls.some(url=>url.endsWith('/'+name)))});
  }else if(event.data.type==='REMOVE_PACKS'){
    const cache=await caches.open(CACHE);for(const request of await cache.keys()){if(!SHELL.some(path=>new URL(path,ROOT).href===request.url))await cache.delete(request);}reply({ok:true});
  }else reply({error:'Unknown offline operation.'});
}catch(error){reply({error:error.message});}})());});
