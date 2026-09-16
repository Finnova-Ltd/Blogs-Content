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
      // Default remains minimized - do not force open window
    }
  }

  function getResolvedTheme(explicitTheme) {
    if (explicitTheme === 'dark') return 'dark';
    if (explicitTheme === 'light') return 'light';

    const html = document.documentElement;
    const body = document.body;
    const isDomDark = 
      (html && html.classList && html.classList.contains('dark')) || 
      (body && body.classList && body.classList.contains('dark')) || 
      (html && html.getAttribute && html.getAttribute('data-theme') === 'dark') || 
      (body && body.getAttribute && body.getAttribute('data-theme') === 'dark') ||
      (html && html.getAttribute && html.getAttribute('color-scheme') === 'dark');

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

    let isVoiceActive = false;
    let isSpeaking = false;
    let recognition = null;
    let isListening = false;
    let currentVoiceAudio = null;
    let currentSpeechId = 0;
    let win = null;

    const EZ_MORTGAGE_CANNED_CONCEPTS = [
      {
        id: "concept-1-fees",
        chip: "💳 How do your fees and commissions work?",
        keywords: ["fee", "fees", "commission", "commissions", "how do your fees", "compensated", "cost", "charge", "pay you"],
        title: "Broker Fees & Commissions (Transparency & Trust)",
        duration: "~10–11 seconds",
        localVideo: "/assets/videos/concept_1_fees.mp4",
        localPoster: "/images/concept_1_fees_poster.jpg",
        videoUrl: "https://share.gemini.google/JZ01AoekO0Ny",
        script: "We're compensated via lender commissions, though a fee may apply depending on your loan's complexity. Everything is disclosed upfront, and we're legally bound to act in your best interests!"
      },
      {
        id: "concept-2-borrowing",
        chip: "📈 How much can I borrow, and how fast is approval?",
        keywords: ["borrow", "borrowing", "capacity", "how much can i borrow", "how fast is approval", "fast loan approvals", "qualify", "borrowing power"],
        title: "Borrowing Power & Speed (Action & Encouragement)",
        duration: "~10 seconds",
        localVideo: "/assets/videos/concept_2_borrowing.mp4",
        localPoster: "/images/concept_2_borrowing_poster.jpg",
        videoUrl: "https://share.gemini.google/98xInqAFLLrm",
        script: "Every lender assesses borrowing capacity differently! We compare multiple lenders to maximise your borrowing power and secure fast loan approvals. Ready to see what you qualify for?"
      },
      {
        id: "concept-3-refinancing",
        chip: "🔄 Could I be saving money on my current mortgage?",
        keywords: ["saving", "saving money", "current mortgage", "refinance", "refinancing", "lower rates", "overpaying", "health check"],
        title: "Refinancing & Savings (Solving Pain Points)",
        duration: "~10 seconds",
        localVideo: "/assets/videos/concept_3_refinancing.mp4",
        localPoster: "/images/concept_3_refinancing_poster.jpg",
        videoUrl: "https://share.gemini.google/Gn6TIIKibsT7",
        script: "If you haven't reviewed your rate recently, you might be overpaying. We compare multiple lenders to find lower rates and trim your repayments. Let's run a quick health check!"
      }
    ];

    let brandAvatarName = "Friday";
    let brandSpecialistTitle = "AI Lending Specialist";
    let brandIntro = "G'day! I'm Friday, your AI Lending Specialist at <strong>EZ Mortgage Broker</strong>. I compare 30+ accredited Australian lenders to find lower interest rates, maximize your borrowing capacity, and secure fast loan approvals. How can I help you with your mortgage today?";
    let brandPillGreeting = "G'day! I'm Friday 👋 Ask me anything";
    let brandPrompts = [
      { text: "💳 Fees & Commissions", prompt: "How do your fees and commissions work?" },
      { text: "📈 Borrowing Power & Speed", prompt: "How much can I borrow, and how fast is approval?" },
      { text: "🔄 Refinancing & Savings", prompt: "Could I be saving money on my current mortgage?" }
    ];
    let brandCtaText = "Connect me with a licensed broker &rarr;";
    let brandPoster = "/images/gemini_chat_avatar_poster.jpg";
    let brandVideo = "/assets/videos/gemini_chat_avatar.mp4";
    let brandPipVideo = brandVideo;
    let brandPipPoster = brandPoster;
    let brandIntroVideoUrl = "https://share.gemini.google/w0iGnx8e65Lk";
    let brandVideoId = "";
    let brandBadgeName = "EZ MORTGAGE BROKER";
    let brandBadgeColor = "#3b82f6";
    let brandVoiceId = "Dh68koMHNSYl8A1jH9Je";
    let brandAvatarId = null;

    if (isFinnova) {
      brandAvatarName = "Friday";
      brandSpecialistTitle = "AI Community Guide";
      brandIntro = "Hello and welcome! I'm Friday, your AI Community Guide at <strong>Finnova</strong>. We are an Australian ACNC-registered charity providing free refurbished computers, digital literacy classes, and senior cyber safety workshops. How can our team support you today?";
      brandPillGreeting = "Hi! I'm Friday 👋 How can Finnova help you?";
      brandPrompts = [
        { text: "Request free refurbished tech", prompt: "How can seniors or students request refurbished digital hardware?" },
        { text: "Senior cyber defense workshops", prompt: "When are the upcoming free cyber safety workshops?" },
        { text: "Donate tech / e-waste pickup", prompt: "How does our company donate corporate laptops and computers?" }
      ];
      brandCtaText = "Contact Finnova Community Team &rarr;";
      brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar_female_poster.jpg";
      brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_female.mp4";
      brandPipVideo = brandVideo;
      brandPipPoster = brandPoster;
      brandVideoId = "j5ck0gcoPY3vyiBPJy6h";
      brandBadgeName = "FINNOVA CHARITY";
      brandBadgeColor = "#ec4899";
      brandVoiceId = "7xOqQceOZC5dhvkaqKtD";
      brandAvatarId = "j5ck0gcoPY3vyiBPJy6h";
    } else if (isProCrm) {
      brandAvatarName = "Xavier";
      brandSpecialistTitle = "AI Enterprise Architect";
      brandIntro = "Hi there! I'm Xavier, your AI Enterprise Architect at <strong>Pro CRM Australia</strong>. We deliver Salesforce Agentforce, Zero-ETL Data Cloud integrations, and sovereign enterprise automation. What can we build for you today?";
      brandPillGreeting = "Hi there! I'm Xavier 👋 Ask me about Pro CRM";
      brandPrompts = [
        { text: "Agentforce Autonomous AI", prompt: "How does Salesforce Agentforce differ from basic chatbots?" },
        { text: "Zero-ETL Data Cloud sync", prompt: "Explain Zero-Copy federation across Snowflake and BigQuery." },
        { text: "APRA CPS 234 Compliance", prompt: "How do you enforce security and sovereign data boundaries?" }
      ];
      brandCtaText = "Book Enterprise AI Consultation &rarr;";
      brandPoster = "https://omni-agent.testcustomer2022.workers.dev/images/procrm_avatar_xavier_poster.jpg";
      brandVideo = "https://omni-agent.testcustomer2022.workers.dev/videos/procrm_avatar_xavier.mp4";
      brandPipVideo = "https://omni-agent.testcustomer2022.workers.dev/videos/procrm_welcome_xavier.mp4";
      brandPipPoster = "https://omni-agent.testcustomer2022.workers.dev/images/procrm_welcome_xavier_poster.jpg";
      brandBadgeName = "PRO CRM AUSTRALIA";
      brandBadgeColor = "#6366f1";
      brandVoiceId = "cjVigY5qzO86Huf0OWal";
      brandAvatarId = "procrm-agentforce";
    } else if (isEzConsultants) {
      brandAvatarName = "Friday";
      brandSpecialistTitle = "AI Cyber & Cloud Advisor";
      brandIntro = "Welcome! I'm Friday, your Cyber and Cloud Advisor at <strong>EZ Consultants</strong>. We provide rapid ASD ACSC threat intelligence, NDIS quality audit defense, and DevSecOps architecture. How can I assist you today?";
      brandPillGreeting = "Welcome! I'm Friday 👋 Ask about cyber & cloud defense";
      brandPrompts = [
        { text: "ACSC Threat Advisory", prompt: "What are the critical ASD ACSC vulnerability advisories today?" },
        { text: "NDIS Provider Audit Defense", prompt: "How do we prepare for mid-term NDIS Quality Commission audits?" },
        { text: "Cloud Security Architecture", prompt: "How do you secure multi-cloud Kubernetes & AWS workloads?" }
      ];
      brandCtaText = "Request Cyber Advisory Call &rarr;";
      brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar_female_poster.jpg";
      brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_female.mp4";
      brandBadgeName = "EZ CONSULTANTS";
      brandBadgeColor = "#00afeb";
      brandVoiceId = "Dh68koMHNSYl8A1jH9Je";
      brandAvatarId = "ezconsultants-cyber";
    } else if (isESignature) {
      brandAvatarName = "Friday";
      brandSpecialistTitle = "AI Document Specialist";
      brandIntro = "Hi there! I'm Friday, your AI Document & Security Specialist at <strong>EZ Signature</strong>. We provide secure, legally binding electronic signatures compliant with the Australian Electronic Transactions Act 1999. How can I assist your team today?";
      brandPillGreeting = "Hi there! I'm Friday 👋 Ask about digital signatures";
      brandPrompts = [
        { text: "Australian legal validity", prompt: "How do electronic signatures comply with the Australian Electronic Transactions Act 1999?" },
        { text: "AATL tamper-evident security", prompt: "Explain AES-256 encryption and Adobe Approved Trust List audit trails." },
        { text: "Compare pricing & plans", prompt: "What are your enterprise and standard signature plan tiers?" }
      ];
      brandCtaText = "Start Free Document Trial &rarr;";
      brandPoster = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/images/friday_avatar_female_poster.jpg";
      brandVideo = "https://raw.githubusercontent.com/Finnova-Ltd/Blogs-Content/main/assets/videos/friday_avatar_female.mp4";
      brandBadgeName = "EZ SIGNATURE";
      brandBadgeColor = "#2563eb";
      brandVoiceId = "Dh68koMHNSYl8A1jH9Je";
      brandAvatarId = "ezsignature-aatl";
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
      #omni-chat-window.is-maximized { width: 620px !important; max-width: calc(100vw - 32px) !important; height: calc(100vh - 120px) !important; max-height: 840px !important; bottom: 24px !important; right: 24px !important; border-radius: 20px !important; box-shadow: 0 25px 60px -10px rgba(0,0,0,0.4) !important; }
      #omni-chat-window.is-maximized .piper-hero-video-stage { height: 310px !important; }
      .omni-btn-maximize { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; padding: 4px 8px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: 700; display: flex; align-items: center; justify-content: center; transition: all 0.15s; }
      .omni-btn-maximize:hover { background: #E2E8F0; color: #0f172a; transform: scale(1.05); }
      @media (max-width: 640px) {
        #omni-chat-window.is-maximized { width: 100vw !important; max-width: 100vw !important; height: 100vh !important; max-height: 100vh !important; bottom: 0 !important; right: 0 !important; border-radius: 0 !important; }
        #omni-chat-window.is-maximized .piper-hero-video-stage { height: 230px !important; }
      }
      
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
      
      /* Centered Click to Talk Overlay Pill on Video Stage */
      .piper-click-talk-pill {
        position: absolute;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #ffffff;
        border: 1.5px solid rgba(255, 255, 255, 0.3);
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
        z-index: 10;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        white-space: nowrap;
      }
      .piper-click-talk-pill:hover {
        background: #0066f5;
        border-color: #0066f5;
        transform: translateX(-50%) scale(1.05);
      }
      .piper-click-talk-pill.talking {
        background: #10B981;
        border-color: rgba(16, 185, 129, 0.5);
      }

      /* PiP (Picture-in-Picture) Floating Video Player Card */
      .omni-pip-player {
        position: relative;
        width: 140px;
        height: 95px;
        border-radius: 14px;
        overflow: hidden;
        cursor: pointer;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25), 0 2px 10px rgba(0, 82, 255, 0.25);
        border: 2px solid #ffffff;
        background: #0A2540;
        transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease;
        user-select: none;
      }
      .omni-pip-player:hover {
        transform: translateY(-4px) scale(1.04);
        box-shadow: 0 16px 38px rgba(0, 0, 0, 0.35), 0 4px 18px rgba(0, 82, 255, 0.35);
      }
      .omni-pip-video-container {
        width: 100%;
        height: 100%;
        position: relative;
      }
      .omni-pip-video-container video {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }
      .omni-pip-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 6px;
        background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 40%, rgba(0,0,0,0.65) 100%);
        pointer-events: none;
      }
      .omni-pip-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
      }
      .omni-pip-badge {
        font-size: 10px;
        font-weight: 700;
        color: #ffffff;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        padding: 2px 7px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        border: 1px solid rgba(255, 255, 255, 0.2);
      }
      .omni-pip-dot {
        width: 6px;
        height: 6px;
        background: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 6px #10B981;
      }
      .omni-pip-minimize {
        font-size: 11px;
        color: rgba(255,255,255,0.7);
        padding: 2px 5px;
        border-radius: 50%;
        pointer-events: auto;
        cursor: pointer;
        line-height: 1;
        transition: color 0.15s;
      }
      .omni-pip-minimize:hover {
        color: #ef4444;
      }
      .omni-pip-bottom-bar {
        display: flex;
        justify-content: center;
        width: 100%;
      }
      .omni-pip-action-pill {
        font-size: 10px;
        font-weight: 700;
        color: #ffffff;
        background: ${primaryColor};
        padding: 3px 9px;
        border-radius: 999px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        display: inline-flex;
        align-items: center;
        gap: 3px;
        animation: omniPipPulse 2.5s infinite;
      }
      @keyframes omniPipPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
      }
      @media (max-width: 640px) {
        .omni-pip-player {
          width: 115px;
          height: 80px;
          border-radius: 12px;
        }
        .omni-pip-action-pill {
          font-size: 9px;
          padding: 2px 6px;
        }
      }

      /* Video Call Controls Bar (Image 2 & 3) - Floating top-right HUD so video captions are 100% visible */
      .piper-call-bar { position: absolute; top: 10px; right: 12px; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); padding: 4px 10px; border-radius: 999px; display: none; align-items: center; gap: 8px; z-index: 10; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35); }
      .piper-ctrl-btn { background: transparent; border: none; color: #ffffff; font-size: 15px; padding: 4px 6px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: color 0.15s; }
      .piper-ctrl-btn.active { color: #10B981; animation: omniMicPulse 1.5s infinite; }
      .piper-ctrl-btn.muted { color: #ef4444; }
      .piper-ctrl-end { background: #ef4444; color: #ffffff; font-size: 11.5px; font-weight: 700; padding: 4px 10px; border-radius: 999px; border: none; cursor: pointer; margin-left: 2px; transition: background 0.15s; }
      .piper-ctrl-end:hover { background: #dc2626; }

      /* Floating Brand / Project Logo Badge over Avatar Video */
      .piper-video-logo-badge { position: absolute; top: 10px; left: 12px; display: flex; align-items: center; gap: 6px; background: rgba(15, 23, 42, 0.82); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); color: #ffffff; padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 700; letter-spacing: 0.4px; border: 1px solid rgba(255, 255, 255, 0.18); box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35); z-index: 9; pointer-events: none; }
      .piper-badge-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; box-shadow: 0 0 6px currentColor; }

      /* Welcome Card Text & Full-Width CTA (Image 1) */
      .piper-card-welcome { padding: 14px 4px 4px; }
      .piper-card-intro { font-size: 13.5px; color: #1E293B; line-height: 1.48; font-weight: 500; margin: 0 0 14px; }
      .piper-connect-btn-full { width: 100%; background: #0066f5; color: #ffffff; border: none; padding: 11px 16px; border-radius: 8px; font-weight: 700; font-size: 13.5px; cursor: pointer; transition: background 0.2s; box-shadow: 0 2px 6px rgba(0, 102, 245, 0.25); margin-bottom: 8px; }
      .piper-connect-btn-full:hover { background: #0052cc; }

      /* Conversation Mode Toggling */
      #omni-chat-window.is-conversing .piper-card-welcome { display: none !important; }
      #omni-chat-window.is-conversing #omni-chat-messages { display: flex !important; }
      #omni-chat-window.is-conversing .piper-speak-now-btn { display: none !important; }
      #omni-chat-window.is-conversing .piper-call-bar { display: flex !important; }

      #omni-chat-messages { flex: 1; padding: 10px 14px; overflow-y: auto; display: none; flex-direction: column; gap: 8px; font-size: 13.5px; background: ${msgAreaBg} !important; min-height: 140px; }
      .omni-msg { padding: 9px 13px; border-radius: 12px; max-width: 88%; word-break: break-word; line-height: 1.48; }
      .omni-msg.user { background: ${primaryColor} !important; color: #ffffff !important; align-self: flex-end; border-bottom-right-radius: 3px; }
      .omni-msg.assistant { background: ${assistantBg} !important; color: ${assistantText} !important; align-self: flex-start; border-bottom-left-radius: 3px; border: 1px solid ${assistantBorder}; }
      .omni-msg.loading { color: #64748b; font-style: italic; }
      .omni-msg-actions { display: flex; gap: 8px; margin-top: 6px; font-size: 12px; opacity: 0.8; }
      .omni-action-btn { cursor: pointer; user-select: none; transition: transform 0.1s; }
      .omni-action-btn:hover { transform: scale(1.2); }

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
      <div id="omni-pip-player" class="omni-pip-player" title="Click to chat with ${brandAvatarName}">
        <div class="omni-pip-video-container">
          <video id="omni-pip-video" src="${brandPipVideo}" poster="${brandPipPoster}" playsinline webkit-playsinline muted loop autoplay preload="auto"></video>
          <div class="omni-pip-overlay">
            <div class="omni-pip-top-bar">
              <span class="omni-pip-badge"><span class="omni-pip-dot"></span> ${brandAvatarName}</span>
              <span class="omni-pip-minimize" id="omniPipMinimize" title="Minimize">✕</span>
            </div>
            <div class="omni-pip-bottom-bar">
              <span class="omni-pip-action-pill">Chat with ${brandAvatarName} &rarr;</span>
            </div>
          </div>
        </div>
      </div>
      <div id="omni-chat-bubble" class="omni-avatar-trigger" title="Chat with ${brandAvatarName}" style="display:none;">
        <div class="omni-avatar-disc">
          <img src="${brandPoster}" alt="${brandAvatarName} AI Avatar" class="omni-avatar-face" />
          <span class="omni-avatar-online-dot"></span>
          <span class="omni-avatar-wave-badge">👋</span>
        </div>
        <div class="omni-avatar-close-icon">✕</div>
      </div>
    `;
    appendToBody(triggerGroup);
    const bubble = document.getElementById('omni-chat-bubble');
    const greetingPill = document.getElementById('omni-chat-greeting-pill');
    const pipPlayer = document.getElementById('omni-pip-player');
    const pipVideo = document.getElementById('omni-pip-video');

    if (pipVideo) {
      pipVideo.muted = true;
      pipVideo.defaultMuted = true;
      pipVideo.playsInline = true;
      pipVideo.loop = true;
      pipVideo.setAttribute('muted', '');
      pipVideo.setAttribute('playsinline', '');
      pipVideo.setAttribute('webkit-playsinline', '');
      pipVideo.setAttribute('loop', '');
      pipVideo.setAttribute('autoplay', '');

      // Keep playing the 3-second video in a continuous seamless loop when minimized
      pipVideo.addEventListener('ended', function() {
        pipVideo.currentTime = 0;
        pipVideo.play().catch(function() {});
      });

      // Continuous loop restart via timeupdate right before duration ends (prevents browser freezing on final frame)
      pipVideo.addEventListener('timeupdate', function() {
        if (pipVideo.duration && pipVideo.currentTime >= (pipVideo.duration - 0.12)) {
          pipVideo.currentTime = 0;
          pipVideo.play().catch(function() {});
        }
      });

      const startPipLoop = function() {
        if (pipPlayer && pipPlayer.style.display !== 'none' && (!win || win.style.display !== 'flex')) {
          pipVideo.muted = true;
          pipVideo.defaultMuted = true;
          const p = pipVideo.play();
          if (p !== undefined) {
            p.catch(function(err) {
              console.log("PiP autoplay note:", err);
            });
          }
        }
      };

      pipVideo.addEventListener('canplay', startPipLoop);
      pipVideo.addEventListener('loadeddata', startPipLoop);
      pipVideo.addEventListener('pause', function() {
        if (pipPlayer && pipPlayer.style.display !== 'none' && (!win || win.style.display !== 'flex')) {
          pipVideo.play().catch(function() {});
        }
      });

      // Browser autoplay policy gesture unlock
      const unlockAutoplay = function() {
        if (pipVideo && pipVideo.paused && pipPlayer && pipPlayer.style.display !== 'none' && (!win || win.style.display !== 'flex')) {
          pipVideo.muted = true;
          pipVideo.play().catch(function() {});
        }
      };
      ['click', 'touchstart', 'scroll', 'mousemove', 'pointerdown'].forEach(function(evt) {
        window.addEventListener(evt, unlockAutoplay, { once: true, passive: true });
      });

      document.addEventListener('visibilitychange', function() {
        if (!document.hidden && pipPlayer && pipPlayer.style.display !== 'none' && (!win || win.style.display !== 'flex')) {
          pipVideo.play().catch(function() {});
        }
      });

      startPipLoop();
    }

    win = document.createElement('div');
    win.id = 'omni-chat-window';
    win.innerHTML = `
      <div id="omni-chat-header">
        <div class="title-wrap">
          <span class="title">${brandAvatarName}</span>
          <span class="badge">${brandSpecialistTitle}</span>
        </div>
        <div class="omni-hdr-actions">
          <button class="omni-btn-endchat" id="omniEndChat" title="Email Transcript">✉️ Email</button>
          <button type="button" class="omni-btn-maximize" id="omniMaximizeBtn" title="Maximize Screen">⤢</button>
          <span id="omni-close" style="cursor:pointer; font-size: 18px; color: #64748b; padding: 2px 6px;">✕</span>
        </div>
      </div>

      <div class="piper-hero-card">
        <div class="piper-hero-video-stage" id="piperVideoStage">
          ${brandVideoId ? `
          <iframe id="piper-hero-iframe" 
            src="https://app.heygen.com/embeds/${brandVideoId}?autoplay=0&loop=0" 
            allow="autoplay; fullscreen; encrypted-media; picture-in-picture" 
            allowfullscreen 
            style="width: 100%; height: 100%; border: none; border-radius: 14px; display: block; position: absolute; top: 0; left: 0; z-index: 1;">
          </iframe>
          <video id="piper-hero-video" playsinline muted preload="auto" poster="${brandPoster}" style="display:none;">
            <source src="${brandVideo}" type="video/mp4">
          </video>
          ` : `
          <video id="piper-hero-video" src="${brandVideo}" playsinline webkit-playsinline muted loop autoplay preload="auto" poster="${brandPoster}">
            <source src="${brandVideo}" type="video/mp4">
          </video>
          `}
          <!-- Floating Brand / Project Logo Badge -->
          <div class="piper-video-logo-badge" id="piperVideoLogoBadge">
            <span class="piper-badge-dot" style="background:${brandBadgeColor};"></span>
            <span>${brandBadgeName}</span>
          </div>
          <!-- Centered Click to Talk Overlay Pill on Video Stage -->
          <div class="piper-click-talk-pill" id="piperClickTalkPill">
            <span>🔊</span> <span>Click to Talk with ${brandAvatarName}</span>
          </div>
          <!-- Video Call Controls Bar (Clean Top-Right HUD) -->
          <div class="piper-call-bar" id="piperCallBar" style="display:flex;">
            <button type="button" class="piper-ctrl-btn" id="piperSoundToggle" title="Audio Sound Mute/Unmute">🔇</button>
            <button type="button" class="piper-ctrl-btn" id="piperExpandBtn" title="Maximize Screen">⤢</button>
            <button type="button" class="piper-ctrl-btn" id="piperMicToggle" title="Microphone Speech to Text">🎙️</button>
            <button type="button" class="piper-ctrl-end" id="piperEndBtn" title="End Call" style="display:none;">End</button>
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

      <div id="omni-image-preview-bar">
        <img id="omniPreviewImg" src="" alt="preview" />
        <span>Attached image ready</span>
        <span id="omniRemoveImg" style="cursor:pointer; color:#ef4444; font-weight:bold; margin-left:auto;">✕</span>
      </div>

      <!-- Unified Ask Input Box (Matching Image 1) -->
      <div id="omni-chat-input-container">
        <input type="file" id="omniFileInput" accept="image/*" style="display:none;" />
        ${config.features?.imageUpload !== false ? '<button class="omni-attach-btn" id="omniAttachBtn" title="Attach Image">📎</button>' : ''}
        <input type="text" id="omni-chat-input" placeholder="Ask ${brandAvatarName} a question" />
        <button class="omni-mic-btn" id="omniMicBtn" title="Speak with ${brandAvatarName}">🎙️</button>
        <button id="omni-chat-send" title="Send message">&rarr;</button>
      </div>

      <div class="omni-disclaimer-footer">
        ${brandAvatarName} is an AI and can make mistakes. Please note, by continuing, you agree to the terms of our privacy policy. This conversation will be recorded.
      </div>
    `;
    appendToBody(win);
    const videoStage = document.getElementById("piperVideoStage");
    const heroVideo = document.getElementById("piper-hero-video");
    const callSoundBtn = document.getElementById("piperSoundToggle");
    const maxHdrBtn = document.getElementById("omniMaximizeBtn");
    const maxStageBtn = document.getElementById("piperExpandBtn");
    const micToggleBtn = document.getElementById("piperMicToggle");

    function updateSoundUi(isUnmuted) {
      if (callSoundBtn) {
        callSoundBtn.textContent = isUnmuted ? "🔊" : "🔇";
        callSoundBtn.title = isUnmuted ? "Mute Audio" : "Unmute Audio";
        callSoundBtn.classList.toggle("active", isUnmuted);
      }
    }

    function toggleSound(forceUnmute) {
      if (!heroVideo) return;
      if (!heroVideo.src || heroVideo.src === window.location.href) {
        heroVideo.src = brandVideo;
      }
      const talkPill = document.getElementById("piperClickTalkPill");
      const willUnmute = (forceUnmute === true) || heroVideo.muted || heroVideo.volume === 0;
      if (willUnmute) {
        heroVideo.muted = false;
        heroVideo.volume = 1.0;
        isVoiceActive = true;
        if (talkPill) {
          talkPill.innerHTML = `<span>🔊</span> <span>${brandAvatarName} Talking • Click to Mute</span>`;
          talkPill.classList.add("talking");
        }
        if (heroVideo.paused || heroVideo.ended) {
          heroVideo.currentTime = 0;
        }
        const p = heroVideo.play();
        if (p !== undefined) {
          p.then(() => updateSoundUi(true)).catch((err) => {
            console.log("Unmute play restricted:", err);
            heroVideo.muted = true;
            heroVideo.play().catch(() => {});
            updateSoundUi(false);
            isVoiceActive = false;
            if (talkPill) {
              talkPill.innerHTML = `<span>🔊</span> <span>Click to Talk with ${brandAvatarName}</span>`;
              talkPill.classList.remove("talking");
            }
          });
        } else {
          updateSoundUi(true);
        }
      } else {
        heroVideo.muted = true;
        stopSpeaking();
        isVoiceActive = false;
        updateSoundUi(false);
        if (talkPill) {
          talkPill.innerHTML = `<span>🔊</span> <span>Click to Talk with ${brandAvatarName}</span>`;
          talkPill.classList.remove("talking");
        }
      }
    }

    function toggleMaximize() {
      const isMax = win.classList.toggle("is-maximized");
      if (maxHdrBtn) maxHdrBtn.innerHTML = isMax ? "⤡" : "⤢";
      if (maxStageBtn) maxStageBtn.innerHTML = isMax ? "⤡" : "⤢";
    }

    if (maxHdrBtn) maxHdrBtn.onclick = (e) => { e.stopPropagation(); toggleMaximize(); };
    if (maxStageBtn) maxStageBtn.onclick = (e) => { e.stopPropagation(); toggleMaximize(); };
    if (callSoundBtn) callSoundBtn.onclick = (e) => { e.stopPropagation(); toggleSound(); };

    const clickTalkPill = document.getElementById("piperClickTalkPill");
    if (clickTalkPill) {
      clickTalkPill.onclick = (e) => {
        e.stopPropagation();
        toggleSound();
      };
    }

    function playVideoWithVoice(src, poster, badgeText) {
      if (!heroVideo) return;
      if (src && !heroVideo.src.includes(src)) {
        heroVideo.src = src;
        if (poster) heroVideo.poster = poster;
        heroVideo.currentTime = 0;
      }
      heroVideo.muted = false;
      heroVideo.volume = 1.0;
      const p = heroVideo.play();
      if (p !== undefined) {
        p.then(() => updateSoundUi(true)).catch((err) => {
          console.log("Unmuted playback restricted, user gesture needed:", err);
          heroVideo.muted = true;
          heroVideo.play().catch(() => {});
          updateSoundUi(false);
        });
      }
      if (badgeText && brandBadgeName) {
        const badgeEl = document.getElementById("piperVideoLogoBadge");
        if (badgeEl) {
          badgeEl.innerHTML = `<span class="piper-badge-dot" style="background:${brandBadgeColor};"></span><span>${badgeText}</span>`;
        }
      }
    }


    function initSpeechRecognition() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) return null;
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = true;
      rec.lang = "en-AU";
      return rec;
    }

    function startListening() {
      const micBtn = document.getElementById("omniMicBtn");
      const micToggle = document.getElementById("piperMicToggle");
      const chatInput = document.getElementById("omni-chat-input");
      if (!recognition) recognition = initSpeechRecognition();
      if (!recognition) {
        if (chatInput) {
          chatInput.focus();
          chatInput.placeholder = "Type your question here...";
        }
        return;
      }
      if (isListening) {
        recognition.stop();
        return;
      }
      try {
        recognition.start();
        isListening = true;
        if (micBtn) micBtn.classList.add("active");
        if (micToggle) micToggle.classList.add("active");
        if (chatInput) chatInput.placeholder = "🎙️ Listening to you... Speak now";
        
        recognition.onresult = (event) => {
          let transcript = "";
          for (let i = 0; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
          }
          if (chatInput) chatInput.value = transcript;
          if (event.results[0].isFinal) {
            isListening = false;
            if (micBtn) micBtn.classList.remove("active");
            if (micToggle) micToggle.classList.remove("active");
            if (chatInput) chatInput.placeholder = "Ask " + brandAvatarName + " a question";
            if (transcript.trim()) {
              sendMessage(transcript.trim());
            }
          }
        };
        recognition.onerror = (err) => {
          console.log("Speech recognition error:", err);
          isListening = false;
          if (micBtn) micBtn.classList.remove("active");
          if (micToggle) micToggle.classList.remove("active");
          if (chatInput) chatInput.placeholder = "Ask " + brandAvatarName + " a question";
        };
        recognition.onend = () => {
          isListening = false;
          if (micBtn) micBtn.classList.remove("active");
          if (micToggle) micToggle.classList.remove("active");
          if (chatInput) chatInput.placeholder = "Ask " + brandAvatarName + " a question";
        };
      } catch (e) {
        console.warn("Speech recognition start failed:", e);
      }
    }

    function stopListening() {
      if (recognition && isListening) {
        try {
          recognition.stop();
        } catch (e) {}
      }
      isListening = false;
      const micBtn = document.getElementById("omniMicBtn");
      const micToggle = document.getElementById("piperMicToggle");
      const chatInput = document.getElementById("omni-chat-input");
      if (micBtn) micBtn.classList.remove("active");
      if (micToggle) micToggle.classList.remove("active");
      if (chatInput && chatInput.placeholder && chatInput.placeholder.includes("Listening")) {
        chatInput.placeholder = "Ask " + brandAvatarName + " a question";
      }
    }

    function triggerVoicePromptAfterSpeech() {
      const msgContainer = document.getElementById("omni-chat-messages");
      if (!msgContainer) return;
      
      const existingInvite = document.getElementById("omni-voice-invite");
      if (existingInvite) existingInvite.remove();

      const inviteEl = document.createElement("div");
      inviteEl.id = "omni-voice-invite";
      inviteEl.style.cssText = "font-size:12px; color:#0369a1; background:#f0f9ff; border:1px solid #bae6fd; border-radius:8px; padding:7px 12px; margin:6px 0; display:flex; align-items:center; gap:8px; cursor:pointer; font-weight:600; transition:all 0.2s;";
      inviteEl.innerHTML = `<span>🎙️</span> <span><strong>${brandAvatarName} is listening...</strong> Tap here or click the mic to speak</span>`;
      inviteEl.onmouseover = () => { inviteEl.style.background = "#e0f2fe"; };
      inviteEl.onmouseout = () => { inviteEl.style.background = "#f0f9ff"; };
      inviteEl.onclick = () => startListening();
      msgContainer.appendChild(inviteEl);
      msgContainer.scrollTop = msgContainer.scrollHeight;
    }

    if (micToggleBtn) micToggleBtn.onclick = (e) => { e.stopPropagation(); startListening(); };

    if (videoStage && heroVideo) {
      videoStage.style.cursor = "pointer";
      function triggerPlay() {
        if (!heroVideo) return;
        heroVideo.muted = true;
        heroVideo.playsInline = true;
        heroVideo.setAttribute("playsinline", "");
        heroVideo.setAttribute("webkit-playsinline", "");
        if (!heroVideo.src || heroVideo.src === window.location.href) {
          heroVideo.src = brandVideo;
        }
        const playPromise = heroVideo.play();
        if (playPromise !== undefined) {
          playPromise.catch(function(err) {
            console.log("Auto-play interaction needed:", err);
          });
        }
      }
      videoStage.addEventListener("mouseenter", function() {
        if (heroVideo.paused) triggerPlay();
      });
      videoStage.addEventListener("mousemove", function() {
        if (heroVideo.paused) triggerPlay();
      });
      videoStage.addEventListener("click", function(e) {
        if (e.target.closest("#piperCallBar")) return;
        toggleSound();
      });
      triggerPlay();

      // Seamless video loop when muted; attentive pause when unmuted
      heroVideo.addEventListener("ended", function() {
        if (heroVideo.muted) {
          heroVideo.currentTime = 0;
          heroVideo.play().catch(() => {});
        } else {
          heroVideo.pause();
          heroVideo.currentTime = 0;
          const talkPill = document.getElementById("piperClickTalkPill");
          if (talkPill) {
            talkPill.innerHTML = `<span>🎙️</span> <span>Click to Talk with ${brandAvatarName}</span>`;
            talkPill.classList.remove("talking");
          }
          triggerVoicePromptAfterSpeech();
        }
      });
    }

    function openChat(withSound = true) {
      win.style.display = 'flex';
      if (pipPlayer) pipPlayer.style.display = 'none';
      if (bubble) {
        bubble.style.display = 'flex';
        bubble.classList.add('is-open');
      }
      if (greetingPill) greetingPill.style.display = 'none';
      if (pipVideo) {
        try { pipVideo.pause(); } catch(e) {}
      }

      if (withSound) {
        // Direct click to chat: make window bigger, unmute, and start talking
        toggleSound(true);
      } else {
        if (heroVideo) {
          heroVideo.muted = true;
          updateSoundUi(false);
          if (heroVideo.paused) {
            heroVideo.play().catch(() => {});
          }
        }
        const talkPill = document.getElementById("piperClickTalkPill");
        if (talkPill) {
          talkPill.innerHTML = `<span>🔊</span> <span>Click to Talk with ${brandAvatarName}</span>`;
          talkPill.classList.remove("talking");
        }
      }
    }

    function closeChat() {
      win.style.display = 'none';
      if (bubble) {
        bubble.classList.remove('is-open');
        bubble.style.display = 'none';
      }
      sessionStorage.setItem('piper_chat_dismissed', 'true');
      if (heroVideo) {
        heroVideo.pause();
        heroVideo.muted = true;
      }
      stopSpeaking();
      stopListening();
      isVoiceActive = false;
      updateSoundUi(false);
      const talkPill = document.getElementById("piperClickTalkPill");
      if (talkPill) {
        talkPill.innerHTML = `<span>🔊</span> <span>Click to Talk with ${brandAvatarName}</span>`;
        talkPill.classList.remove("talking");
      }

      if (pipPlayer) {
        pipPlayer.style.display = 'block';
        if (pipVideo) {
          pipVideo.currentTime = 0;
          pipVideo.muted = true;
          pipVideo.play().catch(() => {});
        }
      }
      if (greetingPill && !sessionStorage.getItem('omni_pill_dismissed')) {
        greetingPill.style.display = 'flex';
      }
    }

    if (pipPlayer) {
      pipPlayer.onclick = () => {
        openChat(true);
      };
    }

    const pipMinBtn = document.getElementById('omniPipMinimize');
    if (pipMinBtn) {
      pipMinBtn.onclick = (e) => {
        e.stopPropagation();
        if (pipPlayer) pipPlayer.style.display = 'none';
        if (bubble) bubble.style.display = 'flex';
      };
    }

    if (bubble) {
      bubble.onclick = () => {
        if (win.style.display !== 'flex') {
          openChat(true);
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
        openChat(true);
      };
    }

    const closeBtn = document.getElementById('omni-close');
    if (closeBtn) closeBtn.onclick = closeChat;

    // Voice & Conversational AI Engine (Salesforce Piper Parity)
    const video = document.getElementById("piper-hero-video");
    const endBtn = document.getElementById("piperEndBtn");
    const micBtn = document.getElementById("omniMicBtn");
    if (micBtn) micBtn.onclick = startListening;

    if (video) {
      video.muted = true;
      video.playsInline = true;
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
      if (isFinnova) {
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
        video.currentTime = 0;
        video.loop = true;
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
        if (isVoiceActive || (win && win.classList.contains('is-conversing'))) {
          setTimeout(() => {
            if (!isSpeaking) startListening();
          }, 350);
        }
      };

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
            return;
          }
        }
      }

      await fetchTtsAndPlay(clean, onComplete, speechId);
    }

    async function fetchTtsAndPlay(cleanText, onComplete, speechId) {
      if (speechId !== currentSpeechId) return;
      try {
        const res = await fetch(`${backendUrl}/api/tts`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: cleanText, domain: currentDomain, voiceId: brandVoiceId, avatarId: brandAvatarId })
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

      if (speechId === currentSpeechId) {
        fallbackBrowserSpeech(cleanText, onComplete, speechId);
      }
    }

    function startVoiceConversation() {
      isVoiceActive = true;
      if (win) win.classList.add('is-conversing');
      
      const msgContainer = document.getElementById('omni-chat-messages');
      const greetingFullText = brandIntro.replace(/<[^>]+>/g, " ").trim();

      if (msgContainer && msgContainer.children.length === 0) {
        const greetDiv = document.createElement('div');
        greetDiv.className = 'omni-msg assistant';
        greetDiv.innerHTML = brandIntro;
        msgContainer.appendChild(greetDiv);
        msgContainer.scrollTop = 0;
      }

      speakFriday(greetingFullText, () => {
        if (isVoiceActive) startListening();
      }, true);
    }

    function endVoiceConversation() {
      isVoiceActive = false;
      stopListening();
      stopSpeaking();
      if (win) win.classList.remove('is-conversing');
    }

    if (endBtn) endBtn.onclick = endVoiceConversation;

    // Connect with Sales Rep / Broker Buttons
    const handleConnectClick = () => {
      const input = document.getElementById('omni-chat-input');
      if (input) {
        if (win) win.classList.add('is-conversing');
        input.value = isProCrm 
          ? "I'd like to book an enterprise consultation with a Pro CRM architect." 
          : "I'd like to connect directly with a licensed specialist for a consultation.";
        sendMessage();
      }
    };
    const connectBtn = document.getElementById('piperConnectRep');
    if (connectBtn) connectBtn.onclick = handleConnectClick;

    const fileInput = document.getElementById('omni-image-upload') || document.getElementById('omniFileInput');
    const attachBtn = document.getElementById('omni-attach-btn') || document.getElementById('omniAttachBtn');
    const previewBar = document.getElementById('omni-image-preview-bar');
    const previewImg = document.getElementById('omniPreviewImg');
    const removeImgBtn = document.getElementById('omniRemoveImg');
    const chatInput = document.getElementById('omni-chat-input');

    if (attachBtn && fileInput) {
      attachBtn.onclick = (e) => {
        e.preventDefault();
        fileInput.click();
      };
      fileInput.onchange = (e) => {
        const file = e.target.files && e.target.files[0];
        if (file) handleImageFile(file);
      };
    }

    if (chatInput && config.features?.imageUpload !== false) {
      chatInput.addEventListener('paste', (e) => {
        const items = (e.clipboardData || (e.originalEvent && e.originalEvent.clipboardData) || {}).items || [];
        for (let item of items) {
          if (item.type && item.type.indexOf('image') === 0) {
            const blob = item.getAsFile();
            if (blob) handleImageFile(blob);
          }
        }
      });
    }

    function handleImageFile(file) {
      const reader = new FileReader();
      reader.onload = (evt) => {
        attachedImageBase64 = evt.target.result;
        if (previewImg) previewImg.src = attachedImageBase64;
        if (previewBar) previewBar.style.display = 'flex';
      };
      reader.readAsDataURL(file);
    }

    if (removeImgBtn) {
      removeImgBtn.onclick = () => {
        attachedImageBase64 = "";
        if (previewBar) previewBar.style.display = 'none';
        if (fileInput) fileInput.value = "";
      };
    }

    const endChatBtn = document.getElementById('omniEndChat');
    if (endChatBtn) {
      endChatBtn.onclick = async () => {
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
    }

    async function sendMessage(textOverride) {
      stopSpeaking();
      stopListening();

      const inputElem = document.getElementById('omni-chat-input');
      const msg = (typeof textOverride === 'string' ? textOverride : (inputElem ? inputElem.value : '')).trim();
      if (!msg && !attachedImageBase64) return;

      // Switch window to conversing/dialogue mode immediately
      if (win) {
        win.classList.add('is-conversing');
      }
      const welcomeCard = document.getElementById('piperCardWelcome');
      if (welcomeCard) {
        welcomeCard.style.display = 'none';
      }
      const msgContainer = document.getElementById('omni-chat-messages');
      if (msgContainer) {
        msgContainer.style.display = 'flex';
      }

      const lowerMsg = msg.toLowerCase().trim();
      updateLeadScore(10, "Sent Message");

      let userHtml = parseMarkdown(msg, primaryColor);
      if (attachedImageBase64) {
        userHtml += `<br/><img src="${attachedImageBase64}" style="max-width:180px; border-radius:6px; margin-top:6px;" />`;
      }

      const userMsgDiv = document.createElement('div');
      userMsgDiv.className = 'omni-msg user';
      userMsgDiv.innerHTML = userHtml;
      if (msgContainer) {
        msgContainer.appendChild(userMsgDiv);
      }

      const sentImage = attachedImageBase64;
      if (inputElem) inputElem.value = '';
      attachedImageBase64 = "";
      if (previewBar) previewBar.style.display = 'none';
      if (msgContainer) msgContainer.scrollTop = msgContainer.scrollHeight;

      const loadingMsg = document.createElement('div');
      loadingMsg.className = 'omni-msg assistant loading';
      loadingMsg.textContent = brandAvatarName + " is thinking...";
      if (msgContainer) {
        msgContainer.appendChild(loadingMsg);
        msgContainer.scrollTop = msgContainer.scrollHeight;
      }

      // Client-Side Strict Legal & Anti-Fraud Interceptor (NCCP Act & Best Interests Duty)
      const FRAUD_AND_UNETHICAL_REGEX = /(trick the bank|hide debt|hide loan|hide credit card|fake payslip|doctor payslip|falsify income|omit dependent|omit debt|cheat serviceability|lie on application|bypass apra|evade tax|straw buyer|fake bonus|off the books cash|unethical tips|against the law|forge statement|forge payslip)/i;
      if (FRAUD_AND_UNETHICAL_REGEX.test(lowerMsg)) {
        loadingMsg.classList.remove("loading");
        const refusalText = "As licensed Australian mortgage credit specialists operating under the National Consumer Credit Protection Act (NCCP Act 2009) and statutory Best Interests Duty (BID), we adhere strictly to Australian lending law.\n\n" +
                            "We do not provide tips or assistance to mislead lenders, conceal liabilities, or submit altered documentation. Attempting to misrepresent financials on a credit application constitutes mortgage fraud under Australian law, carries severe criminal penalties, and leads to immediate loan rejection and credit file blacklisting. It is never worth the risk.\n\n" +
                            "We can, however, help you legally maximize your borrowing capacity by comparing 30+ accredited Australian lenders with diverse assessment benchmarks, restructuring existing debts, or identifying suitable lending policies.\n\n" +
                            "*Disclaimer: All advice is regulated credit assistance under Australian credit law.*";
        
        loadingMsg.innerHTML = parseMarkdown(refusalText, primaryColor);
        if (msgContainer) msgContainer.scrollTop = msgContainer.scrollHeight;
        triggerVoicePromptAfterSpeech();
        return;
      }

      // Check for Canned Video Concept Matches for EZ Mortgage Broker
      const matchedConcept = isEzMortgage && EZ_MORTGAGE_CANNED_CONCEPTS.find(c => 
        lowerMsg.includes(c.title.toLowerCase()) ||
        lowerMsg.includes(c.chip.toLowerCase().replace(/[^a-z0-9 ]/gi, '')) ||
        c.keywords.some(k => lowerMsg.includes(k))
      );

      if (matchedConcept) {
        loadingMsg.classList.remove('loading');

        // Switch hero video to concept video and play with authentic voice
        if (matchedConcept.localVideo) {
          playVideoWithVoice(
            matchedConcept.localVideo, 
            matchedConcept.localPoster, 
            `EZ MORTGAGE BROKER • ${matchedConcept.title.split('(' )[0].trim()}`
          );
        }

        // Render rich canned response with Video Player / Card and Transcript
        const videoResponseHtml = `
          <div style="font-weight:700; margin-bottom:8px; color:${primaryColor}; display:flex; align-items:center; gap:6px;">
            <span>🎬</span> <span>${matchedConcept.title}</span>
            <span style="font-size:10px; background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-weight:600; margin-left:auto;">${matchedConcept.duration}</span>
          </div>
          <div style="margin-bottom:10px; line-height:1.55; color:${assistantText}; font-size:13.5px;">
            "${matchedConcept.script}"
          </div>
          <div style="background:#f8fafc; border-radius:8px; padding:10px; border:1px solid #e2e8f0; margin-top:8px; display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">
            <div style="font-size:11.5px; color:#475569; display:flex; align-items:center; gap:6px;">
              <span>📹</span> <span><strong>AI Specialist Video:</strong> ${matchedConcept.title.split('(' )[0].trim()}</span>
            </div>
            <div style="display:flex; gap:6px; align-items:center; margin-left:auto;">
              <button type="button" class="omni-replay-voice-btn" data-video="${matchedConcept.localVideo || ''}" data-poster="${matchedConcept.localPoster || ''}" data-title="${matchedConcept.title.split('(' )[0].trim()}" style="background:#10B981; color:#ffffff; border:none; padding:6px 11px; border-radius:6px; font-size:11.5px; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:4px; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
                ▶️ Play with Voice
              </button>
              <a href="${matchedConcept.videoUrl}" target="_blank" rel="noopener noreferrer" style="background:#F1F5F9; color:#0f172a; text-decoration:none; padding:6px 9px; border-radius:6px; font-size:11px; font-weight:600; border:1px solid #CBD5E1;" title="View on Google Gemini">
                Gemini ↗
              </a>
            </div>
          </div>
        `;
        loadingMsg.innerHTML = videoResponseHtml;

        const replayBtn = loadingMsg.querySelector('.omni-replay-voice-btn');
        if (replayBtn) {
          replayBtn.onclick = () => {
            const vSrc = replayBtn.getAttribute('data-video');
            const vPost = replayBtn.getAttribute('data-poster');
            const vTitle = replayBtn.getAttribute('data-title');
            playVideoWithVoice(vSrc, vPost, `EZ MORTGAGE BROKER • ${vTitle}`);
          };
        }

        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'omni-msg-actions';
        actionsDiv.innerHTML = `
          <span class="omni-action-btn" title="Thumbs Up">👍</span>
          <span class="omni-action-btn" title="Thumbs Down">👎</span>
          <span class="omni-action-btn" title="Smiley">😊</span>
          <span class="omni-quote-btn" title="Quote reply">💬 Quote</span>
        `;
        const quoteBtn = actionsDiv.querySelector('.omni-quote-btn');
        if (quoteBtn && chatInput) {
          quoteBtn.onclick = () => {
            chatInput.value = `> "${matchedConcept.script.substring(0, 80)}..."\n`;
            chatInput.focus();
          };
        }
        actionsDiv.querySelectorAll('.omni-action-btn').forEach(btn => {
          btn.onclick = () => {
            btn.style.transform = 'scale(1.4)';
            setTimeout(() => btn.style.transform = 'scale(1)', 200);
          };
        });
        loadingMsg.appendChild(actionsDiv);
        if (msgContainer) msgContainer.scrollTop = msgContainer.scrollHeight;
        return;
      }

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
        
        const quoteBtn = actionsDiv.querySelector('.omni-quote-btn');
        if (quoteBtn && chatInput) {
          quoteBtn.onclick = () => {
            chatInput.value = '> "' + replyRaw.substring(0, 80).replace(/\n/g, ' ') + '..."\n';
            chatInput.focus();
          };
        }

        actionsDiv.querySelectorAll('.omni-action-btn').forEach(btn => {
          btn.onclick = () => {
            btn.style.transform = 'scale(1.4)';
            setTimeout(() => btn.style.transform = 'scale(1)', 200);
          };
        });

        loadingMsg.appendChild(actionsDiv);

        if (isVoiceActive) {
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
        if (isVoiceActive) {
          speakFriday("I'm sorry, I'm having trouble connecting right now. Please feel free to try again.", () => {
            if (isVoiceActive) startListening();
          }, false);
        }
      }

      if (msgContainer) msgContainer.scrollTop = msgContainer.scrollHeight;
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

      const submitBtn = document.getElementById('submitLead');
      if (submitBtn) {
        submitBtn.onclick = async () => {
          const name = document.getElementById('leadName')?.value;
          const email = document.getElementById('leadEmail')?.value;
          const phone = document.getElementById('leadPhone')?.value;
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
    }

    const sendBtn = document.getElementById('omni-chat-send');
    if (sendBtn) {
      sendBtn.onclick = (e) => { 
        e.preventDefault(); 
        sendMessage(); 
      };
    }
    const mainChatInput = document.getElementById('omni-chat-input');
    if (mainChatInput) {
      mainChatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      });
    }
  }
})();

