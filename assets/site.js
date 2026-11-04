// Analytics helper: a named, anonymous event in GoatCounter. Does nothing if the script is blocked or not loaded.
window.__event = (path, title) => { try { window.goatcounter && window.goatcounter.count && window.goatcounter.count({ path, title: title || path, event: true }); } catch (e) {} };

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
      const li = r.closest('[style*="--c"]'); peek.style.setProperty('--c', li ? getComputedStyle(li).getPropertyValue('--c') : '');
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
  // Prev/next stay inside the group you opened from: the highlights, or one chapter
  const all = [...document.querySelectorAll('.frame__zoom')];
  let btns = all, i = 0, opener = null;
  const show = n => {
    i = (n + btns.length) % btns.length;
    pic.src = btns[i].dataset.full;
    pic.alt = btns[i].querySelector('img').alt;
    count.textContent = `${i + 1} / ${btns.length}`;
    dlg.classList.remove('is-zoomed');
    dlg.querySelector('.viewer__scroll').scrollTo(0, 0);
  };
  all.forEach(b => b.addEventListener('click', () => {
    // A pick opens the viewer on its whole chapter, starting at that image
    const block = b.closest('.chapter__picks') && b.closest('.chapter-block');
    const group = block ? block.querySelector('.chapter__body') : b.closest('.bento, .chapter__body');
    btns = group ? [...group.querySelectorAll('.frame__zoom')] : all;
    let at = btns.indexOf(b);
    if (at < 0) at = Math.max(0, btns.findIndex(x => x.dataset.full === b.dataset.full));
    opener = b; show(at); dlg.showModal();
  }));
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

// Case-study chapters: links in the chapter list open their chapter; one button opens or closes them all.
(() => {
  const chapters = [...document.querySelectorAll('.chapter')];
  if (!chapters.length) return;
  document.querySelectorAll('[data-open-ch]').forEach(btn => btn.addEventListener('click', () => {
    const d = document.getElementById(btn.dataset.openCh); if (!d) return;
    d.open = true; d.querySelector('summary').focus({ preventScroll: true });
    d.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  }));
  document.querySelectorAll('[data-open]').forEach(a => a.addEventListener('click', () => {
    const d = document.getElementById(a.dataset.open); if (d) d.open = true;
  }));
  const allBtn = document.querySelector('[data-all]');
  const sync = () => {
    if (!allBtn) return;
    const open = chapters.every(c => c.open);
    allBtn.textContent = open ? 'Close all chapters' : 'Open all chapters';
    allBtn.setAttribute('aria-expanded', String(open));
  };
  allBtn && allBtn.addEventListener('click', () => {
    const open = !chapters.every(c => c.open);
    chapters.forEach(c => (c.open = open)); sync();
  });
  chapters.forEach(c => c.addEventListener('toggle', sync));
  const fromHash = () => { const d = location.hash && document.querySelector('.chapter' + location.hash); if (d) d.open = true; };
  fromHash(); addEventListener('hashchange', fromHash);
})();

