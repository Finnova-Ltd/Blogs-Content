import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Search, 
  Sparkles, 
  ArrowRight, 
  Eye, 
  Heart, 
  Clock, 
  Calendar,
  ShieldCheck,
  ExternalLink
} from 'lucide-react';
import { BLOG_POSTS, getArticleStats, toggleArticleLike } from '../data/blogPosts';

export default function Blog() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [statsMap, setStatsMap] = useState({});

  useEffect(() => {
    window.scrollTo(0, 0);
    document.title = "Salesforce & Enterprise CRM Insights | EZ Consultants";
    const map = {};
    BLOG_POSTS.forEach(post => {
      map[post.slug] = getArticleStats(post.slug);
    });
    setStatsMap(map);
  }, []);

  const handleLikeToggle = (e, slug) => {
    e.preventDefault();
    e.stopPropagation();
    const result = toggleArticleLike(slug);
    setStatsMap(prev => ({
      ...prev,
      [slug]: {
        ...prev[slug],
        likes: (prev[slug]?.likes || 0) + result.delta,
        isLiked: result.isLiked
      }
    }));
  };

  const categories = [
    { label: "All Insights", value: "All", count: BLOG_POSTS.length },
    { label: "Salesforce News", value: "Salesforce Ecosystem News", count: BLOG_POSTS.filter(p => p.category && (p.category.includes("News") || p.category.includes("Ecosystem"))).length },
    { label: "Enterprise AI & Cloud", value: "Enterprise AI & Cloud", count: BLOG_POSTS.filter(p => p.category && (p.category.includes("AI") || p.category.includes("Cloud"))).length },
    { label: "CRM Strategy", value: "CRM Architecture", count: BLOG_POSTS.filter(p => p.category && (p.category.includes("Strategy") || p.category.includes("Architecture"))).length }
  ];

  const filteredPosts = BLOG_POSTS.filter(post => {
    const matchesSearch = searchQuery === '' || 
      post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (post.tags && post.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase())));

    const matchesCategory = selectedCategory === 'All' || post.category === selectedCategory ||
      (selectedCategory === 'Salesforce Ecosystem News' && (post.category.includes('News') || post.category.includes('Ecosystem'))) ||
      (selectedCategory === 'Enterprise AI & Cloud' && (post.category.includes('AI') || post.category.includes('Cloud'))) ||
      (selectedCategory === 'CRM Architecture' && (post.category.includes('Strategy') || post.category.includes('Architecture')));

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 font-sans">
      
      {/* 1. FULL-WIDTH EDGE-TO-EDGE HERO HEADER BANNER (PRO CRM Design) */}
      <section className="relative w-full bg-[#07182c] text-white py-14 lg:py-20 overflow-hidden shadow-2xl">
        
        {/* PRO CRM High-Tech Circuit / Cloud Network Background Photo */}
        <div 
          className="absolute inset-0 bg-cover bg-center opacity-20 filter blur-xs scale-105 pointer-events-none"
          style={{ backgroundImage: `url(https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1800&q=80)` }}
        />

        {/* Deep Navy Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#07182c]/85 via-[#07182c]/95 to-[#07182c] pointer-events-none" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-8 z-10 space-y-6">
          
          {/* Top Tag & buy.nsw Accreditation Pill */}
          <div className="flex flex-wrap items-center gap-3">
            <span className="px-3.5 py-1.5 rounded-full bg-[#0077c8]/30 border border-[#0077c8]/60 text-cyan-300 text-xs font-bold uppercase tracking-wider flex items-center gap-1.5 shadow-sm">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
              <span>Daily Enterprise Feed</span>
            </span>
            
            <a 
              href="https://buy.nsw.gov.au/supplier/profile/180179" 
              target="_blank" 
              rel="noopener noreferrer"
              className="px-3.5 py-1.5 rounded-full bg-slate-900/90 border border-slate-700 text-slate-300 hover:text-white text-xs font-semibold inline-flex items-center gap-1.5 transition-colors shadow-sm"
            >
              <img src="/images/nsw-government-approved-supplier.svg" alt="NSW Gov" className="w-3.5 h-4 object-contain" />
              <span>buy.nsw Approved Supplier (ID: 180179) ↗</span>
            </a>
          </div>

          {/* Large Serif Title */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-[1.15] font-serif max-w-4xl">
            Salesforce, Agentforce &amp; Cloud Advisory
          </h1>

          {/* Subtitle */}
          <p className="text-slate-300 text-base sm:text-lg max-w-3xl leading-relaxed font-serif">
            In-depth technical breakdowns, release analyses, and implementation blueprints curated by certified Australian Salesforce architects and accredited public sector consultants.
          </p>

          {/* Search Bar */}
          <div className="pt-2 max-w-2xl">
            <div className="relative flex items-center">
              <Search className="w-5 h-5 text-slate-400 absolute left-4 pointer-events-none" />
              <input 
                type="text" 
                placeholder="Search Salesforce features, Data Cloud, Agentforce AI, compliance..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3.5 rounded-2xl bg-slate-900/90 border border-slate-700 text-white placeholder-slate-400 focus:outline-none focus:border-[#0077c8] focus:ring-2 focus:ring-[#0077c8]/30 text-sm sm:text-base shadow-xl transition-all"
              />
            </div>
          </div>

        </div>
      </section>

      {/* 2. MAIN CONTENT BODY: CATEGORIES + 3-COLUMN CARDS FEED */}
      <main className="max-w-7xl mx-auto px-4 sm:px-8 py-12 space-y-10">
        
        {/* Category Filter Pills */}
        <div className="flex items-center gap-3 flex-wrap border-b border-slate-200 pb-4">
          {categories.map((cat, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedCategory(cat.value)}
              className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all flex items-center gap-2 ${
                selectedCategory === cat.value
                  ? "bg-[#07182c] text-white shadow-md shadow-blue-900/20"
                  : "bg-white border border-slate-200 text-slate-700 hover:border-[#0077c8] hover:text-[#0077c8]"
              }`}
            >
              <span>{cat.label}</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-semibold">
                {cat.count}
              </span>
            </button>
          ))}
        </div>

        {/* 3-Column Blog Feed Grid with Distinct Curated Images */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredPosts.map((post, idx) => {
            const stats = statsMap[post.slug] || { views: post.baseViews, likes: post.baseLikes, isLiked: false };
            return (
              <article 
                key={post.id || idx} 
                className="group flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl hover:border-[#0077c8] transition-all duration-300 transform hover:-translate-y-1"
              >
                {/* Card Cover Image */}
                <div className="relative aspect-[16/9] overflow-hidden bg-slate-950">
                  <img 
                    src={post.heroImage} 
                    alt={post.title} 
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent"></div>
                  <div className="absolute top-3 left-3">
                    <span className="px-2.5 py-1 rounded-md bg-[#07182c]/90 border border-cyan-400/40 text-cyan-300 text-[10px] font-extrabold uppercase tracking-wide backdrop-blur-md">
                      {post.category}
                    </span>
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-6 flex-1 flex flex-col justify-between space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-center gap-3 text-xs text-slate-500">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5 text-[#0077c8]" />
                        {post.formattedDate}
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        {post.readTime}
                      </span>
                    </div>

                    <h2 className="text-base sm:text-lg font-bold text-slate-900 group-hover:text-[#0077c8] transition-colors line-clamp-2 leading-snug font-serif">
                      <Link to={`/blog/${post.slug}`}>
                        {post.title}
                      </Link>
                    </h2>

                    <p className="text-slate-600 text-xs sm:text-sm line-clamp-3 leading-relaxed">
                      {post.excerpt}
                    </p>
                  </div>

                  {/* Footer Telemetry & Read Action */}
                  <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                    <div className="flex items-center gap-3 text-xs text-slate-500">
                      <span className="flex items-center gap-1">
                        <Eye className="w-3.5 h-3.5 text-slate-400" />
                        {stats.views}
                      </span>
                      <button 
                        onClick={(e) => handleLikeToggle(e, post.slug)}
                        className={`flex items-center gap-1 hover:text-red-500 transition-colors ${stats.isLiked ? 'text-red-500 font-bold' : ''}`}
                      >
                        <Heart className={`w-3.5 h-3.5 ${stats.isLiked ? 'fill-red-500' : ''}`} />
                        {stats.likes}
                      </button>
                    </div>

                    <Link 
                      to={`/blog/${post.slug}`} 
                      className="text-xs font-bold text-[#0077c8] hover:underline inline-flex items-center gap-1 group-hover:translate-x-1 transition-transform"
                    >
                      <span>Read article</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              </article>
            );
          })}
        </div>

        {filteredPosts.length === 0 && (
          <div className="py-20 text-center space-y-3">
            <h3 className="text-xl font-bold text-slate-900">No matching articles found</h3>
            <p className="text-slate-500 text-sm">Try adjusting your search query or category filter.</p>
            <button 
              onClick={() => { setSearchQuery(""); setSelectedCategory("All"); }}
              className="mt-2 text-sm font-bold text-[#0077c8] hover:underline"
            >
              Reset Filters
            </button>
          </div>
        )}

        {/* Bottom CTA Consultation Banner */}
        <div className="rounded-2xl p-8 sm:p-12 bg-gradient-to-r from-slate-950 via-[#07182c] to-slate-950 border-2 border-[#0077c8]/50 text-white flex flex-col md:flex-row items-center justify-between gap-8 shadow-xl">
          <div className="space-y-2 max-w-xl text-center md:text-left">
            <div className="text-xs uppercase tracking-wider text-cyan-400 font-bold">Accredited Enterprise Advisory</div>
            <h3 className="text-2xl sm:text-3xl font-extrabold text-white">Need Customized Architecture for Your Salesforce Org?</h3>
            <p className="text-slate-300 text-sm">Schedule a complimentary technical health check with our certified Australian solutions architects.</p>
          </div>
          <Link 
            to="/contact-us"
            className="gradient-button btn-shine px-8 py-3.5 rounded-xl font-bold text-sm whitespace-nowrap shadow-xl shadow-blue-500/20"
          >
            Book Consultation
          </Link>
        </div>

      </main>

    </div>
  );
}
