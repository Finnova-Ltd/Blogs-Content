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

    // Multi-Brand Dynamic Config Resolution
    const isFinnova = /finnova/.test(currentDomain);
    const isProCrm = /procrm|ecrm/.test(currentDomain);
    const isEzConsultants = /ezconsultants/.test(currentDomain);
    const isESignature = /esignature|ezsignature/.test(currentDomain);
    const isEzMortgage = !isFinnova && !isProCrm && !isEzConsultants && !isESignature;

    let brandSpecialistTitle = "AI Lending Specialist";
    let brandIntro = "G'day! I'm Friday, your AI Lending Specialist at <strong>EZ Mortgage Broker</strong>. I compare 30+ accredited Australian lenders to find lower interest rates, maximize your borrowing capacity, and secure fast loan approvals. How can I help you with your mortgage today?";
    let brandPillGreeting = "G'day! I'm Friday 👋 Ask me anything";
    let brandPrompts = [
      { text: "Calculate my borrowing power", prompt: "How much can I borrow on my salary?" },
      { text: "Compare 30+ bank rates", prompt: "Compare lowest 2-year fixed rates across Australian banks" },
      { text: "Latest RBA cash rate update", prompt: "What are the current RBA interest rate forecasts?" }
    ];
    let brandCtaText = "Connect me with a licensed broker &rarr;";
    let brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar_ezmortgage_poster.jpg";
    let brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_ezmortgage.mp4";

    if (isFinnova) {
      brandSpecialistTitle = "AI Community Guide";
      brandIntro = "Hello and welcome! I'm Friday, your AI Community Guide at <strong>Finnova</strong>. We are an Australian ACNC-registered charity providing free refurbished computers, digital literacy classes, and senior cyber safety workshops. How can our team support you today?";
      brandPillGreeting = "Hi! I'm Friday 👋 How can Finnova help you?";
      brandPrompts = [
        { text: "Request free refurbished tech", prompt: "How can seniors or students request refurbished digital hardware?" },
        { text: "Senior cyber defense workshops", prompt: "When are the upcoming free cyber safety workshops?" },
        { text: "Donate tech / e-waste pickup", prompt: "How does our company donate corporate laptops and computers?" }
      ];
      brandCtaText = "Contact Finnova Community Team &rarr;";
      brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar.jpeg";
      brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_finnova.mp4";
    } else if (isProCrm) {
      brandSpecialistTitle = "AI Enterprise Architect";
      brandIntro = "Hi there! I'm Friday, your AI Enterprise Architect at <strong>Pro CRM Australia</strong>. We deliver Salesforce Agentforce, Zero-ETL Data Cloud integrations, and sovereign enterprise automation. What can we build for you today?";
      brandPillGreeting = "Hi there! I'm Friday 👋 Ask me about Pro CRM";
      brandPrompts = [
        { text: "Agentforce Autonomous AI", prompt: "How does Salesforce Agentforce differ from basic chatbots?" },
        { text: "Zero-ETL Data Cloud sync", prompt: "Explain Zero-Copy federation across Snowflake and BigQuery." },
        { text: "APRA CPS 234 Compliance", prompt: "How do you enforce security and sovereign data boundaries?" }
      ];
      brandCtaText = "Book Enterprise AI Consultation &rarr;";
      brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar_procrm_poster.jpg";
      brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_procrm.mp4";
    } else if (isEzConsultants) {
      brandSpecialistTitle = "AI Cyber & Cloud Advisor";
      brandIntro = "Welcome! I'm Friday, your Cyber and Cloud Advisor at <strong>EZ Consultants</strong>. We provide rapid ASD ACSC threat intelligence, NDIS quality audit defense, and DevSecOps architecture. How can I assist you today?";
      brandPillGreeting = "Welcome! I'm Friday 👋 Ask about cyber & cloud defense";
      brandPrompts = [
        { text: "ACSC Threat Advisory", prompt: "What are the critical ASD ACSC vulnerability advisories today?" },
        { text: "NDIS Provider Audit Defense", prompt: "How do we prepare for mid-term NDIS Quality Commission audits?" },
        { text: "Cloud Security Architecture", prompt: "How do you secure multi-cloud Kubernetes & AWS workloads?" }
      ];
      brandCtaText = "Request Cyber Advisory Call &rarr;";
      brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar_ezmortgage_poster.jpg";
      brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_ezconsultants.mp4";
    } else if (isESignature) {
      brandSpecialistTitle = "AI Document Specialist";
      brandIntro = "Hi there! I'm Friday, your AI Document & Security Specialist at <strong>EZ Signature</strong>. We provide secure, legally binding electronic signatures compliant with the Australian Electronic Transactions Act 1999. How can I assist your team today?";
      brandPillGreeting = "Hi there! I'm Friday 👋 Ask about digital signatures";
      brandPrompts = [
        { text: "Australian legal validity", prompt: "How do electronic signatures comply with the Australian Electronic Transactions Act 1999?" },
        { text: "AATL tamper-evident security", prompt: "Explain AES-256 encryption and Adobe Approved Trust List audit trails." },
        { text: "Compare pricing & plans", prompt: "What are your enterprise and standard signature plan tiers?" }
      ];
      brandCtaText = "Start Free Document Trial &rarr;";
      brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar_ezmortgage_poster.jpg";
      brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_ezconsultants.mp4";
    }

    let brandKey = "ezmortgage";
    if (isFinnova) brandKey = "finnova";
    else if (isProCrm) brandKey = "procrm";
    else if (isEzConsultants) brandKey = "ezconsultants";
    else if (isESignature) brandKey = "ezsignature";

    const style = document.createElement('style');
    style.innerHTML = `
      #omni-chat-trigger-group { position: fixed; bottom: 24px; right: 24px; display: flex; align-items: center; gap: 12px; z-index: 999999; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
      .omni-avatar-greeting-pill { background: #ffffff; color: #0f172a; padding: 8px 14px; border-radius: 24px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12), 0 2px 6px rgba(0, 0, 0, 0.06); border: 1px solid rgba(0, 82, 255, 0.18); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; cursor: pointer; animation: omniPillSlideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1); transition: transform 0.2s, box-shadow 0.2s; white-space: nowrap; user-select: none; }
      .omni-avatar-greeting-pill:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(0, 82, 255, 0.2); }
      .omni-pill-wave { font-size: 16px; display: inline-block; animation: omniWaveHand 2.2s infinite ease-in-out; transform-origin: 70% 70%; }
      .omni-pill-close { color: #94a3b8; font-size: 12px; padding: 2px 4px; border-radius: 50%; transition: color 0.15s; margin-left: 2px; }
      .omni-pill-close:hover { color: #ef4444; }
      #omni-chat-bubble { position: relative; width: 66px; height: 66px; border-radius: 50%; cursor: pointer; box-shadow: 0 10px 28px rgba(0, 82, 255, 0.35); transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1); user-select: none; }
      #omni-chat-bubble:hover { transform: scale(1.08); }
      .omni-avatar-disc { width: 100%; height: 100%; border-radius: 50%; position: relative; overflow: visible; }
      .omni-avatar-face { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 3px solid #ffffff; box-sizing: border-box; display: block; background: #0A2540; }
      .omni-avatar-online-dot { position: absolute; bottom: 2px; right: 2px; width: 14px; height: 14px; background: #10B981; border: 2.5px solid #ffffff; border-radius: 50%; box-shadow: 0 0 8px rgba(16, 185, 129, 0.8); }
      .omni-avatar-wave-badge { position: absolute; top: -4px; right: -4px; width: 24px; height: 24px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18); animation: omniWaveHand 2.2s infinite ease-in-out; transform-origin: 70% 70%; }
      @keyframes omniWaveHand { 0%, 100% { transform: rotate(0deg); } 15% { transform: rotate(18deg) scale(1.15); } 30% { transform: rotate(-14deg) scale(1.15); } 45% { transform: rotate(14deg) scale(1.15); } 60% { transform: rotate(-8deg) scale(1.15); } 75% { transform: rotate(10deg) scale(1.1); } }
      @keyframes omniPillSlideIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
      .omni-avatar-close-icon { display: none; width: 100%; height: 100%; border-radius: 50%; background: #0f172a; color: #ffffff; font-size: 22px; align-items: center; justify-content: center; border: 3px solid #ffffff; box-sizing: border-box; }
      #omni-chat-bubble.is-open .omni-avatar-disc { display: none; }
      #omni-chat-bubble.is-open .omni-avatar-close-icon { display: flex; }
      #omni-chat-bubble.is-open { box-shadow: 0 8px 24px rgba(15, 23, 42, 0.35); }
      @media (max-width: 640px) { .omni-avatar-greeting-pill { display: none !important; } #omni-chat-bubble { width: 58px; height: 58px; } #omni-chat-trigger-group { bottom: 16px; right: 16px; } }

      #omni-chat-window { position: fixed; bottom: 96px; right: 24px; width: 395px; height: auto; min-height: 480px; max-height: calc(100vh - 110px); background: ${winBg} !important; color: ${winText} !important; border-radius: 20px; box-shadow: 0 20px 50px -5px rgba(0,0,0,0.22); display: none; flex-direction: column; overflow: hidden; z-index: 999999; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; border: 1px solid ${winBorder}; transition: width 0.3s ease, height 0.3s ease; }
      #omni-chat-window.is-conversing { height: 640px; }
      #omni-chat-window.is-expanded { width: 490px; }
      
      #omni-chat-header { background: #ffffff !important; color: #0f172a !important; padding: 12px 16px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid ${winBorder}; }
      #omni-chat-header .title-wrap { display: flex; align-items: center; gap: 8px; }
      #omni-chat-header span.title { font-size: 15px; font-weight: 800; color: #0A2540; }
      #omni-chat-header span.badge { font-size: 11px; color: #64748b; font-weight: 600; background: #F1F5F9; padding: 2px 8px; border-radius: 999px; }
      .omni-hdr-actions { display: flex; gap: 8px; align-items: center; }
      .omni-btn-endchat { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; padding: 4px 8px; border-radius: 6px; font-size: 11px; cursor: pointer; font-weight: 600; }
      .omni-btn-endchat:hover { background: #E2E8F0; color: #0f172a; }

      /* Salesforce Piper Avatar Card matching Image 1 */
      .piper-hero-card { margin: 12px 14px 6px; border-radius: 16px; overflow: hidden; background: #ffffff; position: relative; }
      .piper-hero-video-stage { position: relative; width: 100%; height: 210px; background: #0A2540; border-radius: 14px; overflow: hidden; transition: height 0.3s ease; }
      #omni-chat-window.is-expanded .piper-hero-video-stage { height: 275px; }
      .piper-hero-video-stage video { width: 100%; height: 100%; object-fit: cover; display: block; }
      
      /* Centered Prominent Speak Now Pill Button (Image 1) */
      .piper-speak-now-btn { position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); background: #0066f5; color: #ffffff; font-size: 13.5px; font-weight: 700; padding: 7px 20px; border-radius: 999px; border: none; cursor: pointer; box-shadow: 0 4px 14px rgba(0, 102, 245, 0.45); display: flex; align-items: center; gap: 6px; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); z-index: 10; white-space: nowrap; }
      .piper-speak-now-btn:hover { background: #0052cc; transform: translateX(-50%) scale(1.05); }
      .piper-speak-now-btn.speaking { background: #10B981; }

      /* Video Call Controls Bar (Image 2 & 3) - Floating top-right HUD so video captions are 100% visible */
      .piper-call-bar { position: absolute; top: 10px; right: 12px; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); padding: 4px 10px; border-radius: 999px; display: none; align-items: center; gap: 8px; z-index: 10; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35); }
      .piper-ctrl-btn { background: transparent; border: none; color: #ffffff; font-size: 15px; padding: 4px 6px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: color 0.15s; }
      .piper-ctrl-btn.active { color: #10B981; animation: omniMicPulse 1.5s infinite; }
      .piper-ctrl-btn.muted { color: #ef4444; }
      .piper-ctrl-end { background: #ef4444; color: #ffffff; font-size: 11.5px; font-weight: 700; padding: 4px 10px; border-radius: 999px; border: none; cursor: pointer; margin-left: 2px; transition: background 0.15s; }
      .piper-ctrl-end:hover { background: #dc2626; }

      /* Welcome Card Text & Full-Width CTA (Image 1) */
      .piper-card-welcome { padding: 14px 4px 4px; }
      .piper-card-intro { font-size: 13.5px; color: #1E293B; line-height: 1.48; font-weight: 500; margin: 0 0 14px; }
      .piper-connect-btn-full { width: 100%; background: #0066f5; color: #ffffff; border: none; padding: 11px 16px; border-radius: 8px; font-weight: 700; font-size: 13.5px; cursor: pointer; transition: background 0.2s; box-shadow: 0 2px 6px rgba(0, 102, 245, 0.25); margin-bottom: 8px; }
      .piper-connect-btn-full:hover { background: #0052cc; }

      /* Conversation Mode Toggling */
      #omni-chat-window.is-conversing .piper-card-welcome { display: none !important; }
      #omni-chat-window.is-conversing #omni-chat-messages { display: flex !important; }
      #omni-chat-window.is-conversing .piper-prompts-tray { display: block !important; }
      #omni-chat-window.is-conversing .piper-speak-now-btn { display: none !important; }
      #omni-chat-window.is-conversing .piper-call-bar { display: flex !important; }
      #omni-chat-window.is-conversing #piperConnectRepSub { display: none !important; }

      #omni-chat-messages { flex: 1; padding: 10px 14px; overflow-y: auto; display: none; flex-direction: column; gap: 8px; font-size: 13.5px; background: ${msgAreaBg} !important; min-height: 140px; }
      .omni-msg { padding: 9px 13px; border-radius: 12px; max-width: 88%; word-break: break-word; line-height: 1.48; }
      .omni-msg.user { background: ${primaryColor} !important; color: #ffffff !important; align-self: flex-end; border-bottom-right-radius: 3px; }
      .omni-msg.assistant { background: ${assistantBg} !important; color: ${assistantText} !important; align-self: flex-start; border-bottom-left-radius: 3px; border: 1px solid ${assistantBorder}; }
      .omni-msg.loading { color: #64748b; font-style: italic; }
      .omni-msg-actions { display: flex; gap: 8px; margin-top: 6px; font-size: 12px; opacity: 0.8; }
      .omni-action-btn { cursor: pointer; user-select: none; transition: transform 0.1s; }
      .omni-action-btn:hover { transform: scale(1.2); }

      /* Prompts Tray (Image 2 & 3) */
      .piper-prompts-tray { padding: 4px 14px 6px; font-size: 12px; }
      .piper-prompts-title { font-weight: 700; color: #64748B; margin-bottom: 4px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
      .piper-prompts-list { display: flex; flex-direction: column; gap: 4px; max-height: 90px; overflow-y: auto; }
      .piper-prompt-item { padding: 5px 8px; background: #ffffff; border: 1px solid #CBD5E1; border-radius: 6px; color: #0A2540; font-weight: 600; cursor: pointer; transition: all 0.15s; display: flex; align-items: center; justify-content: space-between; font-size: 11.5px; }
      .piper-prompt-item:hover { background: #EFF6FF; border-color: #93C5FD; color: #0052FF; transform: translateX(2px); }
      .piper-connect-btn-sub { width: 100%; background: #0066f5; color: #ffffff; border: none; padding: 7px 12px; border-radius: 6px; font-weight: 700; font-size: 12px; cursor: pointer; margin-top: 6px; transition: background 0.15s; }
      .piper-connect-btn-sub:hover { background: #0052cc; }

      /* Lead Form Styling Parity */
      .omni-lead-card { background: #F8FAFC !important; border: 1px solid #CBD5E1 !important; border-radius: 12px; padding: 12px; margin: 8px 0; display: flex; flex-direction: column; gap: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
      .omni-lead-card p { margin: 0 0 2px; font-size: 12px; font-weight: 700; color: #0f172a; }
      .omni-lead-card input { width: 100%; box-sizing: border-box; padding: 8px 10px; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 12.5px; outline: none; background: #ffffff !important; color: #0f172a !important; }
      .omni-lead-card input:focus { border-color: #0066f5; }
      .omni-lead-card button { width: 100%; background: #0066f5; color: #ffffff; border: none; padding: 9px 12px; border-radius: 6px; font-size: 12.5px; font-weight: 700; cursor: pointer; transition: background 0.15s; }
      .omni-lead-card button:hover { background: #0052cc; }

      #omni-image-preview-bar { display: none; padding: 6px 12px; background: ${inputContainerBg}; border-top: 1px solid ${winBorder}; align-items: center; gap: 8px; font-size: 12px; }
      #omni-image-preview-bar img { height: 36px; border-radius: 4px; border: 1px solid ${inputBorder}; }
      
      /* Input Box Container (Matching Image 1) */
      #omni-chat-input-container { display: flex; border: 1px solid #CBD5E1; border-radius: 8px; margin: 4px 14px 8px; padding: 3px 6px; background: #ffffff !important; gap: 4px; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
      #omni-chat-input { flex: 1; background: transparent !important; border: none !important; padding: 8px 6px; outline: none; color: #0f172a !important; font-size: 13.5px; }
      .omni-attach-btn { background: transparent; border: none; color: #64748b; font-size: 17px; cursor: pointer; padding: 3px; }
      .omni-mic-btn { background: transparent; border: none; color: #64748b; font-size: 16px; cursor: pointer; padding: 3px; transition: transform 0.2s; }
      .omni-mic-btn.active { color: #ef4444; animation: omniMicPulse 1s infinite; }
      @keyframes omniMicPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
      #omni-chat-send { background: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0; border-radius: 6px; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-weight: 700; font-size: 14px; transition: all 0.15s; }
      #omni-chat-send:hover { background: #0066f5; color: #ffffff; border-color: #0066f5; }
      .omni-disclaimer-footer { padding: 6px 14px 12px; font-size: 10.5px; color: #94A3B8; text-align: center; line-height: 1.4; }
    `;
    document.head.appendChild(style);

    const triggerGroup = document.createElement('div');
    triggerGroup.id = 'omni-chat-trigger-group';
    triggerGroup.innerHTML = `
      <div id="omni-chat-greeting-pill" class="omni-avatar-greeting-pill">
        <span class="omni-pill-wave">👋</span>
        <span class="omni-pill-text">${brandPillGreeting}</span>
        <span class="omni-pill-close" id="omniPillClose" title="Dismiss">✕</span>
      </div>
      <div id="omni-chat-bubble" class="omni-avatar-trigger" title="Chat with Friday">
        <div class="omni-avatar-disc">
          <img src="${brandPoster}" alt="Friday AI Avatar" class="omni-avatar-face" />
          <span class="omni-avatar-online-dot"></span>
          <span class="omni-avatar-wave-badge">👋</span>
        </div>
        <div class="omni-avatar-close-icon">✕</div>
      </div>
    `;
    appendToBody(triggerGroup);
    const bubble = document.getElementById('omni-chat-bubble');
    const greetingPill = document.getElementById('omni-chat-greeting-pill');

    const win = document.createElement('div');
    win.id = 'omni-chat-window';
    win.innerHTML = `
      <div id="omni-chat-header">
        <div class="title-wrap">
          <span class="title">Friday</span>
          <span class="badge">${brandSpecialistTitle}</span>
        </div>
        <div class="omni-hdr-actions">
          <button class="omni-btn-endchat" id="omniEndChat" title="Email Transcript">✉️ Email</button>
          <span id="omni-close" style="cursor:pointer; font-size: 18px; color: #64748b; padding: 2px 6px;">✕</span>
        </div>
      </div>

      <div class="piper-hero-card">
        <div class="piper-hero-video-stage" id="piperVideoStage">
          <video id="piper-hero-video" playsinline muted preload="auto" poster="${brandPoster}">
            <source src="${brandVideo}" type="video/mp4">
          </video>
          <!-- Prominent Centered Speak Now Button (Image 1) -->
          <button type="button" class="piper-speak-now-btn" id="piperSpeakBtn">
            <span>🎙️</span> Speak now
          </button>
          <!-- Video Call Controls Bar (Image 2 & 3) -->
          <div class="piper-call-bar" id="piperCallBar">
            <button type="button" class="piper-ctrl-btn" id="piperMicToggle" title="Microphone Mute/Unmute">🎙️</button>
            <button type="button" class="piper-ctrl-btn" id="piperExpandBtn" title="Expand Stage">⤢</button>
            <button type="button" class="piper-ctrl-end" id="piperEndBtn" title="End Voice Conversation">End</button>
          </div>
        </div>

        <!-- Initial Welcome Card Body (Image 1) -->
        <div class="piper-card-welcome" id="piperCardWelcome">
          <div class="piper-card-intro">
            ${brandIntro}
          </div>
          <button type="button" class="piper-connect-btn-full" id="piperConnectRep">${brandCtaText}</button>
        </div>
      </div>

      <!-- Dialogue Message Stream (Image 2 & 3) -->
      <div id="omni-chat-messages">
        <!-- Messages stream here -->
      </div>

      <!-- Prompts Tray (Image 2 & 3) -->
      <div class="piper-prompts-tray" id="piperPromptsTray">
        <div class="piper-prompts-title">Ask me things like:</div>
        <div class="piper-prompts-list">
          ${brandPrompts.map(p => `<div class="piper-prompt-item" data-prompt="${p.prompt}">${p.text} <span>&rarr;</span></div>`).join('')}
        </div>
        <button type="button" class="piper-connect-btn-sub" id="piperConnectRepSub">${brandCtaText}</button>
      </div>

      <div id="omni-image-preview-bar">
        <img id="omniPreviewImg" src="" alt="preview" />
        <span>Attached image ready</span>
        <span id="omniRemoveImg" style="cursor:pointer; color:#ef4444; font-weight:bold; margin-left:auto;">✕</span>
      </div>

      <!-- Unified Ask Input Box (Matching Image 1) -->
      <div id="omni-chat-input-container">
        <input type="file" id="omniFileInput" accept="image/*" style="display:none;" />
        ${config.features?.imageUpload !== false ? '<button class="omni-attach-btn" id="omniAttachBtn" title="Attach Image">📎</button>' : ''}
        <input type="text" id="omni-chat-input" placeholder="Ask Friday a question" />
        <button class="omni-mic-btn" id="omniMicBtn" title="Speak with Friday">🎙️</button>
        <button id="omni-chat-send" title="Send message">&rarr;</button>
      </div>

      <div class="omni-disclaimer-footer">
        Friday is an AI and can make mistakes. Please note, by continuing, you agree to the terms of our privacy policy. This conversation will be recorded.
      </div>
    `;
    appendToBody(win);

    function openChat() {
      win.style.display = 'flex';
      if (bubble) bubble.classList.add('is-open');
      if (greetingPill) greetingPill.style.display = 'none';
      const video = document.getElementById('piper-hero-video');
      if (video) {
        video.muted = true;
        video.defaultMuted = true;
        video.volume = 0;
      }
    }

    function closeChat() {
      win.style.display = 'none';
      if (bubble) bubble.classList.remove('is-open');
      sessionStorage.setItem('piper_chat_dismissed', 'true');
      if (greetingPill && !sessionStorage.getItem('omni_pill_dismissed')) {
        greetingPill.style.display = 'flex';
      }
    }

    // 10-Second Salesforce Piper Auto-Open Timer
    setTimeout(() => {
      if (!sessionStorage.getItem('piper_chat_dismissed')) {
        openChat();
      }
    }, 10000);

    if (getLeadScoreFromCookie() >= 35 && !window.__OMNI_PROACTIVE_TRIGGERED__) {
      window.__OMNI_PROACTIVE_TRIGGERED__ = true;
      openChat();
    }

    if (bubble) {
      bubble.onclick = () => {
        if (win.style.display !== 'flex') {
          openChat();
        } else {
          closeChat();
        }
      };
    }

    if (greetingPill) {
      greetingPill.onclick = (e) => {
        if (e.target.id === 'omniPillClose') {
          e.stopPropagation();
          greetingPill.style.display = 'none';
          sessionStorage.setItem('omni_pill_dismissed', 'true');
          return;
        }
        openChat();
      };
    }

    const closeBtn = document.getElementById('omni-close');
    if (closeBtn) closeBtn.onclick = closeChat;

    // Piper Interactive Prompt Pills (Click to instantly query AI)
    document.querySelectorAll(".piper-prompt-item").forEach(item => {
      item.onclick = (e) => {
        e.preventDefault();
        const promptText = item.getAttribute("data-prompt");
        const input = document.getElementById("omni-chat-input");
        if (input && promptText) {
          input.value = promptText;
          sendMessage();
        }
      };
    });

    // Voice & Conversational AI Engine (Salesforce Piper Parity)
    let isVoiceActive = false;
    let isSpeaking = false;
    let recognition = null;
    let isListening = false;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    const speakBtn = document.getElementById("piperSpeakBtn");
    const video = document.getElementById("piper-hero-video");
    const callBar = document.getElementById("piperCallBar");
    const micToggle = document.getElementById("piperMicToggle");
    const expandBtn = document.getElementById("piperExpandBtn");
    const endBtn = document.getElementById("piperEndBtn");
    const micBtn = document.getElementById("omniMicBtn");

    if (video) {
      video.muted = true;
      video.defaultMuted = true;
      video.volume = 0;
      video.addEventListener('volumechange', () => {
        if (!video.muted || video.volume > 0) {
          video.muted = true;
          video.volume = 0;
        }
      });
    }

    function getAuVoice() {
      if (!('speechSynthesis' in window)) return null;
      const voices = window.speechSynthesis.getVoices();
      return voices.find(v => v.lang === 'en-AU' && (v.name.includes('Natural') || v.name.includes('Russell') || v.name.includes('Lee')))
        || voices.find(v => v.lang === 'en-AU')
        || voices.find(v => v.lang.startsWith('en') && v.name.includes('Natural'))
        || voices.find(v => v.lang.startsWith('en')) || null;
    }

    if ('speechSynthesis' in window) {
      window.speechSynthesis.onvoiceschanged = () => getAuVoice();
    }

    let currentVoiceAudio = null;
    let currentSpeechId = 0;

    function stopSpeaking() {
      currentSpeechId++;
      isSpeaking = false;
      if (currentVoiceAudio) {
        try {
          currentVoiceAudio.onended = null;
          currentVoiceAudio.onerror = null;
          currentVoiceAudio.pause();
          currentVoiceAudio.currentTime = 0;
          currentVoiceAudio.src = "";
        } catch(e) {}
        currentVoiceAudio = null;
      }
      if ('speechSynthesis' in window) {
        try { window.speechSynthesis.cancel(); } catch(e) {}
      }
      if (video) {
        video.loop = false;
        video.pause();
        video.currentTime = 0;
      }
    }

    function fallbackBrowserSpeech(cleanText, onComplete, speechId) {
      if (!('speechSynthesis' in window) || (speechId !== undefined && speechId !== currentSpeechId)) {
        if (onComplete) onComplete();
        return;
      }
      try { window.speechSynthesis.cancel(); } catch(e) {}
      const utter = new SpeechSynthesisUtterance(cleanText);
      utter.rate = 1.05;
      utter.pitch = 1.0;
      const voice = getAuVoice();
      if (voice) utter.voice = voice;
      
      if (video) {
        video.muted = true;
        video.defaultMuted = true;
        video.volume = 0;
        video.currentTime = 0;
        video.loop = true;
        video.play().catch(() => {});
      }

      utter.onend = () => {
        if (speechId !== undefined && speechId !== currentSpeechId) return;
        isSpeaking = false;
        if (video) {
          video.loop = false;
          video.pause();
          video.currentTime = 0;
        }
        if (onComplete) onComplete();
      };
      utter.onerror = () => {
        if (speechId !== undefined && speechId !== currentSpeechId) return;
        isSpeaking = false;
        if (video) {
          video.loop = false;
          video.pause();
          video.currentTime = 0;
        }
        if (onComplete) onComplete();
      };
      window.speechSynthesis.speak(utter);
    }

    function getPreRenderedGreetingUrl() {
      if (isProCrm) {
        return "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/audio/friday_greeting_procrm.mp3";
      } else if (isFinnova) {
        return "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/audio/friday_greeting_finnova.mp3";
      } else if (isEzConsultants) {
        return "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/audio/friday_greeting_ezconsultants.mp3";
      } else if (isEzMortgage) {
        return "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/audio/friday_greeting_ezmortgage.mp3";
      }
      return null;
    }

    async function speakFriday(text, onComplete, isGreeting = false) {
      stopSpeaking();

      const clean = text
        .replace(/<[^>]+>/g, ' ')
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
        .replace(/[*_#`~]/g, '')
        .replace(/\bPRO\s+CRM\b/gi, 'Pro CRM')
        .trim();

      if (!clean) {
        if (onComplete) onComplete();
        return;
      }

      const speechId = currentSpeechId;
      isSpeaking = true;
      if (video) {
        video.muted = true;
        video.defaultMuted = true;
        video.volume = 0;
        video.currentTime = 0;
        video.loop = true; // Actively move lips and head throughout speech
        video.play().catch(() => {});
      }

      const handleSpeechEnd = () => {
        if (speechId !== currentSpeechId) return;
        isSpeaking = false;
        if (video) {
          video.loop = false;
          video.pause();
          video.currentTime = 0;
        }
        if (onComplete) onComplete();
        // Automatically open mic for user to speak when Friday finishes talking
        if (isVoiceActive || win.classList.contains('is-conversing')) {
          setTimeout(() => {
            if (!isSpeaking) startListening();
          }, 350);
        }
      };

      // FAST-PATH: ONLY play pre-rendered audio for the initial greeting!
      // NEVER trigger the cached greeting for normal answers to user questions!
      if (isGreeting) {
        const cachedGreetingUrl = getPreRenderedGreetingUrl();
        if (cachedGreetingUrl) {
          try {
            currentVoiceAudio = new Audio(cachedGreetingUrl);
            currentVoiceAudio.onended = handleSpeechEnd;
            currentVoiceAudio.onerror = () => {
              if (speechId === currentSpeechId) {
                fetchTtsAndPlay(clean, onComplete, speechId);
              }
            };
            await currentVoiceAudio.play();
            return;
          } catch (err) {
            console.log("Cached greeting playback note:", err);
            // DO NOT fall through to fetchTtsAndPlay if user aborted/paused
            return;
          }
        }
      }

      await fetchTtsAndPlay(clean, onComplete, speechId);
    }

    async function fetchTtsAndPlay(cleanText, onComplete, speechId) {
      if (speechId !== currentSpeechId) return;
      // Dynamic High-Fidelity Ultra-Realistic ElevenLabs Neural Voice
      try {
        const res = await fetch(`${backendUrl}/api/tts`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: cleanText, domain: currentDomain })
        });

        if (speechId !== currentSpeechId) return;

        if (res.ok) {
          const blob = await res.blob();
          if (speechId !== currentSpeechId) return;

          const audioUrl = URL.createObjectURL(blob);
          currentVoiceAudio = new Audio(audioUrl);

          currentVoiceAudio.onended = () => {
            if (speechId !== currentSpeechId) return;
            isSpeaking = false;
            if (video) {
              video.loop = false;
              video.pause();
              video.currentTime = 0;
            }
            if (onComplete) onComplete();
          };

          currentVoiceAudio.onerror = () => {
            if (speechId !== currentSpeechId) return;
            isSpeaking = false;
            if (video) {
              video.loop = false;
              video.pause();
              video.currentTime = 0;
            }
            if (onComplete) onComplete();
          };

          await currentVoiceAudio.play();
          return;
        }
      } catch (err) {
        console.log("ElevenLabs audio streaming note:", err);
      }

      // Fallback to browser synthesis only if this speech is still the active one
      if (speechId === currentSpeechId) {
        fallbackBrowserSpeech(cleanText, onComplete, speechId);
      }
    }

    function startListening() {
      if (!recognition) return;
      if (isSpeaking) {
        stopSpeaking();
      }
      isVoiceActive = true;
      if (isListening) return;
      try {
        recognition.start();
      } catch (err) {
        console.log("Speech recognition start note:", err);
      }
    }

    function stopListening() {
      if (recognition && isListening) {
        try { recognition.stop(); } catch(e) {}
      }
      isListening = false;
      if (micBtn) micBtn.classList.remove("active");
      if (micToggle) {
        micToggle.classList.remove("active");
        micToggle.classList.add("muted");
      }
      const input = document.getElementById("omni-chat-input");
      if (input && input.placeholder.includes("Listening")) {
        input.placeholder = "Ask Friday a question";
      }
    }

    function startVoiceConversation() {
      isVoiceActive = true;
      win.classList.add('is-conversing');
      
      const msgContainer = document.getElementById('omni-chat-messages');
      const greetingFullText = brandIntro.replace(/<[^>]+>/g, " ").trim();

      if (msgContainer && msgContainer.children.length === 0) {
        const greetDiv = document.createElement('div');
        greetDiv.className = 'omni-msg assistant';
        greetDiv.innerHTML = brandIntro;
        msgContainer.appendChild(greetDiv);
        msgContainer.scrollTop = 0;
      }

      // Play exact brand greeting aloud with animated lipsync (isGreeting = true)
      speakFriday(greetingFullText, () => {
        if (isVoiceActive) startListening();
      }, true);
    }

    function endVoiceConversation() {
      isVoiceActive = false;
      stopListening();
      stopSpeaking();
      win.classList.remove('is-conversing');
    }

    if (speakBtn) speakBtn.onclick = startVoiceConversation;
    if (endBtn) endBtn.onclick = endVoiceConversation;
    if (expandBtn) {
      expandBtn.onclick = () => win.classList.toggle('is-expanded');
    }
    if (micToggle) {
      micToggle.onclick = () => {
        if (isListening) {
          stopListening();
        } else {
          isVoiceActive = true;
          win.classList.add('is-conversing');
          stopSpeaking();
          startListening();
        }
      };
    }

    // Connect with Sales Rep / Broker Buttons
    const handleConnectClick = () => {
      const input = document.getElementById('omni-chat-input');
      if (input) {
        win.classList.add('is-conversing');
        input.value = isProCrm 
          ? "I'd like to book an enterprise consultation with a Pro CRM architect." 
          : "I'd like to connect directly with a licensed specialist for a consultation.";
        document.getElementById('omni-chat-send').click();
      }
    };
    const connectBtn = document.getElementById('piperConnectRep');
    if (connectBtn) connectBtn.onclick = handleConnectClick;
    const connectBtnSub = document.getElementById('piperConnectRepSub');
    if (connectBtnSub) connectBtnSub.onclick = handleConnectClick;

    // Web Speech Recognition Initialization
    if (SpeechRecognition) {
      try {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-AU";

        let silenceTimer = null;

        recognition.onstart = () => {
          isListening = true;
          if (micBtn) micBtn.classList.add("active");
          if (micToggle) {
            micToggle.classList.remove("muted");
            micToggle.classList.add("active");
          }
          const input = document.getElementById("omni-chat-input");
          if (input && !input.value) input.placeholder = "🎙️ Listening... speak now";
        };

        recognition.onend = () => {
          isListening = false;
          if (micBtn) micBtn.classList.remove("active");
          if (micToggle) {
            micToggle.classList.remove("active");
            micToggle.classList.add("muted");
          }
          const input = document.getElementById("omni-chat-input");
          if (input && input.placeholder.includes("Listening")) {
            input.placeholder = "Ask Friday a question";
          }
          // Bidirectional voice loop: Auto-restart listening if voice conversation is active and Friday isn't speaking
          if ((isVoiceActive || win.classList.contains('is-conversing')) && !isSpeaking) {
            setTimeout(() => {
              if (!isSpeaking && !isListening && (isVoiceActive || win.classList.contains('is-conversing'))) {
                startListening();
              }
            }, 300);
          }
        };

        recognition.onerror = (e) => {
          if (e.error === 'no-speech') {
            // Normal silence timeout while listening, do not crash or log loud error
            return;
          }
          if (e.error === 'not-allowed') {
            console.warn("Microphone access blocked.");
            isVoiceActive = false;
          }
          isListening = false;
          if (micBtn) micBtn.classList.remove("active");
          if (micToggle) {
            micToggle.classList.remove("active");
            micToggle.classList.add("muted");
          }
        };

        recognition.onresult = (event) => {
          let interimTranscript = '';
          let finalTranscript = '';

          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript;
            } else {
              interimTranscript += event.results[i][0].transcript;
            }
          }

          const input = document.getElementById("omni-chat-input");
          const liveText = (finalTranscript || interimTranscript).trim();
          if (input && liveText) {
            input.value = liveText;
          }

          if (finalTranscript.trim()) {
            clearTimeout(silenceTimer);
            silenceTimer = setTimeout(() => {
              if (input && input.value.trim()) {
                win.classList.add('is-conversing');
                stopListening();
                sendMessage();
              }
            }, 800);
          }
        };

        if (micBtn) {
          micBtn.onclick = () => {
            if (isListening) {
              stopListening();
            } else {
              isVoiceActive = true;
              win.classList.add('is-conversing');
              stopSpeaking();
              startListening();
            }
          };
        }
      } catch (err) {
        console.log("Speech setup note:", err);
      }
    } else if (micBtn) {
      micBtn.onclick = () => {
        alert("Voice speech recognition is supported in Chrome, Safari, and Edge.");
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
      // Immediately stop any active audio, speech synthesis, or speaking state so questions never overlap with greetings
      stopSpeaking();
      stopListening();

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

        if (isVoiceActive || win.classList.contains('is-conversing')) {
          isVoiceActive = true;
          speakFriday(replyRaw, () => {
            if (isVoiceActive) {
              startListening();
            }
          }, false);
        }

        if (config.features?.leadCapture !== false && /(demo|pricing|quote|consultation|contact sales|call me|help|booking|census|mygov)/i.test(msg)) {
          renderLeadCard(msgContainer, config);
        }
      } catch (err) {
        loadingMsg.classList.remove('loading');
        loadingMsg.textContent = "Unable to connect to AI assistant service.";
        if (isVoiceActive || win.classList.contains('is-conversing')) {
          isVoiceActive = true;
          speakFriday("I'm sorry, I'm having trouble connecting right now. Please feel free to try again.", () => {
            if (isVoiceActive) startListening();
          }, false);
        }
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
