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
  var sidebarHdrBtns = document.querySelectorAll('.sidebar-accordion-header');
  sidebarHdrBtns.forEach(function (hdr) {
    hdr.addEventListener('click', function () {
      var widget = this.closest('.sidebar-accordion-widget');
      if (!widget) return;
      var body = widget.querySelector('.sidebar-accordion-body');
      var icon = this.querySelector('.sidebar-accordion-icon');
      var isOpen = widget.classList.contains('open');

      if (isOpen) {
        widget.classList.remove('open');
        this.setAttribute('aria-expanded', 'false');
        if (body) body.style.display = 'none';
        if (icon) icon.textContent = '+';
      } else {
        widget.classList.add('open');
        this.setAttribute('aria-expanded', 'true');
        if (body) body.style.display = 'block';
        if (icon) icon.textContent = '−';
      }
    });
  });

  // 5. Section Accordions:
  // - ALL accordions are open by default on initial page load.
  // - As soon as the user scrolls down, auto-close all accordions EXCEPT the one the user is currently reading!
  var sectionAccordions = document.querySelectorAll('.article-section-accordion');
  var userManualLock = false;
  var lockTimeout = null;

  // Make sure all are open on initial load
  sectionAccordions.forEach(function (acc) {
    acc.classList.add('open');
    var hdr = acc.querySelector('.article-section-accordion-header');
    var icon = acc.querySelector('.section-accordion-icon');
    if (hdr) hdr.setAttribute('aria-expanded', 'true');
    if (icon) icon.textContent = '−';
  });

  // Manual click handler
  sectionAccordions.forEach(function (acc) {
    var hdr = acc.querySelector('.article-section-accordion-header');
    if (!hdr) return;

    hdr.addEventListener('click', function () {
      userManualLock = true;
      clearTimeout(lockTimeout);
      lockTimeout = setTimeout(function () {
        userManualLock = false;
      }, 3500);

      var icon = this.querySelector('.section-accordion-icon');
      var isOpen = acc.classList.contains('open');

      if (isOpen) {
        acc.classList.remove('open');
        this.setAttribute('aria-expanded', 'false');
        if (icon) icon.textContent = '+';
      } else {
        // Close other accordions when manually opening
        sectionAccordions.forEach(function (otherAcc) {
          if (otherAcc !== acc) {
            otherAcc.classList.remove('open');
            var otherHdr = otherAcc.querySelector('.article-section-accordion-header');
            var otherIcon = otherAcc.querySelector('.section-accordion-icon');
            if (otherHdr) otherHdr.setAttribute('aria-expanded', 'false');
            if (otherIcon) otherIcon.textContent = '+';
          }
        });

        acc.classList.add('open');
        this.setAttribute('aria-expanded', 'true');
        if (icon) icon.textContent = '−';
      }
    });
  });

  // Dynamic Scroll-Driven Auto-Closing Observer
  var scrollDebounce = null;
  function handleScrollSpy() {
    if (userManualLock || sectionAccordions.length === 0) return;

    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // If user is at very top (first 80px), keep all open
    if (scrollY < 80) {
      sectionAccordions.forEach(function (acc) {
        acc.classList.add('open');
        var hdr = acc.querySelector('.article-section-accordion-header');
        var icon = acc.querySelector('.section-accordion-icon');
        if (hdr) hdr.setAttribute('aria-expanded', 'true');
        if (icon) icon.textContent = '−';
      });
      return;
    }

    // Find the accordion whose header is in the active reading zone (top 100px to 450px)
    var activeAcc = null;
    var smallestDistance = Infinity;
    var targetReadingLine = 220; // pixels from top of viewport

    sectionAccordions.forEach(function (acc) {
      var rect = acc.getBoundingClientRect();
      // Distance from top of accordion to reading line
      var dist = Math.abs(rect.top - targetReadingLine);

      // Accordion is visible in viewport reading range
      if (rect.top <= (window.innerHeight * 0.7) && rect.bottom >= 100) {
        if (dist < smallestDistance) {
          smallestDistance = dist;
          activeAcc = acc;
        }
      }
    });

    if (activeAcc) {
      sectionAccordions.forEach(function (acc) {
        var hdr = acc.querySelector('.article-section-accordion-header');
        var icon = acc.querySelector('.section-accordion-icon');

        if (acc === activeAcc) {
          if (!acc.classList.contains('open')) {
            acc.classList.add('open');
            if (hdr) hdr.setAttribute('aria-expanded', 'true');
            if (icon) icon.textContent = '−';
          }
        } else {
          if (acc.classList.contains('open')) {
            acc.classList.remove('open');
            if (hdr) hdr.setAttribute('aria-expanded', 'false');
            if (icon) icon.textContent = '+';
          }
        }
      });
    }
  }

  window.addEventListener('scroll', function () {
    clearTimeout(scrollDebounce);
    scrollDebounce = setTimeout(handleScrollSpy, 40);
  }, { passive: true });

  // 6. Sticky Region Selector Bar on Scroll
  var stickyTabs = document.getElementById('stickyHeaderStateTabs');
  if (stickyTabs) {
    var initialOffset = stickyTabs.offsetTop + 120;
    window.addEventListener('scroll', function () {
      if (window.pageYOffset > initialOffset) {
        stickyTabs.classList.add('is-sticky');
      } else {
        stickyTabs.classList.remove('is-sticky');
      }
    }, { passive: true });
  }

  // 7. State Tabs Switching
  var rawDataEl = document.getElementById('rawStateData');
  if (!rawDataEl) return;

  var stateDataMap = {};
  try {
    stateDataMap = JSON.parse(rawDataEl.textContent);
  } catch (e) {
    console.error('Failed to parse state data', e);
    return;
  }

  var tabBtns = document.querySelectorAll('[data-state-tab]');
  var titleEl = document.getElementById('dynamicStateTitle');
  var badgeEl = document.getElementById('dynamicStateBadge');
  var bodyEl = document.getElementById('dynamicStateBodyContent');
  var portalLinkEl = document.getElementById('dynamicStatePortalLink');
  var hubBox = document.getElementById('dynamicStateHubBox');

  function renderState(stateKey, shouldScroll) {
    var data = stateDataMap[stateKey] || stateDataMap['General'];
    if (!data) return;

    tabBtns.forEach(function (b) {
      if (b.getAttribute('data-state-tab') === stateKey) {
        b.classList.add('active');
      } else {
        b.classList.remove('active');
      }
    });

    if (titleEl) titleEl.textContent = data.title;
    if (badgeEl) badgeEl.textContent = data.badge;
    if (portalLinkEl) {
      portalLinkEl.href = data.portalUrl;
      portalLinkEl.textContent = '🏛️ ' + data.portalName + ' →';
    }

    if (bodyEl && data.sections) {
      var html = '';
      for (var i = 0; i < data.sections.length; i++) {
        var sec = data.sections[i];
        html += '<div class="dynamic-state-content-section">' +
                '<h4>' + sec.heading + '</h4>' +
                sec.content +
                '</div>';
      }
      bodyEl.innerHTML = html;
    }

    if (shouldScroll && hubBox) {
      hubBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  tabBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetState = this.getAttribute('data-state-tab');
      renderState(targetState, true);
    });
  });

  // Initialize with default state
  renderState('General', false);
})();
