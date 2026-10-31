// Two effects: the hero wall of work drifts behind the name, and project covers follow the cursor.
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 1. Hero: the work wall shifts slightly with scroll; progress bar on case pages.
  const hero = document.querySelector('.hero');
  const bar = document.querySelector('.progress');
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = scrollY;
      if (hero && !still) hero.style.setProperty('--p', Math.min(1, y / (hero.offsetHeight * 0.9)).toFixed(3));
      if (bar) {
        const max = document.documentElement.scrollHeight - innerHeight;
        bar.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
      }
      ticking = false;
    });
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // 2. Cover peek: follows the cursor with a little lag over the project list.
  const peek = document.querySelector('.peek');
  if (!peek || still || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const pic = peek.querySelector('img');
  let x = 0, y = 0, cx = 0, cy = 0, on = false, raf = 0;
  const loop = () => {
    cx += (x - cx) * 0.16; cy += (y - cy) * 0.16;
    peek.style.left = cx + 'px'; peek.style.top = cy + 'px';
    raf = on || Math.abs(x - cx) > 0.5 ? requestAnimationFrame(loop) : 0;
  };
  const rows = document.querySelectorAll('[data-peek]');
  // warm the cache so the first hover isn't blank
  rows.forEach(r => { const i = new Image(); i.src = r.dataset.peek; });
  rows.forEach(r => {
    r.addEventListener('mouseenter', ev => {
      pic.src = r.dataset.peek;
      if (!on) { cx = x = ev.clientX; cy = y = ev.clientY; }
      on = true; peek.classList.add('is-on');
      if (!raf) raf = requestAnimationFrame(loop);
    });
    r.addEventListener('mousemove', ev => { x = ev.clientX; y = ev.clientY; });
    r.addEventListener('mouseleave', () => { on = false; peek.classList.remove('is-on'); });
  });
  addEventListener('scroll', () => { if (on) { on = false; peek.classList.remove('is-on'); } }, { passive: true });
})();
