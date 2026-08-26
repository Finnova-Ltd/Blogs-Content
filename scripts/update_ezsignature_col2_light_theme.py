#!/usr/bin/env python3
import os

target_file = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline/dashboard-app/src/components/PhaseOneCommerce.tsx"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update AuthSlide interface and AUTH_CAROUSEL_SLIDES
old_slides_block = """interface AuthSlide {
    badge: string;
    title: string;
    highlight: string;
    description: string;
    ctaText: string;
    ctaHref: string;
    cardTag: string;
    cardTitle: string;
    cardDesc: string;
    features: string[];
    stat: { value: string; label: string };
    accentColor: string;
}

const AUTH_CAROUSEL_SLIDES: AuthSlide[] = [
    {
        badge: 'Forensic Security',
        title: 'The Fast-Start Playbook to Document & eSign ROI',
        highlight: 'eSign ROI',
        description: 'Proven workflows from high-growth teams that eliminate paper bottlenecks, power AI contract insights, and drive immediate ROI. Ditch legacy rebuilds and turn signatures into closed revenue.',
        ctaText: 'Get the Playbook ↗',
        ctaHref: 'https://ezsignature.com',
        cardTag: 'The Data 360 & eSign Playbook',
        cardTitle: 'Court-Admissible Forensic Audit Trail',
        cardDesc: 'Every envelope is sealed with 256-bit encryption, SHA-256 cryptographic hashes, and court-admissible audit logs compliant with ETA 1999 & ESIGN.',
        features: [
            'SHA-256 cryptographic digital seal',
            'Full signer IP, email & GPS timestamp log',
            'Automated reminder & completion sequences',
            '100% legally enforceable in court'
        ],
        stat: { value: '99.9%', label: 'Uptime & Compliance' },
        accentColor: '#00D2D2',
    },
    {
        badge: 'Unlimited Volume',
        title: 'Send Unlimited Envelopes with Zero Hidden Overage Fees',
        highlight: 'Zero Hidden Overage',
        description: 'Legacy eSignature vendors gouge you with per-envelope limits. EZ Signature provides truly unlimited envelopes with sequential and parallel signer routing.',
        ctaText: 'Compare Pricing Plans ↗',
        ctaHref: 'https://ezsignature.com/#pricing',
        cardTag: 'Multi-Signer Routing Engine',
        cardTitle: 'Real-Time Recipient Tracking & Webhooks',
        cardDesc: 'Monitor contracts live as recipients view, sign, and download agreements with automated webhook events.',
        features: [
            'Unlimited envelope sending on all plans',
            'Sequential & parallel multi-signer routing',
            'Custom organization branding & SMTP',
            'Live real-time status activity stream'
        ],
        stat: { value: '60%+', label: 'Average Cost Reduction' },
        accentColor: '#818CF8',
    },
    {
        badge: 'Browser Signing',
        title: 'Instant Drag & Drop Field Builder with In-Person Mobile Signing',
        highlight: 'In-Person Mobile Signing',
        description: 'Place signatures, initials, dates, and text boxes with millimeter precision. Sign directly on tablets and phones with zero app downloads.',
        ctaText: 'Try Free In-Browser Tool ↗',
        ctaHref: 'https://ezsignature.com/sign-pdf-online',
        cardTag: 'High-Speed Client-Side Engine',
        cardTitle: 'Multi-Page Navigation & Custom Calligraphy',
        cardDesc: 'Draw, type, or upload signatures with 8+ calligraphy styles and multi-page thumbnail navigation.',
        features: [
            'Multi-page thumbnail sidebar navigation',
            'Draw, type & upload signature modalities',
            'In-person counter signing on iPad / tablet',
            'Instant client-side PDF flattening'
        ],
        stat: { value: '4.9/5', label: 'Signer Experience Rating' },
        accentColor: '#34D399',
    },
    {
        badge: 'Enterprise Architecture',
        title: 'Multi-Tenant Workspaces & White-Label Domain Routing',
        highlight: 'White-Label Domain',
        description: 'Isolate departments, client firms, and operating companies with dedicated tenant hierarchies, role-based access control, and branded domains.',
        ctaText: 'Explore Solutions ↗',
        ctaHref: 'https://ezsignature.com/#industry-solutions',
        cardTag: 'Enterprise Governance & Isolation',
        cardTitle: 'Custom Subdomains & Centralized Billing',
        cardDesc: 'Dedicated URLs (sign.yourcompany.com), centralized seat management, and turnkey customer onboarding.',
        features: [
            'Multi-company tenant & workspace hierarchy',
            'Custom DNS & white-label domain routing',
            'Super Admin multi-tenant control console',
            'Single Sign-On (Google & Apple ID)'
        ],
        stat: { value: '10x', label: 'Faster Team Deployment' },
        accentColor: '#F472B6',
    }
];"""

