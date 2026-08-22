(() => {
  const flow = document.getElementById('coverflow');
  if (!flow) return;

  const items = [...flow.querySelectorAll('.cover-item')];
  const prev = document.getElementById('prev-game');
  const next = document.getElementById('next-game');
  const switchSound = new Audio('../assets/audio/oot-mainmenu-select.wav');
  switchSound.preload = 'auto';
  switchSound.volume = 0.45;

  const selectedTitle = document.getElementById('selected-title');
  const navIntro = document.getElementById('series-nav-intro');
  const navOverview = document.getElementById('series-nav-overview');
  const navFeatures = document.getElementById('series-nav-features');
  const navDownload = document.getElementById('series-nav-download');
  const actionOverview = document.getElementById('series-action-overview');
  const actionDownload = document.getElementById('series-action-download');
  const hero = document.getElementById('game-detail');
  const heroTitle = document.getElementById('hero-title');
  const heroStatus = document.getElementById('hero-status');
  const heroDate = document.getElementById('hero-date');
  const patchTitle = document.getElementById('patch-title');
  const patchState = document.getElementById('patch-state');
  const patchText = document.getElementById('patch-text');
  const gamePages = [...document.querySelectorAll('[data-game-page]')];

  const STEP_RADIANS = (Math.PI * 2) / items.length;
  const SNAP_DURATION = 620;
  const DRAG_PIXELS_PER_STEP = 260;
  const reduceMotion = false;

  const games = {
    oot: {
      name: '시간의 오카리나',
      status: '배포 중',
      date: '2026.01.10',
      patchTitle: '시간의 오카리나 한국어 패치',
      patchState: '한국어 패치 배포 중',
      patchText: '시간의 오카리나 한국어 패치 정보와 다운로드 항목을 이 프레임에서 이어서 제공합니다.',
      theme: 'oot',
      nav: ['#oot-game-intro', '#oot-overview', '#oot-features', '#oot-download']
    },
    mm: {
      name: '무쥬라의 가면',
      status: '배포 중',
      date: '2026.08.23',
      patchTitle: '무쥬라의 가면 한국어 패치',
      patchState: '한국어 패치 배포 중',
      patchText: '일본판 Rev A를 기준으로 다시 작업한 무쥬라의 가면 한국어 패치를 배포합니다.',
      theme: 'mm',
      nav: ['#mm-game-intro', '#mm-overview', '#mm-features', '#mm-download']
    },
    ura: {
      name: '시간의 오카리나 우라',
      status: '배포 중',
      date: '2026.01.10',
      patchTitle: '시간의 오카리나 우라 한국어 패치',
      patchState: '한국어 패치 배포 중',
      patchText: '시간의 오카리나 우라 한국어 패치 정보와 다운로드 항목을 이 프레임에서 이어서 제공합니다.',
      theme: 'ura',
      nav: ['#ura-intro', '#ura-overview', '#ura-features', '#ura-download']
    }
  };

  const requested = new URLSearchParams(location.search).get('game');
  const initialGame = games[requested] ? requested : (document.body.dataset.activeGame || 'mm');
  let active = Math.max(0, items.findIndex((item) => item.dataset.game === initialGame));
  let rotation = active;
  let animationFrame = 0;
  let isAnimating = false;
  let isDragging = false;
  let dragPointerId = null;
  let dragStartX = 0;
  let dragStartRotation = 0;
  let dragMoved = false;
  let suppressClick = false;

  function modulo(value, divisor) {
    return ((value % divisor) + divisor) % divisor;
  }

  function nearestIndex(value) {
    return modulo(Math.round(value), items.length);
  }

  function getRadius() {
    if (window.innerWidth <= 560) return 235;
    if (window.innerWidth <= 820) return 305;
    return 390;
  }

  function renderOrbit() {
    const radius = getRadius();
    const depth = radius * 0.55;
    const zOffset = radius * 0.25;
    const nearest = nearestIndex(rotation);

    items.forEach((item, index) => {
      const angle = (index - rotation) * STEP_RADIANS;
      const sin = Math.sin(angle);
      const cos = Math.cos(angle);
      const x = sin * radius;
      const z = (cos * depth) - zOffset;
      const y = (1 - cos) * 7;
      const wrappedAngle = Math.atan2(sin, cos);
      const degrees = wrappedAngle * (180 / Math.PI);
      const faceDegrees = -degrees * 0.38;
      const frontness = Math.max(0, Math.min(1, (cos + 1) / 2));
      const scale = 0.88 + (frontness * 0.12);
      const opacity = 0.42 + (frontness * 0.58);
      const brightness = 0.72 + (frontness * 0.28);
      const saturation = 0.68 + (frontness * 0.32);
      const position = index === nearest ? 'center' : (sin < 0 ? 'left' : 'right');

      item.style.transform = `translateX(-50%) translate3d(${x.toFixed(2)}px, ${y.toFixed(2)}px, ${z.toFixed(2)}px) rotateY(${faceDegrees.toFixed(2)}deg) scale(${scale.toFixed(4)})`;
      item.style.opacity = opacity.toFixed(3);
      item.style.filter = `saturate(${saturation.toFixed(3)}) brightness(${brightness.toFixed(3)})`;
      item.style.zIndex = String(Math.round((cos + 1) * 50));
      item.dataset.position = position;
      item.setAttribute('aria-current', index === nearest ? 'true' : 'false');
      item.tabIndex = index === nearest ? 0 : -1;
    });
  }

  function setLocked(locked) {
    isAnimating = locked;
    if (prev) prev.disabled = locked;
    if (next) next.disabled = locked;
  }

  function updateUrl(game) {
    const url = new URL(location.href);
    url.searchParams.set('game', game);
    history.replaceState(null, '', url);
  }

  function updateSelectedTitle(game) {
    if (!selectedTitle) return;
    selectedTitle.innerHTML = game === 'ura' ? '시간의 오카리나 <em>우라</em>' : games[game].name;
  }

  function applyDetail(game, animate = true) {
    const data = games[game];
    if (!data || !hero) return;

    if (animate) hero.classList.add('is-changing');

    updateSelectedTitle(game);
    document.body.dataset.selectedGame = data.theme;
    document.title = `젤다의 전설: ${data.name} — 한마루 한글화 작업소`;
    if (heroTitle) heroTitle.textContent = data.name;
    if (heroStatus) heroStatus.textContent = data.status;
    if (heroDate) heroDate.textContent = data.date;
    if (patchTitle) patchTitle.textContent = data.patchTitle;
    if (patchState) patchState.textContent = data.patchState;
    if (patchText) patchText.textContent = data.patchText;
    [navIntro, navOverview, navFeatures, navDownload].forEach((link, index) => {
      if (link && data.nav?.[index]) link.href = data.nav[index];
    });
    if (actionOverview && data.nav?.[1]) actionOverview.href = data.nav[1];
    if (actionDownload && data.nav?.[3]) actionDownload.href = data.nav[3];
    gamePages.forEach((page) => {
      const isActive = page.dataset.gamePage === game;
      page.hidden = !isActive;
      page.classList.remove('page-enter');
      if (isActive) {
        void page.offsetWidth;
        page.classList.add('page-enter');
      }
    });
    hero.dataset.game = data.theme;
    hero.classList.remove('is-changing');
    hero.classList.remove('detail-enter');
    void hero.offsetWidth;
    hero.classList.add('detail-enter');
  }

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function animateTo(targetRotation, focus = false) {
    cancelAnimationFrame(animationFrame);

    if (reduceMotion) {
      rotation = targetRotation;
      active = nearestIndex(rotation);
      renderOrbit();
      commitActive(focus, false);
      return;
    }

    const from = rotation;
    const distance = targetRotation - from;
    const start = performance.now();
    setLocked(true);

    const tick = (now) => {
      const progress = Math.min(1, (now - start) / SNAP_DURATION);
      rotation = from + (distance * easeOutCubic(progress));
      renderOrbit();

      if (progress < 1) {
        animationFrame = requestAnimationFrame(tick);
        return;
      }

      rotation = targetRotation;
      active = nearestIndex(rotation);
      renderOrbit();
      setLocked(false);
      commitActive(focus, true);
    };

    animationFrame = requestAnimationFrame(tick);
  }

  function commitActive(focus = false, animateDetail = true) {
    const game = items[active]?.dataset.game;
    if (!game || !games[game]) return;
    updateUrl(game);
    applyDetail(game, animateDetail);
    if (focus) items[active]?.focus({ preventScroll: true });
  }

  function move(direction, focus = false) {
    if (isAnimating || isDragging || !items.length) return;
    switchSound.currentTime = 0;
    switchSound.play().catch(() => {});
    animateTo(Math.round(rotation) + direction, focus);
  }

  function select(index, focus = false) {
    if (isAnimating || isDragging || index === active) return;
    const forward = modulo(index - active, items.length);
    move(forward === 1 ? 1 : -1, focus);
  }

  function beginDrag(event) {
    if (reduceMotion || isAnimating || event.button !== 0) return;
    isDragging = true;
    dragPointerId = event.pointerId;
    dragStartX = event.clientX;
    dragStartRotation = rotation;
    dragMoved = false;
    suppressClick = false;
    flow.classList.add('is-dragging');
    flow.setPointerCapture?.(event.pointerId);
  }

  function updateDrag(event) {
    if (!isDragging || event.pointerId !== dragPointerId) return;
    const deltaX = event.clientX - dragStartX;
    if (Math.abs(deltaX) > 6) dragMoved = true;
    const rawRotation = dragStartRotation - (deltaX / DRAG_PIXELS_PER_STEP);
    const min = dragStartRotation - 1.15;
    const max = dragStartRotation + 1.15;
    rotation = Math.max(min, Math.min(max, rawRotation));
    renderOrbit();
  }

  function endDrag(event) {
    if (!isDragging || event.pointerId !== dragPointerId) return;
    flow.releasePointerCapture?.(event.pointerId);
    flow.classList.remove('is-dragging');
    isDragging = false;
    dragPointerId = null;

    const delta = rotation - dragStartRotation;
    suppressClick = dragMoved;

    let target = dragStartRotation;
    if (Math.abs(delta) >= 0.16) target += delta > 0 ? 1 : -1;

    if (target !== dragStartRotation) {
      switchSound.currentTime = 0;
      switchSound.play().catch(() => {});
    }

    animateTo(target, false);
  }

  items.forEach((item, index) => {
    item.addEventListener('click', (event) => {
      if (suppressClick) {
        event.preventDefault();
        suppressClick = false;
        return;
      }
      select(index, true);
    });
  });

  prev?.addEventListener('click', () => move(-1, true));
  next?.addEventListener('click', () => move(1, true));

  flow.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      move(-1, true);
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      move(1, true);
    }
  });

  flow.addEventListener('pointerdown', beginDrag);
  flow.addEventListener('pointermove', updateDrag);
  flow.addEventListener('pointerup', endDrag);
  flow.addEventListener('pointercancel', endDrag);

  window.addEventListener('resize', renderOrbit, { passive: true });

  renderOrbit();
  commitActive(false, false);
})();
