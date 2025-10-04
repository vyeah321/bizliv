// header-loader.js
// Loads the shared header HTML and applies i18n strings from /i18n/<lang>.json

(async function() {
  function detectLang() {
    // simple heuristic: path /ja/ /en/ /zhhans/ /zhhant/
    const path = location.pathname;
    if (path.startsWith('/ja/')) return 'ja';
    if (path.startsWith('/zhhans/')) return 'zhhans';
    if (path.startsWith('/zhhant/')) return 'zhhant';
    return 'en';
  }

  const lang = detectLang();
  const langPath = lang === 'en' ? 'en' : lang;

    // fetch header template
    try {
      // determine app-specific include path (if any)
      const pathSegments = location.pathname.split('/').filter(Boolean);
      const locales = ['ja', 'en', 'zhhans', 'zhhant'];
      let appBase = null;
      if (pathSegments.length > 0) {
        if (!locales.includes(pathSegments[0])) {
          appBase = '/' + pathSegments[0];
        } else if (pathSegments.length > 1 && !locales.includes(pathSegments[1])) {
          appBase = '/' + pathSegments[1];
        }
      }

      let res = null;
      let html = null;

      // try app-specific include first
      if (appBase) {
        try {
          res = await fetch(appBase + '/_includes/header.html');
          if (res && res.ok) {
            html = await res.text();
          }
        } catch (e) {
          // fallthrough to root include
          res = null;
        }
      }

      // fallback to root include
      if (!html) {
        res = await fetch('/_includes/header.html');
        if (!res.ok) throw new Error('Failed to fetch header');
        html = await res.text();
      }

      // inject langPath placeholder
      html = html.replace(/{{langPath}}/g, langPath);

      // insert into DOM at the top of body
      const container = document.createElement('div');
      container.innerHTML = html;
      document.body.insertBefore(container, document.body.firstChild);

    // fetch i18n strings
    const i18nRes = await fetch('/i18n/' + lang + '.json');
    let strings = {};
    if (i18nRes.ok) {
      strings = await i18nRes.json();
    }

    // apply i18n to elements with data-i18n
    container.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (strings[key]) {
        el.textContent = strings[key];
      }
    });

    // adjust blog/podcast hrefs or hide links when content not available
    try {
      const blogEls = container.querySelectorAll('[data-i18n="nav_blog"]');
      const podcastEls = container.querySelectorAll('[data-i18n="nav_podcast"]');
      const hasBlogAnchor = !!document.querySelector('#blog');
      const hasPodcastAnchor = !!document.querySelector('#podcast');

      // Helper to set href or hide element(s)
      function applyLinkOrHide(elems, hrefKey, hasAnchor, fallbackPath) {
        elems.forEach(el => {
          // Prefer explicit URL keys like 'nav_blog_href' or 'nav_podcast_href'
          const explicitHrefKey = hrefKey + '_href';
          let explicitHref = (strings && strings[explicitHrefKey]) || null;

          // Backwards-compatible: if the base key itself contains a URL-looking value, accept it.
          if (!explicitHref && strings && typeof strings[hrefKey] === 'string') {
            const v = strings[hrefKey].trim();
            if (v.startsWith('http') || v.startsWith('/')) {
              explicitHref = v;
            }
          }

          if (explicitHref) {
            el.setAttribute('href', explicitHref);
            el.classList.remove('hidden');
            return;
          }

          // Derive anchor name from the base key, e.g. 'nav_blog' -> 'blog'
          let anchorName = hrefKey.replace(/^nav_/, '').replace(/_href$/, '');
          anchorName = anchorName.replace(/^blog_?/, 'blog').replace(/^podcast_?/, 'podcast');

          if (hasAnchor && document.querySelector('#' + anchorName)) {
            el.setAttribute('href', '#' + anchorName);
            el.classList.remove('hidden');
          } else {
            // No in-page anchor and no explicit URL: hide the link to avoid navigation issues
            el.classList.add('hidden');
          }
        });
      }

      applyLinkOrHide(blogEls, 'nav_blog', hasBlogAnchor, '/blog/' + lang + '/');
      applyLinkOrHide(podcastEls, 'nav_podcast', hasPodcastAnchor, '/podcast/' + lang + '/');
    } catch (e) {
      // non-fatal
      console.warn('header-loader: failed to adjust/hide blog/podcast links', e);
    }

    // Initialize header behaviors (hamburger, language toggles)
    function initHeader() {
      const mobileMenuButton = document.getElementById('mobile-menu-button');
      const mobileMenu = document.getElementById('mobile-menu');
      const menuLines = mobileMenuButton ? mobileMenuButton.querySelectorAll('span') : [];

      if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
          const isOpen = !mobileMenu.classList.contains('hidden');
          if (isOpen) {
            mobileMenu.classList.add('hidden');
            if (menuLines[0]) menuLines[0].style.transform = 'rotate(0deg)';
            if (menuLines[1]) menuLines[1].style.opacity = '1';
            if (menuLines[2]) menuLines[2].style.transform = 'rotate(0deg)';
          } else {
            mobileMenu.classList.remove('hidden');
            if (menuLines[0]) menuLines[0].style.transform = 'rotate(45deg) translate(3px, 3px)';
            if (menuLines[1]) menuLines[1].style.opacity = '0';
            if (menuLines[2]) menuLines[2].style.transform = 'rotate(-45deg) translate(3px, -3px)';
          }
        });

        // close on link click
        const mobileMenuLinks = mobileMenu.querySelectorAll('a');
        mobileMenuLinks.forEach(function(link) {
          link.addEventListener('click', function() {
            mobileMenu.classList.add('hidden');
            if (menuLines[0]) menuLines[0].style.transform = 'rotate(0deg)';
            if (menuLines[1]) menuLines[1].style.opacity = '1';
            if (menuLines[2]) menuLines[2].style.transform = 'rotate(0deg)';
          });
        });
      }

      // desktop language menu
      const languageButton = document.getElementById('language-button');
      const languageMenu = document.getElementById('language-menu');
      if (languageButton && languageMenu) {
        languageButton.addEventListener('click', function(e) {
          e.preventDefault();
          languageMenu.classList.toggle('hidden');
        });
        document.addEventListener('click', function(e) {
          if (!languageButton.contains(e.target) && !languageMenu.contains(e.target)) {
            languageMenu.classList.add('hidden');
          }
        });
      }

      // mobile language toggle
      const mobileLanguageButton = document.getElementById('mobile-language-button');
      const mobileLanguageMenu = document.getElementById('mobile-language-menu');
      if (mobileLanguageButton && mobileLanguageMenu) {
        mobileLanguageButton.addEventListener('click', function(e) {
          e.preventDefault();
          const expanded = mobileLanguageButton.getAttribute('aria-expanded') === 'true';
          mobileLanguageButton.setAttribute('aria-expanded', String(!expanded));
          mobileLanguageMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function(e) {
          if (!mobileLanguageButton.contains(e.target) && !mobileLanguageMenu.contains(e.target)) {
            mobileLanguageMenu.classList.add('hidden');
            mobileLanguageButton.setAttribute('aria-expanded', 'false');
          }
        });

        document.addEventListener('keydown', function(e) {
          if (e.key === 'Escape') {
            if (!mobileLanguageMenu.classList.contains('hidden')) {
              mobileLanguageMenu.classList.add('hidden');
              mobileLanguageButton.setAttribute('aria-expanded', 'false');
            }
          }
        });
      }
    }

    initHeader();

    // Smooth-scroll handling for injected header anchor links (account for fixed header height)
    (function initAnchorScrolling() {
      const headerOffset = 64; // matches CSS padding-top and anchor offset

      function scrollToHash(hash) {
        if (!hash) return;
        const id = hash.replace('#','');
        const el = document.getElementById(id);
        if (!el) return;
        const rect = el.getBoundingClientRect();
        const absoluteTop = window.pageYOffset + rect.top;
        window.scrollTo({ top: absoluteTop - headerOffset, behavior: 'smooth' });
      }

      // handle clicks on injected header links
      container.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', function(e) {
          // allow external links or different-page anchors to work
          const href = a.getAttribute('href');
          if (!href || !href.startsWith('#')) return;
          e.preventDefault();
          // close mobile menu if open
          const mobileMenu = document.getElementById('mobile-menu');
          if (mobileMenu && !mobileMenu.classList.contains('hidden')) mobileMenu.classList.add('hidden');
          scrollToHash(href);
        });
      });

      // If page loaded with a hash, adjust scroll after short delay
      if (location.hash) {
        setTimeout(() => scrollToHash(location.hash), 100);
      }
    })();

  } catch (err) {
    console.error('header-loader error', err);
  }
})();
