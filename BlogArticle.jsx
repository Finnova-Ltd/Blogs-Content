import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Share2, 
  ThumbsUp, 
  MessageSquare, 
  Repeat, 
  Send, 
  ArrowRight, 
  ExternalLink,
  Phone,
  Bell,
  Mail,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react';
import { BLOG_POSTS, getArticleStats, incrementArticleView, toggleArticleLike } from '../data/blogPosts';

export default function BlogArticle() {
  const { slug } = useParams();
  const cleanSlug = slug ? slug.replace(/\.html$/, '') : '';
  const post = BLOG_POSTS.find(p => p.slug === cleanSlug || p.id === cleanSlug) || BLOG_POSTS[0];
  const [stats, setStats] = useState({ views: 1420, likes: 118, isLiked: false });
  const [isTocOpen, setIsTocOpen] = useState(true);
  const [subscriberName, setSubscriberName] = useState('');
  const [subscriberEmail, setSubscriberEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  useEffect(() => {
    window.scrollTo(0, 0);

    if (post) {
      document.title = `${post.title} | EZ Consultants`;
      incrementArticleView(post.slug);
      setStats(getArticleStats(post.slug));

      const schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": post.title,
        "description": post.excerpt,
        "author": {
          "@type": "Person",
          "name": post.author.name,
          "jobTitle": post.author.title
        },
        "publisher": {
          "@type": "Organization",
          "name": "EZ Consultants",
          "url": "https://ezconsultants.com.au",
          "logo": "https://ezconsultants.com.au/images/nsw-government-approved-supplier.svg"
        },
        "datePublished": post.publishedDate,
        "mainEntityOfPage": `https://ezconsultants.com.au/blog/${post.slug}`
      };

      const script = document.createElement('script');
      script.type = 'application/ld+json';
      script.id = 'json-ld-article-schema';
      script.text = JSON.stringify(schema);
      document.head.appendChild(script);

      return () => {
        const existing = document.getElementById('json-ld-article-schema');
        if (existing) document.head.removeChild(existing);
      };
    }
  }, [post]);

  const handleLike = () => {
    if (!post) return;
    const result = toggleArticleLike(post.slug);
    setStats(prev => ({
      ...prev,
      likes: prev.likes + result.delta,
      isLiked: result.isLiked
    }));
  };

  const handleSubscribe = (e) => {
    e.preventDefault();
    if (subscriberEmail) {
      setSubscribed(true);
      setTimeout(() => setSubscribed(false), 5000);
      setSubscriberName('');
      setSubscriberEmail('');
    }
  };

  const copyToClipboard = () => {
    if (typeof window !== 'undefined') {
      navigator.clipboard.writeText(window.location.href);
      alert('Advisory link copied to clipboard!');
    }
  };

  const scrollToSection = (e, id) => {
    e.preventDefault();
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  if (!post) return null;

  // Recent articles for sidebar & bottom grid
  const recentArticles = BLOG_POSTS
    .filter(p => p.slug !== post.slug)
    .slice(0, 4);

  const relatedArticles = BLOG_POSTS
    .filter(p => p.slug !== post.slug)
    .slice(0, 3);

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans">
      
      {/* 1. HIGH-FIDELITY FULL-BLEED HERO HEADER BANNER (Matching Image 1 Pixel-Perfect) */}
      <section className="relative bg-[#07182c] text-white py-12 lg:py-16 overflow-hidden shadow-2xl">
        
        {/* Subtle blurred backdrop photo with cyber texture */}
        <div 
          className="absolute inset-0 bg-cover bg-center opacity-15 filter blur-xs scale-105 pointer-events-none"
          style={{ backgroundImage: `url(${post.heroImage})` }}
        />

        {/* Deep Navy Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#07182c]/80 via-[#07182c]/95 to-[#07182c] pointer-events-none" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-8 z-10 space-y-6">
          
          {/* Breadcrumb & Social Share Row */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-700/60 pb-5">
            
            {/* Breadcrumbs */}
            <nav className="flex items-center gap-2 text-xs sm:text-sm text-slate-300 font-medium flex-wrap">
              <Link to="/" className="text-cyan-400 hover:underline">Home</Link>
              <span className="text-slate-500">/</span>
              <Link to="/blog" className="text-cyan-400 hover:underline">Blog &amp; Insights</Link>
              <span className="text-slate-500">/</span>
              <span className="text-slate-300 font-semibold">{post.category}</span>
            </nav>

            {/* Social Share Round Pills (Image 1 Format) */}
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-white/20">
              <span className="text-[11px] font-extrabold uppercase tracking-wider text-slate-200 mr-1">Share:</span>
              <a
                href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(typeof window !== 'undefined' ? window.location.href : '')}`}
                target="_blank"
                rel="noreferrer"
                className="w-7 h-7 rounded-full bg-[#0a66c2] hover:scale-110 transition-transform flex items-center justify-center text-white text-xs font-black shadow-sm"
                title="Share on LinkedIn"
              >in</a>
              <a
                href={`https://twitter.com/intent/tweet?url=${encodeURIComponent(typeof window !== 'undefined' ? window.location.href : '')}&text=${encodeURIComponent(post.title)}`}
                target="_blank"
                rel="noreferrer"
                className="w-7 h-7 rounded-full bg-black hover:scale-110 transition-transform flex items-center justify-center text-white text-xs font-bold shadow-sm"
                title="Share on X"
              >𝕏</a>
              <a
                href={`https://api.whatsapp.com/send?text=${encodeURIComponent(post.title + ' ' + (typeof window !== 'undefined' ? window.location.href : ''))}`}
                target="_blank"
                rel="noreferrer"
                className="w-7 h-7 rounded-full bg-[#25D366] hover:scale-110 transition-transform flex items-center justify-center text-white text-xs shadow-sm"
                title="Share on WhatsApp"
              >💬</a>
              <button
                type="button"
                onClick={copyToClipboard}
                className="w-7 h-7 rounded-full bg-slate-700 hover:bg-slate-600 hover:scale-110 transition-transform flex items-center justify-center text-white text-xs shadow-sm"
                title="Copy Link"
              >🔗</button>
            </div>
          </div>

          {/* Metadata Badges Row */}
          <div className="flex flex-wrap items-center gap-3 text-xs">
            <span className="px-3 py-1 rounded-md bg-slate-800 text-slate-300 font-semibold flex items-center gap-1.5">
              <span>📅</span>
              <span>Published Today • {post.formattedDate}</span>
            </span>
            <span className="px-2.5 py-1 rounded-md bg-[#eab308] text-slate-950 font-black tracking-wider uppercase">
              🔥 TRENDING
            </span>
            <span className="px-2.5 py-1 rounded-md bg-[#10b981] text-slate-950 font-black tracking-wider uppercase">
              {post.category}
            </span>
            <span className="text-slate-300 font-medium">
              By <strong className="text-white">{post.author.name}</strong> • {post.readTime}
            </span>
            <a 
              href="https://buy.nsw.gov.au/supplier/profile/180179" 
              target="_blank" 
              rel="noopener noreferrer"
              className="px-2.5 py-1 rounded-md bg-[#0077c8] text-white font-bold inline-flex items-center gap-1 text-[11px] hover:bg-[#005a9c]"
            >
              <span>buy.nsw Approved (ID: 180179) ↗</span>
            </a>
          </div>

          {/* Large Serif / Display Title */}
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight leading-[1.2] max-w-5xl font-serif">
            {post.title}
          </h1>

          {/* Excerpt Subtitle */}
          <p className="text-slate-300 text-base sm:text-lg leading-relaxed max-w-4xl font-serif">
            {post.excerpt}
          </p>

          {/* Carousel Dots Indicator */}
          <div className="flex items-center gap-2 pt-2 text-slate-500">
            <span className="w-2.5 h-2.5 rounded-full bg-white"></span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
          </div>

        </div>
      </section>

      {/* 2. MAIN 2-COLUMN LAYOUT: ARTICLE BODY (LEFT) + STICKY SIDEBAR (RIGHT) */}
      <main className="max-w-7xl mx-auto px-4 sm:px-8 py-12 lg:py-16">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          
          {/* LEFT 8-COLUMN: MAIN ARTICLE CARD & ENGAGEMENT */}
          <div className="lg:col-span-8 space-y-8">
            
            {/* White Paper Article Card */}
            <article className="bg-white rounded-2xl border border-slate-200 p-8 sm:p-12 shadow-sm space-y-8">
              
              {/* HTML Content (Executive Summary + Bullet Points + Why It Matters + Source) */}
              <div 
                className="article-body-content text-slate-800 text-base leading-relaxed space-y-6 font-serif"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />

              {/* LinkedIn / Social Engagement Reactions Bar (Image 1 Format) */}
              <div className="pt-6 border-t border-slate-100 space-y-4 font-sans">
                
                {/* Stats Row with Avatar Icons */}
                <div className="flex items-center justify-between text-xs text-slate-500 pb-3 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <div className="flex -space-x-1.5 overflow-hidden">
                      <span className="w-5 h-5 rounded-full bg-amber-400 border-2 border-white flex items-center justify-center text-[10px]">👍</span>
                      <span className="w-5 h-5 rounded-full bg-blue-500 border-2 border-white flex items-center justify-center text-[10px] text-white">👏</span>
                      <span className="w-5 h-5 rounded-full bg-emerald-500 border-2 border-white flex items-center justify-center text-[10px] text-white">❤️</span>
                    </div>
                    <span className="font-semibold text-slate-700">{stats.likes}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span>0 comments</span>
                    <span>•</span>
                    <span>{stats.views.toLocaleString()} views</span>
                    <span>•</span>
                    <span>0 shares</span>
                  </div>
                </div>

                {/* Reaction Actions Toolbar */}
                <div className="flex items-center justify-between flex-wrap gap-2 text-xs font-bold text-slate-600">
                  <button 
                    onClick={handleLike}
                    className={`flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-slate-100 transition-colors ${stats.isLiked ? 'text-blue-600 bg-blue-50' : ''}`}
                  >
                    <ThumbsUp className={`w-4 h-4 ${stats.isLiked ? 'fill-blue-600' : ''}`} />
                    <span>{stats.isLiked ? 'Liked' : 'Like'}</span>
                  </button>

                  <button className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-slate-100 transition-colors">
                    <MessageSquare className="w-4 h-4" />
                    <span>Comment</span>
                  </button>

                  <button onClick={copyToClipboard} className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-slate-100 transition-colors">
                    <Repeat className="w-4 h-4" />
                    <span>Repost</span>
                  </button>

                  <button onClick={copyToClipboard} className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-slate-100 transition-colors">
                    <Send className="w-4 h-4" />
                    <span>Send</span>
                  </button>
                </div>

              </div>

            </article>

            {/* TAGS ROW (Image 1 Format) */}
            <div className="flex items-center gap-2 flex-wrap text-xs text-slate-600 font-sans">
              <span className="font-extrabold uppercase text-slate-900">TAGS:</span>
              {post.tags.map((tag, idx) => (
                <span 
                  key={idx} 
                  className="px-3 py-1 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold border border-slate-200 transition-colors cursor-pointer"
                >
                  {tag}
                </span>
              ))}
            </div>

            {/* "NEVER MISS AN ALERT" NEWSLETTER BOX (Image 1 Format) */}
            <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6 font-sans">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white shrink-0 shadow-md shadow-blue-500/20">
                  <Bell className="w-7 h-7 animate-bounce" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-lg font-bold text-slate-900">Never Miss an Advisory</h3>
                  <p className="text-xs text-slate-500 max-w-sm">
                    Sign up for the latest Salesforce release notes, Agentforce AI audits, and Australian compliance security alerts.
                  </p>
                </div>
              </div>

              {subscribed ? (
                <div className="px-5 py-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Subscribed successfully! Thank you.</span>
                </div>
              ) : (
                <form onSubmit={handleSubscribe} className="flex flex-col sm:flex-row items-center gap-2.5 w-full md:w-auto">
                  <input 
                    type="text" 
                    placeholder="Your name" 
                    value={subscriberName}
                    onChange={(e) => setSubscriberName(e.target.value)}
                    className="px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs w-full sm:w-32 focus:outline-none focus:border-[#0077c8]"
                  />
                  <input 
                    type="email" 
                    required 
                    placeholder="Email *" 
                    value={subscriberEmail}
                    onChange={(e) => setSubscriberEmail(e.target.value)}
                    className="px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs w-full sm:w-44 focus:outline-none focus:border-[#0077c8]"
                  />
                  <button 
                    type="submit" 
                    className="gradient-button btn-shine text-xs font-bold px-5 py-2.5 rounded-xl whitespace-nowrap w-full sm:w-auto"
                  >
                    Sign up for alerts
                  </button>
                </form>
              )}
            </div>

            {/* ENTERPRISE SUPPORT CALLOUT BANNER (Image 1 Format) */}
            <div className="p-8 rounded-2xl bg-gradient-to-r from-slate-950 via-[#001c4f] to-slate-950 border-2 border-[#0077c8]/60 text-white flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl font-sans">
              <div className="space-y-2">
                <div className="text-[11px] uppercase tracking-wider text-cyan-400 font-bold">
                  EZ CONSULTANTS ENTERPRISE SUPPORT
                </div>
                <h3 className="text-xl sm:text-2xl font-extrabold text-white">
                  Want to discuss your Salesforce or AI requirements?
                </h3>
                <p className="text-xs sm:text-sm text-slate-300 max-w-xl">
                  Book a complimentary 30-minute discovery session with our certified Australian CRM and cloud security architects.
                </p>
              </div>

              <div className="flex items-center gap-3 shrink-0 flex-wrap">
                <Link 
                  to="/contact-us"
                  className="gradient-button btn-shine text-xs font-bold px-6 py-3 rounded-xl whitespace-nowrap shadow-lg shadow-blue-500/20"
                >
                  Book Consultation ↗
                </Link>
                <a 
                  href="mailto:info@ezconsultants.com.au"
                  className="px-5 py-3 rounded-xl bg-slate-900 border border-slate-700 text-xs font-bold text-slate-200 hover:text-white transition whitespace-nowrap"
                >
                  Contact Specialists
                </a>
              </div>
            </div>

          </div>

          {/* RIGHT 4-COLUMN: STICKY SIDEBAR (Image 1 Format) */}
          <aside className="lg:col-span-4 sticky top-24 space-y-6 font-sans">
            
            {/* 1. KEY HIGHLIGHTS TIMELINE WIDGET (Crimson Header - Matching Image 1) */}
            <div className="rounded-2xl overflow-hidden shadow-sm border border-slate-200 bg-white">
              {/* Crimson Header Bar */}
              <div className="bg-[#990000] text-white px-5 py-4 flex items-center justify-between">
                <h3 className="text-base font-black tracking-tight text-white m-0">Highlights</h3>
                <span className="text-[10px] font-extrabold tracking-widest uppercase text-white/90">
                  IN THIS ARTICLE
                </span>
              </div>

              {/* Timeline Body */}
              <div className="p-5 space-y-4">
                <div className="text-xs font-bold text-slate-600 flex items-center gap-1.5">
                  <span className="font-extrabold text-slate-900">—</span>
                  <span>{post.formattedDate}</span>
                </div>

                {/* Vertical Spine with Red Dots */}
                <div className="border-l-2 border-slate-200 ml-2 pl-4 space-y-5">
                  {post.highlights.map((hl, idx) => (
                    <div 
                      key={idx} 
                      onClick={(e) => scrollToSection(e, hl.id)}
                      className="relative group cursor-pointer"
                    >
                      {/* Red Dot Marker */}
                      <span className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-[#990000] shadow-[0_0_0_3px_#ffffff,0_0_0_5px_#fee2e2] group-hover:scale-125 transition-transform" />
                      
                      {/* Timestamp */}
                      <div className="text-[10px] font-extrabold text-[#990000] uppercase tracking-wide">
                        {hl.time}
                      </div>

                      {/* Title */}
                      <div className="text-xs font-bold text-slate-900 group-hover:text-[#990000] transition-colors leading-snug">
                        {hl.title}
                      </div>

                      {/* Blurb */}
                      <p className="text-[11px] text-slate-500 leading-snug mt-0.5">
                        {hl.text}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 2. RECENT ADVISORIES WIDGET (Matching Image 1) */}
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-900">
                  RECENT ADVISORIES
                </h3>
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" title="Live Updates" />
              </div>

              <div className="space-y-3.5">
                {recentArticles.map((ra, idx) => (
                  <Link 
                    key={ra.id || idx} 
                    to={`/blog/${ra.slug}`}
                    className="group flex items-center gap-3 pb-3 border-b border-slate-50 last:border-0 last:pb-0"
                  >
                    <img 
                      src={ra.heroImage} 
                      alt={ra.title} 
                      className="w-12 h-12 rounded-lg object-cover shrink-0 border border-slate-100 group-hover:scale-105 transition-transform"
                    />
                    <div className="min-w-0 flex-1">
                      <h4 className="text-xs font-bold text-slate-900 group-hover:text-[#0077c8] transition-colors line-clamp-2 leading-snug">
                        {ra.title}
                      </h4>
                      <span className="text-[10px] text-slate-400 mt-0.5 block">
                        {ra.formattedDate}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            {/* 3. DIRECT ENGINEERING SUPPORT BOX (Matching Image 1) */}
            <div className="bg-[#0A2540] rounded-2xl p-6 text-white shadow-lg space-y-3">
              <div className="text-[10px] font-extrabold uppercase tracking-widest text-cyan-400">
                DIRECT ENGINEERING SUPPORT
              </div>
              <h4 className="text-base font-extrabold text-white leading-snug">
                Speak with our Australian Salesforce architects
              </h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                Complimentary 30-min discovery session for Australian enterprises and public sector agencies.
              </p>
              <Link
                to="/contact-us"
                className="w-full py-2.5 rounded-full bg-white text-[#0A2540] hover:bg-slate-100 font-extrabold text-xs flex items-center justify-center gap-2 shadow-md transition"
              >
                <span>📞 Speak with Specialists</span>
              </Link>
            </div>

          </aside>

        </div>

        {/* 3. RELATED ARTICLES 3-COLUMN GRID (Matching Image 1 Bottom Section) */}
        <section className="mt-16 pt-12 border-t border-slate-200 space-y-8 font-sans">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Related Articles</h2>
            <Link to="/blog" className="text-xs sm:text-sm font-bold text-[#0077c8] hover:underline flex items-center gap-1">
              <span>View All Articles</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {relatedArticles.map((rel, idx) => (
              <article key={rel.id || idx} className="group flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-all">
                <div className="relative aspect-[16/9] overflow-hidden bg-slate-950">
                  <img 
                    src={rel.heroImage} 
                    alt={rel.title} 
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                  />
                </div>
                <div className="p-5 flex-1 flex flex-col justify-between space-y-3">
                  <div className="space-y-2">
                    <span className="text-[10px] text-slate-400 font-semibold">{rel.formattedDate}</span>
                    <h3 className="text-sm font-bold text-slate-900 group-hover:text-[#0077c8] transition-colors line-clamp-2 leading-snug">
                      <Link to={`/blog/${rel.slug}`}>{rel.title}</Link>
                    </h3>
                  </div>
                  <Link to={`/blog/${rel.slug}`} className="text-xs font-bold text-[#0077c8] hover:underline inline-flex items-center gap-1">
                    <span>Read article</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </section>

      </main>

    </div>
  );
}
