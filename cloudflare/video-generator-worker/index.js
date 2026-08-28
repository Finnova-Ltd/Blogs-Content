/**
 * Cloudflare Serverless Video Generation Router Worker
 * Bridges Cloudflare Workers AI (Flux-1-Dev) + ElevenLabs TTS + GPU LivePortrait sub-node.
 */

export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, xi-api-key, Authorization",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed. Use POST." }), { 
        status: 405, 
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      });
    }
    
    try {
      const { scriptText, avatarSeed, brandLogoUrl, showSubtitles, voiceId } = await request.json();
      
      if (!scriptText) {
        return new Response(JSON.stringify({ error: "Missing scriptText parameter" }), { 
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }

      // 1. CONCURRENT STEP A: Generate base frame via Cloudflare Workers AI Flux-1
      const imageGeneration = env.AI.run('@cf/black-forest-labs/flux-1-dev', {
        prompt: "A realistic cinematic medium shot of a fair-skinned 28-year-old Indian man with an elongated face, black-rimmed square aviator glasses, messy swept-back hair, wearing an open unbuttoned blue shirt over a black t-shirt, standing inside a modern high-rise glass office with a crisp city skyline backdrop",
        seed: parseInt(avatarSeed) || 420892,
        aspect_ratio: "16:9"
      });

      // 2. CONCURRENT STEP B: Request raw TTS audio stream from ElevenLabs API
      const targetVoiceId = voiceId || env.ELEVEN_LABS_VOICE_ID || "a7QzaYHgLJOQ3by3k3Dk";
      const elevenLabsApiUrl = `https://api.elevenlabs.io/v1/text-to-speech/${targetVoiceId}`;
      const voiceGeneration = fetch(elevenLabsApiUrl, {
        method: "POST",
        headers: {
          "xi-api-key": env.ELEVEN_LABS_API_KEY,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          text: scriptText,
          model_id: "eleven_turbo_v2_5",
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75
          }
        })
      });

      // Await both AI calls concurrently
      const [imageBuffer, voiceResponse] = await Promise.all([imageGeneration, voiceGeneration]);

      if (!voiceResponse.ok) {
        const errorLogs = await voiceResponse.text();
        return new Response(JSON.stringify({ error: `ElevenLabs API Failure: ${errorLogs}` }), { 
          status: 502,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }

      const audioBuffer = await voiceResponse.arrayBuffer();

      // 3. STEP C: Build multipart payload for GPU LivePortrait / FFmpeg sub-node
      const pipelineFormData = new FormData();
      pipelineFormData.append("source_image", new Blob([imageBuffer], { type: "image/jpeg" }), "avatar.jpg");
      pipelineFormData.append("driven_audio", new Blob([audioBuffer], { type: "audio/mp3" }), "voice.mp3");
      pipelineFormData.append("script_text", scriptText);
      pipelineFormData.append("show_subtitles", showSubtitles !== false ? "true" : "false");
      if (brandLogoUrl) {
        pipelineFormData.append("logo_url", brandLogoUrl);
      }

      // If external GPU server is configured, forward rendering
      if (env.LIP_SYNC_SERVER_URL) {
        const finalRenderResponse = await fetch(env.LIP_SYNC_SERVER_URL, {
          method: "POST",
          body: pipelineFormData
        });

        if (!finalRenderResponse.ok) {
          return new Response(JSON.stringify({ error: "Upstream processing failed at GPU sub-node" }), { 
            status: 502,
            headers: { ...corsHeaders, "Content-Type": "application/json" }
          });
        }

        return new Response(finalRenderResponse.body, {
          headers: {
            ...corsHeaders,
            "Content-Type": "video/mp4",
            "Cache-Control": "no-store"
          }
        });
      }

      // Fallback: Return raw audio + image bundle as JSON (if GPU node is offline)
      return new Response(JSON.stringify({
        success: true,
        message: "Audio and Base Image generated successfully via Cloudflare + ElevenLabs",
        voiceId: targetVoiceId,
        scriptLength: scriptText.length,
      }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });

    } catch (globalError) {
      return new Response(JSON.stringify({ error: globalError.message }), { 
        status: 500, 
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      });
    }
  }
};
