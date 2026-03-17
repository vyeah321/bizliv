// footer-loader.js
// Loads the shared footer HTML and applies i18n strings from /i18n/<lang>.json

(async function() {
  function detectLang() {
    const pathSegments = location.pathname.split('/').filter(Boolean);
    const locales = ['ja', 'en', 'zhhans', 'zhhant'];
    for (let i = 0; i < pathSegments.length; i++) {
      const seg = pathSegments[i];
      if (locales.includes(seg)) return seg;
    }
    return 'en';
  }

  try {
    const lang = detectLang();
    const langPath = lang === 'en' ? 'en' : lang;

    const res = await fetch('/_includes/footer.html');
    if (!res.ok) throw new Error('Failed to fetch footer');

    let html = await res.text();
    html = html.replace(/{{langPath}}/g, langPath);

    const wrapper = document.createElement('div');
    wrapper.innerHTML = html;
    const footer = wrapper.firstElementChild;
    if (!footer) throw new Error('Footer template is empty');

    const i18nRes = await fetch('/i18n/' + lang + '.json');
    let strings = {};
    if (i18nRes.ok) {
      strings = await i18nRes.json();
    }

    footer.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (strings[key]) {
        el.textContent = strings[key];
      }
    });

    document.body.appendChild(footer);
  } catch (err) {
    console.error('footer-loader error', err);
  }
})();