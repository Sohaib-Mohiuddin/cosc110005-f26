const {spawn}=require('node:child_process');
const path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
exports.withSite=async run=>{
  let server,browser;
  try{
    let base=process.env.SITE_BASE_URL;
    if(!base){
      server=spawn('python3',['-u','-c',`
import http.server,sys
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=sys.argv[1],**kwargs)
    def do_GET(self):
        if not self.path.startswith('/cosc110005-f26/'): self.send_error(404); return
        self.path=self.path[len('/cosc110005-f26'):]; super().do_GET()
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
print(server.server_port,flush=True)
server.serve_forever()
`,process.env.SITE_OUTPUT||path.resolve(__dirname,'../../_site')],{stdio:['ignore','pipe','pipe']});
      const port=await new Promise((resolve,reject)=>{server.stdout.once('data',data=>resolve(Number(data.toString().trim())));server.once('error',reject);server.once('exit',code=>reject(new Error('Preview exited: '+code)));});
      base=`http://127.0.0.1:${port}/cosc110005-f26/`;
    }
    browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
    await run({browser,base});
  }finally{await browser?.close();server?.kill();}
};
