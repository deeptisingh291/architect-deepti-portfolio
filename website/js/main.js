/**
 * ARCHITECTURAL PORTFOLIO SCRIPT
 * Architect: Ar. Deepti Singh (B.Arch CSVTU Bhilai)
 * Pure Vanilla JavaScript - Blazing fast, zero runtime dependencies
 */

(function () {
  'use strict';

  // Global state
  let portfolioData = null;
  let activeFilter = 'all';
  let activeProject = null;

  // Embedded data fallback to ensure 100% functionality even on file:// protocol
  const fallbackData = {
    stats: [
      { value: "12+", label: "Years Experience (Since 2013)" },
      { value: "50+", label: "Projects Designed" },
      { value: "100%", label: "Render to Real Fidelity" },
      { value: "6+", label: "Cities in C.G. & M.P." }
    ],
    render_to_real: {
      items: [
        {
          id: "r2r-facade",
          title: "Modern Contemporary Villa - Exterior Facade",
          render_img: "assets/render_to_real/render_facade_final.jpg",
          real_img: "assets/render_to_real/real_facade_built.jpg",
          description: "Exact execution of cantilevered terrace volumes, boundary wall ambient lights, and minimalist cream-stucco facade."
        },
        {
          id: "r2r-entrance",
          title: "Grand Entrance Foyer & Teak Wood Double Doors",
          render_img: "assets/render_to_real/entrance_render_vs_real.jpg",
          real_img: "assets/render_to_real/entrance_render_vs_real.jpg",
          description: "Direct 1:1 translation from 3D visualization to handcrafted solid teak wood door with brass accents and Italian marble steps."
        },
        {
          id: "r2r-structure",
          title: "Structural RCC Framework to Final Villa",
          render_img: "assets/render_to_real/villa_render_front.jpg",
          real_img: "assets/render_to_real/site_construction_view1.jpg",
          description: "From concrete shuttering and cantilever reinforcement casting to the finished contemporary duplex home."
        }
      ]
    }
  };

  // Initialize on DOM ready
  document.addEventListener('DOMContentLoaded', () => {
    initApp();
  });

  async function initApp() {
    initThemeToggle();
    initCadCursor();
    setupNavbar();
    setupMobileMenu();
    setupContactForm();
    await loadPortfolioData();
    initComparisonSlider();
    initProjectsGrid();
    initBlueprintTabs();
    initLightbox();
    initAOS();
  }

  // Load projects data (fetch with graceful fallback)
  async function loadPortfolioData() {
    try {
      const response = await fetch('data/projects.json');
      if (!response.ok) throw new Error('Network response not ok');
      portfolioData = await response.json();
    } catch (e) {
      console.warn('Fetch failed (likely file:// protocol). Using embedded dataset.', e);
      // If fetched fails, try reading from window.__PORTFOLIO_DATA__ or use fallback
      portfolioData = window.__PORTFOLIO_DATA__ || fallbackData;
    }

    if (portfolioData && portfolioData.architect && portfolioData.architect.avatar) {
      const aboutImg = document.querySelector('#about img');
      if (aboutImg) {
        aboutImg.src = portfolioData.architect.avatar;
      }
    }
  }

  // Sticky navbar with blur and scroll spy
  function setupNavbar() {
    const navbar = document.getElementById('navbar');
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
      const scrollY = window.pageYOffset;
      if (scrollY > 40) {
        navbar.classList.add('nav-scrolled');
      } else {
        navbar.classList.remove('nav-scrolled');
      }

      // Scroll spy
      sections.forEach(current => {
        const sectionHeight = current.offsetHeight;
        const sectionTop = current.offsetTop - 120;
        const sectionId = current.getAttribute('id');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          navLinks.forEach(link => {
            link.classList.remove('text-[#c5a880]', 'border-b', 'border-[#c5a880]');
            if (link.getAttribute('href') === `#${sectionId}`) {
              link.classList.add('text-[#c5a880]', 'border-b', 'border-[#c5a880]');
            }
          });
        }
      });
    });
  }

  // Mobile menu drawer
  function setupMobileMenu() {
    const toggleBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeBtn = document.getElementById('mobile-menu-close');
    const mobileLinks = document.querySelectorAll('.mobile-nav-link');

    if (!toggleBtn || !mobileMenu) return;

    toggleBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
      });
    }

    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
      });
    });
  }

  // ==========================================================================
  // RENDER TO REAL INTERACTIVE COMPARISON SLIDER
  // ==========================================================================
  function initComparisonSlider() {
    const container = document.getElementById('comparison-slider-box');
    const overlay = document.getElementById('comparison-overlay-img');
    const handle = document.getElementById('comparison-handle');
    const rangeInput = document.getElementById('comparison-range');
    const selectorButtons = document.querySelectorAll('.r2r-select-btn');

    if (!container || !overlay || !handle) return;

    let isDragging = false;

    function setPosition(xPercent) {
      // Clamp between 2% and 98%
      const clamped = Math.max(2, Math.min(98, xPercent));
      overlay.style.width = `${clamped}%`;
      handle.style.left = `${clamped}%`;
      if (rangeInput) rangeInput.value = clamped;
    }

    function onPointerMove(e) {
      if (!isDragging) return;
      const rect = container.getBoundingClientRect();
      const clientX = e.clientX || (e.touches && e.touches[0].clientX);
      if (clientX === undefined) return;
      const xPos = clientX - rect.left;
      const percent = (xPos / rect.width) * 100;
      setPosition(percent);
    }

    // Mouse events
    container.addEventListener('mousedown', (e) => {
      isDragging = true;
      onPointerMove(e);
    });
    window.addEventListener('mouseup', () => { isDragging = false; });
    window.addEventListener('mousemove', onPointerMove);

    // Touch events for mobile/tablet
    container.addEventListener('touchstart', (e) => {
      isDragging = true;
      onPointerMove(e);
    }, { passive: true });
    window.addEventListener('touchend', () => { isDragging = false; });
    window.addEventListener('touchmove', onPointerMove, { passive: true });

    // Range input fallback for accessibility
    if (rangeInput) {
      rangeInput.addEventListener('input', (e) => {
        setPosition(e.target.value);
      });
    }

    // Switch comparison pairs
    selectorButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        selectorButtons.forEach(b => b.classList.remove('bg-[#c5a880]', 'text-[#0a0a0c]', 'border-[#c5a880]'));
        selectorButtons.forEach(b => b.classList.add('bg-[#1a1a20]', 'text-[#a1a1aa]'));

        btn.classList.add('bg-[#c5a880]', 'text-[#0a0a0c]', 'border-[#c5a880]');
        btn.classList.remove('bg-[#1a1a20]', 'text-[#a1a1aa]');

        const renderSrc = btn.getAttribute('data-render');
        const realSrc = btn.getAttribute('data-real');
        const title = btn.getAttribute('data-title');
        const desc = btn.getAttribute('data-desc');

        const underlayImg = document.getElementById('comparison-underlay-img');
        const overlayImgElem = overlay.querySelector('img');
        const titleElem = document.getElementById('r2r-active-title');
        const descElem = document.getElementById('r2r-active-desc');

        if (underlayImg) underlayImg.src = realSrc;
        if (overlayImgElem) overlayImgElem.src = renderSrc;
        if (titleElem) titleElem.textContent = title;
        if (descElem) descElem.textContent = desc;

        // Reset to center
        setPosition(50);
      });
    });
  }

  // ==========================================================================
  // PROJECTS GRID & FILTERING
  // ==========================================================================
  function initProjectsGrid() {
    const grid = document.getElementById('projects-grid');
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (!grid || !portfolioData || !portfolioData.projects) return;

    renderProjects(portfolioData.projects);

    filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        filterButtons.forEach(b => {
          b.classList.remove('active', 'bg-[#c5a880]', 'text-[#0a0a0c]');
          b.classList.add('text-[#a1a1aa]', 'bg-[#16161a]');
        });

        btn.classList.add('active', 'bg-[#c5a880]', 'text-[#0a0a0c]');
        btn.classList.remove('text-[#a1a1aa]', 'bg-[#16161a]');

        activeFilter = btn.getAttribute('data-filter');

        if (activeFilter === 'all') {
          renderProjects(portfolioData.projects);
        } else {
          const filtered = portfolioData.projects.filter(p => p.category === activeFilter);
          renderProjects(filtered);
        }
      });
    });
  }

  function renderProjects(projectsList) {
    const grid = document.getElementById('projects-grid');
    if (!grid) return;

    grid.innerHTML = '';

    projectsList.forEach(project => {
      const card = document.createElement('div');
      card.className = 'arch-card group bg-[#121216] border border-white/10 rounded-xl overflow-hidden flex flex-col cursor-pointer transition-all duration-300';
      card.setAttribute('data-id', project.id);

      card.innerHTML = `
        <div class="relative overflow-hidden aspect-[4/3] bg-black">
          <img src="${project.image}" alt="${project.title}" loading="lazy" class="card-img w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-all duration-500">
          <div class="absolute inset-0 bg-gradient-to-t from-[#121216] via-transparent to-transparent opacity-80"></div>
          <div class="absolute top-4 left-4 flex gap-2">
            <span class="cad-dim-badge">${project.category_label || project.category}</span>
          </div>
          <div class="absolute top-4 right-4 bg-black/60 backdrop-blur-md px-2.5 py-1 rounded text-[11px] font-mono text-[#c5a880] border border-[#c5a880]/30 flex items-center gap-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path></svg>
            ${project.location}
          </div>
        </div>
        <div class="p-6 flex-1 flex flex-col justify-between">
          <div>
            <div class="text-xs font-mono text-[#c5a880] uppercase tracking-wider mb-1">${project.client || 'Architectural Project'}</div>
            <h3 class="font-display font-bold text-xl text-white group-hover:text-[#c5a880] transition-colors line-clamp-1 mb-2">${project.title}</h3>
            <p class="text-sm text-zinc-400 line-clamp-2 mb-4">${project.tagline || project.description}</p>
          </div>
          <div class="pt-4 border-t border-white/5 flex items-center justify-between">
            <span class="text-xs font-mono text-zinc-500">${project.gallery ? project.gallery.length + ' Perspectives' : 'View Plan'}</span>
            <div class="flex items-center gap-1.5 text-xs font-semibold text-[#c5a880] group-hover:translate-x-1 transition-transform">
              Explore Blueprint & Case
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </div>
          </div>
        </div>
      `;

      card.addEventListener('click', () => {
        openProjectModal(project);
      });

      grid.appendChild(card);
    });
  }

  // ==========================================================================
  // PROJECT DETAILS MODAL
  // ==========================================================================
  function openProjectModal(project) {
    activeProject = project;
    const modal = document.getElementById('project-modal');
    if (!modal) return;

    document.getElementById('modal-title').textContent = project.title;
    document.getElementById('modal-category').textContent = project.category_label || project.category;
    document.getElementById('modal-location').textContent = project.location;
    document.getElementById('modal-client').textContent = project.client || 'Commissioned Work';
    document.getElementById('modal-desc').textContent = project.description;

    // Details table
    const specsContainer = document.getElementById('modal-specs');
    if (specsContainer && project.details) {
      specsContainer.innerHTML = '';
      Object.entries(project.details).forEach(([key, val]) => {
        const row = document.createElement('div');
        row.className = 'py-2 border-b border-white/5 flex justify-between text-xs';
        row.innerHTML = `<span class="text-zinc-400 font-mono">${key}:</span> <span class="text-zinc-200 font-medium text-right">${val}</span>`;
        specsContainer.appendChild(row);
      });
    }

    // Gallery
    const mainImg = document.getElementById('modal-main-img');
    const thumbnailsBox = document.getElementById('modal-thumbnails');
    if (mainImg) mainImg.src = project.image;

    if (thumbnailsBox) {
      thumbnailsBox.innerHTML = '';
      const gallery = project.gallery && project.gallery.length > 0 ? project.gallery : [project.image];
      gallery.forEach((imgSrc, idx) => {
        const thumb = document.createElement('img');
        thumb.src = imgSrc;
        thumb.alt = `${project.title} view ${idx + 1}`;
        thumb.className = `w-16 h-16 rounded-md object-cover cursor-pointer border ${idx === 0 ? 'border-[#c5a880]' : 'border-white/10 opacity-60'} hover:opacity-100 transition-all`;
        thumb.addEventListener('click', () => {
          mainImg.src = imgSrc;
          thumbnailsBox.querySelectorAll('img').forEach(t => {
            t.classList.remove('border-[#c5a880]');
            t.classList.add('border-white/10', 'opacity-60');
          });
          thumb.classList.add('border-[#c5a880]');
          thumb.classList.remove('border-white/10', 'opacity-60');
        });
        thumbnailsBox.appendChild(thumb);
      });
    }

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  // Close modal
  const closeModalBtn = document.getElementById('close-modal-btn');
  const projectModal = document.getElementById('project-modal');
  if (closeModalBtn && projectModal) {
    closeModalBtn.addEventListener('click', () => {
      projectModal.classList.add('hidden');
      document.body.style.overflow = 'auto';
    });
    projectModal.addEventListener('click', (e) => {
      if (e.target === projectModal) {
        projectModal.classList.add('hidden');
        document.body.style.overflow = 'auto';
      }
    });
  }

  // Escape key handler
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (projectModal && !projectModal.classList.contains('hidden')) {
        projectModal.classList.add('hidden');
        document.body.style.overflow = 'auto';
      }
      const lightbox = document.getElementById('lightbox-modal');
      if (lightbox && !lightbox.classList.contains('hidden')) {
        lightbox.classList.add('hidden');
        document.body.style.overflow = 'auto';
      }
    }
  });

  // ==========================================================================
  // BLUEPRINT & TECHNICAL PLANS VIEWER
  // ==========================================================================
  function initBlueprintTabs() {
    const tabButtons = document.querySelectorAll('.blueprint-tab-btn');
    const displayImg = document.getElementById('blueprint-main-img');
    const displayTitle = document.getElementById('blueprint-title');
    const displayCategory = document.getElementById('blueprint-category');
    const displayDesc = document.getElementById('blueprint-desc');

    if (!tabButtons.length || !displayImg) return;

    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        tabButtons.forEach(b => {
          b.classList.remove('bg-[#c5a880]', 'text-[#0a0a0c]', 'font-semibold');
          b.classList.add('bg-[#121216]', 'text-zinc-400');
        });

        btn.classList.add('bg-[#c5a880]', 'text-[#0a0a0c]', 'font-semibold');
        btn.classList.remove('bg-[#121216]', 'text-zinc-400');

        const imgSrc = btn.getAttribute('data-img');
        const title = btn.getAttribute('data-title');
        const cat = btn.getAttribute('data-cat');
        const desc = btn.getAttribute('data-desc');

        displayImg.style.opacity = '0';
        setTimeout(() => {
          displayImg.src = imgSrc;
          if (displayTitle) displayTitle.textContent = title;
          if (displayCategory) displayCategory.textContent = cat;
          if (displayDesc) displayDesc.textContent = desc;
          displayImg.style.opacity = '1';
        }, 150);
      });
    });
  }

  // ==========================================================================
  // LIGHTBOX
  // ==========================================================================
  function initLightbox() {
    const lightbox = document.getElementById('lightbox-modal');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const closeBtn = document.getElementById('lightbox-close');

    if (!lightbox || !lightboxImg) return;

    window.openLightbox = function (src, caption) {
      lightboxImg.src = src;
      if (lightboxCaption) lightboxCaption.textContent = caption || '';
      lightbox.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    };

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        lightbox.classList.add('hidden');
        document.body.style.overflow = 'auto';
      });
    }

    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        lightbox.classList.add('hidden');
        document.body.style.overflow = 'auto';
      }
    });
  }

  // ==========================================================================
  // CONTACT FORM & WHATSAPP GENERATOR
  // ==========================================================================
  function setupContactForm() {
    const form = document.getElementById('consultation-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('client-name')?.value.trim();
      const phone = document.getElementById('client-phone')?.value.trim();
      const projectType = document.getElementById('project-type')?.value;
      const location = document.getElementById('project-location')?.value.trim();
      const message = document.getElementById('client-message')?.value.trim();

      const fullMessage = `Hello Ar. Deepti Singh,\n\nI would like to inquire about architectural & interior design services.\n\n*Name:* ${name}\n*Phone:* ${phone}\n*Project Type:* ${projectType}\n*Location:* ${location}\n*Requirements:* ${message}`;

      const encoded = encodeURIComponent(fullMessage);
      const whatsappUrl = `https://wa.me/918989594919?text=${encoded}`;

      // Open WhatsApp in new tab
      window.open(whatsappUrl, '_blank');

      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = `
          <svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>
          Inquiry Initiated on WhatsApp...
        `;
        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          form.reset();
        }, 3000);
      }
    });
  }

  // Minimal scroll reveal / fade-in observer
  function initAOS() {
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('opacity-100', 'translate-y-0');
          entry.target.classList.remove('opacity-0', 'translate-y-8');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    revealElements.forEach(el => {
      el.classList.add('transition-all', 'duration-700', 'opacity-0', 'translate-y-8');
      observer.observe(el);
    });
  }


  // ==========================================================================
  // DUAL THEME ENGINE (DARK / LIGHT ARCHITECTURAL PAPER)
  // ==========================================================================
  function initThemeToggle() {
    const htmlEl = document.documentElement;
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    const savedTheme = localStorage.getItem('deepti-portfolio-theme');

    // Default to dark or user saved
    if (savedTheme === 'light') {
      htmlEl.classList.add('theme-light');
      updateIcons('light');
    } else {
      htmlEl.classList.remove('theme-light');
      updateIcons('dark');
    }

    toggleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const isCurrentlyLight = htmlEl.classList.contains('theme-light');
        if (isCurrentlyLight) {
          htmlEl.classList.remove('theme-light');
          localStorage.setItem('deepti-portfolio-theme', 'dark');
          updateIcons('dark');
        } else {
          htmlEl.classList.add('theme-light');
          localStorage.setItem('deepti-portfolio-theme', 'light');
          updateIcons('light');
        }
      });
    });

    function updateIcons(mode) {
      document.querySelectorAll('.theme-icon-sun').forEach(el => {
        if (mode === 'light') el.classList.remove('hidden');
        else el.classList.add('hidden');
      });
      document.querySelectorAll('.theme-icon-moon').forEach(el => {
        if (mode === 'light') el.classList.add('hidden');
        else el.classList.remove('hidden');
      });
    }
  }

  // ==========================================================================
  // AUTOCAD TECHNICAL DRAFTING & PENCIL CURSOR
  // ==========================================================================
  function initCadCursor() {
    // Only enable on desktop fine pointer devices
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    document.body.classList.add('enable-cad-cursor');

    const cursorContainer = document.getElementById('cad-cursor');
    const coordsEl = document.getElementById('cad-coords');
    if (!cursorContainer) return;

    let mouseX = -100;
    let mouseY = -100;
    let currentX = -100;
    let currentY = -100;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursorContainer.style.opacity = '1';

      if (coordsEl) {
        coordsEl.textContent = 'X: ' + mouseX.toFixed(0) + ' Y: ' + mouseY.toFixed(0);
      }
    });

    window.addEventListener('mouseleave', () => {
      cursorContainer.style.opacity = '0';
    });

    // Smooth render loop
    function renderCursor() {
      currentX += (mouseX - currentX) * 0.9;
      currentY += (mouseY - currentY) * 0.9;
      cursorContainer.style.left = currentX + 'px';
      cursorContainer.style.top = currentY + 'px';
      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);

    // Snap to interactive elements (AutoCAD OSNAP Target effect)
    const interactiveSelector = 'a, button, input, select, textarea, .arch-card, .r2r-select-btn, .blueprint-tab-btn, [role="button"]';
    
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(interactiveSelector)) {
        cursorContainer.classList.add('cad-cursor-snap');
      }
    });

    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(interactiveSelector)) {
        cursorContainer.classList.remove('cad-cursor-snap');
      }
    });
  }

})();

