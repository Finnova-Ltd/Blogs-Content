(function () {
  // 1. Safe Copy Link
  var copyBtn = document.getElementById('copyArticleLinkBtn');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(window.location.href).then(function () {
          alert('Link copied to clipboard!');
        }).catch(function () {
          prompt('Copy link:', window.location.href);
        });
      } else {
        prompt('Copy link:', window.location.href);
      }
    });
  }

  // 2. Mobile Smart Header Hide / Desktop Sticky Header
  var siteHeader = document.querySelector('.site-header');
  var lastScrollY = window.pageYOffset;
  if (siteHeader) {
    window.addEventListener('scroll', function () {
      var currentScrollY = window.pageYOffset;
      var isMobile = window.innerWidth <= 768;

      if (isMobile) {
        if (currentScrollY > 80 && currentScrollY > lastScrollY) {
          siteHeader.classList.add('mobile-header-hidden');
        } else {
          siteHeader.classList.remove('mobile-header-hidden');
        }
      } else {
        siteHeader.classList.remove('mobile-header-hidden');
      }
      lastScrollY = currentScrollY;
    }, { passive: true });
  }

  // 3. Program Comparison Cards Inner Accordions
  var innerAccordionBtns = document.querySelectorAll('.program-accordion-btn');
  innerAccordionBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var content = this.nextElementSibling;
      var icon = this.querySelector('.accordion-icon');
      var isExpanded = this.getAttribute('aria-expanded') === 'true';
      if (isExpanded) {
        this.setAttribute('aria-expanded', 'false');
        if (content) {
          content.classList.remove('open');
          content.style.display = 'none';
        }
        if (icon) icon.textContent = '+';
      } else {
        this.setAttribute('aria-expanded', 'true');
        if (content) {
          content.classList.add('open');
          content.style.display = 'block';
        }
        if (icon) icon.textContent = '−';
      }
    });
  });

  // 4. Column 2 Sidebar Accordions (Reviews, Calculators, Related Guides)
  var sidebarWidgets = document.querySelectorAll('.sidebar-accordion-widget');
  var sidebarHdrBtns = document.querySelectorAll('.sidebar-accordion-header');
  var sidebarManualLock = false;
  var sidebarLockTimeout = null;

  // Make sure all sidebar widgets start open
  sidebarWidgets.forEach(function (w) {
    w.classList.add('open');
    var hdr = w.querySelector('.sidebar-accordion-header');
    var icon = w.querySelector('.sidebar-accordion-icon');
    if (hdr) hdr.setAttribute('aria-expanded', 'true');
    if (icon) icon.textContent = '−';
  });

  // Manual Sidebar Click Handling
  sidebarHdrBtns.forEach(function (hdr) {
    hdr.addEventListener('click', function (e) {
      e.preventDefault();
      sidebarManualLock = true;
      clearTimeout(sidebarLockTimeout);
      sidebarLockTimeout = setTimeout(function () {
        sidebarManualLock = false;
      }, 5000);

      var widget = this.closest('.sidebar-accordion-widget');
      if (!widget) return;
      var icon = this.querySelector('.sidebar-accordion-icon');
      var isOpen = widget.classList.contains('open');

      if (isOpen) {
        widget.classList.remove('open');
        this.setAttribute('aria-expanded', 'false');
        if (icon) icon.textContent = '+';
      } else {
        sidebarWidgets.forEach(function (otherW) {
          if (otherW !== widget) {
            otherW.classList.remove('open');
            var otherHdr = otherW.querySelector('.sidebar-accordion-header');
            var otherIcon = otherW.querySelector('.sidebar-accordion-icon');
            if (otherHdr) otherHdr.setAttribute('aria-expanded', 'false');
            if (otherIcon) otherIcon.textContent = '+';
          }
        });

        widget.classList.add('open');
        this.setAttribute('aria-expanded', 'true');
        if (icon) icon.textContent = '−';
      }
    });
  });

  // 5. Main Section Accordions (Column 1)
  var sectionAccordions = document.querySelectorAll('.article-section-accordion');
  var userManualLock = false;
  var lockTimeout = null;

  // All accordions open on initial load
  sectionAccordions.forEach(function (acc) {
    acc.classList.add('open');
    var hdr = acc.querySelector('.article-section-accordion-header');
    var icon = acc.querySelector('.section-accordion-icon');
    if (hdr) hdr.setAttribute('aria-expanded', 'true');
    if (icon) icon.textContent = '−';
  });

  // Clean manual toggle handler (independent accordion sections)
  sectionAccordions.forEach(function (acc) {
    var hdr = acc.querySelector('.article-section-accordion-header');
    if (!hdr) return;

    hdr.addEventListener('click', function (e) {
      e.preventDefault();
      var icon = this.querySelector('.section-accordion-icon');
      var isOpen = acc.classList.contains('open');

      if (isOpen) {
        acc.classList.remove('open');
        this.setAttribute('aria-expanded', 'false');
        if (icon) icon.textContent = '+';
      } else {
        acc.classList.add('open');
        this.setAttribute('aria-expanded', 'true');
        if (icon) icon.textContent = '−';
      }
    });
  });

  // 6. Scroll-Aware Minimizing Obligation-Free Assessment Card (with smooth animation)
  var stickyCtaCard = document.getElementById('sidebarStickyAssessmentCard') || document.querySelector('.sidebar-sticky-cta-card');
  var ctaToggleBtn = document.getElementById('sidebarCtaToggleBtn') || (stickyCtaCard ? stickyCtaCard.querySelector('.sidebar-cta-toggle-btn') : null);
  var isUserManuallyExpanded = false;

  if (stickyCtaCard) {
    window.addEventListener('scroll', function () {
      var scrollY = window.pageYOffset || document.documentElement.scrollTop;
      if (scrollY > 300) {
        if (!isUserManuallyExpanded) {
          stickyCtaCard.classList.add('is-scrolled-minimized');
          if (ctaToggleBtn) ctaToggleBtn.textContent = '+';
        }
      } else {
        stickyCtaCard.classList.remove('is-scrolled-minimized');
        stickyCtaCard.classList.remove('user-expanded');
        isUserManuallyExpanded = false;
        if (ctaToggleBtn) ctaToggleBtn.textContent = '−';
      }
    }, { passive: true });

    if (ctaToggleBtn) {
      ctaToggleBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var isMin = stickyCtaCard.classList.contains('is-scrolled-minimized');
        if (isMin) {
          var isExp = stickyCtaCard.classList.toggle('user-expanded');
          ctaToggleBtn.textContent = isExp ? '−' : '+';
          isUserManuallyExpanded = isExp;
        } else {
          stickyCtaCard.classList.add('is-scrolled-minimized');
          ctaToggleBtn.textContent = '+';
        }
      });
    }
  }
})();