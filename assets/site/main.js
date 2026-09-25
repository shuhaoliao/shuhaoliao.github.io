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
const videos = [...document.querySelectorAll('video[data-src]')];
const visibleVideos = new Set();
let motionEnabled = !reducedMotion.matches;
function motionLabel() {
  motionButton.textContent = motionEnabled ? 'Ⅱ Pause previews' : '▷ Play previews';
  motionButton.setAttribute('aria-pressed', String(motionEnabled));
}
function syncVideos() {
  videos.forEach(video => {
    const shouldPlay = motionEnabled && visibleVideos.has(video) && !document.hidden;
    if (shouldPlay) {
      if (!video.getAttribute('src')) video.src = video.dataset.src;
      video.play().catch(() => { /* Its poster remains visible if autoplay is unavailable. */ });
    } else video.pause();
  });
}
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.isIntersecting ? visibleVideos.add(entry.target) : visibleVideos.delete(entry.target));
    syncVideos();
  }, { threshold: 0.12 });
  videos.forEach(video => observer.observe(video));
} else videos.forEach(video => visibleVideos.add(video));
motionButton.addEventListener('click', () => { motionEnabled = !motionEnabled; motionLabel(); syncVideos(); });
reducedMotion.addEventListener('change', event => { motionEnabled = !event.matches; motionLabel(); syncVideos(); });
document.addEventListener('visibilitychange', syncVideos);
motionLabel();
syncVideos();
