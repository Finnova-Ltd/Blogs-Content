(function () {
  if (window.__OMNI_AGENT_INITIALIZED__) return;
  window.__OMNI_AGENT_INITIALIZED__ = true;

  const currentDomain = window.location.hostname || "localhost";
  const scriptTag = document.currentScript || document.querySelector('script[src*="widget.js"]');
  const backendUrl = scriptTag ? new URL(scriptTag.src).origin : window.location.origin;

  // Dynamic Auto-Loader: Load Cookie Consent & Promo Banner if not already on the page
  if (!document.querySelector('script[src*="cookie-consent.js"]')) {
    const consentScript = document.createElement('script');
    consentScript.src = backendUrl + '/cookie-consent.js';
    consentScript.defer = true;
    document.head.appendChild(consentScript);
  }
  if (!document.querySelector('script[src*="promo-banner.js"]')) {
    const promoScript = document.createElement('script');
    promoScript.src = backendUrl + '/promo-banner.js';
    promoScript.defer = true;
    document.head.appendChild(promoScript);
  }

  let attachedImageBase64 = "";

  function getLeadScoreFromCookie() {
    const match = document.cookie.match(/(?:^|; )lead_score=([^;]*)/);
    if (match) return parseInt(decodeURIComponent(match[1]), 10) || 0;
    return parseInt(localStorage.getItem('lead_score') || "0", 10) || 0;
  }

  function setLeadScoreCookie(val) {
    const days = 30;
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `lead_score=${val}; expires=${date.toUTCString()}; path=/; SameSite=Lax`;
    try { localStorage.setItem('lead_score', val.toString()); } catch (e) {}
  }

  function updateLeadScore(points, reason) {
    const current = getLeadScoreFromCookie();
    const newScore = current + points;
    setLeadScoreCookie(newScore);

    if (newScore >= 35 && !window.__OMNI_PROACTIVE_TRIGGERED__) {
      window.__OMNI_PROACTIVE_TRIGGERED__ = true;
      const win = document.getElementById('omni-chat-window');
      if (win && win.style.display !== 'flex') {
        win.style.display = 'flex';
      }
    }
  }

  function getResolvedTheme(explicitTheme) {
    if (explicitTheme === 'dark') return 'dark';
    if (explicitTheme === 'light') return 'light';

    const html = document.documentElement;
    const body = document.body;
    const isDomDark = 
      (html && html.classList.contains('dark')) || 
      (body && body.classList.contains('dark')) || 
      (html && html.getAttribute('data-theme') === 'dark') || 
      (body && body.getAttribute('data-theme') === 'dark') ||
      (html && html.getAttribute('color-scheme') === 'dark');

    return isDomDark ? 'dark' : 'light';
  }

  let sessionId = localStorage.getItem('omni_chat_session') || 'sess_' + Math.random().toString(36).substring(2, 9);
  localStorage.setItem('omni_chat_session', sessionId);

  function parseMarkdown(text, primaryColor) {
    if (!text) return "";
    let html = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
    
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    html = html.replace(/^\s*[\*\-]\s+(.*)$/gm, '<div style="display:flex;gap:6px;margin:4px 0;"><span style="color:' + (primaryColor||"#0052FF") + '">•</span><span>$1</span></div>');
    html = html.replace(/^\s*(\d+)\.\s+(.*)$/gm, '<div style="display:flex;gap:6px;margin:4px 0;"><strong style="color:' + (primaryColor||"#0052FF") + '">$1.</strong><span>$2</span></div>');
    html = html.replace(/\n\n/g, '<br/><br/>').replace(/\n/g, '<br/>');
    return html;
  }

  function getBrowserScreenContext() {
    const mainHeading = document.querySelector('h1')?.innerText || document.querySelector('h2')?.innerText || "";
    const selectedText = window.getSelection ? window.getSelection().toString() : "";
    return {
      title: document.title,
      url: window.location.href,
      heading: mainHeading.substring(0, 150),
      selectedText: selectedText.substring(0, 200)
    };
  }

  const currentPath = window.location.pathname.toLowerCase();
  const sessionKey = 'scored_' + currentPath;

  if (!sessionStorage.getItem(sessionKey)) {
    if (/(careers|jobs|job-board)/.test(currentPath)) {
      updateLeadScore(-10, "Job Seeker");
    } else if (/(pricing|quote|request-demo|demo|consultation)/.test(currentPath)) {
      updateLeadScore(30, "High Intent Pricing");
    } else if (/(services|solutions)/.test(currentPath)) {
      updateLeadScore(20, "Services");
    } else if (/(case-studies|portfolio)/.test(currentPath)) {
      updateLeadScore(15, "Case Studies");
    } else if (/(blog|articles)/.test(currentPath)) {
      updateLeadScore(5, "Content View");
    }
    sessionStorage.setItem(sessionKey, "true");
  }

  window.addEventListener('scroll', function scrollHandler() {
    const scrollPercent = (window.scrollY + window.innerHeight) / document.body.scrollHeight;
    if (scrollPercent > 0.7) {
      updateLeadScore(15, "Deep Scroll");
      window.removeEventListener('scroll', scrollHandler);
    }
  });

  function appendToBody(el) {
    if (document.body) {
      document.body.appendChild(el);
    } else {
      document.addEventListener('DOMContentLoaded', () => {
        if (document.body && !document.getElementById(el.id)) {
          document.body.appendChild(el);
        }
      });
    }
  }

  const clientConfig = window.OMNI_CHAT_CONFIG || {};

  fetch(`${backendUrl}/api/config?domain=${currentDomain}`)
    .then(r => r.json())
    .catch(() => ({
      category: "DEFAULT",
      businessName: currentDomain,
      primaryColor: "#0052FF",
      theme: "light",
      proactiveGreeting: "Hello! How can I assist you today?",
      features: { rag: true, leadCapture: true, imageUpload: true, screenAwareness: true, leadScoring: true }
    }))
    .then(apiConfig => {
      const config = {
        ...apiConfig,
        ...clientConfig,
        category: clientConfig.category || apiConfig.category || "DEFAULT",
        businessName: clientConfig.businessInfo?.businessName || apiConfig.businessName || currentDomain,
        email: clientConfig.businessInfo?.email || apiConfig.email,
        phone: clientConfig.businessInfo?.phone || apiConfig.phone,
        primaryColor: clientConfig.primaryColor || apiConfig.primaryColor || "#0052FF"
      };
      initWidget(config);
    });

  function initWidget(config) {
    const themeMode = getResolvedTheme(config.theme);
    const isDark = themeMode === 'dark';
    const primaryColor = config.primaryColor || "#0052FF";
    const customTitle = config.businessName ? (config.businessName + " AI Assistant") : (currentDomain + " AI");
    const welcomeMsg = config.proactiveGreeting || ("Hello! Welcome to " + config.businessName + ". How can I help you today?");

    const winBg = isDark ? "#12141d" : "#ffffff";
    const winText = isDark ? "#f8fafc" : "#0f172a";
    const winBorder = isDark ? "rgba(255,255,255,0.1)" : "#e2e8f0";
    const msgAreaBg = isDark ? "#0f172a" : "#f8fafc";
    const assistantBg = isDark ? "#1e293b" : "#ffffff";
    const assistantText = isDark ? "#e2e8f0" : "#0f172a";
    const assistantBorder = isDark ? "rgba(255,255,255,0.05)" : "#e2e8f0";
    const inputContainerBg = isDark ? "#1e293b" : "#ffffff";
    const inputBg = isDark ? "#0f172a" : "#f1f5f9";
    const inputText = isDark ? "#ffffff" : "#0f172a";
    const inputBorder = isDark ? "rgba(255,255,255,0.15)" : "#cbd5e1";

    const style = document.createElement('style');
    style.innerHTML = `
      #omni-chat-bubble { position: fixed; bottom: 24px; right: 24px; width: 60px; height: 60px; background: ${primaryColor}; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 8px 24px rgba(0,82,255,0.35); z-index: 999999; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; transition: transform 0.2s; animation: omniPulse 3s infinite; }
      #omni-chat-bubble:hover { transform: scale(1.06); }
      #omni-chat-bubble svg { width: 28px; height: 28px; fill: #fff; }
      @keyframes omniPulse { 0%, 100% { box-shadow: 0 8px 24px rgba(0,82,255,0.35); } 50% { box-shadow: 0 0 0 8px rgba(0,82,255,0.18), 0 12px 28px rgba(0,82,255,0.4); } }
      #omni-chat-window { position: fixed; bottom: 96px; right: 24px; width: 410px; height: 620px; max-width: calc(100vw - 32px); max-height: calc(100vh - 110px); background: ${winBg} !important; color: ${winText} !important; border-radius: 20px; box-shadow: 0 20px 45px -5px rgba(0,0,0,0.22); display: none; flex-direction: column; overflow: hidden; z-index: 999999; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; border: 1px solid ${winBorder}; }
      #omni-chat-header { background: #ffffff !important; color: #0f172a !important; padding: 12px 16px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid ${winBorder}; }
      #omni-chat-header .title-wrap { display: flex; align-items: center; gap: 8px; }
      #omni-chat-header span.title { font-size: 15px; font-weight: 800; color: #0A2540; }
      #omni-chat-header span.badge { font-size: 11px; color: #64748b; font-weight: 600; background: #F1F5F9; padding: 2px 8px; border-radius: 999px; }
      .omni-hdr-actions { display: flex; gap: 8px; align-items: center; }
      .omni-btn-endchat { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; padding: 4px 8px; border-radius: 6px; font-size: 11px; cursor: pointer; font-weight: 600; }
      .omni-btn-endchat:hover { background: #E2E8F0; color: #0f172a; }
      
      /* Salesforce Piper Style Hero Card */
      .piper-hero-card { margin: 12px 14px 4px; border-radius: 16px; overflow: hidden; background: linear-gradient(180deg, #E0F2FE 0%, #FFFFFF 100%); border: 1px solid #BAE6FD; position: relative; box-shadow: 0 4px 14px rgba(0, 82, 255, 0.06); }
      .piper-hero-video-stage { position: relative; width: 100%; aspect-ratio: 16/9; background: #0A2540; overflow: hidden; }
      .piper-hero-video-stage video { width: 100%; height: 100%; object-fit: cover; display: block; }
      .piper-speak-badge-btn { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); background: #0052FF; color: #ffffff; border: none; padding: 6px 14px; border-radius: 999px; font-size: 12px; font-weight: 700; display: flex; align-items: center; gap: 6px; cursor: pointer; box-shadow: 0 4px 12px rgba(0, 82, 255, 0.4); z-index: 5; transition: all 0.2s; }
      .piper-speak-badge-btn:hover { background: #003ECC; transform: translateX(-50%) scale(1.04); }
      .piper-hero-intro { padding: 12px 14px; font-size: 13.5px; color: #1E293B; line-height: 1.45; font-weight: 500; }
      .piper-prompts-box { margin: 0 14px 10px; padding: 10px 12px; background: #F8FAFC; border-radius: 12px; border: 1px solid #E2E8F0; font-size: 12px; }
      .piper-prompts-title { font-weight: 700; color: #64748B; margin-bottom: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
      .piper-prompt-item { padding: 5px 8px; margin: 4px 0; background: #ffffff; border: 1px solid #CBD5E1; border-radius: 6px; color: #0A2540; font-weight: 600; cursor: pointer; transition: all 0.15s; display: flex; align-items: center; justify-content: space-between; }
      .piper-prompt-item:hover { background: #EFF6FF; border-color: #93C5FD; color: #0052FF; transform: translateX(2px); }
      .piper-cta-row { margin: 0 14px 12px; }
      .piper-connect-btn { width: 100%; background: #0052FF; color: #ffffff; border: none; padding: 9px 14px; border-radius: 8px; font-weight: 700; font-size: 13px; cursor: pointer; transition: background 0.2s; }
      .piper-connect-btn:hover { background: #003ECC; }

      #omni-chat-messages { flex: 1; padding: 12px 14px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; font-size: 13.5px; background: ${msgAreaBg} !important; }
      .omni-msg { padding: 10px 14px; border-radius: 12px; max-width: 88%; word-break: break-word; line-height: 1.5; }
      .omni-msg.user { background: ${primaryColor} !important; color: #ffffff !important; align-self: flex-end; border-bottom-right-radius: 3px; }
      .omni-msg.assistant { background: ${assistantBg} !important; color: ${assistantText} !important; align-self: flex-start; border-bottom-left-radius: 3px; border: 1px solid ${assistantBorder}; }
      .omni-msg.loading { color: #64748b; font-style: italic; }
      .omni-msg-actions { display: flex; gap: 8px; margin-top: 6px; font-size: 12px; opacity: 0.8; }
      .omni-action-btn { cursor: pointer; user-select: none; transition: transform 0.1s; }
      .omni-action-btn:hover { transform: scale(1.2); }
      
      #omni-image-preview-bar { display: none; padding: 6px 12px; background: ${inputContainerBg}; border-top: 1px solid ${winBorder}; align-items: center; gap: 8px; font-size: 12px; }
      #omni-image-preview-bar img { height: 36px; border-radius: 4px; border: 1px solid ${inputBorder}; }
      #omni-chat-input-container { display: flex; border-top: 1px solid ${winBorder}; padding: 10px 12px; background: ${inputContainerBg} !important; gap: 6px; align-items: center; }
      #omni-chat-input { flex: 1; background: ${inputBg} !important; border: 1px solid ${inputBorder} !important; border-radius: 8px; padding: 10px 12px; outline: none; color: ${inputText} !important; font-size: 13.5px; }
      #omni-chat-input:focus { border-color: ${primaryColor} !important; }
      .omni-attach-btn { background: transparent; border: none; color: #64748b; font-size: 18px; cursor: pointer; padding: 4px; }
      .omni-mic-btn { background: transparent; border: none; color: #64748b; font-size: 16px; cursor: pointer; padding: 4px; }
      .omni-mic-btn.active { color: #ef4444; animation: omniMicPulse 1s infinite; }
      @keyframes omniMicPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
      #omni-chat-send { background: ${primaryColor} !important; color: #ffffff !important; border: none; border-radius: 8px; padding: 10px 14px; cursor: pointer; font-weight: 700; font-size: 13.5px; }
      .omni-disclaimer-footer { padding: 6px 12px; font-size: 10.5px; color: #94A3B8; text-align: center; background: ${inputContainerBg}; border-top: 1px solid rgba(226,232,240,0.5); }
    `;
    document.head.appendChild(style);

    const bubble = document.createElement('div');
    bubble.id = 'omni-chat-bubble';
    bubble.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>';
    appendToBody(bubble);

    // Multi-Brand Dynamic Config Resolution
    const isFinnova = /finnova/.test(currentDomain);
    const isProCrm = /procrm/.test(currentDomain);
    const isEzConsultants = /ezconsultants/.test(currentDomain);

    let brandSpecialistTitle = "AI Mortgage Specialist";
    let brandIntro = "Hi, I'm Friday from <strong>EZ Mortgage Broker</strong>! Ready to see how our AI compares 50+ lenders to unlock lower rates & boost borrowing power?";
    let brandPrompts = [
      { text: "Calculate my borrowing power", prompt: "How much can I borrow on my salary?" },
      { text: "Compare 50+ bank rates", prompt: "Compare lowest 2-year fixed rates across Australian banks" },
      { text: "Latest RBA cash rate update", prompt: "What are the current RBA interest rate forecasts?" }
    ];
    let brandCtaText = "Connect me with a licensed broker &rarr;";

    if (isFinnova) {
      brandSpecialistTitle = "AI Community Guide";
      brandIntro = "Hi, I'm Friday from <strong>Finnova</strong>! I can guide you through our free refurbished digital devices, senior cyber safety workshops, and ACNC community programs.";
      brandPrompts = [
        { text: "Request free refurbished tech", prompt: "How can seniors or students request refurbished digital hardware?" },
        { text: "Senior cyber defense workshops", prompt: "When are the upcoming free cyber safety workshops?" },
        { text: "Donate tech / e-waste pickup", prompt: "How does our company donate corporate laptops and computers?" }
      ];
      brandCtaText = "Contact Finnova Community Team &rarr;";
    } else if (isProCrm) {
      brandSpecialistTitle = "AI Enterprise Architect";
      brandIntro = "Hi, I'm Friday from <strong>PRO CRM</strong>! Ready to explore how Salesforce Agentforce & Zero-ETL Data Cloud can automate your enterprise workflows?";
      brandPrompts = [
        { text: "Agentforce Autonomous AI", prompt: "How does Salesforce Agentforce differ from basic chatbots?" },
        { text: "Zero-ETL Data Cloud sync", prompt: "Explain Zero-Copy federation across Snowflake and BigQuery." },
        { text: "APRA CPS 234 Compliance", prompt: "How do you enforce security and sovereign data boundaries?" }
      ];
      brandCtaText = "Book Enterprise AI Consultation &rarr;";
    } else if (isEzConsultants) {
      brandSpecialistTitle = "AI Cyber & Cloud Advisor";
      brandIntro = "Hi, I'm Friday from <strong>EZ Consultants</strong>! I provide rapid intelligence on ACSC cybersecurity alerts, DevSecOps, and NDIS compliance frameworks.";
      brandPrompts = [
        { text: "ACSC Threat Advisory", prompt: "What are the critical ASD ACSC vulnerability advisories today?" },
        { text: "NDIS Provider Audit Defense", prompt: "How do we prepare for mid-term NDIS Quality Commission audits?" },
        { text: "Cloud Security Architecture", prompt: "How do you secure multi-cloud Kubernetes & AWS workloads?" }
      ];
      brandCtaText = "Request Cyber Advisory Call &rarr;";
    }

    const win = document.createElement('div');
    win.id = 'omni-chat-window';
    win.innerHTML = `
      <div id="omni-chat-header">
        <div class="title-wrap">
          <span class="title">Friday</span>
          <span class="badge">${brandSpecialistTitle}</span>
        </div>
        <div class="omni-hdr-actions">
          <button class="omni-btn-endchat" id="omniEndChat">✉️ Email Chat</button>
          <span id="omni-close" style="cursor:pointer; font-size: 18px; color: #64748b; padding: 2px 6px;">✕</span>
        </div>
      </div>

      <div class="piper-hero-card">
        <div class="piper-hero-video-stage">
          <video id="piper-hero-video" playsinline loop muted preload="auto" poster="/images/friday_avatar.jpeg">
            <source src="/assets/videos/friday_avatar.mp4" type="video/mp4">
            <source src="https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar.mp4" type="video/mp4">
          </video>
          <button type="button" class="piper-speak-badge-btn" id="piperSpeakBtn">
            🎙️ Speak with Friday
          </button>
        </div>
        <div class="piper-hero-intro">
          ${brandIntro}
        </div>
        <div class="piper-prompts-box">
          <div class="piper-prompts-title">Ask me things like:</div>
          ${brandPrompts.map(p => `<div class="piper-prompt-item" data-prompt="${p.prompt}">${p.text} <span>&rarr;</span></div>`).join('')}
        </div>
        <div class="piper-cta-row">
          <button type="button" class="piper-connect-btn" id="piperConnectRep">${brandCtaText}</button>
        </div>
      </div>

      <div id="omni-chat-messages">
        <!-- Messages stream here -->
      </div>
      <div id="omni-image-preview-bar">
        <img id="omniPreviewImg" src="" alt="preview" />
        <span>Attached image ready</span>
        <span id="omniRemoveImg" style="cursor:pointer; color:#ef4444; font-weight:bold; margin-left:auto;">✕</span>
      </div>
      <div id="omni-chat-input-container">
        <input type="file" id="omniFileInput" accept="image/*" style="display:none;" />
        ${config.features?.imageUpload !== false ? '<button class="omni-attach-btn" id="omniAttachBtn" title="Attach/Paste Image">📎</button>' : ''}
        <button class="omni-mic-btn" id="omniMicBtn" title="Voice Input">🎙️</button>
        <input type="text" id="omni-chat-input" placeholder="Ask Friday a question..." />
        <button id="omni-chat-send">&rarr;</button>
      </div>
      <div class="omni-disclaimer-footer">
        Friday is an AI intelligence assistant and can make mistakes. Please verify important terms with our accredited team.
      </div>
    `;
    appendToBody(win);

    // 10-Second Salesforce Piper Auto-Open Timer
    setTimeout(() => {
      if (!sessionStorage.getItem('piper_chat_dismissed')) {
        win.style.display = 'flex';
        const video = document.getElementById('piper-hero-video');
        if (video) video.play().catch(() => {});
      }
    }, 10000);

    if (getLeadScoreFromCookie() >= 35 && !window.__OMNI_PROACTIVE_TRIGGERED__) {
      window.__OMNI_PROACTIVE_TRIGGERED__ = true;
      win.style.display = 'flex';
    }

    bubble.onclick = () => {
      const isOpening = win.style.display !== 'flex';
      win.style.display = isOpening ? 'flex' : 'none';
      if (isOpening) {
        const video = document.getElementById('piper-hero-video');
        if (video) video.play().catch(() => {});
      }
    };
    document.getElementById('omni-close').onclick = () => {
      win.style.display = 'none';
      sessionStorage.setItem('piper_chat_dismissed', 'true');
    };

    // Piper Interactive Prompt Pills
    document.querySelectorAll('.piper-prompt-item').forEach(item => {
      item.onclick = () => {
        const promptText = item.getAttribute('data-prompt');
        const input = document.getElementById('omni-chat-input');
        if (input && promptText) {
          input.value = promptText;
          document.getElementById('omni-chat-send').click();
        }
      };
    });

    // Speak with Friday Button (Authentic ElevenLabs synthesized voice playback)
    let brandAudioKey = 'ezmortgage';
    if (isFinnova) brandAudioKey = 'finnova';
    else if (isProCrm) brandAudioKey = 'procrm';
    else if (isEzConsultants) brandAudioKey = 'ezconsultants';

    let fridayAudioPlayer = null;
    const speakBtn = document.getElementById('piperSpeakBtn');
    if (speakBtn) {
      speakBtn.onclick = () => {
        const video = document.getElementById('piper-hero-video');
        if (video) {
          video.muted = true; // Always keep video muted so placeholder audio is never heard
          video.play().catch(() => {});
        }

        if (fridayAudioPlayer && !fridayAudioPlayer.paused) {
          fridayAudioPlayer.pause();
          fridayAudioPlayer.currentTime = 0;
          speakBtn.innerHTML = '🎙️ Speak with Friday';
          return;
        }

        const primarySrc = `/assets/audio/friday_greeting_${brandAudioKey}.mp3`;
        const cdnSrc = `https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/audio/friday_greeting_${brandAudioKey}.mp3`;

        fridayAudioPlayer = new Audio(primarySrc);
        fridayAudioPlayer.onerror = () => {
          fridayAudioPlayer = new Audio(cdnSrc);
          fridayAudioPlayer.play();
        };

        speakBtn.innerHTML = '🔊 Friday is speaking...';
        fridayAudioPlayer.play().catch(e => console.log('Audio autoplay note:', e));

        fridayAudioPlayer.onended = () => {
          speakBtn.innerHTML = '🎙️ Speak with Friday';
        };
      };
    }

    // Connect with Broker Button
    const connectBtn = document.getElementById('piperConnectRep');
    if (connectBtn) {
      connectBtn.onclick = () => {
        const input = document.getElementById('omni-chat-input');
        if (input) {
          input.value = "I'd like to connect directly with a licensed mortgage broker for a consultation.";
          document.getElementById('omni-chat-send').click();
        }
      };
    }

    // Voice Input via Web Speech Recognition API
    const micBtn = document.getElementById('omniMicBtn');
    if (micBtn && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-AU';

      recognition.onstart = () => { micBtn.classList.add('active'); };
      recognition.onend = () => { micBtn.classList.remove('active'); };
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById('omni-chat-input');
        if (input && transcript) {
          input.value = transcript;
          document.getElementById('omni-chat-send').click();
        }
      };

      micBtn.onclick = () => {
        try { recognition.start(); } catch (e) { recognition.stop(); }
      };
    }

    const fileInput = document.getElementById('omniFileInput');
    const attachBtn = document.getElementById('omniAttachBtn');
    const previewBar = document.getElementById('omni-image-preview-bar');
    const previewImg = document.getElementById('omniPreviewImg');
    const removeImgBtn = document.getElementById('omniRemoveImg');
    const chatInput = document.getElementById('omni-chat-input');

    if (attachBtn) {
      attachBtn.onclick = () => fileInput.click();
      fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) handleImageFile(file);
      };
    }

    if (config.features?.imageUpload !== false) {
      chatInput.addEventListener('paste', (e) => {
        const items = (e.clipboardData || e.originalEvent.clipboardData).items;
        for (let item of items) {
          if (item.type.indexOf('image') === 0) {
            const blob = item.getAsFile();
            handleImageFile(blob);
          }
        }
      });
    }

    function handleImageFile(file) {
      const reader = new FileReader();
      reader.onload = (evt) => {
        attachedImageBase64 = evt.target.result;
        previewImg.src = attachedImageBase64;
        previewBar.style.display = 'flex';
      };
      reader.readAsDataURL(file);
    }

    removeImgBtn.onclick = () => {
      attachedImageBase64 = "";
      previewBar.style.display = 'none';
      if (fileInput) fileInput.value = "";
    };

    document.getElementById('omniEndChat').onclick = async () => {
      const userEmail = prompt("Enter your email address to receive the full chat transcript:", "");
      if (!userEmail || !userEmail.includes("@")) return;

      try {
        await fetch(`${backendUrl}/api/email-transcript`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            sessionId: sessionId,
            email: userEmail,
            domain: currentDomain
          })
        });
        alert(`Transcript successfully queued for ${userEmail}!`);
        sessionId = 'sess_' + Math.random().toString(36).substring(2, 9);
        localStorage.setItem('omni_chat_session', sessionId);
      } catch (err) {
        alert("Unable to export transcript.");
      }
    };

    async function sendMessage() {
      const msg = chatInput.value.trim();
      if (!msg && !attachedImageBase64) return;

      updateLeadScore(10, "Sent Message");

      const msgContainer = document.getElementById('omni-chat-messages');
      
      let userHtml = parseMarkdown(msg, primaryColor);
      if (attachedImageBase64) {
        userHtml += `<br/><img src="${attachedImageBase64}" style="max-width:180px; border-radius:6px; margin-top:6px;" />`;
      }

      const userMsgDiv = document.createElement('div');
      userMsgDiv.className = 'omni-msg user';
      userMsgDiv.innerHTML = userHtml;
      msgContainer.appendChild(userMsgDiv);

      const sentImage = attachedImageBase64;
      chatInput.value = '';
      attachedImageBase64 = "";
      previewBar.style.display = 'none';
      msgContainer.scrollTop = msgContainer.scrollHeight;

      const loadingMsg = document.createElement('div');
      loadingMsg.className = 'omni-msg assistant loading';
      loadingMsg.textContent = 'Agent is thinking...';
      msgContainer.appendChild(loadingMsg);
      msgContainer.scrollTop = msgContainer.scrollHeight;

      try {
        const response = await fetch(`${backendUrl}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: msg,
            sessionId: sessionId,
            domain: currentDomain,
            pageContext: config.features?.screenAwareness !== false ? getBrowserScreenContext() : {},
            image: sentImage
          })
        });

        const data = await response.json();
        loadingMsg.classList.remove('loading');
        
        const replyRaw = data.response || data.reply || data.error || "Received response.";
        loadingMsg.innerHTML = parseMarkdown(replyRaw, primaryColor);

        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'omni-msg-actions';
        actionsDiv.innerHTML = `
          <span class="omni-action-btn" title="Thumbs Up">👍</span>
          <span class="omni-action-btn" title="Thumbs Down">👎</span>
          <span class="omni-action-btn" title="Smiley">😊</span>
          <span class="omni-quote-btn" title="Quote reply">💬 Quote</span>
        `;
        
        actionsDiv.querySelector('.omni-quote-btn').onclick = () => {
          chatInput.value = '> "' + replyRaw.substring(0, 80).replace(/\n/g, ' ') + '..."\n';
          chatInput.focus();
        };

        actionsDiv.querySelectorAll('.omni-action-btn').forEach(btn => {
          btn.onclick = () => {
            btn.style.transform = 'scale(1.4)';
            setTimeout(() => btn.style.transform = 'scale(1)', 200);
          };
        });

        loadingMsg.appendChild(actionsDiv);

        if (config.features?.leadCapture !== false && /(demo|pricing|quote|consultation|contact sales|call me|help|booking|census|mygov)/i.test(msg)) {
          renderLeadCard(msgContainer, config);
        }
      } catch (err) {
        loadingMsg.classList.remove('loading');
        loadingMsg.textContent = "Unable to connect to AI assistant service.";
      }

      msgContainer.scrollTop = msgContainer.scrollHeight;
    }

    function renderLeadCard(container, cfg) {
      if (document.getElementById('omni-lead-form')) return;
      const card = document.createElement('div');
      card.id = 'omni-lead-form';
      card.className = 'omni-lead-card';
      const score = getLeadScoreFromCookie();
      card.innerHTML = `
        <p style="margin:0 0 8px 0; font-weight:600; color:${primaryColor};">📬 Contact / Booking Request (Lead Score: ${score})</p>
        <input type="text" id="leadName" placeholder="Your Name" />
        <input type="email" id="leadEmail" placeholder="Your Email" />
        <input type="tel" id="leadPhone" placeholder="Phone Number (Optional)" />
        <button id="submitLead">Submit Contact Request</button>
      `;
      container.appendChild(card);
      container.scrollTop = container.scrollHeight;

      document.getElementById('submitLead').onclick = async () => {
        const name = document.getElementById('leadName').value;
        const email = document.getElementById('leadEmail').value;
        const phone = document.getElementById('leadPhone').value;
        if (!name || (!email && !phone)) {
          alert("Please provide your name and an email or phone number.");
          return;
        }

        await fetch(`${backendUrl}/api/lead`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            sessionId: sessionId,
            domain: currentDomain,
            category: cfg.category,
            name: name,
            email: email,
            phone: phone,
            leadScore: getLeadScoreFromCookie(),
            notes: "Lead captured via behavioral qualification pipeline"
          })
        });

        card.innerHTML = '<p style="color:#10b981; margin:0; font-weight:600;">✅ Thank you! We will reach out shortly.</p>';
      };
    }

    document.getElementById('omni-chat-send').onclick = sendMessage;
    document.getElementById('omni-chat-input').onkeypress = (e) => { if (e.key === 'Enter') sendMessage(); };
  }
})();
