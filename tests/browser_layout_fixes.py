"""First-screen fit, sidebar scroll bounds and workspace account controls."""
from pathlib import Path
import sys, shutil, threading
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from playwright.sync_api import sync_playwright, expect
from werkzeug.serving import make_server


def run():
    app=create_app()
    app.extensions['accounts'].create('layout@example.test','Layout-test-password-123','Demo Layout Student','STUDENT')
    server=make_server('127.0.0.1',0,app)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    output=Path('artifacts/layout-fixes'); output.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True)
        page=browser.new_page()
        errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            for width,height in [(1366,768),(1440,900),(1280,720),(1024,600),(390,844),(360,640),(320,568)]:
                page.set_viewport_size({'width':width,'height':height})
                page.goto(base+'/'); page.evaluate('document.fonts.ready')
                for selector in ['.hero-primary','.hero-demo','.scroll-cue']:
                    rect=page.locator(selector).bounding_box()
                    assert rect['y']+rect['height']<=height,(width,height,selector,rect)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                if width <= 600:
                    boxes=[page.locator(selector).bounding_box() for selector in ['.public-brand','.public-account','.public-menu']]
                    assert max(box['y'] for box in boxes)<min(box['y']+box['height'] for box in boxes)
                    expect(page.locator('.public-account')).to_contain_text('Sign in')
                    expect(page.locator('.public-account')).to_contain_text('Get started')
                if width in [1366,390]: page.screenshot(path=str(output/f'homepage-{width}.png'))
            for height in [500,640,900]:
                page.set_viewport_size({'width':1440,'height':height})
                page.goto(base+'/dashboard')
                sidebar=page.locator('.sidebar')
                sidebar.evaluate('(e)=>e.scrollTop=e.scrollHeight')
                # Exercise a scrolled expanded menu, then bring its toggle into view.
                page.locator('.sidebar-toggle').scroll_into_view_if_needed()
                page.locator('.sidebar-toggle').click()
                expect(sidebar).to_have_css('width','72px')
                assert sidebar.evaluate('(e)=>e.scrollHeight<=e.clientHeight && e.scrollTop===0')
                expect(page.locator('.sidebar-note')).to_be_hidden()
                expect(page.locator('.sidebar-toggle')).to_have_css('left','14px')
                expect(page.locator('.rail-link')).to_have_count(4)
                if height==640: page.screenshot(path=str(output/'collapsed-menu.png'))
                page.locator('.sidebar-toggle').click()
                expect(sidebar).to_have_css('width','240px')
                expect(page.locator('.sidebar-note')).to_be_visible()
            # Guest workspace also has exactly the requested three control groups.
            for width in [320,390,1024,1440]:
                page.set_viewport_size({'width':width,'height':844})
                page.goto(base+'/dashboard')
                expect(page.locator('.topbar a[href="/login"], .topbar a[href="/register"]')).to_have_count(0)
                expect(page.locator('.topbar-actions > *')).to_have_count(3)
                page.locator('.account-menu summary').click()
                expect(page.locator('.account-panel')).to_be_visible()
                page.keyboard.press('Escape')
                expect(page.locator('.account-panel')).to_be_hidden()
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.goto(base+'/login')
            page.get_by_label('Email',exact=True).fill('layout@example.test')
            page.get_by_label('Password',exact=True).fill('Layout-test-password-123')
            page.get_by_role('button',name='Sign in',exact=True).click()
            expect(page).to_have_url(base+'/dashboard')
            page.locator('.account-menu summary').click()
            expect(page.get_by_role('button',name='Sign out')).to_be_visible()
            page.screenshot(path=str(output/'account-menu.png'))
            page.get_by_role('button',name='Sign out').click()
            expect(page.locator('.public-home')).to_be_visible()
            assert not errors,errors
            print('PASS: first-screen CTA/cue fit at 7 viewport sizes, collapsed rail scroll bounds, 3 header controls, guest/auth account menu and sign-out.')
        finally:
            browser.close();server.shutdown()

if __name__=='__main__': run()
