"""Feature-demo playback, pause, replay, cursor and accessible fallbacks."""
from pathlib import Path
import sys, threading, shutil, re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import create_app
from werkzeug.serving import make_server
from playwright.sync_api import sync_playwright, expect


def run():
    server=make_server('127.0.0.1',0,create_app())
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    output=Path('artifacts/feature-demos');output.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            page.goto(base+'/');page.evaluate('document.fonts.ready')
            for kind in ['discovery','tracker']:
                card=page.locator('.'+kind+'-preview')
                card.scroll_into_view_if_needed()
                expect(card).to_have_class(re.compile('demo-playing'))
                control=card.locator('.demo-control')
                control.click()
                expect(card).to_have_class(re.compile('demo-paused'))
                expect(card.locator('.demo-frame').first).to_have_css('animation-play-state','paused')
                paused=card.locator('.demo-progress span').evaluate('(e)=>getComputedStyle(e).transform')
                page.wait_for_timeout(250)
                assert card.locator('.demo-progress span').evaluate('(e)=>getComputedStyle(e).transform')==paused
                control.click()
                expect(control).to_contain_text('Pause')
                height=card.bounding_box()['height']
                expect(control).to_contain_text('Replay',timeout=5000)
                assert card.bounding_box()['height']==height
                expect(card.locator('.demo-frame').last).to_have_css('opacity','1')
                card.hover()
                expect(page.locator('.feature-cursor-dot')).to_be_visible()
                expect(card).to_have_css('cursor','none')
                card.screenshot(path=str(output/(kind+'-final.png')))
                control.focus();page.keyboard.press('Enter')
                expect(control).to_contain_text('Pause')
                # Playback suspends when the card leaves the viewport.
                page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                expect(card).to_have_class(re.compile('demo-paused'))
                card.scroll_into_view_if_needed()
                expect(control).to_contain_text('Replay',timeout=5000)
            page.emulate_media(reduced_motion='reduce')
            expect(page.locator('.demo-control').first).to_be_hidden()
            expect(page.locator('.demo-frame').nth(2)).to_have_css('opacity','1')
            for width in [320,390,768]:
                page.set_viewport_size({'width':width,'height':844})
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.locator('.tracker-preview').scroll_into_view_if_needed()
            page.set_viewport_size({'width':390,'height':844})
            page.locator('.tracker-preview').screenshot(path=str(output/'tracker-mobile.png'))
            plain=browser.new_context(java_script_enabled=False)
            fallback=plain.new_page();fallback.goto(base+'/')
            expect(fallback.locator('.discovery-preview .demo-frame').last).to_be_visible()
            expect(fallback.locator('.demo-control').first).to_be_hidden()
            plain.close()
            touch=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
            mobile=touch.new_page();mobile.goto(base+'/')
            card=mobile.locator('.discovery-preview');card.scroll_into_view_if_needed()
            expect(card.locator('.demo-control')).to_contain_text('Replay',timeout=5000)
            expect(mobile.locator('.feature-cursor-dot')).to_be_hidden()
            touch.close()
            assert not errors,errors
            print('PASS: two finite demos, pause/resume/replay, offscreen suspension, stable geometry, custom desktop cursor, touch, reduced motion and no-JS.')
        finally:
            browser.close();server.shutdown()

if __name__=='__main__':run()
