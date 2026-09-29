'use strict';
const themeButton = document.querySelector('#theme-toggle');
function themeLabel() {
  themeButton.setAttribute('aria-label', document.documentElement.dataset.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
}
themeLabel();
themeButton.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem('shuhao-theme', next); } catch (_) {}
  themeLabel();
});

const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const motionButton = document.querySelector('#motion-toggle');
motionButton.hidden = false;
const previews = [...document.querySelectorAll('video[data-src], img[data-animated-src]')];
const visiblePreviews = new Set();
let motionEnabled = !reducedMotion.matches;
function motionLabel() {
  motionButton.textContent = motionEnabled ? 'Ⅱ Pause previews' : '▷ Play previews';
  motionButton.setAttribute('aria-pressed', String(motionEnabled));
}
function syncPreviews() {
  previews.forEach(preview => {
    const shouldPlay = motionEnabled && visiblePreviews.has(preview) && !document.hidden;
    if (preview.dataset.animatedSrc) {
      const source = shouldPlay ? preview.dataset.animatedSrc : preview.dataset.stillSrc;
      if (preview.getAttribute('src') !== source) preview.src = source;
      return;
    }
    if (shouldPlay) {
      if (!preview.getAttribute('src')) preview.src = preview.dataset.src;
      preview.play().catch(() => { /* Its poster remains visible if autoplay is unavailable. */ });
    } else preview.pause();
  });
}
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.isIntersecting ? visiblePreviews.add(entry.target) : visiblePreviews.delete(entry.target));
    syncPreviews();
  }, { threshold: 0.12 });
  previews.forEach(preview => observer.observe(preview));
} else previews.forEach(preview => visiblePreviews.add(preview));
motionButton.addEventListener('click', () => { motionEnabled = !motionEnabled; motionLabel(); syncPreviews(); });
reducedMotion.addEventListener('change', event => { motionEnabled = !event.matches; motionLabel(); syncPreviews(); });
document.addEventListener('visibilitychange', syncPreviews);
motionLabel();
syncPreviews();
