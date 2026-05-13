# Spec: Video Composition

## Job to be Done
Combine all scene videos, per-section audio, and subtitles into a single final MP4.

## Process

### Step 1: Pair scenes with audio
For each section index, pair:
- `scenes/scene_{index:02d}.mp4` (video, no audio)
- `audio/section_{index:02d}.mp3` (audio)

Merge each pair into a single clip using ffmpeg:
- If scene video is shorter than audio: hold last frame (ffmpeg `-loop` or pad video)
- If scene video is longer than audio: trim video to audio length
- Output: `scenes/clip_{index:02d}.mp4` (video + audio merged)

### Step 2: Concatenate clips
Use ffmpeg concat demuxer to join all clips in order.
Output: `output/{slug}/combined.mp4`

### Step 3: Burn subtitles
Use ffmpeg `subtitles` filter on `combined.mp4` with `subtitles.srt`.

Subtitle style (passed via ffmpeg `force_style`):
```
FontName=Arial,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,Bold=1,Outline=2,Shadow=1,Alignment=2,MarginV=30
```

Output: `output/{slug}/final.mp4`

### Step 4: Cleanup
Remove intermediate files:
- `scenes/clip_*.mp4`
- `combined.mp4`

Keep for debugging (do not delete):
- `scenes/scene_*.mp4`
- `audio/section_*.mp3`
- `audio/section_*_words.json`
- `script.json`
- `subtitles.srt`

## Final Output
- `output/{slug}/final.mp4`
- H.264 video, AAC audio
- 1920x1080, 30fps
- Playable in any standard video player

## Implementation
- `pipeline/composition.py`
- All ffmpeg calls via `subprocess.run` with error checking
- Requires: `ffmpeg` in PATH
