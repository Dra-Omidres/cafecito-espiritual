#!/usr/bin/env python3
"""Cafecito Espiritual: renderiza un video vertical reutilizable en Shorts/Reels/Stories."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def safe_file(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("Ruta fuera del repositorio")
    return path

def render(manifest_path):
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    name = data["id"]
    if not name or not all(ch.isalnum() or ch in "-_" for ch in name):
        raise ValueError("ID invalido")
    source = safe_file(data["imagen"])
    if not source.is_file() or source.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        raise ValueError("Imagen PNG/JPG inexistente")
    duration = int(data.get("duracion", 12))
    if duration < 6 or duration > 30:
        raise ValueError("Duracion fuera de rango 6-30 segundos")
    out = ROOT / "videos" / (name + ".mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 10000:
        print(f"YA EXISTE {out.relative_to(ROOT)}")
        return
    audio_value = data.get("audio", "")
    audio = None
    if audio_value:
        candidate = safe_file(audio_value)
        record = safe_file(data.get("licencia_audio", ""))
        if candidate.is_file() and record.is_file() and candidate.suffix.lower() in (".mp3", ".wav", ".m4a"):
            audio = candidate
        else:
            raise ValueError("Audio sin archivo/licencia verificados; no se renderiza")
    filt = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,boxblur=35:2[bg];"
            "[0:v]scale=1000:1600:force_original_aspect_ratio=decrease,"
            "format=rgba[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,"
            f"fade=t=in:st=0:d=0.6,fade=t=out:st={duration-0.8}:d=0.8[v]")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-loop", "1", "-framerate", "25", "-i", str(source)]
    if audio:
        cmd += ["-stream_loop", "-1", "-i", str(audio)]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    cmd += ["-filter_complex", filt, "-map", "[v]", "-map", "1:a:0",
            "-t", str(duration), "-r", "25", "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "25", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k",
            "-af", f"afade=t=in:st=0:d=0.5,afade=t=out:st={duration-1}:d=1,volume=0.16" if audio else "volume=0",
            "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=codec_name,width,height",
                    "-of", "json", str(out)], check=True)
    print(f"GENERADO {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
    data["video"] = "videos/" + name + ".mp4"
    data["estado_video"] = "renderizado"
    data["tipo"] = ["youtube_short", "instagram_story", "facebook_story", "instagram_reel", "facebook_reel"]
    report = ROOT / "videos" / (name + ".json")
    report.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    for filename in sys.argv[1:]:
        render(safe_file(filename))
