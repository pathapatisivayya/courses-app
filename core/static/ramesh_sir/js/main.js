(function () {
    'use strict';

    // ----- Mobile nav toggle -----
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('open');
            navToggle.classList.toggle('active');
            document.body.style.overflow = navMenu.classList.contains('open') ? 'hidden' : '';
        });

        navMenu.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                navMenu.classList.remove('open');
                navToggle.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ----- Header scroll -----
    const header = document.getElementById('header');
    if (header) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                header.style.background = 'rgba(15, 15, 18, 0.98)';
            } else {
                header.style.background = 'rgba(15, 15, 18, 0.9)';
            }
        });
    }

    // ----- Smooth scroll for anchor links -----
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ----- Testimonials slider -----
    const cards = document.querySelectorAll('.testimonial-card');
    const dotsContainer = document.getElementById('testimonial-dots');

    if (cards.length && dotsContainer) {
        cards.forEach(function (_, i) {
            const dot = document.createElement('button');
            dot.className = 'testimonial-dot' + (i === 0 ? ' active' : '');
            dot.setAttribute('aria-label', 'Go to testimonial ' + (i + 1));
            dot.addEventListener('click', function () {
                setTestimonial(i);
            });
            dotsContainer.appendChild(dot);
        });

        var currentIndex = 0;
        var autoInterval;

        function setTestimonial(index) {
            currentIndex = index;
            cards.forEach(function (card, i) {
                card.classList.toggle('active', i === index);
            });
            dotsContainer.querySelectorAll('.testimonial-dot').forEach(function (dot, i) {
                dot.classList.toggle('active', i === index);
            });
        }

        function nextTestimonial() {
            currentIndex = (currentIndex + 1) % cards.length;
            setTestimonial(currentIndex);
        }

        autoInterval = setInterval(nextTestimonial, 5000);

        var slider = document.querySelector('.testimonials-slider');
        if (slider) {
            slider.addEventListener('mouseenter', function () {
                clearInterval(autoInterval);
            });
            slider.addEventListener('mouseleave', function () {
                autoInterval = setInterval(nextTestimonial, 5000);
            });
        }
    }

    // ----- Contact form: only preventDefault when NOT server-handled (no data-django-form) -----
    const contactForm = document.getElementById('contact-form');
    if (contactForm && !contactForm.hasAttribute('data-django-form')) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            var name = document.getElementById('name').value.trim();
            var email = document.getElementById('email').value.trim();
            var message = document.getElementById('message').value.trim();
            if (!name || !email || !message) {
                alert('Please fill in Name, Email, and Message.');
                return;
            }
            alert('Thank you! Your message has been sent. We will get back to you soon.');
            contactForm.reset();
        });
    }

    // ----- Highlight nav link for current section -----
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

    function updateActiveNav() {
        var scrollY = window.scrollY;
        sections.forEach(function (section) {
            var top = section.offsetTop - 100;
            var height = section.offsetHeight;
            var id = section.getAttribute('id');
            if (id && scrollY >= top && scrollY < top + height) {
                navLinks.forEach(function (link) {
                    if (link.getAttribute('href') === '#' + id) {
                        link.style.color = 'var(--color-accent)';
                    } else {
                        link.style.color = '';
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav);
    updateActiveNav();
})();
