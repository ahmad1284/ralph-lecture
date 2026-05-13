# Spec: Subtitle Generation

## Job to be Done
Produce a single SRT subtitle file for the entire video, accurately timed using word boundary data from the TTS stage.

## Output
- `output/{slug}/subtitles.srt`
- Standard SRT format, UTF-8 encoded

## Timing
- Word boundaries from `audio/section_{index:02d}_words.json` give per-word ms timestamps
- Each section's timestamps are offset by the cumulative duration of all previous sections' audio
- Audio duration per section determined by reading the mp3 file duration (use `mutagen` or `ffprobe`)

## Subtitle Chunking
- Group words into subtitle lines of 6–10 words maximum
- Never break a subtitle line mid-phrase if avoidable
- Each subtitle block: start_time → end_time of the word group
- Gap between consecutive subtitles: 50ms minimum

## SRT Format
```
1
00:00:00,000 --> 00:00:03,200
The Fourier Transform is one of the most

2
00:00:03,250 --> 00:00:06,800
beautiful ideas in all of mathematics.

3
...
```

## Style note
Subtitles will be burned into the video by the composition stage using ffmpeg `subtitles` filter. The SRT file itself has no style — styling is applied during composition (white text, black outline, bottom-centre position).

## Implementation
- `pipeline/subtitles.py`
- Takes list of word boundary JSON files and audio durations as input
- Outputs single SRT file
- Requires: `mutagen` (for audio duration) or uses ffprobe subprocess
