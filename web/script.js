/* ============================================
   HATCHBACK — Vaporwave Arcade Interactions
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // --- Star Canvas Background ---
    const canvas = document.getElementById('star-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let stars = [];
        const STAR_COUNT = 150;

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        function createStars() {
            stars = [];
            for (let i = 0; i < STAR_COUNT; i++) {
                stars.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    radius: Math.random() * 1.5 + 0.3,
                    alpha: Math.random(),
                    speed: Math.random() * 0.5 + 0.1,
                    hue: Math.random() > 0.5 ? 300 : 180 // pink or cyan
                });
            }
        }

        function drawStars() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            stars.forEach(s => {
                s.alpha += Math.sin(Date.now() * 0.001 * s.speed) * 0.008;
                s.alpha = Math.max(0.1, Math.min(1, s.alpha));
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${s.hue}, 100%, 70%, ${s.alpha})`;
                ctx.fill();
            });
            requestAnimationFrame(drawStars);
        }

        resizeCanvas();
        createStars();
        drawStars();
        window.addEventListener('resize', () => {
            resizeCanvas();
            createStars();
        });
    }


    // --- Navbar Scroll Effect ---
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }


    // --- Mobile Nav Toggle ---
    const toggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (toggle && navLinks) {
        toggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            const spans = toggle.querySelectorAll('span');
            if (navLinks.classList.contains('open')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            }
        });

        // Close nav on link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                const spans = toggle.querySelectorAll('span');
                spans[0].style.transform = '';
                spans[1].style.opacity = '';
                spans[2].style.transform = '';
            });
        });
    }


    // --- Copy Install Command ---
    const installBox = document.querySelector('.install-box');
    if (installBox) {
        installBox.addEventListener('click', () => {
            const cmd = 'pip install hatchback';
            navigator.clipboard.writeText(cmd).then(() => {
                const tooltip = installBox.querySelector('.copied-tooltip');
                if (tooltip) {
                    tooltip.classList.add('show');
                    setTimeout(() => tooltip.classList.remove('show'), 1500);
                }
            });
        });
    }


    // --- Scroll Reveal (Intersection Observer) ---
    const revealElements = document.querySelectorAll('.reveal');
    if (revealElements.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealElements.forEach(el => observer.observe(el));
    }


    // --- Smooth Scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // --- Donate Modal ---
    const donateBtn = document.getElementById('donate-btn');
    const donateModal = document.getElementById('donate-modal');
    const modalClose = document.getElementById('modal-close');
    const copyBtcBtn = document.getElementById('copy-btc');

    if (donateBtn && donateModal && modalClose) {
        // Open from nav button and any .donate-trigger links
        const allDonateTriggers = [donateBtn, ...document.querySelectorAll('.donate-trigger')];
        allDonateTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                donateModal.classList.add('active');

                // Close mobile menu if open
                const mobileLnk = document.querySelector('.nav-links');
                const mobileTogg = document.querySelector('.mobile-toggle');

                if (mobileLnk && mobileLnk.classList.contains('open')) {
                    mobileLnk.classList.remove('open');
                    if (mobileTogg) {
                        const sp = mobileTogg.querySelectorAll('span');
                        if (sp.length === 3) {
                            sp[0].style.transform = '';
                            sp[1].style.opacity = '';
                            sp[2].style.transform = '';
                        }
                    }
                }
            });
        });

        // Close functions
        const closeModal = () => donateModal.classList.remove('active');
        
        modalClose.addEventListener('click', closeModal);
        
        donateModal.addEventListener('click', (e) => {
            if (e.target === donateModal) closeModal();
        });

        // Generic escape key close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && donateModal.classList.contains('active')) {
                closeModal();
            }
        });
    }

    // --- Copy BTC Address ---
    if (copyBtcBtn) {
        copyBtcBtn.addEventListener('click', () => {
            const btcAddr = document.getElementById('btc-address').textContent;
            navigator.clipboard.writeText(btcAddr).then(() => {
                const tooltip = document.getElementById('btc-tooltip');
                tooltip.classList.add('visible');
                setTimeout(() => tooltip.classList.remove('visible'), 2000);
            });
        });
    }

});

