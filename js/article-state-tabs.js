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
    hdr.addEventListener('click', function () {
      sidebarManualLock = true;
      clearTimeout(sidebarLockTimeout);
      sidebarLockTimeout = setTimeout(function () {
        sidebarManualLock = false;
      }, 4000);

      var widget = this.closest('.sidebar-accordion-widget');
      if (!widget) return;
      var icon = this.querySelector('.sidebar-accordion-icon');
      var isOpen = widget.classList.contains('open');

      if (isOpen) {
        widget.classList.remove('open');
        this.setAttribute('aria-expanded', 'false');
        if (icon) icon.textContent = '+';
      } else {
        // Smoothly collapse other sidebar widgets to keep column 2 neat
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

  // Manual Click handler for main content
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

  // 6. Dynamic Scroll-Driven Auto-Closing (Column 1 & Column 2)
  var scrollDebounce = null;
  function handleScrollSpy() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // At top of page (< 80px): keep everything open
    if (scrollY < 80) {
      if (!userManualLock) {
        sectionAccordions.forEach(function (acc) {
          acc.classList.add('open');
          var hdr = acc.querySelector('.article-section-accordion-header');
          var icon = acc.querySelector('.section-accordion-icon');
          if (hdr) hdr.setAttribute('aria-expanded', 'true');
          if (icon) icon.textContent = '−';
        });
      }
      if (!sidebarManualLock) {
        sidebarWidgets.forEach(function (w) {
          w.classList.add('open');
          var hdr = w.querySelector('.sidebar-accordion-header');
          var icon = w.querySelector('.sidebar-accordion-icon');
          if (hdr) hdr.setAttribute('aria-expanded', 'true');
          if (icon) icon.textContent = '−';
        });
      }
      return;
    }

    // When scrolling down, auto-collapse Column 1 sections except active one in reading line
    if (!userManualLock && sectionAccordions.length > 0) {
      var activeAcc = null;
      var smallestDist = Infinity;
      var targetReadingLine = 220;

      sectionAccordions.forEach(function (acc) {
        var rect = acc.getBoundingClientRect();
        var dist = Math.abs(rect.top - targetReadingLine);
        if (rect.top <= (window.innerHeight * 0.7) && rect.bottom >= 100) {
          if (dist < smallestDist) {
            smallestDist = dist;
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

    // When scrolling down into deep reading, also collapse Column 2 widgets so the sticky CTA stays visible
    if (!sidebarManualLock && sidebarWidgets.length > 0) {
      if (scrollY > 350) {
        sidebarWidgets.forEach(function (w) {
          if (w.classList.contains('open')) {
            w.classList.remove('open');
            var hdr = w.querySelector('.sidebar-accordion-header');
            var icon = w.querySelector('.sidebar-accordion-icon');
            if (hdr) hdr.setAttribute('aria-expanded', 'false');
            if (icon) icon.textContent = '+';
          }
        });
      }
    }
  }

  window.addEventListener('scroll', function () {
    clearTimeout(scrollDebounce);
    scrollDebounce = setTimeout(handleScrollSpy, 40);
  }, { passive: true });

  // 7. Sticky Region Selector Bar on Scroll
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

  // 8. State Tabs Switching
  var rawDataEl = document.getElementById('rawStateData');
  if (rawDataEl) {
    var stateDataMap = {};
    try {
      stateDataMap = JSON.parse(rawDataEl.textContent);
    } catch (e) {
      console.error('Failed to parse state data', e);
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

    renderState('General', false);
  }

  // 9. 2-Step 360° Review Lead Modal Engine
  var modal = document.getElementById('ezModalOverlay');
  var closeBtn = document.getElementById('ezModalClose');
  var nextBtn = document.getElementById('ezNextBtn');
  var backBtn = document.getElementById('ezBackBtn');
  var step1 = document.getElementById('ezStep1');
  var step2 = document.getElementById('ezStep2');
  var progressFill = document.getElementById('ezProgressFill');
  var modalTitle = document.getElementById('ezModalTitle');

  if (modal) {
    var openModal = function (e) {
      if (e) e.preventDefault();
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    };

    var closeModal = function () {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    document.querySelectorAll('.open-ez-modal, a[href="#contact"], a[href="#book-consult"], a[href="#free-review"]').forEach(function (el) {
      el.addEventListener('click', openModal);
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) {
      if (e.target === modal) closeModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('active')) closeModal();
    });

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        if (step1 && step2) {
          step1.classList.remove('active');
          step2.classList.add('active');
          if (progressFill) progressFill.style.width = '100%';
          if (modalTitle) modalTitle.textContent = 'Where should we send your borrowing report?';
          var nameInput = document.getElementById('ezFullName');
          if (nameInput) nameInput.focus();
        }
      });
    }

    if (backBtn) {
      backBtn.addEventListener('click', function () {
        if (step1 && step2) {
          step2.classList.remove('active');
          step1.classList.add('active');
          if (progressFill) progressFill.style.width = '50%';
          if (modalTitle) modalTitle.textContent = "Let's find your best loan options";
        }
      });
    }
  }
})();
