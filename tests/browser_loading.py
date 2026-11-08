"""Real delayed-request coverage for shared loading and dashboard UI."""
from pathlib import Path
import shutil, sys, threading
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from playwright.sync_api import sync_playwright, expect
from werkzeug.serving import make_server


def run():
    app = create_app()
    server = make_server('127.0.0.1', 0, app)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    output = Path('artifacts/dashboard'); output.mkdir(parents=True, exist_ok=True)
    base = f'http://127.0.0.1:{server.server_port}'
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=shutil.which('chromium'), headless=True)
        page = browser.new_page(viewport={'width':1440,'height':1000})
        errors, icon_requests = [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda r: icon_requests.append(r.url) if '/static/icons/' in r.url else None)
        def settled():
            expect(page.locator('[aria-busy="true"]')).to_have_count(0)
            expect(page.locator('.load-skeleton')).to_have_count(0)
        def delayed_click(selector, destination):
            held = []
            page.route(base+destination, lambda route: held.append(route))
            page.locator(selector).first.click()
            expect(page.locator('[aria-busy="true"]').first).to_be_visible()
            expect(page.locator('.skeleton-block').first).to_have_css('background-color','rgb(229, 233, 238)')
            assert held
            return held
        try:
            page.goto(base+'/dashboard'); page.evaluate('document.fonts.ready')
            expect(page.locator('.name-highlight')).to_have_css('text-decoration-color','rgb(22, 184, 166)')
            expect(page.locator('.sidebar-note')).to_contain_text('Your skills. Your next chapter.')
            page.screenshot(path=str(output/'desktop.png'), full_page=True)
            page.screenshot(path=str(output/'desktop-first-fold.png'))
            assert page.locator('svg.ui-icon').evaluate_all('(els)=>els.every(e=>e.children.length && e.getAttribute("stroke")==="currentColor")')
            page.evaluate('window.testDocumentMarker = 42')
            before = page.locator('.stats').bounding_box()
            held = delayed_click('a[aria-label="Explore"]', '/opportunities')
            assert page.locator('.stats').bounding_box() == before
            expect(page.locator('.stat').first).to_have_css('opacity','0')
            # Every stat digit has its own gray bar, never an interim zero/null.
            assert page.locator('.stats .skeleton-block').count() >= 4
            page.screenshot(path=str(output/'loading-desktop.png'), full_page=True)
            page.set_viewport_size({'width':390,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            expect(page.locator('.stats')).to_have_attribute('aria-busy','true')
            page.screenshot(path=str(output/'loading-mobile.png'))
            page.set_viewport_size({'width':1440,'height':1000})
            held.pop().continue_(); page.unroute(base+'/opportunities')
            expect(page).to_have_url(base+'/opportunities'); settled()
            assert page.evaluate('window.testDocumentMarker') == 42
            expect(page.locator('#main')).to_be_focused()
            # Async filtering uses the same skeleton while its request is held.
            held=[]; page.route('**/opportunities?q=Python', lambda route: held.append(route))
            page.locator('#global-search').fill('Python')
            page.locator('form[role="search"] button').click()
            expect(page.locator('.browse-grid')).to_have_attribute('aria-busy','true')
            expect(page.locator('.job-card').first).to_have_css('opacity','0')
            held.pop().continue_(); page.unroute('**/opportunities?q=Python')
            expect(page).to_have_url(base+'/opportunities?q=Python'); settled()
            expect(page.locator('#global-search')).to_have_value('Python')
            # Save mutation retains CSRF and follows the server's redirect.
            page.get_by_role('button',name='Save opportunity').first.click()
            expect(page).to_have_url(base+'/saved'); settled()
            expect(page.get_by_role('button',name='Remove saved job')).to_be_visible()
            assert page.evaluate('window.testDocumentMarker') == 42
            page.go_back(); expect(page).to_have_url(base+'/opportunities?q=Python'); settled()
            expect(page.locator('#global-search')).to_have_value('Python')
            # Two searches can overlap: only the newest request may render.
            held=[]; page.route('**/opportunities?q=Old', lambda route: held.append(route))
            page.locator('#global-search').fill('Old'); page.locator('form[role="search"] button').click()
            expect(page.locator('[aria-busy="true"]').first).to_be_visible()
            page.locator('#global-search').fill('Git'); page.locator('form[role="search"] button').click()
            expect(page).to_have_url(base+'/opportunities?q=Git'); settled()
            for route in held: route.abort()
            page.unroute('**/opportunities?q=Old')
            expect(page.locator('#global-search')).to_have_value('Git')
            # Network errors restore usable data and a readable error, never endless skeletons.
            page.route(base+'/profile', lambda route: route.abort())
            page.locator('a[aria-label="Settings"]').click()
            expect(page.locator('.load-error')).to_contain_text('could not load')
            settled(); expect(page.locator('.job-card').first).to_have_css('opacity','1')
            page.unroute(base+'/profile')
            page.locator('a[aria-label="Settings"]').click(); expect(page).to_have_url(base+'/profile'); settled()
            page.locator('#full_name').fill('Demo Teal Student')
            page.get_by_role('button',name='Save demo profile').click()
            expect(page.locator('.notice[role="status"]')).to_contain_text('profile saved'); settled()
            expect(page.locator('#full_name')).to_have_value('Demo Teal Student')
            # A server-side validation error keeps entered values and restores controls.
            page.locator('#resume_url').fill('ftp://example.test/resume')
            page.locator('form[action="/profile"]').evaluate('(form)=>form.noValidate=true')
            page.get_by_role('button',name='Save demo profile').click()
            expect(page.locator('.form-errors')).to_be_visible(); settled()
            expect(page.locator('#full_name')).to_have_value('Demo Teal Student')
            expect(page).to_have_url(base+'/profile')
            # All data pages participate and recover after real pending requests.
            for route in ['/tracker','/notifications','/alerts','/profile','/dashboard']:
                page.goto(base+route)
                held=[]; page.route(base+'/saved', lambda r: held.append(r))
                page.locator('a[aria-label="Saved"]').click()
                expect(page.locator('[aria-busy="true"]').first).to_be_visible()
                assert page.locator('.skeleton-block').count()>0, route
                held.pop().continue_(); page.unroute(base+'/saved'); settled()
            # Finite animation budget, including a long list.
            page.goto(base+'/opportunities')
            delays=page.evaluate('''() => {
              const grid=document.querySelector('.browse-grid');
              const card=grid.querySelector('.job-card');
              while(grid.children.length<14) grid.append(card.cloneNode(true));
              CareerPulseLoading.reveal(document.querySelector('main'));
              return [...grid.children].filter(e=>e.matches('.job-card')).map(e=>parseFloat(e.style.transitionDelay));
            }''')
            assert delays[:3]==[0,70,140] and max(delays)+230<=1000,delays
            settled()
            # Responsive dashboard, compact rail, and restored sidebar CTA.
            for width in [320,390,768,1024,1440]:
                page.set_viewport_size({'width':width,'height':900})
                page.goto(base+'/dashboard'); page.evaluate('document.fonts.ready')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
                if width==390: page.screenshot(path=str(output/'mobile.png'),full_page=True)
                if width==1440:
                    page.locator('.sidebar-toggle').click()
                    expect(page.locator('.sidebar-note')).to_be_hidden()
                    expect(page.locator('.sidebar')).to_have_css('width','72px')
                    page.screenshot(path=str(output/'collapsed.png'))
            page.emulate_media(reduced_motion='reduce')
            page.locator('a[aria-label="Explore"]').click(); expect(page).to_have_url(base+'/opportunities')
            expect(page.locator('.load-skeleton')).to_have_count(0)
            assert not errors,errors
            assert not icon_requests,icon_requests
            # No-JS content is immediately available and normal forms still work.
            plain=browser.new_context(java_script_enabled=False)
            fallback=plain.new_page(); fallback.goto(base+'/dashboard')
            expect(fallback.get_by_role('heading',name='Recommended for you')).to_be_visible()
            expect(fallback.locator('.stat').first).to_have_css('opacity','1')
            fallback.locator('a[aria-label="Explore"]').click()
            expect(fallback).to_have_url(base+'/opportunities'); plain.close()
            print('PASS: dashboard, delayed skeletons, inline icons, async filters/save/profile, history, racing GETs, network recovery, timing caps, mobile, reduced motion and no-JS.')
        finally:
            browser.close(); server.shutdown()

if __name__=='__main__': run()
