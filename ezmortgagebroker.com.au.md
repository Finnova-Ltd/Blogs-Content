# 🏦 EZ Mortgage Broker (`ezmortgagebroker.com.au`)
## AI Lending Specialist Video Library & Canned Responses Matrix

This document preserves the official **Video Library**, **AI Persona Setup (Friday)**, **Clickable Pre-tag Chips**, **Canned Scripts**, and **Cinematic Realism Guidelines** for `ezmortgagebroker.com.au`.

---

## 🎬 Master Video Directory

| Asset | Concept | Video URL | Target Duration |
| :--- | :--- | :--- | :--- |
| **Intro Video** | Platform Welcome & AI Greeting | [https://share.gemini.google/w0iGnx8e65Lk](https://share.gemini.google/w0iGnx8e65Lk) | ~10s |
| **Concept 1** | Broker Fees & Commissions (Transparency & Trust) | [https://share.gemini.google/JZ01AoekO0Ny](https://share.gemini.google/JZ01AoekO0Ny) | ~10–11s (28 words) |
| **Concept 2** | Borrowing Power & Speed (Action & Encouragement) | [https://share.gemini.google/98xInqAFLLrm](https://share.gemini.google/98xInqAFLLrm) | ~10s (26 words) |
| **Concept 3** | Refinancing & Savings (Solving Pain Points) | [https://share.gemini.google/Gn6TIIKibsT7](https://share.gemini.google/Gn6TIIKibsT7) | ~10s (25 words) |

---

## 📹 Video Concepts & Canned Response Specifications

### 🌟 Intro Video
* **Link**: [https://share.gemini.google/w0iGnx8e65Lk](https://share.gemini.google/w0iGnx8e65Lk)
* **Purpose**: Primary floating video avatar greeting and hero assistant stage greeting for visitors landing on `ezmortgagebroker.com.au`.

---

### 💳 Concept 1: Broker Fees & Commissions (Transparency & Trust)
* **Video Link**: [https://share.gemini.google/JZ01AoekO0Ny](https://share.gemini.google/JZ01AoekO0Ny)
* **Clickable Pre-tag Chip**: `💳 How do your fees and commissions work?`
* **Target Duration**: ~10–11 seconds (28 words)
* **Script**:
  > *"We're compensated via lender commissions, though a fee may apply depending on your loan's complexity. Everything is disclosed upfront, and we're legally bound to act in your best interests!"*
* **Camera Style & Realism Setup**:
  * **Shot Composition**: Medium close-up (chest-to-head) framed with plenty of headroom.
  * **Camera Movement**: Subtle, organic push-in (slow dolly zoom) of about 5–8% toward the face as he delivers the line about transparency, creating intimacy and trust.
  * **Lighting & Atmosphere**: Soft natural key light from the side window with high-rise buildings visible in the background; shallow depth-of-field (bokeh) so the background plants and EZ Mortgage Broker glass logo look cinematic and high-end.
  * **Talent Movement**: Friendly nod at the start, engaging direct eye-contact with the camera lens, subtle open-hand gesture when mentioning *"everything is disclosed upfront"*.

---

### 📈 Concept 2: Borrowing Power & Speed (Action & Encouragement)
* **Video Link**: [https://share.gemini.google/98xInqAFLLrm](https://share.gemini.google/98xInqAFLLrm)
* **Clickable Pre-tag Chip**: `📈 How much can I borrow, and how fast is approval?`
* **Target Duration**: ~10 seconds (26 words)
* **Script**:
  > *"Every lender assesses borrowing capacity differently! We compare multiple lenders to maximise your borrowing power and secure fast loan approvals. Ready to see what you qualify for?"*
* **Camera Style & Realism Setup**:
  * **Shot Composition**: Medium shot (waist-up) with Friday standing in a modern corner office.
  * **Camera Movement**: Slight conversational parallax / slow subtle pan from left to center, locking on him when asking the closing question.
  * **Lighting & Atmosphere**: Clean, bright corporate daylight; sharp focal plane on his glasses and facial features.
  * **Talent Movement**: Confident posture, natural blink rate, subtle tilt of the head on *"how fast is approval"*, inviting warm smile on the closing call-to-action.

---

### 🔄 Concept 3: Refinancing & Savings (Solving Pain Points)
* **Video Link**: [https://share.gemini.google/Gn6TIIKibsT7](https://share.gemini.google/Gn6TIIKibsT7)
* **Clickable Pre-tag Chip**: `🔄 Could I be saving money on my current mortgage?`
* **Target Duration**: ~10 seconds (25 words)
* **Script**:
  > *"If you haven't reviewed your rate recently, you might be overpaying. We compare multiple lenders to find lower rates and trim your repayments. Let's run a quick health check!"*
* **Camera Style & Realism Setup**:
  * **Shot Composition**: Close-up / medium-close portrait shot.
  * **Camera Movement**: Static, tripod-locked camera with a subtle rack focus effect: starts slightly focused on the EZ Mortgage Broker emblem on the glass window/lapel and snaps cleanly into sharp focus on Friday’s eyes as he begins speaking.
  * **Lighting & Atmosphere**: Premium executive studio fill light, soft overcast daylight reflecting subtly off the window behind him.
  * **Talent Movement**: Empathetic micro-expressions, gentle lean-in toward the camera on *"overpaying"*, nodding warmly at *"let's run a quick health check"*.

---

## 🤖 Chat & Video Assistant Integration Architecture

1. **`js/widget.js` (Omni / Piper Video Chat Assistant)**:
   * Displays the 3 clickable pre-tag chips directly in the suggestions tray (`.piper-prompts-list`).
   * When any chip is selected (or when matched by user query keywords: *fees, commissions, borrowing power, approval speed, refinancing, lower rates*):
     - Displays the authoritative scripted response.
     - Embeds a rich video response card with the verified video URL.
     - Automatically switches the hero video stage to the selected concept video.
2. **`js/piper-video-assistant.js` (Floating Video Bubble & Card)**:
   * Initialized with the Intro Video.
   * Action pills allow quick selection of each concept.
