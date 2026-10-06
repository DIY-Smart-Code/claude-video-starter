#!/usr/bin/env python3
"""Turn videos/<slug>/script.txt into narration.wav + transcript.json with ElevenLabs.

One API call returns the audio and the start time of every character. This script
groups the characters into words and writes them in the same transcript.json shape
that `npx hyperframes transcribe` writes, so the rest of the workflow does not care
which voice route you used.

Usage:
    python scripts/tts.py videos/<slug>
    python scripts/tts.py videos/<slug> --model eleven_v4

Needs ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID in .env (see .env.example).
--voice <voice_id> overrides the .env voice for one run; the workflow never needs it.

Optional .env voice settings, sent only when set: ELEVENLABS_STABILITY,
ELEVENLABS_SIMILARITY_BOOST, ELEVENLABS_STYLE, ELEVENLABS_USE_SPEAKER_BOOST, ELEVENLABS_SPEED
(ELEVENLABS_SPEED_SHORTS instead when the video's STORYBOARD.md format is portrait), and
ELEVENLABS_PRONUNCIATION_DICT_ID + ELEVENLABS_PRONUNCIATION_DICT_VERSION_ID.
Python 3.8+, standard library only.
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format={fmt}"
SAMPLE_RATE = 24000  # pcm_24000: raw 16-bit mono PCM, written straight into a WAV file


def load_env(repo_root: Path) -> None:
    """Read KEY=VALUE lines from .env without overriding real environment variables."""
    env_file = repo_root / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = re.sub(r"\s+#.*$", "", value)  # inline comment: KEY=1.0   # note
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def is_portrait(video_dir: Path) -> bool:
    """True when STORYBOARD.md's `format: WxH` is taller than wide (Shorts / Reels / TikTok)."""
    storyboard = video_dir / "STORYBOARD.md"
    if not storyboard.exists():
        return False
    match = re.search(r"^format:\s*(\d+)x(\d+)", storyboard.read_text(encoding="utf-8"), re.M)
    return bool(match) and int(match.group(2)) > int(match.group(1))


def voice_settings(portrait: bool) -> dict:
    """The .env voice settings that are set, in the shape the ElevenLabs API expects."""
    settings = {}
    for key, env in (
        ("stability", "ELEVENLABS_STABILITY"),
        ("similarity_boost", "ELEVENLABS_SIMILARITY_BOOST"),
        ("style", "ELEVENLABS_STYLE"),
    ):
        if os.environ.get(env):
            settings[key] = float(os.environ[env])
    if os.environ.get("ELEVENLABS_USE_SPEAKER_BOOST"):
        settings["use_speaker_boost"] = os.environ["ELEVENLABS_USE_SPEAKER_BOOST"].lower() == "true"
    speed = os.environ.get("ELEVENLABS_SPEED_SHORTS") if portrait else None
    speed = speed or os.environ.get("ELEVENLABS_SPEED")
    if speed:
        settings["speed"] = float(speed)
    return settings


def pronunciation_locators() -> list:
    dict_id = os.environ.get("ELEVENLABS_PRONUNCIATION_DICT_ID")
    version_id = os.environ.get("ELEVENLABS_PRONUNCIATION_DICT_VERSION_ID")
    if not (dict_id and version_id):
        return []
    return [{"pronunciation_dictionary_id": dict_id, "version_id": version_id}]


def synthesize(text: str, voice: str, model: str, api_key: str, settings: dict, locators: list) -> dict:
    payload = {"text": text, "model_id": model}
    if settings:
        payload["voice_settings"] = settings
    if locators:
        payload["pronunciation_dictionary_locators"] = locators
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API.format(voice=voice, fmt=f"pcm_{SAMPLE_RATE}"),
        data=body,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        sys.exit(f"ElevenLabs returned {err.code}: {detail}")


def words_from_alignment(alignment: dict) -> list:
    """Group character timings into words: [{text, start, end, id}]."""
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    words, current = [], None
    for ch, start, end in zip(chars, starts, ends):
        if ch.isspace():
            if current:
                words.append(current)
                current = None
            continue
        if current is None:
            current = {"text": ch, "start": round(start, 3), "end": round(end, 3)}
        else:
            current["text"] += ch
            current["end"] = round(end, 3)
    if current:
        words.append(current)
    for i, word in enumerate(words):
        word["id"] = f"w{i}"
    return words


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    load_env(repo_root)

    parser = argparse.ArgumentParser(description="ElevenLabs narration + word timings")
    parser.add_argument("video_dir", help="the video folder, e.g. videos/my-explainer")
    parser.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    parser.add_argument("--model", default=os.environ.get("ELEVENLABS_MODEL_ID", "eleven_v4"))
    args = parser.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY is missing. Copy .env.example to .env and fill it in.")
    if not args.voice:
        sys.exit("ELEVENLABS_VOICE_ID is missing. Add it to .env or pass --voice.")

    video_dir = Path(args.video_dir)
    script = video_dir / "script.txt"
    if not script.exists():
        sys.exit(f"No script found at {script}")
    text = script.read_text(encoding="utf-8").strip()

    settings = voice_settings(is_portrait(video_dir))
    locators = pronunciation_locators()
    result = synthesize(text, args.voice, args.model, api_key, settings, locators)
    pcm = base64.b64decode(result["audio_base64"])
    with wave.open(str(video_dir / "narration.wav"), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm)

    words = words_from_alignment(result["alignment"])
    (video_dir / "transcript.json").write_text(json.dumps(words, indent=2), encoding="utf-8")

    seconds = len(pcm) / (2 * SAMPLE_RATE)
    print(f"narration.wav    {seconds:.1f}s")
    print(f"transcript.json  {len(words)} words")
    print(f"voice settings   {json.dumps(settings) if settings else 'voice defaults'}")
    if locators:
        print("pronunciation    dictionary from .env")


if __name__ == "__main__":
    main()
