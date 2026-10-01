(() => {
  'use strict';

  const slides = Array.from(document.querySelectorAll('.slide'));
  const get = (id) => document.getElementById(id);
  const viewport = get('viewport');
  const canvas = get('canvas');
  const controls = {
    prev: get('prev'), next: get('next'), overview: get('overview-toggle'),
    notes: get('notes-toggle'), fullscreen: get('fullscreen'),
  };
  const overview = get('overview');
  const notes = get('notes');
  let current = 0;
  let savedFocus = null;
  if (!slides.length || !canvas || !viewport) return;

  const clamp = (value, minimum, maximum) => Math.min(maximum, Math.max(minimum, value));
  const titleFor = (index) => slides[index].dataset.title || `Slide ${index + 1}`;

  function scaleCanvas() {
    const toolbar = get('toolbar');
    const toolbarHeight = toolbar ? toolbar.getBoundingClientRect().height : 64;
    viewport.style.bottom = `${toolbarHeight}px`;
    if (get('progress')) get('progress').style.bottom = `${Math.max(0, toolbarHeight - 1)}px`;
    const bounds = viewport.getBoundingClientRect();
    const scale = Math.min(bounds.width / 1280, bounds.height / 720);
    canvas.style.transform = `translate(${(bounds.width - 1280 * scale) / 2}px, ${(bounds.height - 720 * scale) / 2}px) scale(${scale})`;
  }

  function hashState() {
    const params = new URLSearchParams(location.hash.slice(1));
    const slideNumber = Number(params.get('slide'));
    return clamp(Number.isFinite(slideNumber) && slideNumber > 0 ? Math.floor(slideNumber) - 1 : 0, 0, slides.length - 1);
  }

  function saveHash() {
    const hash = `#slide=${current + 1}`;
    if (location.hash === hash) return;
    // replaceState may be restricted for local files in some browsers.
    try { history.replaceState(null, '', hash); }
    catch { location.hash = hash; }
  }

  function render({ writeHash = true } = {}) {
    slides.forEach((slide, index) => {
      const active = index === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.inert = !active;
    });
    if (get('counter')) get('counter').textContent = `${current + 1} / ${slides.length}`;
    if (get('progress')) {
      get('progress').style.transform = `scaleX(${(current + 1) / slides.length})`;
      get('progress').setAttribute('aria-valuemax', String(slides.length));
      get('progress').setAttribute('aria-valuenow', String(current + 1));
      get('progress').setAttribute('aria-valuetext', `Slide ${current + 1} of ${slides.length}`);
    }
    if (controls.prev) controls.prev.disabled = current === 0;
    if (controls.next) controls.next.disabled = current === slides.length - 1;
    if (notes) notes.textContent = slides[current].dataset.notes || 'No presenter notes for this slide.';
    if (overview) overview.querySelectorAll('button').forEach((button, index) => button.setAttribute('aria-current', String(index === current)));
    if (get('announcer')) get('announcer').textContent = `Slide ${current + 1} of ${slides.length}. ${titleFor(current)}.`;
    document.title = `${titleFor(current)} · Vibe Coding Workshop`;
    if (writeHash) saveHash();
  }

  function navigate(index) {
    current = clamp(index, 0, slides.length - 1);
    render();
  }

  function advance() {
    if (current < slides.length - 1) navigate(current + 1);
  }

  function reverse() {
    if (current > 0) navigate(current - 1);
  }

  function togglePanel(panel, button, force) {
    if (!panel) return;
    const open = force === undefined ? panel.hidden : force;
    const other = panel === overview ? notes : overview;
    const otherButton = panel === overview ? controls.notes : controls.overview;
    if (open) {
      savedFocus = document.activeElement;
      if (other) other.hidden = true;
      if (otherButton) otherButton.setAttribute('aria-expanded', 'false');
    }
    panel.hidden = !open;
    if (button) button.setAttribute('aria-expanded', String(open));
    if (open && panel === overview) panel.querySelector('[aria-current="true"]')?.focus();
    if (!open && savedFocus instanceof HTMLElement && savedFocus.isConnected) savedFocus.focus();
  }

  async function toggleFullscreen() {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen();
      else if (get('announcer')) get('announcer').textContent = 'Use the browser fullscreen shortcut to present.';
    } catch {
      if (get('announcer')) get('announcer').textContent = 'Use the browser fullscreen shortcut to present.';
    }
  }

  if (overview) slides.forEach((_, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    const number = document.createElement('span');
    number.className = 'overview-number';
    number.textContent = String(index + 1).padStart(2, '0');
    button.append(number, document.createTextNode(titleFor(index)));
    button.addEventListener('click', () => { navigate(index); togglePanel(overview, controls.overview, false); });
    overview.append(button);
  });

  controls.prev?.addEventListener('click', reverse);
  controls.next?.addEventListener('click', advance);
  controls.overview?.addEventListener('click', () => togglePanel(overview, controls.overview));
  controls.notes?.addEventListener('click', () => togglePanel(notes, controls.notes));
  controls.fullscreen?.addEventListener('click', toggleFullscreen);
  canvas.addEventListener('click', (event) => {
    if (event.target.closest('a, button, input, textarea, select, [contenteditable="true"]')) return;
    if (window.getSelection()?.toString()) return;
    advance();
  });

  document.addEventListener('keydown', (event) => {
    if (event.ctrlKey || event.metaKey || event.altKey || event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
    if (event.key === 'Escape') {
      if (overview && !overview.hidden) togglePanel(overview, controls.overview, false);
      else if (notes && !notes.hidden) togglePanel(notes, controls.notes, false);
      return;
    }
    // Preserve Space/Enter on focused controls and arrow keys in the overview.
    if (event.target.closest('button, a') && [' ', 'Enter'].includes(event.key)) return;
    if (overview && !overview.hidden && ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      const buttons = Array.from(overview.querySelectorAll('button'));
      const index = buttons.indexOf(document.activeElement);
      const direction = ['ArrowRight', 'ArrowDown'].includes(event.key) ? 1 : -1;
      buttons[clamp(index + direction, 0, buttons.length - 1)]?.focus();
      event.preventDefault();
      return;
    }
    const actions = {
      ' ': advance, ArrowRight: advance, PageDown: advance,
      ArrowLeft: reverse, Backspace: reverse, PageUp: reverse,
      Home: () => navigate(0), End: () => navigate(slides.length - 1),
      f: toggleFullscreen, F: toggleFullscreen,
      o: () => togglePanel(overview, controls.overview), O: () => togglePanel(overview, controls.overview),
      n: () => togglePanel(notes, controls.notes), N: () => togglePanel(notes, controls.notes),
    };
    if (actions[event.key]) { event.preventDefault(); actions[event.key](); }
  });
  window.addEventListener('resize', scaleCanvas);
  if (window.ResizeObserver) {
    const resizeObserver = new ResizeObserver(scaleCanvas);
    resizeObserver.observe(viewport);
    if (get('toolbar')) resizeObserver.observe(get('toolbar'));
  }
  window.addEventListener('hashchange', () => {
    current = hashState();
    render();
  });
  document.addEventListener('fullscreenchange', () => {
    controls.fullscreen?.setAttribute('aria-pressed', String(Boolean(document.fullscreenElement)));
    scaleCanvas();
  });
  current = hashState();
  scaleCanvas();
  render();
})();
