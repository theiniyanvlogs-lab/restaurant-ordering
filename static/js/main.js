// ======================================================
// Restaurant Ordering System
// main.js
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    initializeApp();

});

// ======================================================
// INITIALIZE
// ======================================================

function initializeApp() {

    stickyHeader();

    createBackToTopButton();

    revealOnScroll();

    highlightActiveNavigation();

    buttonRippleEffect();

    lazyLoadImages();

    keyboardShortcuts();

    updateFooterYear();

    pageLoader();

}

// ======================================================
// STICKY HEADER
// ======================================================

function stickyHeader() {

    const header = document.querySelector("header");

    if (!header) return;

    window.addEventListener("scroll", () => {

        if (window.scrollY > 20) {

            header.classList.add("header-shadow");

        } else {

            header.classList.remove("header-shadow");

        }

    });

}

// ======================================================
// BACK TO TOP BUTTON
// ======================================================

function createBackToTopButton() {

    const button = document.createElement("button");

    button.className = "back-top";

    button.innerHTML = "⬆";

    document.body.appendChild(button);

    window.addEventListener("scroll", () => {

        if (window.scrollY > 400) {

            button.classList.add("show");

        } else {

            button.classList.remove("show");

        }

    });

    button.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}

// ======================================================
// REVEAL ANIMATION
// ======================================================

function revealOnScroll() {

    const elements = document.querySelectorAll(

        ".food-card,.cart-item,.checkout-box,.order-summary,.success-box"

    );

    if (!("IntersectionObserver" in window)) return;

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("fade-in");

            }

        });

    }, {

        threshold: 0.15

    });

    elements.forEach(element => observer.observe(element));

}

// ======================================================
// ACTIVE NAVIGATION
// ======================================================

function highlightActiveNavigation() {

    const current = window.location.pathname;

    document.querySelectorAll("nav a").forEach(link => {

        if (link.getAttribute("href") === current) {

            link.classList.add("active");

        }

    });

}

// ======================================================
// RIPPLE EFFECT
// ======================================================

function buttonRippleEffect() {

    document.querySelectorAll("button").forEach(button => {

        button.addEventListener("click", function(e) {

            const ripple = document.createElement("span");

            ripple.className = "ripple";

            const rect = this.getBoundingClientRect();

            ripple.style.left =

                (e.clientX - rect.left) + "px";

            ripple.style.top =

                (e.clientY - rect.top) + "px";

            this.appendChild(ripple);

            setTimeout(() => {

                ripple.remove();

            }, 600);

        });

    });

}

// ======================================================
// LAZY LOAD IMAGES
// ======================================================

function lazyLoadImages() {

    const images = document.querySelectorAll("img[data-src]");

    if (!images.length) return;

    if (!("IntersectionObserver" in window)) {

        images.forEach(img => {

            img.src = img.dataset.src;

        });

        return;

    }

    const observer = new IntersectionObserver((entries, obs) => {

        entries.forEach(entry => {

            if (!entry.isIntersecting) return;

            const img = entry.target;

            img.src = img.dataset.src;

            img.removeAttribute("data-src");

            obs.unobserve(img);

        });

    });

    images.forEach(img => observer.observe(img));

}

// ======================================================
// KEYBOARD SHORTCUTS
// ======================================================

function keyboardShortcuts() {

    document.addEventListener("keydown", function(e) {

        if (e.ctrlKey && e.key.toLowerCase() === "h") {

            e.preventDefault();

            location.href = "/";

        }

        if (e.ctrlKey && e.key.toLowerCase() === "m") {

            e.preventDefault();

            location.href = "/menu";

        }

        if (e.ctrlKey && e.key.toLowerCase() === "c") {

            e.preventDefault();

            location.href = "/cart";

        }

        if (e.ctrlKey && e.key.toLowerCase() === "k") {

            e.preventDefault();

            location.href = "/checkout";

        }

    });

}

// ======================================================
// FOOTER YEAR
// ======================================================

function updateFooterYear() {

    const year = document.getElementById("currentYear");

    if (year) {

        year.textContent = new Date().getFullYear();

    }

}

// ======================================================
// PAGE LOADER
// ======================================================

function pageLoader() {

    const loader = document.getElementById("loader");

    if (!loader) return;

    window.addEventListener("load", () => {

        loader.style.opacity = "0";

        setTimeout(() => {

            loader.remove();

        }, 400);

    });

}