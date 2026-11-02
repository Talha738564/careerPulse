"""Exercise the real UI with Chromium. Run separately from unittest discovery."""
import argparse
from datetime import date, timedelta
from pathlib import Path
import secrets
import shutil
import sys
import threading
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from playwright.sync_api import sync_playwright, expect
from werkzeug.serving import make_server


def run(output):
    app=create_app()
    password=secrets.token_urlsafe(20)
    app.extensions['accounts'].create('browser-admin@example.test',password,'Demo Administrator','ADMIN')
    server=make_server('127.0.0.1',0,app)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}'
    output.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        page.set_default_timeout(8000)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        def visit(path):
            response=page.goto(base+path)
            assert response.status==200,(path,response.status)
        def capture(name):
            page.screenshot(path=str(output/(name+'-desktop.png')),full_page=True)
            page.set_viewport_size({'width':390,'height':844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),name
            page.screenshot(path=str(output/(name+'-mobile.png')),full_page=True)
            page.set_viewport_size({'width':1440,'height':1000})
        try:
            for route in ('/login', '/register'):
                visit(route)
                for width in (320, 390, 768, 1440):
                    page.set_viewport_size({'width':width, 'height':844})
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route, width)
                    expect(page.locator('h1')).to_be_visible()
                page.set_viewport_size({'width':1440, 'height':1000})
                capture('glass-' + route.lstrip('/'))
            visit('/')
            capture('auth-entry')
            page.get_by_label('Account access',exact=True).get_by_role('link',name='Create account',exact=True).click()
            page.get_by_label('Full name',exact=True).fill('Demo Browser Student')
            page.get_by_label('Email',exact=True).fill('browser-student@example.test')
            page.get_by_label('Password',exact=True).fill(password)
            page.get_by_label('Confirm password',exact=True).fill(password)
            page.get_by_role('button',name='Create account',exact=True).click()
            page.get_by_label('Email',exact=True).fill('browser-student@example.test')
            page.get_by_label('Password',exact=True).fill(password)
            page.get_by_role('button',name='Sign in',exact=True).click()
            visit('/profile')
            page.get_by_label('City',exact=True).fill('Lahore')
            page.get_by_role('button',name='Save demo profile',exact=True).click()
            for skill in ('Python','SQL','Git'):
                page.get_by_label('Skill',exact=True).select_option(skill)
                page.get_by_role('button',name='Save skill',exact=True).click()
            expect(page.get_by_text('Skill saved. Your opportunity matches have been updated.')).to_be_visible()
            visit('/opportunities/1')
            expect(page.get_by_text('100% required-skill match',exact=True)).to_be_visible()
            page.get_by_role('button',name='Save opportunity',exact=True).click()
            expect(page.get_by_role('heading',name='1 saved opportunities')).to_be_visible()
            visit('/opportunities/1')
            page.get_by_role('button',name='Add to tracker',exact=True).click()
            page.get_by_label('Status',exact=True).select_option('APPLIED')
            page.get_by_label('Date applied',exact=True).fill(date.today().isoformat())
            page.get_by_label('Notes',exact=True).fill('Fictional demo: portfolio sent, follow up next week.')
            page.get_by_label('I confirm this status reflects my own application activity.',exact=True).check()
            page.get_by_role('button',name='Save status update',exact=True).click()
            expect(page.get_by_text('Your application tracker has been updated.',exact=True)).to_be_visible()
            capture('journey-tracker')
            visit('/alerts')
            page.get_by_label('Alert name',exact=True).fill('My Python shortlist')
            page.get_by_label('Python',exact=True).check()
            page.get_by_role('button',name='Create alert',exact=True).click()
            visit('/notifications')
            expect(page.get_by_text('Deadline Pulse',exact=True)).to_be_visible()
            page.get_by_role('button',name='Mark as read',exact=True).first.click()
            visit('/dashboard')
            capture('journey-dashboard')
            page.get_by_role('button',name='Sign out',exact=True).click()
            visit('/login')
            page.get_by_label('Email',exact=True).fill('browser-admin@example.test')
            page.get_by_label('Password',exact=True).fill(password)
            page.get_by_role('button',name='Sign in',exact=True).click()
            visit('/admin/companies/new')
            page.get_by_label('Company name',exact=True).fill('Fictional Browser Studio')
            page.get_by_label('City',exact=True).fill('Lahore')
            page.get_by_role('button',name='Save company',exact=True).click()
            visit('/admin/opportunities/new')
            page.get_by_label('Title',exact=True).fill('Browser-tested Python Internship')
            page.get_by_label('Company',exact=True).select_option(label='Fictional Browser Studio')
            page.get_by_label('Deadline',exact=True).fill((date.today()+timedelta(days=10)).isoformat())
            page.get_by_label('City',exact=True).fill('Lahore')
            page.get_by_role('group',name='Required skills').get_by_label('Python',exact=True).check()
            page.get_by_role('button',name='Save opportunity',exact=True).click()
            expect(page.get_by_role('heading',name='Browser-tested Python Internship',exact=True)).to_be_visible()
            capture('journey-admin-catalog')
            visit('/admin/dashboard')
            capture('journey-admin')
            page.get_by_role('button',name='Sign out',exact=True).click()
            visit('/login')
            page.get_by_label('Email',exact=True).fill('browser-student@example.test')
            page.get_by_label('Password',exact=True).fill(password)
            page.get_by_role('button',name='Sign in',exact=True).click()
            visit('/notifications')
            expect(page.get_by_text('Browser-tested Python Internship at Fictional Browser Studio',exact=True)).to_be_visible()
            for path in ['/','/dashboard','/opportunities','/opportunities/1','/saved','/tracker','/profile','/alerts','/notifications']:
                visit(path)
                page.set_viewport_size({'width':390,'height':844})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),path
                page.set_viewport_size({'width':1440,'height':1000})
            visit('/')
            page.keyboard.press('Tab')
            expect(page.get_by_role('link',name='Skip to content')).to_be_focused()
            page.emulate_media(reduced_motion='reduce')
            assert page.locator('.button').first.evaluate('(el) => getComputedStyle(el).transitionDuration')=='0s'
            # Role guard is validated through an actual browser response too.
            response=page.goto(base+'/admin/dashboard')
            assert response.status==403
            assert not errors,errors
            print('PASS: complete student/admin workflow; 9 student routes at 390px; role guard; no browser JS errors.')
        finally:
            browser.close()
            server.shutdown()

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--screenshots',type=Path,default=Path('artifacts/browser'))
    run(parser.parse_args().screenshots)
