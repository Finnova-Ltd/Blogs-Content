#!/usr/bin/env python3
"""
Update eSignaturesonline Blog Layout, Roboto Typography, Table Pricing & Fixed Col 2
"""

import os
import re
import subprocess

ESIGN_DIR = "/Users/robinbakshi/Documents/GitHub/eSignaturesonline"
BLOG_ARTICLE_JSX = os.path.join(ESIGN_DIR, "frontend", "src", "pages", "BlogArticle.jsx")
BLOG_POSTS_JS = os.path.join(ESIGN_DIR, "frontend", "src", "data", "blogPosts.js")

JSX_CONTENT = '''import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { BLOG_POSTS, getArticleStats, incrementArticleView, toggleArticleLike } from '../data/blogPosts';
import Header from '../components/Header';
import Footer from '../components/Footer';

// Curated high-definition light hero background carousel images
const HERO_CAROUSEL_IMAGES = [
  "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1600&q=80",
  "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=1600&q=80",
  "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1600&q=80",
  "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1600&q=80"
];

export default function BlogArticle() {
  const { slug } = useParams();
  const post = BLOG_POSTS.find(p => p.slug === slug || (p.aliases && p.aliases.includes(slug)) || p.id === slug);
  const [stats, setStats] = useState({ views: 0, likes: 0, isLiked: false });
  const [isTocOpen, setIsTocOpen] = useState(true);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [activeHeroIndex, setActiveHeroIndex] = useState(0);

  // 1. Reading Progress Bar on Scroll
  useEffect(() => {
    const handleScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        const currentProgress = (window.scrollY / totalHeight) * 100;
        setScrollProgress(Math.min(100, Math.max(0, currentProgress)));
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // 2. Background Image Carousel in Header (Cycles every 6 seconds)
  useEffect(() => {
    const timer = setInterval(() => {
      setActiveHeroIndex(prev => (prev + 1) % HERO_CAROUSEL_IMAGES.length);
    }, 6000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    window.scrollTo(0, 0);

    if (post) {
      document.title = `${post.title} | EZ Signature`;
      incrementArticleView(post.slug);
      setStats(getArticleStats(post.slug));

      const schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.excerpt,
        "author": {
          "@type": "Organization",
          "name": post.author.name,
          "jobTitle": post.author.title
        },
        "publisher": {
          "@type": "Organization",
          "name": "EZ Signature",
          "url": "https://ezsignature.com",
          "logo": "https://ezsignature.com/brand/ezsignature-au-logo.png"
        },
        "datePublished": post.publishedDate,
        "mainEntityOfPage": `https://ezsignature.com/blog/${post.slug}`
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

  const copyToClipboard = () => {
    navigator.clipboard.writeText(window.location.href);
    alert('Article link copied to clipboard!');
  };

  const scrollToSection = (e, id) => {
    e.preventDefault();
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      el.classList.remove('section-highlight');
      void el.offsetWidth;
      el.classList.add('section-highlight');
    }
  };

  if (!post) {
    return (
      <div style={{ minHeight: '100vh', background: '#f8fafc', color: '#0f172a', display: 'flex', flexDirection: 'column', fontFamily: "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif" }}>
        <Header />
        <div style={{ padding: '80px 24px', textAlign: 'center', flex: 1 }}>
          <h2>Article Not Found</h2>
          <p style={{ color: '#64748b' }}>The requested article does not exist or has been moved.</p>
          <Link to="/blog" style={{ color: '#0176D3', fontWeight: 700, marginTop: '16px', display: 'inline-block' }}>← Back to Blog Feed</Link>
        </div>
        <Footer />
      </div>
    );
  }

  const recentArticles = BLOG_POSTS
    .filter(p => p.slug !== post.slug)
    .sort((a, b) => new Date(b.publishedDate) - new Date(a.publishedDate))
    .slice(0, 4);

  return (
    <div style={{
      minHeight: '100vh',
      background: '#f8fafc',
      color: '#0f172a',
      fontFamily: "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif"
    }}>
      {/* 🚀 Reading Progress Bar (Fixed Top) */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: `${scrollProgress}%`,
        height: '3.5px',
        background: 'linear-gradient(90deg, #0176D3 0%, #00C49F 100%)',
        zIndex: 99999,
        transition: 'width 0.1s ease-out',
        boxShadow: '0 0 10px rgba(1, 118, 211, 0.7)'
      }} />

      {/* Universal Navigation Header */}
      <Header />

      {/* High-Fidelity Hero Header Banner with Background Image Carousel */}
      <section style={{
        position: 'relative',
        backgroundColor: '#0A2540',
        color: '#ffffff',
        padding: '44px 0 36px',
        overflow: 'hidden',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)'
      }}>
        {/* Background Image Carousel Slides */}
        {HERO_CAROUSEL_IMAGES.map((imgUrl, idx) => (
          <div
            key={idx}
            style={{
              position: 'absolute',
              top: '-20px', left: '-20px', right: '-20px', bottom: '-20px',
              backgroundImage: `url(${idx === 0 && post.heroImage ? post.heroImage : imgUrl})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center 30%',
              filter: 'blur(3px) brightness(0.62) saturate(1.1)',
              transform: 'scale(1.04)',
              opacity: activeHeroIndex === idx ? 1 : 0,
              transition: 'opacity 1.2s ease-in-out',
              zIndex: 1
            }}
          />
        ))}

        {/* Navy Gradient Overlay */}
        <div style={{
          position: 'absolute',
          top: 0, left: 0, right: 0, bottom: 0,
          background: 'linear-gradient(180deg, rgba(10, 37, 64, 0.82) 0%, rgba(10, 37, 64, 0.96) 100%)',
          zIndex: 2
        }} />

        {/* Carousel Indicators / Dots */}
        <div style={{
          position: 'absolute',
          bottom: '12px',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: '8px',
          zIndex: 4
        }}>
          {HERO_CAROUSEL_IMAGES.map((_, dotIdx) => (
            <button
              key={dotIdx}
              type="button"
              onClick={() => setActiveHeroIndex(dotIdx)}
              style={{
                width: activeHeroIndex === dotIdx ? '20px' : '6px',
                height: '6px',
                borderRadius: '3px',
                background: activeHeroIndex === dotIdx ? '#00C49F' : 'rgba(255, 255, 255, 0.4)',
                border: 'none',
                cursor: 'pointer',
                padding: 0,
                transition: 'all 0.3s ease'
              }}
              title={`Slide ${dotIdx + 1}`}
            />
          ))}
        </div>

        {/* Content Box */}
        <div style={{
          position: 'relative',
          zIndex: 3,
          maxWidth: '1380px',
          margin: '0 auto',
          padding: '0 24px'
        }}>
          {/* Top Breadcrumb & Share Toolbar */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '14px',
            marginBottom: '16px'
          }}>
            {/* Breadcrumb */}
            <nav style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', fontSize: '0.84rem', color: '#E2E8F0', fontWeight: 500 }}>
              <Link to="/" style={{ color: '#93C5FD', textDecoration: 'none' }}>Home</Link>
              <span>/</span>
              <Link to="/blog" style={{ color: '#93C5FD', textDecoration: 'none' }}>Blog &amp; Legal Insights</Link>
              <span>/</span>
              <span style={{ color: '#CBD5E1', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '360px' }}>{post.title}</span>
            </nav>

            {/* Social Share Floating Pill */}
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              background: 'rgba(255, 255, 255, 0.95)',
              padding: '4px 12px',
              borderRadius: '50px',
              boxShadow: '0 4px 14px rgba(0, 0, 0, 0.15)'
            }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#0f172a', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Share:</span>
              
              <a
                href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`}
                target="_blank"
                rel="noreferrer"
                title="Share on LinkedIn"
                style={{ width: '26px', height: '26px', borderRadius: '50%', background: '#0a66c2', display: 'grid', placeItems: 'center', color: '#ffffff', textDecoration: 'none', fontSize: '0.75rem', fontWeight: 700 }}
              >in</a>

              <a
                href={`https://twitter.com/intent/tweet?url=${encodeURIComponent(window.location.href)}&text=${encodeURIComponent(post.title)}`}
                target="_blank"
                rel="noreferrer"
                title="Share on X"
                style={{ width: '26px', height: '26px', borderRadius: '50%', background: '#000000', display: 'grid', placeItems: 'center', color: '#ffffff', textDecoration: 'none', fontSize: '0.72rem', fontWeight: 700 }}
              >𝕏</a>

              <a
                href={`https://api.whatsapp.com/send?text=${encodeURIComponent(post.title + ' ' + window.location.href)}`}
                target="_blank"
                rel="noreferrer"
                title="Share on WhatsApp"
                style={{ width: '26px', height: '26px', borderRadius: '50%', background: '#25D366', display: 'grid', placeItems: 'center', color: '#ffffff', textDecoration: 'none', fontSize: '0.78rem', fontWeight: 700 }}
              >💬</a>

              <button
                type="button"
                onClick={copyToClipboard}
                title="Copy Link"
                style={{ width: '26px', height: '26px', borderRadius: '50%', background: '#475569', display: 'grid', placeItems: 'center', color: '#ffffff', border: 'none', cursor: 'pointer', fontSize: '0.75rem' }}
              >🔗</button>
            </div>
          </div>

          {/* Category Badge */}
          <div style={{ display: 'inline-block', background: '#0176D3', color: '#ffffff', padding: '4px 12px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: '12px' }}>
            {post.category}
          </div>

          {/* Headline H1 (Roboto Specimen: 28px) */}
          <h1 style={{
            fontFamily: "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif",
            fontSize: 'clamp(22px, 2.3vw, 28px)',
            fontWeight: 700,
            lineHeight: 1.3,
            margin: '0 0 12px 0',
            color: '#ffffff',
            letterSpacing: '-0.01em',
            textShadow: '0 2px 8px rgba(0, 0, 0, 0.4)'
          }}>
            {post.title}
          </h1>

          {/* Excerpt Subtitle */}
          <p style={{
            fontFamily: "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif",
            fontSize: '0.98rem',
            color: '#E2E8F0',
            lineHeight: 1.55,
            maxWidth: '960px',
            margin: '0 0 18px 0',
            fontWeight: 400
          }}>
            {post.excerpt}
          </p>

          {/* Author, Date, Reading Time & Likes Bar */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '14px',
            fontSize: '0.82rem',
            color: '#CBD5E1'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '1rem' }}>⚖️</span>
              <strong style={{ color: '#ffffff' }}>{post.author.name}</strong>
              <span>({post.author.title})</span>
            </div>
            <span>•</span>
            <span>📅 {post.formattedDate}</span>
            <span>•</span>
            <span>⏱️ {post.readTime}</span>
            <span>•</span>
            <span>👁️ {stats.views.toLocaleString()} readers</span>
            <span>•</span>
            <button
              type="button"
              onClick={handleLike}
              style={{
                background: stats.isLiked ? '#dbeafe' : 'rgba(255, 255, 255, 0.15)',
                color: stats.isLiked ? '#1d4ed8' : '#ffffff',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '6px',
                padding: '2px 8px',
                fontSize: '0.78rem',
                fontWeight: 700,
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px'
              }}
            >
              👍 {stats.isLiked ? 'Liked' : 'Like'} ({stats.likes})
            </button>
          </div>
        </div>
      </section>

      {/* Main Content Layout: Article Body (Expanded Width) + Permanently Fixed Sidebar */}
      <main style={{ maxWidth: '1380px', margin: '0 auto', padding: '36px 24px 80px 24px' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(0, 1fr) 370px',
          gap: '36px',
          alignItems: 'start'
        }}>
          {/* Left Column: Article Body */}
          <div style={{ minWidth: 0 }}>
            {/* Dynamic CSS for Roboto Editorial Typography & Clean Table Formatting */}
            <style dangerouslySetInnerHTML={{ __html: `
              @keyframes sectionHighlightAnim {
                0% { background-color: rgba(220, 38, 38, 0.15); border-radius: 8px; transform: scale(1.01); box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.1); }
                50% { background-color: rgba(220, 38, 38, 0.08); }
                100% { background-color: transparent; transform: scale(1); box-shadow: none; }
              }
              .section-highlight {
                animation: sectionHighlightAnim 1.4s ease-in-out;
              }
              .highlight-timeline-item {
                transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
              }
              .highlight-timeline-item:hover {
                transform: translateX(4px);
              }
              .highlight-timeline-item:hover .hl-title {
                color: #990000 !important;
              }
              
              /* Roboto Typography Scale (28px H1, 22px H2, 18px H3, 15px Body) */
              .article-content {
                font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 15.5px;
                line-height: 1.65;
                color: #334155;
              }
              .article-content h2 {
                font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 22px; /* 22px H2 */
                font-weight: 700;
                line-height: 1.35;
                color: #0A2540;
                margin: 32px 0 14px 0;
                padding-bottom: 6px;
                border-bottom: 2px solid #E2E8F0;
                scroll-margin-top: 90px;
                display: flex;
                align-items: center;
                gap: 8px;
              }
              .article-content h3 {
                font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 18px; /* 18px H3 */
                font-weight: 600;
                color: #0A2540;
                margin: 24px 0 10px 0;
              }
              .article-content p, .article-content li {
                font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 15.5px;
                line-height: 1.65;
                color: #334155;
                margin-bottom: 16px;
              }
              .article-content ul, .article-content ol {
                padding-left: 24px;
                margin-bottom: 18px;
              }
              .article-content li {
                margin-bottom: 8px;
              }
              .article-content table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 14px;
              }
              .article-content table th {
                background: #0A2540;
                color: #ffffff;
                font-weight: 700;
                padding: 12px 14px;
                border: 1px solid #0A2540;
                text-align: left;
                white-space: nowrap;
              }
              .article-content table td {
                padding: 11px 14px;
                border: 1px solid #e2e8f0;
                color: #334155;
                vertical-align: middle;
              }
              /* Keep Price & Quotas on a Single Row / Column */
              .article-content table td:nth-child(2),
              .article-content table th:nth-child(2),
              .article-content table td:nth-child(3),
              .article-content table th:nth-child(3) {
                white-space: nowrap;
              }
              .article-content table tr:hover td {
                background: #f8fafc;
              }
              .recent-item-link:hover .recent-item-title {
                color: #0176D3 !important;
              }
              
              /* Custom Scrollbar for Sticky Sidebar */
              .fixed-sidebar-container::-webkit-scrollbar {
                width: 4px;
              }
              .fixed-sidebar-container::-webkit-scrollbar-track {
                background: transparent;
              }
              .fixed-sidebar-container::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 4px;
              }
            `}} />

            {/* Main Article Body Card */}
            <article
              className="article-content"
              style={{
                background: '#ffffff',
                padding: '36px 40px',
                borderRadius: '16px',
                border: '1px solid #e2e8f0',
                boxShadow: '0 4px 18px rgba(15, 23, 42, 0.03)'
              }}
              dangerouslySetInnerHTML={{ __html: post.content }}
            />

            {/* In-Article Conversion Callout Box */}
            <div style={{
              background: 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)',
              border: '1.5px solid #bfdbfe',
              borderRadius: '16px',
              padding: '28px 32px',
              marginTop: '36px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '18px'
            }}>
              <div>
                <h3 style={{ margin: '0 0 6px 0', fontSize: '1.2rem', color: '#1e3a8a', fontWeight: 700 }}>
                  Ready to Sign Documents Legally in Australia &amp; US?
                </h3>
                <p style={{ margin: 0, fontSize: '0.92rem', color: '#3b82f6' }}>
                  Execute contracts with 100% ETA 1999 &amp; ESIGN Act compliance for just $12/user/mo (unlimited envelopes).
                </p>
              </div>
              <a
                href="https://app.ezsignature.com/login"
                style={{
                  background: '#0176D3',
                  color: '#ffffff',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  padding: '11px 22px',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  boxShadow: '0 4px 12px rgba(1, 118, 211, 0.3)',
                  whiteSpace: 'nowrap'
                }}
              >
                Start Free Trial →
              </a>
            </div>
          </div>

          {/* Right Column: PERMANENTLY FIXED SIDEBAR (Col 2/3) */}
          <aside
            className="fixed-sidebar-container"
            style={{
              position: 'sticky',
              top: '80px',
              maxHeight: 'calc(100vh - 95px)',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: '20px',
              paddingRight: '2px'
            }}
          >
            {/* 1. KEY HIGHLIGHTS TIMELINE WIDGET */}
            {post.highlights && post.highlights.length > 0 && (
              <div style={{
                borderRadius: '14px',
                overflow: 'hidden',
                boxShadow: '0 4px 16px rgba(15, 23, 42, 0.04)',
                border: '1px solid #e2e8f0',
                background: '#ffffff'
              }}>
                {/* Crimson Header Bar */}
                <div style={{
                  background: '#990000',
                  color: '#ffffff',
                  padding: '13px 18px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}>
                  <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 800, letterSpacing: '-0.01em', color: '#ffffff' }}>
                    Highlights
                  </h3>
                  <span style={{ fontSize: '0.7rem', fontWeight: 700, letterSpacing: '0.08em', color: '#ffffff', textTransform: 'uppercase' }}>
                    IN THIS ARTICLE
                  </span>
                </div>

                {/* Timeline Body */}
                <div style={{
                  padding: '16px 16px 20px',
                  fontFamily: "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif"
                }}>
                  <div style={{
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    color: '#475569',
                    marginBottom: '14px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}>
                    <span style={{ color: '#0f172a', fontWeight: 800 }}>—</span>
                    <span>{post.formattedDate || '23 August 2026'}</span>
                  </div>

                  <div style={{
                    borderLeft: '2px solid #e2e8f0',
                    marginLeft: '10px',
                    paddingLeft: '18px',
                    position: 'relative'
                  }}>
                    {post.highlights.map((hl, idx) => (
                      <div
                        key={idx}
                        onClick={(e) => scrollToSection(e, hl.id)}
                        style={{
                          position: 'relative',
                          marginBottom: idx === post.highlights.length - 1 ? '0' : '18px',
                          cursor: 'pointer'
                        }}
                        className="highlight-timeline-item"
                      >
                        <div style={{
                          position: 'absolute',
                          left: '-24px',
                          top: '3px',
                          width: '9px',
                          height: '9px',
                          borderRadius: '50%',
                          background: '#990000',
                          boxShadow: '0 0 0 2px #ffffff, 0 0 0 4px #fee2e2'
                        }} />

                        <div style={{
                          color: '#990000',
                          fontSize: '0.72rem',
                          fontWeight: 700,
                          letterSpacing: '0.03em',
                          marginBottom: '2px',
                          textTransform: 'uppercase'
                        }}>
                          {hl.time}
                        </div>

                        {hl.title && (
                          <div style={{
                            fontSize: '0.88rem',
                            fontWeight: 700,
                            color: '#0f172a',
                            lineHeight: 1.35,
                            marginBottom: '3px'
                          }} className="hl-title">
                            {hl.title}
                          </div>
                        )}

                        <div style={{
                          fontSize: '0.8rem',
                          color: '#475569',
                          lineHeight: 1.45
                        }}>
                          {hl.text}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* 2. TABLE OF CONTENTS ACCORDION */}
            {post.toc && post.toc.length > 0 && (
              <div style={{
                borderRadius: '14px',
                border: '1px solid #e2e8f0',
                background: '#ffffff',
                overflow: 'hidden',
                boxShadow: '0 4px 16px rgba(15, 23, 42, 0.04)'
              }}>
                <button
                  type="button"
                  onClick={() => setIsTocOpen(!isTocOpen)}
                  style={{
                    width: '100%',
                    padding: '13px 18px',
                    background: '#f8fafc',
                    border: 'none',
                    borderBottom: isTocOpen ? '1px solid #e2e8f0' : 'none',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                    fontFamily: "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif"
                  }}
                >
                  <span style={{ fontSize: '0.84rem', fontWeight: 700, color: '#0f172a', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                    📑 Table of Contents
                  </span>
                  <span style={{ fontSize: '0.9rem', color: '#64748b' }}>
                    {isTocOpen ? '▲' : '▼'}
                  </span>
                </button>

                {isTocOpen && (
                  <div style={{ padding: '14px 18px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {post.toc.map((item, idx) => (
                      <a
                        key={idx}
                        href={`#${item.id}`}
                        onClick={(e) => scrollToSection(e, item.id)}
                        style={{
                          fontSize: '0.84rem',
                          color: '#0176D3',
                          textDecoration: 'none',
                          fontWeight: 500,
                          lineHeight: 1.4,
                          padding: '4px 0',
                          borderBottom: idx === post.toc.length - 1 ? 'none' : '1px dashed #f1f5f9',
                          transition: 'color 0.2s ease'
                        }}
                      >
                        {item.title}
                      </a>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* 3. RECENT ARTICLES FEED */}
            <div style={{
              borderRadius: '14px',
              border: '1px solid #e2e8f0',
              background: '#ffffff',
              padding: '16px 18px',
              boxShadow: '0 4px 16px rgba(15, 23, 42, 0.04)'
            }}>
              <div style={{
                fontSize: '0.8rem',
                fontWeight: 700,
                color: '#0f172a',
                textTransform: 'uppercase',
                letterSpacing: '0.06em',
                marginBottom: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <span>📰 Recent Articles</span>
                <span style={{ fontSize: '0.68rem', color: '#16a34a', fontWeight: 700 }}>● Live</span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {recentArticles.map((ra, idx) => (
                  <Link
                    key={idx}
                    to={`/blog/${ra.slug}`}
                    className="recent-item-link"
                    style={{
                      display: 'flex',
                      gap: '12px',
                      textDecoration: 'none',
                      alignItems: 'center',
                      paddingBottom: idx === recentArticles.length - 1 ? '0' : '10px',
                      borderBottom: idx === recentArticles.length - 1 ? 'none' : '1px solid #f1f5f9'
                    }}
                  >
                    <img
                      src={ra.heroImage}
                      alt={ra.title}
                      style={{
                        width: '56px',
                        height: '46px',
                        borderRadius: '6px',
                        objectFit: 'cover',
                        flexShrink: 0
                      }}
                    />
                    <div style={{ minWidth: 0 }}>
                      <div className="recent-item-title" style={{
                        fontSize: '0.82rem',
                        fontWeight: 600,
                        color: '#0f172a',
                        lineHeight: 1.35,
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                        transition: 'color 0.2s ease'
                      }}>
                        {ra.title}
                      </div>
                      <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '2px' }}>
                        {ra.formattedDate || ra.publishedDate}
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            {/* 4. CONTACT / DIRECT SUPPORT CARD */}
            <div style={{
              background: '#0A2540',
              borderRadius: '14px',
              padding: '20px 18px',
              color: '#ffffff',
              textAlign: 'center',
              boxShadow: '0 6px 20px rgba(10, 37, 64, 0.15)'
            }}>
              <div style={{ fontSize: '0.72rem', color: '#93C5FD', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>
                DIRECT MELBOURNE SUPPORT
              </div>
              <h4 style={{ margin: '0 0 8px 0', fontSize: '1rem', fontWeight: 700, color: '#ffffff' }}>
                Speak with our Melbourne specialists
              </h4>
              <p style={{ fontSize: '0.8rem', color: '#CBD5E1', lineHeight: 1.45, margin: '0 0 14px 0' }}>
                Get custom onboarding, volume quotes, or API sandbox access in minutes.
              </p>
              <a
                href="tel:1300050099"
                style={{
                  display: 'block',
                  background: '#ffffff',
                  color: '#0A2540',
                  fontWeight: 700,
                  fontSize: '0.88rem',
                  padding: '10px',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
                }}
              >
                📞 Call 1300 050 099
              </a>
            </div>

          </aside>
        </div>
      </main>

      <Footer />
    </div>
  );
}
'''