new_slides_block = """interface AuthSlide {
    badge: string;
    title: string;
    highlight: string;
    description: string;
    ctaText: string;
    ctaHref: string;
    cardTag: string;
    cardTitle: string;
    cardDesc: string;
    features: string[];
    stat: { value: string; label: string };
    accentColor: string;
    bgImage: string;
}

const AUTH_CAROUSEL_SLIDES: AuthSlide[] = [
    {
        badge: 'Forensic Security',
        title: 'The Fast-Start Playbook to Document & eSign ROI',
        highlight: 'eSign ROI',
        description: 'Proven workflows from high-growth teams that eliminate paper bottlenecks, power AI contract insights, and drive immediate ROI. Ditch legacy rebuilds and turn signatures into closed revenue.',
        ctaText: 'Get the Playbook ↗',
        ctaHref: 'https://ezsignature.com',
        cardTag: 'The Data 360 & eSign Playbook',
        cardTitle: 'Court-Admissible Forensic Audit Trail',
        cardDesc: 'Every envelope is sealed with 256-bit encryption, SHA-256 cryptographic hashes, and court-admissible audit logs compliant with ETA 1999 & ESIGN.',
        features: [
            'SHA-256 cryptographic digital seal',
            'Full signer IP, email & GPS timestamp log',
            'Automated reminder & completion sequences',
            '100% legally enforceable in court'
        ],
        stat: { value: '99.9%', label: 'Uptime & Compliance' },
        accentColor: '#0176D3',
        bgImage: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1600&q=80',
    },
    {
        badge: 'Unlimited Volume',
        title: 'Send Unlimited Envelopes with Zero Hidden Overage Fees',
        highlight: 'Zero Hidden Overage',
        description: 'Legacy eSignature vendors gouge you with per-envelope limits. EZ Signature provides truly unlimited envelopes with sequential and parallel signer routing.',
        ctaText: 'Compare Pricing Plans ↗',
        ctaHref: 'https://ezsignature.com/#pricing',
        cardTag: 'Multi-Signer Routing Engine',
        cardTitle: 'Real-Time Recipient Tracking & Webhooks',
        cardDesc: 'Monitor contracts live as recipients view, sign, and download agreements with automated webhook events.',
        features: [
            'Unlimited envelope sending on all plans',
            'Sequential & parallel multi-signer routing',
            'Custom organization branding & SMTP',
            'Live real-time status activity stream'
        ],
        stat: { value: '60%+', label: 'Average Cost Reduction' },
        accentColor: '#0176D3',
        bgImage: 'https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=1600&q=80',
    },
    {
        badge: 'Browser Signing',
        title: 'Instant Drag & Drop Field Builder with In-Person Mobile Signing',
        highlight: 'In-Person Mobile Signing',
        description: 'Place signatures, initials, dates, and text boxes with millimeter precision. Sign directly on tablets and phones with zero app downloads.',
        ctaText: 'Try Free In-Browser Tool ↗',
        ctaHref: 'https://ezsignature.com/sign-pdf-online',
        cardTag: 'High-Speed Client-Side Engine',
        cardTitle: 'Multi-Page Navigation & Custom Calligraphy',
        cardDesc: 'Draw, type, or upload signatures with 8+ calligraphy styles and multi-page thumbnail navigation.',
        features: [
            'Multi-page thumbnail sidebar navigation',
            'Draw, type & upload signature modalities',
            'In-person counter signing on iPad / tablet',
            'Instant client-side PDF flattening'
        ],
        stat: { value: '4.9/5', label: 'Signer Experience Rating' },
        accentColor: '#0176D3',
        bgImage: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1600&q=80',
    },
    {
        badge: 'Enterprise Architecture',
        title: 'Multi-Tenant Workspaces & White-Label Domain Routing',
        highlight: 'White-Label Domain',
        description: 'Isolate departments, client firms, and operating companies with dedicated tenant hierarchies, role-based access control, and branded domains.',
        ctaText: 'Explore Solutions ↗',
        ctaHref: 'https://ezsignature.com/#industry-solutions',
        cardTag: 'Enterprise Governance & Isolation',
        cardTitle: 'Custom Subdomains & Centralized Billing',
        cardDesc: 'Dedicated URLs (sign.yourcompany.com), centralized seat management, and turnkey customer onboarding.',
        features: [
            'Multi-company tenant & workspace hierarchy',
            'Custom DNS & white-label domain routing',
            'Super Admin multi-tenant control console',
            'Single Sign-On (Google & Apple ID)'
        ],
        stat: { value: '10x', label: 'Faster Team Deployment' },
        accentColor: '#0176D3',
        bgImage: 'https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1600&q=80',
    }
];"""

