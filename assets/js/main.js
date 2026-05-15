const revealItems = document.querySelectorAll(".reveal-up");

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

document.querySelector(".footer-copy").textContent = `© ${new Date().getFullYear()} Hrusheekesh Neje.`;

if (menuToggle && mobileMenu) {
  const setMenuState = (open) => {
    menuToggle.classList.toggle("is-open", open);
    mobileMenu.classList.toggle("is-open", open);
    menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
    mobileMenu.setAttribute("aria-hidden", open ? "false" : "true");
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
}
