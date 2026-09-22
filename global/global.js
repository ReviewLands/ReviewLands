// ==================================================
// GLOBAL JS – CLEAN, SAFE, VIEWPORT-AWARE
// ==================================================
document.addEventListener("DOMContentLoaded", () => {

  window.FIC = window.FIC || {};
  window.FIC.ready = true;

  const isMobile = () => window.matchMedia("(max-width: 768px)").matches;

  // ==================================================
  // MOBILE NAV TOGGLE (MOBILE ONLY)
  // ==================================================
  const menuToggle = document.querySelector(".menu-toggle");
  const mobileNav = document.querySelector(".mobile-nav");

  const closeMobileNav = () => {
    if (!mobileNav || !menuToggle) return;
    mobileNav.classList.remove("open");
    menuToggle.classList.remove("active");
    menuToggle.setAttribute("aria-expanded", "false");
  };

  if (menuToggle && mobileNav) {

    // Toggle menu (mobile only)
    menuToggle.addEventListener("click", (e) => {
      if (!isMobile()) return;   // 🔒 DESKTOP GUARD
      e.preventDefault();

      const isOpen = mobileNav.classList.toggle("open");
      menuToggle.classList.toggle("active", isOpen);
      menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    // Close on outside click (mobile only)
    document.addEventListener("click", (e) => {
      if (!isMobile()) return;   // 🔒 DESKTOP GUARD

      const clickedInside =
        mobileNav.contains(e.target) || menuToggle.contains(e.target);

      if (!clickedInside) closeMobileNav();
    });

    // Close on ESC (mobile only)
    document.addEventListener("keydown", (e) => {
      if (!isMobile()) return;   // 🔒 DESKTOP GUARD
      if (e.key === "Escape") closeMobileNav();
    });

    // Close when clicking a link
    mobileNav.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", closeMobileNav);
    });
  }

  // ==================================================
  // MOBILE BLOG & TOOLS SUBMENUS (MOBILE ONLY)
  // ==================================================
  const blogToggle = document.querySelector(".mobile-blog-toggle");
  const blogMenu = document.querySelector(".mobile-blog-menu");

  const toolsToggle = document.querySelector(".mobile-tools-toggle");
  const toolsMenu = document.querySelector(".mobile-tools-menu");

  const closeOtherSubmenus = (except) => {
    [blogMenu, toolsMenu].forEach(menu => {
      if (menu && menu !== except) menu.classList.remove("open");
    });
  };

  if (blogToggle && blogMenu) {
    blogToggle.addEventListener("click", (e) => {
      if (!isMobile()) return;   // 🔒 DESKTOP GUARD
      e.preventDefault();

      blogMenu.classList.toggle("open");
      closeOtherSubmenus(blogMenu);
    });
  }

  if (toolsToggle && toolsMenu) {
    toolsToggle.addEventListener("click", (e) => {
      if (!isMobile()) return;   // 🔒 DESKTOP GUARD
      e.preventDefault();

      toolsMenu.classList.toggle("open");
      closeOtherSubmenus(toolsMenu);
    });
  }

  // ==================================================
  // SCROLL TO TOP
  // ==================================================
  const scrollBtn = document.querySelector(".scroll-to-top-btn");
  if (scrollBtn) {
    const onScroll = () => {
      scrollBtn.classList.toggle("show", window.scrollY > 400);
    };

    window.addEventListener("scroll", onScroll);
    onScroll();

    scrollBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // ==================================================
  // BLOG LOAD MORE (OPTIONAL)
  // ==================================================
  const loadMoreBtn = document.getElementById("loadMoreBtn");
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener("click", () => {
      loadMoreBtn.textContent = "No more articles";
      loadMoreBtn.disabled = true;
    });
  }
});


// ==================================================
// BLOG TABS (DESKTOP + MOBILE – SAFE)
// ==================================================
document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".blog-tab");
  const panels = document.querySelectorAll(".tab-panel");
  const select = document.querySelector(".blog-category-select");

  if (!panels.length) return;

  function activateCategory(key) {
    tabs.forEach(t => {
      t.classList.remove("active");
      t.setAttribute("aria-selected", "false");
    });
    panels.forEach(p => p.classList.remove("active"));

    const panel = document.querySelector(`.tab-panel[data-panel="${key}"]`);
    if (panel) panel.classList.add("active");

    const tab = document.querySelector(`.blog-tab[data-tab="${key}"]`);
    if (tab) {
      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");
    }

    if (select) select.value = key;
  }

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      activateCategory(tab.dataset.tab);
    });
  });

  if (select) {
    select.addEventListener("change", e => {
      activateCategory(e.target.value);
    });
  }

  activateCategory(
    document.querySelector(".blog-tab.active")?.dataset.tab || "heic"
  );
});
