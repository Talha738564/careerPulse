/* Progressive HTML navigation: existing Flask routes/forms remain the source of truth.
 * Full document loads work without JS. Skeletons only cover real pending requests.
 */
(() => {
  if (!document.querySelector('.workspace') || !window.fetch) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const tokens = getComputedStyle(document.documentElement);
  const duration = parseFloat(tokens.getPropertyValue('--load-duration'));
  const stagger = parseFloat(tokens.getPropertyValue('--load-stagger'));
  const shortCap = parseFloat(tokens.getPropertyValue('--load-short-cap'));
  const longCap = parseFloat(tokens.getPropertyValue('--load-long-cap'));
  const status = document.getElementById('loading-status');
  const entrances = new Set();
  let pending = null;
  let currentURL = location.href;
  let searchTimer;
  const workspacePath = path => /^\/(dashboard|opportunities(?:\/\d+)?|saved|tracker|notifications|alerts|profile)$/.test(path);
  const mutationPath = path => /^\/(profile(?:\/reset)?|skills(?:\/remove)?|opportunities\/\d+\/(save|track)|tracker\/\d+(?:\/remove)?|alerts(?:\/[^/]+\/(toggle|delete))?|notifications\/[^/]+\/read)$/.test(path);

  function itemsFor(region) {
    return [...region.children].filter(el => !el.matches('[data-load-region],script,.load-skeleton') && !el.querySelector('[data-load-region]'));
  }
  function skeletonFor(item, region) {
    const origin = region.getBoundingClientRect();
    const overlay = document.createElement('div');
    overlay.className = 'load-skeleton';
    overlay.setAttribute('aria-hidden', 'true');
    function block(rect, radius = '5px') {
      if (!rect.width || !rect.height) return;
      const shape = document.createElement('span');
      shape.className = 'skeleton-block';
      Object.assign(shape.style, {left: `${rect.left-origin.left}px`, top: `${rect.top-origin.top}px`, width: `${rect.width}px`, height: `${rect.height}px`, borderRadius: radius});
      overlay.append(shape);
    }
    if (item.matches('.stat,.panel,.job-card')) {
      const rect = item.getBoundingClientRect();
      const surface = document.createElement('span');
      surface.className = 'skeleton-surface';
      const style = getComputedStyle(item);
      Object.assign(surface.style, {position:'absolute',left:`${rect.left-origin.left}px`,top:`${rect.top-origin.top}px`,width:`${rect.width}px`,height:`${rect.height}px`,borderRadius:style.borderRadius,background:style.backgroundColor,border:style.border});
      overlay.append(surface);
    }
    // Actual rendered text geometry includes digit widths and wrapped long names.
    const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        return node.textContent.trim() && !node.parentElement.closest('svg,option,textarea,script,style,[hidden]') ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    while (walker.nextNode()) {
      const range = document.createRange();
      range.selectNodeContents(walker.currentNode);
      [...range.getClientRects()].forEach(rect => block(rect));
    }
    item.querySelectorAll('input:not([type="hidden"]),select,textarea,progress,.ui-icon').forEach(el => block(el.getBoundingClientRect(), getComputedStyle(el).borderRadius));
    // A field may itself be a region child.
    if (item.matches('input:not([type="hidden"]),select,textarea,progress')) block(item.getBoundingClientRect(), getComputedStyle(item).borderRadius);
    return overlay;
  }
  function begin(root) {
    for (const entrance of entrances) {
      clearTimeout(entrance.timer);
      cancelAnimationFrame(entrance.frame1); cancelAnimationFrame(entrance.frame2);
      clear(entrance.states);
    }
    entrances.clear();
    const regions = [...root.querySelectorAll('[data-load-region]')];
    return regions.map(region => {
      const entries = itemsFor(region).map(element => ({element, overlay:skeletonFor(element, region), inert:element.inert}));
      region.setAttribute('aria-busy', 'true');
      region.classList.add('load-pending');
      entries.forEach(({element,overlay}) => {
        element.classList.add('load-content');
        element.inert = true;
        region.append(overlay);
      });
      return {region, entries};
    });
  }
  function clear(states) {
    states.forEach(({region,entries}) => {
      region.removeAttribute('aria-busy');
      region.classList.remove('load-pending');
      entries.forEach(({element,overlay,inert}) => {
        overlay.remove();
        element.inert = inert;
        element.classList.remove('load-enter','load-ready','load-content');
        element.style.removeProperty('transition-delay');
      });
    });
  }
  function reveal(root) {
    const states = begin(root);
    if (reduced.matches) { clear(states); return; }
    states.forEach(({region,entries}) => {
      region.classList.remove('load-pending');
      entries.forEach(({element,overlay,inert}, index) => {
        const delay = Math.min(index * stagger, entries.length < 10 ? shortCap : longCap);
        element.classList.add('load-enter');
        element.inert = inert;
        element.style.transitionDelay = `${delay}ms`;
        overlay.style.transitionDelay = `${delay}ms`;
      });
    });
    const entrance = {states};
    entrances.add(entrance);
    entrance.frame1 = requestAnimationFrame(() => {
      entrance.frame2 = requestAnimationFrame(() => {
      if (!entrances.has(entrance)) return;
      states.forEach(({region,entries}) => {
        region.removeAttribute('aria-busy');
        entries.forEach(({element,overlay}) => {
          element.classList.add('load-ready');
          overlay.classList.add('load-ready');
        });
      });
      entrance.timer = setTimeout(() => { clear(states); entrances.delete(entrance); }, duration + longCap + 50);
      });
    });
  }
  // A breakpoint can change every field's geometry. End entrances and remeasure
  // pending placeholders; do not keep desktop-sized overlays on a mobile layout.
  window.addEventListener('resize', () => {
    for (const entrance of entrances) {
      clearTimeout(entrance.timer);
      cancelAnimationFrame(entrance.frame1); cancelAnimationFrame(entrance.frame2);
      clear(entrance.states);
    }
    entrances.clear();
    if (pending) { clear(pending.states); pending.states = begin(pending.root); }
  });
  // Shared API also supports future section-level fetches without duplicating timing.
  window.CareerPulseLoading = {begin, clear, reveal};

  function updateNavigation(doc) {
    ['#sidebar-navigation', '.mobile-nav'].forEach(selector => {
      const target = document.querySelector(selector), source = doc.querySelector(selector);
      if (target && source) target.replaceChildren(...source.childNodes);
    });
    document.body.dataset.page = doc.body.dataset.page;
  }
  function showError(message) {
    document.querySelector('.load-error')?.remove();
    const box = document.createElement('div');
    box.className = 'load-error'; box.setAttribute('role','alert'); box.tabIndex = -1;
    const text = document.createElement('p'); text.textContent = message;
    box.append(text);
    document.getElementById('main').prepend(box);
    box.focus();
  }
  async function navigate(url, options = {}) {
    clearTimeout(searchTimer);
    if (pending?.method === 'POST') return; // Never interrupt/replay an in-flight write.
    if (pending) { pending.controller.abort(); clear(pending.states); }
    document.querySelector('.load-error')?.remove();
    // Cancel unfinished entrance effects before measuring the pending skeleton.
    document.querySelectorAll('.load-enter').forEach(el => {
      el.classList.remove('load-enter','load-ready'); el.style.removeProperty('transition-delay');
    });
    document.querySelectorAll('.load-skeleton').forEach(el => el.remove());
    const controller = new AbortController();
    const method = options.method || 'GET';
    const task = {controller, method, root: options.resultsOnly ? document.getElementById('discovery-results') : document.getElementById('main')};
    task.states = begin(task.root);
    pending = task;
    status.textContent = method === 'POST' ? 'Saving changes…' : 'Loading workspace…';
    const submitter = options.submitter;
    if (submitter) { submitter.disabled = true; submitter.classList.add('action-pending'); }
    const timeout = setTimeout(() => controller.abort(), 30000);
    try {
      const response = await fetch(url, {method, body:options.body, credentials:'same-origin', cache:'no-store', signal:controller.signal, headers:{'X-Requested-With':'CareerPulse'}});
      const html = await response.text();
      if (pending !== task) return;
      if (response.status >= 500) throw new Error('server');
      const doc = new DOMParser().parseFromString(html, 'text/html');
      if (options.resultsOnly && !response.ok) throw new Error('Invalid filters');
      const next = doc.querySelector(options.resultsOnly ? '#discovery-results' : '.workspace');
      if (!next) {
        // Session redirects and public routes retain normal browser navigation.
        location.assign(response.url); return;
      }
      clear(task.states);
      document.querySelector(options.resultsOnly ? '#discovery-results' : '.workspace').replaceWith(next);
      document.title = doc.title;
      updateNavigation(doc);
      if (options.resultsOnly) {
        document.querySelector('.filter-active-pill').textContent = doc.querySelector('.filter-active-pill').textContent;
      }
      // A validation response to /skills must keep the canonical profile URL.
      const destination = response.ok ? response.url : currentURL;
      if (options.history !== 'pop' && destination !== location.href) {
        history[options.history === 'replace' ? 'replaceState' : 'pushState']({}, '', destination);
      }
      currentURL = location.href;
      reveal(next);
      const main = document.getElementById('main');
      if (!options.resultsOnly) main.focus({preventScroll:true});
      if (!options.keepScroll) window.scrollTo({top:0,behavior:'instant'});
      status.textContent = response.ok ? (options.resultsOnly ? next.querySelector('[data-result-count]').textContent : method === 'POST' ? 'Changes saved.' : 'Workspace loaded.') : 'Please review the form errors.';
    } catch (error) {
      if (pending !== task) return;
      clear(task.states);
      status.textContent = 'The request could not be completed.';
      showError(method === 'POST' ? 'We could not confirm whether your changes were saved. Your entries are still here. Check the page before submitting again.' : 'We could not load that page. Check your connection and try again.');
      if (options.history === 'pop') history.replaceState({}, '', currentURL);
    } finally {
      clearTimeout(timeout);
      if (submitter) { submitter.disabled = false; submitter.classList.remove('action-pending'); }
      if (pending === task) pending = null;
    }
  }
  function discoveryURL() {
    const form = document.querySelector('form.filters');
    const search = document.getElementById('global-search');
    const url = new URL('/opportunities', location.origin);
    const data = new FormData(form);
    data.set('q', search.value.trim());
    form.querySelector('[name="q"]').value = search.value;
    for (const [key, value] of data) if (value && !(key === 'sort' && value === 'match')) url.searchParams.set(key, value);
    return url.href;
  }
  document.addEventListener('input', event => {
    if (event.target.id !== 'global-search' || event.isComposing) return;
    clearTimeout(searchTimer);
    if (pending?.method === 'GET') { pending.controller.abort(); clear(pending.states); pending = null; }
    searchTimer = setTimeout(() => navigate(discoveryURL(), {resultsOnly:true,keepScroll:true,history:'replace'}), 300);
  });
  document.addEventListener('compositionend', event => {
    if (event.target.id === 'global-search') event.target.dispatchEvent(new Event('input', {bubbles:true}));
  });
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target || link.hasAttribute('download')) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || url.hash || !workspacePath(url.pathname)) return;
    event.preventDefault();
    if (link.hasAttribute('data-reset-discovery') && document.getElementById('discovery-results')) {
      document.querySelectorAll('form.filters input, form.filters select').forEach(field => {
        if (field.tagName === 'SELECT') field.selectedIndex = 0;
        else field.value = '';
      });
      document.getElementById('global-search').value = '';
      navigate(url.href, {resultsOnly:true,keepScroll:true});
    } else navigate(url.href);
  });
  document.addEventListener('submit', event => {
    const form = event.target;
    const url = new URL(form.getAttribute('action') || location.href, location.href);
    const method = (form.getAttribute('method') || 'GET').toUpperCase();
    if (form.target || url.origin !== location.origin || (method === 'POST' ? !mutationPath(url.pathname) : !workspacePath(url.pathname))) return;
    event.preventDefault();
    if (pending?.method === 'POST') return;
    if (method === 'GET' && document.getElementById('discovery-results') && (form.matches('.filters') || form.getAttribute('role') === 'search')) {
      const filters = document.querySelector('form.filters');
      if (filters.reportValidity()) navigate(discoveryURL(), {resultsOnly:true,keepScroll:true});
      return;
    }
    const data = new FormData(form, event.submitter);
    if (method === 'GET') { url.search = new URLSearchParams(data).toString(); navigate(url.href); }
    else navigate(url.href, {method, body:data, submitter:event.submitter, keepScroll:true});
  });
  window.addEventListener('popstate', () => {
    if (pending?.method === 'POST') { location.reload(); return; }
    navigate(location.href, {history:'pop'});
  });
})();
