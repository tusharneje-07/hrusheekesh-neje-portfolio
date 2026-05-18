const revealItems = document.querySelectorAll(".reveal-up");
const themeToggles = document.querySelectorAll("[data-theme-toggle]");
const THEME_STORAGE_KEY = "hrushee-theme";

const applyTheme = (theme) => {
  const isDark = theme === "dark";
  document.body.setAttribute("data-theme", isDark ? "dark" : "light");

  themeToggles.forEach((toggle) => {
    toggle.classList.toggle("is-active", isDark);
    toggle.setAttribute("aria-pressed", isDark ? "true" : "false");
    toggle.setAttribute("aria-label", isDark ? "Switch to light theme" : "Switch to dark theme");
  });
};

const getInitialTheme = () => {
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  if (storedTheme === "dark" || storedTheme === "light") {
    return storedTheme;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
};

applyTheme(getInitialTheme());

if (themeToggles.length > 0) {
  themeToggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const currentTheme = document.body.getAttribute("data-theme") === "dark" ? "dark" : "light";
      const nextTheme = currentTheme === "dark" ? "light" : "dark";
      applyTheme(nextTheme);
      localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
    });
  });
}

if (revealItems.length > 0) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: "0px 0px -60px 0px"
    }
  );

  revealItems.forEach((item) => observer.observe(item));
}

const menuToggle = document.querySelector("[data-menu-toggle]");
const mobileMenu = document.querySelector("[data-mobile-menu]");

const footerCopy = document.querySelector(".footer-copy");
if (footerCopy) {
  footerCopy.textContent = `© ${new Date().getFullYear()} Hrusheekesh Neje.`;
}

if (menuToggle && mobileMenu) {
  const menuLinks = mobileMenu.querySelectorAll("a");

  const setMenuState = (open) => {
    menuToggle.classList.toggle("is-open", open);
    mobileMenu.classList.toggle("is-open", open);
    menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
    mobileMenu.setAttribute("aria-hidden", open ? "false" : "true");
    document.body.classList.toggle("menu-open", open);
  };

  menuToggle.addEventListener("click", () => {
    const isOpen = mobileMenu.classList.contains("is-open");
    setMenuState(!isOpen);
  });

  mobileMenu.addEventListener("click", (event) => {
    if (event.target === mobileMenu) {
      setMenuState(false);
    }
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setMenuState(false);
    }
  });

  menuLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      const href = link.getAttribute("href") || "";

      if (href.startsWith("#") && href.length > 1) {
        event.preventDefault();
        const target = document.querySelector(href);
        setMenuState(false);
        if (target) {
          setTimeout(() => {
            target.scrollIntoView({ behavior: "smooth", block: "start" });
          }, 220);
        }
        return;
      }

      setMenuState(false);
    });
  });
}