NEW_ARTICLE_HTML_CONTENT = """      <p class="article-lead">Electronic signatures should accelerate deals and protect compliance—not hold team budgets hostage with punitive per-seat pricing and restrictive annual envelope quotas. In this honest value breakdown, we evaluate the real costs of document execution platforms in 2026.</p>

      <h2 id="honest-value">1. The Reality of Modern eSignature Pricing</h2>
      <p>For growing sales, legal, and operational teams, document management is rarely just "signing a line." It encompasses proposal generation, template management, customer collaboration, legally binding cryptographic signing, payment collection, and permanent audit archiving.</p>
      <p>While legacy market leaders like DocuSign and PandaDoc have expanded their toolkits, their entry prices often disguise substantial hidden costs—most notably restrictive envelope send limits (typically 100 envelopes per user/year on DocuSign Business Pro) and expensive mandatory seat licenses for occasional collaborators.</p>

      <h2 id="plan-breakdown">2. What Each EZ Signature Plan Includes</h2>
      <p>EZ Signature provides four tailored tiers engineered for predictable monthly budgeting with <strong>zero per-envelope penalties</strong>:</p>

      <div class="article-data-table-wrapper" style="overflow-x:auto; margin:20px 0;">
        <table class="article-data-table" style="width:100%; border-collapse:collapse; text-align:left;">
          <thead>
            <tr style="background:#0A2540; color:#ffffff;">
              <th style="padding:12px 14px; white-space:nowrap;">Plan Tier</th>
              <th style="padding:12px 14px; white-space:nowrap;">Price (Annual)</th>
              <th style="padding:12px 14px; white-space:nowrap;">Envelope Quotas</th>
              <th style="padding:12px 14px;">Key Included Features</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;"><strong>Free eSignature</strong></td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#0A2540;">$0 / mo</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap;">5 documents / mo</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Legally binding ETA/ESIGN signatures, basic audit trail, 3 templates.</td>
            </tr>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;"><strong>Starter Pro</strong></td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#0A2540;">$12 / user / mo <span style="color:#ef4444; font-weight:bold;">*</span></td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#16a34a;">Unlimited</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Drag-and-drop builder, unlimited templates, custom branding, audit certificate.</td>
            </tr>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;"><strong>Business Automation</strong></td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#0A2540;">$29 / user / mo <span style="color:#ef4444; font-weight:bold;">*</span></td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#16a34a;">Unlimited</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">CRM integrations (Salesforce, HubSpot, Pro CRM), payment collection, approval workflows.</td>
            </tr>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;"><strong>Enterprise &amp; API</strong></td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#0A2540;">Custom Volume</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#16a34a;">High-Volume API</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">Single Sign-On (SSO), REST API webhooks, dedicated account manager, custom SLA.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p style="font-size:0.82rem; color:#64748b; margin-top:-10px; margin-bottom:24px;"><em><span style="color:#ef4444; font-weight:bold;">*</span> Billed annually or month-to-month flexibility. 100% transparent pricing with zero per-envelope surcharges.</em></p>

      <h2 id="stack-costs">3. The Hidden Cost of an Independent Document Stack</h2>
      <p>When businesses piece together disparate point solutions, software costs balloon exponentially:</p>
      <ul>
        <li><strong>Document Creation:</strong> Microsoft 365 or Adobe InDesign ($25–$35/user/mo)</li>
        <li><strong>Competitor e-Signature Solutions:</strong> DocuSign Business Pro ($45/user/mo)</li>
        <li><strong>Contract Tracking &amp; CRM Sync:</strong> Add-on connector licenses ($30–$50/mo)</li>
        <li><strong>Total Stack Cost:</strong> <strong>$100–$130/user/month</strong></li>
      </ul>
      <p>Consolidating document creation, legal electronic signing, and CRM synchronization into EZ Signature reduces this monthly commitment by over <strong>65%</strong>.</p>

      <h2 id="limits-blockers">4. Envelope Limits, Overage Fees &amp; Blockers Explained</h2>
      <p>Many organizations only discover the downside of legacy e-signature providers after exceeding their contracted envelope allotment:</p>
      <div style="background:#EFF6FF; border-left:4px solid #1D4ED8; padding:16px 20px; border-radius:0 10px 10px 0; margin:20px 0;">
        <strong style="color:#1E3A8A; display:block; margin-bottom:4px; font-size:0.9rem;">⚠️ Restrictive Competitor Envelope Caps</strong>
        <p style="margin:0; font-size:0.92rem; color:#1E293B; line-height:1.55;">
          DocuSign Business Pro plans enforce an annual ceiling of 100 sent envelopes per user. Exceeding this quota triggers mandatory plan upgrades or per-envelope surcharges between $3.50 and $7.00 per document.
        </p>
      </div>
      <p>EZ Signature eliminates sending anxiety with <strong>truly unlimited envelope execution</strong> across all paid tiers.</p>

      <h2 id="roi-comparison">5. Pricing Comparison: EZ Signature vs DocuSign vs PandaDoc</h2>
      <div class="article-data-table-wrapper" style="overflow-x:auto; margin:20px 0;">
        <table class="article-data-table" style="width:100%; border-collapse:collapse; text-align:left;">
          <thead>
            <tr style="background:#0A2540; color:#ffffff;">
              <th style="padding:12px 14px; white-space:nowrap;">Feature / Tier</th>
              <th style="padding:12px 14px; white-space:nowrap;">EZ Signature (Business)</th>
              <th style="padding:12px 14px; white-space:nowrap;">DocuSign (Business Pro)</th>
              <th style="padding:12px 14px; white-space:nowrap;">PandaDoc (Business)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;">Price per User / Month</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#16a34a;">$29 <span style="color:#ef4444; font-weight:bold;">*</span></td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap;">$45</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap;">$49</td>
            </tr>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;">Annual Envelope Limit</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap; font-weight:700; color:#16a34a;">Unlimited</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap;">100 envelopes / user / yr</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; white-space:nowrap;">Unlimited</td>
            </tr>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;">Australian ETA 1999 Compliance</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:700; color:#16a34a;">✅ Native AU ISO 27001</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">✅ Yes</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">✅ Yes</td>
            </tr>
            <tr>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:600;">Native CRM Integrations</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0; font-weight:700; color:#16a34a;">✅ Included (Salesforce &amp; HubSpot)</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">❌ Extra Cost Add-On</td>
              <td style="padding:12px 14px; border-bottom:1px solid #e2e8f0;">✅ Included (Salesforce extra)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 id="verdict">6. Is EZ Signature Worth the Investment?</h2>
      <p>For small and mid-market enterprises seeking bank-grade legal security, intuitive document building, and predictable expenses without seat gouging, EZ Signature delivers an average <strong>310% ROI within the first 6 months</strong>.</p>
"""

