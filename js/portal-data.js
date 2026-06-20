(function () {
  const localeAliases = {
    "zh-hans": "zhhans",
    "zh-hant": "zhhant",
    "zh-cn": "zhhans",
    "zh-tw": "zhhant",
    "zh-hk": "zhhant"
  };

  const rawLocale = (document.documentElement.lang || "ja").toLowerCase();
  const locale = localeAliases[rawLocale] || rawLocale.replace("-", "");
  const supportedLocales = ["ja", "en", "zhhans", "zhhant"];
  const activeLocale = supportedLocales.includes(locale) ? locale : "ja";
  const assetVersion = "20260620-cardfix2";

  function isExternal(href) {
    return /^https?:\/\//.test(href);
  }

  function resolveHref(href) {
    if (!href || typeof href === "string") {
      return href || "#";
    }
    return href[activeLocale] || href.ja || Object.values(href)[0] || "#";
  }

  function enhanceLink(anchor, href) {
    const resolved = resolveHref(href);
    anchor.href = resolved;
    if (isExternal(resolved)) {
      anchor.target = "_blank";
      anchor.rel = "noopener noreferrer";
    }
  }

  function escapeText(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function mergeProperties(data, translations) {
    const localized = translations.properties || {};
    return (data.properties || []).map((property) => ({
      ...property,
      ...localized[property.id],
      href: resolveHref(property.href)
    }));
  }

  function renderMapPins(properties) {
    const mount = document.querySelector("[data-portal-map-pins]");
    if (!mount) return;

    mount.innerHTML = "";
    properties.filter((property) => property.show_in_map !== false).forEach((property) => {
      const pin = document.createElement("a");
      pin.className = `map-pin map-pin-${property.id}`;
      pin.style.left = `${property.x}%`;
      pin.style.top = `${property.y}%`;
      pin.style.setProperty("--pin-accent", property.accent);
      pin.setAttribute("data-zone", property.zone);
      pin.innerHTML = `
        ${escapeText(property.map_label)}
        <small>${escapeText(property.map_note)}</small>
      `;
      enhanceLink(pin, property.href);
      mount.appendChild(pin);
    });
  }

  function renderProperties(properties, statusLabels) {
    const mount = document.querySelector("[data-portal-properties]");
    if (!mount) return;

    mount.innerHTML = "";
    properties.filter((property) => property.show_in_properties).forEach((property) => {
      const article = document.createElement("article");
      article.className = "portal-property-card";
      article.style.setProperty("--property-accent", property.accent);
      article.setAttribute("data-zone", property.zone);
      article.innerHTML = `
        <div class="property-meta">
          <span class="property-verb">${escapeText(property.verb)}</span>
          <span>${escapeText(statusLabels[property.status] || property.status)}</span>
        </div>
        <h3>${escapeText(property.name)}</h3>
        <p class="property-audience">${escapeText(property.audience)}</p>
        <p>${escapeText(property.description)}</p>
      `;
      const link = document.createElement("a");
      link.textContent = property.cta;
      enhanceLink(link, property.href);
      article.appendChild(link);
      mount.appendChild(article);
    });
  }

  function renderFunnel(items, properties) {
    const mount = document.querySelector("[data-portal-funnel]");
    if (!mount) return;

    const byId = new Map(properties.map((property) => [property.id, property]));
    mount.innerHTML = "";
    items.forEach((item) => {
      const property = byId.get(item.id) || {};
      const article = document.createElement("article");
      article.className = "portal-funnel-card";
      article.style.setProperty("--property-accent", property.accent || "#e3a72f");
      article.innerHTML = `
        <span>${escapeText(property.verb || "")}</span>
        <h3>${escapeText(item.title)}</h3>
        <p>${escapeText(item.text)}</p>
      `;
      const link = document.createElement("a");
      link.textContent = item.cta;
      enhanceLink(link, property.href || "#properties");
      article.appendChild(link);
      mount.appendChild(article);
    });
  }

  async function initPortal() {
    const response = await fetch(`/data/portal.json?v=${assetVersion}`, { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`Portal data request failed: ${response.status}`);
    }
    const data = await response.json();
    const translations = data.locales[activeLocale] || data.locales.ja;
    const properties = mergeProperties(data, translations);

    renderMapPins(properties);
    renderProperties(properties, translations.status || {});
    renderFunnel(translations.funnel || [], properties);
  }

  document.addEventListener("DOMContentLoaded", () => {
    initPortal().catch((error) => {
      document.documentElement.classList.add("portal-data-error");
      console.error(error);
    });
  });
})();
