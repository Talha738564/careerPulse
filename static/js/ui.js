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
    sidebar.inert = !expanded || !desktop.matches;
    toggle.setAttribute('aria-expanded', String(expanded));
    toggle.setAttribute('aria-label', expanded ? 'Collapse navigation menu' : 'Expand navigation menu');
  };
  toggle.addEventListener('click', () => { expanded = !expanded; sync(); });
  desktop.addEventListener('change', sync);
  sync();
}
document.querySelectorAll('.public-menu').forEach(menu => {
  const close = (focus = false) => { menu.open = false; if (focus) menu.querySelector('summary').focus(); };
  menu.addEventListener('keydown', event => { if (event.key === 'Escape') close(true); });
  menu.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  document.addEventListener('click', event => { if (!menu.contains(event.target)) close(); });
  menu.addEventListener('focusout', event => { if (!menu.contains(event.relatedTarget)) close(); });
});
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