def main():
    print("🚀 1. Writing updated BlogArticle.jsx with Roboto font, progress bar, header carousel, and sticky Col 2...")
    with open(BLOG_ARTICLE_JSX, "w", encoding="utf-8") as f:
        f.write(JSX_CONTENT)
    print("✅ BlogArticle.jsx successfully updated!")

    print("🚀 2. Updating blogPosts.js with clean single-row pricing table, red asterisks, and renamed competitor point 3...")
    with open(BLOG_POSTS_JS, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace content for esignatures-online-pricing-value-breakdown
    # Find start and end of this post's content
    pattern = r'id:\s*"esignatures-online-pricing-value-breakdown".*?content:\s*`.*?`'
    
    # Check if we can cleanly replace the content block
    if "esignatures-online-pricing-value-breakdown" in content:
        # Replace the content property
        content = re.sub(
            r'(id:\s*"esignatures-online-pricing-value-breakdown"[^`]*content:\s*`)(.*?)(`\s*\n\s*\},)',
            lambda m: m.group(1) + "\n" + NEW_ARTICLE_HTML_CONTENT + "\n    " + m.group(3),
            content,
            flags=re.DOTALL
        )
        with open(BLOG_POSTS_JS, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ blogPosts.js successfully updated with single-row pricing table & red asterisks!")

if __name__ == "__main__":
    main()
