# Spec: Text-to-Speech

## Job to be Done
Convert each section's narration text to audio. Capture word-level timestamps for subtitle generation. Use a natural-sounding English neural voice.

## Voice Selection

### Curated voice list (all neural, all natural-sounding)
```
en-US-AriaNeural       # Warm, conversational American
en-US-GuyNeural        # Calm, clear American male
en-GB-SoniaNeural      # Crisp British female
en-GB-RyanNeural       # Measured British male
en-AU-NatashaNeural    # Clear Australian female
en-AU-WilliamNeural    # Steady Australian male
en-CA-ClaraNeural      # Neutral Canadian female
en-IE-EmilyNeural      # Soft Irish female
en-NZ-MitchellNeural   # New Zealand male
en-IN-NeerjaNeural     # Indian English female
```

### Selection logic
- `--voice <name>`: use exactly that voice
- `--random-voice` or default: pick randomly from curated list at runtime
- Selected voice is logged to stdout: `Voice: en-GB-SoniaNeural`
- Same voice used for all sections in one run

## Output per section
- Audio: `output/{slug}/audio/section_{index:02d}.mp3`
- Word boundaries: `output/{slug}/audio/section_{index:02d}_words.json`

### Word boundaries JSON format
```json
[
  { "word": "The", "start_ms": 0, "end_ms": 180 },
  { "word": "Fourier", "start_ms": 200, "end_ms": 480 },
  ...
]
```

## Implementation
- Uses `edge-tts` Python library (async)
- `edge_tts.Communicate` with `word_boundary` events captured
- Run sections sequentially
- Rate: default edge-tts rate (natural pacing)
- Pitch: default
- After generation, verify audio file exists and is non-empty
- Requires: `edge-tts`, `ffmpeg` (for mp3 conversion if needed)
