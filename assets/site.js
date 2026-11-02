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

// Pause the hero wall when it's off-screen (saves battery).
(() => {
  const wall = document.querySelector('.wall');
  if (!wall || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(([en]) => wall.classList.toggle('is-paused', !en.isIntersecting)).observe(wall);
})();

// Page transition: the clicked project's cover morphs into the case-study cover.
(() => {
  document.querySelectorAll('a.row').forEach(a => a.addEventListener('click', () => {
    const peek = document.querySelector('.peek.is-on img');
    const thumb = a.querySelector('.row__thumb');
    const el = peek || (thumb && thumb.offsetParent ? thumb : null);
    if (el) {
      document.querySelectorAll('.case__cover').forEach(c => c.style.viewTransitionName = 'none');
      el.style.viewTransitionName = 'hero-cover';
    }
  }));
  // undo if the person comes back with the back button
  addEventListener('pageshow', () => document.querySelectorAll('[style*="view-transition-name"]').forEach(el => el.style.viewTransitionName = ''));
})();

// Frame viewer: tap a frame to see it full size, tap again to zoom, arrows to move.
(() => {
  const dlg = document.querySelector('.viewer');
  if (!dlg) return;
  const pic = dlg.querySelector('.viewer__img'), count = dlg.querySelector('.viewer__count');
  const btns = [...document.querySelectorAll('.frame__zoom')];
  let i = 0, opener = null;
  const show = n => {
    i = (n + btns.length) % btns.length;
    pic.src = btns[i].dataset.full;
    pic.alt = btns[i].querySelector('img').alt;
    count.textContent = `${i + 1} / ${btns.length}`;
    dlg.classList.remove('is-zoomed');
    dlg.querySelector('.viewer__scroll').scrollTo(0, 0);
  };
  btns.forEach((b, n) => b.addEventListener('click', () => { opener = b; show(n); dlg.showModal(); }));
  dlg.addEventListener('click', ev => {
    const v = ev.target.dataset && ev.target.dataset.v;
    if (v === 'prev') show(i - 1);
    else if (v === 'next') show(i + 1);
    else if (v === 'close') dlg.close();
    else if (ev.target === pic) dlg.classList.toggle('is-zoomed');
  });
  dlg.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowRight') show(i + 1);
    if (ev.key === 'ArrowLeft') show(i - 1);
  });
  dlg.addEventListener('close', () => { pic.removeAttribute('src'); opener && opener.focus(); });
})();
