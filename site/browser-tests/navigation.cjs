/* Navigation acceptance checks; Python execution remains in smoke/studio. */
const assert=require('node:assert/strict');
const path=require('node:path');
const {withSite}=require('./harness.cjs');
withSite(async({browser,base})=>{
 const context=await browser.newContext({serviceWorkers:'block',viewport:{width:1440,height:1000}});
 const page=await context.newPage(),errors=[];
 page.on('pageerror',error=>errors.push(error.message));page.setDefaultTimeout(15000);
 const go=route=>page.goto(base+route);
 const primary=page.locator('#primary-navigation');
 const menu=page.locator('.menu-toggle');
 const sidebar=page.locator('#course-navigation');
 const noOverflow=async label=>assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),label);
 async function section(name){
  assert.deepEqual((await primary.getByRole('link').allTextContents()).map(text=>text.trim()),['Course','Assignments','Practice','Workspace','My Study']);
  assert.equal(await primary.locator('[aria-current="true"]').textContent(),name);
  assert.equal(await primary.locator('[aria-current="page"]').count(),0);
 }
 await go('index.html');await section('Course');
 await primary.getByRole('link',{name:'Assignments',exact:true}).click();await section('Assignments');
 await sidebar.getByRole('link',{name:/^Assignment 1/}).first().click();
 assert.equal(await sidebar.locator('[aria-current="page"]').count(),1);
 await page.getByRole('link',{name:'Read brief',exact:true}).click();await section('Assignments');
 assert.equal(new URL(await sidebar.locator('[aria-current="page"]').getAttribute('href'),page.url()).pathname,new URL(page.url()).pathname);
 await page.getByRole('link',{name:'Open original PDF preview',exact:true}).click();
 assert.equal(await sidebar.locator('[aria-current="page"]').count(),1);
 assert.equal(new URL(await sidebar.locator('[aria-current="page"]').getAttribute('href'),page.url()).pathname,new URL(page.url()).pathname);
 await go('view/week-3-demos/01_explore_data_types.py.html');await section('Course');
 assert.equal(await sidebar.locator('[aria-current="page"]').count(),1);
 assert.equal(new URL(await sidebar.locator('[aria-current="page"]').getAttribute('href'),page.url()).pathname,new URL(page.url()).pathname);
 await go('concepts.html');await section('Course');await go('updates.html');await section('Course');
 await go('study.html');await sidebar.getByRole('link',{name:'Study queue',exact:true}).click();
 assert.equal(new URL(page.url()).searchParams.get('show'),'queue');
 await page.waitForFunction(()=>document.querySelector('#study-filter').value==='queue');
 assert.equal(await sidebar.getByRole('link',{name:'Study queue',exact:true}).getAttribute('aria-current'),'location');
 await page.locator('#study-filter').selectOption('bookmarked');
 assert.equal(new URL(page.url()).searchParams.get('show'),'bookmarked');
 assert.equal(await sidebar.getByRole('link',{name:'Bookmarks',exact:true}).getAttribute('aria-current'),'location');
 console.log('PASS: five primary sections, contextual links, released lesson/assignment deep links and exact page selection.');

 await go('index.html');const before=await page.locator('#main').boundingBox();
 await page.locator('#section-toggle').click();assert.equal(await page.locator('body').getAttribute('data-navigation'),'collapsed');
 assert.equal(await page.evaluate(()=>Course.read('navigation',{}).collapsed),true);
 assert((await page.locator('#main').boundingBox()).width>before.width);
 await page.reload();assert.equal(await page.locator('body').getAttribute('data-navigation'),'collapsed');
 await page.locator('#section-toggle').click();assert.notEqual(await page.locator('body').getAttribute('data-navigation'),'collapsed');
 await go('workspace.html');await section('Workspace');
 assert.equal(await page.locator('body').getAttribute('data-layout'),'embedded');assert(!(await sidebar.isVisible()));
 assert(await page.locator('.project-files').isVisible());
 await page.locator('#new-file-name').fill('navigation.py');await page.locator('#add-file').click();
 await page.locator('#workspace-editor').fill('print("saved through navigation")');
 await go('practice.html');await section('Practice');
 assert.equal(await page.locator('body').getAttribute('data-layout'),'embedded');assert(!(await sidebar.isVisible()));
 await page.locator('#activity-list button').nth(1).waitFor();assert(await page.locator('#activity-list').isVisible());await page.locator('#activity-list button').nth(1).click();
 console.log('PASS: persistent collapsible context sidebar and dedicated workspace/practice panels.');

 for(const width of [1440,1024,800,390,320]){
  await page.setViewportSize({width,height:900});
  for(const route of ['index.html','assignments/assignment-1.html','workspace.html','practice.html']){
   await go(route);await noOverflow(`${route} at ${width}px`);
  }
 }
 await page.setViewportSize({width:390,height:844});await go('index.html');
 assert(!(await primary.isVisible()));assert.equal(await primary.evaluate(element=>element.inert),true);
 assert.equal(await sidebar.evaluate(element=>element.inert),true);
 await menu.click();assert.equal(await menu.getAttribute('aria-expanded'),'true');
 assert.equal(await sidebar.evaluate(element=>element.inert),false);assert.equal(await page.locator('#main').evaluate(element=>element.inert),true);
 await page.waitForFunction(()=>document.querySelector('#course-navigation').contains(document.activeElement));
 const drawerPrimary=page.locator('.mobile-primary-navigation');
 assert.equal(await drawerPrimary.getAttribute('aria-label'),'Primary sections');assert.equal(await drawerPrimary.getByRole('link').count(),5);
 await page.keyboard.press('Shift+Tab');assert(await sidebar.evaluate(element=>element.contains(document.activeElement)));
 await page.keyboard.press('Tab');assert(await sidebar.evaluate(element=>element.contains(document.activeElement)));
 for(let step=0;step<24;step++){await page.keyboard.press('Tab');assert(await sidebar.evaluate(element=>element.contains(document.activeElement)),'Tab must stay inside the open drawer');}
 await page.keyboard.press('Escape');assert.equal(await menu.getAttribute('aria-expanded'),'false');
 assert.equal(await page.locator('#main').evaluate(element=>element.inert),false);assert(await menu.evaluate(element=>element===document.activeElement));
 await menu.click();assert.equal(await menu.getAttribute('aria-expanded'),'true');await menu.click();
 assert.equal(await menu.getAttribute('aria-expanded'),'false');assert.equal(await page.locator('#main').evaluate(element=>element.inert),false);
 assert.equal(await sidebar.evaluate(element=>element.inert),true);assert(await menu.evaluate(element=>element===document.activeElement));
 await menu.click();await page.locator('#navigation-backdrop').click({position:{x:385,y:750}});
 assert.equal(await menu.getAttribute('aria-expanded'),'false');
 await menu.click();await drawerPrimary.getByRole('link',{name:'Practice',exact:true}).click();
 assert.equal(new URL(page.url()).pathname,new URL(base+'practice.html').pathname);assert.equal(await menu.getAttribute('aria-expanded'),'false');
 await page.locator('#activity-topic').selectOption('loops');
 assert.equal(new URL(page.url()).searchParams.get('topic'),'loops');
 await menu.click();const topicLink=sidebar.locator('nav[aria-label="Practice topics"] a[aria-current="location"]');
 assert.equal(await topicLink.count(),1);assert((await topicLink.getAttribute('href')).includes('topic=loops'));
 await page.keyboard.press('Escape');
 const activitySelect=page.locator('#activity-select');await activitySelect.locator('option').nth(1).waitFor({state:'attached'});
 const secondActivity=await activitySelect.locator('option').nth(1).getAttribute('value');
 await activitySelect.selectOption(secondActivity);
 assert.equal(await activitySelect.inputValue(),secondActivity);assert(await page.locator('#activity-detail').isVisible());
 const selectedActivity=await activitySelect.locator('option:checked').textContent();
 assert((await page.locator('#activity-detail').textContent()).includes(selectedActivity.trim()));
 await go('workspace.html');const fileSelect=page.locator('#workspace-file-select');await fileSelect.selectOption('navigation.py');
 assert.equal(await page.locator('#workspace-editor').inputValue(),'print("saved through navigation")');
 await page.locator('#workspace-editor').fill('print("mobile selection works")');
 await fileSelect.selectOption('main.py');await fileSelect.selectOption('navigation.py');
 assert.equal(await page.locator('#workspace-editor').inputValue(),'print("mobile selection works")');
 await page.locator('#workspace-editor').focus();await page.keyboard.press('Tab');
 assert(!(await page.locator('#workspace-editor').evaluate(element=>element===document.activeElement)));
 await noOverflow('mobile editor with selected project file');
 await menu.click();await page.setViewportSize({width:1440,height:1000});
 await page.waitForFunction(()=>document.querySelector('#primary-navigation [aria-current="true"]')===document.activeElement);
 await page.setViewportSize({width:390,height:844});await page.waitForFunction(()=>document.querySelector('.menu-toggle')===document.activeElement);
 for(let crossing=0;crossing<3;crossing++){
  await page.setViewportSize({width:1440,height:1000});
  await page.waitForFunction(()=>document.querySelector('#primary-navigation [aria-current="true"]')===document.activeElement);
  await page.setViewportSize({width:390,height:844});
  await page.waitForFunction(()=>document.querySelector('.menu-toggle')===document.activeElement);
 }
 await go('view/week-3-demos/01_explore_data_types.py.html');await page.setViewportSize({width:1440,height:1000});
 await sidebar.locator('[aria-current="page"]').focus();
 await page.waitForFunction(()=>document.querySelector('#course-navigation [aria-current="page"]')===document.activeElement);
 await page.setViewportSize({width:390,height:844});
 await page.waitForFunction(()=>document.querySelector('.menu-toggle')===document.activeElement);
 await page.setViewportSize({width:1440,height:1000});
 await page.waitForFunction(()=>document.querySelector('#primary-navigation [aria-current="true"]')===document.activeElement);
 await page.locator('#section-toggle').focus();await page.setViewportSize({width:390,height:844});
 await page.waitForFunction(()=>document.querySelector('.menu-toggle')===document.activeElement);
 await go('workspace.html');await page.setViewportSize({width:1440,height:1000});await page.locator('#workspace-editor').focus();
 await page.waitForFunction(()=>document.querySelector('#workspace-editor')===document.activeElement);
 await page.setViewportSize({width:390,height:844});
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 assert(await page.locator('#workspace-editor').evaluate(element=>element===document.activeElement),'Resize must preserve focus in an editor that stays available');
 await menu.focus();await page.setViewportSize({width:1440,height:1000});
 await page.waitForFunction(()=>document.querySelector('#primary-navigation [aria-current="true"]')===document.activeElement);
 await page.setViewportSize({width:390,height:844});await page.waitForFunction(()=>document.querySelector('.menu-toggle')===document.activeElement);
 if(process.env.SCREENSHOT_DIR){await page.screenshot({path:path.join(process.env.SCREENSHOT_DIR,'navigation-workspace-mobile.png'),fullPage:true});await go('index.html');await menu.click();await page.screenshot({path:path.join(process.env.SCREENSHOT_DIR,'navigation-drawer-mobile.png')});await page.keyboard.press('Escape');await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:path.join(process.env.SCREENSHOT_DIR,'navigation-desktop.png'),fullPage:true});}
 const staticContext=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844},serviceWorkers:'block'});
 const staticPage=await staticContext.newPage();await staticPage.goto(base);
 assert(await staticPage.locator('#primary-navigation').isVisible());
 assert(!(await staticPage.getByRole('button',{name:'Toggle navigation',exact:true}).isVisible()));
 await staticPage.locator('#primary-navigation').getByRole('link',{name:'Assignments',exact:true}).click();
 assert(await staticPage.getByRole('heading',{name:'Assignments',exact:true}).isVisible());
 assert(await staticPage.locator('#course-navigation').isVisible());
 await staticPage.locator('#course-navigation').getByRole('link',{name:'Assignment 1',exact:true}).click();
 assert(await staticPage.getByRole('link',{name:'Read brief',exact:true}).isVisible());
 assert(await staticPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await staticContext.close();assert.deepEqual(errors,[]);await context.close();
 console.log('PASS: 320–1440px layout, accessible drawer/focus/backdrop, section switching, compact activity/file selectors, usable saved editor and navigation without JavaScript.');
}).catch(error=>{console.error(error);process.exitCode=1;});
