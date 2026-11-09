"""Live discovery, URL state, full-card links and scoped cursor behavior."""
from pathlib import Path
import sys, shutil, threading, re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from werkzeug.serving import make_server
from playwright.sync_api import sync_playwright, expect


def run():
    server=make_server('127.0.0.1',0,create_app())
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    out=Path('artifacts/discovery');out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            page.goto(base+'/opportunities')
            requests=[]
            page.on('request',lambda r:requests.append(r.url) if r.resource_type=='fetch' and '/opportunities' in r.url else None)
            search=page.locator('#global-search')
            search.press_sequentially('Python',delay=30)
            expect(page).to_have_url(base+'/opportunities?q=Python')
            expect(search).to_be_focused()
            assert len(requests)==1,requests
            expect(page.locator('.job-card-title').first).to_contain_text('Python')
            page.get_by_label('Job type',exact=True).select_option('INTERNSHIP')
            page.get_by_label('City',exact=True).select_option('Lahore')
            page.get_by_label('Location',exact=True).select_option('no')
            page.get_by_label('Skill',exact=True).select_option('Python')
            page.get_by_label('Experience',exact=True).select_option('STUDENT')
            page.get_by_label('Minimum pay (PKR)',exact=True).fill('30000')
            page.get_by_role('button',name='Apply filters',exact=True).click()
            expect(page.locator('[data-result-count]')).to_have_text('1 opportunity')
            expect(page.locator('.job-card .match')).to_have_text('100% skill match')
            assert all(value in page.url for value in ['q=Python','city=Lahore','remote=no','salary=30000'])
            shared=page.url;page.reload()
            expect(search).to_have_value('Python')
            expect(page.get_by_label('City',exact=True)).to_have_value('Lahore')
            expect(page.get_by_label('Location',exact=True)).to_have_value('no')
            page.screenshot(path=str(out/'filtered-desktop.png'),full_page=True)
            page.locator('.filter-reset-link').click()
            expect(page).to_have_url(base+'/opportunities')
            expect(search).to_have_value('')
            expect(page.get_by_label('City',exact=True)).to_have_value('')
            page.get_by_label('Sort by',exact=True).select_option('salary')
            page.get_by_role('button',name='Apply filters',exact=True).click()
            expect(page).to_have_url(base+'/opportunities?sort=salary')
            page.go_back();expect(page).to_have_url(base+'/opportunities')
            expect(page.get_by_label('Sort by',exact=True)).to_have_value('match')
            search.fill('nonexistent-role-xyz')
            expect(page.get_by_role('heading',name='No roles match your filters — try widening your search')).to_be_visible()
            page.get_by_role('link',name='Reset filters',exact=True).click()
            expect(page).to_have_url(base+'/opportunities')
            expect(page.locator('.job-card').first).to_be_visible()
            expect(page.locator('.load-skeleton')).to_have_count(0)
            card=page.locator('.job-card').first
            href=card.locator('.job-card-title').get_attribute('href')
            card.click(position={'x':8,'y':8})
            expect(page).to_have_url(base+href)
            page.goto(base+'/opportunities')
            page.get_by_role('button',name='Save opportunity',exact=True).first.click()
            expect(page).to_have_url(base+'/saved')
            for width in [320,390,768]:
                page.set_viewport_size({'width':width,'height':844});page.goto(shared)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
            page.screenshot(path=str(out/'filtered-mobile.png'),full_page=True)
            # The static skill-match section follows discovery; alerts have no animation.
            page.set_viewport_size({'width':1440,'height':1000});page.goto(base+'/')
            assert page.locator('.home-how').evaluate('(e)=>e.children[0].classList.contains("discovery-feature") && e.children[1].classList.contains("how-inner")')
            expect(page.locator('[data-feature-demo]')).to_have_count(2)
            expect(page.locator('.alert-preview [data-feature-demo],.alert-preview .demo-frame')).to_have_count(0)
            assert not page.locator('.alert-preview').evaluate('(e)=>e.closest("[data-reveal]")')
            dot=page.locator('.feature-cursor-dot');ring=page.locator('.feature-cursor-ring')
            for kind in ['discovery','tracker']:
                demo=page.locator('.'+kind+'-preview');demo.scroll_into_view_if_needed()
                expect(demo.locator('.demo-control')).to_contain_text('Replay',timeout=6000)
                demo.hover(position={'x':40,'y':40})
                expect(dot).to_be_visible();expect(dot).to_have_css('width','8px')
                expect(ring).to_have_css('width','34px')
                expect(ring).to_have_css('border-top-width','2px')
                expect(dot).to_have_css('background-color','rgb(13, 148, 136)')
                expect(demo).to_have_css('cursor','none')
                demo.locator('.demo-control').hover()
                expect(ring).to_have_css('width','54px')
                expect(ring).to_have_css('border-top-color','rgb(13, 148, 136)')
                expect(dot).to_be_visible()
                point=dot.bounding_box()
                mouse=demo.locator('.demo-control').bounding_box()
                assert abs(point['x']+4-(mouse['x']+mouse['width']/2))<1
                page.screenshot(path=str(out/(kind+'-cursor.png')))
            page.mouse.move(5,5);expect(dot).to_be_hidden()
            page.emulate_media(color_scheme='dark')
            page.locator('.tracker-preview').hover(position={'x':40,'y':40})
            expect(dot).to_have_css('background-color','rgb(94, 234, 212)')
            page.emulate_media(reduced_motion='reduce')
            page.locator('.tracker-preview').hover(position={'x':50,'y':50})
            expect(ring).to_have_css('transition-duration','0s')
            assert not errors,errors
            print('PASS: debounced search/focus, combined filters, URL restore/history/reset, match badges, whole-card navigation/save, mobile, homepage order/static alerts, dot/ring dimensions/hover/dark/reduced motion.')
        finally:
            browser.close();server.shutdown()

if __name__=='__main__':run()
