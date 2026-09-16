(function () {
  'use strict';

  var config = window.CookiePolicyConfig || {};
  var businessName = config.businessName || 'Finnova Ltd';
  var policyPath = config.policyPath || 'cookie-policy.html';
  var storageKey = config.storageKey || 'cookie-consent-v1';
  var stored = null;

  try {
    var raw = window.localStorage.getItem(storageKey);
    stored = raw ? JSON.parse(raw) : null;
  } catch (error) {
    try { window.localStorage.removeItem(storageKey); } catch (storageError) {}
  }

  function save(preferences) {
    var consent = {
      necessary: true,
      analytics: Boolean(preferences.analytics),
      advertising: Boolean(preferences.advertising),
      updatedAt: new Date().toISOString()
    };
    try { window.localStorage.setItem(storageKey, JSON.stringify(consent)); } catch (error) {}
    document.documentElement.dataset.cookieAnalytics = consent.analytics ? 'allowed' : 'denied';
    document.documentElement.dataset.cookieAdvertising = consent.advertising ? 'allowed' : 'denied';

    // Dispatch Custom Event for external scripts / vendor tags
    try {
      var event = new CustomEvent('cookieConsentChanged', { detail: consent });
      window.dispatchEvent(event);
    } catch (e) {}

    return consent;
  }

  function renderUI() {
    if (document.getElementById('cookieBanner')) return;

    document.body.insertAdjacentHTML('beforeend',
      '<div class="cookie-banner" id="cookieBanner" role="region" aria-label="Cookie notice">' +
        '<div class="cookie-banner-copy"><strong>' + businessName + ' (ABN 55 687 130 767 | ACNC Registered Charity &amp; PBI) uses essential cookies by default.</strong><p>Optional experience, measurement, and community tool cookies are off unless you choose to enable them. Read our <a href="' + policyPath + '">Cookie Policy</a> or change your preferences at any time.</p></div>' +
        '<div class="cookie-banner-actions"><button type="button" class="cookie-button" id="cookieReject">Reject optional</button><button type="button" class="cookie-button" id="cookieSettings">Cookie settings</button><button type="button" class="cookie-button cookie-button-primary" id="cookieAccept">Accept cookies</button></div>' +
        '<button type="button" class="cookie-banner-close" id="cookieBannerClose" aria-label="Open cookie settings">&times;</button>' +
      '</div>' +
      '<div class="cookie-preferences" id="cookiePreferences" aria-hidden="true" hidden>' +
        '<div class="cookie-preferences-backdrop" data-cookie-close></div>' +
        '<section class="cookie-preferences-dialog" role="dialog" aria-modal="true" aria-labelledby="cookiePreferencesTitle">' +
          '<button type="button" class="cookie-preferences-close" data-cookie-close aria-label="Close cookie preferences">&times;</button>' +
          '<h2 id="cookiePreferencesTitle">Cookie settings</h2>' +
          '<p>Necessary cookies are always enabled. Optional cookies remain off until you choose to allow them. Read our <a href="' + policyPath + '">Cookie Policy</a>.</p>' +
          '<hr>' +
          '<div class="cookie-category"><span class="cookie-check is-checked">&#10003;</span><div><strong>Necessary cookies</strong><p>Required for navigation, security, forms, and remembering your privacy choice.</p></div></div>' +
          '<label class="cookie-category cookie-category-toggle"><input type="checkbox" id="cookieAnalytics"><span class="cookie-check"></span><span><strong>Experience and measurement cookies</strong><small>Help us understand usage and improve the website.</small></span></label>' +
          '<label class="cookie-category cookie-category-toggle"><input type="checkbox" id="cookieAdvertising"><span class="cookie-check"></span><span><strong>Advertising cookies</strong><small>May help measure campaigns or make advertising more relevant.</small></span></label>' +
          '<div class="cookie-preferences-actions"><button type="button" class="cookie-button" id="cookiePreferencesReject">Reject optional</button><button type="button" class="cookie-button cookie-button-primary" id="cookieSave">Save selection</button><button type="button" class="cookie-button cookie-button-primary" id="cookiePreferencesAccept">Accept cookies</button></div>' +
        '</section>' +
      '</div>'
    );

    var banner = document.getElementById('cookieBanner');
    var preferences = document.getElementById('cookiePreferences');
    var analytics = document.getElementById('cookieAnalytics');
    var advertising = document.getElementById('cookieAdvertising');

    function openPreferences() {
      var current = stored || { analytics: false, advertising: false };
      analytics.checked = Boolean(current.analytics);
      advertising.checked = Boolean(current.advertising);
      preferences.hidden = false;
      preferences.setAttribute('aria-hidden', 'false');
      var saveBtn = document.getElementById('cookieSave');
      if (saveBtn) saveBtn.focus();
    }

    function closePreferences() {
      preferences.hidden = true;
      preferences.setAttribute('aria-hidden', 'true');
    }

    function finish(preferencesChoice) {
      stored = save(preferencesChoice);
      banner.classList.add('is-dismissed');
      closePreferences();
    }

    if (stored || navigator.globalPrivacyControl === true) {
      stored = save(navigator.globalPrivacyControl === true ? { analytics: false, advertising: false } : stored);
      banner.classList.add('is-dismissed');
    }

    document.getElementById('cookieAccept').addEventListener('click', function () { finish({ analytics: true, advertising: true }); });
    document.getElementById('cookieReject').addEventListener('click', function () { finish({ analytics: false, advertising: false }); });
    document.getElementById('cookiePreferencesAccept').addEventListener('click', function () { finish({ analytics: true, advertising: true }); });
    document.getElementById('cookiePreferencesReject').addEventListener('click', function () { finish({ analytics: false, advertising: false }); });
    document.getElementById('cookieSave').addEventListener('click', function () { finish({ analytics: analytics.checked, advertising: advertising.checked }); });
    document.getElementById('cookieSettings').addEventListener('click', openPreferences);
    document.getElementById('cookieBannerClose').addEventListener('click', openPreferences);
    document.querySelectorAll('[data-cookie-close]').forEach(function (element) { element.addEventListener('click', closePreferences); });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape' && !preferences.hidden) closePreferences(); });

    // Expose Global Helper API
    window.CookieConsent = {
      get: function() { return stored; },
      isAllowed: function(category) {
        if (!category || category === 'necessary') return true;
        return stored ? Boolean(stored[category]) : false;
      },
      set: finish,
      openSettings: openPreferences,
      onConsent: function(fn) {
        if (typeof fn === 'function') {
          if (stored) fn(stored);
          window.addEventListener('cookieConsentChanged', function(e) { fn(e.detail); });
        }
      }
    };
    window.openFinnovaCookieSettings = openPreferences;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderUI);
  } else {
    renderUI();
  }
})();
