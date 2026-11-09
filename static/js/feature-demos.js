/* Explanatory landing-page motion only: one 3.6s play, then a stable final frame. */
(() => {
  const cards = [...document.querySelectorAll('[data-feature-demo]')];
  if (!cards.length || !('IntersectionObserver' in window)) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  cards.forEach(card => {
    const button = card.querySelector('.demo-control');
    const label = card.classList.contains('discovery-preview') ? 'getting started' : 'application tracker';
    let seen = false, visible = false, manuallyPaused = false;
    const playing = () => card.classList.contains('demo-playing');
    function control(text) {
      button.firstChild.textContent = text + ' ';
      button.setAttribute('aria-label', `${text.replace(' demo','')} ${label} demo`);
    }
    function syncPause() {
      if (!playing()) return;
      const paused = manuallyPaused || !visible || document.hidden;
      card.classList.toggle('demo-paused', paused);
      control(paused ? 'Play demo' : 'Pause demo');
    }
    function play() {
      if (reduced.matches) return;
      card.querySelector('.demo-announcement').textContent = '';
      manuallyPaused = false;
      card.classList.add('demo-playing');
      syncPause();
    }
    function finish() {
      card.classList.remove('demo-playing','demo-paused');
      control('Replay demo');
    }
    button.addEventListener('click', () => {
      if (!playing()) play();
      else { manuallyPaused = !manuallyPaused; syncPause(); }
    });
    card.querySelector('.demo-progress span').addEventListener('animationend', () => {
      finish();
      card.querySelector('.demo-announcement').textContent = 'Demo complete. Replay is available.';
    });
    const observer = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (visible && !seen && !reduced.matches) { seen = true; play(); }
      else syncPause();
    }, {threshold:0.4});
    function preference() {
      finish();
      card.classList.toggle('demo-enhanced', !reduced.matches);
      button.hidden = reduced.matches;
      card.querySelector('.demo-duration').textContent = reduced.matches ? 'Feature preview' : '3.6s demo';
      if (!reduced.matches && visible && !seen) { seen = true; play(); }
    }
    preference();
    observer.observe(card);
    document.addEventListener('visibilitychange', syncPause);
    reduced.addEventListener('change', preference);
  });
})();
