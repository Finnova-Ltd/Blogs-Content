/**
 * Salesforce Piper-Style 10-Second Interactive Floating Video Greeting Assistant
 * Automatically engages website visitors after 10s with an interactive video greeting.
 */

(function () {
  'use strict';

  // Prevent duplicate initialization
  if (window.__PIPER_ASSISTANT_INITIALIZED__) return;
  window.__PIPER_ASSISTANT_INITIALIZED__ = true;

  // Configuration with Brand Defaults
  const config = Object.assign(
    {
      delayMs: 10000, // 10-second timer matching Salesforce Piper
      brandName: 'EZ Mortgage Broker',
      avatarName: 'R Bakshi • AI Mortgage Specialist',
      posterImg: '/images/finnova-avatar.jpeg',
      // High-resolution video generated from ElevenLabs / Cloudflare
      videoSrc: '/images/finnova-avatar.mp4',
      greetingText: 'G\'day! I\'m your AI Lending Specialist at <strong>EZ Mortgage Broker</strong>. I compare 50+ Australian banks to unlock lower rates & boost your borrowing power.',
      actions: [
        { label: '📊 Calculate Borrowing Power', href: '/calculators.html#borrowing-power', primary: true },
        { label: '💰 Compare 50+ Bank Rates', href: 'javascript:window.openRateImpactModal ? window.openRateImpactModal() : (window.location.href=\"/pages/refinancing.html\")' },
        { label: '📞 Request Free Broker Callback', href: 'tel:1300050099' }
      ]
    },
    window.PIPER_AVATAR_CONFIG || {}
  );

  // Check if previously dismissed in session
  const isDismissed = sessionStorage.getItem('piper_dismissed') === 'true';

  function createMarkup() {
    // 1. Trigger Bubble
    const bubble = document.createElement('div');
    bubble.id = 'piper-bubble-trigger';
    bubble.setAttribute('role', 'button');
    bubble.setAttribute('aria-label', 'Open AI Video Guide');
    bubble.innerHTML = `
      <div class="piper-avatar-thumb">
        <img src="${config.posterImg}" alt="${config.avatarName}" loading="lazy" />
        <span class="piper-online-dot"></span>
      </div>
      <div class="piper-trigger-text">
        <span class="piper-trigger-title">${config.avatarName.split('•')[0].trim()}</span>
        <span class="piper-trigger-sub">👋 Tap to chat</span>
      </div>
    `;

    // 2. Expanded Video Card
    const card = document.createElement('div');
    card.id = 'piper-video-card';
    card.innerHTML = `
      <div class="piper-card-header">
        <div class="piper-header-info">
          <span class="piper-badge-live">AI LIVE</span>
          <span class="piper-header-title">${config.avatarName}</span>
        </div>
        <div class="piper-card-actions">
          <button type="button" class="piper-icon-btn" id="piper-btn-minimize" aria-label="Minimize Assistant">_</button>
          <button type="button" class="piper-icon-btn" id="piper-btn-close" aria-label="Close Assistant">&times;</button>
        </div>
      </div>

      <div class="piper-video-stage">
        <video id="piper-video-element" playsinline loop muted preload="metadata" poster="${config.posterImg}">
          <source src="${config.videoSrc}" type="video/mp4">
        </video>
        <div class="piper-unmute-overlay" id="piper-unmute-layer">
          <button type="button" class="piper-unmute-btn" id="piper-unmute-trigger">
            🔊 Tap to Unmute & Listen
          </button>
        </div>
      </div>

      <div class="piper-speech-box">
        <p class="piper-speech-text">${config.greetingText}</p>
      </div>

      <div class="piper-action-pills">
        ${config.actions
          .map(
            (act) =>
              `<a href="${act.href}" class="piper-pill-btn ${act.primary ? 'primary' : ''}">${act.label} <span>&rarr;</span></a>`
          )
          .join('')}
      </div>
    `;

    document.body.appendChild(bubble);
    document.body.appendChild(card);

    // Event Handlers
    const video = card.querySelector('#piper-video-element');
    const unmuteLayer = card.querySelector('#piper-unmute-layer');
    const unmuteTrigger = card.querySelector('#piper-unmute-trigger');
    const btnMinimize = card.querySelector('#piper-btn-minimize');
    const btnClose = card.querySelector('#piper-btn-close');

    function openAssistant(playAudio = false) {
      card.classList.add('piper-open');
      bubble.style.display = 'none';
      if (video) {
        if (playAudio) {
          video.muted = false;
          unmuteLayer.classList.add('hidden');
        }
        video.play().catch(() => {});
      }
    }

    function closeAssistant() {
      card.classList.remove('piper-open');
      bubble.style.display = 'flex';
      if (video) {
        video.pause();
      }
    }

    bubble.addEventListener('click', () => openAssistant(true));
    btnMinimize.addEventListener('click', closeAssistant);
    btnClose.addEventListener('click', () => {
      closeAssistant();
      sessionStorage.setItem('piper_dismissed', 'true');
    });

    unmuteLayer.addEventListener('click', () => {
      if (video) {
        video.muted = false;
        video.currentTime = 0;
        video.play().catch(() => {});
        unmuteLayer.classList.add('hidden');
      }
    });

    // 10-Second Smart Auto-Trigger (Salesforce Piper Behavior)
    if (!isDismissed) {
      setTimeout(() => {
        if (!sessionStorage.getItem('piper_dismissed')) {
          openAssistant(false); // Opens after 10s (muted autoplay as per browser autoplay policy)
        }
      }, config.delayMs);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createMarkup);
  } else {
    createMarkup();
  }
})();
