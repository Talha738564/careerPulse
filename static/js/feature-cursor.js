/* Scoped to the two product demos. No animation loop while idle or outside cards. */
(() => {
  if (!document.querySelector('[data-feature-demo]')) return;
  const fine = matchMedia('(hover: hover) and (pointer: fine)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const dot = document.createElement('span');
  const ring = document.createElement('span');
  dot.className = 'feature-cursor-dot'; ring.className = 'feature-cursor-ring';
  [dot, ring].forEach(el => { el.hidden = true; el.setAttribute('aria-hidden','true'); document.body.append(el); });
  let mouseKnown = false;
  let active = null, frame = 0, x = 0, y = 0, ringX = 0, ringY = 0;
  const position = (el, px, py) => { el.style.transform = `translate3d(${px}px,${py}px,0) translate(-50%,-50%)`; };
  function hide() {
    active?.classList.remove('cursor-active'); active = null;
    dot.hidden = ring.hidden = true;
    cancelAnimationFrame(frame); frame = 0;
  }
  function follow() {
    frame = 0;
    if (!active) return;
    const factor = reduced.matches ? 1 : 0.18;
    ringX += (x-ringX)*factor; ringY += (y-ringY)*factor;
    if (Math.hypot(x-ringX, y-ringY) < 0.1) { ringX = x; ringY = y; }
    position(ring, ringX, ringY);
    if (ringX !== x || ringY !== y) frame = requestAnimationFrame(follow);
  }
  function move(event) {
    if (!fine.matches || event.pointerType !== 'mouse') { hide(); return; }
    mouseKnown = true;
    x = event.clientX; y = event.clientY;
    const card = event.target.closest('[data-feature-demo]');
    if (!card) { hide(); return; }
    if (active !== card) {
      hide(); active = card; active.classList.add('cursor-active');
      ringX = x; ringY = y; position(ring,x,y);
      dot.hidden = ring.hidden = false;
    }
    position(dot,x,y);
    ring.classList.toggle('cursor-interactive', Boolean(event.target.closest('a,button,input,select,textarea,summary,[role="button"]')));
    if (!frame) frame = requestAnimationFrame(follow);
  }
  document.addEventListener('pointermove', move, {passive:true});
  document.addEventListener('pointerover', move, {passive:true});
  document.documentElement.addEventListener('pointerleave', () => { mouseKnown = false; hide(); });
  window.addEventListener('blur', () => { mouseKnown = false; hide(); });
  window.addEventListener('scroll', () => {
    if (!mouseKnown) return;
    const target = document.elementFromPoint(x,y);
    if (target) move({target, pointerType:'mouse', clientX:x, clientY:y});
    else hide();
  }, {passive:true});
  document.addEventListener('visibilitychange', () => { if (document.hidden) hide(); });
  fine.addEventListener('change', hide);
  reduced.addEventListener('change', hide);
})();
