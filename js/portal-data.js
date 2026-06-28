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
  const assetVersion = "20260620-linkfix";
  const siteBaseUrl = getSiteBaseUrl();
  const fallbackPortalData = {
    locales: {
      ja: {
        status: { open: "受付中", building: "開発中", live: "公開中" },
        properties: {
          about: { name: "BizLiv.life", verb: "知る", map_label: "灯台", map_note: "運営者を知る", audience: "まず全体像を知りたい", description: "問いに答える、設計する、記録する、使う、読む。今の状態から入口を選べる場所です。", cta: "運営者を知る" },
          coach: { name: "BizLiv Coach", verb: "問いに答える", map_label: "問いの庭", map_note: "自分を整える", audience: "自分で問いに答えながら整理したい", description: "セルフコーチングの問いに答えながら、言葉にならない悩みをほどき、次に考えることを1つに絞ります。", cta: "Coachへ" },
          design: { name: "BizLiv Design", verb: "設計する", map_label: "設計の広場", map_note: "次を設計", audience: "進み方を決めて動き出したい", description: "仕事・暮らし・AI活用を整理し、今日から試せる小さな計画にします。", cta: "Designへ" },
          emosnap: { name: "EmoSnap", verb: "記録する", map_label: "感情の観測所", map_note: "感情を残す", audience: "気分の変化をあとから振り返りたい", description: "その時の感情をすぐ残し、自分の調子や変化に気づきやすくします。", cta: "EmoSnapへ" },
          apps: { name: "BizLiv Apps", verb: "使う", map_label: "道具小屋", map_note: "日々に使う", audience: "日々の小さな手間を減らしたい", description: "会議、買い物、帰宅、記録など、毎日の面倒を軽くする道具を使えます。", cta: "Appsへ" },
          media: { name: "BizLiv Media", verb: "読む・聴く", map_label: "発信の書斎", map_note: "読む・聴く", audience: "考え方や試行錯誤を読みたい", description: "コーチング、AI、開発、日常の問いを、記事や音声で追えます。", cta: "Mediaへ" }
        },
        funnel: [
          { id: "design", title: "次にやることを決めたい", text: "頭の中にある不安や選択肢を整理し、今日から動ける小さな計画にする。", cta: "BizLiv Designへ" },
          { id: "coach", title: "問いに答えて整理したい", text: "セルフコーチングの問いに答えながら、まだ言葉にならない悩みを整理し、次に考えることを1つに絞る。", cta: "BizLiv Coachへ" },
          { id: "apps", title: "道具を使って軽くしたい", text: "会議、買い物、帰宅、記録など、日々の小さな手間を道具で軽くする。", cta: "BizLiv Appsへ" }
        ]
      },
      en: {
        status: { open: "Open", building: "Building", live: "Live" },
        properties: {
          about: { name: "BizLiv.life", verb: "Know", map_label: "Lighthouse", map_note: "About the operator", audience: "I want the whole picture first", description: "A place to choose between self-coaching prompts, designing, recording, using tools, and reading.", cta: "Meet the operator" },
          coach: { name: "BizLiv Coach", verb: "Answer prompts", map_label: "Question Garden", map_note: "Self-coaching", audience: "I want to sort my thoughts on my own", description: "Use self-coaching prompts to untangle unnamed concerns and narrow what to think about next.", cta: "Go to Coach" },
          design: { name: "BizLiv Design", verb: "Design", map_label: "Design Plaza", map_note: "Design the next step", audience: "I want to decide how to move", description: "Organize work, life, and AI use into a small plan you can try today.", cta: "Go to Design" },
          emosnap: { name: "EmoSnap", verb: "Record", map_label: "Emotion Observatory", map_note: "Record emotion", audience: "I want to look back on mood changes", description: "Record feelings quickly so you can notice your own patterns and changes later.", cta: "Go to EmoSnap" },
          apps: { name: "BizLiv Apps", verb: "Use", map_label: "Tool Workshop", map_note: "Use in daily life", audience: "I want to reduce small daily friction", description: "Use simple tools for meetings, shopping, getting home, and daily records.", cta: "Go to Apps" },
          media: { name: "BizLiv Media", verb: "Read / Listen", map_label: "Media Library", map_note: "Read and listen", audience: "I want to read the thinking behind it", description: "Follow essays and audio about coaching, AI, development, and everyday questions.", cta: "Go to Media" }
        },
        funnel: [
          { id: "design", title: "Decide what to do next", text: "Sort through worries and options, then make a small plan you can try today.", cta: "Go to BizLiv Design" },
          { id: "coach", title: "Use self-coaching prompts", text: "Answer prompts to organize unnamed concerns and narrow what to think about next.", cta: "Go to BizLiv Coach" },
          { id: "apps", title: "Use tools to lighten daily life", text: "Reduce small daily tasks with tools for meetings, shopping, getting home, and records.", cta: "Go to BizLiv Apps" }
        ]
      },
      zhhans: {
        status: { open: "开放中", building: "开发中", live: "公开中" },
        properties: {
          about: { name: "BizLiv.life", verb: "了解", map_label: "灯塔", map_note: "了解运营者", audience: "先想了解整体", description: "可以从自我提问、设计、记录、使用、阅读中选择入口的地方。", cta: "了解运营者" },
          coach: { name: "BizLiv Coach", verb: "自我提问", map_label: "提问之庭", map_note: "自我教练", audience: "想用提问整理自己的想法", description: "通过自我教练的提问，整理还没命名的烦恼，缩小下一步要思考的事。", cta: "去 Coach" },
          design: { name: "BizLiv Design", verb: "设计", map_label: "设计广场", map_note: "设计下一步", audience: "想决定接下来怎么动", description: "整理工作、生活和 AI 使用，变成今天就能尝试的小计划。", cta: "去 Design" },
          emosnap: { name: "EmoSnap", verb: "记录", map_label: "情绪观测所", map_note: "记录情绪", audience: "想回看自己的情绪变化", description: "快速留下当下的情绪，之后更容易发现自己的节奏和变化。", cta: "去 EmoSnap" },
          apps: { name: "BizLiv Apps", verb: "使用", map_label: "工具小屋", map_note: "日常使用", audience: "想减轻日常小麻烦", description: "使用会议、购物、回家、记录等小工具，减轻每天的麻烦。", cta: "去 Apps" },
          media: { name: "BizLiv Media", verb: "读・听", map_label: "发布书房", map_note: "读・听", audience: "想阅读背后的想法", description: "通过文章和音声追踪教练、AI、开发和日常问题。", cta: "去 Media" }
        },
        funnel: [
          { id: "design", title: "想决定下一步做什么", text: "整理不安和选项，变成今天就能尝试的小计划。", cta: "去 BizLiv Design" },
          { id: "coach", title: "想用提问整理自己", text: "通过自我教练的提问，整理还没命名的烦恼，缩小下一步要思考的事。", cta: "去 BizLiv Coach" },
          { id: "apps", title: "想用工具减轻日常", text: "用会议、购物、回家、记录等工具，减轻每天的小麻烦。", cta: "去 BizLiv Apps" }
        ]
      },
      zhhant: {
        status: { open: "開放中", building: "開發中", live: "公開中" },
        properties: {
          about: { name: "BizLiv.life", verb: "了解", map_label: "燈塔", map_note: "了解營運者", audience: "先想了解整體", description: "可以從自我提問、設計、記錄、使用、閱讀中選擇入口的地方。", cta: "了解營運者" },
          coach: { name: "BizLiv Coach", verb: "自我提問", map_label: "提問之庭", map_note: "自我教練", audience: "想用提問整理自己的想法", description: "透過自我教練的提問，整理還沒命名的煩惱，縮小下一步要思考的事。", cta: "去 Coach" },
          design: { name: "BizLiv Design", verb: "設計", map_label: "設計廣場", map_note: "設計下一步", audience: "想決定接下來怎麼動", description: "整理工作、生活和 AI 使用，變成今天就能嘗試的小計畫。", cta: "去 Design" },
          emosnap: { name: "EmoSnap", verb: "記錄", map_label: "情緒觀測所", map_note: "記錄情緒", audience: "想回看自己的情緒變化", description: "快速留下當下的情緒，之後更容易發現自己的節奏和變化。", cta: "去 EmoSnap" },
          apps: { name: "BizLiv Apps", verb: "使用", map_label: "工具小屋", map_note: "日常使用", audience: "想減輕日常小麻煩", description: "使用會議、購物、回家、記錄等小工具，減輕每天的麻煩。", cta: "去 Apps" },
          media: { name: "BizLiv Media", verb: "讀・聽", map_label: "發布書房", map_note: "讀・聽", audience: "想閱讀背後的想法", description: "透過文章和音聲追蹤教練、AI、開發和日常問題。", cta: "去 Media" }
        },
        funnel: [
          { id: "design", title: "想決定下一步做什麼", text: "整理不安和選項，變成今天就能嘗試的小計畫。", cta: "去 BizLiv Design" },
          { id: "coach", title: "想用提問整理自己", text: "透過自我教練的提問，整理還沒命名的煩惱，縮小下一步要思考的事。", cta: "去 BizLiv Coach" },
          { id: "apps", title: "想用工具減輕日常", text: "用會議、購物、回家、記錄等工具，減輕每天的小麻煩。", cta: "去 BizLiv Apps" }
        ]
      }
    },
    properties: [
      { id: "about", zone: "lighthouse", x: 19, y: 30, href: { ja: "/ja/about/", en: "/en/about/", zhhans: "/zhhans/about/", zhhant: "/zhhant/about/" }, status: "open", accent: "#e3a72f", show_in_map: true, show_in_properties: false },
      { id: "coach", zone: "garden", x: 43, y: 34, href: "https://coach.bizliv.life/", status: "open", accent: "#607d58", show_in_map: true, show_in_properties: true },
      { id: "design", zone: "studio", x: 20, y: 79, href: "https://design.bizliv.life/", status: "open", accent: "#e3a72f", show_in_map: true, show_in_properties: true },
      { id: "emosnap", zone: "observatory", x: 69, y: 25, href: { ja: "https://www.emosnap.com/", en: "https://www.emosnap.com/en/", zhhans: "https://www.emosnap.com/zh-cn/", zhhant: "https://www.emosnap.com/zh-tw/" }, status: "building", accent: "#2f6f91", show_in_map: true, show_in_properties: true },
      { id: "apps", zone: "workshop", x: 48, y: 57, href: { ja: "https://apps.bizliv.life/ja/", en: "https://apps.bizliv.life/en/", zhhans: "https://apps.bizliv.life/zhhans/", zhhant: "https://apps.bizliv.life/zhhant/" }, status: "live", accent: "#b46a4a", show_in_map: true, show_in_properties: true },
      { id: "media", zone: "library", x: 81, y: 47, href: { ja: "https://media.bizliv.life/", en: "https://media.bizliv.life/en/", zhhans: "https://media.bizliv.life/zh-cn/", zhhant: "https://media.bizliv.life/zh-tw/" }, status: "live", accent: "#78664b", show_in_map: true, show_in_properties: true }
    ]
  };

  function getSiteBaseUrl() {
    if (window.location.protocol !== "file:") {
      return "";
    }

    const stylesheet = document.querySelector('link[rel="stylesheet"][href*="css/site.css"]');
    if (stylesheet) {
      const stylesheetUrl = new URL(stylesheet.getAttribute("href"), window.location.href);
      return stylesheetUrl.href.replace(/css\/site\.css.*$/, "");
    }

    return "";
  }

  function isExternal(href) {
    return /^https?:\/\//.test(href);
  }

  function resolveSitePath(path) {
    if (!path || !path.startsWith("/") || path.startsWith("//") || !siteBaseUrl) {
      return path;
    }

    return new URL(path.slice(1), siteBaseUrl).href;
  }

  function resolveHref(href) {
    if (!href || typeof href === "string") {
      return href || "#";
    }
    return href[activeLocale] || href.ja || Object.values(href)[0] || "#";
  }

  function enhanceLink(anchor, href) {
    const resolved = resolveSitePath(resolveHref(href));
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

  function renderPortal(data) {
    const translations = data.locales[activeLocale] || data.locales.ja;
    const properties = mergeProperties(data, translations);

    renderMapPins(properties);
    renderProperties(properties, translations.status || {});
    renderFunnel(translations.funnel || [], properties);
  }

  async function initPortal() {
    const response = await fetch(resolveSitePath(`/data/portal.json?v=${assetVersion}`), { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`Portal data request failed: ${response.status}`);
    }
    renderPortal(await response.json());
  }

  document.addEventListener("DOMContentLoaded", () => {
    initPortal().catch((error) => {
      document.documentElement.classList.add("portal-data-error");
      console.error(error);
      renderPortal(fallbackPortalData);
    });
  });
})();