if old_slides_block in content:
    content = content.replace(old_slides_block, new_slides_block)
    print("✅ Replaced AUTH_CAROUSEL_SLIDES")
else:
    print("⚠️ Could not match old_slides_block exactly, checking partial...")

# 2. Update Right Column Component JSX
old_col2_start = '{/* RIGHT COLUMN: 50% WIDTH SALESFORCE-STYLE HERO SHOWCASE WITH INTERACTIVE CAROUSEL */}'
old_col2_end = '{/* GOOGLE & APPLE AUTHENTIC IDENTITY MODAL */}'

new_col2_jsx = """{/* RIGHT COLUMN: 50% WIDTH LIGHT-THEME SHOWCASE WITH BACKGROUND IMAGE & WHITE CARD */}
            <div 
                className="hidden lg:flex lg:w-1/2 flex-col justify-between p-8 sm:p-10 xl:p-14 relative overflow-hidden bg-[#F8FAFC]"
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
            >
                {/* Dynamic Background Image with Smooth Crossfade */}
                <div 
                    className="absolute inset-0 bg-cover bg-center transition-all duration-700 ease-out transform scale-105"
                    style={{ backgroundImage: `url(${activeSlide.bgImage})` }}
                />
                {/* Sunlit High-Key Frosted Glass Overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-white/92 via-white/85 to-[#F1F5F9]/90 backdrop-blur-[2px]" />
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-[#0176D3]/10 rounded-full blur-3xl pointer-events-none" />
                <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-[#00D2D2]/10 rounded-full blur-3xl pointer-events-none" />

                {/* Central Elevated White Showcase Card */}
                <div className="relative z-10 my-auto max-w-xl mx-auto w-full">
                    <div className="rounded-[28px] border border-slate-200/90 bg-white/95 backdrop-blur-xl p-7 xl:p-9 shadow-[0_20px_50px_rgba(15,23,42,0.08)] transition-all duration-300">
                        {/* Top Header Badge & Live Enterprise Status */}
                        <div className="flex items-center justify-between gap-3 mb-5">
                            <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3.5 py-1 text-xs font-bold text-slate-700 shadow-2xs">
                                <Sparkles className="h-3.5 w-3.5 text-[#0176D3]" />
                                <span className="text-[#0176D3]">{activeSlide.badge}</span>
                            </div>
                            <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200/60 rounded-full px-3 py-1 text-[11px] font-bold text-emerald-700">
                                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                                <span>Live Enterprise View</span>
                            </div>
                        </div>

                        {/* Title Text */}
                        <h2 className="text-2xl xl:text-3xl font-extrabold tracking-tight text-slate-900 leading-[1.22]">
                            {activeSlide.title.replace(activeSlide.highlight, '')}
                            <span className="text-[#0176D3] underline decoration-[#0176D3]/30 decoration-wavy underline-offset-4">
                                {activeSlide.highlight}
                            </span>
                        </h2>

                        {/* Sub-Title / Description */}
                        <p className="mt-3 text-xs sm:text-sm text-slate-600 leading-relaxed font-normal">
                            {activeSlide.description}
                        </p>

                        {/* CTA Buttons */}
                        <div className="mt-5 flex flex-wrap items-center gap-3">
                            <a
                                href={activeSlide.ctaHref}
                                className="inline-flex items-center justify-center gap-2 rounded-[12px] bg-[#0176D3] px-6 py-2.5 text-xs font-bold text-white shadow-[0_4px_14px_rgba(1,118,211,0.25)] transition hover:bg-[#014486] hover:scale-[1.02] cursor-pointer"
                            >
                                <span>{activeSlide.ctaText}</span>
                            </a>
                            <a
                                href="https://ezsignature.com/#industry-solutions"
                                className="inline-flex items-center justify-center gap-2 rounded-[12px] border border-slate-200 bg-slate-50 px-5 py-2.5 text-xs font-bold text-slate-700 shadow-2xs transition hover:bg-slate-100 hover:text-slate-900 cursor-pointer"
                            >
                                <span>Explore Solutions ↗</span>
                            </a>
                        </div>

                        {/* Interactive Feature Breakdown Box */}
                        <div className="mt-6 pt-5 border-t border-slate-100">
                            <div className="flex items-center justify-between pb-3">
                                <div className="flex items-center gap-2">
                                    <div className="h-2.5 w-2.5 rounded-full bg-red-400" />
                                    <div className="h-2.5 w-2.5 rounded-full bg-amber-400" />
                                    <div className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
                                    <span className="ml-2 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                                        {activeSlide.cardTag}
                                    </span>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                                {activeSlide.features.map((feat, i) => (
                                    <div key={i} className="flex items-center gap-2 rounded-xl bg-slate-50 border border-slate-100 px-3 py-2 text-xs font-medium text-slate-700">
                                        <CheckCircle2 className="h-3.5 w-3.5 shrink-0 text-[#0176D3]" />
                                        <span className="truncate">{feat}</span>
                                    </div>
                                ))}
                            </div>

                            {/* Stat Badge */}
                            <div className="mt-3.5 flex items-center justify-between rounded-xl bg-gradient-to-r from-slate-50 to-blue-50/50 border border-slate-200/80 px-4 py-2.5">
                                <span className="text-xs font-semibold text-slate-600">{activeSlide.stat.label}</span>
                                <span className="text-base font-extrabold text-[#0176D3]">
                                    {activeSlide.stat.value}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bottom Carousel Navigation Controls (Light Theme) */}
                <div className="relative z-10 flex items-center justify-between pt-6 border-t border-slate-200/60 max-w-xl mx-auto w-full">
                    {/* Dots / Indicators */}
                    <div className="flex items-center gap-2">
                        {AUTH_CAROUSEL_SLIDES.map((_, idx) => (
                            <button
                                key={idx}
                                type="button"
                                onClick={() => setCarouselIndex(idx)}
                                className={`h-2.5 rounded-full transition-all duration-300 cursor-pointer ${
                                    carouselIndex === idx ? 'w-8 bg-[#0176D3]' : 'w-2.5 bg-slate-300 hover:bg-slate-400'
                                }`}
                                aria-label={`Go to slide ${idx + 1}`}
                            />
                        ))}
                    </div>

                    {/* Arrow Switchers */}
                    <div className="flex items-center gap-2">
                        <button
                            type="button"
                            onClick={() => setCarouselIndex((prev) => (prev - 1 + AUTH_CAROUSEL_SLIDES.length) % AUTH_CAROUSEL_SLIDES.length)}
                            className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-700 shadow-2xs hover:bg-slate-50 transition cursor-pointer"
                            aria-label="Previous Slide"
                        >
                            <ChevronLeft className="h-4 w-4" />
                        </button>
                        <button
                            type="button"
                            onClick={() => setCarouselIndex((prev) => (prev + 1) % AUTH_CAROUSEL_SLIDES.length)}
                            className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-700 shadow-2xs hover:bg-slate-50 transition cursor-pointer"
                            aria-label="Next Slide"
                        >
                            <ChevronRight className="h-4 w-4" />
                        </button>
                    </div>
                </div>
            </div>

            """

if old_col2_start in content and old_col2_end in content:
    start_pos = content.find(old_col2_start)
    end_pos = content.find(old_col2_end)
    content = content[:start_pos] + new_col2_jsx + content[end_pos:]
    print("✅ Replaced Column 2 JSX with Light Theme & White Card")

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

print("🚀 Successfully updated PhaseOneCommerce.tsx")
