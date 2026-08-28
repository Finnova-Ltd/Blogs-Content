#!/usr/bin/env python3
"""
GPU LivePortrait & Automatic Subtitle Rendering Microservice (FastAPI)
Deployable on RunPod, AWS EC2, or local Apple Silicon / CUDA machine.
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
import subprocess
import math

app = FastAPI(title="LivePortrait & Branded Video Renderer", version="1.0.0")

def generate_srt_file(text: str, output_srt_path: str):
    """Parses text script into timed SRT subtitles styled for video."""
    words = text.split()
    words_per_segment = 4
    words_per_minute = 150
    seconds_per_word = 60.0 / words_per_minute
    
    with open(output_srt_path, "w", encoding="utf-8") as srt:
        segment_index = 1
        current_word_pointer = 0
        total_words = len(words)
        
        while current_word_pointer < total_words:
            chunk = words[current_word_pointer : current_word_pointer + words_per_segment]
            chunk_text = " ".join(chunk)
            
            start_time = current_word_pointer * seconds_per_word
            end_time = (current_word_pointer + len(chunk)) * seconds_per_word
            
            def format_time(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                millis = int((seconds % 1) * 1000)
                return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
            
            srt.write(f"{segment_index}\n")
            srt.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            srt.write(f"{chunk_text}\n\n")
            
            segment_index += 1
            current_word_pointer += words_per_segment

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LivePortrait Video Renderer"}

@app.post("/lipsync")
async def process_lipsync(
    source_image: UploadFile = File(...), 
    driven_audio: UploadFile = File(...),
    script_text: str = Form(...),
    show_subtitles: str = Form("true"),
    logo_url: str = Form(None)
):
    workspace = "./workspace"
    os.makedirs(workspace, exist_ok=True)
    img_path = os.path.join(workspace, "target_avatar.jpg")
    audio_path = os.path.join(workspace, "input_voice.mp3")
    srt_path = os.path.join(workspace, "captions.srt")
    raw_video = os.path.join(workspace, "raw_render.mp4")
    final_output = os.path.join(workspace, "final_delivery.mp4")

    # Save uploaded chunks
    with open(img_path, "wb") as f:
        shutil.copyfileobj(source_image.file, f)
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(driven_audio.file, f)

    # 1. Check if LivePortrait or FFmpeg loop should be used
    if os.path.exists("inference.py"):
        subprocess.run([
            "python3", "inference.py",
            "--source_image", img_path,
            "--driven_audio", audio_path,
            "--output_path", raw_video
        ], check=True)
    else:
        # Fallback high-quality static/animated plate with audio loop
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", img_path, "-i", audio_path,
            "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac",
            "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", raw_video
        ], check=True)

    # 2. Add Subtitles & Branding Logo
    filter_complex_string = ""
    ffmpeg_inputs = ["-i", raw_video]

    if logo_url:
        ffmpeg_inputs.extend(["-i", logo_url])
        filter_complex_string += "[0:v][1:v]overlay=W-w-20:20"

    if show_subtitles.lower() == "true":
        generate_srt_file(script_text, srt_path)
        # Yellow bold text with black outline (TikTok / Instagram standard)
        subtitle_filter = f"subtitles={srt_path}:force_style='Fontname=Arial,Fontsize=18,PrimaryColour=&H0000FFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2,Alignment=2'"
        if filter_complex_string:
            filter_complex_string += f"[patched];[patched]{subtitle_filter}"
        else:
            filter_complex_string += subtitle_filter

    ffmpeg_command = ["ffmpeg", "-y"] + ffmpeg_inputs
    if filter_complex_string:
        ffmpeg_command.extend(["-filter_complex", filter_complex_string])
    
    ffmpeg_command.extend([
        "-codec:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-codec:a", "copy", final_output
    ])

    subprocess.run(ffmpeg_command, check=True)
    return FileResponse(final_output, media_type="video/mp4", filename="piper_avatar_video.mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
