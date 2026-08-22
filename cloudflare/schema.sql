-- Multi-Tenant Cloudflare D1 Schema for All Websites
-- Optimized for high-throughput reads, minimal storage, and zero-cost edge caching.

-- 1. Hot Articles Table (Active 0-90 Days)
CREATE TABLE IF NOT EXISTS articles_hot (
    id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,          -- 'ezmortgage', 'ezconsultants', 'procrm', 'ezsignature', etc.
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    author TEXT DEFAULT 'Editorial Staff',
    date TEXT NOT NULL,
    iso_date TEXT NOT NULL,
    read_time TEXT DEFAULT '5 min read',
    excerpt TEXT,
    content_html TEXT,              -- Optional full text (kept lean)
    image_url TEXT NOT NULL,
    views INTEGER DEFAULT 1420,
    likes INTEGER DEFAULT 118,
    status TEXT DEFAULT 'published',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(site_id, slug)
);

CREATE INDEX IF NOT EXISTS idx_articles_site_date ON articles_hot (site_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_site_cat ON articles_hot (site_id, category);

-- 2. Cold Archive Metadata Index (Pointers to R2 Storage)
CREATE TABLE IF NOT EXISTS articles_cold_index (
    id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    publish_date TEXT NOT NULL,
    r2_archive_key TEXT NOT NULL,    -- e.g. 'archives/2026/08/ezmortgage_2026_08.jsonl.gz'
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(site_id, slug)
);

CREATE INDEX IF NOT EXISTS idx_cold_site ON articles_cold_index (site_id, publish_date DESC);
