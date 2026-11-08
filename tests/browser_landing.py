"""Landing, navigation and password-control browser regressions."""
from pathlib import Path
import shutil
import sys
import threading
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from playwright.sync_api import sync_playwright, expect
from werkzeug.serving import make_server


def run():
    server = make_server('127.0.0.1', 0, create_app())
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    output = Path('artifacts/landing')
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=shutil.which('chromium'), headless=True)
        page = browser.new_page(viewport={'width':1440,'height':1000})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('response', lambda response: errors.append(f'{response.status}: {response.url}') if response.status >= 400 else None)
        try:
            routes = ['/', '/login', '/register', '/dashboard', '/opportunities', '/profile', '/saved', '/tracker', '/alerts', '/notifications']
            for width in [320, 360, 390, 430, 768, 1024, 1159, 1440]:
                page.set_viewport_size({'width':width,'height':844})
                for route in routes:
                    page.goto(base+route)
                    page.evaluate('document.fonts.ready')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route,width)
                    expect(page.locator('input[name="q"]:not([type="hidden"])')).to_have_count(1 if route == '/opportunities' else 0)
                for route, name in [('/', 'home'), ('/login','login'), ('/register','register')]:
                    page.goto(base+route)
                    page.evaluate('document.fonts.ready')
                    if route == '/':
                        for section in page.locator('[data-reveal]').all():
                            section.scroll_into_view_if_needed()
                            page.wait_for_timeout(550)
                        page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                    if width in (390,1159,1440):
                        page.screenshot(path=str(output/f'{name}-{width}.png'),full_page=True)
                # Native public menu must work at all sizes and close on Escape.
                page.goto(base+'/')
                summary=page.locator('.public-menu summary')
                summary.click()
                expect(page.get_by_role('navigation',name='Quick navigation')).to_be_visible()
                page.keyboard.press('Escape')
                expect(page.locator('.public-menu')).not_to_have_attribute('open','')
                expect(summary).to_be_focused()
            # Feature-tour links reach the actual guest tools without creating data.
            page.goto(base+'/')
            for title, destination in [('Create your first alert','/alerts'), ('Explore your tracker','/tracker'), ('Open your saved jobs','/saved'), ('View your notifications','/notifications')]:
                page.get_by_role('link',name=title).click()
                expect(page).to_have_url(base+destination)
                page.goto(base+'/')
            page.goto(base+'/register')
            expect(page.locator('.circled-here')).to_have_count(0)
            # Each password control works independently without navigation or value loss.
            for route in ['/login','/register']:
                page.goto(base+route)
                for field_id,label in [('password','password')]+([('confirm-password','confirm password')] if route=='/register' else []):
                    field=page.locator('#'+field_id)
                    field.fill('Fictional-password-123')
                    page.get_by_role('button',name='Show '+label,exact=True).click()
                    expect(field).to_have_attribute('type','text')
                    expect(field).to_have_value('Fictional-password-123')
                    expect(page).to_have_url(base+route)
                    page.get_by_role('button',name='Hide '+label,exact=True).click()
                    expect(field).to_have_attribute('type','password')
            page.goto(base+'/login')
            expect(page.locator('.circled-here')).to_have_text('here')
            # Desktop navigation hides from both sight and keyboard traversal.
            page.goto(base+'/dashboard')
            page.get_by_role('button',name='Collapse navigation menu').click()
            expect(page.locator('#workspace-sidebar')).to_have_css('width','72px')
            assert not page.locator('#workspace-sidebar').evaluate('(e)=>e.inert')
            page.get_by_role('button',name='Expand navigation menu').click()
            expect(page.locator('#workspace-sidebar')).to_have_css('width','240px')
            # CTA destinations and scroll-triggered reveal.
            page.set_viewport_size({'width':1440,'height':800})
            page.goto(base+'/')
            page.get_by_role('link',name='Find my next opportunity').click()
            expect(page).to_have_url(base+'/register')
            page.goto(base+'/')
            page.get_by_role('link',name='See how it works').click()
            for section in page.locator('[data-reveal]').all():
                section.scroll_into_view_if_needed()
                expect(section).to_have_css('opacity','1')
            page.emulate_media(reduced_motion='reduce')
            page.goto(base+'/')
            for section in page.locator('[data-reveal]').all():
                section.scroll_into_view_if_needed()
                expect(section).to_have_css('opacity','1')
            assert page.locator('html').evaluate('(e)=>getComputedStyle(e).scrollBehavior')=='auto'
            # No JS: core links, menu and all content remain usable; inert buttons are hidden.
            context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
            plain=context.new_page()
            plain.goto(base+'/')
            for section in plain.locator('[data-reveal]').all():
                expect(section).to_have_css('opacity','1')
            plain.goto(base+'/login')
            expect(plain.locator('.password-toggle')).to_be_hidden()
            expect(plain.locator('#password')).to_have_attribute('type','password')
            context.close()
            assert not errors, errors
            print('PASS: 80 route/width checks; public and desktop menus; password toggles; CTA; scroll reveal; reduced motion; no-JS fallback; no browser errors.')
        finally:
            browser.close()
            server.shutdown()

if __name__ == '__main__':
    run()
