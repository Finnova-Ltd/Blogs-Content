CREATE TABLE IF NOT EXISTS chat_logs (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS leads (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  category TEXT,
  name TEXT,
  email TEXT,
  phone TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS domain_configs (
  domain TEXT PRIMARY KEY,
  category TEXT DEFAULT 'DEFAULT',
  business_name TEXT,
  phone TEXT,
  email TEXT,
  primary_color TEXT DEFAULT '#0052FF',
  plan_tier TEXT DEFAULT 'PRO',
  features TEXT DEFAULT '{"rag":true,"leadCapture":true,"imageUpload":true,"screenAwareness":true}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consent_logs (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  necessary INTEGER DEFAULT 1,
  analytics INTEGER DEFAULT 0,
  advertising INTEGER DEFAULT 0,
  gpc_detected INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
