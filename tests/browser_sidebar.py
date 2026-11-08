"""Verify the two-state sidebar geometry, icons and keyboard behavior."""
from pathlib import Path
import sys, shutil, threading
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from playwright.sync_api import sync_playwright, expect
from werkzeug.serving import make_server


def run():
    server=make_server('127.0.0.1',0,create_app())
    threading.Thread(target=server.serve_forever,daemon=True).start()
    output=Path('artifacts/sidebar'); output.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:errors.append(r.url) if r.status>=400 else None)
        base=f'http://127.0.0.1:{server.server_port}'
        def anchors():
            return page.locator('.sidebar-toggle, .rail-icon').evaluate_all('(els)=>els.map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y]})')
        try:
            for width in [901,1024,1440,1920]:
                page.set_viewport_size({'width':width,'height':900})
                page.goto(base+'/dashboard',wait_until='networkidle')
                sidebar=page.locator('#workspace-sidebar')
                expect(sidebar).to_have_css('width','240px')
                expect(sidebar).to_have_css('background-color','rgb(21, 34, 61)')
                expect(sidebar.locator('.rail-link')).to_have_count(4)
                initial=anchors()
                if width==1440:
                    page.screenshot(path=str(output/'expanded-desktop.png'))
                    sidebar.screenshot(path=str(output/'expanded-rail.png'))
                button=page.locator('.sidebar-toggle')
                button.focus(); page.keyboard.press('Enter')
                expect(sidebar).to_have_css('width','72px')
                assert anchors()==initial
                expect(button).to_be_focused()
                expect(page.get_by_role('link',name='Dashboard',exact=True).first).to_be_visible()
                expect(sidebar.locator('.rail-label').first).to_have_css('opacity','0')
                assert not sidebar.evaluate('(e)=>e.inert')
                assert sidebar.locator('img').evaluate_all('(els)=>els.every(e=>e.complete && e.naturalWidth>0)')
                assert sidebar.locator('.rail-icon svg').evaluate_all('(els)=>els.length===4 && els.every(e=>e.getBBox().width>0)')
                if width==1440:
                    page.screenshot(path=str(output/'collapsed-desktop.png'))
                    sidebar.screenshot(path=str(output/'collapsed-rail.png'))
                page.keyboard.press('Space')
                expect(sidebar).to_have_css('width','240px')
                assert anchors()==initial
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.goto(base+'/profile')
            expect(page.get_by_role('navigation',name='Main navigation').get_by_role('link',name='Settings')).to_have_attribute('aria-current','page')
            page.get_by_role('button',name='Collapse navigation menu').click()
            expect(page.locator('.sidebar')).to_have_css('width','72px')
            page.set_viewport_size({'width':390,'height':844})
            expect(page.locator('.sidebar')).to_be_hidden()
            expect(page.get_by_role('navigation',name='Mobile navigation')).to_be_visible()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.locator('.workspace-tools summary').click()
            page.get_by_role('navigation',name='Workspace tools').get_by_role('link',name='Job alerts').click()
            expect(page).to_have_url(base+'/alerts')
            page.set_viewport_size({'width':1440,'height':900})
            page.emulate_media(reduced_motion='reduce')
            page.goto(base+'/dashboard')
            assert page.locator('.sidebar').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
            page.get_by_role('button',name='Collapse navigation menu').click()
            expect(page.locator('.sidebar')).to_have_css('width','72px')
            assert not errors,errors
            print('PASS: widths 72/240, fixed icon coordinates, SVG loading, keyboard toggle/focus, active Settings, mobile tools and reduced motion.')
        finally:
            browser.close(); server.shutdown()

if __name__=='__main__': run()