// Enquiry form: writes the email for the client, nothing is stored or sent from here.
(() => {
  document.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = 'Copied'; }
    catch { b.textContent = 'Select and copy'; }
    setTimeout(() => (b.textContent = 'Copy'), 2000);
  }));
  const count = window.__event;
  // Coming from a case study? Pre-tick its service and mention the project. Everything stays editable.
  const params = new URLSearchParams(location.search);
  document.querySelectorAll('.start__form').forEach(f => {
    const need = params.get('need'), from = params.get('from');
    const titles = JSON.parse(f.dataset.projects || '{}');
    let filledSomething = false;
    if (need) { const box = [...f.querySelectorAll('input[name="need"]')].find(i => i.value === need); if (box) { box.checked = true; filledSomething = true; } }
    const msg = f.querySelector('textarea[name="message"]');
    if (from && titles[from] && msg && !msg.value) { msg.value = `I saw your ${titles[from]} case study and would like something similar.`; filledSomething = true; }
    const note = f.querySelector('.start__prefill');
    if (filledSomething && note) { note.hidden = false; note.querySelector('b').textContent = titles[from] || need; }
    // Form start: first time someone types or ticks something, once per page
    let started = false;
    const start = () => { if (started) return; started = true; count('form-start', 'Enquiry form started'); };
    f.addEventListener('input', start); f.addEventListener('change', start);
  });
  document.querySelectorAll('.start__form').forEach(f => f.addEventListener('submit', ev => {
    ev.preventDefault();
    const viaWa = ev.submitter && ev.submitter.value === 'whatsapp';
    const d = new FormData(f);
    const needs = d.getAll('need');
    const name = (d.get('name') || '').trim();
    const company = (d.get('company') || '').trim();
    const lines = [
      'Hi Ahmed,', '',
      `I'm ${name}${company ? ' from ' + company : ''}.`, '',
      'What I need: ' + (needs.length ? needs.join(', ') : 'Not sure yet'),
      'Timeline: ' + (d.get('timeline') || 'Not decided'),
      'Budget range: ' + ((d.get('budget') || '').trim() || 'Not decided'), '',
      'About the project:', (d.get('message') || '').trim() || '-', '',
      'Thanks,', name
    ];
    const subject = `New project: ${needs[0] && needs[0] !== 'Not sure yet' ? needs[0] : 'enquiry'}${company ? ' for ' + company : ''}`;
    const note = f.querySelector('.start__note');
    if (viaWa) {
      // WhatsApp: same message, without the email greeting/sign-off lines doubling up
      const url = `https://wa.me/${f.dataset.wa}?text=${encodeURIComponent(lines.join('\n'))}`;
      count('form-whatsapp', 'Enquiry form sent via WhatsApp');
      const a = Object.assign(document.createElement('a'), { href: url, target: '_blank', rel: 'noopener' });
      document.body.appendChild(a); a.click(); a.remove();
      note.textContent = "WhatsApp should open with your message ready. If it didn't, use the WhatsApp link next to the form.";
      note.classList.add('is-sent');
      return;
    }
    const url = `mailto:${f.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    count('form-email', 'Enquiry form sent by email');
    (window.__mailto || (u => { location.href = u; }))(url);
    note.textContent = "Your email app should open now. If nothing happened, use the Copy button next to my email address.";
    note.classList.add('is-sent');
  }));
})();

// "Ask about this" on the services page ticks the matching box in the form.
document.querySelectorAll('[data-need]').forEach(a => a.addEventListener('click', () => {
  const box = [...document.querySelectorAll('.start__form input[name="need"]')].find(i => i.value === a.dataset.need);
  if (box) box.checked = true;
}));

// Work filters: tap a label to see only that kind of project.
(() => {
  const chips = [...document.querySelectorAll('.fchip')];
  if (!chips.length) return;
  const items = [...document.querySelectorAll('.feats .item, .rows .item')];
  const status = document.querySelector('.filters__status');
  chips.forEach(c => c.addEventListener('click', () => {
    const f = c.dataset.filter;
    chips.forEach(x => x.setAttribute('aria-pressed', String(x === c)));
    let n = 0;
    items.forEach(it => {
      const show = f === 'all' || it.dataset.tags.split(' ').includes(f);
      it.classList.toggle('is-hidden', !show);
      it.classList.remove('is-in');
      if (show) { n++; void it.offsetWidth; it.classList.add('is-in'); }
    });
    if (status) status.textContent = f === 'all' ? `${n} projects` : `${n} of ${items.length} projects`;
  }));
})();

// Floating "Start a project": shows once you're past the top, hides near the form.
(() => {
  const fl = document.querySelector('.float');
  if (!fl) return;
  const form = document.querySelector('#start');
  let formVisible = false;
  if (form && 'IntersectionObserver' in window)
    new IntersectionObserver(([en]) => { formVisible = en.isIntersecting; tick(); }, { threshold: 0.05 }).observe(form);
  const tick = () => fl.classList.toggle('is-on', scrollY > innerHeight * 0.7 && !formVisible);
  addEventListener('scroll', tick, { passive: true });
  tick();
})();

// Top bar turns solid once the page scrolls, so it stays readable over any image.
(() => {
  const bar = document.querySelector('.bar');
  if (!bar) return;
  const set = () => bar.classList.toggle('is-solid', scrollY > 40);
  addEventListener('scroll', set, { passive: true }); set();
})();

// Custom cursor (from V2): a dot that grows over links and says "View" over work, "Zoom" over images.
(() => {
  const cur = document.querySelector('.cursor');
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!cur || !fine || still) return;
  document.body.classList.add('has-cursor');
  const label = cur.querySelector('.cursor__label');
  let x = -100, y = -100, cx = -100, cy = -100;
  addEventListener('mousemove', ev => { x = ev.clientX; y = ev.clientY; cur.classList.add('is-on'); }, { passive: true });
  document.addEventListener('mouseleave', () => cur.classList.remove('is-on'));
  // Animate only while the dot is catching up with the mouse; stop when it has, so the page sits idle.
  let raf = 0;
  const loop = () => {
    cx += (x - cx) * .25; cy += (y - cy) * .25;
    cur.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
    raf = (Math.abs(x - cx) > .3 || Math.abs(y - cy) > .3) ? requestAnimationFrame(loop) : 0;
  };
  addEventListener('mousemove', () => { if (!raf) raf = requestAnimationFrame(loop); }, { passive: true });
  // A modal <dialog> sits in the top layer, so carry the dot inside it while it is open.
  document.querySelectorAll('dialog').forEach(d => {
    new MutationObserver(() => (d.open ? d : document.body).appendChild(cur)).observe(d, { attributes: true, attributeFilter: ['open'] });
  });
  const textFor = t => {
    if (!t) return '';
    if (t.dataset.cursor) return t.dataset.cursor;
    if (t.matches('.frame__zoom')) return 'Zoom';
    const h = t.getAttribute('href') || '';
    if (/(^|\/)work\/[^/#]+\/(index\.html)?$/.test(h) && !t.closest('.bar, .foot')) return 'View';
    return '';
  };
  document.addEventListener('mouseover', ev => {
    const t = ev.target.closest('[data-cursor], a, button, summary, label');
    const txt = textFor(t);
    cur.classList.toggle('is-label', !!txt); cur.classList.toggle('is-link', !!t && !txt);
    label.textContent = txt;
  });
})();

// Case-study engagement events: reached 75% of the page, opened a chapter, opened the image viewer. Each once per page view.
(() => {
  const slug = document.body.dataset.slug;
  if (!slug) return;
  const once = new Set();
  const ev = (key, title) => { if (once.has(key)) return; once.add(key); window.__event(key, title); };
  addEventListener('scroll', () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (max > 0 && scrollY / max >= 0.75) ev(`case-75-${slug}`, `Case study read to 75%: ${slug}`);
  }, { passive: true });
  document.querySelectorAll('.chapter').forEach(d => d.addEventListener('toggle', () => { if (d.open) ev(`chapter-open-${slug}`, `Chapter opened: ${slug}`); }));
  const dlg = document.querySelector('.viewer');
  if (dlg) new MutationObserver(() => { if (dlg.open) ev(`viewer-open-${slug}`, `Image viewer opened: ${slug}`); }).observe(dlg, { attributes: true, attributeFilter: ['open'] });
})();

// Featured previews: on desktop, hovering a small image shows it in the card; leaving the card restores the cover.
(() => {
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  document.querySelectorAll('.feat__link').forEach(card => {
    const main = card.querySelector('.feat__img');
    const strip = card.querySelectorAll('.feat__strip img');
    if (!main || !strip.length) return;
    const orig = { src: main.getAttribute('src'), srcset: main.getAttribute('srcset') };
    let used = false;
    strip.forEach(t => t.addEventListener('mouseenter', () => {
      strip.forEach(x => x.classList.toggle('is-on', x === t));
      main.removeAttribute('srcset'); main.src = t.dataset.full;
      if (!used) { used = true; window.__event('feat-preview-' + card.getAttribute('href').split('/').slice(-2, -1)[0], 'Featured preview used'); }
    }));
    card.addEventListener('mouseleave', () => {
      strip.forEach(x => x.classList.remove('is-on'));
      main.src = orig.src; if (orig.srcset) main.setAttribute('srcset', orig.srcset);
    });
  });
})();
