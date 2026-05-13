import json
import os
import subprocess


def _audio_duration_seconds(mp3_path: str) -> float:
    try:
        from mutagen.mp3 import MP3
        return MP3(mp3_path).info.length
    except Exception:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", mp3_path],
            capture_output=True, text=True, check=True,
        )
        streams = json.loads(result.stdout).get("streams", [])
        for s in streams:
            if "duration" in s:
                return float(s["duration"])
        raise RuntimeError(f"Cannot determine duration of {mp3_path}")


def _ms_to_srt(ms: int) -> str:
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _chunk_words(words: list[dict], max_words: int = 8) -> list[list[dict]]:
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(words[i:i + max_words])
        i += max_words
    return chunks


def generate_subtitles(out_dir: str) -> None:
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path) as f:
        script = json.load(f)

    audio_dir = os.path.join(out_dir, "audio")
    srt_path = os.path.join(out_dir, "subtitles.srt")

    subtitle_index = 1
    cumulative_ms = 0
    lines = []

    for section in script["sections"]:
        idx = section["index"]
        words_path = os.path.join(audio_dir, f"section_{idx:02d}_words.json")
        mp3_path = os.path.join(audio_dir, f"section_{idx:02d}.mp3")

        with open(words_path) as f:
            words = json.load(f)

        duration_s = _audio_duration_seconds(mp3_path)

        for chunk in _chunk_words(words):
            start_ms = cumulative_ms + chunk[0]["start_ms"]
            end_ms = cumulative_ms + chunk[-1]["end_ms"]

            if lines:
                prev_end = lines[-1]["end_ms"]
                if start_ms < prev_end + 50:
                    start_ms = prev_end + 50

            text = " ".join(w["word"] for w in chunk)
            lines.append({"index": subtitle_index, "start_ms": start_ms, "end_ms": end_ms, "text": text})
            subtitle_index += 1

        cumulative_ms += int(duration_s * 1000)

    with open(srt_path, "w", encoding="utf-8") as f:
        for entry in lines:
            f.write(f"{entry['index']}\n")
            f.write(f"{_ms_to_srt(entry['start_ms'])} --> {_ms_to_srt(entry['end_ms'])}\n")
            f.write(f"{entry['text']}\n\n")
