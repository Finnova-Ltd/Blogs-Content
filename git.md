# 🚀 State-of-the-Art AI Voice & Video Repositories: Architectural Analysis & Learnings

This document benchmarks 14 leading open-source repositories across **AI Speech Synthesis (TTS)**, **Zero-Shot Voice Cloning**, **Long Video Generation**, and **Automated Video Pipelines**, extracting key architectural patterns to upgrade our automated content generation, Cloudflare AI pipeline, and ElevenLabs credit efficiency.

---

## 📊 Comparative Analysis Matrix

| Repository | Category / Type | Core Architecture & Technology | Key Capabilities & Strengths | Actionable Learnings for Our Platform |
| :--- | :--- | :--- | :--- | :--- |
| **[PKU-YuanGroup/Helios](https://github.com/PKU-YuanGroup/Helios)** | Real-Time Long Video Synthesis | **14B Parameter Autoregressive DiT (33 frames/chunk)** | Real-time minute-scale video generation at 19.5 FPS on H100; Text-to-Video (T2V), Image-to-Video (I2V), and Video-to-Video (V2V) without temporal drift. | • **I2V Presenter Animation**: Animate high-res broker avatar portraits into continuous 60-second video presentations without character warping.<br>• Generates minute-scale long-form social shorts without 5-second cutoffs. |
| **[gyoridavid/short-video-maker](https://github.com/gyoridavid/short-video-maker)** | Agentic Short Video Maker | **Model Context Protocol (MCP) + REST API** | Automated 9:16 vertical short creation for TikTok, IG Reels, and YouTube Shorts; triggers directly via AI agent tool calls. | • **MCP Agent Integration**: Expose video generation as an MCP tool directly in Antigravity/IDE or Cloudflare Agent, generating video immediately when a blog is published.<br>• Automated subtitle timing and 9:16 aspect ratio framing. |
| **[lcy362/agnes-video-generator](https://github.com/lcy362/agnes-video-generator)** | Multi-Scene Video & Avatar Studio | **Self-Hosted Agnes AI WebUI + Digital Anchor Overlay** | Multi-scene narrative orchestration (Intro ➔ Body Insights ➔ Outro), digital anchor overlay with chroma key compositing, audio-subtitle sync. | • **Multi-Scene Pacing**: Segment mortgage/finance blogs into dynamic 3-scene storyboards (Scene 1: Hook with b-roll, Scene 2: 3 key rate data points, Scene 3: Broker avatar CTA).<br>• Clean digital anchor compositing. |
| **[naqashafzal/AI-Content-Studio](https://github.com/naqashafzal/AI-Content-Studio)** | Autonomous Content Studio | **End-to-End Hands-Free Pipeline + Auto-Uploader** | Autonomous topic discovery, script generation, ElevenLabs/Edge voiceover, Pexels/Pixabay B-roll scraping, MoviePy stitching, and YouTube Data API v3 uploader. | • **Automated B-Roll Scraper**: Extract mortgage/banking keywords to fetch free 4K vertical clips from Pexels/Pixabay at $0 cost.<br>• Hands-free automated publishing to YouTube Shorts with SEO tags and descriptions. |
| **[anil-matcha/open-generative-ai](https://github.com/anil-matcha/open-generative-ai)** | Unified Open-Source Studio | **Multi-Model Orchestrator (600+ Models)** | Self-hosted alternative to InVideo/Runway; aggregates Flux, Kling, Sora-compatible APIs, ElevenLabs, Kokoro, and Whisper with zero content filtering. | • **Model Failover Router**: Tier 1 (ElevenLabs Pro) for premium broker voiceovers ➔ Tier 2 ($0 Cloudflare Workers AI / Kokoro) if quota runs low.<br>• Unified asset and prompt management across multiple brands. |
| **[itsjwill/vanta](https://github.com/itsjwill/vanta)** | Full AI Video Engine | **Remotion + React Canvas + Local Multi-Model Aggregator** | Aggregates 40+ models for talking-head avatars, dynamic animated captions, timeline transitions, and text-to-video without external API costs. | • Adopt code-driven programmatic video rendering (like Remotion / Pillow frame sequencing).<br>• Decouple scene generation into timeline blocks (Hook ➔ 3 Insights ➔ Presenter ➔ CTA). |
| **[OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM)** | Next-Gen Multilingual TTS | **Tokenizer-Free Diffusion Autoregressive Architecture** | Supports 30+ languages, creative voice design, studio-fidelity voice cloning, and continuous acoustic modeling without token discretization artifacts. | • Integrate continuous acoustic representations for smoother Australian English prosody.<br>• Use token-free audio streaming for instantaneous video narration synthesis. |
| **[resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)** | Expressive Voice Agent TTS | **Llama-Based Backbone + Paralinguistic Markers** | High-throughput speech synthesis with native support for expressive speech tags (e.g., `[laugh]`, `[sigh]`, `[whisper]`, `[emphasis]`). | • Inject paralinguistic tone markers into our LLM article-to-script prompts for highly engaging human-like voiceovers.<br>• Implement OpenAI-compatible TTS streaming proxy endpoints. |
| **[SWivid/F5-TTS](https://github.com/SWivid/F5-TTS)** | Zero-Shot Flow-Matching TTS | **Diffusion Transformer (DiT) + Continuous Flow Matching** | Non-autoregressive, blazing-fast, highly natural speech generation with zero-shot reference speaker cloning in < 3 seconds of audio. | • Replace legacy autoregressive synthesis with flow-matching DiT for sub-second voice generation.<br>• Perfect for real-time video batching across 4 brands simultaneously. |
| **[hexgrad/kokoro](https://github.com/hexgrad/kokoro)** | Ultra-Lightweight TTS (82M) | **StyleTTS 2 + Discriminator-Guided Latent Synthesis** | Featherweight (82M parameters), tops global TTS leaderboards, ultra-fast CPU inference on standard laptops and serverless edges without GPU requirements. | • Deploy Kokoro directly on Cloudflare Workers / lightweight edge runners for $0 GPU cost.<br>• Generate high-fidelity studio voiceovers in milliseconds directly on edge workers. |
| **[myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice)** | Granular Tone & Style Cloner | **Decoupled Tone Color Converter + Style Encoder** | Clones reference speaker tone color with short audio; allows independent granular control over emotion, accent, rhythm, pitch, and speed. | • Decouple voice identity from language/accent: Clone Robin Bakshi / brand persona voices while maintaining native Australian English accents across all brands. |
| **[AliRash3ed/VUZA](https://github.com/AliRash3ed/VUZA-Free-AI-Video-Creator-and-Pinterest-Video-Scraper)** | Faceless Video Generator | **Automated B-Roll Scraper + Dynamic Caption Burner + FFmpeg** | End-to-end automated pipeline creating high-retention faceless social shorts from blog posts, scraping high-engagement stock visuals automatically. | • Automate topic-based Pexels/Unsplash B-roll video caching matching blog article keywords.<br>• Layer kinetic caption animations over stock b-roll for non-avatar shorts. |
| **[SainathPattipati/ai-video-pipeline](https://github.com/SainathPattipati/ai-video-generation-pipeline)** | End-to-End Storyboard Pipeline | **Automated Script-to-Storyboard + Multi-Model Dispatcher** | Preserves consistent character keyframes across scenes, automates prompt generation for Kling/Runway, and orchestrates video stitching. | • Implement structured storyboarding (Scene 1: Hook, Scene 2: Problem, Scene 3: Solution, Scene 4: Contact).<br>• Enforce visual brand asset consistency across generated video layers. |
| **[RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)** | Few-Shot Voice Cloning & TTS | **GPT Semantic Predictor + VITS Acoustic Generator** | SOTA voice conversion and zero-shot TTS with only 1 minute of sample voice training; includes automated dataset segmentation & WebUI. | • Train custom 1-minute voice models for each brand executive (PRO CRM, EZ Mortgage, EZ Consultants, EZ Signature) for hyper-realistic brand voice consistency. |

---

## 🎯 High-Impact Features to Improve Our AI Video Generation

### 1. Hybrid Cost-Optimization Engine: ElevenLabs + Cloudflare ($0 Fallback)
* **Tier 1 (ElevenLabs Pro - High Impact)**:
  - We currently have **597,873 characters remaining** out of 610,000 monthly credits (~98% available).
  - Use ElevenLabs for **customer-facing high-converting videos**:
    - EZ Mortgage Broker: Voice ID `Dh68koMHNSYl8A1jH9Je` (Warm, authoritative Australian mortgage advisor).
    - Finnova: Voice ID `7xOqQceOZC5dhvkaqKtD` (Empathetic, clear community narrator).
  - Script optimization: Cap short video scripts at **75–90 words** (~450 characters). At 450 characters per video, our remaining credits can produce over **1,328 full studio-grade videos** this billing cycle!
* **Tier 2 (Cloudflare Workers AI + Edge-TTS - Unlimited Free Fallback)**:
  - When batching high-volume daily RSS news summaries, use Cloudflare Workers AI (`@cf/meta/llama-3.3-70b-instruct`) for script writing (free within 10,000 daily neurons).
  - Use Microsoft Edge Neural TTS (`en-AU-WilliamNeural` / `en-AU-NatashaNeural`) or Kokoro 82M for $0.00 unlimited voice synthesis.

### 2. Multi-Scene Narrative Architecture (Learned from Agnes & Short-Video-Maker)
* Never generate a flat single-frame video. Structure every 30–60s video into 3 dynamic scenes:
  1. **Scene 1 (0–5s - Hook)**: High-energy kinetic text + 4K free B-roll (Melbourne cityscape, home auction, keys).
  2. **Scene 2 (5–25s - Core Insights)**: 3 animated data cards with financial takeaways (e.g., "30+ Lenders", "81% Broker Share", "Save 0.45% on Refinance").
  3. **Scene 3 (25–35s - Presenter & CTA)**: Executive Presenter (Robin Bakshi or female broker avatar) delivering the closing advice with clickable phone/domain badge.

### 3. Agentic MCP Integration (Learned from Short-Video-Maker)
* Build an MCP tool callable by Antigravity and our Cloudflare Agent:
  - Input: Article slug or title.
  - Action: Automatically extracts keywords, fetches stock clips from Pexels, calls ElevenLabs with the brand voice ID, burns styled word-by-word subtitles, and outputs a 1080x1920 MP4 ready for YouTube Shorts / Reels.

### 4. Continuous Long-Video Generation (Learned from Helios)
* Use autoregressive chunk generation patterns (like Helios) when generating multi-minute webinars, podcast snippets, or complete loan comparison walkthroughs, preventing visual drift in the presenter avatar.

---

## 📈 Daily AI Credits & Quota Tracking System

We have implemented an automated tracker script [`scripts/track_ai_credits.py`](file:///Volumes/Samsung%20SSD%202TB/03.%20Documents/GitHub/Blogs-Content/scripts/track_ai_credits.py) that queries both ElevenLabs and Cloudflare APIs in real time with strict Australian timezone formatting (`Australia/Melbourne`).

### How to Run:
```bash
python3 scripts/track_ai_credits.py
```

### Current Live Status:
* **ElevenLabs**:
  - **Plan Tier**: PRO
  - **Remaining Credits**: **597,873 characters** (12,127 used out of 610,000 limit)
  - **Health**: 98.0% remaining
  - **Next Reset**: 2026-09-29 07:39:32 AEST
* **Cloudflare**:
  - **Plan Tier**: Free Plan with Enterprise Anycast Edge
  - **Requests Today**: 2,391 / 100,000 daily limit (97,609 remaining today)
  - **Workers AI**: 10,000 Neurons / Day allowance
  - **Cost**: $0.00 AUD (Zero-cost target maintained)
