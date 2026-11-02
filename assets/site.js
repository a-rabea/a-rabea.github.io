// Ahmed Rabea portfolio, V2 interactions. Everything degrades to a plain, working page without JS.
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Section reveals: one consistent entrance
  const rev = $$('.reveal');
  if ('IntersectionObserver' in window && !still) {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
    rev.forEach(el => io.observe(el));
  } else rev.forEach(el => el.classList.add('is-in'));

  // Bar turns solid on scroll; reading progress on case pages
  const bar = $('.bar'), prog = $('.progress');
  let tick = false;
  const onScroll = () => {
    if (tick) return; tick = true;
    requestAnimationFrame(() => {
      bar && bar.classList.toggle('is-solid', scrollY > 40);
      if (prog) { const max = document.documentElement.scrollHeight - innerHeight; prog.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`; }
      tick = false;
    });
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Pause the hero wall when it's off-screen
  const wall = $('.wall');
  if (wall && 'IntersectionObserver' in window) new IntersectionObserver(([en]) => wall.classList.toggle('is-paused', !en.isIntersecting)).observe(wall);

  // Cover preview that follows the cursor over project rows
  const peek = $('.peek');
  if (peek && !still && fine) {
    const pic = $('img', peek); let x = 0, y = 0, cx = 0, cy = 0, on = false, raf = 0;
    const loop = () => { cx += (x - cx) * .16; cy += (y - cy) * .16; peek.style.left = cx + 'px'; peek.style.top = cy + 'px'; raf = on || Math.abs(x - cx) > .5 ? requestAnimationFrame(loop) : 0; };
    $$('.row[data-peek]').forEach(r => {
      const i = new Image(); i.src = r.dataset.peek;
      r.addEventListener('mouseenter', ev => {
        pic.src = r.dataset.peek; const li = r.closest('[style*="--c"]');
        peek.style.setProperty('--c', li ? getComputedStyle(li).getPropertyValue('--c') : '');
        if (!on) { cx = x = ev.clientX; cy = y = ev.clientY; }
        on = true; peek.classList.add('is-on'); if (!raf) raf = requestAnimationFrame(loop);
      });
      r.addEventListener('mousemove', ev => { x = ev.clientX; y = ev.clientY; });
      r.addEventListener('mouseleave', () => { on = false; peek.classList.remove('is-on'); });
    });
    addEventListener('scroll', () => { if (on) { on = false; peek.classList.remove('is-on'); } }, { passive: true });
  }

  // Custom cursor: a dot that grows over links and shows a label over work
  const cur = $('.cursor');
  if (cur && fine && !still) {
    document.body.classList.add('has-cursor');
    const label = $('.cursor__label', cur); let x = -100, y = -100, cx = -100, cy = -100;
    addEventListener('mousemove', ev => { x = ev.clientX; y = ev.clientY; cur.classList.add('is-on'); }, { passive: true });
    document.addEventListener('mouseleave', () => cur.classList.remove('is-on'));
    const loop = () => { cx += (x - cx) * .25; cy += (y - cy) * .25; cur.style.transform = `translate3d(${cx}px, ${cy}px, 0)`; requestAnimationFrame(loop); };
    loop();
    document.addEventListener('mouseover', ev => {
      const t = ev.target.closest('[data-cursor], a, button, summary, label');
      const txt = t && t.dataset.cursor;
      cur.classList.toggle('is-label', !!txt); cur.classList.toggle('is-link', !!t && !txt);
      label.textContent = txt || '';
    });
  }

  // Work filters
  const chips = $$('.fchip');
  if (chips.length) {
    const items = $$('.rows .item'), status = $('.filters__status');
    chips.forEach(c => c.addEventListener('click', () => {
      const f = c.dataset.filter; let n = 0;
      chips.forEach(x => x.setAttribute('aria-pressed', String(x === c)));
      items.forEach(it => {
        const show = f === 'all' || it.dataset.tags.split(' ').includes(f);
        it.classList.toggle('is-hidden', !show); it.classList.remove('is-in');
        if (show) { n++; void it.offsetWidth; it.classList.add('is-in'); }
      });
      if (status) status.textContent = f === 'all' ? `${n} projects` : `${n} of ${items.length} projects`;
    }));
  }

  // Floating "Start a project": appears after the first screen, hides near the contact form
  const fl = $('.float');
  if (fl) {
    const form = $('#contact'); let near = false;
    const set = () => fl.classList.toggle('is-on', scrollY > innerHeight * .7 && !near);
    if (form && 'IntersectionObserver' in window) new IntersectionObserver(([en]) => { near = en.isIntersecting; set(); }, { threshold: .05 }).observe(form);
    addEventListener('scroll', set, { passive: true }); set();
  }

  // Page transition: the clicked cover morphs into the case-study cover
  $$('a.row, a.feat, a.pn__item').forEach(a => a.addEventListener('click', () => {
    const el = $('.peek.is-on img') || $('.feat__img img', a) || ((t => t && t.offsetParent ? t : null)($('.row__thumb', a)));
    if (el) { $$('.case__cover').forEach(c => c.style.viewTransitionName = 'none'); el.style.viewTransitionName = 'hero-cover'; }
  }));
  addEventListener('pageshow', () => $$('[style*="view-transition-name"]').forEach(el => el.style.viewTransitionName = ''));

  // Chapters: side nav opens the chapter it points to; "Open all"; highlight the current one
  const chaps = $$('.chapter');
  if (chaps.length) {
    $$('[data-open]').forEach(a => a.addEventListener('click', () => { const d = document.getElementById(a.dataset.open); if (d) d.open = true; }));
    const all = $('[data-all]');
    if (all) all.addEventListener('click', () => {
      const open = !chaps.every(d => d.open);
      chaps.forEach(d => d.open = open);
      all.textContent = open ? 'Close all chapters' : 'Open all chapters';
    });
    if (location.hash.startsWith('#ch-')) { const d = $(location.hash); if (d) d.open = true; }
    const links = $$('.chapters__nav a');
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(es => es.forEach(en => {
        if (en.isIntersecting) links.forEach(l => l.classList.toggle('is-current', l.dataset.open === en.target.id));
      }), { rootMargin: '-40% 0px -55% 0px' });
      chaps.forEach(c => io.observe(c));
    }
  }

  // Frame viewer: tap any frame to see it full size; tap again to zoom; arrows to move
  const dlg = $('.viewer');
  if (dlg) {
    const pic = $('.viewer__img', dlg), count = $('.viewer__count', dlg);
    let list = [], i = 0, opener = null;
    const show = n => {
      i = (n + list.length) % list.length;
      pic.src = list[i].dataset.full; pic.alt = $('img', list[i]).alt;
      count.textContent = `${i + 1} / ${list.length}`;
      dlg.classList.remove('is-zoomed'); $('.viewer__scroll', dlg).scrollTo(0, 0);
    };
    document.addEventListener('click', ev => {
      const b = ev.target.closest('.frame__zoom'); if (!b) return;
      const scope = b.closest('.bento, .chapter__body');
      list = $$('.frame__zoom', scope); opener = b; show(list.indexOf(b)); dlg.showModal();
    });
    dlg.addEventListener('click', ev => {
      const v = ev.target.closest('[data-v]'); const k = v && v.dataset.v;
      if (k === 'prev') show(i - 1); else if (k === 'next') show(i + 1); else if (k === 'close') dlg.close();
      else if (ev.target === pic) dlg.classList.toggle('is-zoomed');
    });
    dlg.addEventListener('keydown', ev => { if (ev.key === 'ArrowRight') show(i + 1); if (ev.key === 'ArrowLeft') show(i - 1); });
    dlg.addEventListener('close', () => { pic.removeAttribute('src'); opener && opener.focus(); });
  }

  // Enquiry form writes the email; nothing is stored or sent from the site
  $$('[data-copy]').forEach(b => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = 'Copied'; } catch { b.textContent = 'Select and copy'; }
    setTimeout(() => (b.textContent = 'Copy'), 2000);
  }));
  $$('.start__form').forEach(f => f.addEventListener('submit', ev => {
    ev.preventDefault();
    const d = new FormData(f), needs = d.getAll('need');
    const name = (d.get('name') || '').trim(), company = (d.get('company') || '').trim();
    const lines = ['Hi Ahmed,', '', `I'm ${name}${company ? ' from ' + company : ''}.`, '',
      'What I need: ' + (needs.length ? needs.join(', ') : 'Not sure yet'),
      'Timeline: ' + (d.get('timeline') || 'Not decided'),
      'Budget range: ' + ((d.get('budget') || '').trim() || 'Not decided'), '',
      'About the project:', (d.get('message') || '').trim() || '-', '', 'Thanks,', name];
    const subject = `New project: ${needs[0] && needs[0] !== 'Not sure yet' ? needs[0] : 'enquiry'}${company ? ' for ' + company : ''}`;
    const url = `mailto:${f.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    (window.__mailto || (u => { location.href = u; }))(url);
    $('.start__note', f).textContent = 'Your email app should open now. If nothing happened, use the Copy button next to my email address, or message me on WhatsApp.';
  }));
})();
