try {
  const saved = localStorage.getItem('shuhao-theme');
  document.documentElement.dataset.theme = saved === 'dark' || saved === 'light'
    ? saved : matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
} catch (_) { /* The light theme remains available when storage is blocked. */ }
