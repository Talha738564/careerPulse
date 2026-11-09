/* Progressive enhancement: navigation, password visibility and one-shot reveals. */
document.querySelectorAll('[data-password-toggle]').forEach(button => {
  const input = document.getElementById(button.getAttribute('aria-controls'));
  if (!input) return;
  button.hidden = false;
  const hide = () => {
    input.type = 'password';
    button.setAttribute('aria-pressed', 'false');
    button.setAttribute('aria-label', button.dataset.showLabel);
  };
  button.addEventListener('click', () => {
    const showing = input.type === 'password';
    input.type = showing ? 'text' : 'password';
    button.setAttribute('aria-pressed', String(showing));
    button.setAttribute('aria-label', showing ? button.dataset.hideLabel : button.dataset.showLabel);
  });
  input.form.addEventListener('submit', hide);
  window.addEventListener('pageshow', hide);
});
const sidebar = document.getElementById('workspace-sidebar');
const toggle = document.querySelector('[data-sidebar-toggle]');
if (sidebar && toggle) {
  toggle.hidden = false;
  const desktop = matchMedia('(min-width: 901px)');
  let expanded = true;
  const sync = () => {
    document.body.classList.toggle('sidebar-collapsed', !expanded && desktop.matches);
    sidebar.inert = !desktop.matches;
    if (!expanded) sidebar.scrollTop = 0;
    sidebar.querySelector('[data-sidebar-note]').inert = !expanded;
    sidebar.querySelector('.sidebar-tagline').setAttribute('aria-hidden', String(!expanded));
    const expandedBrand = sidebar.querySelector('.sidebar-brand-expanded');
    const collapsedBrand = sidebar.querySelector('.sidebar-brand-collapsed');
    expandedBrand.tabIndex = expanded ? 0 : -1;
    expandedBrand.setAttribute('aria-hidden', String(!expanded));
    collapsedBrand.tabIndex = expanded ? -1 : 0;
    collapsedBrand.setAttribute('aria-hidden', String(expanded));
    toggle.setAttribute('aria-expanded', String(expanded));
    toggle.setAttribute('aria-label', expanded ? 'Collapse navigation menu' : 'Expand navigation menu');
  };
  toggle.addEventListener('click', () => { expanded = !expanded; sync(); });
  desktop.addEventListener('change', sync);
  sync();
}
function closeMenus(event) {
  document.querySelectorAll('.public-menu[open], .workspace-tools[open], .account-menu[open]').forEach(menu => {
    if (event.type === 'keydown' && event.key !== 'Escape') return;
    if (event.type === 'click' && menu.contains(event.target) && !event.target.closest('a')) return;
    if (event.type === 'focusout' && (!menu.contains(event.target) || menu.contains(event.relatedTarget))) return;
    menu.open = false;
    if (event.type === 'keydown') menu.querySelector('summary').focus();
  });
}
['click', 'keydown', 'focusout'].forEach(type => document.addEventListener(type, closeMenus));
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !reducedMotion.matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('[data-reveal]').forEach(element => {
    // Do not hide content already in view or targeted by a direct anchor link.
    if (element.getBoundingClientRect().top < innerHeight || location.hash) return;
    element.classList.add('reveal-ready');
    observer.observe(element);
  });
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) {
      observer.disconnect();
      document.querySelectorAll('.reveal-ready').forEach(element => element.classList.add('is-visible'));
    }
  });
}
